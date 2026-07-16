"""잔존 파일 삭제 전 백업 zip 존재·크기 확인 스크립트.

Phase 2b 마지막 정리 단계에서 백업 안전망을 재확인하기 위한 용도.
"""

from __future__ import annotations

import pathlib
import sys

BACKUPS = [
    "power-mickey.pre-v10-bak.zip",
]


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    fail = 0
    for rel in BACKUPS:
        target = root / rel
        if target.exists() and target.stat().st_size > 0:
            print(f"[ OK ] {rel} : {target.stat().st_size} bytes")
        else:
            print(f"[FAIL] {rel} : 없음 또는 0바이트")
            fail += 1
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
