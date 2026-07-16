"""프로젝트 원본 mickey/README.md 를 사용자 홈 ~/.kiro/mickey/ 로 복사한다 (Phase 1 임시 유틸).

Phase 5 에서 install.ps1 / install.sh 가 mickey/ 디렉토리 전체 배포를 담당하도록
개편되면 본 스크립트는 삭제 대상이다.

원칙:
- shutil.copy2 로 메타데이터 보존 복사.
- 대상 디렉토리 미존재 시 실패 (사용자 홈 서고 자체가 없다는 뜻이므로 install 스크립트 선행 필요).
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT_ROOT / "mickey" / "README.md"
TARGET = Path.home() / ".kiro" / "mickey" / "README.md"


def main() -> int:
    if not SOURCE.is_file():
        print(f"[FAIL] 원본 없음: {SOURCE}")
        return 1
    if not TARGET.parent.is_dir():
        print(f"[FAIL] 사용자 홈 서고 미존재: {TARGET.parent}")
        print("       install.ps1 (또는 install.sh) 를 먼저 실행할 것")
        return 1

    shutil.copy2(SOURCE, TARGET)
    print(f"[ok] {SOURCE} -> {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
