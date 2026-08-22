# -*- coding: utf-8 -*-
"""M43: mickey_lock + invoke_curator 테스트 하니스.

실제 kiro-cli 호출 없이 subprocess.run 을 가짜 Curator(monkeypatch)로 대체하여
run 흐름(락 → 실행 → diff 실측 → awaiting-merge)을 실 파일 IO로 검증한다.
락 경합/강제 진입/stale 정책은 mickey_lock 단위로 직접 검증.
"""
import subprocess
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import invoke_curator as ic
import mickey_lock as ml


# ── mickey_lock 단위 ──────────────────────────────────────────────
class TestMickeyLock:
    def test_acquire_release_roundtrip(self, tmp_path):
        lock = ml.acquire(tmp_path / "L", "a")
        assert lock.exists() and ml.status(lock)["owner"] == "a"
        ml.release(lock)
        assert ml.status(lock) is None

    def test_busy_raises_with_owner(self, tmp_path):
        ml.acquire(tmp_path / "L", "a")
        with pytest.raises(ml.LockBusyError, match="a"):
            ml.acquire(tmp_path / "L", "b")

    def test_force_takes_over(self, tmp_path):
        """사람 확인 후 강제 진입 — 선점 락을 제거하고 획득."""
        ml.acquire(tmp_path / "L", "dead")
        lock = ml.acquire(tmp_path / "L", "b", force=True)
        assert ml.owner_info(lock)["owner"] == "b"

    def test_no_auto_reclaim_by_default(self, tmp_path):
        """curation 정책: stale 이어도 자동 회수 금지 (human-in-the-loop)."""
        lock = ml.acquire(tmp_path / "L", "dead")
        import os
        old = time.time() - 999999
        os.utime(lock, (old, old))
        with pytest.raises(ml.LockBusyError):
            ml.acquire(tmp_path / "L", "b")  # auto_reclaim=False 기본

    def test_auto_reclaim_when_stale(self, tmp_path):
        """promote 정책: stale 초과 락은 자동 회수."""
        lock = ml.acquire(tmp_path / "L", "dead")
        import os
        old = time.time() - 999999
        os.utime(lock, (old, old))
        lock2 = ml.acquire(tmp_path / "L", "b", auto_reclaim=True)
        assert ml.owner_info(lock2)["owner"] == "b"

    def test_set_state_keeps_owner(self, tmp_path):
        lock = ml.acquire(tmp_path / "L", "a")
        ml.set_state(lock, "awaiting-merge")
        info = ml.status(lock)
        assert info["owner"] == "a" and info["state"] == "awaiting-merge"


# ── 경로 규약 ─────────────────────────────────────────────────────
class TestStagingDir:
    def test_standard_layout(self, tmp_path):
        (tmp_path / "MICKEY-1-SESSION.md").write_text("x", encoding="utf-8")
        assert ic.staging_dir(tmp_path) == tmp_path / "_curator-staging"

    def test_nonstandard_kiro_layout(self, tmp_path):
        d = tmp_path / ".kiro" / "mickey"
        d.mkdir(parents=True)
        (d / "MICKEY-1-SESSION.md").write_text("x", encoding="utf-8")
        assert ic.staging_dir(tmp_path) == tmp_path / ".kiro" / "_curator-staging"


# ── 스냅샷/diff (락·리포트 제외 규칙 포함) ────────────────────────
class TestSnapshotDiff:
    def test_excludes_lock_and_reports(self, tmp_path):
        staging = tmp_path / "_curator-staging"
        (staging / ".curation.lock").mkdir(parents=True)
        (staging / ".curation.lock" / "owner.json").write_text("{}", encoding="utf-8")
        (staging / "promote-report-1.txt").write_text("r", encoding="utf-8")
        (staging / "curator-invoke-report-1.txt").write_text("r", encoding="utf-8")
        (staging / "gd-x.md").write_text("bundle", encoding="utf-8")
        snap = ic.snapshot(staging)
        assert list(snap) == ["gd-x.md"]

    def test_diff_detects_new_and_modified(self, tmp_path):
        staging = tmp_path / "_curator-staging"
        staging.mkdir()
        f = staging / "gd-a.md"
        f.write_text("v1", encoding="utf-8")
        before = ic.snapshot(staging)
        time.sleep(0.01)
        f.write_text("v2", encoding="utf-8")
        import os
        os.utime(f, None)
        (staging / "ck-b.md").write_text("new", encoding="utf-8")
        lines = ic.diff_lines(before, ic.snapshot(staging))
        joined = "\n".join(lines)
        assert "+ ck-b.md" in joined and "* gd-a.md" in joined


# ── run 흐름 (가짜 Curator) ───────────────────────────────────────
@pytest.fixture
def project(tmp_path):
    (tmp_path / "MICKEY-9-SESSION.md").write_text("# log", encoding="utf-8")
    return tmp_path


def fake_kiro(staging_writes):
    """subprocess.run 대체 — Curator가 staging 파일을 쓰는 부작용을 흉내."""
    def _run(cmd, cwd=None, **kw):
        for rel, body in staging_writes:
            p = Path(cwd) / "_curator-staging" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout="curator ok", stderr="")
    return _run


class TestRunFlow:
    def test_run_full_flow_awaiting_merge(self, project, monkeypatch, capsys):
        monkeypatch.setattr(ic.shutil, "which", lambda _: "kiro-cli")
        monkeypatch.setattr(ic.subprocess, "run", fake_kiro([("gd-new.md", "b")]))
        rc = ic.do_run(project, project / "MICKEY-9-SESSION.md",
                       "tester", False, "knowledge-curator", 60)
        assert rc == 0
        # 완주 판정 = 디스크 실측: diff에 산출물 반영
        out = capsys.readouterr().out
        assert "+ gd-new.md" in out
        # 락은 해제되지 않고 머지 대기 상태
        info = ml.status(ic.lock_dir(project))
        assert info["state"] == "awaiting-merge"
        # 리포트 파일 생성
        assert list(ic.staging_dir(project).glob("curator-invoke-report-*.txt"))

    def test_run_busy_lock_blocks_without_force(self, project, monkeypatch, capsys):
        """코드 강제 지점: 락 선점 시 Curator는 실행조차 되지 않는다."""
        ml.acquire(ic.lock_dir(project), "other-session")
        called = []
        monkeypatch.setattr(ic.shutil, "which", lambda _: "kiro-cli")
        monkeypatch.setattr(ic.subprocess, "run",
                            lambda *a, **k: called.append(1))
        rc = ic.do_run(project, project / "MICKEY-9-SESSION.md",
                       "tester", False, "knowledge-curator", 60)
        assert rc == 2 and not called
        assert "BUSY" in capsys.readouterr().out

    def test_run_force_enters_despite_lock(self, project, monkeypatch):
        ml.acquire(ic.lock_dir(project), "crashed-session")
        monkeypatch.setattr(ic.shutil, "which", lambda _: "kiro-cli")
        monkeypatch.setattr(ic.subprocess, "run", fake_kiro([]))
        rc = ic.do_run(project, project / "MICKEY-9-SESSION.md",
                       "tester", True, "knowledge-curator", 60)
        assert rc == 0
        assert ml.status(ic.lock_dir(project))["owner"] == "tester"

    def test_timeout_keeps_lock_for_fallback(self, project, monkeypatch, capsys):
        """타임아웃 시 락 유지 — 메인 세션이 락 아래서 직접 대행."""
        def _timeout(*a, **k):
            raise subprocess.TimeoutExpired(cmd="kiro-cli", timeout=60)
        monkeypatch.setattr(ic.shutil, "which", lambda _: "kiro-cli")
        monkeypatch.setattr(ic.subprocess, "run", _timeout)
        rc = ic.do_run(project, project / "MICKEY-9-SESSION.md",
                       "tester", False, "knowledge-curator", 60)
        assert rc == 1
        info = ml.status(ic.lock_dir(project))
        assert info is not None and info["state"] == "held"
        assert "TIMEOUT" in capsys.readouterr().out

    def test_curator_failure_keeps_lock(self, project, monkeypatch):
        monkeypatch.setattr(ic.shutil, "which", lambda _: "kiro-cli")
        monkeypatch.setattr(
            ic.subprocess, "run",
            lambda *a, **k: SimpleNamespace(returncode=1, stdout="", stderr="err"))
        rc = ic.do_run(project, project / "MICKEY-9-SESSION.md",
                       "tester", False, "knowledge-curator", 60)
        assert rc == 1
        assert ml.status(ic.lock_dir(project))["state"] == "held"

    def test_release_is_idempotent(self, project):
        assert ic.do_release(project) == 0  # 락 없어도 성공
        ml.acquire(ic.lock_dir(project), "a")
        assert ic.do_release(project) == 0
        assert ml.status(ic.lock_dir(project)) is None
