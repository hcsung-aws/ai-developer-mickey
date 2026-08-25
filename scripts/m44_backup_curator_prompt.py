# M44: 글로벌 CURATOR-PROMPT.md 백업 (adaptive #10 — git 미추적 글로벌 파일 편집 전 백업 필수)
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
src = Path.home() / ".kiro" / "mickey" / "domain" / "CURATOR-PROMPT.md"
dst = src.with_name(src.name + ".bak-ai-developer-mickey-m44")
shutil.copy2(src, dst)
print("[OK] 백업:", dst, dst.stat().st_size, "bytes")
