# -*- coding: utf-8 -*-
"""M49 멀티 세션 serena 해결 최종 확인

검증 3갈래:
1. 실행 중 serena 프로세스 전수 — --project 기동 인자 부재 (fail-closed 유지)
2. ~/.serena/logs 최근 로그에서 activate/project 관련 라인 수집 — 각 세션이 어느 프로젝트를
   활성화했는지 실측 (M47 사고: 전 세션이 조상 work\kiro로 낙착)
3. fail-wrong 시그니처 재발 점검 — 조상 디렉토리(work\kiro)에 .serena/ 또는 세션 파일 오배치 여부
   + 같은 depth 프로젝트들의 오늘자 Mickey 세션 활동 목록

출력: 콘솔 + 리포트 파일 직접 utf-8 기록 (adaptive #19)
"""
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

KIRO_DIR = Path(r"C:\Users\hcsung\work\kiro")          # 같은 depth 프로젝트들의 부모
SERENA_HOME = Path.home() / ".serena"
REPORT = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\_curator-staging\m49-multisession-serena-report.txt")
TODAY_CUTOFF = time.time() - 24 * 3600                  # 최근 24시간을 "오늘 세션" 기준으로

lines = []


def log(msg: str) -> None:
    lines.append(msg)
    print(msg)


def check1_processes() -> bool:
    """serena 프로세스 cmdline 전수 — --project 부재 확인"""
    ps_cmd = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.CommandLine -match 'serena' -and $_.CommandLine -notmatch 'Get-CimInstance' } | "
        "ForEach-Object { $_.ProcessId.ToString() + '|' + $_.CommandLine }"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    procs = [l.strip() for l in r.stdout.splitlines() if l.strip() and "m49_multisession" not in l]
    log(f"[1] serena processes: {len(procs)}")
    ok = True
    for p in procs:
        pid, _, cmd = p.partition("|")
        bad = "--project" in cmd
        log(f"    PID {pid}: --project {'PRESENT <-- FAIL' if bad else 'absent'}")
        if bad:
            ok = False
    return ok


def check2_activation_logs() -> None:
    """serena 로그에서 최근 activate 이력 수집 — 세션별 활성 프로젝트 실측"""
    log("")
    log("[2] recent serena activation evidence (~/.serena/logs, last 24h):")
    logs_dir = SERENA_HOME / "logs"
    if not logs_dir.exists():
        log("    logs dir not found — INCONCLUSIVE (activation은 각 세션 응답으로 확인 필요)")
        return
    found = 0
    # 최근 24시간 내 수정된 로그 파일만 검사
    for f in sorted(logs_dir.rglob("*.txt")) + sorted(logs_dir.rglob("*.log")):
        try:
            if f.stat().st_mtime < TODAY_CUTOFF:
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for ln in text.splitlines():
            low = ln.lower()
            # activate 흔적 라인만 추출 (활성 프로젝트 경로 포함 기대)
            if "activat" in low and ("project" in low):
                found += 1
                log(f"    {f.name}: {ln.strip()[:200]}")
    if found == 0:
        log("    (activation 라인 미발견 — 로그 포맷 상이 가능. 프로세스/오배치 검증으로 보완)")


def check3_failwrong_signature() -> bool:
    """조상 디렉토리 오배치 재발 + 같은 depth 프로젝트 오늘자 세션 활동"""
    log("")
    log(f"[3] fail-wrong signature check at ancestor: {KIRO_DIR}")
    ok = True
    # 조상(work\kiro) 직하에 .serena/ 또는 Mickey 세션 파일이 있으면 오배치 신호
    stray_serena = KIRO_DIR / ".serena"
    if stray_serena.exists():
        # M47 사고 잔재일 수도, 신규 재발일 수도 — mtime으로 구분
        mtime = datetime.fromtimestamp(stray_serena.stat().st_mtime)
        fresh = stray_serena.stat().st_mtime > TODAY_CUTOFF
        log(f"    .serena/ EXISTS at ancestor (mtime {mtime:%Y-%m-%d %H:%M}) — {'FRESH <-- 재발 의심' if fresh else 'stale (과거 잔재, 재발 아님)'}")
        if fresh:
            ok = False
    else:
        log("    .serena/ at ancestor: absent (ok)")
    strays = list(KIRO_DIR.glob("MICKEY-*-*.md"))
    if strays:
        for s in strays:
            fresh = s.stat().st_mtime > TODAY_CUTOFF
            log(f"    stray session file: {s.name} — {'FRESH <-- 재발 의심' if fresh else 'stale'}")
            if fresh:
                ok = False
    else:
        log("    stray MICKEY-* files at ancestor: none (ok)")

    log("")
    log("[3b] sibling projects with Mickey session activity (last 24h):")
    for d in sorted(KIRO_DIR.iterdir()):
        if not d.is_dir():
            continue
        sessions = list(d.glob("MICKEY-*-SESSION.md"))
        recent = [s for s in sessions if s.stat().st_mtime > TODAY_CUTOFF]
        if recent:
            has_serena = (d / ".serena").exists()
            names = ", ".join(s.name for s in recent)
            log(f"    {d.name}: {names} | .serena marker: {'yes' if has_serena else 'no'}")
    return ok


def main() -> int:
    log(f"=== M49 multi-session serena verification ({datetime.now():%Y-%m-%d %H:%M}) ===")
    p_ok = check1_processes()
    check2_activation_logs()
    s_ok = check3_failwrong_signature()
    log("")
    log(f"RESULT: processes={'PASS' if p_ok else 'FAIL'}, fail-wrong-signature={'PASS (재발 없음)' if s_ok else 'FAIL (재발 의심)'}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    log(f"report: {REPORT}")
    return 0 if (p_ok and s_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
