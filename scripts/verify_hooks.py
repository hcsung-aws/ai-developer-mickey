"""Mickey v10 Phase 3 검증기 (Test Harness).

계획서 §6 Phase 3 CC 4개 항목을 자동 검증:

1. 파이썬 스크립트 파일 존재 (mickey_session_boot.py · mickey_session_close.py).
2. CLI v3 hook JSON 유효성 (mickey-session-start.json) + 폐기 hook 부재 가드
   (mickey-session-stop.json — F5: Stop 은 per-response 발화라 세션 마감 의도와 불일치, 폐기됨).
3. IDE hook skeleton 존재 및 _note 필드 (mickey-pre-task.kiro.hook · mickey-post-task.kiro.hook).
4. 스크립트 --help exit 0.
5. 스크립트 실 실행 exit 0.
6. P3 BRANCH 마커 (boot 4종 · close 3종) 가 stdout 에 등장.

원칙 (Phase 2c 검증기 계승):
- 단일 파일 · 각 검증 항목은 단일 책임 함수.
- 표준 출력 ASCII only (Windows cp949 콘솔 대응).
- 사이드 이펙트 없음. 사이드 이펙트가 필요한 subprocess 는 --dry-run 성격의 실측만 수행.
- 종료 코드: PASS 0 / FAIL 1.

관심사 분리: verify_power_structure.py 는 steering 구조 검증, 본 스크립트는 hook·session 스크립트 검증.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


# --- 검증 대상 스펙 -------------------------------------------------------

SESSION_SCRIPTS: dict[str, dict[str, list[str]]] = {
    ".kiro/scripts/mickey_session_boot.py": {
        "required_markers": [
            "[BRANCH: PURPOSE-SCENARIO]",
            "[BRANCH: HANDOFF]",
            "[BRANCH: BROWNFIELD]",
            "[BRANCH: MCP-TOOLS]",
        ],
    },
    ".kiro/scripts/mickey_session_close.py": {
        "required_markers": [
            "[BRANCH: HANDOFF-SESSION-END]",
            "[BRANCH: SESSION-HISTORY]",
            "[BRANCH: CURATOR-STAGING]",
        ],
    },
}

CLI_V3_HOOKS: dict[str, dict[str, str]] = {
    ".kiro/hooks/mickey-session-start.json": {
        "expected_trigger": "SessionStart",
        "expected_command_hint": "mickey_session_boot.py",
    },
}

# F5 (2026-07-15 실측): Stop 트리거는 세션 종료가 아니라 '응답 종료마다' 발화(per-response).
# 세션 마감(close) 의도와 불일치하여 stop hook 은 폐기됨. close 스크립트는 "세션 정리"
# 요청 시 수동 호출 경로로 유지. 재도입 회귀를 막기 위해 부재를 검증한다.
REMOVED_HOOKS: tuple[str, ...] = (
    ".kiro/hooks/mickey-session-stop.json",
)

IDE_HOOKS: dict[str, dict[str, str]] = {
    ".kiro/hooks/mickey-pre-task.kiro.hook": {
        "expected_trigger": "preTaskExecution",
        "expected_command_hint": "mickey_session_boot.py",
    },
    ".kiro/hooks/mickey-post-task.kiro.hook": {
        "expected_trigger": "postTaskExecution",
        "expected_command_hint": "mickey_session_close.py",
    },
}


# --- 자료구조 ------------------------------------------------------------

@dataclass
class CheckResult:
    """Phase 2c 검증기와 동일 자료구조. 재사용성·일관성 확보."""

    name: str
    passed: bool
    details: list[str] = field(default_factory=list)


# --- 유틸리티 ------------------------------------------------------------

def _mark(passed: bool) -> str:
    """PASS/FAIL 항목 표기용 ASCII 마커."""
    return "[ OK ]" if passed else "[FAIL]"


def _run_python(
    script: Path,
    args: list[str],
    root: Path,
) -> subprocess.CompletedProcess[str]:
    """자식 파이썬 프로세스 실행. 자식의 stdout 을 utf-8 로 강제하여 mojibake 회피.

    PYTHONIOENCODING · PYTHONUTF8 환경변수를 붙여 자식이 무슨 로케일이든 utf-8 출력.
    """
    env = {
        **os.environ,
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    }
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


# --- 검증 함수 -----------------------------------------------------------

def check_scripts_exist(root: Path) -> CheckResult:
    """스크립트 2건 파일 존재 확인."""
    details: list[str] = []
    passed = True
    for rel in SESSION_SCRIPTS:
        p = root / rel
        exists = p.is_file()
        passed = passed and exists
        details.append(f"{_mark(exists)} {rel}")
    return CheckResult(name="1. Session scripts exist", passed=passed, details=details)


def check_hooks_v3_valid(root: Path) -> CheckResult:
    """CLI v3 hook JSON 파싱 · 필수 필드 · 트리거·명령 일치 확인.

    필수 필드: version(v1), hooks[*].name, hooks[*].trigger, hooks[*].action.type='command',
    hooks[*].action.command.
    """
    details: list[str] = []
    passed = True
    for rel, spec in CLI_V3_HOOKS.items():
        p = root / rel
        if not p.is_file():
            passed = False
            details.append(f"{_mark(False)} {rel}: file missing")
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            passed = False
            details.append(f"{_mark(False)} {rel}: json parse error: {exc}")
            continue

        ok, notes = _validate_v3_hook_dict(data, spec)
        if not ok:
            passed = False
        details.append(f"{_mark(ok)} {rel}: " + "; ".join(notes))

    # 폐기된 hook 의 재도입 가드 (F5): 부재해야 PASS
    for rel in REMOVED_HOOKS:
        absent = not (root / rel).exists()
        passed = passed and absent
        details.append(
            f"{_mark(absent)} {rel}: absent (removed by F5, Stop=per-response)"
            if absent
            else f"{_mark(absent)} {rel}: MUST NOT exist (F5: Stop trigger is per-response)"
        )
    return CheckResult(name="2. CLI v3 hooks valid", passed=passed, details=details)


def _validate_v3_hook_dict(
    data: object,
    spec: dict[str, str],
) -> tuple[bool, list[str]]:
    """CLI v3 hook dict 검증. createHook 도구 스펙 준수 확인."""
    notes: list[str] = []
    if not isinstance(data, dict):
        return False, ["not a dict"]
    if data.get("version") != "v1":
        return False, [f"version != v1 ({data.get('version')})"]
    hooks = data.get("hooks")
    if not isinstance(hooks, list) or not hooks:
        return False, ["hooks[] missing or empty"]
    hook = hooks[0]
    if not isinstance(hook, dict):
        return False, ["hook[0] not a dict"]

    trigger = hook.get("trigger")
    if trigger != spec["expected_trigger"]:
        return False, [f"trigger != {spec['expected_trigger']} ({trigger})"]
    notes.append(f"trigger={trigger}")

    action = hook.get("action")
    if not isinstance(action, dict) or action.get("type") != "command":
        return False, ["action.type != command"]
    cmd = action.get("command", "")
    if spec["expected_command_hint"] not in cmd:
        return False, [f"command missing hint '{spec['expected_command_hint']}'"]
    notes.append("action=command")
    notes.append(f"cmd~='{spec['expected_command_hint']}'")
    return True, notes


def check_hooks_ide_skeleton(root: Path) -> CheckResult:
    """IDE hook skeleton 파일 존재 · JSON 파싱 · _note 필드 · 예상 트리거 확인.

    _note 필드는 사용자가 skeleton 임을 인지하도록 하는 표식. 반드시 존재해야 함 (Q3(a)).
    """
    details: list[str] = []
    passed = True
    for rel, spec in IDE_HOOKS.items():
        p = root / rel
        if not p.is_file():
            passed = False
            details.append(f"{_mark(False)} {rel}: file missing")
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            passed = False
            details.append(f"{_mark(False)} {rel}: json parse error: {exc}")
            continue

        note = data.get("_note", "") if isinstance(data, dict) else ""
        trigger = data.get("trigger", "") if isinstance(data, dict) else ""
        note_ok = "SKELETON" in note
        trigger_ok = trigger == spec["expected_trigger"]
        item_ok = note_ok and trigger_ok
        passed = passed and item_ok
        details.append(
            f"{_mark(item_ok)} {rel}: "
            f"trigger={trigger} note_has_SKELETON={note_ok}"
        )
    return CheckResult(name="3. IDE hooks skeleton", passed=passed, details=details)


def check_scripts_help(root: Path) -> CheckResult:
    """각 스크립트 --help exit 0 확인."""
    details: list[str] = []
    passed = True
    for rel in SESSION_SCRIPTS:
        p = root / rel
        try:
            proc = _run_python(p, ["--help"], root)
        except subprocess.TimeoutExpired:
            passed = False
            details.append(f"{_mark(False)} {rel} --help: timeout")
            continue
        ok = proc.returncode == 0
        passed = passed and ok
        details.append(f"{_mark(ok)} {rel} --help: exit={proc.returncode}")
    return CheckResult(name="4. Scripts --help exit 0", passed=passed, details=details)


def check_scripts_run(root: Path) -> CheckResult:
    """각 스크립트 --project-root . 실 실행 exit 0 확인 (사이드 이펙트 없음 · 리포트만)."""
    details: list[str] = []
    passed = True
    for rel in SESSION_SCRIPTS:
        p = root / rel
        try:
            proc = _run_python(p, ["--project-root", str(root)], root)
        except subprocess.TimeoutExpired:
            passed = False
            details.append(f"{_mark(False)} {rel} run: timeout")
            continue
        ok = proc.returncode == 0
        passed = passed and ok
        details.append(f"{_mark(ok)} {rel} run: exit={proc.returncode}")
    return CheckResult(name="5. Scripts run exit 0", passed=passed, details=details)


def check_p3_branches(root: Path) -> CheckResult:
    """스크립트 stdout 에 P3 BRANCH 마커가 모두 등장하는지 확인.

    boot 스크립트는 4개, close 스크립트는 3개. 마커는 대괄호로 감싼 ASCII 문자열이며,
    검증기가 grep 하는 유일한 계약이다.
    """
    details: list[str] = []
    passed = True
    for rel, spec in SESSION_SCRIPTS.items():
        p = root / rel
        try:
            proc = _run_python(p, ["--project-root", str(root)], root)
        except subprocess.TimeoutExpired:
            passed = False
            details.append(f"{_mark(False)} {rel}: timeout")
            continue
        stdout = proc.stdout or ""
        missing = [
            marker for marker in spec["required_markers"]
            if marker not in stdout
        ]
        ok = not missing
        passed = passed and ok
        if ok:
            details.append(
                f"{_mark(True)} {rel}: {len(spec['required_markers'])} markers found"
            )
        else:
            details.append(
                f"{_mark(False)} {rel}: missing markers {missing}"
            )
    return CheckResult(name="6. P3 BRANCH markers present", passed=passed, details=details)


# --- 리포트 · 진입점 -----------------------------------------------------

CHECKS = (
    check_scripts_exist,
    check_hooks_v3_valid,
    check_hooks_ide_skeleton,
    check_scripts_help,
    check_scripts_run,
    check_p3_branches,
)


def run_all(root: Path) -> list[CheckResult]:
    return [fn(root) for fn in CHECKS]


def render_report(results: list[CheckResult]) -> str:
    lines: list[str] = []
    for r in results:
        verdict = "PASS" if r.passed else "FAIL"
        lines.append(f"--- {r.name} : {verdict} ---")
        for d in r.details:
            lines.append(f"  {d}")
        lines.append("")
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mickey v10 Phase 3 검증기: hook · session 스크립트 무결성 검사.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="프로젝트 루트 경로 (기본: 이 스크립트의 상위 디렉토리).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    root = args.root.resolve()

    if not root.is_dir():
        print(f"ERROR: root not a directory: {root}", file=sys.stderr)
        return 1

    results = run_all(root)
    print(render_report(results))

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    failed = total - passed
    print(f"Summary: PASS {passed} / FAIL {failed} / total {total}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
