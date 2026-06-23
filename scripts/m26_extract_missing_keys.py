"""
M26 — 정상 에이전트(ai-developer-mickey)의 누락 키 값 추출.
curator 에 보충할 mcpServers / useLegacyMcpJson / model / resources / toolsSettings 값 확인.
"""

import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(os.path.expandvars("%USERPROFILE%"))
NORMAL = HOME / ".kiro" / "agents" / "ai-developer-mickey.json"
CURATOR = HOME / ".kiro" / "agents" / "knowledge-curator.json"

MISSING_KEYS = ["mcpServers", "useLegacyMcpJson", "model", "resources", "toolsSettings"]


def main() -> int:
    normal = json.loads(NORMAL.read_text(encoding="utf-8-sig"))
    curator = json.loads(CURATOR.read_text(encoding="utf-8-sig"))

    print("=== ai-developer-mickey (정상) — 누락 키들의 실제 값 ===\n")
    for key in MISSING_KEYS:
        present_in_curator = key in curator
        value = normal.get(key, "<NOT IN NORMAL>")
        print(f"[{key}]")
        print(f"  curator 에 있음: {present_in_curator}")
        if present_in_curator:
            print(f"  curator 값: {json.dumps(curator[key], ensure_ascii=False, indent=2)}")
        print(f"  ai-developer-mickey 값:")
        if isinstance(value, (dict, list)):
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            print(f"  {value!r}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
