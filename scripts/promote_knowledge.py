# -*- coding: utf-8 -*-
"""M41: 세션 로컬 staging → 글로벌 domain/ 결정론적 승격 스크립트.

배경 (옵션 A — 멀티 세션 충돌 해소):
  Curator는 글로벌을 직접 수정하지 않고 {프로젝트}/_curator-staging/gd-*.md 에
  승격 번들을 작성한다. 사용자 승인 후 Mickey가 본 스크립트를 실행하면,
  글로벌 쓰기는 "락으로 직렬화된 짧은 원자적 승격 순간"에만 발생한다.
  락 규율을 LLM 프롬프트가 아닌 코드로 강제한다 (LLM 결정론적 하이브리드 패턴).

승격 번들(gd-*.md) 형식:
  ## Meta               : Key: value 줄 (Mode/Entry-Path/Source/Base-Hash)
  <<<ENTRY-BODY ... ENTRY-BODY>>>  : entry 파일 본문 (내부 ``` 펜스와 충돌 없는 마커)
  ## Graph Node Row     : GRAPH.md Nodes 표에 넣을 행 1개
  ## Graph Edge Rows    : GRAPH.md Edges 표에 넣을 행 0개+
  ## Index Row          : domain/INDEX.md Domain Map 표에 넣을 행 1개
  ## Backlink Row       : {프로젝트}/common_knowledge/INDEX.md Domain Links 행 (선택)

동작 보장:
  - 락: ~/.kiro/mickey/.promote.lock/ (mkdir 원자성 + owner.json + stale 10분 타임아웃)
  - 백업: 수정 전 GRAPH/INDEX/entry를 .promote-backups/<ts>-<owner>/ 에 보관
  - 무결성: 승격 후 병합 dangling 검사 (m40_dangling_check 시맨틱) — FAIL 시 자동 롤백
  - 충돌: Mode=new 인데 노드/파일 기존재, Mode=augment 인데 Base-Hash 불일치 → 해당
    번들만 CONFLICT 스킵 (staging 보존, 재큐레이션 유도) — 낙관적 동시성 제어
  - 리포트: stdout + staging 디렉토리에 파일 리다이렉트 (adaptive #14)
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── 상수 ──────────────────────────────────────────────────────────
LOCK_STALE_SECONDS = 600          # 이 시간 지난 락은 비정상 종료 잔여물로 간주
ENTRY_BODY_OPEN = "<<<ENTRY-BODY"
ENTRY_BODY_CLOSE = "ENTRY-BODY>>>"


def global_root() -> Path:
    """글로벌 지식 루트. 테스트에서 env로 리다이렉트 가능 (installer-seed-semantics)."""
    env = os.environ.get("MICKEY_GLOBAL_ROOT")
    return Path(env) if env else Path.home() / ".kiro" / "mickey"


# ── 승격 번들 파싱 ────────────────────────────────────────────────
@dataclass
class Bundle:
    """gd-*.md 한 개가 담는 승격 정보."""
    path: Path                      # staging 파일 자신
    mode: str = "new"               # new | augment
    entry_path: str = ""            # 글로벌 domain/ 기준 상대 경로 (entries/[id].md)
    source: str = ""                # "<project> Mickey N"
    base_hash: str = ""             # augment 전제: 큐레이션 시점 entry sha256
    entry_body: str = ""
    node_row: str = ""
    edge_rows: list = field(default_factory=list)
    index_row: str = ""
    backlink_row: str = ""

    def entry_id(self) -> str:
        return Path(self.entry_path).stem


def parse_bundle(path: Path) -> Bundle:
    """번들 파일을 섹션 단위로 파싱. 형식 위반은 ValueError로 즉시 실패."""
    text = path.read_text(encoding="utf-8")
    b = Bundle(path=path)

    # entry 본문: heredoc 마커 사이 (내부에 ``` 펜스가 있어도 안전)
    m = re.search(
        rf"^{re.escape(ENTRY_BODY_OPEN)}\n(.*?)\n{re.escape(ENTRY_BODY_CLOSE)}\s*$",
        text, re.DOTALL | re.MULTILINE)
    if not m:
        raise ValueError(f"{path.name}: ENTRY-BODY 마커 없음")
    b.entry_body = m.group(1).strip() + "\n"

    # 섹션별 라인 수집 (## 헤딩 기준)
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section == "Meta":
            kv = re.match(r"^([A-Za-z-]+):\s*(.+)$", line.strip())
            if kv:
                key, val = kv.group(1).lower(), kv.group(2).strip()
                if key == "mode":
                    b.mode = val
                elif key == "entry-path":
                    b.entry_path = val
                elif key == "source":
                    b.source = val
                elif key == "base-hash":
                    b.base_hash = val
        elif line.strip().startswith("|") and not _is_separator_row(line):
            if section == "Graph Node Row" and not b.node_row:
                b.node_row = line.rstrip()
            elif section == "Graph Edge Rows":
                b.edge_rows.append(line.rstrip())
            elif section == "Index Row" and not b.index_row:
                b.index_row = line.rstrip()
            elif section == "Backlink Row" and not b.backlink_row:
                b.backlink_row = line.rstrip()

    # 필수 필드 검증
    if b.mode not in ("new", "augment"):
        raise ValueError(f"{path.name}: Mode는 new|augment ({b.mode!r})")
    for name, val in (("Entry-Path", b.entry_path), ("Source", b.source),
                      ("Graph Node Row", b.node_row), ("Index Row", b.index_row)):
        if not val:
            raise ValueError(f"{path.name}: {name} 누락")
    if b.mode == "augment" and not b.base_hash:
        raise ValueError(f"{path.name}: augment는 Base-Hash 필수")
    if not b.entry_path.startswith("entries/") or ".." in b.entry_path:
        raise ValueError(f"{path.name}: Entry-Path는 entries/ 하위만 ({b.entry_path!r})")
    return b


def _is_separator_row(line: str) -> bool:
    """표 구분선(|---|---|) 여부."""
    return bool(re.match(r"^\|[\s\-|]+\|\s*$", line.strip()))


# ── 마크다운 표 조작 (섹션 한정, 결정론적) ────────────────────────
def section_bounds(lines: list, title: str):
    """'## title' 섹션의 (시작, 다음 헤딩) 라인 인덱스. 없으면 ValueError."""
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == f"## {title}":
            start = i
        elif start is not None and ln.startswith("## "):
            return start, i
    if start is None:
        raise ValueError(f"섹션 없음: ## {title}")
    return start, len(lines)


def insert_rows(text: str, title: str, rows: list) -> str:
    """섹션 내 마지막 표 행 뒤에 rows 삽입 (표 중간 공백 라인 허용)."""
    lines = text.splitlines()
    start, end = section_bounds(lines, title)
    last_pipe = max((i for i in range(start, end) if lines[i].strip().startswith("|")),
                    default=None)
    if last_pipe is None:
        raise ValueError(f"## {title} 섹션에 표 없음")
    return "\n".join(lines[:last_pipe + 1] + rows + lines[last_pipe + 1:]) + (
        "\n" if text.endswith("\n") else "")


def replace_row(text: str, title: str, match_key: str, new_row: str) -> str:
    """섹션 내에서 첫 셀이 match_key인 행을 교체. 없으면 ValueError."""
    lines = text.splitlines()
    start, end = section_bounds(lines, title)
    for i in range(start, end):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if lines[i].strip().startswith("|") and cells and cells[0] == match_key:
            lines[i] = new_row
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    raise ValueError(f"## {title} 에 행 없음: {match_key}")


def set_last_updated(text: str, stamp: str) -> str:
    """## Last Updated 섹션의 내용 줄을 교체."""
    lines = text.splitlines()
    start, end = section_bounds(lines, "Last Updated")
    body = [i for i in range(start + 1, end) if lines[i].strip()]
    if body:
        lines[body[0]] = stamp
        for i in body[1:]:
            lines[i] = ""
    else:
        lines.insert(start + 1, stamp)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def node_ids(graph_text: str) -> set:
    """GRAPH.md Nodes 표의 기존 노드 ID 집합."""
    lines = graph_text.splitlines()
    start, end = section_bounds(lines, "Nodes")
    ids = set()
    for i in range(start, end):
        ln = lines[i].strip()
        if ln.startswith("|") and not _is_separator_row(ln):
            first = ln.strip("|").split("|")[0].strip()
            if first and first != "ID":
                ids.add(first)
    return ids


# ── 락 (mkdir 원자성) ─────────────────────────────────────────────
def acquire_lock(root: Path, owner: str) -> Path:
    """글로벌 승격 락 획득. stale 락은 1회 강제 해제 후 재시도. 실패 시 RuntimeError."""
    lock = root / ".promote.lock"
    for attempt in (1, 2):
        try:
            lock.mkdir()  # 원자적: 이미 있으면 FileExistsError
            (lock / "owner.json").write_text(json.dumps({
                "owner": owner, "pid": os.getpid(),
                "acquired_at": datetime.now().isoformat(timespec="seconds"),
            }, ensure_ascii=False), encoding="utf-8")
            return lock
        except FileExistsError:
            info = _lock_owner_info(lock)
            age = time.time() - lock.stat().st_mtime
            if age > LOCK_STALE_SECONDS and attempt == 1:
                shutil.rmtree(lock, ignore_errors=True)  # 비정상 종료 잔여 락 회수
                continue
            raise RuntimeError(
                f"락 사용 중 (보유자: {info}, 경과 {int(age)}s) — 잠시 후 재시도")
    raise RuntimeError("락 획득 실패")


def _lock_owner_info(lock: Path) -> str:
    try:
        return json.loads((lock / "owner.json").read_text(encoding="utf-8")).get("owner", "?")
    except Exception:
        return "unknown"


def release_lock(lock: Path):
    shutil.rmtree(lock, ignore_errors=True)


# ── 무결성 검증 (m40_dangling_check 병합 시맨틱 재사용) ───────────
def integrity_check(domain: Path) -> list:
    """상위+하위 GRAPH 병합 후 불변 조건 위반 목록 반환 (비면 PASS)."""
    def parse(text):
        nodes, edges, sec = {}, [], None
        for line in text.splitlines():
            if line.startswith("## "):
                sec = line.strip()
                continue
            if not line.strip().startswith("|") or _is_separator_row(line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if sec == "## Nodes" and len(cells) >= 5 and cells[0] != "ID":
                nodes[cells[0]] = cells[4]
            elif sec == "## Edges" and len(cells) >= 3 and cells[0] != "From":
                edges.append((cells[0], cells[1]))
        return nodes, edges

    nodes, edges = parse((domain / "GRAPH.md").read_text(encoding="utf-8"))
    for sub in domain.glob("entries/*/GRAPH.md"):
        sub_nodes, sub_edges = parse(sub.read_text(encoding="utf-8"))
        cat = sub.parent.name
        for nid, p in sub_nodes.items():
            nodes.setdefault(nid, p if p.startswith("entries/") else f"entries/{cat}/{p}")
        edges.extend(sub_edges)

    problems = []
    problems += [f"[DANGLING] {a} -> {b}" for a, b in edges
                 if a not in nodes or b not in nodes]
    problems += [f"[MISSING] {nid}: {p}" for nid, p in nodes.items()
                 if not (domain / p).exists()]
    return problems


# ── 승격 트랜잭션 ─────────────────────────────────────────────────
class Promoter:
    """백업 → 적용 → 검증 → (실패 시) 롤백을 관리하는 단일 트랜잭션."""

    def __init__(self, root: Path, project: Path, owner: str, report: list):
        self.domain = root / "domain"
        self.project = project
        self.owner = owner
        self.report = report
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.backup_dir = root / ".promote-backups" / f"{ts}-{re.sub(r'[^A-Za-z0-9_-]', '_', owner)}"
        self._backed_up = {}     # 원본경로 -> 백업경로
        self._created = []       # 롤백 시 삭제할 신규 파일

    # 백업/롤백 -----------------------------------------------------
    def _backup(self, path: Path):
        if path in self._backed_up or not path.exists():
            return
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        dest = self.backup_dir / f"{len(self._backed_up):02d}-{path.name}"
        shutil.copy2(path, dest)
        self._backed_up[path] = dest

    def rollback(self):
        for orig, bak in self._backed_up.items():
            shutil.copy2(bak, orig)
        for created in self._created:
            created.unlink(missing_ok=True)
        self.report.append(f"[ROLLBACK] 백업 복원 {len(self._backed_up)}건, 신규 파일 제거 {len(self._created)}건")

    # 개별 번들 적용 -------------------------------------------------
    def apply(self, b: Bundle) -> bool:
        """번들 1건 적용. 충돌 시 False (스킵, staging 보존)."""
        entry_file = self.domain / b.entry_path
        graph_file = self.domain / "GRAPH.md"
        index_file = self.domain / "INDEX.md"
        graph = graph_file.read_text(encoding="utf-8")

        # 충돌 검사 (낙관적 동시성 제어)
        if b.mode == "new":
            if entry_file.exists():
                self.report.append(f"[CONFLICT] {b.path.name}: entry 기존재 ({b.entry_path}) — 스킵")
                return False
            if b.entry_id() in node_ids(graph):
                self.report.append(f"[CONFLICT] {b.path.name}: 노드 ID 기존재 ({b.entry_id()}) — 스킵")
                return False
        else:  # augment
            if not entry_file.exists():
                self.report.append(f"[CONFLICT] {b.path.name}: augment 대상 없음 — 스킵")
                return False
            current = hashlib.sha256(entry_file.read_bytes()).hexdigest()
            if current != b.base_hash:
                self.report.append(
                    f"[CONFLICT] {b.path.name}: Base-Hash 불일치 (타 세션 변경 감지) — 스킵, 재큐레이션 필요")
                return False

        # entry 파일
        if b.mode == "new":
            entry_file.parent.mkdir(parents=True, exist_ok=True)
            entry_file.write_text(b.entry_body, encoding="utf-8")
            self._created.append(entry_file)
        else:
            self._backup(entry_file)
            entry_file.write_text(b.entry_body, encoding="utf-8")

        # GRAPH.md: 노드 행 (new=삽입, augment=교체) + 엣지 행 추가
        self._backup(graph_file)
        graph = graph_file.read_text(encoding="utf-8")
        if b.mode == "new":
            graph = insert_rows(graph, "Nodes", [b.node_row])
        else:
            graph = replace_row(graph, "Nodes", b.entry_id(), b.node_row)
        if b.edge_rows:
            existing = {ln.strip() for ln in graph.splitlines()}
            fresh = [r for r in b.edge_rows if r.strip() not in existing]  # 중복 엣지 스킵
            if fresh:
                graph = insert_rows(graph, "Edges", fresh)
        graph_file.write_text(graph, encoding="utf-8")

        # domain/INDEX.md: 트리거 행 (new=삽입, augment=경로 매칭 행 교체 시도)
        self._backup(index_file)
        index = index_file.read_text(encoding="utf-8")
        if b.mode == "new":
            index = insert_rows(index, "Domain Map", [b.index_row])
        else:
            index = self._replace_index_row_by_path(index, b) or index
        index_file.write_text(index, encoding="utf-8")

        # 프로젝트 backlink (INDEX 존재 시에만, 이미 있으면 스킵)
        if b.backlink_row:
            self._add_backlink(b)

        self.report.append(
            f"[OK] {b.path.name}: {b.mode} {b.entry_path} (엣지 +{len(b.edge_rows)})")
        return True

    def _replace_index_row_by_path(self, index: str, b: Bundle):
        """augment 시 Domain Map에서 entry 경로를 담은 행을 새 행으로 교체."""
        lines = index.splitlines()
        start, end = section_bounds(lines, "Domain Map")
        for i in range(start, end):
            if lines[i].strip().startswith("|") and b.entry_path in lines[i]:
                lines[i] = b.index_row
                return "\n".join(lines) + ("\n" if index.endswith("\n") else "")
        # 경로 매칭 행이 없으면 신규 삽입
        return insert_rows(index, "Domain Map", [b.index_row])

    def _add_backlink(self, b: Bundle):
        """{프로젝트}/common_knowledge/INDEX.md Domain Links에 역방향 링크 추가."""
        idx = self.project / "common_knowledge" / "INDEX.md"
        if not idx.exists():
            self.report.append(f"[SKIP] backlink: 프로젝트 INDEX 없음 ({b.path.name})")
            return
        text = idx.read_text(encoding="utf-8")
        if b.entry_path in text:
            self.report.append(f"[SKIP] backlink: 이미 존재 ({b.entry_id()})")
            return
        self._backup(idx)
        if "## Domain Links" not in text:
            text = text.rstrip() + "\n\n## Domain Links\n\n| 키워드 | Domain Entry | 힌트 |\n|--------|-------------|------|\n"
        text = insert_rows(text, "Domain Links", [b.backlink_row])
        idx.write_text(text, encoding="utf-8")

    # 마무리 ---------------------------------------------------------
    def finalize_stamps(self, applied: int, edges: int):
        """GRAPH/INDEX Last Updated를 승격 명의로 갱신."""
        stamp = (f"{datetime.now().strftime('%Y-%m-%d')} ({self.owner} promote — "
                 f"노드 +{applied}, 엣지 +{edges})")
        for f in (self.domain / "GRAPH.md", self.domain / "INDEX.md"):
            f.write_text(set_last_updated(f.read_text(encoding="utf-8"), stamp),
                         encoding="utf-8")


# ── 메인 ──────────────────────────────────────────────────────────
def find_staging_dir(project: Path) -> Path:
    """§17 staging 위치 자동 감지와 동일 규칙."""
    if list(project.glob("MICKEY-*-SESSION.md")):
        return project / "_curator-staging"
    if list(project.glob(".kiro/mickey/MICKEY-*-SESSION.md")):
        return project / ".kiro" / "_curator-staging"
    return project / "_curator-staging"


def main() -> int:
    ap = argparse.ArgumentParser(description="세션 로컬 staging(gd-*.md) → 글로벌 domain/ 승격")
    ap.add_argument("--project", required=True, help="프로젝트 루트 경로")
    ap.add_argument("--owner", required=True, help="승격 명의 (예: 'ai-developer-mickey Mickey 41')")
    ap.add_argument("--files", nargs="*", help="특정 번들 파일만 (기본: staging의 gd-*.md 전부)")
    ap.add_argument("--dry-run", action="store_true", help="검증/계획만 출력, 쓰기 없음")
    args = ap.parse_args()

    root = global_root()
    project = Path(args.project).resolve()
    staging = find_staging_dir(project)
    report = [f"promote_knowledge — owner={args.owner}, global={root}",
              f"staging={staging}"]

    # 번들 수집 + 파싱 (파싱 실패는 전체 중단 — 부분 적용 방지)
    files = ([Path(f) for f in args.files] if args.files
             else sorted(staging.glob("gd-*.md")))
    if not files:
        print("\n".join(report + ["처리할 gd-*.md 번들 없음 — 종료"]))
        return 0
    try:
        bundles = [parse_bundle(f) for f in files]
    except ValueError as e:
        print("\n".join(report + [f"[FAIL] 번들 파싱 실패: {e}"]))
        return 1

    if args.dry_run:
        for b in bundles:
            report.append(f"[PLAN] {b.path.name}: {b.mode} {b.entry_path} "
                          f"(엣지 {len(b.edge_rows)}, backlink {'유' if b.backlink_row else '무'})")
        print("\n".join(report))
        return 0

    # 락 획득 → 트랜잭션
    try:
        lock = acquire_lock(root, args.owner)
    except RuntimeError as e:
        print("\n".join(report + [f"[BUSY] {e}"]))
        return 2

    exit_code = 0
    try:
        promoter = Promoter(root, project, args.owner, report)
        applied, total_edges = [], 0
        for b in bundles:
            if promoter.apply(b):
                applied.append(b)
                total_edges += len(b.edge_rows)

        problems = integrity_check(root / "domain")
        if problems:
            report.append(f"[FAIL] 무결성 검증 위반 {len(problems)}건 → 롤백")
            report.extend(f"  {p}" for p in problems[:20])
            promoter.rollback()
            exit_code = 1
        else:
            if applied:
                promoter.finalize_stamps(len(applied), total_edges)
                for b in applied:
                    b.path.unlink()  # 승격 완료된 staging 정리
            report.append(f"[RESULT] PASS — 승격 {len(applied)}/{len(bundles)}건, "
                          f"무결성 dangling 0")
            if len(applied) < len(bundles):
                exit_code = 1  # CONFLICT 잔여 존재
    finally:
        release_lock(lock)

    out = staging / f"promote-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report + [f"(리포트: {out})"]))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
