"""Phase 2b steering 파일 크기 · 필수 요소 간단 검증기.

목적: 각 steering 초안이 200줄(Clean Code) 이내인지, 최소 필수 요소(front matter,
v17 원문 대응 주석, H1)를 갖추었는지 빠르게 확인한다. Phase 2c 정식 검증기의
사전 단계로만 쓴다.

사용법:
    python scripts/m34_check_steering_size.py [파일1] [파일2] ...
    인자가 없으면 power-mickey/steering/*.md 전체 검사.
"""

from __future__ import annotations

import sys
from pathlib import Path

# 200줄 상한 (계획서 §6 Phase 2 CC)
LINE_LIMIT = 200

# 필수 요소 검사 조건 (문자열 부분 일치)
REQUIRED_MARKERS = {
    "front matter": "---\ninclusion:",
    "v17 원문 대응 주석": "v17 T1",
    "H1 헤더": "\n# ",
}


def check_one(path: Path) -> tuple[bool, list[str]]:
    """파일 하나에 대해 검사 수행. (통과 여부, 리포트 라인들) 반환."""
    if not path.exists():
        return False, [f"[FAIL] {path} : 파일 없음"]

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    line_count = len(lines)

    report: list[str] = []
    ok = True

    # 줄 수 검사
    if line_count > LINE_LIMIT:
        ok = False
        report.append(f"[FAIL] 줄 수 {line_count} > {LINE_LIMIT}")
    else:
        report.append(f"[ OK ] 줄 수 {line_count} / {LINE_LIMIT}")

    # 필수 요소 검사
    for label, marker in REQUIRED_MARKERS.items():
        if marker in text:
            report.append(f"[ OK ] {label} 존재")
        else:
            ok = False
            report.append(f"[FAIL] {label} 누락 (marker='{marker}')")

    return ok, report


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    steering_dir = root / "power-mickey" / "steering"

    if len(sys.argv) > 1:
        # 명시 인자
        targets = [Path(arg) for arg in sys.argv[1:]]
    else:
        # 기본: steering 디렉토리 전체
        targets = sorted(steering_dir.glob("*.md"))

    if not targets:
        print("검사 대상 없음.")
        return 1

    fail_count = 0
    for target in targets:
        rel = target.relative_to(root) if target.is_absolute() else target
        print(f"--- {rel} ---")
        ok, report = check_one(target)
        for line in report:
            print("  " + line)
        if not ok:
            fail_count += 1
        print()

    total = len(targets)
    passed = total - fail_count
    print(f"결과: PASS {passed} / FAIL {fail_count} / 총 {total}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
