# -*- coding: utf-8 -*-
"""m46_scan_global_baks.py — 글로벌 영역의 .bak 파일 전수 조사 (Mickey 46)

목적: ~/.kiro/mickey/ 와 ~/.kiro/agents/ 아래의 백업 파일(.bak*, .m<N>-bak 류)을
      전부 나열하고 명의(project)별로 분류하여 삭제 계획의 근거를 만든다.
읽기 전용 — 삭제는 사용자 확인 후 별도 수행.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: cp949 환경 대비

HOME = Path.home()
# 조사 대상 루트: 글로벌 지식 저장소 + agents JSON 디렉토리
ROOTS = [HOME / ".kiro" / "mickey", HOME / ".kiro" / "agents"]

# 백업 파일 판별: 이름에 .bak 또는 -bak 이 포함된 파일 (promote 자동 백업 디렉토리는 규약 대상 아님 — 제외)
EXCLUDE_DIRS = {".promote-backups"}

found = []
for root in ROOTS:
    if not root.exists():
        continue
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        # 제외 디렉토리 하위는 건너뜀
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        name = p.name.lower()
        if ".bak" in name or "-bak" in name:
            found.append(p)

print(f"[SCAN] 백업 파일 총 {len(found)}건\n")
for p in sorted(found):
    size_kb = p.stat().st_size / 1024
    # 명의 분류: .bak-<project>-m<N> 규약 파싱
    tag = ""
    if ".bak-ai-developer-mickey-" in p.name:
        tag = "본 프로젝트 명의"
    elif ".bak-" in p.name:
        tag = "타 프로젝트 명의"
    else:
        tag = "규약 외 (구식 네이밍)"
    print(f"  [{tag}] {p}  ({size_kb:.0f} KB)")
