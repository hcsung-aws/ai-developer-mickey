"""
Mickey 21 — knowledge-curator.json 보정 스크립트.

목적:
- CURATOR-PROMPT.md 본문을 prompt 필드에 동기화 (inline)
- tools / allowedTools / toolsSettings 권한 보정 적용
- 활성 + repo 두 곳 동시 작성 (동기화 보장)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Windows cp949 회피
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 입력: 새 CURATOR-PROMPT.md 본문 (글로벌)
CURATOR_PROMPT_PATH = Path(r"C:\Users\hcsung\.kiro\mickey\domain\CURATOR-PROMPT.md")

# 출력: 두 곳에 동일 JSON 작성
TARGET_JSONS = [
    Path(r"C:\Users\hcsung\.kiro\agents\knowledge-curator.json"),                  # 활성
    Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\examples\knowledge-curator.json"),  # repo
]


def build_curator_config(prompt_text: str) -> dict:
    """Mickey 21 보정안에 따른 knowledge-curator agent JSON 구성."""
    return {
        "name": "knowledge-curator",
        "description": (
            "Mickey 세션 종료 시 호출되는 지식 관리 에이전트. "
            "domain/ 와 adaptive.md 는 직접 수정, 그 외 (common_knowledge/, context_rule/, patterns/, REMEMBER) "
            "는 _curator-staging/ 에 초안을 작성하여 사용자 일괄 결정을 받는다 (Pre-staged Apply 패턴, Mickey 21)."
        ),
        "prompt": prompt_text,
        "tools": ["fs_read", "fs_write", "grep", "glob"],
        "toolAliases": {},
        "allowedTools": ["fs_read", "grep", "glob", "fs_write"],
        "toolsSettings": {
            "fs_write": {
                "allowedPaths": [
                    "~/.kiro/mickey/domain/**",
                    "**/context_rule/adaptive.md",
                    "**/_curator-staging/**",
                ],
                "deniedPaths": [
                    "**/.git/**",
                    "**/node_modules/**",
                    "**/.venv/**",
                    "**/credentials*",
                    "**/.env*",
                    "**/*.key",
                    "**/*.pem",
                ],
            }
        },
        "resources": [],
        "hooks": {},
    }


def main() -> int:
    if not CURATOR_PROMPT_PATH.exists():
        print(f"[ERROR] CURATOR-PROMPT.md not found: {CURATOR_PROMPT_PATH}", file=sys.stderr)
        return 1

    prompt_text = CURATOR_PROMPT_PATH.read_text(encoding="utf-8")
    config = build_curator_config(prompt_text)
    payload = json.dumps(config, ensure_ascii=False, indent=2)

    for target in TARGET_JSONS:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
        print(f"[OK] wrote {target} ({len(payload)} bytes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
