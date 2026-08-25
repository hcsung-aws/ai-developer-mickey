# M44: 엣지 의미 품질 측정
#   1) 엣지 타입 분포 (similar-to / extends / applies-to / prerequisite)
#   2) 허브 집중도: 상위 허브가 전체 엣지에서 차지하는 비율
#   3) 상투적 사유 비율: "가족 패턴" / "동일 철학" / "동일 계열" 류 일반론 사유
# 출력: scripts/output/m44_edge_semantics.txt
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from graph_audit import parse_graph  # noqa: E402

DOMAIN = Path.home() / ".kiro" / "mickey" / "domain"
OUT = Path(__file__).resolve().parent / "output" / "m44_edge_semantics.txt"
GENERIC = ("가족 패턴", "동일 철학", "동일 계열", "가족", "계열")  # 일반론 사유 마커


def full_edges():
    """상위 + 하위 그래프의 (from, to, type, reason) 전체 목록."""
    edges = []
    for gpath in [DOMAIN / "GRAPH.md"] + sorted(DOMAIN.glob("entries/*/GRAPH.md")):
        text = gpath.read_text(encoding="utf-8")
        section = None
        for line in text.splitlines():
            if line.startswith("## "):
                section = line.strip()
                continue
            if section != "## Edges" or not line.startswith("|"):
                continue
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) >= 4 and cells[0] != "From" and not re.match(r"^[-\s]+$", cells[0]):
                edges.append((cells[0], cells[1], cells[2], cells[3]))
    return edges


def main() -> int:
    edges = full_edges()
    lines = [f"전체 엣지: {len(edges)}"]

    types = Counter(t for _, _, t, _ in edges)
    lines.append("\n[엣지 타입 분포]")
    for t, c in types.most_common():
        lines.append(f"  - {t}: {c} ({c/len(edges)*100:.0f}%)")

    deg = Counter()
    for f, t, _, _ in edges:
        deg[f] += 1
        deg[t] += 1
    top5 = [n for n, _ in deg.most_common(5)]
    touch_top5 = sum(1 for f, t, _, _ in edges if f in top5 or t in top5)
    lines.append(f"\n[허브 집중도] 상위 5 허브({', '.join(top5)})가 닿는 엣지: {touch_top5}/{len(edges)} ({touch_top5/len(edges)*100:.0f}%)")

    generic = [(f, t, ty, r) for f, t, ty, r in edges if any(g in r for g in GENERIC)]
    lines.append(f"\n[상투적 사유 엣지] ('가족/철학/계열' 일반론): {len(generic)}/{len(edges)} ({len(generic)/len(edges)*100:.0f}%)")
    gen_types = Counter(ty for _, _, ty, _ in generic)
    lines.append(f"  타입 내역: {dict(gen_types)}")
    hub_generic = sum(1 for f, t, _, _ in generic if f in top5 or t in top5)
    lines.append(f"  상위 5 허브에 닿는 비율: {hub_generic}/{len(generic)}")

    report = "\n".join(lines)
    OUT.write_text(report, encoding="utf-8")
    print(f"[RESULT] {OUT}")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
