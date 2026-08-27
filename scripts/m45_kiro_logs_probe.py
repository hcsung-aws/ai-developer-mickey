# M45 조사 ④: kiro-cli 로그 위치 탐색 + 실패 시각대 로그 존재 확인
import sys, os
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

home = Path.home()
candidates = [
    home / ".kiro" / "logs",
    home / "AppData" / "Local" / "kiro-cli",
    home / "AppData" / "Local" / "kiro",
    home / "AppData" / "Roaming" / "kiro",
    Path(os.environ.get("TEMP", "")) ,
]
print("=== 로그 디렉토리 후보 ===")
for c in candidates:
    if c and c.exists():
        print(f"[존재] {c}")
        # 최근 수정 파일 상위 8개
        files = sorted((f for f in c.rglob("*") if f.is_file()),
                       key=lambda f: f.stat().st_mtime, reverse=True)[:8]
        for f in files:
            mt = datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d %H:%M")
            print(f"    {mt}  {f.relative_to(c)}  ({f.stat().st_size} bytes)")
    else:
        print(f"[없음] {c}")

print()
print("=== kiro-cli 실행 파일 갱신 시각 (버전 업데이트 여부) ===")
import shutil
exe = shutil.which("kiro-cli")
if exe:
    st = Path(exe).stat()
    print(f"{exe} — 수정 시각: {datetime.fromtimestamp(st.st_mtime)}")
