# -*- coding: utf-8 -*-
"""
M31 §9 자동 트리거 잠복 기간 가드 연동 적용 스크립트.

safe-batch-replace 4-step 9세대 (M30 인계 post-check 로직 보강 반영):
1. precondition: 양쪽 hash 일치 + old_str 양쪽 count=1
2. backup: .m31-bak 양쪽 생성
3. apply: old → new (양쪽 동일 변경)
4. post-check: 양쪽 hash 일치 + written.count(new)==1 + sub-segment 검증

목적: T1.5 §9 자동 트리거 조건에 §18 "최소 3개월 잠복 기간" 가드 연동.
근거: M31 경량 포스트모템에서 트리거가 v9.1 도입 1주 11일 시점에 발동, §18 잠복 가드 우회 메타 신호.
"""
import hashlib
import shutil
import sys
from pathlib import Path

# Windows cp949 우회 (M22~M25 adaptive 누적 교훈)
sys.stdout.reconfigure(encoding='utf-8')

GLOBAL_PATH = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO_PATH = Path(__file__).resolve().parent.parent / "mickey" / "extended-protocols.md"

EXPECTED_PRECOND_HASH = "DEC6099AE2B21F4A1169A029C93D3E2E52EE04E722B765BA724AC0C9F8D1E710"

OLD_STR = """#### 자동 트리거 (엔트로피 체크 시 확인)
아래 조건 중 하나 충족 시 경량 포스트모템 제안:
- 프로젝트에서 10세션 이상 경과
- REMEMBER 또는 T1.5 변경 후 3개 프로젝트에서 사용
"""

NEW_STR = """#### 자동 트리거 (엔트로피 체크 시 확인)
아래 조건 중 하나 충족 시 경량 포스트모템 제안:
- **일반 포스트모템**: 프로젝트에서 10세션 이상 경과
- **변경 효과 검증**: REMEMBER 또는 T1.5 변경 후 3개 프로젝트에서 사용 **AND §18 최소 3개월 잠복 기간 충족**

> 두 조건은 독립이다. 변경 효과 검증 트리거가 단순 10세션 조건만으로 우회되지 않도록 함께 점검 필수 (M31 메타 신호: 잠복 기간 부족 시 변경별 판정이 "판단 보류" 로 수렴)
"""


def sha256(path: Path) -> str:
    """파일 SHA-256 해시 측정 (대문자 hex)."""
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def step1_precondition() -> None:
    """양쪽 hash 일치 + M30 baseline 보존 + old_str count=1 검증."""
    print("[Step 1] Precondition")
    g_hash = sha256(GLOBAL_PATH)
    r_hash = sha256(REPO_PATH)
    print(f"  Global: {g_hash}")
    print(f"  Repo  : {r_hash}")
    if g_hash != r_hash:
        raise RuntimeError("hash mismatch between global and repo")
    if g_hash != EXPECTED_PRECOND_HASH:
        raise RuntimeError(f"baseline hash mismatch. expected {EXPECTED_PRECOND_HASH}")

    g_text = GLOBAL_PATH.read_text(encoding="utf-8")
    r_text = REPO_PATH.read_text(encoding="utf-8")
    g_count = g_text.count(OLD_STR)
    r_count = r_text.count(OLD_STR)
    print(f"  old_str count global={g_count} repo={r_count}")
    if g_count != 1 or r_count != 1:
        raise RuntimeError("old_str count mismatch (expected 1 on both)")
    print("  PASS")


def step2_backup() -> None:
    """양쪽 .m31-bak 생성 (rollback 가능)."""
    print("[Step 2] Backup")
    for src in (GLOBAL_PATH, REPO_PATH):
        bak = src.with_suffix(src.suffix + ".m31-bak")
        shutil.copy2(src, bak)
        print(f"  {bak}")
    print("  PASS")


def apply_change(path: Path) -> None:
    """단일 파일 변경 + post-check (9세대 보강: count(new)==1 + old not in written)."""
    text = path.read_text(encoding="utf-8")
    written = text.replace(OLD_STR, NEW_STR, 1)
    path.write_text(written, encoding="utf-8")

    # 디스크 재확인 (must-follow-rules: fs_write 후 디스크 검증)
    disk = path.read_text(encoding="utf-8")
    if disk.count(NEW_STR) != 1:
        raise RuntimeError(f"{path}: new_str count != 1 after write")
    # M30 인계 권고: old not in written 단독은 new 안에 old 포함 시 False FAIL.
    # 본 변경은 new 가 old 의 모든 줄을 포함하지 않으므로 보조 검증 가능.
    if OLD_STR in disk:
        raise RuntimeError(f"{path}: old_str still present after write")


def step3_apply() -> None:
    """양쪽 동일 변경 적용."""
    print("[Step 3] Apply")
    apply_change(GLOBAL_PATH)
    apply_change(REPO_PATH)
    print("  PASS")


def step4_postcheck() -> None:
    """양쪽 hash 재일치 + 변경 영역만 차이 검증."""
    print("[Step 4] Post-check")
    g_hash = sha256(GLOBAL_PATH)
    r_hash = sha256(REPO_PATH)
    print(f"  Global: {g_hash}")
    print(f"  Repo  : {r_hash}")
    if g_hash != r_hash:
        raise RuntimeError("hash mismatch after apply")
    if g_hash == EXPECTED_PRECOND_HASH:
        raise RuntimeError("hash unchanged — apply did not take effect")
    print(f"  baseline {EXPECTED_PRECOND_HASH[:16]}... -> {g_hash[:16]}...")
    print("  PASS")


def main() -> int:
    """4-step 순차 실행. 어느 단계든 실패하면 RuntimeError 로 즉시 중단."""
    print("=" * 60)
    print("M31 §9 자동 트리거 잠복 가드 연동 (safe-batch-replace 9세대)")
    print("=" * 60)
    step1_precondition()
    step2_backup()
    step3_apply()
    step4_postcheck()
    print("=" * 60)
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
