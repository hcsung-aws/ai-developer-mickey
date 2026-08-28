# -*- coding: utf-8 -*-
"""m46_delete_baks.py — 글로벌 .bak 정리 (Mickey 46, 사용자 승인분 13건)

대상: ai-developer-mickey 명의 m41~m45 백업만. 명시적 목록 방식 —
      substring 매칭 오탐(예: 'bake' 안의 'bak')을 원천 차단한다.
각 파일의 존재를 확인 후 삭제하고, 결과를 건별 보고한다.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: cp949 환경 대비

HOME = Path.home()
MICKEY = HOME / ".kiro" / "mickey"
AGENTS = HOME / ".kiro" / "agents"

# 사용자 승인된 삭제 목록 (2026-08-28) — 안정성 근거는 MICKEY-46-SESSION.md 참조
TARGETS = [
    MICKEY / "extended-protocols.md.bak-ai-developer-mickey-m41",
    MICKEY / "extended-protocols.md.bak-ai-developer-mickey-m42",
    MICKEY / "extended-protocols.md.bak-ai-developer-mickey-m43",
    MICKEY / "extended-protocols.md.bak-ai-developer-mickey-m44",
    MICKEY / "domain" / "CURATOR-PROMPT.md.bak-ai-developer-mickey-m41",
    MICKEY / "domain" / "CURATOR-PROMPT.md.bak-ai-developer-mickey-m44",
    MICKEY / "domain" / "CURATOR-PROMPT.md.bak-ai-developer-mickey-m45",
    MICKEY / "domain" / "GRAPH.md.bak-ai-developer-mickey-m45",
    MICKEY / "domain" / "PROFILE.md.bak-ai-developer-mickey-m41",
    AGENTS / "ai-developer-mickey.json.bak-ai-developer-mickey-m41",
    AGENTS / "ai-developer-mickey.json.bak-ai-developer-mickey-m42",
    AGENTS / "ai-developer-mickey.json.bak-ai-developer-mickey-m43",
    AGENTS / "knowledge-curator.json.bak-ai-developer-mickey-m41",
]

deleted, missing = 0, 0
for p in TARGETS:
    if p.exists():
        # 삭제 전 원본 파일(백업 접미사 제거)이 실존하는지 최종 안전 확인
        original = p.parent / p.name.split(".bak-")[0]
        if not original.exists():
            print(f"  [SKIP] 원본 부재 — 삭제 보류: {p}")
            continue
        p.unlink()
        print(f"  [DEL] {p}")
        deleted += 1
    else:
        print(f"  [MISS] 이미 없음: {p}")
        missing += 1

print(f"\n[RESULT] 삭제 {deleted}건 / 부재 {missing}건 / 목록 {len(TARGETS)}건")

# 삭제 후 잔존 검증: 본 프로젝트 명의 .bak- 파일이 남아 있으면 보고
remain = []
for root in (MICKEY, AGENTS):
    for p in root.rglob("*.bak-ai-developer-mickey-*"):
        if p.is_file():
            remain.append(p)
print(f"[VERIFY] 잔존 본 프로젝트 명의 .bak: {len(remain)}건")
for p in sorted(remain):
    print(f"  - {p}")
