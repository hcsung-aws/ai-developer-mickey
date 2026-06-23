"""
M25 — Curator vs ai-developer-mickey JSON 비교 측정.
변형 B 가설(prompt 본문 길이) 정밀화를 위한 데이터 수집.
"""

import json
import os
import sys
from pathlib import Path

# Windows cp949 환경 대응 (adaptive.md Rule #8)
sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(os.path.expandvars("%USERPROFILE%"))
GLOBAL_AGENTS = HOME / ".kiro" / "agents"

TARGETS = {
    "curator (비정상)": GLOBAL_AGENTS / "knowledge-curator.json",
    "ai-developer-mickey (정상)": GLOBAL_AGENTS / "ai-developer-mickey.json",
}


def measure(label: str, path: Path) -> None:
    if not path.exists():
        print(f"[{label}] NOT FOUND: {path}")
        return

    raw = path.read_text(encoding="utf-8")
    file_bytes = path.stat().st_size

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[{label}] JSON parse FAIL: {e}")
        return

    prompt = obj.get("prompt", "")
    name = obj.get("name", "")
    description = obj.get("description", "")
    tools = obj.get("tools", [])
    allowed = obj.get("allowedTools", [])
    model = obj.get("model")

    print(f"=== {label} ===")
    print(f"  path: {path.name}")
    print(f"  file size: {file_bytes} bytes")
    print(f"  raw length: {len(raw)} chars")
    print(f"  name: {name}")
    print(f"  description length: {len(description)} chars")
    print(f"  prompt length: {len(prompt)} chars")
    print(f"  prompt lines: {prompt.count(chr(10)) + 1}")
    # 코드블록 개수 (markdown ``` 페어)
    triple_backtick = prompt.count("```")
    print(f"  prompt code blocks: {triple_backtick // 2} (triple-backtick pairs)")
    print(f"  tools: {tools}")
    print(f"  allowedTools: {allowed}")
    print(f"  model: {model}")
    # 한글/비-ASCII 문자 비율 (인코딩 가설용)
    non_ascii = sum(1 for ch in prompt if ord(ch) > 127)
    pct = (non_ascii / len(prompt) * 100) if prompt else 0.0
    print(f"  non-ASCII in prompt: {non_ascii} chars ({pct:.1f}%)")
    print()


def main() -> int:
    for label, path in TARGETS.items():
        measure(label, path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
