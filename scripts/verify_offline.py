"""Rendered HTML 오프라인 자립 검증.

체크 항목:
    - placeholder 미치환 없음
    - vis-network 라이브러리 문자열 포함
    - graph data JSON 임베딩
    - CDN/외부 리소스 참조 없음 (src=... http)
    - 결과 크기 sanity check

사용법:
    python scripts/verify_offline.py [html-path]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DEFAULT_HTML = Path(__file__).parent / "output" / "mickey-graph-global.html"

REMAINING_PLACEHOLDERS = ["__VIS_NETWORK_JS__", "__GRAPH_DATA_JSON__", "__PAGE_TITLE__"]
# 외부 리소스 참조: src="http..." 또는 href="http..." 또는 import ... "http..."
EXTERNAL_PATTERN = re.compile(r'(?:src|href)\s*=\s*["\']https?://', re.IGNORECASE)


def _ensure_stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def verify(html_path: Path) -> int:
    _ensure_stdout_utf8()

    if not html_path.exists():
        print(f"[verify] ERROR: file not found: {html_path}", file=sys.stderr)
        return 1

    text = html_path.read_text(encoding="utf-8")
    size = html_path.stat().st_size

    problems: list[str] = []

    for ph in REMAINING_PLACEHOLDERS:
        if ph in text:
            problems.append(f"unsubstituted placeholder: {ph}")

    if "vis" not in text.lower():
        problems.append("vis-network library signature 'vis' not found")

    if size < 200_000:
        problems.append(f"file too small ({size:,} bytes) - vendor JS likely missing")

    external_matches = EXTERNAL_PATTERN.findall(text)
    if external_matches:
        problems.append(
            f"external resource references found ({len(external_matches)}): "
            f"{external_matches[:3]}"
        )

    if 'MICKEY_GRAPH' not in text:
        problems.append("graph data variable 'MICKEY_GRAPH' not found")

    # nodes/edges 카운트 sanity check
    nodes_count = text.count('"id":"')
    print(f"[verify] file: {html_path}")
    print(f"[verify] size: {size:,} bytes")
    print(f"[verify] approx nodes (\"id\":\" occurrences): {nodes_count}")

    if problems:
        print("[verify] FAIL:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print("[verify] OK: all offline-self-contained checks passed")
    return 0


def main(argv: list[str]) -> int:
    html_path = Path(argv[0]) if argv else DEFAULT_HTML
    return verify(html_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
