"""
Mickey 30 — 변경 적용 후 종합 검증.

검증 항목:
1. 글로벌 / repo extended-protocols.md hash 일치 + 새 섹션·새 줄 존재
2. staging 3건의 Source 메타데이터가 새 형식 (project-name + Mickey N)
3. staging 3건의 본문은 메타데이터 줄 외 변경 없음 (backup 과 diff = 1줄)
4. backup 파일들 양쪽 모두 존재 (rollback 가능 확인)
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME_KIRO_MICKEY = Path.home() / ".kiro" / "mickey"
REPO_ROOT = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")

GLOBAL_PROTOCOLS = HOME_KIRO_MICKEY / "extended-protocols.md"
REPO_PROTOCOLS = REPO_ROOT / "mickey" / "extended-protocols.md"
STAGING_DIR = HOME_KIRO_MICKEY / "_curator-staging"

STAGING_NEW_META = {
    "pat-plan-implement-verify-trisection.md": (
        "> Pre-staged by Knowledge Curator at 2026-06-26T15:57, "
        "Source: gamejob_crawler Mickey 32"
    ),
    "pat-handoff-unresolved-trigger-marker.md": (
        "> Pre-staged by Knowledge Curator at 2026-06-23T20:26, "
        "Source: vision-math-helper Mickey 13"
    ),
    "pat-solution-bypass-vs-formal-resolution-separation.md": (
        "> Pre-staged by Knowledge Curator at 2026-06-23T20:26, "
        "Source: vision-math-helper Mickey 13"
    ),
}

# extended-protocols.md 변경 후 존재해야 할 주요 마커
PROTOCOLS_REQUIRED_MARKERS = [
    "### Source 프로젝트 ownership",  # §17 신규 섹션 헤더
    "글로벌 `~/.kiro/mickey/_curator-staging/` 의 모든 항목은 본 형식이 **필수**",  # 본문
    "staging dangling 점검 시 ownership 필터링 적용 (§17 참조)",  # §3 새 줄
]


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def diff_lines(a: Path, b: Path) -> tuple[int, list[str]]:
    """두 파일의 diff 줄 수 + diff 샘플 반환."""
    if not (a.exists() and b.exists()):
        return -1, []
    lines_a = a.read_text(encoding="utf-8").splitlines()
    lines_b = b.read_text(encoding="utf-8").splitlines()
    diffs = []
    for i, (la, lb) in enumerate(zip(lines_a, lines_b)):
        if la != lb:
            diffs.append(f"  L{i+1}: '{la[:60]}' vs '{lb[:60]}'")
    # length 차이도 카운트
    len_diff = abs(len(lines_a) - len(lines_b))
    return len(diffs) + len_diff, diffs[:5]


def main() -> int:
    print("=" * 100)
    print("M30 VERIFICATION (변경 적용 후 종합 검증)")
    print("=" * 100)

    all_ok = True

    # ─── [1] extended-protocols.md 양쪽 일치 + 새 마커 ───
    print("\n[1] extended-protocols.md 양쪽 동기화 + 변경 적용 검증")
    g_hash = file_hash(GLOBAL_PROTOCOLS)
    r_hash = file_hash(REPO_PROTOCOLS)
    print(f"  글로벌 hash: {g_hash}")
    print(f"  repo hash:   {r_hash}")
    if g_hash == r_hash:
        print(f"  [PASS] hash 일치")
    else:
        print(f"  [FAIL] hash 불일치")
        all_ok = False

    text = GLOBAL_PROTOCOLS.read_text(encoding="utf-8")
    for marker in PROTOCOLS_REQUIRED_MARKERS:
        if marker in text:
            print(f"  [PASS] 마커 존재: '{marker[:60]}...'")
        else:
            print(f"  [FAIL] 마커 누락: '{marker[:60]}...'")
            all_ok = False

    # ─── [2] staging 3건 메타데이터 + 본문 무결성 ───
    print(f"\n[2] staging 3건 검증")
    for fname, expected_meta in STAGING_NEW_META.items():
        fpath = STAGING_DIR / fname
        backup = fpath.with_suffix(fpath.suffix + ".m30-bak")
        print(f"\n  {fname}")

        if not fpath.exists():
            print("    [FAIL] 파일 미존재")
            all_ok = False
            continue

        # 메타데이터 검증
        content = fpath.read_text(encoding="utf-8")
        if expected_meta in content:
            print(f"    [PASS] 새 메타데이터 존재")
        else:
            print(f"    [FAIL] 새 메타데이터 누락")
            all_ok = False

        # 본문 무결성: backup 과 diff = 1줄 (메타데이터 줄만)
        if backup.exists():
            n_diff, samples = diff_lines(backup, fpath)
            if n_diff == 1:
                print(f"    [PASS] 본문 무결성 (diff 정확히 1줄 — 메타데이터만 변경)")
            else:
                print(f"    [FAIL] diff {n_diff}줄 — 본문 변경 의심")
                for s in samples:
                    print(s)
                all_ok = False
        else:
            print(f"    [WARN] backup 미존재 — rollback 불가")

    # ─── [3] 백업 파일 존재 확인 (rollback 가능성) ───
    print(f"\n[3] 백업 파일 존재 확인")
    backups_to_check = [
        GLOBAL_PROTOCOLS.with_suffix(GLOBAL_PROTOCOLS.suffix + ".m30-bak"),
        REPO_PROTOCOLS.with_suffix(REPO_PROTOCOLS.suffix + ".m30-bak"),
    ]
    for fname in STAGING_NEW_META:
        backups_to_check.append(
            (STAGING_DIR / fname).with_suffix(".md.m30-bak")
        )

    for bk in backups_to_check:
        if bk.exists():
            print(f"  [PASS] {bk.name}")
        else:
            print(f"  [FAIL] {bk.name} 미존재")
            all_ok = False

    # ─── [4] 최종 판정 ───
    print("\n" + "=" * 100)
    if all_ok:
        print("M30 VERIFICATION: 전체 PASS — 변경 적용 완료, rollback 가능 상태")
    else:
        print("M30 VERIFICATION: 일부 FAIL — 상세 확인 필요")
    print("=" * 100)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
