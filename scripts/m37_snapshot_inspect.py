# -*- coding: utf-8 -*-
"""M37: pre-스냅샷의 GRAPH/INDEX mtime 확인 — 변경 주체(anjin M4 vs M37 Curator) 분리."""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SNAP = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\scripts\output\m37_curator_snapshot.json")
data = json.loads(SNAP.read_text(encoding="utf-8"))

for key in ("global:domain/GRAPH.md", "global:domain/INDEX.md", "global:domain/entries/llm-flat-graph-id-schema.md"):
    if key in data:
        mt, size = data[key]
        print(f"{key}: pre mtime={datetime.fromtimestamp(mt)} size={size}")
    else:
        print(f"{key}: 스냅샷에 없음")
