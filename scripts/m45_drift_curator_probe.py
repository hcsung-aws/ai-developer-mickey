# M45 조사 스크립트: ① 오늘 promote가 그래프에 무엇을 추가했는지 (백업 diff)
# ② back-to-basic 프로젝트의 curator invoke 리포트에서 실패 흔적 확인
# ③ malformed 행의 기원 추적 (promote 백업 시계열에서 최초 등장 시점)
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: cp949 방어

HOME = Path.home()
DOMAIN = HOME / ".kiro" / "mickey" / "domain"
BACKUPS = HOME / ".kiro" / "mickey" / ".promote-backups"

def node_ids(graph_text):
    """GRAPH.md Nodes 섹션에서 노드 ID 집합 추출 (첫 셀 기준)"""
    ids = set()
    in_nodes = False
    for line in graph_text.splitlines():
        if line.startswith("## "):
            in_nodes = line.strip() == "## Nodes"
            continue
        if in_nodes and line.startswith("|"):
            cells = line.split("|")
            if len(cells) > 1:
                nid = cells[1].strip()
                if nid and nid not in ("ID", ":---", "---") and not nid.startswith(":"):
                    ids.add(nid)
    return ids

def count_edges(graph_text):
    in_edges = False
    n = 0
    for line in graph_text.splitlines():
        if line.startswith("## "):
            in_edges = line.strip() == "## Edges"
            continue
        if in_edges and line.startswith("|") and "---" not in line and "From" not in line:
            n += 1
    return n

cur_graph = (DOMAIN / "GRAPH.md").read_text(encoding="utf-8")
cur_ids = node_ids(cur_graph)

print("=== ① 오늘(08-27) promote 백업 diff — 각 시점 백업 GRAPH 대비 현재 추가된 노드 ===")
for d in sorted(BACKUPS.iterdir()):
    if not d.name.startswith("2026082"):  # 최근 며칠만
        continue
    gfiles = list(d.glob("*GRAPH.md"))
    if not gfiles:
        continue
    old = gfiles[0].read_text(encoding="utf-8")
    old_ids = node_ids(old)
    added = cur_ids - old_ids
    print(f"[{d.name}] 백업 시점 노드 {len(old_ids)}, 엣지 {count_edges(old)} -> 이후 추가 노드 {len(added)}개")
    if len(added) <= 6:
        for a in sorted(added):
            print(f"    + {a}")

print()
print("=== ② malformed 행(installer-auth) 최초 등장 시점 추적 ===")
for d in sorted(BACKUPS.iterdir()):
    gfiles = list(d.glob("*GRAPH.md"))
    if not gfiles:
        continue
    txt = gfiles[0].read_text(encoding="utf-8")
    has_node = "| installer-auth-state-followup-gap |" in txt
    # 미이스케이프 || 존재 여부 (해당 노드 행 안에서)
    row = next((l for l in txt.splitlines() if l.startswith("| installer-auth-state-followup-gap |") and "similar-to" not in l), None)
    raw_pipe = bool(row and re.search(r"[^\\]\|\| true", row))
    print(f"[{d.name}] 노드 존재={has_node}, 행 내 미이스케이프 ||={raw_pipe}")

print()
print("=== ③ back-to-basic 프로젝트 위치 + curator/promote 리포트 스캔 ===")
work = Path(r"C:\Users\hcsung\work")
candidates = [p for p in work.rglob("_curator-staging") if p.is_dir() and "back-to-basic" in str(p)]
if not candidates:
    # work 전체 rglob이 느리면 상위 2단계만
    candidates = [p / "_curator-staging" for p in work.glob("*/*") if (p / "_curator-staging").is_dir() and "back-to-basic" in p.name]
for st in candidates:
    print(f"[staging] {st}")
    for f in sorted(st.iterdir()):
        print(f"    {f.name}  ({f.stat().st_size} bytes)")
