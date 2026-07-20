# M39: cloud/ 하위 GRAPH 태그 클러스터 감시 스크립트
# 목적: entries/cloud/GRAPH.md 내부의 태그별 노드 수를 실측하여
#       §20 재귀 분할 임계값(동일 태그 클러스터 7개 노드 이상) 도달 여부를 감시한다.
# 출력: 임계값 도달 태그(HIT)와 근접 태그(5~6, WATCH)를 구분 보고.
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: Windows cp949 대응

SUB_GRAPH = Path.home() / ".kiro" / "mickey" / "domain" / "entries" / "cloud" / "GRAPH.md"
THRESHOLD = 7  # §20 카테고리화 임계값


def parse_nodes(text: str) -> dict[str, list[str]]:
    """Nodes 표를 파싱하여 {노드ID: [태그...]} 를 반환한다."""
    nodes = {}
    in_nodes = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_nodes = line.strip() == "## Nodes"
            continue
        if not in_nodes or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # 헤더/구분선 행 제외 (5컬럼: ID, Title, Tags, Core, Path)
        if len(cells) < 5 or cells[0] in ("ID", "") or re.match(r"^-+$", cells[0]):
            continue
        nodes[cells[0]] = [t.strip() for t in cells[2].split(",") if t.strip()]
    return nodes


def main() -> int:
    nodes = parse_nodes(SUB_GRAPH.read_text(encoding="utf-8"))
    clusters = defaultdict(list)
    for node_id, tags in nodes.items():
        for tag in tags:
            clusters[tag].append(node_id)

    print(f"cloud/ 하위 GRAPH 노드 수: {len(nodes)}")
    hits = {t: m for t, m in clusters.items() if len(m) >= THRESHOLD}
    watch = {t: m for t, m in clusters.items() if THRESHOLD - 2 <= len(m) < THRESHOLD}

    print(f"\n=== 임계값({THRESHOLD}+) 도달 태그: {len(hits)}건 ===")
    for tag, members in sorted(hits.items(), key=lambda x: -len(x[1])):
        print(f"  [HIT] {tag} ({len(members)}): {', '.join(sorted(members))}")

    print(f"\n=== 근접(5~6) 감시 태그: {len(watch)}건 ===")
    for tag, members in sorted(watch.items(), key=lambda x: -len(x[1])):
        print(f"  [WATCH] {tag} ({len(members)}): {', '.join(sorted(members))}")

    print("\n=== 상위 클러스터 분포 (3+) ===")
    for tag, members in sorted(clusters.items(), key=lambda x: -len(x[1])):
        if len(members) >= 3:
            print(f"  {tag}: {len(members)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
