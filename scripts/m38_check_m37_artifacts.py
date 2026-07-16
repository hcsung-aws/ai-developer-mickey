# M38 진입 검증: M37 산출물이 디스크에 실존하는지 확인
# (세션 전환 시 에디터 버퍼 vs 디스크 불일치 대비 — adaptive #9)
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 대응 (adaptive #8)

ROOT = Path(__file__).resolve().parent.parent

# 확인 대상: M37 세션이 생성/수정했다고 기록한 파일들
targets = [
    "scripts/m37_mickey_mirror_diff.py",
    "scripts/m37_test_install_seed.py",
    "install.ps1",
    "install.sh",
    "sessions/MICKEY-37-SESSION.md",
    "mickey/extended-protocols.md",
]

for rel in targets:
    p = ROOT / rel
    if p.exists():
        stat = p.stat()
        from datetime import datetime
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"EXISTS  {rel}  ({stat.st_size:,} bytes, mtime {mtime})")
    else:
        print(f"MISSING {rel}")
