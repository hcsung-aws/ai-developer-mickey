# -*- coding: utf-8 -*-
"""M43: Knowledge Curator 호출의 유일한 코드 진입점.

배경 (D-43 — 호출 코드화):
  M41이 쓰기 격리(staging), M42가 전송 안전(in-band)을 확보했으나, "같은
  프로젝트 동시 큐레이션 회피"는 지시(프롬프트) 기반이라 감지 수단이 없었다.
  본 스크립트는 락 검사를 호출과 같은 코드 경로에 내장한다 — 락을 잡지 못하면
  Curator가 아예 실행되지 않는다 (LLM 결정론적 하이브리드, promote와 동일 사상).

전송 경로:
  kiro-cli chat --agent knowledge-curator --no-interactive 를 직접 자식
  프로세스로 실행, stdout 파이프로 결과 수신. delegate의 전역 랑데부 저장소
  (.subagents + user_notified 선점 = crosstalk 원흉)를 경유하지 않음을
  m43_probe_headless_transport.py 로 실측 완료 (in-band + .subagents 무변화).

락 (mickey_lock 공유 모듈, promote 락과 코드 통합 — 파일은 스코프별 분리):
  - 위치: {프로젝트 staging}/.curation.lock/ (프로젝트 로컬)
  - 자동 회수 없음 — 선점 락 발견 시 보유자/경과 시간 보고 후 중단.
    사람이 확인한 뒤 --force 로만 강제 진입 (human-in-the-loop)
  - run 성공 후에도 해제하지 않고 state=awaiting-merge 로 유지 — staging
    머지/폐기(Session End 3단계)까지 공유 자원 조작이므로. 완료 후 release 필수

서브커맨드:
  run     : 락 획득 → Curator headless 실행 → staging diff 실측 → 리포트
  acquire : 락만 획득 (Curator 실패 시 메인 세션 직접 대행용 — 폴백도 락 아래서)
  release : 락 해제 (staging 머지/폐기 완료 후)
  status  : 락 상태 + staging 목록 조회

종료 코드: 0=성공, 1=실행 실패/타임아웃, 2=락 선점(BUSY), 3=환경 오류
"""
import argparse
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# 같은 디렉토리에 배치되는 공유 락 모듈 (repo scripts/ 및 ~/.kiro/mickey/scripts/ 동일)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mickey_lock  # noqa: E402

DEFAULT_AGENT = "knowledge-curator"
DEFAULT_TIMEOUT = 1800          # Curator 1회 실행 상한 (초) — 무한 대기 방지
STALE_HINT_SECONDS = 1800       # 이 시간 지난 락은 크래시 잔여물일 가능성 안내

# staging 내부에 있지만 큐레이션 산출물이 아닌 것들 (diff 계산에서 제외)
DIFF_EXCLUDE_PREFIXES = (".curation.lock",)
DIFF_EXCLUDE_PATTERNS = ("promote-report-", "curator-invoke-report-")


# ── 경로 규약 (§17 staging 자동 감지와 동일) ──────────────────────
def staging_dir(project: Path) -> Path:
    """프로젝트의 _curator-staging 위치 결정. 표준/비표준 구조 모두 지원."""
    if list(project.glob("MICKEY-*-SESSION.md")):
        return project / "_curator-staging"
    if list((project / ".kiro" / "mickey").glob("MICKEY-*-SESSION.md")):
        return project / ".kiro" / "_curator-staging"
    # 세션 파일 미발견 — 표준 위치로 폴백 (첫 큐레이션 등)
    return project / "_curator-staging"


def lock_dir(project: Path) -> Path:
    return staging_dir(project) / ".curation.lock"


# ── staging 스냅샷 (완주 판정의 디스크 실측 근거) ─────────────────
def snapshot(staging: Path) -> dict:
    """staging 내 큐레이션 산출물의 (상대경로 → mtime) 스냅샷."""
    if not staging.exists():
        return {}
    result = {}
    for p in staging.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(staging))
        if rel.startswith(DIFF_EXCLUDE_PREFIXES):
            continue
        if any(pat in rel for pat in DIFF_EXCLUDE_PATTERNS):
            continue
        result[rel] = p.stat().st_mtime
    return result


def diff_lines(before: dict, after: dict) -> list:
    """전후 스냅샷 비교 → 사람이 읽을 diff 라인 목록."""
    lines = []
    for rel in sorted(set(after) - set(before)):
        lines.append(f"  + {rel} (신규)")
    for rel in sorted(set(before) - set(after)):
        lines.append(f"  - {rel} (삭제)")
    for rel in sorted(set(before) & set(after)):
        if before[rel] != after[rel]:
            lines.append(f"  * {rel} (수정)")
    return lines


# ── 락 획득 (BUSY 시 사용자 보고용 정보 출력) ─────────────────────
def do_acquire(project: Path, owner: str, force: bool) -> int:
    try:
        mickey_lock.acquire(lock_dir(project), owner, force=force)
        print(f"[LOCK] 획득: {lock_dir(project)} (owner: {owner})")
        return 0
    except mickey_lock.LockBusyError as e:
        print(f"[BUSY] 다른 세션이 큐레이션 진행 중일 수 있음")
        print(f"  보유자 : {e.owner}")
        print(f"  경과   : {int(e.age_seconds)}s"
              + (" — 크래시 잔여물 가능성, 확인 후 --force 로 강제 진입 가능"
                 if e.age_seconds > STALE_HINT_SECONDS else ""))
        print(f"  락     : {e.lock_dir}")
        return 2


# ── Curator headless 실행 ─────────────────────────────────────────
def build_prompt(project: Path, session: Path) -> str:
    """Curator에게 전달할 호출 메시지 (프로젝트 경로 + 세션 로그 경로)."""
    return (
        f"세션 종료 큐레이션을 수행하라.\n"
        f"- 프로젝트 경로: {project}\n"
        f"- 세션 로그: {session}\n"
        f"시스템 프롬프트의 절차대로 진행하고, 완료 시 staging 파일 목록과 "
        f"1줄 요약을 출력하라."
    )


def do_run(project: Path, session: Path, owner: str, force: bool,
           agent: str, timeout: int) -> int:
    exe = shutil.which("kiro-cli")
    if not exe:
        print("[FAIL] kiro-cli 실행 파일을 찾을 수 없음")
        return 3
    if not session.exists():
        print(f"[FAIL] 세션 로그 없음: {session}")
        return 3

    # 1) 락 — 잡지 못하면 Curator는 실행되지 않는다 (코드 강제 지점)
    rc = do_acquire(project, owner, force)
    if rc != 0:
        return rc

    staging = staging_dir(project)
    report = [f"# Curator invoke report — {datetime.now().isoformat(timespec='seconds')}",
              f"project: {project}", f"session: {session.name}", f"owner: {owner}"]
    before = snapshot(staging)

    # 2) headless 실행 (stdout 파이프 = in-band 수신, 타임아웃 강제 상한)
    started = time.time()
    try:
        proc = subprocess.run(
            [exe, "chat", "--agent", agent, "--no-interactive",
             build_prompt(project, session)],
            cwd=str(project), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        elapsed = int(time.time() - started)
        report.append(f"exit: {proc.returncode}, elapsed: {elapsed}s")
        curator_out = proc.stdout or ""
    except subprocess.TimeoutExpired:
        # 타임아웃: 락은 유지 (state=held) — 메인 세션이 락 아래서 직접 대행
        report.append(f"[TIMEOUT] {timeout}s 초과 — 프로세스 강제 종료. "
                      f"락 유지 중이므로 직접 대행 후 release 할 것")
        _finish_report(staging, report, extra_out="")
        return 1

    # 3) 완주 판정 = 디스크 실측 (응답 표면 아닌 staging diff — §17 규약의 코드화)
    after = snapshot(staging)
    changes = diff_lines(before, after)
    adaptive = project / "context_rule" / "adaptive.md"
    adaptive_note = ""
    if adaptive.exists() and adaptive.stat().st_mtime > started:
        adaptive_note = "  * context_rule/adaptive.md (Curator 직접 수정 감지)"

    report.append(f"staging diff ({len(changes)}건):")
    report.extend(changes if changes else ["  (변화 없음)"])
    if adaptive_note:
        report.append(adaptive_note)

    ok = proc.returncode == 0
    if ok:
        # 락을 해제하지 않고 머지 대기 상태로 전환 — 3단계 완료 후 release
        mickey_lock.set_state(lock_dir(project), "awaiting-merge")
        report.append("[RESULT] COMPLETED — 락 state=awaiting-merge. "
                      "staging 머지/폐기 후 `invoke_curator.py release` 실행 필수")
    else:
        report.append("[RESULT] FAILED — 락 유지 중 (state=held). "
                      "직접 대행 가능, 완료 후 release")

    _finish_report(staging, report, extra_out=curator_out)
    return 0 if ok else 1


def _finish_report(staging: Path, report: list, extra_out: str):
    """리포트를 stdout + staging 파일로 이중 기록 (adaptive #14와 동일 사상)."""
    staging.mkdir(parents=True, exist_ok=True)
    out = staging / f"curator-invoke-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    body = "\n".join(report)
    if extra_out:
        body += "\n\n## curator stdout\n" + extra_out
    out.write_text(body, encoding="utf-8")
    print("\n".join(report))
    print(f"(리포트: {out})")


# ── status / release ──────────────────────────────────────────────
def do_status(project: Path) -> int:
    info = mickey_lock.status(lock_dir(project))
    if info is None:
        print("[FREE] curation 락 없음")
    else:
        print(f"[HELD] owner: {info.get('owner')}, state: {info.get('state')}, "
              f"경과: {info.get('age_seconds')}s")
    staging = staging_dir(project)
    files = sorted(snapshot(staging))
    print(f"staging ({len(files)}건): {staging}")
    for rel in files:
        print(f"  {rel}")
    return 0


def do_release(project: Path) -> int:
    mickey_lock.release(lock_dir(project))
    print(f"[LOCK] 해제: {lock_dir(project)}")
    return 0


# ── CLI ───────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="Knowledge Curator 코드 진입점 (M43)")
    ap.add_argument("command", choices=["run", "acquire", "release", "status"])
    ap.add_argument("--project", default=".", help="프로젝트 루트 (기본: cwd)")
    ap.add_argument("--session", help="세션 로그 경로 (run 필수)")
    ap.add_argument("--owner", help="락 명의 (기본: <프로젝트명> curator)")
    ap.add_argument("--force", action="store_true",
                    help="선점 락 무시하고 강제 진입 (사람 확인 후에만)")
    ap.add_argument("--agent", default=DEFAULT_AGENT)
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = ap.parse_args()

    project = Path(args.project).resolve()
    owner = args.owner or f"{project.name} curator"

    if args.command == "status":
        return do_status(project)
    if args.command == "release":
        return do_release(project)
    if args.command == "acquire":
        return do_acquire(project, owner, args.force)
    # run
    if not args.session:
        print("[FAIL] run 은 --session 필수")
        return 3
    return do_run(project, Path(args.session).resolve(), owner,
                  args.force, args.agent, args.timeout)


if __name__ == "__main__":
    sys.exit(main())
