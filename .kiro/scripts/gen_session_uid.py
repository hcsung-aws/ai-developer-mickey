# 세션 기록 규약(D-0717-1)용 UID 생성기
# 목적: session_history/ 내 기존 파일명과 충돌하지 않는 6자리 hex UID를 생성한다.
# 사용: python .kiro/scripts/gen_session_uid.py
import sys
import uuid
from pathlib import Path

# hook/스크립트 출력의 cp949 mojibake 방지 (Windows 콘솔 대비)
sys.stdout.reconfigure(encoding="utf-8")

# 프로젝트 루트 기준 session_history 디렉토리 위치 계산
HISTORY_DIR = Path(__file__).resolve().parents[2] / "session_history"


def existing_uids() -> set:
    """session_history 내 파일명에서 이미 사용된 UID를 수집한다.

    파일명 형식: YYYY-MM-DD-<uid>-log.md / YYYY-MM-DD-<uid>-handoff.md
    """
    uids = set()
    if not HISTORY_DIR.exists():
        return uids
    for f in HISTORY_DIR.glob("*.md"):
        parts = f.stem.split("-")
        # 날짜(3토큰) + uid + 종별(log/handoff) = 5토큰 이상일 때만 UID 추출
        if len(parts) >= 5 and parts[-1] in ("log", "handoff"):
            uids.add(parts[-2])
    return uids


def generate_uid() -> str:
    """기존 UID와 충돌하지 않는 6자리 hex UID를 반환한다."""
    used = existing_uids()
    while True:
        uid = uuid.uuid4().hex[:6]
        if uid not in used:
            return uid


if __name__ == "__main__":
    print(generate_uid())
