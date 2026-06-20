"""ai-developer-mickey.json 글로벌(활성)/repo 동기화 검증 + 메타 출력

- 두 파일의 hash, byte, JSON parse 검증
- prompt 필드의 줄 수, 길이 출력
- 두 파일이 다르면 첫 차이 위치 + 컨텍스트
"""
import hashlib
import json
from pathlib import Path

ACTIVE = Path.home() / '.kiro' / 'agents' / 'ai-developer-mickey.json'
REPO = Path(r'C:\Users\hcsung\work\kiro\ai-developer-mickey\examples\ai-developer-mickey.json')


def measure(path: Path) -> dict:
    """파일 통계와 prompt 본문 메타 반환."""
    data = path.read_bytes()
    parsed = json.loads(data)
    prompt = parsed.get('prompt', '')
    return {
        'path': str(path),
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'name': parsed.get('name'),
        'tools': parsed.get('tools'),
        'allowedTools': parsed.get('allowedTools'),
        'prompt_lines': prompt.count('\n') + (1 if prompt and not prompt.endswith('\n') else 0),
        'prompt_len': len(prompt),
        'prompt_first_line': prompt.split('\n', 1)[0] if prompt else '',
        'data': data,
    }


def first_diff(a: bytes, b: bytes) -> int:
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    if len(a) != len(b):
        return n
    return -1


def main():
    a = measure(ACTIVE)
    r = measure(REPO)

    print(f"Active: bytes={a['bytes']}, sha256={a['sha256']}")
    print(f"Repo:   bytes={r['bytes']}, sha256={r['sha256']}")
    print()
    print(f"Active.name='{a['name']}', tools={a['tools']}, allowedTools={a['allowedTools']}")
    print(f"Repo.name  ='{r['name']}', tools={r['tools']}, allowedTools={r['allowedTools']}")
    print()
    print(f"Active.prompt: lines={a['prompt_lines']}, len={a['prompt_len']}")
    print(f"Repo.prompt:   lines={r['prompt_lines']}, len={r['prompt_len']}")
    print(f"Active.prompt[0]: {a['prompt_first_line']!r}")
    print(f"Repo.prompt[0]:   {r['prompt_first_line']!r}")
    print()

    if a['sha256'] == r['sha256']:
        print('OK: hash match (active and repo are identical)')
        return

    print('FAIL: hash mismatch')
    pos = first_diff(a['data'], r['data'])
    print(f'First diff position: {pos}')
    if pos >= 0:
        start = max(0, pos - 30)
        end = pos + 60
        print(f'Active[{start}:{end}]: {a["data"][start:end]!r}')
        print(f'Repo  [{start}:{end}]: {r["data"][start:end]!r}')


if __name__ == '__main__':
    main()
