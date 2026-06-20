"""ai-developer-mickey.json의 prompt 필드를 별도 파일로 추출 (수정 작업용 임시 파일)

Step 5에서 prompt를 변경하기 위해 prompt 본문을 마크다운으로 꺼내 변경 영역을 식별한다.
"""
import json
from pathlib import Path

ACTIVE = Path.home() / '.kiro' / 'agents' / 'ai-developer-mickey.json'
OUT = Path(r'C:\Users\hcsung\work\kiro\ai-developer-mickey\scripts\_m22_prompt_dump.md')


def main():
    parsed = json.loads(ACTIVE.read_text(encoding='utf-8'))
    prompt = parsed.get('prompt', '')
    OUT.write_text(prompt, encoding='utf-8')
    print(f'Wrote {len(prompt)} chars, {prompt.count(chr(10)) + 1} lines to {OUT}')


if __name__ == '__main__':
    main()
