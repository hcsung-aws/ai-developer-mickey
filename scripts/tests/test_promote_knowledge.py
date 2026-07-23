# -*- coding: utf-8 -*-
"""promote_knowledge.py WELC 테스트.

가짜 글로벌 루트(MICKEY_GLOBAL_ROOT 리다이렉트) + 가짜 프로젝트를 tmp_path에
구성하여, 승격 트랜잭션의 전 분기(정상/충돌/롤백/락)를 실 파일 IO로 검증한다.
실제 ~/.kiro/mickey/ 는 건드리지 않는다 (installer-seed-semantics 패턴).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

import pytest

import promote_knowledge as pk

SCRIPT = Path(__file__).parent.parent / "promote_knowledge.py"


# ── fixtures ──────────────────────────────────────────────────────
GRAPH_MD = """# Knowledge Graph

## Nodes

| ID | Title | Tags | Core | Path |
|----|-------|------|------|------|
| existing-entry | 기존 엔트리 | testing | 기존 지식 | entries/existing-entry.md |

## Edges

| From | To | Type | Note |
|------|-----|------|------|
| existing-entry | existing-entry | similar-to | self |

## Last Updated
2026-07-21 (이전 세션)
"""

INDEX_MD = """# Global Domain Knowledge INDEX

## Domain Map

| 트리거 | 파일 | 요약 |
|--------|------|------|
| 기존, 테스트 | entries/existing-entry.md | 기존 지식 |

## Last Updated
2026-07-21 (이전 세션)
"""

PROJECT_INDEX_MD = """# Common Knowledge INDEX

## Knowledge Map

| 트리거 | 파일 | 요약 |
|--------|------|------|
| 예시 | sample.md | 예시 |

## Last Updated
2026-07-21
"""


def make_bundle(mode="new", entry_path="entries/new-entry.md", base_hash="",
                edges=True, backlink=True) -> str:
    """gd-*.md 번들 텍스트 생성 도우미."""
    edge_section = (
        "| new-entry | existing-entry | similar-to | 테스트 연결 |\n" if edges else "")
    backlink_section = (
        "| 신규 지식 | ~/.kiro/mickey/domain/entries/new-entry.md | 힌트 |\n"
        if backlink else "")
    base = f"Base-Hash: {base_hash}\n" if base_hash else ""
    return f"""# 승격 번들: new-entry
> Pre-staged by Knowledge Curator

## Meta
Mode: {mode}
Entry-Path: {entry_path}
Source: test-project Mickey 1
{base}
<<<ENTRY-BODY
# 신규 엔트리

## Core
테스트용 지식이다.

## Tags
testing

## Content
```python
print("내부 펜스 충돌 검증")
```
ENTRY-BODY>>>

## Graph Node Row
| new-entry | 신규 엔트리 | testing | 테스트용 | entries/new-entry.md |

## Graph Edge Rows
{edge_section}
## Index Row
| 신규, 테스트 | entries/new-entry.md | 테스트용 지식 |

## Backlink Row
{backlink_section}"""


@pytest.fixture
def env(tmp_path, monkeypatch):
    """가짜 글로벌 루트 + 가짜 프로젝트 구성. (global_root, project, staging) 반환."""
    groot = tmp_path / "global"
    domain = groot / "domain" / "entries"
    domain.mkdir(parents=True)
    (groot / "domain" / "GRAPH.md").write_text(GRAPH_MD, encoding="utf-8")
    (groot / "domain" / "INDEX.md").write_text(INDEX_MD, encoding="utf-8")
    (domain / "existing-entry.md").write_text("# 기존\n", encoding="utf-8")

    project = tmp_path / "proj"
    (project / "common_knowledge").mkdir(parents=True)
    (project / "common_knowledge" / "INDEX.md").write_text(PROJECT_INDEX_MD, encoding="utf-8")
    (project / "MICKEY-1-SESSION.md").write_text("# s\n", encoding="utf-8")
    staging = project / "_curator-staging"
    staging.mkdir()

    monkeypatch.setenv("MICKEY_GLOBAL_ROOT", str(groot))
    return groot, project, staging


def run_promote(project: Path, extra=None) -> subprocess.CompletedProcess:
    """스크립트를 실 프로세스로 실행 (E2E 경로 검증)."""
    cmd = [sys.executable, str(SCRIPT), "--project", str(project),
           "--owner", "test-project Mickey 1"] + (extra or [])
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


# ── 파싱 ──────────────────────────────────────────────────────────
class TestParseBundle:
    def test_valid_bundle(self, tmp_path):
        f = tmp_path / "gd-new-entry.md"
        f.write_text(make_bundle(), encoding="utf-8")
        b = pk.parse_bundle(f)
        assert b.mode == "new"
        assert b.entry_path == "entries/new-entry.md"
        assert b.entry_id() == "new-entry"
        assert "내부 펜스 충돌 검증" in b.entry_body   # heredoc 마커가 ``` 펜스 보존
        assert b.node_row.startswith("| new-entry |")
        assert len(b.edge_rows) == 1
        assert b.index_row and b.backlink_row

    def test_missing_entry_body(self, tmp_path):
        f = tmp_path / "gd-bad.md"
        f.write_text("## Meta\nMode: new\n", encoding="utf-8")
        with pytest.raises(ValueError, match="ENTRY-BODY"):
            pk.parse_bundle(f)

    def test_augment_requires_base_hash(self, tmp_path):
        f = tmp_path / "gd-aug.md"
        f.write_text(make_bundle(mode="augment"), encoding="utf-8")
        with pytest.raises(ValueError, match="Base-Hash"):
            pk.parse_bundle(f)

    def test_path_traversal_rejected(self, tmp_path):
        f = tmp_path / "gd-evil.md"
        f.write_text(make_bundle(entry_path="entries/../../evil.md"), encoding="utf-8")
        with pytest.raises(ValueError, match="entries/"):
            pk.parse_bundle(f)


# ── 표 조작 ───────────────────────────────────────────────────────
class TestTableOps:
    def test_insert_rows_at_table_end(self):
        out = pk.insert_rows(GRAPH_MD, "Nodes", ["| n2 | t | tag | c | entries/n2.md |"])
        lines = out.splitlines()
        idx = lines.index("| n2 | t | tag | c | entries/n2.md |")
        assert lines[idx - 1].startswith("| existing-entry")  # 기존 행 바로 뒤
        assert "## Edges" in out                              # 섹션 구조 보존

    def test_replace_row(self):
        out = pk.replace_row(GRAPH_MD, "Nodes", "existing-entry",
                             "| existing-entry | 개정 | t | c | entries/existing-entry.md |")
        assert "| existing-entry | 개정 |" in out
        assert "기존 엔트리" not in out

    def test_replace_row_missing_raises(self):
        with pytest.raises(ValueError, match="행 없음"):
            pk.replace_row(GRAPH_MD, "Nodes", "nope", "| nope |")

    def test_set_last_updated(self):
        out = pk.set_last_updated(GRAPH_MD, "2026-07-22 (test promote)")
        assert "2026-07-22 (test promote)" in out
        assert "2026-07-21 (이전 세션)" not in out


# ── 락 ────────────────────────────────────────────────────────────
class TestLock:
    def test_acquire_and_release(self, tmp_path):
        lock = pk.acquire_lock(tmp_path, "owner-a")
        assert lock.exists() and (lock / "owner.json").exists()
        pk.release_lock(lock)
        assert not lock.exists()

    def test_busy_lock_raises(self, tmp_path):
        pk.acquire_lock(tmp_path, "owner-a")
        with pytest.raises(RuntimeError, match="owner-a"):
            pk.acquire_lock(tmp_path, "owner-b")

    def test_stale_lock_takeover(self, tmp_path):
        lock = pk.acquire_lock(tmp_path, "dead-owner")
        old = time.time() - pk.LOCK_STALE_SECONDS - 60
        import os
        os.utime(lock, (old, old))  # 비정상 종료 잔여 락 시뮬레이션
        lock2 = pk.acquire_lock(tmp_path, "owner-b")
        assert pk._lock_owner_info(lock2) == "owner-b"


# ── E2E: 정상 승격 ────────────────────────────────────────────────
class TestPromoteE2E:
    def test_new_entry_full_promotion(self, env):
        groot, project, staging = env
        (staging / "gd-new-entry.md").write_text(make_bundle(), encoding="utf-8")

        r = run_promote(project)
        assert r.returncode == 0, r.stdout + r.stderr

        # entry 생성 + 본문 보존
        entry = groot / "domain" / "entries" / "new-entry.md"
        assert entry.exists()
        assert "내부 펜스 충돌 검증" in entry.read_text(encoding="utf-8")
        # GRAPH: 노드 + 엣지 + Last Updated 명의
        graph = (groot / "domain" / "GRAPH.md").read_text(encoding="utf-8")
        assert "| new-entry | 신규 엔트리 |" in graph
        assert "| new-entry | existing-entry | similar-to |" in graph
        assert "test-project Mickey 1 promote" in graph
        # INDEX 행
        index = (groot / "domain" / "INDEX.md").read_text(encoding="utf-8")
        assert "| 신규, 테스트 | entries/new-entry.md |" in index
        # backlink (Domain Links 섹션 자동 생성 포함)
        pidx = (project / "common_knowledge" / "INDEX.md").read_text(encoding="utf-8")
        assert "## Domain Links" in pidx and "new-entry.md" in pidx
        # staging 정리 + 리포트 생성 + 락 해제
        assert not (staging / "gd-new-entry.md").exists()
        assert list(staging.glob("promote-report-*.txt"))
        assert not (groot / ".promote.lock").exists()

    def test_augment_with_matching_hash(self, env):
        groot, project, staging = env
        target = groot / "domain" / "entries" / "existing-entry.md"
        base = hashlib.sha256(target.read_bytes()).hexdigest()
        bundle = make_bundle(mode="augment", entry_path="entries/existing-entry.md",
                             base_hash=base, edges=False, backlink=False)
        # augment 는 노드 행 교체 — ID 를 기존 노드에 맞춤
        bundle = bundle.replace(
            "| new-entry | 신규 엔트리 | testing | 테스트용 | entries/new-entry.md |",
            "| existing-entry | 기존 엔트리 보강 | testing | 보강됨 | entries/existing-entry.md |")
        (staging / "gd-existing-entry.md").write_text(bundle, encoding="utf-8")

        r = run_promote(project)
        assert r.returncode == 0, r.stdout + r.stderr
        assert "테스트용 지식이다" in target.read_text(encoding="utf-8")  # 본문 교체됨
        graph = (groot / "domain" / "GRAPH.md").read_text(encoding="utf-8")
        assert "기존 엔트리 보강" in graph

    def test_dry_run_writes_nothing(self, env):
        groot, project, staging = env
        (staging / "gd-new-entry.md").write_text(make_bundle(), encoding="utf-8")
        before = (groot / "domain" / "GRAPH.md").read_text(encoding="utf-8")

        r = run_promote(project, ["--dry-run"])
        assert r.returncode == 0
        assert "[PLAN]" in r.stdout
        assert (groot / "domain" / "GRAPH.md").read_text(encoding="utf-8") == before
        assert (staging / "gd-new-entry.md").exists()  # staging 보존

    def test_empty_staging_ok(self, env):
        _, project, _ = env
        r = run_promote(project)
        assert r.returncode == 0
        assert "번들 없음" in r.stdout


# ── 충돌 (낙관적 동시성 제어) ─────────────────────────────────────
class TestConflicts:
    def test_new_conflicts_with_existing_node(self, env):
        groot, project, staging = env
        bundle = make_bundle(entry_path="entries/existing-entry.md", edges=False,
                             backlink=False)
        (staging / "gd-dup.md").write_text(bundle, encoding="utf-8")

        r = run_promote(project)
        assert r.returncode == 1                       # CONFLICT 잔여 → 비정상 종료 코드
        assert "[CONFLICT]" in r.stdout
        assert (staging / "gd-dup.md").exists()        # staging 보존 (재큐레이션 유도)

    def test_augment_base_hash_mismatch(self, env):
        groot, project, staging = env
        bundle = make_bundle(mode="augment", entry_path="entries/existing-entry.md",
                             base_hash="0" * 64, edges=False, backlink=False)
        (staging / "gd-stale.md").write_text(bundle, encoding="utf-8")

        r = run_promote(project)
        assert r.returncode == 1
        assert "Base-Hash 불일치" in r.stdout
        # 대상 파일 무변경 (타 세션 변경 보호)
        assert (groot / "domain" / "entries" / "existing-entry.md").read_text(
            encoding="utf-8") == "# 기존\n"

    def test_conflict_skips_but_others_apply(self, env):
        """번들 2개 중 1개 충돌 → 나머지 1개는 정상 승격 (부분 성공)."""
        groot, project, staging = env
        (staging / "gd-dup.md").write_text(
            make_bundle(entry_path="entries/existing-entry.md", edges=False,
                        backlink=False), encoding="utf-8")
        (staging / "gd-new-entry.md").write_text(make_bundle(), encoding="utf-8")

        r = run_promote(project)
        assert r.returncode == 1                       # 잔여 충돌 알림
        assert (groot / "domain" / "entries" / "new-entry.md").exists()
        assert not (staging / "gd-new-entry.md").exists()
        assert (staging / "gd-dup.md").exists()


# ── 무결성 실패 → 롤백 ────────────────────────────────────────────
class TestRollback:
    def test_dangling_edge_triggers_rollback(self, env):
        groot, project, staging = env
        bundle = make_bundle(backlink=False).replace(
            "| new-entry | existing-entry | similar-to | 테스트 연결 |",
            "| new-entry | ghost-node | similar-to | 존재하지 않는 노드 |")
        (staging / "gd-new-entry.md").write_text(bundle, encoding="utf-8")

        r = run_promote(project)
        assert r.returncode == 1
        assert "[ROLLBACK]" in r.stdout and "DANGLING" in r.stdout
        # 글로벌 상태 원복 확인
        graph = (groot / "domain" / "GRAPH.md").read_text(encoding="utf-8")
        assert "new-entry" not in graph.replace("existing-entry", "")
        assert not (groot / "domain" / "entries" / "new-entry.md").exists()
        assert (staging / "gd-new-entry.md").exists()  # staging 보존
        assert not (groot / ".promote.lock").exists()  # 락 해제 보장


# ── 락 경합 (프로세스 시맨틱) ─────────────────────────────────────
class TestLockContention:
    def test_promote_blocked_while_locked(self, env):
        groot, project, staging = env
        (staging / "gd-new-entry.md").write_text(make_bundle(), encoding="utf-8")
        pk.acquire_lock(groot, "other-session Mickey 9")  # 타 세션이 락 보유 중

        r = run_promote(project)
        assert r.returncode == 2                       # BUSY 전용 종료 코드
        assert "other-session Mickey 9" in r.stdout    # 보유자 식별 가능
        assert (staging / "gd-new-entry.md").exists()  # 아무것도 적용 안 됨
