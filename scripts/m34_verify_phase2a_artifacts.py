"""Phase 2a 산출물 7건이 디스크에 정상 반영되었는지 확인한다.

세션 전환 시 IDE 에이전트 파일 쓰기 도구(fs_write 등)가 에디터 버퍼에만
반영되고 디스크에 flush 되지 않는 경우가 있어, 다음 세션 시작 전에
디스크 상태를 직접 검증한다 (must-follow-rules 지침).
"""

# 목적: 파일 존재 + 최소 크기 확인. 다음 세션(Phase 2b) 진입 전 안전망.

import io
import sys
from pathlib import Path

# Windows cp949 콘솔에서 em-dash 등 유니코드 문자 인코딩 실패 방지
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 산출물 목록: (경로, 최소 바이트, 설명)
ARTIFACTS = [
    ("docs/v2-to-v3-mapping.md", 5000, "이식 매트릭스"),
    ("power-mickey/POWER.md", 3000, "새 POWER.md 골격"),
    ("power-mickey/mcp.json", 100, "새 mcp.json (memorygraph 제거)"),
    ("IMPROVEMENT-PLAN-v10-power-migration.md", 8000, "계획서 (§8-b 신설 후)"),
    ("scripts/m34_inspect_v17_prompt.py", 800, "정찰 스크립트"),
    ("scripts/output/v17_prompt.md", 10000, "v17 T1 원문 dump"),
    (
        "session_history/2026-07-07-mickey-v10-migration-phase-2a.md",
        3000,
        "Phase 2a 세션 로그",
    ),
]


def main() -> int:
    ok = 0
    fail = 0
    for rel, min_size, desc in ARTIFACTS:
        p = Path(rel)
        if not p.exists():
            print(f"[FAIL] {rel} — 파일 없음 ({desc})")
            fail += 1
            continue
        size = p.stat().st_size
        if size < min_size:
            print(f"[FAIL] {rel} — 크기 {size} < 최소 {min_size} ({desc})")
            fail += 1
            continue
        print(f"[ OK ] {rel} — {size} bytes ({desc})")
        ok += 1

    print()
    print(f"결과: OK {ok} / FAIL {fail} / 총 {len(ARTIFACTS)}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
