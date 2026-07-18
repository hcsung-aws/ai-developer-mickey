# -*- coding: utf-8 -*-
"""M37: Curator 관련 파일 타임스탬프 실측 (PowerShell 표시 이슈 우회)."""
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

D = Path(r"C:\Users\hcsung\.kiro\mickey\domain")
targets = [
    D / "entries" / "llm-flat-graph-id-schema.md",
    D / "GRAPH.md",
    D / "INDEX.md",
]
for t in targets:
    if t.exists():
        st = t.stat()
        print(f"{t.name}: created={datetime.fromtimestamp(st.st_ctime)} modified={datetime.fromtimestamp(st.st_mtime)} size={st.st_size}")
    else:
        print(f"{t.name}: 없음")

# GRAPH/INDEX Last Updated 명의 확인
for name in ("GRAPH.md", "INDEX.md"):
    text = (D / name).read_text(encoding="utf-8")
    idx = text.find("## Last Updated")
    print(f"\n--- {name} Last Updated ---")
    print(text[idx : idx + 250])
