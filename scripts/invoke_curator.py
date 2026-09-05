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
import hashlib
import os
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
DEFAULT_RETRIES = 1             # 비정상 종료(exit≠0) 시 재시도 횟수 (M45 — ModelThrottle 간헐 실패 실측 대응)
DEFAULT_RETRY_DELAY = 60        # 재시도 전 대기 (초) — 서비스 부하 완화 시간
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


# ── Base-Hash 자동 기입 (M48 — Curator/promote 형식 계약의 결정론 보완) ──
def global_root() -> Path:
    """글로벌 지식 루트 (promote_knowledge.global_root 와 동일 규약 — 테스트 격리용 env 지원)."""
    env = os.environ.get("MICKEY_GLOBAL_ROOT")
    return Path(env) if env else Path.home() / ".kiro" / "mickey"


def fill_pending_basehash(staging: Path, run_started: float) -> list:
    """augment 번들의 `Base-Hash: pending` 을 대상 entry의 실제 sha256으로 기입.

    배경 (M47 CONFLICT 오탐): Curator(LLM)는 sha256을 계산할 수 없어 pending
    마커를 남기는데, promote의 낙관적 동시성 대조는 실제 해시를 요구한다 —
    번들 형식 계약과 Curator 능력의 불일치를 결정론 코드로 메운다
    (LLM 결정론적 하이브리드 패턴).

    안전 조건: 대상 entry가 큐레이션 시작(run_started) 이후 수정됐다면 타 세션의
    실제 drift — 기입하지 않고 pending 유지하여 promote가 CONFLICT 스킵으로
    재큐레이션을 유도하게 둔다 (기존 계약 보존).
    반환: 리포트용 라인 목록 (처리 없으면 빈 목록).
    """
    entries_root = global_root() / "domain"
    lines = []
    for bundle in sorted(staging.glob("gd-*.md")):
        text = bundle.read_text(encoding="utf-8")
        if "Base-Hash: pending" not in text:
            continue
        # Meta 섹션의 Entry-Path 파싱 (promote 파서와 동일한 Key: value 규약)
        entry_path = None
        for line in text.splitlines():
            if line.strip().lower().startswith("entry-path:"):
                entry_path = line.split(":", 1)[1].strip()
                break
        if not entry_path or not entry_path.startswith("entries/") or ".." in entry_path:
            lines.append(f"  ! {bundle.name}: Entry-Path 이상({entry_path!r}) — pending 유지")
            continue
        entry = entries_root / entry_path
        if not entry.exists():
            # augment 대상 부재는 promote가 CONFLICT로 잡을 사안 — 여기선 손대지 않음
            lines.append(f"  ! {bundle.name}: 대상 없음({entry_path}) — pending 유지")
            continue
        if entry.stat().st_mtime >= run_started:
            lines.append(f"  ! {bundle.name}: 대상이 큐레이션 시작 후 수정됨 — 실제 drift, pending 유지")
            continue
        digest = hashlib.sha256(entry.read_bytes()).hexdigest()
        bundle.write_text(
            text.replace("Base-Hash: pending", f"Base-Hash: {digest}"),
            encoding="utf-8")
        lines.append(f"  = {bundle.name}: Base-Hash 기입 ({digest[:16]}…)")
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


def _cli_version(exe: str) -> str:
    """kiro-cli 버전 실측 — 실패 리포트의 환경 증거 (M45: CLI 갱신 직후 실패 다발 실측).

    조회 실패가 본 실행을 막아서는 안 되므로 예외는 문자열로 흡수한다.
    """
    try:
        p = subprocess.run([exe, "--version"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30)
        return (p.stdout or p.stderr or "").strip() or f"(빈 출력, exit {p.returncode})"
    except Exception as e:  # noqa: BLE001
        return f"(조회 실패: {e})"


def _to_text(v) -> str:
    """TimeoutExpired.stdout/stderr는 버전에 따라 bytes/None — 항상 str로 정규화."""
    if v is None:
        return ""
    return v.decode("utf-8", errors="replace") if isinstance(v, bytes) else v


def _attempt(exe: str, agent: str, prompt: str, project: Path, timeout: int) -> dict:
    """Curator 1회 실행. 타임아웃 포함 모든 결과를 dict로 반환 (증거 유실 금지 — M45).

    실패 원인 진단을 위해 stderr와 (타임아웃 시) 부분 출력까지 전부 보존한다.
    """
    started = time.time()
    try:
        proc = subprocess.run(
            [exe, "chat", "--agent", agent, "--no-interactive", prompt],
            cwd=str(project), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        return {"returncode": proc.returncode, "elapsed": int(time.time() - started),
                "stdout": proc.stdout or "", "stderr": proc.stderr or "",
                "timed_out": False}
    except subprocess.TimeoutExpired as e:
        # 강제 종료 직전까지의 부분 출력도 진단 증거로 보존
        return {"returncode": None, "elapsed": int(time.time() - started),
                "stdout": _to_text(e.stdout), "stderr": _to_text(e.stderr),
                "timed_out": True}


def do_run(project: Path, session: Path, owner: str, force: bool,
           agent: str, timeout: int,
           retries: int = DEFAULT_RETRIES,
           retry_delay: int = DEFAULT_RETRY_DELAY) -> int:
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
    run_started = time.time()
    prompt = build_prompt(project, session)
    # 스냅샷을 환경 조회보다 먼저 — 조회 부작용이 diff 기준선을 오염시키지 않도록
    before = snapshot(staging)

    # 실행 환경 증거 (M45: 실패 원인 추적에 필요한 맥락을 리포트에 전부 남긴다)
    report = [f"# Curator invoke report — {datetime.now().isoformat(timespec='seconds')}",
              f"project: {project}", f"session: {session.name}", f"owner: {owner}",
              f"command: {exe} chat --agent {agent} --no-interactive <prompt {len(prompt)} chars>",
              f"kiro-cli: {_cli_version(exe)}",
              f"timeout: {timeout}s, retries: {retries}, retry-delay: {retry_delay}s"]

    # 2) headless 실행 + 재시도 (M45: ModelThrottle "unexpectedly high load"로
    #    자식 kiro-cli가 작업 도중 exit 1로 절단되는 간헐 실패 실측 → 1회 재시도가 정답)
    attempts = []
    prev_snap = before
    for i in range(1, retries + 2):
        stamp = datetime.now().strftime("%H:%M:%S")
        r = _attempt(exe, agent, prompt, project, timeout)
        attempts.append(r)
        # 시도별 staging diff — 부분 산출물(절단 시점) 추적용
        now_snap = snapshot(staging)
        step = diff_lines(prev_snap, now_snap)
        prev_snap = now_snap
        report.append(f"## attempt {i}/{retries + 1} — {stamp} 시작")
        report.append(f"exit: {r['returncode']}, elapsed: {r['elapsed']}s, "
                      f"timed_out: {r['timed_out']}, "
                      f"stdout: {len(r['stdout'])} chars, stderr: {len(r['stderr'])} chars")
        report.append(f"attempt staging diff ({len(step)}건):")
        report.extend(step if step else ["  (변화 없음)"])
        if r["timed_out"]:
            # 타임아웃(30분 hang)은 스로틀 절단과 양상이 다름 — 무인 재시도 없이 중단
            report.append(f"[TIMEOUT] {timeout}s 초과 — 프로세스 강제 종료. "
                          f"재시도하지 않음. 락 유지 중이므로 직접 대행 후 release 할 것")
            break
        if r["returncode"] == 0:
            break
        if i <= retries:
            report.append(f"[RETRY] exit {r['returncode']} — {retry_delay}s 대기 후 재시도 "
                          f"(간헐 스로틀 대응). 직전 시도의 부분 산출물은 staging에 잔존할 수 있음")
            time.sleep(retry_delay)

    # 3) Base-Hash 자동 기입 (M48) — 완주 판정 전, 산출 번들의 pending 마커를
    #    실제 해시로 보정 (실패 시도의 부분 산출물도 직접 대행 경로에서 재사용되므로 수행)
    basehash_lines = fill_pending_basehash(staging, run_started)
    if basehash_lines:
        report.append(f"Base-Hash 자동 기입 ({len(basehash_lines)}건):")
        report.extend(basehash_lines)

    # 4) 완주 판정 = 디스크 실측 (응답 표면 아닌 staging diff — §17 규약의 코드화)
    last = attempts[-1]
    after = snapshot(staging)
    changes = diff_lines(before, after)
    adaptive = project / "context_rule" / "adaptive.md"
    adaptive_note = ""
    if adaptive.exists() and adaptive.stat().st_mtime > run_started:
        adaptive_note = "  * context_rule/adaptive.md (Curator 직접 수정 감지)"

    report.append(f"staging diff (전체 {len(changes)}건):")
    report.extend(changes if changes else ["  (변화 없음)"])
    if adaptive_note:
        report.append(adaptive_note)

    ok = (not last["timed_out"]) and last["returncode"] == 0
    if ok:
        # 락을 해제하지 않고 머지 대기 상태로 전환 — 3단계 완료 후 release
        mickey_lock.set_state(lock_dir(project), "awaiting-merge")
        report.append("[RESULT] COMPLETED — 락 state=awaiting-merge. "
                      "staging 머지/폐기 후 `invoke_curator.py release` 실행 필수")
    else:
        report.append("[RESULT] FAILED — 락 유지 중 (state=held). "
                      "직접 대행 가능, 완료 후 release")

    _finish_report(staging, report, extra_out=_attempts_transcript(attempts))
    return 0 if ok else 1


def _attempts_transcript(attempts: list) -> str:
    """시도별 stderr/stdout 전문을 리포트 말미에 보존 (M45 — 진단 증거 유실 방지).

    기존에는 stderr를 캡처만 하고 버려서 실패 원인을 kiro 로그에서 역추적해야 했다.
    """
    parts = []
    for i, r in enumerate(attempts, 1):
        parts.append(f"## attempt {i} stderr\n" + (r["stderr"] or "(비어 있음)"))
        parts.append(f"## attempt {i} stdout\n" + (r["stdout"] or "(비어 있음)"))
    return "\n\n".join(parts)


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
    ap.add_argument("--retries", type=int, default=DEFAULT_RETRIES,
                    help="exit≠0 시 재시도 횟수 (기본 1 — 간헐 스로틀 대응, M45)")
    ap.add_argument("--retry-delay", type=int, default=DEFAULT_RETRY_DELAY,
                    help="재시도 전 대기 초 (기본 60)")
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
                  args.force, args.agent, args.timeout,
                  retries=args.retries, retry_delay=args.retry_delay)


if __name__ == "__main__":
    sys.exit(main())
