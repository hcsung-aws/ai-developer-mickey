"""Mickey Session Boot Script (Phase 3, v10 power migration).

세션 시작 시 Mickey 프로토콜 부팅에 필요한 P3 분기 4종을 정적 실측하여
stdout 리포트로 출력. hook 자동 호출과 사용자 직접 호출을 모두 지원.

관련 산출물:
- `.kiro/hooks/mickey-session-start.json` (CLI v3 SessionStart hook 예시)
- `.kiro/hooks/mickey-pre-task.kiro.hook` (IDE preTaskExecution skeleton)
- `scripts/verify_hooks.py` (본 스크립트의 BRANCH 마커 추적 검증)

원칙:
- 사이드 이펙트 없음 (파일 편집·네트워크 접근 없음). 실측·리포트만 수행.
- 각 분기 함수는 단일 책임. BRANCH 마커 주석으로 검증기가 grep 가능하게 함.
- 조건부 실행에 대해 '양쪽 분기'를 stdout 안내 문구로 명시 (계획서 P3).
- 표준 출력 마커는 ASCII only. 자연어 설명은 한글 병기.

참고: 계획서 `IMPROVEMENT-PLAN-v10-power-migration.md` §6 Phase 3.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# --- 상수 ---------------------------------------------------------------

# Brownfield 감지 임계값. 프로젝트 루트에서 코드 파일이 이 수치 이상이면 감지로 판정.
BROWNFIELD_CODE_THRESHOLD = 5

# Brownfield 감지 대상 확장자 (일반 코드 언어 위주).
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".gd", ".java", ".rs", ".go",
    ".cs", ".cpp", ".c", ".h", ".hpp",
    ".rb", ".php", ".kt", ".swift",
}

# 코드 탐색 시 무시할 디렉토리 (성능 · 노이즈 방지).
IGNORED_DIRS = {
    ".git", ".venv", "venv", "env", "__pycache__",
    "node_modules", "dist", "build", "target",
    ".pytest_cache", ".serena", ".mypy_cache",
    ".kiro",  # Mickey 자신의 hook/스크립트 제외
}

# 감지 대상 MCP 서버명. 정확 매치. (계획서 §6 Q2 결정에 따라 정적 감지만 수행)
TARGET_MCP_SERVERS = ("serena", "graphify")


# --- 자료구조 ------------------------------------------------------------

@dataclass
class BranchResult:
    """P3 분기 판정 결과를 담는 단일 자료구조.

    - name: 분기 식별자 (BRANCH 마커에 사용). 대문자 스네이크 케이스.
    - state: 판정 상태. 'exists' | 'missing' | 'unknown'.
    - detail: 부가 정보 (파일 경로 · 카운트 등). 자유 딕셔너리.
    - guidance: Mickey 에게 전달할 다음 행동 안내 문구 (양쪽 분기 명시).
    """

    name: str
    state: str
    detail: dict[str, Any] = field(default_factory=dict)
    guidance: str = ""


# --- 분기 판정 함수 ------------------------------------------------------

# BRANCH: PURPOSE-SCENARIO
def detect_purpose_scenario(project_root: Path) -> BranchResult:
    """PURPOSE-SCENARIO.md 존재 여부를 확인.

    존재 시 -> 기존 목적·시나리오 로드. 부재 시 -> 신규 질문 필요.
    (계획서 §6 Phase 3 P3 분기 1)
    """
    target = project_root / "PURPOSE-SCENARIO.md"
    if target.exists() and target.is_file():
        return BranchResult(
            name="PURPOSE-SCENARIO",
            state="exists",
            detail={"path": str(target.relative_to(project_root))},
            guidance=(
                "기존 목적·시나리오 로드. 신규 질문 스킵."
            ),
        )
    return BranchResult(
        name="PURPOSE-SCENARIO",
        state="missing",
        detail={"path": None},
        guidance=(
            "PURPOSE-SCENARIO.md 부재. 프로젝트 목적·시나리오 신규 질문 필요."
        ),
    )


# BRANCH: HANDOFF
def detect_handoff(project_root: Path) -> BranchResult:
    """session_history/ 아래 HANDOFF 문서 최신본 존재 여부를 확인.

    존재 시 -> 이전 세션 HANDOFF 로드. 부재 시 -> Mickey 1 세션 취급.
    (계획서 §6 Phase 3 P3 분기 3)
    """
    history_dir = project_root / "session_history"
    if not history_dir.is_dir():
        return BranchResult(
            name="HANDOFF",
            state="missing",
            detail={"latest": None, "reason": "session_history/ dir not found"},
            guidance=(
                "session_history/ 부재. 이번은 Mickey 1 세션으로 취급."
            ),
        )
    # HANDOFF 를 이름에 포함하는 파일만 대상 (Mickey 규약).
    candidates = sorted(
        history_dir.glob("*HANDOFF*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        latest = candidates[0]
        return BranchResult(
            name="HANDOFF",
            state="exists",
            detail={"latest": str(latest.relative_to(project_root))},
            guidance=(
                "이전 세션 HANDOFF 로드. Feedback 반영 여부 판정 필요."
            ),
        )
    return BranchResult(
        name="HANDOFF",
        state="missing",
        detail={"latest": None},
        guidance=(
            "HANDOFF 문서 부재. 이번은 Mickey 1 세션으로 취급."
        ),
    )


# BRANCH: BROWNFIELD
def detect_brownfield(project_root: Path, threshold: int) -> BranchResult:
    """프로젝트 루트에서 코드 파일 수를 세어 Brownfield 여부 판정.

    임계값 이상 -> Brownfield 온보딩 수행. 미만 -> 온보딩 스킵.
    (계획서 §6 Phase 3 P3 분기 4)
    """
    count = 0
    for dirpath, dirnames, filenames in os.walk(project_root):
        # 무시 디렉토리 pruning (in-place).
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fname in filenames:
            if Path(fname).suffix in CODE_EXTENSIONS:
                count += 1
    if count >= threshold:
        return BranchResult(
            name="BROWNFIELD",
            state="exists",
            detail={"code_file_count": count, "threshold": threshold},
            guidance=(
                "Brownfield 감지. 온보딩 수행 (기존 코드 구조 · 관례 · 테스트 harness 파악)."
            ),
        )
    return BranchResult(
        name="BROWNFIELD",
        state="missing",
        detail={"code_file_count": count, "threshold": threshold},
        guidance=(
            "Greenfield 판정. Brownfield 온보딩 스킵. 신규 설계로 진행."
        ),
    )


# BRANCH: MCP-TOOLS
def detect_mcp_registration(project_root: Path) -> BranchResult:
    """MCP 서버 등록 상태를 정적 파싱으로 확인 (serena · graphify).

    프로젝트 mcp.json 우선, 사용자 mcp.json 보조. 실행 시점 활성 여부는 알 수 없으므로
    등록 여부만 리포트. INDEX 파일은 편집하지 않음. (계획서 §6 Q2 결정)

    감지 시 -> INDEX Tool Links 등록 대상 확인. 미감지 시 -> Tier 3 baseline 사용.
    (계획서 §6 Phase 3 P3 분기 2)
    """
    project_mcp = project_root / ".kiro" / "settings" / "mcp.json"
    home_mcp = Path.home() / ".kiro" / "settings" / "mcp.json"

    registered: dict[str, list[str]] = {name: [] for name in TARGET_MCP_SERVERS}
    sources_read: list[str] = []
    parse_errors: list[str] = []

    for label, mcp_path in (("project", project_mcp), ("user", home_mcp)):
        if not mcp_path.is_file():
            continue
        try:
            data = json.loads(mcp_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            parse_errors.append(f"{label}: {exc}")
            continue
        servers = data.get("mcpServers", {}) if isinstance(data, dict) else {}
        if not isinstance(servers, dict):
            continue
        sources_read.append(label)
        for server_name in servers.keys():
            for target in TARGET_MCP_SERVERS:
                # 정확 매치. 변형은 감지하지 않음 (Q2 정적 감지 원칙).
                if server_name == target:
                    registered[target].append(label)

    any_registered = any(registered[name] for name in TARGET_MCP_SERVERS)
    state = "exists" if any_registered else "missing"

    if any_registered:
        guidance = (
            "감지된 서버는 INDEX Tool Links 등록 대상. 미감지 서버는 Tier 3 baseline. "
            "편집은 Mickey 가 사용자 확인 후 결정."
        )
    else:
        guidance = (
            "serena · graphify 미등록. 그래프 접근은 파일 기반 (INDEX/GRAPH/PROFILE) 만 사용."
        )

    return BranchResult(
        name="MCP-TOOLS",
        state=state,
        detail={
            "servers": {name: registered[name] for name in TARGET_MCP_SERVERS},
            "sources_read": sources_read,
            "parse_errors": parse_errors,
        },
        guidance=guidance,
    )


# --- stdin 파싱 (선택) ---------------------------------------------------

def read_hook_context(enabled: bool) -> dict[str, Any] | None:
    """CLI v3 hook 이 stdin 으로 넘긴 세션 컨텍스트 JSON 을 파싱.

    - enabled=False 이면 (사용자 직접 실행) 즉시 스킵. stdin block 위험 회피.
    - enabled=True 이면 stdin 을 EOF 까지 읽고 JSON 파싱.
    - JSON 파싱 실패 시 None 반환. 스크립트는 그래도 계속 진행 (단독 실행 지원).

    hook JSON 에서는 command 에 `--read-stdin` 을 붙여 활성. 단독 실행 시는 붙이지 않음.
    """
    if not enabled:
        return None
    if sys.stdin is None:
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
    """분기 결과를 사람이 읽고 Mickey 가 소화할 수 있는 형태로 렌더링.

    - 각 항목 헤더는 `[BRANCH: <NAME>] <state>` 형식 (검증기 grep 대상).
    - 세부 정보 · 가이던스는 들여쓰기로 표시.
    """
    lines: list[str] = []
    lines.append("=== Mickey Session Boot Report ===")
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

    lines.append("=== End Boot Report ===")
    return "\n".join(lines)


# --- 진입점 --------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mickey Session Boot 실측 리포트 스크립트 (Phase 3).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="프로젝트 루트 경로 (기본: 현재 작업 디렉토리).",
    )
    parser.add_argument(
        "--brownfield-threshold",
        type=int,
        default=BROWNFIELD_CODE_THRESHOLD,
        help=f"Brownfield 판정 임계값 (기본: {BROWNFIELD_CODE_THRESHOLD}).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="분기 결과를 JSON 형식으로 출력 (기본은 사람이 읽는 텍스트).",
    )
    parser.add_argument(
        "--read-stdin",
        action="store_true",
        help="stdin 에서 hook 컨텍스트 JSON 을 읽음 (hook 자동 호출 시에만 사용).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    project_root = args.project_root.resolve()

    if not project_root.is_dir():
        print(f"ERROR: project root not a directory: {project_root}", file=sys.stderr)
        return 1

    hook_context = read_hook_context(enabled=args.read_stdin)

    results = [
        detect_purpose_scenario(project_root),
        detect_handoff(project_root),
        detect_brownfield(project_root, args.brownfield_threshold),
        detect_mcp_registration(project_root),
    ]

    if args.json:
        payload = {
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
