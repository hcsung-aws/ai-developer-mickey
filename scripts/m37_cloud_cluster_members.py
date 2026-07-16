# -*- coding: utf-8 -*-
"""M37: Phase 2 설계 근거 — Cloud/AWS/IaC 계열 태그별 노드 구성원 실측.

GRAPH.md Nodes 표를 파싱하여 후보 태그(cdk + Cloud 대계열)별 소속 노드를 나열.
"cdk만 vs cloud 대계열 통합" 판단의 구체적 데이터를 제공한다.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GRAPH = Path(r"C:\Users\hcsung\.kiro\mickey\domain\GRAPH.md")

# M36 분석의 Cloud/AWS/IaC 계열 태그 (SESSION-36 근거)
CLOUD_TAGS = [
    "cdk", "aws", "cognito", "infrastructure", "terraform", "agentcore",
    "boto3", "deployment", "bedrock", "iam", "lambda", "botocore",
    "serverless", "provisioning", "cdk-nag", "ci-cd",
]

text = GRAPH.read_text(encoding="utf-8")

# Nodes 표 파싱: | id | ... | tags | ... 형태 — 헤더 구조 먼저 확인
lines = text.splitlines()
in_nodes = False
header = None
rows = []
for ln in lines:
    if ln.startswith("## "):
        in_nodes = ln.strip().lower().startswith("## nodes")
        continue
    if in_nodes and ln.startswith("|"):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set(ln.replace("|", "").strip()) <= {"-", " ", ":"}:
            continue
        rows.append(cells)

print(f"헤더: {header}")
print(f"노드 수: {len(rows)}")

id_i = header.index("id") if "id" in header else 0
tags_i = next(i for i, h in enumerate(header) if "tag" in h)
path_i = next((i for i, h in enumerate(header) if "path" in h), None)

tag_nodes = defaultdict(list)
node_tags = {}
for cells in rows:
    nid = cells[id_i]
    tags = [t.strip() for t in re.split(r"[,;]", cells[tags_i]) if t.strip()]
    node_tags[nid] = tags
    for t in tags:
        tag_nodes[t].append(nid)

print("\n=== Cloud 계열 태그별 노드 ===")
cloud_members = set()
for t in CLOUD_TAGS:
    nodes = tag_nodes.get(t, [])
    cloud_members.update(nodes)
    print(f"\n[{t}] ({len(nodes)})")
    for n in nodes:
        print(f"  - {n}")

print(f"\n=== Cloud 대계열 합집합: {len(cloud_members)}개 노드 ===")
for n in sorted(cloud_members):
    print(f"  - {n}  (태그: {', '.join(node_tags[n])})")
