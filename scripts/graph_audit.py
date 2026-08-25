# 글로벌 도메인 지식 그래프 통합 감사 (상비 도구 — M44 도입, §3 엔트로피 체크 8항)
#
# 목적: 그래프 전면 점검의 정량 실측 담당 (판단은 세션이 수행).
# 기준점 대조: ai-developer-mickey/GRAPH-HEALTH-BASELINE-*.md (M44 baseline 고정)
#   [A] dangling 엣지 (끝점 미실존 — cloud/ 하위 그래프 병합 시맨틱, m40_dangling_check 계승)
#   [B] 노드 Path 파일 실존
#   [C] orphan 노드 (엣지 0개)
#   [D] 저연결 노드 (엣지 1개 — 연결 보강 후보 입력)
#   [E] 중복 엣지 (동일 from-to 쌍 2회 이상)
#   [F] 중복 노드 행
#   [G] INDEX.md ↔ GRAPH.md 정합 (INDEX 행이 가리키는 entry vs GRAPH 노드 Path)
#   [H] entries/ 디스크 파일 vs GRAPH 노드 (미등재 entry)
#   [I] 태그 클러스터 >=7 + 응집도 실측 (§20 Step 3 기준: 과반 co-tag / 응집률 vs (k-1)/(N-1))
#   [J] 차수 분포 (허브 상위 / 평균 차수)
#   [K] 엔트로피: 표 내부 빈 줄(마크다운 테이블 분절) 카운트
#
# 출력: scripts/output/m44_graph_audit.txt (cp949 콘솔 잘림 대비 — adaptive #14)
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: Windows cp949 대응

DOMAIN = Path.home() / ".kiro" / "mickey" / "domain"
PARENT_GRAPH = DOMAIN / "GRAPH.md"
INDEX = DOMAIN / "INDEX.md"
OUT = Path(__file__).resolve().parent / "output" / "graph_audit.txt"
THRESHOLD = 7  # §20 카테고리화 임계값


def parse_graph(text: str):
    """GRAPH.md에서 Nodes {ID: (tags, path)} / Edges [(from,to,type)] / 표 내부 빈 줄 수를 파싱."""
    nodes: dict[str, tuple[list[str], str]] = {}
    node_rows: list[str] = []  # 중복 노드 행 검출용 (ID 나열)
    edges: list[tuple[str, str, str]] = []
    malformed: list[tuple[str, str]] = []  # 셀 수 이상 행 (미이스케이프 파이프 등)
    section = None
    blank_in_table = {"## Nodes": 0, "## Edges": 0}
    in_table = False
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
            in_table = False
            continue
        if not line.strip():
            # 직전까지 표를 읽고 있었다면 표 내부 분절 빈 줄로 카운트
            if in_table and section in blank_in_table:
                blank_in_table[section] += 1
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        in_table = True
        # 이스케이프(\|)를 존중하여 셀 분리 — 미이스케이프 파이프가 있으면 셀 수가 틀어져 malformed로 검출됨
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if not cells or re.match(r"^[-\s]+$", cells[0]):
            continue
        if section == "## Nodes" and cells[0] != "ID":
            if len(cells) != 5 or not cells[4].strip():
                malformed.append((section, line[:100]))
                if len(cells) < 5:
                    continue
            node_rows.append(cells[0])
            nodes[cells[0]] = ([t.strip() for t in cells[2].split(",") if t.strip()], cells[-1] if cells[-1].strip() else cells[4])
        elif section == "## Edges" and len(cells) >= 3 and cells[0] != "From":
            if len(cells) != 4:
                malformed.append((section, line[:100]))
            edges.append((cells[0], cells[1], cells[2] if len(cells) > 2 else ""))
    return nodes, node_rows, edges, blank_in_table, malformed


def parse_index_entry_paths(text: str) -> list[str]:
    """INDEX.md Domain Map 표에서 '파일' 컬럼(entries/... 또는 patterns/...)을 순서대로 수집."""
    paths = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[1] not in ("파일", "하위 GRAPH") and not re.match(r"^[-\s]+$", cells[1]):
            if "entries/" in cells[1] or "patterns/" in cells[1]:
                paths.append(cells[1])
    return paths


def main() -> int:
    lines: list[str] = []
    p_nodes, p_rows, p_edges, p_blank, p_malformed = parse_graph(PARENT_GRAPH.read_text(encoding="utf-8"))

    # 하위 카테고리 그래프 병합 (dangling 판정용 — builder/promote와 동일 시맨틱)
    sub_nodes_all: dict[str, tuple[list[str], str]] = {}
    sub_edges_all: list[tuple[str, str, str]] = []
    sub_names: dict[str, str] = {}  # 노드ID -> 카테고리명
    for sub in sorted(DOMAIN.glob("entries/*/GRAPH.md")):
        cat = sub.parent.name
        s_nodes, _, s_edges, s_blank, s_malformed = parse_graph(sub.read_text(encoding="utf-8"))
        p_malformed.extend(s_malformed)
        for nid, (tags, path) in s_nodes.items():
            sub_nodes_all[nid] = (tags, f"entries/{cat}/" + Path(path).name if not path.startswith("entries/") else path)
            sub_names[nid] = cat
        sub_edges_all.extend(s_edges)
        lines.append(f"[하위 그래프] {cat}: 노드 {len(s_nodes)}, 엣지 {len(s_edges)}, 표 내부 빈 줄 {sum(s_blank.values())}")

    all_nodes = dict(p_nodes)
    all_nodes.update(sub_nodes_all)
    all_edges = p_edges + sub_edges_all

    lines.insert(0, f"[전체] 상위 노드 {len(p_nodes)} + 하위 노드 {len(sub_nodes_all)} = {len(all_nodes)} / 상위 엣지 {len(p_edges)} + 하위 엣지 {len(sub_edges_all)} = {len(all_edges)}")

    # [A] dangling 엣지
    dangling = [(f, t) for f, t, _ in all_edges if f not in all_nodes or t not in all_nodes]
    lines.append(f"\n[A] dangling 엣지: {len(dangling)}")
    for f, t in dangling:
        miss = [x for x in (f, t) if x not in all_nodes]
        lines.append(f"  - {f} -> {t} (미실존: {', '.join(miss)})")

    # [B] Path 실존
    missing_path = []
    for nid, (_, path) in all_nodes.items():
        rel = path.replace("../", "")  # patterns/ 상대 참조 보정
        target = (DOMAIN / path).resolve() if not path.startswith("../") else (DOMAIN / path).resolve()
        if not target.exists():
            missing_path.append((nid, path))
    lines.append(f"\n[B] Path 미실존 노드: {len(missing_path)}")
    for nid, path in missing_path:
        lines.append(f"  - {nid}: {path}")

    # 차수 계산 (무방향, 병합 그래프)
    degree: dict[str, int] = defaultdict(int)
    pair_count: dict[tuple[str, str], int] = defaultdict(int)
    for f, t, _ in all_edges:
        degree[f] += 1
        degree[t] += 1
        pair_count[tuple(sorted((f, t)))] += 1

    # [C] orphan / [D] 저연결
    orphans = [n for n in all_nodes if degree[n] == 0]
    low = [n for n in all_nodes if degree[n] == 1]
    lines.append(f"\n[C] orphan 노드 (차수 0): {len(orphans)}")
    for n in orphans:
        lines.append(f"  - {n} (tags: {', '.join(all_nodes[n][0][:6])})")
    lines.append(f"\n[D] 저연결 노드 (차수 1): {len(low)}")
    for n in low:
        lines.append(f"  - {n} (tags: {', '.join(all_nodes[n][0][:6])})")

    # [E] 중복 엣지
    dup_edges = {pair: c for pair, c in pair_count.items() if c > 1}
    lines.append(f"\n[E] 중복 엣지 쌍 (동일 from-to 2회+): {len(dup_edges)}")
    for (a, b), c in dup_edges.items():
        lines.append(f"  - {a} <-> {b}: {c}회")

    # [F] 중복 노드 행
    seen: set[str] = set()
    dup_nodes = [n for n in p_rows if n in seen or seen.add(n)]
    lines.append(f"\n[F] 상위 GRAPH 중복 노드 행: {len(dup_nodes)} {dup_nodes}")

    # [G] INDEX ↔ GRAPH 정합
    idx_paths = parse_index_entry_paths(INDEX.read_text(encoding="utf-8"))
    idx_dup = [p for p, c in ((p, idx_paths.count(p)) for p in set(idx_paths)) if c > 1]
    graph_paths = {path.lstrip("./") for _, (_, path) in all_nodes.items()}
    # patterns/ 참조는 domain 밖이므로 비교 대상에서 표기만 통일
    idx_only = [p for p in set(idx_paths) if p not in graph_paths and not p.startswith("patterns/")]
    graph_only = [p for p in graph_paths if p not in set(idx_paths) and not p.startswith("../")]
    lines.append(f"\n[G] INDEX 행 수(경로 기준): {len(idx_paths)} (고유 {len(set(idx_paths))})")
    lines.append(f"  - INDEX 중복 등재: {len(idx_dup)}")
    for p in sorted(idx_dup):
        lines.append(f"    * {p} ({idx_paths.count(p)}회)")
    lines.append(f"  - INDEX에만 있고 GRAPH에 없음: {len(idx_only)}")
    for p in sorted(idx_only):
        lines.append(f"    * {p}")
    lines.append(f"  - GRAPH에만 있고 INDEX에 없음: {len(graph_only)}")
    for p in sorted(graph_only):
        lines.append(f"    * {p}")

    # [H] 디스크 entries ↔ GRAPH 노드
    disk_entries = set()
    for f in DOMAIN.glob("entries/**/*.md"):
        # 백업 파일 제외는 확장자/접미사 정밀 매칭 (appconfig-allatonce-"bake" 오탐 방지)
        if f.name == "GRAPH.md" or re.search(r"\.(bak|m\d+[a-f0-9]*-bak)\b|\.bak-", f.name):
            continue
        disk_entries.add(f.relative_to(DOMAIN).as_posix())
    unregistered = sorted(disk_entries - graph_paths)
    ghost = sorted(p for p in graph_paths if p.startswith("entries/") and not p.endswith("GRAPH.md") and p not in disk_entries)
    lines.append(f"\n[H] 디스크 entry 파일: {len(disk_entries)}")
    lines.append(f"  - GRAPH 미등재 디스크 파일: {len(unregistered)}")
    for p in unregistered:
        lines.append(f"    * {p}")
    lines.append(f"  - GRAPH 등재이나 디스크 부재: {len(ghost)} {ghost}")

    # [I] 태그 클러스터 (상위 flat 노드만 — §20 Step 3 트리거는 상위 GRAPH 기준)
    flat_nodes = {n: tags for n, (tags, path) in p_nodes.items() if not tags or "category-anchor" not in tags}
    clusters: dict[str, list[str]] = defaultdict(list)
    for n, tags in flat_nodes.items():
        for t in tags:
            clusters[t].append(n)
    hits = {t: ms for t, ms in clusters.items() if len(ms) >= THRESHOLD}
    N = len(flat_nodes)
    # 무방향 인접 (상위 엣지만 — flat 클러스터 내부/경계 판정)
    adj: dict[str, set[str]] = defaultdict(set)
    for f, t, _ in p_edges:
        adj[f].add(t)
        adj[t].add(f)
    lines.append(f"\n[I] 태그 클러스터 >= {THRESHOLD} (상위 flat {N}개 노드 기준): {len(hits)}건")
    for tag, members in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        k = len(members)
        mset = set(members)
        internal = sum(1 for m in members for nb in adj[m] if nb in mset) // 2
        boundary = sum(1 for m in members for nb in adj[m] if nb not in mset)
        cohesion = internal / (internal + boundary) if (internal + boundary) else 0.0
        expected = (k - 1) / (N - 1) if N > 1 else 0.0
        # 과반 co-tag: 멤버 과반이 공유하는 다른 태그
        co = defaultdict(int)
        for m in members:
            for t2 in flat_nodes[m]:
                if t2 != tag:
                    co[t2] += 1
        majority = [t2 for t2, c in co.items() if c > k / 2]
        verdict = "도메인 후보" if (majority or cohesion > expected * 1.5) else "aspect 신호"
        lines.append(f"  - {tag}: k={k}, 응집률={cohesion:.2f} vs 기대치={expected:.2f}, 과반 co-tag={majority or '없음'} → {verdict}")
        lines.append(f"      멤버: {', '.join(sorted(members))}")

    # [J] 차수 분포
    degs = sorted(((degree[n], n) for n in all_nodes), reverse=True)
    avg = sum(degree[n] for n in all_nodes) / len(all_nodes)
    lines.append(f"\n[J] 평균 차수: {avg:.2f} / 허브 상위 10:")
    for d, n in degs[:10]:
        lines.append(f"  - {n}: {d}")

    # [K] 표 내부 빈 줄 (마크다운 테이블 분절)
    lines.append(f"\n[K] 상위 GRAPH 표 내부 빈 줄: Nodes {p_blank['## Nodes']}, Edges {p_blank['## Edges']}")

    # [L] malformed 행 (미이스케이프 파이프 등 셀 수 이상)
    lines.append(f"\n[L] malformed 표 행 (셀 수 이상): {len(p_malformed)}")
    for sec, frag in p_malformed:
        lines.append(f"  - {sec}: {frag}")

    # [M] 구조 드리프트: 상위 GRAPH에 등재됐지만 Path가 카테고리 하위인 노드 (promote가 상위에 직접 추가)
    drift = [(n, path) for n, (_, path) in p_nodes.items()
             if re.match(r"entries/[^/]+/", path) and not path.endswith("GRAPH.md")]
    lines.append(f"\n[M] 상위 GRAPH 등재 + 카테고리 Path 노드 (하위 그래프 미이관): {len(drift)}")
    for n, path in sorted(drift):
        lines.append(f"  - {n}: {path}")

    report = "\n".join(lines)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(report, encoding="utf-8")
    print(f"[RESULT] 리포트 저장: {OUT}")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
