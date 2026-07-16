"""Mickey 지식 서고 정합성 검증기 (Phase 1 Test Harness · v2).

검증 대상은 두 가지 성격을 가지며, 서로 다른 기준으로 검사한다:

1. **사용자 홈 (`~/.kiro/mickey/`)** — 개인 지식 그래프의 실체.
   Curator 가 계속 축적하므로 실제 지식이 최소 개수 이상 있어야 정상.

2. **프로젝트 원본 (`mickey/`)** — 모든 사용자에게 배포되는 seed 골격.
   개별 지식 파일(entries/patterns)은 원칙적으로 없어도 무방하며,
   seed 완결성(README + 프로토콜 + 각 INDEX + PROFILE + CURATOR-PROMPT)만
   확인하면 새 사용자가 install 후 Curator 워크플로를 즉시 시작할 수 있다.

사용법:
    python scripts/verify_mickey_home.py                    # 사용자 홈 (기본, --mode home)
    python scripts/verify_mickey_home.py --mode seed --path mickey    # 프로젝트 seed
    python scripts/verify_mickey_home.py --mode auto --path <경로>    # 자동 판정

--mode auto: 경로가 `~/.kiro/mickey` 로 해석되면 home, 그 외는 seed 로 판정.

Exit code:
    0 = 통과, 1 = 하나 이상 결함, 2 = 대상 경로 자체가 없음.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# Seed 완결성 검사에 필요한 최소 파일 목록.
# 이 목록만 있으면 새 사용자가 install 후 Curator 를 바로 돌릴 수 있다.
SEED_REQUIRED_FILES = [
    "README.md",
    "extended-protocols.md",
    "patterns/INDEX.md",
    "domain/INDEX.md",
    "domain/GRAPH.md",
    "domain/PROFILE.md",
    "domain/CURATOR-PROMPT.md",
]

# 사용자 홈 검사는 seed 조건 + 실제 축적된 지식 최소 개수를 추가로 요구한다.
HOME_MIN_MD_FILES = {
    "patterns": 2,        # INDEX + 최소 1개 패턴
    "domain/entries": 5,  # 승격된 entry 가 실질적으로 있어야 서고 의미가 있음
}

# 두 모드에서 공통으로 존재해야 하는 디렉토리.
COMMON_REQUIRED_DIRS = [
    "patterns",
    "domain",
    "domain/entries",   # 비어 있어도 디렉토리 자체는 존재해야 함 (Curator 가 파일을 이 안에 만듦)
]


def check_files_exist(root: Path, rel_files: list[str]) -> list[str]:
    """지정된 상대 경로 파일들의 존재 여부를 검사한다."""
    return [f"[missing file] {rel}" for rel in rel_files
            if not (root / rel).is_file()]


def check_dirs_exist(root: Path, rel_dirs: list[str]) -> list[str]:
    """지정된 상대 경로 디렉토리들의 존재 여부를 검사한다."""
    return [f"[missing dir]  {rel}" for rel in rel_dirs
            if not (root / rel).is_dir()]


def check_md_min_count(root: Path, dir_min: dict[str, int]) -> list[str]:
    """디렉토리별 최소 md 파일 개수를 검사한다."""
    issues: list[str] = []
    for rel, min_count in dir_min.items():
        path = root / rel
        if not path.is_dir():
            # 디렉토리 자체 부재는 별도 검사에서 잡히므로 여기선 스킵
            continue
        count = sum(1 for p in path.glob("*.md") if p.is_file())
        if count < min_count:
            issues.append(
                f"[insufficient] {rel}: md 파일 {count}개 < 최소 {min_count}개"
            )
    return issues


def verify_seed(root: Path) -> list[str]:
    """Seed 완결성 검사 — 개별 지식 파일 개수는 검사하지 않는다."""
    issues: list[str] = []
    issues.extend(check_dirs_exist(root, COMMON_REQUIRED_DIRS))
    issues.extend(check_files_exist(root, SEED_REQUIRED_FILES))
    return issues


def verify_home(root: Path) -> list[str]:
    """사용자 홈 검사 — seed 조건 + 실제 축적된 지식 최소 개수 요구."""
    issues: list[str] = []
    issues.extend(verify_seed(root))
    issues.extend(check_md_min_count(root, HOME_MIN_MD_FILES))
    return issues


def resolve_mode(mode: str, root: Path) -> str:
    """--mode auto 인 경우 경로로 실제 모드를 판정한다."""
    if mode != "auto":
        return mode
    home_mickey = (Path.home() / ".kiro" / "mickey").resolve()
    return "home" if root == home_mickey else "seed"


def parse_args() -> argparse.Namespace:
    """CLI 인자 파싱."""
    parser = argparse.ArgumentParser(
        description="Mickey 지식 서고 정합성 검증기 (seed / home 두 모드)",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / ".kiro" / "mickey",
        help="검증 대상 서고 루트 (기본: ~/.kiro/mickey)",
    )
    parser.add_argument(
        "--mode",
        choices=["home", "seed", "auto"],
        default="auto",
        help="검증 모드 (기본: auto — 경로로 자동 판정)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.path.resolve()
    mode = resolve_mode(args.mode, root)

    print(f"=== verify_mickey_home [{mode}]: {root} ===")

    if not root.exists():
        print(f"[FAIL] 대상 경로가 존재하지 않음: {root}")
        return 2

    if mode == "seed":
        issues = verify_seed(root)
    else:
        issues = verify_home(root)

    if not issues:
        print(f"[PASS] {mode} 검증 통과")
        return 0

    print(f"[FAIL] {mode} 검증 실패 · 결함 {len(issues)}건:")
    for line in issues:
        print(f"  - {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
