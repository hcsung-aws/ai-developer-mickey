# M36: Curator 오작동으로 유입된 anjin-llm-scenario-poc M3 지식 2건을 글로벌 GRAPH.md 에서 외과 제거.
# 사용자 결정 B — anjin 지식은 anjin 세션이 정식 승격. M36 산출물(verification-tool-as-health-scanner)은 보존.
# GRAPH.md 의 해당 Nodes 행 + 해당 ID를 From/To 로 갖는 Edges 행 제거. --apply 없으면 dry-run.
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

GRAPH = Path.home() / ".kiro" / "mickey" / "domain" / "GRAPH.md"
REMOVE = {"silent-ignore-static-prevalidation", "llm-temperature-determinism"}


def parse_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    text = GRAPH.read_text(encoding="utf-8")
    head, rest = text.split("## Nodes", 1)
    nodes_body, edges_part = rest.split("## Edges", 1)

    removed_nodes = []
    removed_edges = []

    # Nodes: col0(id) in REMOVE 제거
    new_nodes = []
    for ln in nodes_body.splitlines():
        s = ln.strip()
        if s.startswith("|"):
            cols = parse_row(ln)
            if cols and cols[0] in REMOVE:
                removed_nodes.append(cols[0])
                continue
        new_nodes.append(ln)

    # Edges: From(col0) 또는 To(col1) in REMOVE 제거
    new_edges = []
    for ln in edges_part.splitlines():
        s = ln.strip()
        if s.startswith("|"):
            cols = parse_row(ln)
            if len(cols) >= 2 and (cols[0] in REMOVE or cols[1] in REMOVE):
                removed_edges.append(f"{cols[0]} -> {cols[1]}")
                continue
        new_edges.append(ln)

    new_text = head + "## Nodes" + "\n".join(new_nodes) + "## Edges" + "\n".join(new_edges)
    # split 시 사라진 개행 보정: "## Nodes" 다음이 원래 개행으로 시작했으므로 new_nodes[0] 은 빈 문자열이어야 함
    # 안전하게 원본 구조 유지 위해 splitlines 재조립 확인
    # (nodes_body 는 "\n| ID ..." 로 시작하므로 splitlines()[0]=="" → join 시 "## Nodes\n..." 복원됨)

    print(f"제거 노드({len(removed_nodes)}): {removed_nodes}")
    print(f"제거 엣지({len(removed_edges)}):")
    for e in removed_edges:
        print(f"  {e}")

    if not args.apply:
        print("\n[DRY-RUN] --apply 없어 쓰지 않음")
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = GRAPH.parent / f"GRAPH.md.m36-revert-bak-{stamp}"
    shutil.copy2(GRAPH, bak)
    GRAPH.write_text(new_text, encoding="utf-8")
    print(f"\n[APPLIED] 백업: {bak.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
