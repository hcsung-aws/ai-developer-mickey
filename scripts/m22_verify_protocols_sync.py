"""extended-protocols.md 글로벌/repo 동기화 검증 (Python 기반)

PowerShell Get-FileHash가 빈 결과를 반환하는 경우가 있어 Python으로 직접 측정.
- byte 수, line 수, SHA256 hash 출력
- 두 파일의 첫 차이 위치 출력 (불일치 시)
"""
import hashlib
from pathlib import Path

GLOBAL = Path.home() / '.kiro' / 'mickey' / 'extended-protocols.md'
REPO = Path(r'C:\Users\hcsung\work\kiro\ai-developer-mickey\mickey\extended-protocols.md')


def measure(path: Path) -> dict:
    """파일을 바이트 단위로 읽어 hash와 통계를 반환한다."""
    data = path.read_bytes()
    return {
        'path': str(path),
        'bytes': len(data),
        'lines': data.count(b'\n'),
        'sha256': hashlib.sha256(data).hexdigest(),
        'data': data,
    }


def first_diff(a: bytes, b: bytes) -> int:
    """두 바이트 시퀀스의 첫 다른 위치 반환. 동일하면 -1."""
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    if len(a) != len(b):
        return n
    return -1


def main():
    g = measure(GLOBAL)
    r = measure(REPO)

    print(f"Global: bytes={g['bytes']}, lines={g['lines']}, sha256={g['sha256']}")
    print(f"Repo:   bytes={r['bytes']}, lines={r['lines']}, sha256={r['sha256']}")

    if g['sha256'] == r['sha256']:
        print('OK: hash match')
        return

    print('FAIL: hash mismatch')
    pos = first_diff(g['data'], r['data'])
    print(f'First diff position: {pos}')

    # 차이 위치 주변 컨텍스트 출력 (40 바이트씩)
    if pos >= 0:
        start = max(0, pos - 20)
        end = pos + 40
        print(f'Global[{start}:{end}]: {g["data"][start:end]!r}')
        print(f'Repo  [{start}:{end}]: {r["data"][start:end]!r}')


if __name__ == '__main__':
    main()
