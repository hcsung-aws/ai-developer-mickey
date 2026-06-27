# -*- coding: utf-8 -*-
# 목적: Curator JSON 의 prompt 본문 + 메타 통계 출력
# (PowerShell 따옴표 충돌 회피 — must-follow-rules)
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CURATOR_PATH = Path.home() / ".kiro" / "agents" / "knowledge-curator.json"
MICKEY_PATH = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"


def stats(name: str, prompt: str) -> None:
    """prompt 본문의 길이/줄/코드블록/blank 비율 등 메타 통계"""
    if prompt is None:
        print(f"[{name}] prompt is None")
        return
    lines = prompt.split("\n")
    code_fences = prompt.count("```")
    blank = sum(1 for ln in lines if ln.strip() == "")
    print(f"[{name}] chars={len(prompt)} lines={len(lines)} code_fences={code_fences} blanks={blank}")


def main() -> int:
    """양 prompt 본문 + 메타 통계 + Curator prompt 전문 dump"""
    mickey = json.loads(MICKEY_PATH.read_text(encoding="utf-8"))
    curator = json.loads(CURATOR_PATH.read_text(encoding="utf-8"))

    print("=" * 80)
    print("PROMPT META")
    print("=" * 80)
    stats("mickey ", mickey.get("prompt") or "")
    stats("curator", curator.get("prompt") or "")

    print()
    print("=" * 80)
    print("CURATOR PROMPT (full)")
    print("=" * 80)
    print(curator.get("prompt") or "<none>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
