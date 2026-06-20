"""
Mickey 21 — 5주간 누적 활용도 정량 측정 스크립트.

목적:
- M20 진단(76세션, 글로벌 domain 0% / Curator 0회)이 5주 후에도 유효한지 검증.
- 프로젝트별로 SESSION/HANDOFF 파일에서 지식 저장소 참조 횟수 + [Protocol] 태그 + Curator 호출 흔적 측정.
- 5주 경계(2026-05-14, M20 종료 시점) 기준으로 신규/기존 구분.

출력: stdout으로 표 형태 (프로젝트별 + 전체 합계). 결과는 SESSION 로그에 수동 정리.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# 측정 경계: M20 종료 시점 (2026-05-14 23:59:59 UTC). 그 이후 mtime은 "신규".
M20_BOUNDARY = datetime(2026, 5, 14, 23, 59, 59, tzinfo=timezone.utc).timestamp()

# 측정 대상 프로젝트 정의: (이름, 루트 경로, 추가 SESSION 디렉토리 리스트)
# 각 프로젝트의 SESSION/HANDOFF 파일이 있는 곳을 모두 포함.
PROJECTS = [
    (
        "ai-developer-mickey",
        Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey"),
        ["", "sessions"],  # 루트 + sessions/ (sessions/는 archived M2~M5만 있음, 측정 포함)
    ),
    (
        "code-analyze-helper",
        Path(r"C:\Users\hcsung\work\kiro\code-analyze-helper"),
        ["", "sessions"],
    ),
    (
        "vision-math-helper",
        Path(r"C:\Users\hcsung\work\kiro\vision-math-helper"),
        [".kiro/mickey", ".kiro/mickey/sessions"],  # 비표준 구조
    ),
    (
        "aws-cost-audit-project",
        Path(r"C:\Users\hcsung\work\kiro\aws-cost-audit-project"),
        [""],
    ),
    (
        "gamejob_crawler",
        Path(r"C:\Users\hcsung\work\gamejob_crawler"),
        ["", "sessions"],
    ),
    (
        "skr-reverse-poc",
        Path(r"C:\Users\hcsung\work\kiro\skr-reverse-poc"),
        ["", "sessions"],
    ),
]

# 측정 키워드: (라벨, regex 패턴, case_sensitive)
# 글로벌 domain은 Windows/Unix 경로 모두 포착.
PATTERNS = [
    ("global_domain", re.compile(r"~/\.kiro/mickey|\.kiro[\\/]mickey[\\/]domain|mickey/domain/entries|domain/entries/|domain/INDEX|domain/GRAPH|domain/PROFILE", re.IGNORECASE), False),
    ("common_knowledge", re.compile(r"common_knowledge", re.IGNORECASE), False),
    ("context_rule", re.compile(r"context_rule", re.IGNORECASE), False),
    ("auto_notes", re.compile(r"auto_notes", re.IGNORECASE), False),
    ("protocol_tag", re.compile(r"\[Protocol[+\-]?\]"), True),
    ("curator", re.compile(r"curator|knowledge-curator", re.IGNORECASE), False),
    ("graph_md", re.compile(r"GRAPH\.md|domain[\\/]GRAPH"), True),
    ("patterns_global", re.compile(r"~/\.kiro/mickey/patterns|mickey[\\/]patterns[\\/]"), False),
]


@dataclass
class FileMeasurement:
    """단일 파일 측정 결과."""
    path: Path
    mtime: float
    counts: dict = field(default_factory=dict)
    line_count: int = 0


@dataclass
class ProjectMeasurement:
    """프로젝트 단위 집계 결과."""
    name: str
    files_total: int = 0
    files_recent: int = 0  # M20 이후 mtime
    sessions: list[FileMeasurement] = field(default_factory=list)
    handoffs: list[FileMeasurement] = field(default_factory=list)
    # 카테고리별 카운트 합계 (전체/recent)
    counts_total: dict = field(default_factory=dict)
    counts_recent: dict = field(default_factory=dict)


def measure_file(path: Path) -> FileMeasurement:
    """파일 한 개 측정: 키워드별 출현 횟수 + 줄 수 + mtime."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"[WARN] read fail: {path} ({exc})", file=sys.stderr)
        return FileMeasurement(path=path, mtime=0.0)

    counts = {label: len(pat.findall(text)) for label, pat, _ in PATTERNS}
    return FileMeasurement(
        path=path,
        mtime=path.stat().st_mtime,
        counts=counts,
        line_count=text.count("\n") + 1,
    )


def collect_project(name: str, root: Path, subdirs: list[str]) -> ProjectMeasurement:
    """프로젝트 단위로 SESSION/HANDOFF 파일을 모두 수집 + 측정."""
    proj = ProjectMeasurement(name=name)
    if not root.exists():
        print(f"[WARN] project root missing: {root}", file=sys.stderr)
        return proj

    seen: set[Path] = set()  # 중복 방지 (subdir 중첩 시)
    for sub in subdirs:
        target_dir = root / sub if sub else root
        if not target_dir.exists():
            continue

        for pattern in ("MICKEY-*-SESSION.md", "MICKEY-*-HANDOFF.md"):
            for p in target_dir.glob(pattern):
                # 재귀 X (각 디렉토리 표면만). subdirs 명시적으로 들어옴.
                if p in seen:
                    continue
                seen.add(p)
                fm = measure_file(p)
                if "SESSION" in p.name:
                    proj.sessions.append(fm)
                else:
                    proj.handoffs.append(fm)

    # 집계
    all_files = proj.sessions + proj.handoffs
    proj.files_total = len(all_files)
    proj.files_recent = sum(1 for fm in all_files if fm.mtime > M20_BOUNDARY)

    for label, _, _ in PATTERNS:
        proj.counts_total[label] = sum(fm.counts.get(label, 0) for fm in all_files)
        proj.counts_recent[label] = sum(
            fm.counts.get(label, 0) for fm in all_files if fm.mtime > M20_BOUNDARY
        )

    return proj


def fmt_count(c: int, files: int) -> str:
    """파일 수 대비 평균을 보기 쉽게 포매팅."""
    if files == 0:
        return f"{c:>4} (n/a)"
    avg = c / files
    return f"{c:>4} ({avg:>4.1f}/f)"


def print_report(projects: list[ProjectMeasurement]) -> None:
    """프로젝트별 측정 결과 표 출력."""
    headers = ["proj", "S", "H", "S5w", "global_dom", "patterns_g", "graph_md", "common_kn", "context_r", "auto_notes", "protocol", "curator"]
    print("=" * 120)
    print(f"{'PROJECT':<25} {'#S':>4} {'#H':>4} {'S5w':>4} {'gDOM':>10} {'patG':>10} {'GRAPH':>10} {'cKn':>10} {'ctxR':>10} {'autoN':>10} {'[Pr]':>10} {'curator':>10}")
    print("=" * 120)

    totals = {label: 0 for label, _, _ in PATTERNS}
    totals_recent = {label: 0 for label, _, _ in PATTERNS}
    sessions_total = 0
    sessions_recent = 0

    for p in projects:
        s = len(p.sessions)
        h = len(p.handoffs)
        s_recent = sum(1 for fm in p.sessions if fm.mtime > M20_BOUNDARY)
        sessions_total += s
        sessions_recent += s_recent

        for label, _, _ in PATTERNS:
            totals[label] += p.counts_total[label]
            totals_recent[label] += p.counts_recent[label]

        print(
            f"{p.name:<25} {s:>4} {h:>4} {s_recent:>4} "
            f"{p.counts_total['global_domain']:>10} "
            f"{p.counts_total['patterns_global']:>10} "
            f"{p.counts_total['graph_md']:>10} "
            f"{p.counts_total['common_knowledge']:>10} "
            f"{p.counts_total['context_rule']:>10} "
            f"{p.counts_total['auto_notes']:>10} "
            f"{p.counts_total['protocol_tag']:>10} "
            f"{p.counts_total['curator']:>10}"
        )

    print("-" * 120)
    print(
        f"{'TOTAL (all)':<25} {sessions_total:>4} {'':>4} {sessions_recent:>4} "
        f"{totals['global_domain']:>10} "
        f"{totals['patterns_global']:>10} "
        f"{totals['graph_md']:>10} "
        f"{totals['common_knowledge']:>10} "
        f"{totals['context_rule']:>10} "
        f"{totals['auto_notes']:>10} "
        f"{totals['protocol_tag']:>10} "
        f"{totals['curator']:>10}"
    )

    # M20 경계 후 신규만 별도 표시 (5주간 변화)
    print("=" * 120)
    print(f"{'PROJECT':<25} {'S5w':>4} {'  '*4} {'gDOM5w':>10} {'patG5w':>10} {'GRAPH5w':>10} {'cKn5w':>10} {'ctxR5w':>10} {'autoN5w':>10} {'[Pr]5w':>10} {'cur5w':>10}")
    print("-" * 120)
    for p in projects:
        s_recent = sum(1 for fm in p.sessions if fm.mtime > M20_BOUNDARY)
        if s_recent == 0 and sum(p.counts_recent.values()) == 0:
            continue
        print(
            f"{p.name:<25} {s_recent:>4} {'':>10} "
            f"{p.counts_recent['global_domain']:>10} "
            f"{p.counts_recent['patterns_global']:>10} "
            f"{p.counts_recent['graph_md']:>10} "
            f"{p.counts_recent['common_knowledge']:>10} "
            f"{p.counts_recent['context_rule']:>10} "
            f"{p.counts_recent['auto_notes']:>10} "
            f"{p.counts_recent['protocol_tag']:>10} "
            f"{p.counts_recent['curator']:>10}"
        )

    print("-" * 120)
    print(
        f"{'TOTAL (5w 신규)':<25} {sessions_recent:>4} {'':>10} "
        f"{totals_recent['global_domain']:>10} "
        f"{totals_recent['patterns_global']:>10} "
        f"{totals_recent['graph_md']:>10} "
        f"{totals_recent['common_knowledge']:>10} "
        f"{totals_recent['context_rule']:>10} "
        f"{totals_recent['auto_notes']:>10} "
        f"{totals_recent['protocol_tag']:>10} "
        f"{totals_recent['curator']:>10}"
    )
    print("=" * 120)


def main() -> int:
    projects = [collect_project(name, root, subs) for name, root, subs in PROJECTS]
    print_report(projects)
    return 0


if __name__ == "__main__":
    sys.exit(main())
