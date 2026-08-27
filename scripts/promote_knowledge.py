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
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# 같은 디렉토리에 배치되는 공유 락 모듈 (repo scripts/ 및 ~/.kiro/mickey/scripts/ 동일)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mickey_lock  # noqa: E402

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
            # M45: 코드 스팬 내 파이프 정규화 → 셀 수 검증 (쓰기 전 fail-fast)
            row = escape_pipes_in_code_spans(line.rstrip())
            if section in EXPECTED_CELLS:
                validate_cell_count(row, EXPECTED_CELLS[section],
                                    f"{path.name} [{section}]")
            if section == "Graph Node Row" and not b.node_row:
                b.node_row = row
            elif section == "Graph Edge Rows":
                b.edge_rows.append(row)
            elif section == "Index Row" and not b.index_row:
                b.index_row = row
            elif section == "Backlink Row" and not b.backlink_row:
                b.backlink_row = row

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


# ── 표 행 위생 (M45): 파이프 정규화 + 셀 수 검증 ──────────────────
# 배경: `|| true` 미이스케이프 노드 행이 GRAPH 표 셀을 분절 (2026-07-24 유입,
# M44 감사 [L] malformed + [G] INDEX 대조 오탐의 근인). 정규화 가능한 것은
# 코드로 고치고, 나머지는 어떤 디스크 쓰기도 일어나기 전에 거부한다 (fail-fast).
EXPECTED_CELLS = {
    "Graph Node Row": 5,    # | ID | 요약 | Tags | 언제 | Path |
    "Graph Edge Rows": 4,   # | From | To | Type | 사유 |
    "Index Row": 3,         # | 트리거 | 파일 | 요약 |
    "Backlink Row": 3,      # | 키워드 | Domain Entry | 힌트 |
}
_CODE_SPAN = re.compile(r"`[^`]+`")


def escape_pipes_in_code_spans(row: str) -> str:
    """인라인 코드 스팬(`...`) 내부의 미이스케이프 `|`를 `\\|`로 정규화.

    코드 스팬 안의 파이프는 표 구분자가 아님이 명백하므로 결정론적으로 고칠 수 있다.
    (스팬 밖의 미이스케이프 파이프는 의도를 알 수 없어 validate에서 거부만 한다)
    """
    def _fix(m):
        return re.sub(r"(?<!\\)\|", r"\\|", m.group(0))
    return _CODE_SPAN.sub(_fix, row)


def split_cells(row: str) -> list:
    """이스케이프(\\|)를 보존하며 표 행을 셀 리스트로 분해."""
    parts = re.split(r"(?<!\\)\|", row.strip())
    # 정상 행은 |로 시작/종료 → 양끝 빈 조각 제거
    return [c.strip() for c in parts[1:-1]] if len(parts) >= 3 else []


def validate_cell_count(row: str, expected: int, context: str):
    """셀 수가 스키마와 다르면 ValueError — 셀 내부 미이스케이프 파이프 의심."""
    n = len(split_cells(row))
    if n != expected:
        raise ValueError(
            f"{context}: 표 행 셀 수 {n} ≠ 기대 {expected} — 셀 내부의 '|'는 "
            f"'\\|'로 이스케이프 필요 (특히 코드 스팬 밖). 행: {row[:120]}")


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
    """섹션 내 마지막 표 행 뒤에 rows 삽입 + 표 내부 빈 줄 제거.

    빈 줄이 표 중간에 누적되면 마크다운 테이블이 분절되므로(M44 감사: Edges 41개),
    삽입 시점에 표 범위(첫 행~마지막 행)를 compact하게 정규화한다 (M44 개선 A-②).
    """
    lines = text.splitlines()
    start, end = section_bounds(lines, title)
    pipes = [i for i in range(start, end) if lines[i].strip().startswith("|")]
    if not pipes:
        raise ValueError(f"## {title} 섹션에 표 없음")
    first_pipe, last_pipe = pipes[0], pipes[-1]
    table = [lines[i] for i in range(first_pipe, last_pipe + 1) if lines[i].strip()]
    new_lines = lines[:first_pipe] + table + rows + lines[last_pipe + 1:]
    return "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")


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


def category_graph_file(domain: Path, entry_path: str):
    """entry가 카테고리 하위(entries/{cat}/...)이고 하위 GRAPH.md가 있으면 그 경로 반환.

    §20 규약상 카테고리 멤버 노드의 정위치는 하위 GRAPH다. promote가 이를 인식하지 못해
    상위 GRAPH에 직접 등재하던 드리프트(M44 감사 [M] 5건)를 차단한다 (M44 개선 A-①).
    """
    parts = Path(entry_path).parts
    if len(parts) >= 3 and parts[0] == "entries":
        sub = domain / parts[0] / parts[1] / "GRAPH.md"
        if sub.exists():
            return sub
    return None


def edge_endpoints(row: str) -> tuple:
    """엣지 표 행에서 (From, To) 노드 ID를 추출한다."""
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    return (cells[0], cells[1]) if len(cells) >= 2 else ("", "")


def top_hub_ids(graph_texts: list, n: int = 5) -> set:
    """Edges 표 기준 차수 상위 n개 노드 ID.

    신규 엣지가 전부 최상위 허브로만 향하는 hub-and-spoke 편중(M44 감사: 상위 5 허브가
    엣지 35% 점유)을 승격 시점에 통지하기 위한 기준 집합 (M44 개선 A-③).
    """
    deg = Counter()
    for text in graph_texts:
        lines = text.splitlines()
        try:
            start, end = section_bounds(lines, "Edges")
        except ValueError:
            continue
        for ln in lines[start:end]:
            if not ln.strip().startswith("|") or _is_separator_row(ln):
                continue
            f, t = edge_endpoints(ln)
            if f in ("From", ""):
                continue
            deg[f] += 1
            deg[t] += 1
    return {nid for nid, _ in deg.most_common(n)}


# ── 락 (mickey_lock 공유 모듈 위임 — M43) ─────────────────────────
# 기존 공개 시그니처(acquire_lock/release_lock/_lock_owner_info/LOCK_STALE_SECONDS)를
# 보존하는 얇은 래퍼. 메커니즘(mkdir 원자성 + owner.json + stale)은 mickey_lock 소관.
def acquire_lock(root: Path, owner: str) -> Path:
    """글로벌 승격 락 획득. stale 락은 자동 회수 (promote 정책). 실패 시 RuntimeError."""
    return mickey_lock.acquire(
        root / ".promote.lock", owner,
        stale_seconds=LOCK_STALE_SECONDS, auto_reclaim=True)


def _lock_owner_info(lock: Path) -> str:
    return mickey_lock.owner_info(lock).get("owner", "unknown")


def release_lock(lock: Path):
    mickey_lock.release(lock)


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
        self._created = []
        self._touched_subs = set()  # 이번 승격에서 수정한 하위 카테고리 GRAPH (스탬프 대상)       # 롤백 시 삭제할 신규 파일

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
        # 카테고리 entry(entries/{cat}/...)는 하위 GRAPH가 노드의 정위치 (§20 — M44 개선 A-①)
        sub_file = category_graph_file(self.domain, b.entry_path)
        sub_text = sub_file.read_text(encoding="utf-8") if sub_file else ""

        # 충돌 검사 (낙관적 동시성 제어) — 노드 ID는 상위+하위 병합 기준
        known_ids = node_ids(graph) | (node_ids(sub_text) if sub_file else set())
        if b.mode == "new":
            if entry_file.exists():
                self.report.append(f"[CONFLICT] {b.path.name}: entry 기존재 ({b.entry_path}) — 스킵")
                return False
            if b.entry_id() in known_ids:
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

        # 허브 편중 통지 (M44 개선 A-③) — 차단이 아닌 경고: 신규 엣지의 상대 끝점이
        # 전부 최상위 허브면 hub-and-spoke 편중을 키우므로 비허브 peer 연결을 유도.
        # 허브 5개가 성립할 규모의 그래프에서만 판정 (소형/테스트 그래프 잡음 방지)
        if b.edge_rows:
            hubs = top_hub_ids([graph] + ([sub_text] if sub_file else []))
            others = set()
            for r in b.edge_rows:
                ep_from, ep_to = edge_endpoints(r)
                others.update(x for x in (ep_from, ep_to) if x and x != b.entry_id())
            if others and len(hubs) >= 5 and others <= hubs:
                self.report.append(
                    f"[WARN] {b.path.name}: 신규 엣지가 전부 최상위 허브로만 연결"
                    f" ({', '.join(sorted(others))}) — 비허브 peer 연결 1개 이상 권장")

        # entry 파일
        if b.mode == "new":
            entry_file.parent.mkdir(parents=True, exist_ok=True)
            entry_file.write_text(b.entry_body, encoding="utf-8")
            self._created.append(entry_file)
        else:
            self._backup(entry_file)
            entry_file.write_text(b.entry_body, encoding="utf-8")

        # GRAPH: 노드 행 — 카테고리 entry는 하위 GRAPH에 (augment는 노드가 실재하는 그래프에서 교체)
        self._backup(graph_file)
        graph = graph_file.read_text(encoding="utf-8")
        if sub_file:
            self._backup(sub_file)
            self._touched_subs.add(sub_file)
        if b.mode == "new":
            if sub_file:
                sub_text = insert_rows(sub_text, "Nodes", [b.node_row])
            else:
                graph = insert_rows(graph, "Nodes", [b.node_row])
        else:
            if sub_file and b.entry_id() in node_ids(sub_text):
                sub_text = replace_row(sub_text, "Nodes", b.entry_id(), b.node_row)
            else:
                # 드리프트 호환: 과거 상위에 등재된 카테고리 노드는 상위에서 교체
                graph = replace_row(graph, "Nodes", b.entry_id(), b.node_row)

        # GRAPH: 엣지 행 — 양 끝점이 하위 그래프 내부면 하위에, 아니면 상위에(cross-category)
        if b.edge_rows:
            existing = {ln.strip() for ln in (graph + "\n" + sub_text).splitlines()}
            fresh = [r for r in b.edge_rows if r.strip() not in existing]  # 중복 엣지 스킵
            if fresh and sub_file:
                sub_ids = node_ids(sub_text)
                internal = [r for r in fresh
                            if all(e in sub_ids for e in edge_endpoints(r) if e)]
                cross = [r for r in fresh if r not in internal]
                if internal:
                    sub_text = insert_rows(sub_text, "Edges", internal)
                if cross:
                    graph = insert_rows(graph, "Edges", cross)
            elif fresh:
                graph = insert_rows(graph, "Edges", fresh)
        graph_file.write_text(graph, encoding="utf-8")
        if sub_file:
            sub_file.write_text(sub_text, encoding="utf-8")

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

        routed = " → 하위 GRAPH 라우팅" if sub_file else ""
        self.report.append(
            f"[OK] {b.path.name}: {b.mode} {b.entry_path} (엣지 +{len(b.edge_rows)}){routed}")
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
        """GRAPH/INDEX (+수정된 하위 GRAPH) Last Updated를 승격 명의로 갱신."""
        stamp = (f"{datetime.now().strftime('%Y-%m-%d')} ({self.owner} promote — "
                 f"노드 +{applied}, 엣지 +{edges})")
        targets = [self.domain / "GRAPH.md", self.domain / "INDEX.md"] + sorted(self._touched_subs)
        for f in targets:
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
