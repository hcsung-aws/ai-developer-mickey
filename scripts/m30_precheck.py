"""
Mickey 30 — precondition: extended-protocols.md (글로벌 vs repo) 동기화 방향 판정 + staging 3건 현재 상태 점검.

목적:
1. 글로벌 ~/.kiro/mickey/extended-protocols.md 와 repo mickey/extended-protocols.md 의 hash + size 비교
2. 글로벌 _curator-staging/ 3건의 첫 줄 메타데이터 현재 형식 확인
3. 변경 대상 문자열 정확 매칭 검증 (변경 적용 전 precondition)

출력: stdout 으로 표 형태 + 변경 가능/불가 판정.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

# Windows cp949 환경 대응: UTF-8 강제 (adaptive.md #8)
sys.stdout.reconfigure(encoding="utf-8")

HOME_KIRO_MICKEY = Path.home() / ".kiro" / "mickey"
REPO_ROOT = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")

# 대상 파일 정의
GLOBAL_PROTOCOLS = HOME_KIRO_MICKEY / "extended-protocols.md"
REPO_PROTOCOLS = REPO_ROOT / "mickey" / "extended-protocols.md"

STAGING_DIR = HOME_KIRO_MICKEY / "_curator-staging"
STAGING_FILES = {
    "pat-plan-implement-verify-trisection.md": "gamejob_crawler Mickey 32",
    "pat-handoff-unresolved-trigger-marker.md": "vision-math-helper Mickey 13",
    "pat-solution-bypass-vs-formal-resolution-separation.md": "vision-math-helper Mickey 13",
}


def file_hash(path: Path) -> str:
    """파일의 SHA-256 hash 반환 (8 byte prefix)."""
    if not path.exists():
        return "MISSING"
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()[:16].upper()


def first_line(path: Path) -> str:
    """파일 첫 줄 (메타데이터 줄) 반환."""
    if not path.exists():
        return "MISSING"
    with path.open("r", encoding="utf-8") as f:
        return f.readline().rstrip("\n")


def second_line(path: Path) -> str:
    """파일 두 번째 줄 (메타데이터 줄) 반환."""
    if not path.exists():
        return "MISSING"
    with path.open("r", encoding="utf-8") as f:
        f.readline()
        return f.readline().rstrip("\n")


def main() -> int:
    print("=" * 100)
    print("M30 PRECONDITION CHECK")
    print("=" * 100)

    # 1. extended-protocols.md 동기화 방향 판정
    g_hash = file_hash(GLOBAL_PROTOCOLS)
    r_hash = file_hash(REPO_PROTOCOLS)
    g_size = GLOBAL_PROTOCOLS.stat().st_size if GLOBAL_PROTOCOLS.exists() else 0
    r_size = REPO_PROTOCOLS.stat().st_size if REPO_PROTOCOLS.exists() else 0

    print("\n[1] extended-protocols.md 동기화 상태")
    print(f"  글로벌: {GLOBAL_PROTOCOLS}")
    print(f"          hash={g_hash}, size={g_size}")
    print(f"  repo:   {REPO_PROTOCOLS}")
    print(f"          hash={r_hash}, size={r_size}")
    if g_hash == r_hash:
        print("  → 일치 (양쪽 동일)")
    else:
        print("  → 불일치 — 변경 적용 후 동기화 필요 (글로벌 → repo)")

    # 2. §17 Pre-staged Apply 5단계 직후 anchor 확인 (변경안 삽입 지점)
    print("\n[2] §17 anchor 확인 (변경안 삽입 지점)")
    if GLOBAL_PROTOCOLS.exists():
        text = GLOBAL_PROTOCOLS.read_text(encoding="utf-8")
        # 5단계 직후의 "### staging 디렉토리 위치 (자동 감지)" 섹션이 다음 anchor
        anchor_5steps_end = "5. dangling 항목은 다음 세션 시작 엔트로피 체크에서 재제시. 3세션 이상 보류 시 자동 폐기 후보"
        anchor_next_section = "### staging 디렉토리 위치 (자동 감지)"
        count_5steps = text.count(anchor_5steps_end)
        count_next = text.count(anchor_next_section)
        print(f"  '5단계 마지막' anchor 매칭: {count_5steps} (정확히 1이어야 함)")
        print(f"  '다음 섹션' anchor 매칭:    {count_next} (정확히 1이어야 함)")
        if count_5steps == 1 and count_next == 1:
            print("  → anchor PASS: 변경 적용 가능")
        else:
            print("  → anchor FAIL: 변경 적용 불가 (수동 확인 필요)")

    # 3. §3 엔트로피 관리 anchor 확인
    print("\n[3] §3 엔트로피 관리 anchor 확인")
    if GLOBAL_PROTOCOLS.exists():
        text = GLOBAL_PROTOCOLS.read_text(encoding="utf-8")
        anchor_section_3 = "### 정리 행동"
        # §3 의 "정리 행동" 섹션이 변경 대상
        count_3 = text.count(anchor_section_3)
        print(f"  '### 정리 행동' anchor 매칭: {count_3} (정확히 1이어야 함)")
        if count_3 == 1:
            print("  → anchor PASS: 변경 적용 가능")
        else:
            print("  → anchor FAIL: 추가 분석 필요")

    # 4. staging 3건 메타데이터 현재 상태
    print("\n[4] 글로벌 staging 3건 메타데이터 현재 상태")
    for fname, expected_source in STAGING_FILES.items():
        fpath = STAGING_DIR / fname
        first = first_line(fpath)
        second = second_line(fpath)
        h = file_hash(fpath)
        print(f"\n  {fname}")
        print(f"    hash:    {h}")
        print(f"    line 1:  {first[:80]}...")
        print(f"    line 2:  {second[:80]}...")
        print(f"    예상 Source: {expected_source}")
        # 메타데이터 위치 식별: "> Pre-staged by" 가 첫 줄 또는 두 번째 줄에 있을 수 있음
        if first.startswith("> Pre-staged by") or second.startswith("> Pre-staged by"):
            print("    → 메타데이터 행 존재")
        else:
            print("    → 메타데이터 행 미확인 (수동 점검 필요)")

    print("\n" + "=" * 100)
    print("PRECONDITION CHECK 완료")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
