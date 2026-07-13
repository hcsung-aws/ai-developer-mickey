"""pytest 설정 - scripts/ 를 sys.path 에 추가하여 mickey_graph 임포트 가능.

프로젝트 루트에서 `pytest scripts/tests/` 실행 시에도 정상 동작하도록 보장한다.
"""

from __future__ import annotations

import sys
from pathlib import Path

# scripts/ 를 sys.path 에 추가 (mickey_graph 패키지 임포트용)
SCRIPTS_DIR = Path(__file__).parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
