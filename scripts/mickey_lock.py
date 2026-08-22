# -*- coding: utf-8 -*-
"""M43: Mickey 공유 파일 락 모듈 (mkdir 원자성).

promote_knowledge.py(글로벌 승격 락)와 invoke_curator.py(프로젝트 curation 락)가
같은 메커니즘을 공유한다. 합치는 것은 코드이지 락 파일이 아니다 — 락 디렉토리
경로는 호출자가 스코프에 맞게 지정한다 (promote: 글로벌, curation: 프로젝트 로컬).

메커니즘:
  - 획득: Path.mkdir() — 이미 존재하면 FileExistsError. NTFS/POSIX 모두 원자적
  - 명의: 락 디렉토리 안 owner.json (owner, pid, acquired_at, state)
  - stale 정책은 호출자가 선택:
      auto_reclaim=True  → stale 초과 락을 자동 회수 후 재시도 (promote 방식)
      auto_reclaim=False → 자동 회수 없음. LockBusyError로 보고만 하고,
                           사람이 확인 후 force=True로만 강제 진입 (curation 방식)
"""
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

DEFAULT_STALE_SECONDS = 600  # promote 기본값 (M41과 동일)


class LockBusyError(RuntimeError):
    """락 선점 상태. 보유자/경과 시간을 담아 호출자가 사용자에게 보고할 수 있게 한다."""

    def __init__(self, lock_dir: Path, owner: str, age_seconds: float):
        self.lock_dir = lock_dir
        self.owner = owner
        self.age_seconds = age_seconds
        super().__init__(
            f"락 사용 중 (보유자: {owner}, 경과 {int(age_seconds)}s): {lock_dir}")


def acquire(lock_dir: Path, owner: str, *,
            stale_seconds: int = DEFAULT_STALE_SECONDS,
            auto_reclaim: bool = False,
            force: bool = False) -> Path:
    """락 획득. 성공 시 락 디렉토리 Path 반환, 선점 시 LockBusyError.

    - force: 선점 여부와 무관하게 기존 락을 제거하고 획득 (human-in-the-loop 강제 진입)
    - auto_reclaim: stale_seconds 초과 락만 자동 회수 (비정상 종료 잔여물 간주)
    """
    for attempt in (1, 2):
        try:
            lock_dir.mkdir(parents=True, exist_ok=False)  # 원자적 획득 지점
            _write_owner(lock_dir, owner, state="held")
            return lock_dir
        except FileExistsError:
            holder = owner_info(lock_dir)
            age = _age_seconds(lock_dir)
            reclaim = force or (auto_reclaim and age > stale_seconds)
            if reclaim and attempt == 1:
                shutil.rmtree(lock_dir, ignore_errors=True)
                continue  # 재시도 1회 — 그 사이 타 프로세스가 잡으면 정직하게 실패
            raise LockBusyError(lock_dir, holder.get("owner", "unknown"), age)
    raise LockBusyError(lock_dir, "unknown", 0)


def release(lock_dir: Path) -> None:
    """락 해제. 존재하지 않아도 조용히 성공 (멱등)."""
    shutil.rmtree(lock_dir, ignore_errors=True)


def set_state(lock_dir: Path, state: str) -> None:
    """보유 중인 락의 상태 갱신 (예: held → awaiting-merge). 명의는 유지."""
    info = owner_info(lock_dir)
    _write_owner(lock_dir, info.get("owner", "unknown"), state=state)


def status(lock_dir: Path) -> dict | None:
    """락 상태 조회. 미보유 시 None, 보유 시 owner.json + 경과 시간."""
    if not lock_dir.exists():
        return None
    info = owner_info(lock_dir)
    info["age_seconds"] = int(_age_seconds(lock_dir))
    return info


def owner_info(lock_dir: Path) -> dict:
    """owner.json 파싱. 손상/부재 시 unknown (락 존재 자체가 우선 증거)."""
    try:
        return json.loads((lock_dir / "owner.json").read_text(encoding="utf-8"))
    except Exception:
        return {"owner": "unknown"}


def _write_owner(lock_dir: Path, owner: str, *, state: str) -> None:
    (lock_dir / "owner.json").write_text(json.dumps({
        "owner": owner,
        "pid": os.getpid(),
        "acquired_at": datetime.now().isoformat(timespec="seconds"),
        "state": state,
    }, ensure_ascii=False), encoding="utf-8")


def _age_seconds(lock_dir: Path) -> float:
    try:
        return time.time() - lock_dir.stat().st_mtime
    except OSError:
        return 0.0
