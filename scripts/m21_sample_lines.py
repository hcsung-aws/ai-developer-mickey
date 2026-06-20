"""
Mickey 21 — false positive 검증 표본 추출.

목적:
- 정량 측정에서 카운트된 'curator' / 'domain/entries' / '~/.kiro/mickey/' 매칭이
  실제 활용(호출/참조)인지 vs 단순 회상/논의인지 표본 확인.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

# Windows cp949 회피: stdout/stderr를 utf-8로 강제 설정.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TARGETS = [
    ("vision-math-helper M10/M11/M12", [
        Path(r"C:\Users\hcsung\work\kiro\vision-math-helper\.kiro\mickey\MICKEY-10-SESSION.md"),
        Path(r"C:\Users\hcsung\work\kiro\vision-math-helper\.kiro\mickey\MICKEY-11-SESSION.md"),
        Path(r"C:\Users\hcsung\work\kiro\vision-math-helper\.kiro\mickey\MICKEY-12-SESSION.md"),
    ]),
    ("gamejob_crawler M25/M26/M27/M28/M29", [
        Path(r"C:\Users\hcsung\work\gamejob_crawler\sessions\MICKEY-25-SESSION.md"),
        Path(r"C:\Users\hcsung\work\gamejob_crawler\sessions\MICKEY-26-SESSION.md"),
        Path(r"C:\Users\hcsung\work\gamejob_crawler\sessions\MICKEY-27-SESSION.md"),
        Path(r"C:\Users\hcsung\work\gamejob_crawler\sessions\MICKEY-28-SESSION.md"),
        Path(r"C:\Users\hcsung\work\gamejob_crawler\sessions\MICKEY-29-SESSION.md"),
    ]),
    ("code-analyze-helper M5/M6", [
        Path(r"C:\Users\hcsung\work\kiro\code-analyze-helper\MICKEY-5-SESSION.md"),
        Path(r"C:\Users\hcsung\work\kiro\code-analyze-helper\MICKEY-6-SESSION.md"),
    ]),
]

PATTERN = re.compile(r"curator|domain/entries|~/\.kiro/mickey|knowledge-organization|GRAPH\.md", re.IGNORECASE)

def main() -> None:
    for label, paths in TARGETS:
        print(f"\n{'='*100}")
        print(f"[{label}]")
        print(f"{'='*100}")
        for p in paths:
            if not p.exists():
                print(f"  (missing) {p.name}")
                continue
            try:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError as e:
                print(f"  (read fail) {p.name}: {e}")
                continue
            matches = [(i + 1, ln) for i, ln in enumerate(lines) if PATTERN.search(ln)]
            if not matches:
                print(f"  {p.name}: (no match)")
                continue
            print(f"\n  {p.name} ({len(matches)} matches, showing first 8):")
            for ln_num, line in matches[:8]:
                # 길면 자르기
                trimmed = line.strip()
                if len(trimmed) > 150:
                    trimmed = trimmed[:147] + "..."
                print(f"    L{ln_num}: {trimmed}")

if __name__ == "__main__":
    main()
