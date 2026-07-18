# -*- coding: utf-8 -*-
"""M37: staging 디렉토리 내용 직접 확인 (PowerShell 표시 이슈 우회)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

for root in (
    Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\_curator-staging"),
    Path(r"C:\Users\hcsung\.kiro\mickey\_curator-staging"),
):
    print(f"\n=== {root} (exists={root.exists()}) ===")
    if root.exists():
        for f in sorted(root.rglob("*")):
            print(f"  {f.relative_to(root)}  ({f.stat().st_size} bytes)")
