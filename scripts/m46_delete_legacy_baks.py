# -*- coding: utf-8 -*-
"""m46_delete_legacy_baks.py — 구식 네이밍(m24~m37 계열) .bak 정리 (Mickey 46, 사용자 승인)

대상: ~/.kiro/agents/ 의 구 규약(.m<N>-bak) 백업 9건 — 전부 M24~M37 시기 산물로
      현행 원본(agent JSON)이 다세션 정상 동작 중이라 롤백 가치 소멸.
제외: pre-v10-bak(의도 보존본), m058f5f-bak(타 세션 명의), 타 프로젝트 명의 백업.
명시적 목록 방식 — substring 오탐 차단. 삭제 전 원본 실존 확인.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: cp949 환경 대비

AGENTS = Path.home() / ".kiro" / "agents"

# 사용자 승인된 삭제 목록 (2026-08-28) — 근거: MICKEY-46-SESSION.md D-46-2
TARGETS = [
    AGENTS / "knowledge-curator.json.m24-bak",
    AGENTS / "knowledge-curator.json.m25-bak",
    AGENTS / "knowledge-curator.json.m26-bak",
    AGENTS / "knowledge-curator.json.m27-bak",
    AGENTS / "knowledge-curator.json.m28-bak",
    AGENTS / "knowledge-curator.json.m29-bak",
    AGENTS / "knowledge-curator.json.m37-bak",
    AGENTS / "knowledge-curator.json.m37-toolfix-bak",
    AGENTS / "ai-developer-mickey.json.m32-bak",
]

# 원본 파일명 추출: ".m<N>-bak" / ".m37-toolfix-bak" 접미사 제거 → ".json"으로 끝나는 부분까지
def original_of(p: Path) -> Path:
    name = p.name
    idx = name.find(".json")
    return p.parent / name[: idx + len(".json")]

deleted, missing = 0, 0
for p in TARGETS:
    if p.exists():
        if not original_of(p).exists():
            print(f"  [SKIP] 원본 부재 — 삭제 보류: {p}")
            continue
        p.unlink()
        print(f"  [DEL] {p}")
        deleted += 1
    else:
        print(f"  [MISS] 이미 없음: {p}")
        missing += 1

print(f"\n[RESULT] 삭제 {deleted}건 / 부재 {missing}건 / 목록 {len(TARGETS)}건")

# 잔존 검증: agents/ 에 남은 백업류 나열 (보존 의도분 확인용)
remain = [p for p in AGENTS.iterdir() if p.is_file() and ("-bak" in p.name or ".bak" in p.name)]
print(f"[VERIFY] agents/ 잔존 백업류: {len(remain)}건")
for p in sorted(remain):
    print(f"  - {p.name}")
