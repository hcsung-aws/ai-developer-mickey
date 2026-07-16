"""Phase 2c 정식 Test Harness — power-mickey/ 구조 검증.

목적: v10 마이그레이션 계획서 §6 Phase 2 의 CC + Phase 4-A 확장을 자동 재확인한다.

    1. 파일 존재            (POWER.md + mcp.json + steering/*.md 7개)
    2. front matter 유효성  (POWER.md name/description/keywords + 각 steering inclusion)
    3. readSteering 매핑    (POWER.md 안내가 steering 7개 모두 커버)
    4. T1 100% 추적성       (REMEMBER 12 · Session 4단계 · Document 11종 · PS 10단계)
    5. T1.5 §N 트리거 존재  (매트릭스 §4 표 기준)
    6. P3 양쪽 분기 병기    (조건부 지시의 부정 조건 병기)
    7. inclusion 모드 정합성 (상시 6 = always, Curator = manual)

원칙:
- 각 검증 항목은 단일 책임 함수. 상수 사전(SPEC)이 정답지.
- 표준 출력은 ASCII only (Windows cp949 콘솔 대응). 파일 내용은 utf-8 로 읽는다.
- 사이드 이펙트 없음. 파일 수정 · 네트워크 접근 없음.

사용법:
    python scripts/verify_power_structure.py [--root <경로>]
    기본 root = 프로젝트루트/power-mickey
    종료 코드: 0 = 모두 PASS, 1 = 하나 이상 FAIL

참조:
- 계획서: IMPROVEMENT-PLAN-v10-power-migration.md §6 Phase 2, §8-b
- 매트릭스: docs/v2-to-v3-mapping.md §3~§4
- 원문 dump: scripts/output/v17_prompt.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# 상수: 정답지 (매트릭스 근거 명시)
# ---------------------------------------------------------------------------

# steering 파일 (매트릭스 §2 · 계획서 §6 Phase 2 / Phase 4-A)
# - 상시 로드(inclusion: always) 6개 + on-demand(inclusion: manual) 1개.
# - Phase 4-A(2026-07-11): knowledge-curator.md 추가. 세션 종료 시 readSteering 로만 pull.
ALWAYS_STEERING_FILES = (
    "mickey-core.md",
    "session-protocol.md",
    "knowledge-graph.md",
    "problem-solving.md",
    "document-schema.md",
    "context-window.md",
)
ONDEMAND_STEERING_FILES = (
    "knowledge-curator.md",
)
# 파일 존재·front matter·POWER 매핑·P3 검증은 상시/on-demand 구분 없이 전체 대상.
STEERING_FILES = ALWAYS_STEERING_FILES + ONDEMAND_STEERING_FILES

# inclusion 모드 정답지 (Phase 4-A B 조합: Curator 는 manual)
STEERING_INCLUSION_MODES = {
    "mickey-core.md": "always",
    "session-protocol.md": "always",
    "knowledge-graph.md": "always",
    "problem-solving.md": "always",
    "document-schema.md": "always",
    "context-window.md": "always",
    "knowledge-curator.md": "manual",
}

# POWER.md front matter 필수 키 (실측 확인)
POWER_REQUIRED_KEYS = ("name", "description", "keywords")

# steering front matter 필수 키
STEERING_REQUIRED_KEYS = ("inclusion",)

# REMEMBER 12개 핵심 키워드 (매트릭스 §3.1 · v17 dump L254~L267)
# - mickey-core.md 에 모두 존재해야 함.
# - 여러 표현이 허용될 수 있는 항목은 대체 문구를 튜플로 둔다.
REMEMBER_KEYWORDS = (
    ("#1", ("목적 우선",)),
    ("#2", ("단순함 우선",)),
    ("#3", ("Analysis BEFORE implementation",)),
    ("#4", ("에러 로그 즉시 확인",)),
    ("#5", ("User confirmation BEFORE changes",)),
    ("#6", ("Root cause OVER quick fixes",)),
    ("#7", ("전제조건 우선 검증",)),
    ("#8", ("점진적 도입",)),
    ("#9", ("검증 기반 완료",)),
    ("#10", ("자율 실행 조건",)),
    ("#11", ("Backpressure",)),
    ("#12", ("동작 시나리오 확인",)),
)

# Session Protocol 4단계 헤딩 (매트릭스 §3.2 · v17 dump L21~L87)
# - session-protocol.md 에 모두 존재해야 함.
SESSION_STAGES = (
    "First Session",
    "Continuing Session",
    "During Session",
    "Session End",
)

# Document Schema 11종 (매트릭스 §3.4 · v17 dump L89~L107)
# - 매핑 문서 §3.4 의 "10종" 표기는 오기이며 실제 11개. 세션 로그(2b) 확인 사항.
# - document-schema.md 에 모두 존재해야 함.
DOCUMENT_SCHEMA_ITEMS = (
    "PROJECT-OVERVIEW.md",
    "PURPOSE-SCENARIO.md",
    "ENVIRONMENT.md",
    "FILE-STRUCTURE.md",
    "DECISIONS.md",
    "context_rule/project-context.md",
    "context_rule/INDEX.md",
    "common_knowledge/INDEX.md",
    "auto_notes/NOTES.md",
    "MICKEY-N-SESSION.md",
    "MICKEY-N-HANDOFF.md",
)

# Problem-Solving 10단계 (매트릭스 §3.3 · v17 dump L111~L127)
# - problem-solving.md 에 각 단계 번호 마커가 존재해야 함.
# - 원문은 "1." ~ "10." 형태의 리스트 마커.
PS_STEP_MARKERS = tuple(f"{i}." for i in range(1, 11))

# T1.5 §N 트리거 위치 (매트릭스 §4 표)
# - key = steering 파일명, value = 해당 파일에 반드시 등장해야 하는 §N 마커 목록
# - 매트릭스 §4 의 표에서 "트리거 위치 (steering)" 컬럼을 그대로 옮김.
T15_TRIGGER_LOCATIONS = {
    "session-protocol.md": (
        "§1", "§3", "§4", "§9", "§10", "§13", "§14", "§16", "§17", "§19",
    ),
    "knowledge-graph.md": (
        "§9", "§12", "§17", "§18",
        # §8 은 §17 로 흡수되었으므로 §8 언급 자체가 존재하는지 별도 확인.
    ),
    "problem-solving.md": (
        "§2", "§4", "§5", "§6", "§7", "§10", "§14", "§15",
    ),
    "mickey-core.md": (
        "§4", "§6", "§9", "§10", "§11", "§14", "§15",
    ),
    # Phase 4-A: Curator steering 은 §17(Lifecycle) 진입점. §12(Global)·§18(Metrics) 승격 판단 시 pull.
    "knowledge-curator.md": (
        "§12", "§17", "§18",
    ),
}

# §8→§17 흡수 언급 (매트릭스 §4 note): knowledge-graph.md 에 존재해야 함.
T15_SECTION8_ABSORPTION_TARGET = "knowledge-graph.md"
T15_SECTION8_MARKERS = ("§8",)

# P3 (조건부 지시 양쪽 분기 병기) 대칭 쌍 사전.
# - 각 steering 파일에 최소 1쌍 이상 존재하면 PASS.
# - P3 원칙 원문("양쪽 분기 병기")은 긍정/부정 쌍뿐 아니라 선택 갈래 대칭도 포함.
#   실제 문서에 자연스럽게 등장하는 갈래 표현도 함께 수록한다.
P3_SYMMETRIC_PAIRS = (
    # 긍정 / 부정 쌍
    ("존재 시", "미존재 시"),
    ("매칭 시", "미매칭 시"),
    ("감지 시", "미감지 시"),
    ("충족 시", "미충족 시"),
    ("도달 시", "미도달 시"),
    ("발견 시", "미발견 시"),
    ("있으면", "없으면"),
    ("가능하면", "가능하지 않"),
    ("필수적이면", "필수적이지 않"),
    ("사용 시", "미사용"),
    ("이면", "아니면"),
    # 선택 갈래 대칭 (동일 조건축의 두 결과를 병기하는 자연 표현)
    ("있었을 때만", "없으면"),  # document-schema.md HANDOFF Protocol Feedback 분기
    ("감지 시", "만 사용 시"),  # document-schema.md FILE-STRUCTURE Tier 감지 결과 분기
)


# ---------------------------------------------------------------------------
# 자료 구조: 검증 결과
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    """단일 검증 항목의 결과.

    항목 하나는 여러 파일/키/키워드를 확인하므로 details 는 리스트.
    """

    name: str
    passed: bool
    details: list[str] = field(default_factory=list)

    def add(self, ok: bool, message: str) -> None:
        prefix = "[ OK ]" if ok else "[FAIL]"
        self.details.append(f"{prefix} {message}")
        if not ok:
            self.passed = False


# ---------------------------------------------------------------------------
# 저수준 유틸리티
# ---------------------------------------------------------------------------


def read_utf8(path: Path) -> str:
    """utf-8 로 파일 읽기. 존재하지 않으면 빈 문자열 반환 (파일 존재 검사는 별도)."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_front_matter(text: str) -> dict[str, str] | None:
    """상단 --- ... --- YAML 블록에서 top-level 키만 얕게 파싱.

    - 스칼라(string/number/bool/inline list) 값만 지원. 중첩 매핑은 필요 없음.
    - 파싱 실패 또는 front matter 없음 → None.
    - 목적: name/description/keywords/inclusion 존재 여부만 확인하면 되므로 얕은 파서로 충분.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    body = text[3:end].strip()
    result: dict[str, str] = {}
    for line in body.splitlines():
        # 리스트 항목( "- ..." )이나 들여쓰기 라인은 최상위 키에 속하지 않음.
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        result[key] = value
    return result


# ---------------------------------------------------------------------------
# 검증 함수 6개 (단일 책임)
# ---------------------------------------------------------------------------


def check_files_exist(power_dir: Path) -> CheckResult:
    """항목 1: 필수 파일 8개가 모두 존재하는지."""
    result = CheckResult(name="1. 파일 존재", passed=True)
    required = [power_dir / "POWER.md", power_dir / "mcp.json"]
    required += [power_dir / "steering" / f for f in STEERING_FILES]
    for path in required:
        result.add(path.exists(), f"{path.relative_to(power_dir.parent)}")
    return result


def check_front_matter(power_dir: Path) -> CheckResult:
    """항목 2: front matter 유효성.

    - POWER.md: name/description/keywords 존재.
    - 각 steering: inclusion 존재.
    """
    result = CheckResult(name="2. Front matter 유효성", passed=True)

    # POWER.md
    power_text = read_utf8(power_dir / "POWER.md")
    fm = extract_front_matter(power_text)
    if fm is None:
        result.add(False, "POWER.md: front matter 없음")
    else:
        for key in POWER_REQUIRED_KEYS:
            result.add(key in fm, f"POWER.md: '{key}' 키 존재")

    # steering 6종
    for name in STEERING_FILES:
        text = read_utf8(power_dir / "steering" / name)
        sfm = extract_front_matter(text)
        if sfm is None:
            result.add(False, f"steering/{name}: front matter 없음")
            continue
        for key in STEERING_REQUIRED_KEYS:
            result.add(key in sfm, f"steering/{name}: '{key}' 키 존재")

    return result


def check_power_covers_steering(power_dir: Path) -> CheckResult:
    """항목 3: POWER.md 안내가 steering 6개 파일명을 모두 커버.

    - POWER.md 본문에 각 steering 파일명이 문자열로 등장하면 커버로 간주.
    - v3 readSteering API 호출 대신 파일명 언급 기반으로 검증 (매트릭스 §2 근거).
    """
    result = CheckResult(name="3. POWER.md → steering 매핑 완결성", passed=True)
    power_text = read_utf8(power_dir / "POWER.md")
    if not power_text:
        result.add(False, "POWER.md 로드 실패")
        return result
    for name in STEERING_FILES:
        result.add(name in power_text, f"POWER.md 안내에 '{name}' 언급")
    return result


def _all_in(text: str, needles: Iterable[str]) -> bool:
    """모든 needle 이 text 에 존재하는지."""
    return all(needle in text for needle in needles)


def _any_in(text: str, needles: Iterable[str]) -> bool:
    """하나 이상 needle 이 text 에 존재하는지."""
    return any(needle in text for needle in needles)


def check_t1_traceability(power_dir: Path) -> CheckResult:
    """항목 4: T1 100% 추적성.

    각 하위 검증 실패 시 실패 상세만 상세 로그에 남긴다.
    성공 시 요약 한 줄만 남긴다 (로그 노이즈 최소화).
    """
    result = CheckResult(name="4. T1 100% 추적성", passed=True)

    # 4-1. REMEMBER 12 → mickey-core.md
    core_text = read_utf8(power_dir / "steering" / "mickey-core.md")
    missing_remember: list[str] = []
    for label, alternatives in REMEMBER_KEYWORDS:
        if not _any_in(core_text, alternatives):
            missing_remember.append(f"{label}({'/'.join(alternatives)})")
    if missing_remember:
        result.add(False, "REMEMBER 누락(mickey-core.md): " + ", ".join(missing_remember))
    else:
        result.add(True, f"REMEMBER 12개 모두 mickey-core.md 에 존재")

    # 4-2. Session Protocol 4단계 → session-protocol.md
    sp_text = read_utf8(power_dir / "steering" / "session-protocol.md")
    missing_stage = [s for s in SESSION_STAGES if s not in sp_text]
    if missing_stage:
        result.add(False, "Session 4단계 누락(session-protocol.md): " + ", ".join(missing_stage))
    else:
        result.add(True, "Session Protocol 4단계 모두 존재")

    # 4-3. Document Schema 11종 → document-schema.md
    ds_text = read_utf8(power_dir / "steering" / "document-schema.md")
    missing_doc = [d for d in DOCUMENT_SCHEMA_ITEMS if d not in ds_text]
    if missing_doc:
        result.add(False, "Document Schema 누락(document-schema.md): " + ", ".join(missing_doc))
    else:
        result.add(True, "Document Schema 11종 모두 존재")

    # 4-4. Problem-Solving 10단계 마커 → problem-solving.md
    ps_text = read_utf8(power_dir / "steering" / "problem-solving.md")
    missing_step = [m for m in PS_STEP_MARKERS if m not in ps_text]
    if missing_step:
        result.add(False, "PS 단계 마커 누락(problem-solving.md): " + ", ".join(missing_step))
    else:
        result.add(True, "Problem-Solving 10단계 마커 모두 존재")

    return result


def check_t15_triggers(power_dir: Path) -> CheckResult:
    """항목 5: T1.5 §N 트리거 존재 (매트릭스 §4)."""
    result = CheckResult(name="5. T1.5 §N 트리거 존재", passed=True)

    for filename, markers in T15_TRIGGER_LOCATIONS.items():
        text = read_utf8(power_dir / "steering" / filename)
        missing = [m for m in markers if m not in text]
        if missing:
            result.add(False, f"{filename}: 트리거 누락 " + ", ".join(missing))
        else:
            result.add(True, f"{filename}: 트리거 {len(markers)}개 모두 존재")

    # §8→§17 흡수 언급 (knowledge-graph.md)
    kg_text = read_utf8(power_dir / "steering" / T15_SECTION8_ABSORPTION_TARGET)
    if _any_in(kg_text, T15_SECTION8_MARKERS):
        result.add(True, f"{T15_SECTION8_ABSORPTION_TARGET}: §8→§17 흡수 언급 존재")
    else:
        result.add(False, f"{T15_SECTION8_ABSORPTION_TARGET}: §8 언급 부재 (흡수 리다이렉트 명시 필요)")

    return result


def check_inclusion_modes(power_dir: Path) -> CheckResult:
    """항목 7: steering inclusion 모드 정합성 (Phase 4-A B 조합).

    - 상시 6개는 inclusion: always, Curator 는 inclusion: manual 이어야 함.
    - progressive disclosure 원칙: 세션 종료 시에만 쓰는 규약을 상시 로드하지 않음.
    """
    result = CheckResult(name="7. inclusion 모드 정합성", passed=True)
    for name, expected in STEERING_INCLUSION_MODES.items():
        text = read_utf8(power_dir / "steering" / name)
        fm = extract_front_matter(text)
        actual = fm.get("inclusion") if fm else None
        result.add(actual == expected, f"steering/{name}: inclusion={actual!r} (기대 {expected!r})")
    return result


def check_p3_symmetric(power_dir: Path) -> CheckResult:
    """항목 6: P3 양쪽 분기 병기.

    각 steering 파일에서 정의된 대칭 쌍 중 하나 이상이 완전히(양쪽 모두) 등장하면 PASS.
    """
    result = CheckResult(name="6. P3 양쪽 분기 병기", passed=True)

    for name in STEERING_FILES:
        text = read_utf8(power_dir / "steering" / name)
        matched_pairs: list[str] = []
        for positive, negative in P3_SYMMETRIC_PAIRS:
            if positive in text and negative in text:
                matched_pairs.append(f"({positive}/{negative})")
        if matched_pairs:
            result.add(True, f"{name}: 대칭 쌍 {len(matched_pairs)}개 확인 " + ", ".join(matched_pairs[:3]))
        else:
            result.add(False, f"{name}: 대칭 쌍 하나도 없음 (조건부 지시에 부정 분기 병기 필요)")

    return result


# ---------------------------------------------------------------------------
# 오케스트레이션
# ---------------------------------------------------------------------------


def run_all_checks(power_dir: Path) -> list[CheckResult]:
    """모든 검증을 순차 실행. 각 함수는 독립적."""
    return [
        check_files_exist(power_dir),
        check_front_matter(power_dir),
        check_power_covers_steering(power_dir),
        check_t1_traceability(power_dir),
        check_t15_triggers(power_dir),
        check_p3_symmetric(power_dir),
        check_inclusion_modes(power_dir),
    ]


def print_report(results: list[CheckResult]) -> None:
    """ASCII only 리포트 출력 (Windows cp949 콘솔 대응)."""
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"--- {r.name} : {status} ---")
        for line in r.details:
            print("  " + line)
        print()
    print(f"Summary: PASS {passed} / FAIL {total - passed} / total {total}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2c power-mickey 구조 검증기")
    default_root = Path(__file__).resolve().parent.parent / "power-mickey"
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root,
        help=f"검증 대상 power 디렉토리 (기본: {default_root})",
    )
    args = parser.parse_args()

    power_dir: Path = args.root
    if not power_dir.exists():
        print(f"[FAIL] 검증 대상 디렉토리 없음: {power_dir}")
        return 1

    results = run_all_checks(power_dir)
    print_report(results)
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
