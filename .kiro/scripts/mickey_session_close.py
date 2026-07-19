"""Mickey Session Close Script (Phase 3, v10 power migration).

세션 종료 직전 Mickey 규약 준수 여부를 정적 실측하여 stdout 리포트로 출력.
hook 자동 호출과 사용자 직접 호출을 모두 지원.

실측 항목 (3종):
- HANDOFF: 오늘 날짜의 handoff 문서(`YYYY-MM-DD-<uid>-handoff.md`)가 존재하는가.
- SESSION-HISTORY: 오늘 날짜의 세션 로그(`YYYY-MM-DD-<uid>-log.md`)가 존재하는가.
- CURATOR-STAGING: Pre-staged Apply 대기 (_curator-staging/) 가 있는가.

관련 산출물:
- `scripts/verify_hooks.py` (본 스크립트의 BRANCH 마커 추적 검증)
- 세션 기록 규약: D-0717-1 (날짜+UID) — kickoff 문서 §2 / DECISIONS.md 참조
- 참고: Stop hook 은 per-response 발화 특성으로 미채택 (F5 결정) — 본 스크립트는
  세션 마감 시 사용자/Mickey 가 수동 실행하는 체크리스트 도구

개정 이력:
- 2026-07-19 (세션 551c3f): D-0717-2 집행 — 탐지 패턴을 날짜+UID 규약으로 교체
  (소문자 `-handoff.md` / `-log.md` glob, UID 파싱), stdout UTF-8 고정,
  폐기된 hook (.kiro.hook, session-stop.json) 참조 제거

원칙:
- 사이드 이펙트 없음. 실측·리포트만.
- 각 실측 함수는 단일 책임. BRANCH 마커 주석으로 검증기가 grep.
- 조건부 실행에 대해 '양쪽 분기'를 stdout 안내 문구로 명시 (계획서 P3).
- 표준 출력 마커는 ASCII only, 자연어 설명은 한글 병기.

참고: 계획서 `IMPROVEMENT-PLAN-v10-power-migration.md` §6 Phase 3.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# --- 자료구조 ------------------------------------------------------------

@dataclass
class BranchResult:
    """세션 종료 실측 결과 자료구조. boot 스크립트와 동일한 구조를 채택하여
    검증기 · 리포트 렌더러를 공유 가능하게 함.
    """

    name: str
    state: str  # 'exists' | 'missing' | 'unknown'
    detail: dict[str, Any] = field(default_factory=dict)
    guidance: str = ""


# --- 실측 함수 -----------------------------------------------------------

# BRANCH: HANDOFF-SESSION-END
def detect_handoff_today(project_root: Path, today: dt.date) -> BranchResult:
    """오늘 날짜의 HANDOFF 문서가 session_history/ 아래 존재하는가 실측.

    존재 시 -> 세션 종료 규약 준수. 부재 시 -> HANDOFF 신규 작성 필요.
    (Mickey 세션 종료 프로토콜)
    """
    history_dir = project_root / "session_history"
    if not history_dir.is_dir():
        return BranchResult(
            name="HANDOFF-SESSION-END",
            state="missing",
            detail={"path": None, "reason": "session_history/ dir not found"},
            guidance=(
                "session_history/ 부재. HANDOFF 문서 작성 위치 확보 필요."
            ),
        )
    today_str = today.strftime("%Y-%m-%d")
    # 날짜+UID 규약 (D-0717-1): 오늘 날짜로 시작하고 -handoff.md 로 끝나는 파일만 매치.
    # 소문자 패턴 고정 (구 대문자 HANDOFF 패턴은 Windows glob 에서만 우연히 동작).
    matches = sorted(
        p for p in history_dir.glob(f"{today_str}-*-handoff.md") if p.is_file()
    )
    if matches:
        return BranchResult(
            name="HANDOFF-SESSION-END",
            state="exists",
            detail={
                "date": today_str,
                "files": [str(p.relative_to(project_root)) for p in matches],
                # 파일명에서 UID 추출해 함께 표기 (채팅 응답에 UID 명시 의무 지원).
                "uids": [p.stem.split("-")[-2] for p in matches],
            },
            guidance=(
                "오늘자 handoff 존재. 세션 종료 규약 준수. "
                "채팅 응답에 UID 명시했는지 확인 (D-0717-1 기록 후 의무)."
            ),
        )
    return BranchResult(
        name="HANDOFF-SESSION-END",
        state="missing",
        detail={"date": today_str, "files": []},
        guidance=(
            "오늘자 handoff 부재. 세션 종료 전 "
            "session_history/YYYY-MM-DD-<uid>-handoff.md 작성 필요 "
            "(UID 생성: python .kiro/scripts/gen_session_uid.py)."
        ),
    )


# BRANCH: SESSION-HISTORY
def detect_session_history_today(project_root: Path, today: dt.date) -> BranchResult:
    """오늘 날짜의 세션 로그가 session_history/ 아래 존재하는가 실측.

    존재 시 -> 세션 로그 유지 규약 준수. 부재 시 -> 세션 로그 신규 작성 필요.
    (Mickey 세션 로그 규약)
    """
    history_dir = project_root / "session_history"
    if not history_dir.is_dir():
        return BranchResult(
            name="SESSION-HISTORY",
            state="missing",
            detail={"path": None, "reason": "session_history/ dir not found"},
            guidance=(
                "session_history/ 부재. 세션 로그 작성 위치 확보 필요."
            ),
        )
    today_str = today.strftime("%Y-%m-%d")
    # 날짜+UID 규약 (D-0717-1): 오늘 날짜의 -log.md 파일만 매치 (handoff 는 별도 분기).
    matches = sorted(
        p for p in history_dir.glob(f"{today_str}-*-log.md") if p.is_file()
    )
    if matches:
        return BranchResult(
            name="SESSION-HISTORY",
            state="exists",
            detail={
                "date": today_str,
                "files": [str(p.relative_to(project_root)) for p in matches],
                "uids": [p.stem.split("-")[-2] for p in matches],
            },
            guidance=(
                "오늘자 세션 로그 존재. 마감 항목(결정 이력·반성·인계) 채움 여부 확인."
            ),
        )
    return BranchResult(
        name="SESSION-HISTORY",
        state="missing",
        detail={"date": today_str, "files": []},
        guidance=(
            "오늘자 세션 로그 부재. 세션 종료 전 "
            "session_history/YYYY-MM-DD-<uid>-log.md 작성 필요."
        ),
    )


# BRANCH: CURATOR-STAGING
def detect_curator_staging(project_root: Path) -> BranchResult:
    """Curator Pre-staged Apply 대기 디렉토리 (_curator-staging/) 존재 실측.

    프로젝트 루트와 사용자 홈 (~/.kiro/mickey/) 두 위치를 모두 조사.

    존재 시 -> Pre-staged Apply 검토·반영 필요. 부재 시 -> 이번 세션에서 반영 대기 없음.
    (계획서 §6 Phase 4-A Pre-staged Apply 패턴)
    """
    candidates = [
        project_root / "_curator-staging",
        Path.home() / ".kiro" / "mickey" / "_curator-staging",
    ]
    found = [c for c in candidates if c.is_dir()]
    if found:
        return BranchResult(
            name="CURATOR-STAGING",
            state="exists",
            detail={"paths": [str(p) for p in found]},
            guidance=(
                "_curator-staging/ 감지. Pre-staged Apply 대기 파일 검토·반영 필요."
            ),
        )
    return BranchResult(
        name="CURATOR-STAGING",
        state="missing",
        detail={"paths": []},
        guidance=(
            "_curator-staging/ 부재. 반영 대기 없음. 정상 종료 가능."
        ),
    )


# --- stdin 파싱 (선택) ---------------------------------------------------

def read_hook_context(enabled: bool) -> dict[str, Any] | None:
    """CLI v3 hook 이 stdin 으로 넘긴 세션 컨텍스트 JSON 을 파싱.

    - enabled=False 이면 (사용자 직접 실행) 즉시 스킵. stdin block 위험 회피.
    - enabled=True 이면 stdin 을 EOF 까지 읽고 JSON 파싱.
    - 파싱 실패 시 None 반환. 스크립트는 계속 진행.
    """
    if not enabled or sys.stdin is None:
        return None
    raw = sys.stdin.read()
    if not raw.strip():
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


# --- 리포트 렌더링 -------------------------------------------------------

def render_report(
    results: list[BranchResult],
    hook_context: dict[str, Any] | None,
) -> str:
    """실측 결과를 텍스트 리포트로 렌더링. boot 스크립트와 동일 형식."""
    lines: list[str] = []
    lines.append("=== Mickey Session Close Report ===")
    lines.append("")

    if hook_context is not None:
        lines.append(f"[HOOK-CONTEXT] keys: {sorted(hook_context.keys())}")
        lines.append("")

    for r in results:
        lines.append(f"[BRANCH: {r.name}] {r.state}")
        for k, v in r.detail.items():
            lines.append(f"  - {k}: {v}")
        if r.guidance:
            lines.append(f"  - guidance: {r.guidance}")
        lines.append("")

    lines.append("=== End Close Report ===")
    return "\n".join(lines)


# --- 진입점 --------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mickey Session Close 실측 리포트 스크립트 (Phase 3).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="프로젝트 루트 경로 (기본: 현재 작업 디렉토리).",
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="ISO 날짜 override (예: 2026-07-10). 기본은 오늘. 테스트 용.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="실측 결과를 JSON 형식으로 출력 (기본은 사람이 읽는 텍스트).",
    )
    parser.add_argument(
        "--read-stdin",
        action="store_true",
        help="stdin 에서 hook 컨텍스트 JSON 을 읽음 (hook 자동 호출 시에만 사용).",
    )
    return parser


def resolve_today(raw: str | None) -> dt.date:
    """--today 옵션을 파싱. 잘못된 형식이면 예외 (fail-fast)."""
    if raw is None:
        return dt.date.today()
    return dt.date.fromisoformat(raw)


def main(argv: list[str] | None = None) -> int:
    # hook 소비자(CLI 런타임)는 stdout 을 UTF-8 로 디코딩한다 (boot 스크립트와 동일 근거).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = build_arg_parser().parse_args(argv)
    project_root = args.project_root.resolve()

    if not project_root.is_dir():
        print(f"ERROR: project root not a directory: {project_root}", file=sys.stderr)
        return 1

    try:
        today = resolve_today(args.today)
    except ValueError as exc:
        print(f"ERROR: invalid --today value: {exc}", file=sys.stderr)
        return 1

    hook_context = read_hook_context(enabled=args.read_stdin)

    results = [
        detect_handoff_today(project_root, today),
        detect_session_history_today(project_root, today),
        detect_curator_staging(project_root),
    ]

    if args.json:
        payload = {
            "today": today.isoformat(),
            "hook_context_keys": (
                sorted(hook_context.keys()) if hook_context else None
            ),
            "branches": [
                {
                    "name": r.name,
                    "state": r.state,
                    "detail": r.detail,
                    "guidance": r.guidance,
                }
                for r in results
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_report(results, hook_context))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
