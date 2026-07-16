# M38: gitignore 된 .kiro/hooks + .kiro/scripts 를 mickey-power clone 으로 복사
# (.kiro/ 전체가 .gitignore 대상이라 clone 에 hook/부팅 스크립트가 누락됨 — 수동 이식)
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 대응 (adaptive #8)

SRC = Path(r"c:\Users\hcsung\work\kiro\ai-developer-mickey\.kiro")
DEST = Path(r"c:\Users\hcsung\work\kiro\mickey-power\.kiro")

# 복사 대상: hooks(세션 hook 정의) + scripts(boot/close 스크립트)만.
# settings 등 머신/워크스페이스 상태는 제외 (clone 쪽에서 독립 관리)
for sub in ("hooks", "scripts"):
    src_dir = SRC / sub
    dest_dir = DEST / sub
    if not src_dir.exists():
        print(f"SKIP    {sub}: 소스 미존재")
        continue
    if dest_dir.exists():
        print(f"SKIP    {sub}: 대상 이미 존재 (덮어쓰지 않음)")
        continue
    shutil.copytree(src_dir, dest_dir)
    copied = sorted(p.name for p in dest_dir.iterdir())
    print(f"COPIED  {sub}: {len(copied)} entries -> {copied}")
