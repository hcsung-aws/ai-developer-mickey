# -*- coding: utf-8 -*-
"""M32 사전 검증: extended-protocols.md 및 agent JSON baseline hash 확인."""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
GLOBAL_PROTO = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO_PROTO = ROOT / "mickey" / "extended-protocols.md"
AGENT_JSON = ROOT / "examples" / "ai-developer-mickey.json"
GLOBAL_AGENT = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"


def sha256(path: Path) -> str:
    """파일 SHA-256 해시 측정."""
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    """4 파일 hash + 존재 여부 보고."""
    files = [
        ("global protocols", GLOBAL_PROTO),
        ("repo protocols   ", REPO_PROTO),
        ("repo agent json  ", AGENT_JSON),
        ("global agent json", GLOBAL_AGENT),
    ]
    for label, path in files:
        if not path.exists():
            print(f"{label}: MISSING at {path}")
            continue
        print(f"{label}: {sha256(path)}  {path}")

    # 부가: agent JSON version/prompt 길이
    if AGENT_JSON.exists():
        data = json.loads(AGENT_JSON.read_text(encoding="utf-8"))
        prompt = data.get("prompt", "")
        print(f"\nagent JSON prompt length: {len(prompt)}")
        idx = prompt.find("**Version**:")
        if idx >= 0:
            print(f"agent JSON version snippet: {prompt[idx:idx+80]!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
