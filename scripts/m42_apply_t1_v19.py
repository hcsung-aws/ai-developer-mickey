# -*- coding: utf-8 -*-
"""M42: T1 시스템 프롬프트 v18→v19 — Session End 2단계 Curator 전송 전환 (delegate→use_subagent).

배경: delegate의 머신 전역 상태(.subagents, agent 이름 키 + user_notified 선점)가
멀티 세션 crosstalk을 유발 (M42 실측). use_subagent는 동기 + in-band 반환으로 구조적 안전.

대상 (m32/m41 선례: 독립 md 부재, JSON 2곳):
1. ~/.kiro/agents/ai-developer-mickey.json (활성 런타임)
2. {repo}/examples/ai-developer-mickey.json (install 배포원)

변경 3건 (prompt 필드 내부 문자열, safe-batch-replace count-1 guard):
1. Session End 2단계: delegate → use_subagent(동기) + 완주 판정 디스크 실측 + 직접 대행 폴백
2. Version 18 → 19
3. Changes 갱신

백업: .bak-ai-developer-mickey-m42. JSON escape 함정 회피 위해 json.load/dump 사용.
판정: 리포트 파일 실측 (adaptive #14).
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME_JSON = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"
REPO_JSON = Path(__file__).resolve().parent.parent / "examples" / "ai-developer-mickey.json"
OUT = Path(__file__).resolve().parent / "output" / "m42_t1_v19.txt"

EDITS = []

# 1) Session End 2단계 — 전송 방식 전환
EDITS.append((
    """2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 delegate. Curator는 글로벌을 쓰지 않는다(격리 원칙) — ① adaptive.md만 직접 수정, ② 모든 승격 후보(글로벌 domain은 gd- 번들, 그 외 ck-/cr-/pat-/remember-)를 프로젝트 _curator-staging/에 초안 작성. delegate가 BUSY(타 세션 실행 중)면 메인 세션이 직접 대행 — 격리 구조상 안전. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)""",
    """2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 use_subagent(동기)로 호출 — delegate 금지 (전역 상태가 멀티 세션 crosstalk 유발, T1.5 §17 전송 규약). Curator는 글로벌을 쓰지 않는다(격리 원칙) — ① adaptive.md만 직접 수정, ② 모든 승격 후보(글로벌 domain은 gd- 번들, 그 외 ck-/cr-/pat-/remember-)를 프로젝트 _curator-staging/에 초안 작성. 완주 판정은 응답 표면이 아닌 staging 파일 디스크 실측으로. 실패/미완주 시 메인 세션이 직접 대행 — 격리 구조상 안전. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)""",
))

# 2) 버전 푸터
EDITS.append((
    """**Version**: 18
**Last Updated**: 2026-07-23""",
    """**Version**: 19
**Last Updated**: 2026-08-19""",
))

# 3) Changes 갱신
EDITS.append((
    """**Changes**: Session End 2~3단계 멀티 세션 격리 (M41, 옵션 A): Curator 글로벌 직접 수정 폐지 → adaptive.md만 직접 수정 + 승격 후보 전체를 프로젝트 staging(gd- 번들 포함)에 초안, 승인분 글로벌 반영은 promote_knowledge.py(락 직렬화 + 무결성 검증). delegate BUSY 시 직접 대행 안전 명시. T1.5 §17 v21과 연동""",
    """**Changes**: Session End 2단계 Curator 전송 전환 (M42): delegate → use_subagent(동기). 근거: delegate 전역 상태(.subagents, agent 이름 키 + user_notified 선점 + status 폴링)가 session-agnostic이라 멀티 세션 crosstalk/replace 실측. 완주 판정은 staging 디스크 실측 (Kiro #6765 채널 절단 대비), 실패 시 직접 대행. T1.5 §17 v24 전송 규약과 연동""",
))


def apply(json_path: Path, report: list) -> bool:
    bak = json_path.with_suffix(json_path.suffix + ".bak-ai-developer-mickey-m42")
    if not bak.exists():
        shutil.copy2(json_path, bak)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    prompt = data["prompt"]
    for i, (old, new) in enumerate(EDITS, 1):
        n = prompt.count(old)
        if n != 1:
            report.append(f"[FAIL] {json_path.name} edit {i}: count={n} (기대 1)")
            return False
        prompt = prompt.replace(old, new)
    data["prompt"] = prompt
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    report.append(f"[OK] {json_path.name}: 3건 적용 (백업 {bak.name})")
    return True


def main() -> int:
    report, ok = [], True
    for target in (HOME_JSON, REPO_JSON):
        ok &= apply(target, report)
    if ok:
        p1 = json.loads(HOME_JSON.read_text(encoding="utf-8"))["prompt"]
        p2 = json.loads(REPO_JSON.read_text(encoding="utf-8"))["prompt"]
        checks = [
            (p1 == p2, "HOME == REPO prompt"),
            ("use_subagent(동기)로 호출" in p1, "신규 키워드: use_subagent 호출"),
            ("delegate 금지" in p1, "신규 키워드: delegate 금지"),
            ("**Version**: 19" in p1, "Version 19"),
            ("knowledge-curator agent에 delegate." not in p1, "구 문구 잔존 0 (delegate 호출)"),
            ("delegate가 BUSY" not in p1, "구 문구 잔존 0 (BUSY)"),
            ("**Version**: 18" not in p1, "구 버전 잔존 0"),
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
