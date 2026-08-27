# M45 조사 ⑤: ~/.kiro/logs 전체 나열 + 실패 시각대(08-26 18:30, 08-27 00:21/01:37/10:30) 로그에서 에러 패턴 추출
import sys, re
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

logs = Path.home() / ".kiro" / "logs"
print("=== ~/.kiro/logs 디렉토리 전체 ===")
dirs = sorted(logs.iterdir(), key=lambda d: d.stat().st_mtime)
for d in dirs:
    mt = datetime.fromtimestamp(d.stat().st_mtime).strftime("%m-%d %H:%M")
    files = list(d.glob("*.log")) if d.is_dir() else []
    sizes = ", ".join(f"{f.name}:{f.stat().st_size}" for f in files)
    print(f"  [{mt}] {d.name}  ({sizes})")

print()
print("=== 최근 kiro.log에서 에러/패닉/절단 패턴 검색 ===")
patterns = re.compile(r"(error|panic|fatal|EmptyResponse|stream|abort|exit code|unexpected)", re.I)
for d in dirs[-6:]:
    klog = d / "kiro.log"
    if not klog.exists() or klog.stat().st_size == 0:
        continue
    print(f"\n--- {d.name}/kiro.log ({klog.stat().st_size} bytes) ---")
    txt = klog.read_text(encoding="utf-8", errors="replace")
    hits = [l for l in txt.splitlines() if patterns.search(l)]
    print(f"  매칭 {len(hits)}줄 (마지막 15줄 표시)")
    for l in hits[-15:]:
        print("  " + l[:220])
