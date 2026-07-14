# M36: 글로벌 domain GRAPH.md 의 Nodes 표를 파싱하여 태그별 노드 수(클러스터 크기)를 집계한다.
# 목적: Step 3 카테고리화 임계값을 정하기 위해 "임계값 N일 때 몇 개 클러스터가 초과하는지" 실측.
# 중복 노드 ID(같은 id가 2행)는 태그를 합집합으로 병합하여 1개 노드로 계산.
import sys
import re
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 회피 (adaptive #8)

graph_path = Path.home() / ".kiro" / "mickey" / "domain" / "GRAPH.md"
text = graph_path.read_text(encoding="utf-8")

# Nodes 섹션만 추출 (## Nodes ~ ## Edges 사이)
nodes_section = text.split("## Nodes", 1)[1].split("## Edges", 1)[0]

# 노드 ID -> 태그 집합 (중복 ID 병합)
node_tags = defaultdict(set)
for line in nodes_section.splitlines():
    line = line.strip()
    if not line.startswith("|"):
        continue
    cols = [c.strip() for c in line.strip("|").split("|")]
    if len(cols) < 4:
        continue
    node_id = cols[0]
    # 헤더/구분선 스킵
    if node_id in ("ID", "") or set(node_id) <= set("-: "):
        continue
    tags_raw = cols[2]
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    node_tags[node_id].update(tags)

total_nodes = len(node_tags)

# 태그별 노드 수 집계
tag_count = defaultdict(int)
for nid, tags in node_tags.items():
    for t in tags:
        tag_count[t] += 1

# 클러스터 크기 내림차순 정렬
sorted_tags = sorted(tag_count.items(), key=lambda x: (-x[1], x[0]))

print(f"총 고유 노드 수(중복 ID 병합 후): {total_nodes}")
print(f"총 고유 태그 수: {len(tag_count)}")
print()
print("=== 클러스터 크기 상위 (노드 수 2 이상) ===")
print(f"{'태그':40s} {'노드수':>5s}")
for tag, cnt in sorted_tags:
    if cnt >= 2:
        print(f"{tag:40s} {cnt:>5d}")

print()
print("=== 임계값별 초과 클러스터 수 (임계값 이상인 태그 개수) ===")
for threshold in range(3, 11):
    exceeding = [t for t, c in tag_count.items() if c >= threshold]
    print(f"임계값 {threshold:2d} 이상: {len(exceeding):2d}개 클러스터  ->  {sorted(exceeding, key=lambda t:-tag_count[t])}")
