# -*- coding: utf-8 -*-
"""M42 포스트모템 — §18 Activity Metrics 실측 (M21 baseline 대조).

방법론: m21_measure_usage.py와 동일 PATTERNS(정규식 그대로 복사)로 비교 가능성 유지.
- 카운트: 프로젝트별 SESSION+HANDOFF 파일의 키워드 출현 합산
- 세션당 평균: 합산 ÷ SESSION 파일 수 (M21 방식)
- 경계: M21 baseline 확정 시점(2026-06-19 23:59 KST) 이후 mtime = "신규" (측정 대상)
- 표본 가드 (M21 교훈): ai-developer-mickey(자기 자신)는 별도 행 — 메타 작업 편향
- 추가: [Protocol] 태그 원문 라인 수집 (경량 포스트모템 정성 분석용)

출력: scripts/output/m42_metrics.txt + scripts/output/m42_protocol_lines.txt
"""
from __future__ import annotations

import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

KST = timezone(timedelta(hours=9))
# M21 baseline 확정 시점 이후를 측정 윈도우로 (약 9주)
M21_BOUNDARY = datetime(2026, 6, 19, 23, 59, 59, tzinfo=KST).timestamp()

# 활성 프로젝트 (2026-08-21 전수 스캔 — M21 경계 이후 세션 존재)
# work\kiro 루트 직접 위치 SESSION 2건은 M41 serena 오배치 산물로 제외 (별도 보고)
PROJECTS = [
    ("ai-developer-mickey", Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")),
    ("anjin-llm-scenario-poc", Path(r"C:\Users\hcsung\work\kiro\anjin-llm-scenario-poc")),
    ("back-to-basic-modernize", Path(r"C:\Users\hcsung\work\kiro\back-to-basic-modernize")),
    ("epic-lore-benchmark", Path(r"C:\Users\hcsung\work\kiro\epic-lore-benchmark")),
    ("unreal-mcp-demo", Path(r"C:\Users\hcsung\work\kiro\unreal-mcp-demo")),
    ("kirocrew-0.1.3", Path(r"C:\Users\hcsung\work\kiro\kirocrew-0.1.3")),
    ("vpco-incident-lab", Path(r"C:\Users\hcsung\work\kiro\vpco-incident-lab")),
    # mickey-power 제외: sessions/ 33건 전부 2026-07-16 동일 mtime = m38 워크스페이스 복사 산물
    # (본 프로젝트 아카이브 복사본 — 이중 카운트 + 자기 메타 편향 이중 오염)
    ("bvt-anjin-comparison", Path(r"C:\Users\hcsung\work\kiro\bvt-anjin-comparison")),
    ("gamejob_crawler", Path(r"C:\Users\hcsung\work\gamejob_crawler")),
    ("vision-math-helper", Path(r"C:\Users\hcsung\work\kiro\vision-math-helper")),
    ("code-analyze-helper", Path(r"C:\Users\hcsung\work\kiro\code-analyze-helper")),
]
# 모든 프로젝트에 대해 동일한 후보 서브디렉토리 스캔 (m21의 명시 목록 방식을 일반화)
SUBDIRS = ["", "sessions", ".kiro/mickey", ".kiro/mickey/sessions"]

# m21_measure_usage.py PATTERNS 원본 그대로 (비교 가능성)
PATTERNS = [
    ("global_domain", re.compile(r"~/\.kiro/mickey|\.kiro[\\/]mickey[\\/]domain|mickey/domain/entries|domain/entries/|domain/INDEX|domain/GRAPH|domain/PROFILE", re.IGNORECASE)),
    ("common_knowledge", re.compile(r"common_knowledge", re.IGNORECASE)),
    ("context_rule", re.compile(r"context_rule", re.IGNORECASE)),
    ("auto_notes", re.compile(r"auto_notes", re.IGNORECASE)),
    ("protocol_tag", re.compile(r"\[Protocol[+\-]?\]")),
    ("curator", re.compile(r"curator|knowledge-curator", re.IGNORECASE)),
]

# §18 baseline (M21, 5주 31세션) + 임계값
BASELINE = {"global_domain": (2.45, 0.5), "curator": (2.65, 0.5),
            "auto_notes": (5.55, 1.0), "protocol_tag": (2.03, 0.3)}

OUT_METRICS = Path(__file__).resolve().parent / "output" / "m42_metrics.txt"
OUT_PROTO = Path(__file__).resolve().parent / "output" / "m42_protocol_lines.txt"

PROTO_LINE = re.compile(r"^.*\[Protocol[+\-]?\].*$", re.MULTILINE)


def main() -> int:
    lines, proto_lines = [], []
    grand = {}  # name -> (sessions, counts dict)
    for name, root in PROJECTS:
        seen: set[Path] = set()
        counts = {label: 0 for label, _ in PATTERNS}
        n_sessions = 0
        for sub in SUBDIRS:
            d = root / sub if sub else root
            if not d.exists():
                continue
            for pattern in ("MICKEY-*-SESSION.md", "MICKEY-*-HANDOFF.md"):
                for p in d.glob(pattern):
                    if p in seen:
                        continue
                    seen.add(p)
                    if p.stat().st_mtime <= M21_BOUNDARY:
                        continue  # 측정 윈도우 밖
                    text = p.read_text(encoding="utf-8", errors="replace")
                    for label, pat in PATTERNS:
                        counts[label] += len(pat.findall(text))
                    if "SESSION" in p.name:
                        n_sessions += 1
                    for m in PROTO_LINE.findall(text):
                        proto_lines.append(f"[{name}/{p.name}] {m.strip()}")
        grand[name] = (n_sessions, counts)

    # 리포트 조립
    def block(title, names):
        total_s = sum(grand[n][0] for n in names)
        agg = {label: sum(grand[n][1][label] for n in names) for label, _ in PATTERNS}
        lines.append(f"\n## {title} — 세션 {total_s}건 (윈도우: 2026-06-20 ~ 08-21)")
        lines.append(f"{'metric':<18}{'count':>7}{'/세션':>8}{'baseline':>10}{'임계':>7}{'판정':>8}")
        for label, _ in PATTERNS:
            avg = agg[label] / total_s if total_s else 0.0
            if label in BASELINE:
                base, thresh = BASELINE[label]
                verdict = "OK" if avg >= thresh else "VIOLATION"
                lines.append(f"{label:<18}{agg[label]:>7}{avg:>8.2f}{base:>10.2f}{thresh:>7.2f}{verdict:>10}")
            else:
                lines.append(f"{label:<18}{agg[label]:>7}{avg:>8.2f}{'—':>10}{'—':>7}{'—':>10}")
        return total_s

    others = [n for n, _ in PROJECTS if n != "ai-developer-mickey"]
    lines.append("# M42 Activity Metrics (M21 baseline 대조)")
    block("전체 (표본 전체)", [n for n, _ in PROJECTS])
    block("타 프로젝트만 (표본 가드 — 우선 판정 기준)", others)
    block("ai-developer-mickey 단독 (메타 편향 참고용)", ["ai-developer-mickey"])

    lines.append("\n## 프로젝트별 세션 수 (윈도우 내)")
    for n, _ in PROJECTS:
        lines.append(f"- {n}: {grand[n][0]}")

    OUT_METRICS.parent.mkdir(parents=True, exist_ok=True)
    OUT_METRICS.write_text("\n".join(lines), encoding="utf-8")
    OUT_PROTO.write_text("\n".join(proto_lines), encoding="utf-8")
    print(f"written: {OUT_METRICS}")
    print(f"written: {OUT_PROTO} ({len(proto_lines)} protocol lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
