# -*- coding: utf-8 -*-
"""M42: T1.5 extended-protocols §17 v23→v24 — Curator 호출 전송 규약 신설 (delegate→use_subagent).

배경 (M42 실측): delegate는 머신 전역 저장소(.subagents/)에 agent 이름 키로 상태를 남기고
status 폴링으로 결과를 수신하는 session-agnostic 설계 — 멀티 세션에서 Curator 결과가
타 세션에 출력되는 crosstalk 발생. use_subagent는 동기 + in-band 반환 + UUID 키로 구조적 안전.

대상 (adaptive #3: global 수정 시 repo 미러 동기화):
1. ~/.kiro/mickey/extended-protocols.md (글로벌, T1.5 런타임 로딩)
2. {repo}/mickey/extended-protocols.md (repo 미러, install 배포원)

변경 3건 (safe-batch-replace count-1 guard):
1. 라이프사이클 다이어그램: delegate 문구 → use_subagent 동기 호출
2. "Curator 호출 전송 규약 (M42)" 소절 신설 (분기 판단 기준 앞에 삽입)
3. Version 23 → 24 + Changes (v24) 추가

백업: 글로벌은 .bak-ai-developer-mickey-m42 (사전 생성 확인), repo는 git 추적이라 불필요.
판정: 리포트 파일 실측 (adaptive #14 — 콘솔 출력 잘림 대비).
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GLOBAL_MD = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO_MD = Path(__file__).resolve().parent.parent / "mickey" / "extended-protocols.md"
OUT = Path(__file__).resolve().parent / "output" / "m42_protocols_v24.txt"

EDITS = []

# 1) 라이프사이클 다이어그램 — 전송 방식 개정
EDITS.append((
    "Knowledge Curator (subagent delegate — 락 사용 중이면 메인 세션이 직접 대행, 격리 구조상 항상 안전)",
    "Knowledge Curator (use_subagent 동기 호출 — 결과 in-band 반환. 실패/미완주 시 메인 세션이 직접 대행, 격리 구조상 항상 안전)",
))

# 2) 전송 규약 소절 신설 — "분기 판단 기준" 제목 앞에 삽입
EDITS.append((
    "### 분기 판단 기준 (Curator 내부)",
    """### Curator 호출 전송 규약 (M42)

Curator 호출은 **use_subagent(동기)** 로만 수행한다. **delegate 사용 금지.**

- 금지 근거 (M42 실측): delegate는 머신 전역 단일 저장소(`<AppData>/kiro-cli/.subagents/`)에 **agent 이름 키**로 상태를 남기고, 결과 수신은 status 폴링뿐 — 상태 파일에 세션 식별자가 없고 `user_notified` 선점 플래그만 있어, **먼저 조회한 세션이 결과를 가로챈다** (crosstalk). 같은 agent를 타 세션이 launch하면 기존 작업이 replace됨
- use_subagent 안전 근거: 동기 실행 + 결과 in-band 반환(summary 도구) + 실행 아티팩트는 실행별 UUID 키 — 랑데부 저장소 자체가 없어 crosstalk 구조적 불가 (probe 실측: 전역 .subagents 무변화)
- 알려진 위험 (Kiro #6765): 응답 채널이 60~95초에 끊겨 장시간 작업이 미완주할 수 있음 — **완주 판정은 use_subagent 응답 표면이 아닌 staging 파일 디스크 실측으로**. 실패/미완주 시 메인 세션이 직접 대행 (격리 구조상 안전)
- 여러 세션의 동시 큐레이션은 안전 (쓰기 대상이 각 프로젝트 로컬 + 글로벌은 promote 락). 단 **같은 프로젝트**를 두 세션이 동시 정리하는 것은 피한다 (staging/adaptive.md 공유)

### 분기 판단 기준 (Curator 내부)""",
))

# 3) 버전 푸터
EDITS.append((
    "**Version**: 23\n**Last Updated**: 2026-08-08\n**Changes (v23)**:",
    "**Version**: 24\n**Last Updated**: 2026-08-19\n"
    "**Changes (v24)**: §17 Curator 호출 전송 규약 신설 (ai-developer-mickey M42): delegate → use_subagent(동기) 전환. "
    "근거: delegate 전역 상태(.subagents, agent 이름 키 + user_notified 선점 + status 폴링)가 session-agnostic이라 "
    "멀티 세션 crosstalk/replace 실측. use_subagent는 in-band 반환 + UUID 키로 구조적 안전 (probe 검증). "
    "완주 판정은 staging 디스크 실측 (Kiro #6765 채널 절단 대비), 실패 시 직접 대행. T1 v19와 연동.\n"
    "**Changes (v23)**:",
))


def apply(md_path: Path, report: list) -> bool:
    text = md_path.read_text(encoding="utf-8")
    for i, (old, new) in enumerate(EDITS, 1):
        n = text.count(old)
        if n != 1:
            report.append(f"[FAIL] {md_path} edit {i}: count={n} (기대 1)")
            return False
        text = text.replace(old, new)
    md_path.write_text(text, encoding="utf-8")
    report.append(f"[OK] {md_path}: 3건 적용")
    return True


def main() -> int:
    report, ok = [], True
    # 사전 조건: 글로벌 백업 존재 (adaptive #10)
    bak = GLOBAL_MD.with_name(GLOBAL_MD.name + ".bak-ai-developer-mickey-m42")
    if not bak.exists():
        report.append(f"[FAIL] 백업 미존재: {bak}")
        ok = False
    if ok:
        for target in (GLOBAL_MD, REPO_MD):
            ok &= apply(target, report)
    if ok:
        g = GLOBAL_MD.read_text(encoding="utf-8")
        r = REPO_MD.read_text(encoding="utf-8")
        checks = [
            (g == r, "global == repo (내용 일치)"),
            ("Curator 호출 전송 규약 (M42)" in g, "신규 소절 존재"),
            ("use_subagent 동기 호출 — 결과 in-band 반환" in g, "다이어그램 개정"),
            ("**Version**: 24" in g, "Version 24"),
            ("subagent delegate — 락 사용 중이면" not in g, "구 다이어그램 문구 잔존 0"),
            ("**Version**: 23\n**Last Updated**" not in g, "구 버전 푸터 잔존 0"),
        ]
        for cond, label in checks:
            report.append(f"[{'PASS' if cond else 'FAIL'}] {label}")
            ok &= cond
    report.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(report), encoding="utf-8")
    print(f"written: {OUT} ({'ALL PASS' if ok else 'FAIL'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
