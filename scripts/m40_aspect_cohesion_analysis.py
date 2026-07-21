# M40: 태그 클러스터 응집도 분석 — "응집 도메인 vs 횡단 관점(aspect)" 판정을 데이터로 검증
#
# 배경: §20 Step 3 판단 지침은 "aspect(예: verification/testing/distrust/architecture)면 skip"
#       이라고 예시하지만, 이것이 실제 그래프 구조상 타당한지 실측한 적 없음 (M36은 태그 빈도만 측정).
# 방법: 임계값(7+) 도달 태그 클러스터별로 3가지 응집도 지표를 계산
#   1) 엣지 응집률: 클러스터 내부 엣지 / (내부 + 경계 엣지) — 응집 도메인이면 높음
#   2) 내부 밀도: 내부 엣지 / 가능한 쌍 C(n,2) — 멤버끼리 실제로 연결되어 있는가
#   3) co-tag 분산: 멤버들의 나머지 태그가 얼마나 다양한 도메인에 걸치는가 — aspect면 넓게 분산
# 기준선: 이미 카테고리화된 cloud/ 하위 그래프에 동일 지표를 적용하여 "응집 도메인"의 실측치와 비교
import re
import sys
from pathlib import Path
from collections import defaultdict
from itertools import combinations

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: Windows cp949 대응

DOMAIN_DIR = Path.home() / ".kiro" / "mickey" / "domain"
PARENT_GRAPH = DOMAIN_DIR / "GRAPH.md"
CLOUD_GRAPH = DOMAIN_DIR / "entries" / "cloud" / "GRAPH.md"
THRESHOLD = 7  # §20 카테고리화 임계값
OUT_FILE = Path(__file__).parent / "output" / "m40_cohesion_report.txt"


def parse_graph(text: str) -> tuple[dict[str, list[str]], list[tuple[str, str, str]]]:
    """GRAPH.md에서 Nodes {ID: [태그...]} 와 Edges [(from, to, type)...] 를 파싱한다."""
    nodes: dict[str, list[str]] = {}
    edges: list[tuple[str, str, str]] = []
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
            nodes[cells[0]] = [t.strip() for t in cells[2].split(",") if t.strip()]
        elif section == "## Edges" and len(cells) >= 3 and cells[0] != "From":
            edges.append((cells[0], cells[1], cells[2]))
    return nodes, edges


def cohesion_metrics(members: set[str], edges: list[tuple[str, str, str]]) -> dict:
    """클러스터의 엣지 응집률 + 내부 밀도를 계산한다."""
    internal = [e for e in edges if e[0] in members and e[1] in members]
    boundary = [e for e in edges if (e[0] in members) != (e[1] in members)]
    n = len(members)
    possible_pairs = n * (n - 1) // 2 if n > 1 else 1
    total_touch = len(internal) + len(boundary)
    return {
        "size": n,
        "internal_edges": len(internal),
        "boundary_edges": len(boundary),
        "cohesion_ratio": len(internal) / total_touch if total_touch else 0.0,
        "internal_density": len(internal) / possible_pairs,
        "internal_edge_list": internal,
    }


def cotag_spread(members: set[str], nodes: dict[str, list[str]], trigger: str) -> dict:
    """멤버들의 trigger 외 태그 분포를 계산한다. aspect면 소수 공유 없이 넓게 분산됨."""
    counter: dict[str, int] = defaultdict(int)
    for m in members:
        for t in nodes.get(m, []):
            if t != trigger:
                counter[t] += 1
    distinct = len(counter)
    # 멤버 과반이 공유하는 co-tag 수 — 응집 도메인이면 공유 co-tag가 존재
    majority_shared = {t: c for t, c in counter.items() if c >= (len(members) + 1) // 2}
    top = sorted(counter.items(), key=lambda x: -x[1])[:8]
    return {"distinct_cotags": distinct, "majority_shared": majority_shared, "top_cotags": top}


def report_cluster(tag: str, members: set[str], nodes: dict, edges: list, lines: list[str]) -> None:
    """단일 클러스터의 응집도 리포트를 lines에 추가한다."""
    met = cohesion_metrics(members, edges)
    spread = cotag_spread(members, nodes, tag)
    lines.append(f"\n### [{tag}] size={met['size']}")
    lines.append(f"  멤버: {', '.join(sorted(members))}")
    lines.append(f"  내부 엣지: {met['internal_edges']}  / 경계 엣지: {met['boundary_edges']}")
    lines.append(f"  엣지 응집률(내부/(내부+경계)): {met['cohesion_ratio']:.2f}")
    lines.append(f"  내부 밀도(내부/가능쌍): {met['internal_density']:.3f}")
    lines.append(f"  co-tag 종류 수: {spread['distinct_cotags']} (멤버당 평균 {spread['distinct_cotags']/met['size']:.1f})")
    lines.append(f"  과반 공유 co-tag: {spread['majority_shared'] or '(없음)'}")
    lines.append(f"  상위 co-tag: {spread['top_cotags']}")
    if met["internal_edge_list"]:
        for e in met["internal_edge_list"]:
            lines.append(f"    - 내부: {e[0]} -> {e[1]} ({e[2]})")


def main() -> int:
    nodes, edges = parse_graph(PARENT_GRAPH.read_text(encoding="utf-8"))
    lines: list[str] = []
    lines.append(f"글로벌 GRAPH: nodes={len(nodes)}, edges={len(edges)}")

    # 1) 임계값 도달 클러스터 산출 (ANCHOR 노드는 카테고리 자체이므로 제외)
    clusters: dict[str, set[str]] = defaultdict(set)
    for node_id, tags in nodes.items():
        if "category-anchor" in tags:
            continue
        for t in tags:
            clusters[t].add(node_id)
    hits = {t: m for t, m in clusters.items() if len(m) >= THRESHOLD}
    lines.append(f"\n=== 임계값({THRESHOLD}+) 도달 태그: {len(hits)}건 ===")
    for t, m in sorted(hits.items(), key=lambda x: -len(x[1])):
        lines.append(f"  {t}: {len(m)}")

    # 2) 각 도달 클러스터의 응집도 상세
    lines.append("\n=== 클러스터별 응집도 분석 ===")
    for t, m in sorted(hits.items(), key=lambda x: -len(x[1])):
        report_cluster(t, m, nodes, edges, lines)

    # 3) 기준선: cloud/ 하위 그래프 (이미 승인된 '응집 도메인'의 실측치)
    #    하위 그래프는 자체 엣지를 보유하므로 전체 멤버를 하나의 클러스터로 계산
    c_nodes, c_edges = parse_graph(CLOUD_GRAPH.read_text(encoding="utf-8"))
    c_members = set(c_nodes.keys())
    c_met = cohesion_metrics(c_members, c_edges)
    lines.append("\n=== 기준선: cloud/ (승인된 응집 도메인) ===")
    lines.append(f"  size={c_met['size']}, 내부 엣지={c_met['internal_edges']}, "
                 f"내부 밀도={c_met['internal_density']:.3f}")
    # cloud 내부에서 aspect성 태그(verification 등)가 얼마나 침투해 있는지 — 횡단성 방증
    aspect_probe = ["verification", "testing", "distrust"]
    lines.append("  (참고) cloud/ 내부의 aspect성 태그 보유 노드:")
    for probe in aspect_probe:
        holders = sorted(nid for nid, tags in c_nodes.items() if probe in tags)
        lines.append(f"    {probe}: {len(holders)}건 {holders}")

    report = "\n".join(lines)
    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text(report, encoding="utf-8")  # adaptive #14: 파일 리다이렉트로 실측 보존
    print(report)
    print(f"\n[리포트 저장] {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
