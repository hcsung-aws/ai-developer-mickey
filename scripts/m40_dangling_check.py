# M40: 글로벌 GRAPH.md 무결성 검증 — 신규 노드/엣지 추가 후 dangling 0 확인
# 불변 조건만 검증 (invariant-vs-snapshot-verification 원칙): 엣지 끝점 실존 + Path 파일 실존
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DOMAIN = Path.home() / ".kiro" / "mickey" / "domain"
GRAPH = DOMAIN / "GRAPH.md"
OUT = Path(__file__).resolve().parent / "output" / "m40_dangling_check.txt"


def parse(text: str):
    nodes, edges = {}, []
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or re.match(r"^-+$", cells[0]):
            continue
        if section == "## Nodes" and len(cells) >= 5 and cells[0] != "ID":
            nodes[cells[0]] = cells[4]  # ID -> Path
        elif section == "## Edges" and len(cells) >= 3 and cells[0] != "From":
            edges.append((cells[0], cells[1]))
    return nodes, edges


def main() -> int:
    nodes, edges = parse(GRAPH.read_text(encoding="utf-8"))
    # §20 규약: 상위 GRAPH는 카테고리 anchor + cross-category 엣지를 보유하고,
    # 하위 노드는 entries/{category}/GRAPH.md에 존재 → 병합 후 dangling 판정 (builder와 동일 시맨틱)
    for sub in DOMAIN.glob("entries/*/GRAPH.md"):
        sub_nodes, sub_edges = parse(sub.read_text(encoding="utf-8"))
        cat = sub.parent.name
        for nid, p in sub_nodes.items():
            nodes.setdefault(nid, f"entries/{cat}/{p}" if not p.startswith("entries/") else p)
        edges.extend(sub_edges)
    lines = [f"nodes(merged)={len(nodes)}, edges(merged)={len(edges)}"]
    # 불변 1: 엣지 끝점이 모두 노드 표에 실존
    dangling = [(a, b) for a, b in edges if a not in nodes or b not in nodes]
    lines.append(f"dangling edges: {len(dangling)}")
    for d in dangling:
        lines.append(f"  [DANGLING] {d}")
    # 불변 2: 노드 Path 파일 실존 (GRAPH.md 기준 상대 경로)
    missing = [(nid, p) for nid, p in nodes.items() if not (DOMAIN / p).exists()]
    lines.append(f"missing paths: {len(missing)}")
    for nid, p in missing:
        lines.append(f"  [MISSING] {nid}: {p}")
    ok = not dangling and not missing
    lines.append("RESULT: PASS" if ok else "RESULT: FAIL")
    report = "\n".join(lines)
    OUT.write_text(report, encoding="utf-8")
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
