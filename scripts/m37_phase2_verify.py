# -*- coding: utf-8 -*-
"""M37 Phase 2 검증: cloud 카테고리화 후 링크/파일/그래프 정합성 전수 확인.

체크 항목:
1. 파일 배치: cloud/ 에 18개 존재, flat 에서 부재, entry 총수 보존(이동 전 총수와 일치)
2. 상위 GRAPH: 모든 Path 실파일 존재 + anchor 행 존재 + 이동 노드 행 부재
3. 하위 GRAPH: 18 노드 + 모든 Path 실파일 존재
4. 엣지 dangling: 상위 엣지 양끝 ∈ (상위∪하위 노드), 하위 엣지 양끝 ∈ 하위 노드
5. INDEX: Anchors 표에 cloud 행 존재 + 트리거 행의 entries/ 경로가 이동으로 깨지지 않았는지
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DOMAIN = Path(r"C:\Users\hcsung\.kiro\mickey\domain")
GRAPH = DOMAIN / "GRAPH.md"
SUB = DOMAIN / "entries" / "cloud" / "GRAPH.md"
INDEX = DOMAIN / "INDEX.md"
ENTRIES = DOMAIN / "entries"

EXPECTED_MOVED = 18
EXPECTED_TOTAL = 67  # entry 파일 총수. M36 "68"은 노드 수(= entry 67 + patterns 소속 batch-confirm 1)

PASS = FAIL = 0

def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name} — {detail}")

def parse_graph(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    nodes, edges = {}, []
    section = None
    seen_header = {"nodes": False, "edges": False}
    for ln in lines:
        if ln.startswith("## "):
            s = ln[3:].strip().lower()
            section = "nodes" if s.startswith("nodes") else "edges" if s.startswith("edges") else None
            continue
        if section and ln.strip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if not seen_header[section]:
                seen_header[section] = True
                continue
            if set(ln.replace("|", "").strip()) <= {"-", " ", ":"}:
                continue
            if section == "nodes":
                nodes[cells[0]] = cells[-1]  # id -> path
            else:
                edges.append((cells[0], cells[1]))
    return nodes, edges

top_nodes, top_edges = parse_graph(GRAPH)
sub_nodes, sub_edges = parse_graph(SUB)

print("=== 1. 파일 배치 ===")
cloud_files = sorted(p.name for p in (ENTRIES / "cloud").glob("*.md") if p.name != "GRAPH.md")
check(f"cloud/ entry {EXPECTED_MOVED}개", len(cloud_files) == EXPECTED_MOVED, f"실제 {len(cloud_files)}")
flat_files = [p for p in ENTRIES.glob("*.md")]
overlap = {p.stem for p in flat_files} & {Path(f).stem for f in cloud_files}
check("flat/cloud 중복 없음", not overlap, str(overlap))
total = len(flat_files) + len(cloud_files)
check(f"entry 총수 보존 ({EXPECTED_TOTAL})", total == EXPECTED_TOTAL, f"실제 {total} (flat {len(flat_files)} + cloud {len(cloud_files)})")

print("=== 2. 상위 GRAPH ===")
check("anchor 행 존재 (cloud)", "cloud" in top_nodes)
check(f"상위 노드 수 = {EXPECTED_TOTAL + 1 - EXPECTED_MOVED} + anchor 1", len(top_nodes) == EXPECTED_TOTAL + 1 - EXPECTED_MOVED + 1, f"실제 {len(top_nodes)}")
moved_in_top = {n for n in sub_nodes if n in top_nodes}
check("이동 노드 상위 행 부재", not moved_in_top, str(moved_in_top))
bad_paths = [(n, p) for n, p in top_nodes.items() if not (DOMAIN / p).exists()]
check("상위 Path 전행 실파일 존재", not bad_paths, str(bad_paths[:5]))

print("=== 3. 하위 GRAPH ===")
check(f"하위 노드 {EXPECTED_MOVED}개", len(sub_nodes) == EXPECTED_MOVED, f"실제 {len(sub_nodes)}")
bad_sub = [(n, p) for n, p in sub_nodes.items() if not (DOMAIN / p).exists()]
check("하위 Path 전행 실파일 존재", not bad_sub, str(bad_sub[:5]))

print("=== 4. 엣지 dangling ===")
known = set(top_nodes) | set(sub_nodes)
dangling_top = [(f, t) for f, t in top_edges if f not in known or t not in known]
check(f"상위 엣지({len(top_edges)}) dangling 0", not dangling_top, str(dangling_top[:5]))
dangling_sub = [(f, t) for f, t in sub_edges if f not in sub_nodes or t not in sub_nodes]
check(f"하위 엣지({len(sub_edges)}) dangling 0 (양끝 내부)", not dangling_sub, str(dangling_sub[:5]))
check("엣지 총수 보존 (212)", len(top_edges) + len(sub_edges) == 212, f"상위 {len(top_edges)} + 하위 {len(sub_edges)}")

print("=== 5. INDEX ===")
idx = INDEX.read_text(encoding="utf-8")
check("Anchors 표에 cloud 행", "| cloud | entries/cloud/GRAPH.md" in idx)
# INDEX 트리거 행의 entries/*.md 경로 실존 확인 (이동으로 깨진 경로 탐지)
idx_paths = set(re.findall(r"entries/[\w\-/]+\.md", idx))
broken = [p for p in idx_paths if not (DOMAIN / p).exists()]
check(f"INDEX 내 entries 경로({len(idx_paths)}) 전부 실존", not broken, str(broken))

print(f"\n결과: {PASS} passed / {FAIL} failed")
sys.exit(1 if FAIL else 0)
