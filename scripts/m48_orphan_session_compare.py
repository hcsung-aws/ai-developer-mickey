# -*- coding: utf-8 -*-
"""M48: 미아 세션 파일 2건 vs 소속 프로젝트 기존 파일 비교 (C 항목 판단 자료).

각 쌍에 대해 크기/수정시각/sha256 + 내용 diff 요약을 출력한다.
동일하면 미아 쪽 안전 삭제 가능, 다르면 사용자 최종 결정용 분석 자료 제공.

리포트는 PowerShell 리다이렉트 인코딩 함정(utf-8→cp949→UTF-16 mojibake)을 피하기 위해
Python이 직접 utf-8 파일로 기록한다 (M48 §22 발동 후 수정).
"""
import difflib
import hashlib
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

REPORT = Path(__file__).with_name("m48_orphan_compare_report.txt")
_report_lines = []


def emit(line: str) -> None:
    """콘솔 + 리포트 파일 양쪽에 기록 (파일이 진본)."""
    print(line)
    _report_lines.append(line)

PAIRS = [
    (
        Path(r"C:\Users\hcsung\work\kiro\MICKEY-7-SESSION.md"),
        Path(r"C:\Users\hcsung\work\kiro\bvt-anjin-comparison\MICKEY-7-SESSION.md"),
    ),
    (
        Path(r"C:\Users\hcsung\work\kiro\MICKEY-24-SESSION.md"),
        Path(r"C:\Users\hcsung\work\kiro\epic-lore-benchmark\sessions\MICKEY-24-SESSION.md"),
    ),
]


def meta(p: Path) -> str:
    data = p.read_bytes()
    h = hashlib.sha256(data).hexdigest()[:16]
    mt = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    return f"{p}\n    size={len(data)}B  mtime={mt}  sha256={h}"


def main() -> None:
    for orphan, official in PAIRS:
        emit("=" * 70)
        emit(f"[미아]   {meta(orphan)}")
        emit(f"[정식]   {meta(official)}")
        a = orphan.read_text(encoding="utf-8", errors="replace").splitlines()
        b = official.read_text(encoding="utf-8", errors="replace").splitlines()
        if a == b:
            emit(">> 내용 동일 — 미아 삭제 안전")
            continue
        diff = list(difflib.unified_diff(a, b, lineterm="", n=1))
        # 통계: 미아에만 있는 줄(-), 정식에만 있는 줄(+)
        minus = [l for l in diff if l.startswith("-") and not l.startswith("---")]
        plus = [l for l in diff if l.startswith("+") and not l.startswith("+++")]
        emit(f">> 내용 상이 — 미아 {len(a)}줄 vs 정식 {len(b)}줄 | 미아 전용 {len(minus)}줄 / 정식 전용 {len(plus)}줄")
        emit("---- diff (미아 → 정식, 전체) ----")
        for line in diff:
            emit(line)
    REPORT.write_text("\n".join(_report_lines) + "\n", encoding="utf-8")
    print(f"\n[리포트 기록] {REPORT}")


if __name__ == "__main__":
    main()
