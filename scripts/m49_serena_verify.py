# -*- coding: utf-8 -*-
"""M49 serena 최종 확인 (§19.3 규약 실측)

목적:
1. 실행 중인 serena 프로세스의 cmdline에 --project 기동 인자가 없는지 실측 (Option A fail-closed 유지 확인)
2. 정리된 serena_config.yml(M48)의 등록 프로젝트 수가 17건인지 확인
판정: 두 항목 모두 PASS면 .bak-m48 삭제 가능 시점.

출력: 콘솔(ASCII 위주) + 리포트 파일 직접 utf-8 기록 (adaptive #19 — 셸 리다이렉트 금지)
"""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: cp949 방어

REPORT = Path(__file__).resolve().parent.parent / "_curator-staging" / "m49-serena-verify-report.txt"
CONFIG = Path.home() / ".serena" / "serena_config.yml"

lines = []  # 리포트 누적 버퍼


def log(msg: str) -> None:
    lines.append(msg)
    print(msg)


def check_process_cmdline() -> bool:
    """serena 관련 프로세스 cmdline 수집 → --project 인자 부재 확인"""
    # PowerShell CIM 조회 결과를 Python이 직접 수신 (파이프 캡처 — 파일 리다이렉트 아님)
    ps_cmd = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.CommandLine -match 'serena' } | "
        "ForEach-Object { $_.ProcessId.ToString() + '|' + $_.CommandLine }"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_cmd],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    procs = [l.strip() for l in result.stdout.splitlines() if l.strip()]
    # 본 스크립트를 띄운 조회 자체가 걸리는 경우 제외 (powershell/python 프로세스의 검색어 포함)
    serena_procs = [p for p in procs if "serena" in p.lower() and "Get-CimInstance" not in p]

    log(f"[1] serena process scan: {len(serena_procs)} found")
    ok = True
    for p in serena_procs:
        pid, _, cmdline = p.partition("|")
        has_project = "--project" in cmdline
        log(f"    PID {pid}: --project {'PRESENT (FAIL)' if has_project else 'absent (ok)'}")
        log(f"      cmdline: {cmdline[:300]}")
        if has_project:
            ok = False
    if not serena_procs:
        log("    (no serena process found — MCP server may run under different name; treat as INCONCLUSIVE)")
        return None
    return ok


def check_config_registrations() -> bool:
    """serena_config.yml 등록 프로젝트 수 확인 (기대: 17)"""
    if not CONFIG.exists():
        log(f"[2] config NOT FOUND: {CONFIG}")
        return False
    text = CONFIG.read_text(encoding="utf-8", errors="replace")
    # projects: 섹션의 리스트 항목("- ") 카운트 — 단순 구조 가정, 실패 시 원문 일부 출력
    in_projects = False
    count = 0
    entries = []
    for line in text.splitlines():
        if line.strip().startswith("projects:"):
            in_projects = True
            continue
        if in_projects:
            if line.startswith((" ", "\t", "-")) and line.strip().startswith("-"):
                count += 1
                entries.append(line.strip())
            elif line.strip() and not line.startswith((" ", "\t")):
                in_projects = False  # 다음 최상위 키 도달
    log(f"[2] serena_config.yml registered projects: {count} (expect 17)")
    for e in entries:
        log(f"    {e}")
    return count == 17


def main() -> int:
    log("=== M49 serena verification (2026-09-05) ===")
    proc_ok = check_process_cmdline()
    cfg_ok = check_config_registrations()
    log("")
    log(f"RESULT: process-cmdline={'PASS' if proc_ok else ('INCONCLUSIVE' if proc_ok is None else 'FAIL')}, "
        f"config-17={'PASS' if cfg_ok else 'FAIL'}")
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    log(f"report: {REPORT}")
    return 0 if (proc_ok and cfg_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
