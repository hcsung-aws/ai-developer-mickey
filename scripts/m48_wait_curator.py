# -*- coding: utf-8 -*-
"""M48: 고아가 된(호출 셸 타임아웃) Curator 자식 프로세스의 완주 대기 + 결과 실측.

배경: invoke_curator.py를 serena execute_shell_command로 실행했다가 도구
타임아웃(240s)으로 호출 측만 끊김. 자식 kiro-cli(Curator)는 계속 실행 중 —
죽이지 않고 완주를 기다린 뒤 staging/락/리포트를 디스크 실측으로 판정한다.

1회 호출당 최대 WAIT_CHUNK 초 대기 (도구 타임아웃 회피 — 필요 시 재호출).
"""
import sys
import time
from pathlib import Path

import psutil

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

CURATOR_PID = int(sys.argv[1]) if len(sys.argv) > 1 else 27016
WAIT_CHUNK = 120  # 초 — 호출 도구 타임아웃보다 짧게
STAGING = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\_curator-staging")


def curator_alive() -> bool:
    """pid 존재 + cmdline이 knowledge-curator인지 확인 (pid 재사용 오판 방지)."""
    try:
        p = psutil.Process(CURATOR_PID)
        return "knowledge-curator" in " ".join(p.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def main() -> None:
    deadline = time.time() + WAIT_CHUNK
    while time.time() < deadline:
        if not curator_alive():
            print(f"[EXITED] Curator(pid={CURATOR_PID}) 종료됨")
            break
        time.sleep(5)
    else:
        print(f"[RUNNING] Curator(pid={CURATOR_PID}) 아직 실행 중 — 재호출 필요")

    # 디스크 실측: staging 산출물 + 리포트 + 락 상태 파일
    print("\n--- staging 목록 ---")
    if STAGING.exists():
        for p in sorted(STAGING.rglob("*")):
            if p.is_file():
                print(f"  {p.relative_to(STAGING)}  ({p.stat().st_size}B)")
    lock_state = STAGING / ".curation.lock" / "owner.json"
    if lock_state.exists():
        print("\n--- 락 owner.json ---")
        print(lock_state.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
