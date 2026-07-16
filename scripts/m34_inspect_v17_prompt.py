"""v17 정본 agent JSON 의 프롬프트 구조를 상위 레벨로 요약한다.

Phase 2 진입 전, v17 프롬프트가 어떤 섹션으로 구성되는지 파악해
새 power-mickey/steering/ 7개 파일로의 분할 계획을 세우기 위한 정찰 유틸.
"""

# 목적: examples/ai-developer-mickey.json 에서 prompt 필드를 추출하고
# 헤더( '# ', '## ') 목차만 나열해 매핑 매트릭스 초안을 잡는다.

import io
import json
import re
import sys
from pathlib import Path

# Windows cp949 콘솔에서 유니코드(em dash 등) 인코딩 에러가 나지 않도록 utf-8 로 강제
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = Path("examples/ai-developer-mickey.json")


def main() -> int:
    if not SRC.exists():
        print(f"[error] {SRC} not found", file=sys.stderr)
        return 1

    data = json.loads(SRC.read_text(encoding="utf-8"))
    prompt = data.get("prompt", "") or ""

    print(f"== agent meta ==")
    print(f"name       : {data.get('name')}")
    print(f"version    : {data.get('version')}")
    desc = (data.get("description") or "").strip()
    print(f"description: {desc[:200]}")
    print(f"prompt len : {len(prompt)} chars, {prompt.count(chr(10)) + 1} lines")
    print()

    print("== prompt outline (# / ##) ==")
    for line_no, line in enumerate(prompt.splitlines(), start=1):
        # 코드 블록 안의 헤더는 건드리지 않도록 leading '```' 스킵은 생략(단순 개요라 필요 없음)
        if re.match(r"^#{1,3} ", line):
            print(f"{line_no:5d}  {line.rstrip()}")

    # 매핑 매트릭스 근거 확보용: prompt 전문을 별도 파일로 dump
    # (JSON 안에 escape 되어 있어 직접 grep 하기 불편하므로 풀어서 저장)
    out_path = Path("scripts/output/v17_prompt.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(prompt, encoding="utf-8")
    print(f"\n[dump] prompt saved to {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
