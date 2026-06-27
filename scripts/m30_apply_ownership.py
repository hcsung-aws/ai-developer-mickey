"""
Mickey 30 — Source ownership 규칙 적용 (safe-batch-replace 4-step 8세대).

변경 대상:
1. 글로벌 ~/.kiro/mickey/extended-protocols.md
   - §17 Pre-staged Apply 5단계 직후 "Source 프로젝트 ownership" 섹션 추가
   - §3 "정리 행동" 에 staging ownership 필터링 한 줄 추가
2. repo mickey/extended-protocols.md (글로벌 변경 후 복사)
3. 글로벌 _curator-staging/ 3건의 메타데이터 보강 (Source 프로젝트명 추가)

각 변경은 count-1 guard + backup (.m30-bak) + post-check 검증.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

# Windows cp949 환경 대응 (adaptive.md #8)
sys.stdout.reconfigure(encoding="utf-8")

HOME_KIRO_MICKEY = Path.home() / ".kiro" / "mickey"
REPO_ROOT = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")

GLOBAL_PROTOCOLS = HOME_KIRO_MICKEY / "extended-protocols.md"
REPO_PROTOCOLS = REPO_ROOT / "mickey" / "extended-protocols.md"
STAGING_DIR = HOME_KIRO_MICKEY / "_curator-staging"

# ─────────────────────────────────────────────────────────────
# 변경 1: §17 새 섹션 (Source 프로젝트 ownership) 삽입
# ─────────────────────────────────────────────────────────────
ANCHOR_17_INSERT_BEFORE = "### staging 디렉토리 위치 (자동 감지)"

NEW_SECTION_17_OWNERSHIP = """### Source 프로젝트 ownership

각 staging 파일은 **Source 프로젝트**가 명시되며, 머지/폐기 결정 권한은 Source 프로젝트의 Mickey 만 보유한다. 다른 프로젝트의 Mickey 가 외부 source 의 staging 을 결정·변경하지 못하도록 보장하는 ownership 가드.

#### Source 태그 형식

staging 파일의 메타데이터 줄은 다음 형식을 사용한다:

```
> Pre-staged by Knowledge Curator at <ISO8601>, Source: <project-name> Mickey N
```

- `<project-name>`: Source 프로젝트 루트 디렉토리명 (예: `gamejob_crawler`, `vision-math-helper`)
- `<N>`: Source 프로젝트의 해당 시점 Mickey 번호

글로벌 `~/.kiro/mickey/_curator-staging/` 의 모든 항목은 본 형식이 **필수**. 프로젝트 `_curator-staging/` 도 권장.

#### ownership 규칙

| 상황 | 행동 |
|------|------|
| 본 프로젝트가 Source 인 staging | 머지/폐기 결정 가능. 사용자 단일 응답 요청 |
| 외부 프로젝트가 Source 인 staging | **skip** — 내용 결정 금지. 메타데이터 보강(Source 식별 가능하게)은 가능 |
| Source 미명시 staging | 본문 분석으로 Source 추정 → 메타데이터 보강만 수행. 결정은 추정된 Source 프로젝트에 위임 |

#### 엔트로피 체크와의 연동

세션 시작 시 §3 엔트로피 체크에서 staging dangling 점검 시 ownership 필터링 적용:
- 본 프로젝트 source 항목만 사용자 결정 요청
- 외부 source 항목은 카운트만 보고 (3세션 이상 dangling 시에도 자동 폐기 금지 — Source 프로젝트만 폐기 가능)

"""

# ─────────────────────────────────────────────────────────────
# 변경 2: §3 "정리 행동" 마지막 줄 다음에 한 줄 추가
# ─────────────────────────────────────────────────────────────
ANCHOR_3_TAIL = '- 오래된 auto_notes → "이 내용이 여전히 유효한지" 사용자에게 확인'
NEW_LINE_3_OWNERSHIP = (
    '- 오래된 auto_notes → "이 내용이 여전히 유효한지" 사용자에게 확인\n'
    "- staging dangling 점검 시 ownership 필터링 적용 (§17 참조). "
    "외부 source 항목은 skip + 카운트만 보고"
)

# ─────────────────────────────────────────────────────────────
# 변경 3: staging 3건 메타데이터 (Source 보강)
# ─────────────────────────────────────────────────────────────
STAGING_UPDATES = [
    (
        "pat-plan-implement-verify-trisection.md",
        "> Pre-staged by Knowledge Curator at 2026-06-26T15:57, Source: Mickey 32",
        "> Pre-staged by Knowledge Curator at 2026-06-26T15:57, "
        "Source: gamejob_crawler Mickey 32",
    ),
    (
        "pat-handoff-unresolved-trigger-marker.md",
        "> Pre-staged by Knowledge Curator at 2026-06-23T20:26, Source: Mickey 13",
        "> Pre-staged by Knowledge Curator at 2026-06-23T20:26, "
        "Source: vision-math-helper Mickey 13",
    ),
    (
        "pat-solution-bypass-vs-formal-resolution-separation.md",
        "> Pre-staged by Knowledge Curator at 2026-06-23T20:26, Source: Mickey 13",
        "> Pre-staged by Knowledge Curator at 2026-06-23T20:26, "
        "Source: vision-math-helper Mickey 13",
    ),
]


def file_hash(path: Path) -> str:
    """SHA-256 hash 의 첫 16자 (대문자)."""
    if not path.exists():
        return "MISSING"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def apply_change(path: Path, old: str, new: str, label: str) -> bool:
    """count-1 guard + backup + memory replace + post-check 패턴.

    Returns:
        True if change applied successfully, False otherwise.
    """
    if not path.exists():
        print(f"  [FAIL] {label}: 파일 미존재")
        return False

    text = path.read_text(encoding="utf-8")
    count = text.count(old)

    if count != 1:
        print(f"  [FAIL] {label}: 매칭 횟수 {count} (정확히 1이어야 함)")
        return False

    # backup
    backup = path.with_suffix(path.suffix + ".m30-bak")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"  [BACKUP] {backup.name} 생성")

    # apply (메모리 내)
    new_text = text.replace(old, new, 1)
    path.write_text(new_text, encoding="utf-8", newline="\n")

    # post-check
    written = path.read_text(encoding="utf-8")
    if new in written and old not in written:
        print(f"  [PASS] {label} 적용 완료")
        return True
    print(f"  [FAIL] {label}: post-check 실패")
    return False


def insert_before(path: Path, anchor: str, new_block: str, label: str) -> bool:
    """anchor 직전에 new_block 삽입 (count-1 guard)."""
    if not path.exists():
        print(f"  [FAIL] {label}: 파일 미존재")
        return False

    text = path.read_text(encoding="utf-8")
    count = text.count(anchor)

    if count != 1:
        print(f"  [FAIL] {label}: anchor 매칭 {count} (정확히 1이어야 함)")
        return False

    backup = path.with_suffix(path.suffix + ".m30-bak")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"  [BACKUP] {backup.name} 생성")

    new_text = text.replace(anchor, new_block + anchor, 1)
    path.write_text(new_text, encoding="utf-8", newline="\n")

    written = path.read_text(encoding="utf-8")
    # 첫 줄(섹션 헤더)만으로 삽입 확인
    first_line_of_block = new_block.splitlines()[0]
    if first_line_of_block in written and written.count(anchor) == 1:
        print(f"  [PASS] {label} 삽입 완료")
        return True
    print(f"  [FAIL] {label}: post-check 실패")
    return False


def main() -> int:
    print("=" * 100)
    print("M30 OWNERSHIP RULE APPLY (safe-batch-replace 4-step 8세대)")
    print("=" * 100)

    all_ok = True

    # ─── 단계 1: 글로벌 extended-protocols.md ───
    print(f"\n[1] 글로벌 extended-protocols.md 변경")
    print(f"    hash before: {file_hash(GLOBAL_PROTOCOLS)}")

    print("\n  1a. §17 Source 프로젝트 ownership 섹션 삽입")
    ok = insert_before(
        GLOBAL_PROTOCOLS,
        ANCHOR_17_INSERT_BEFORE,
        NEW_SECTION_17_OWNERSHIP,
        "§17 신규 섹션",
    )
    all_ok = all_ok and ok

    print("\n  1b. §3 정리 행동 한 줄 추가")
    ok = apply_change(
        GLOBAL_PROTOCOLS,
        ANCHOR_3_TAIL,
        NEW_LINE_3_OWNERSHIP,
        "§3 ownership 한 줄",
    )
    all_ok = all_ok and ok

    print(f"\n    hash after: {file_hash(GLOBAL_PROTOCOLS)}")

    # ─── 단계 2: repo extended-protocols.md (글로벌 복사) ───
    print(f"\n[2] repo extended-protocols.md 동기화 (글로벌 → repo)")
    print(f"    hash before: {file_hash(REPO_PROTOCOLS)}")

    backup_repo = REPO_PROTOCOLS.with_suffix(REPO_PROTOCOLS.suffix + ".m30-bak")
    if not backup_repo.exists():
        shutil.copy2(REPO_PROTOCOLS, backup_repo)
        print(f"  [BACKUP] {backup_repo.name} 생성")

    # 글로벌 → repo 단순 복사 (양쪽 동일 변경 보장)
    shutil.copy2(GLOBAL_PROTOCOLS, REPO_PROTOCOLS)
    g_hash_after = file_hash(GLOBAL_PROTOCOLS)
    r_hash_after = file_hash(REPO_PROTOCOLS)

    if g_hash_after == r_hash_after:
        print(f"  [PASS] 동기화 완료 (양쪽 hash {g_hash_after})")
    else:
        print(f"  [FAIL] hash 불일치: 글로벌 {g_hash_after} vs repo {r_hash_after}")
        all_ok = False

    # ─── 단계 3: staging 3건 메타데이터 보강 ───
    print(f"\n[3] 글로벌 staging 3건 메타데이터 보강 (Source 프로젝트명 추가)")
    for fname, old_meta, new_meta in STAGING_UPDATES:
        fpath = STAGING_DIR / fname
        print(f"\n  3.{fname}")
        ok = apply_change(fpath, old_meta, new_meta, f"메타데이터 보강 ({fname})")
        all_ok = all_ok and ok

    # ─── 최종 판정 ───
    print("\n" + "=" * 100)
    if all_ok:
        print("M30 OWNERSHIP RULE APPLY: 전체 PASS")
    else:
        print("M30 OWNERSHIP RULE APPLY: 일부 FAIL — 백업으로 rollback 검토 필요")
    print("=" * 100)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
