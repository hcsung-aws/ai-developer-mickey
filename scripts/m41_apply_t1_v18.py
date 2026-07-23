# -*- coding: utf-8 -*-
"""M41: T1 시스템 프롬프트 v17→v18 — Session End를 격리 구조(옵션 A)로 개정.

대상 (m32 선례 실측: 독립 md 부재, JSON 2곳):
1. ~/.kiro/agents/ai-developer-mickey.json (활성 런타임)
2. {repo}/examples/ai-developer-mickey.json (install 배포원)

변경 3건 (prompt 필드 내부 문자열, safe-batch-replace count-1 guard):
1. Session End 2~3단계: Curator 글로벌 직접 수정 → 프로젝트 staging + promote 스크립트
2. 교훈 승격 문구: 직접 수정 표현 정리
3. Version 17 → 18 + Changes 갱신

백업: .bak-ai-developer-mickey-m41. JSON escape 함정 회피 위해 json.load/dump 사용.
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME_JSON = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"
REPO_JSON = Path(__file__).resolve().parent.parent / "examples" / "ai-developer-mickey.json"
OUT = Path(__file__).resolve().parent / "output" / "m41_t1_v18.txt"

EDITS = []

# 1) Session End 2~3단계 — 격리 구조 반영
EDITS.append((
    """2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 delegate. 보정된 권한(fs_write 자동 승인 경로 한정)으로 마찰 최소화. Curator가 ① domain/ + adaptive.md + INDEX Domain Links 직접 수정, ② common_knowledge/context_rule/patterns/REMEMBER 후보를 staging 디렉토리에 Pre-staged 초안 작성. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)
3. **Curator 결과 제시**: 직접 수정분 보고 + Pre-staged 항목 목록 제시. 사용자에게 단일 응답 요청: "전체" / 번호 ("1,3" 등) / "없음" / "보류". 응답에 따라 staging → 정식 위치 이동 또는 폐기""",
    """2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 delegate. Curator는 글로벌을 쓰지 않는다(격리 원칙) — ① adaptive.md만 직접 수정, ② 모든 승격 후보(글로벌 domain은 gd- 번들, 그 외 ck-/cr-/pat-/remember-)를 프로젝트 _curator-staging/에 초안 작성. delegate가 BUSY(타 세션 실행 중)면 메인 세션이 직접 대행 — 격리 구조상 안전. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)
3. **Curator 결과 제시 + 승격**: 직접 수정분 보고 + staging 항목 목록 제시. 사용자에게 단일 응답 요청: "전체" / 번호 ("1,3" 등) / "없음" / "보류". 승인된 gd- 번들은 promote_knowledge.py로 글로벌 승격 (락 직렬화 + 무결성 검증 + 리포트 — T1.5 §17 락 규약), 그 외 승인분은 staging → 정식 위치 이동, 미승인분 폐기""",
))

# 2) 교훈 승격 문구
EDITS.append((
    """사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면 Knowledge Curator를 호출 (Session End와 동일 흐름). Curator가 R/G/S 분기 판단 + 직접 수정 + Pre-staged 초안 작성을 수행한다. 상세 절차는 T1.5 §17 참조.""",
    """사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면 Knowledge Curator를 호출 (Session End와 동일 흐름). Curator가 R/G/S 분기 판단 + adaptive.md 직접 수정 + 승격 번들/초안 작성(프로젝트 staging)을 수행하고, 글로벌 반영은 promote 스크립트가 담당한다. 상세 절차는 T1.5 §17 참조.""",
))

# 3) 버전 푸터
EDITS.append((
    """**Version**: 17
**Last Updated**: 2026-07-01""",
    """**Version**: 18
**Last Updated**: 2026-07-23""",
))
EDITS.append((
    """**Changes**: SESSION PROTOCOL 4a (코드 분석 도구 감지) 신설, Continuing Session 엔트로피 체크에 §19 항목 추가, FILE-STRUCTURE.md 스키마 필수/선택 분리 (Tier 감지에 따라 상세 도구 위임 vs Mickey 지도 유지). T1.5 §19 External Code Analysis Integration 신설과 연동 (Tier 1 Serena/Graphify default + Tier 2 사용자 확인 + Tier 3 내장 code baseline)""",
    """**Changes**: Session End 2~3단계 멀티 세션 격리 (M41, 옵션 A): Curator 글로벌 직접 수정 폐지 → adaptive.md만 직접 수정 + 승격 후보 전체를 프로젝트 staging(gd- 번들 포함)에 초안, 승인분 글로벌 반영은 promote_knowledge.py(락 직렬화 + 무결성 검증). delegate BUSY 시 직접 대행 안전 명시. T1.5 §17 v21과 연동""",
))


def apply(json_path: Path, report: list) -> bool:
    bak = json_path.with_suffix(json_path.suffix + ".bak-ai-developer-mickey-m41")
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
        # 검증: 두 prompt 동일 + 신규 키워드 존재 + 구 문구 잔존 0
        p1 = json.loads(HOME_JSON.read_text(encoding="utf-8"))["prompt"]
        p2 = json.loads(REPO_JSON.read_text(encoding="utf-8"))["prompt"]
        checks = [
            (p1 == p2, "HOME == REPO prompt"),
            ("promote_knowledge.py" in p1, "신규 키워드: promote_knowledge.py"),
            ("격리 원칙" in p1, "신규 키워드: 격리 원칙"),
            ("**Version**: 18" in p1, "Version 18"),
            ("domain/ + adaptive.md + INDEX Domain Links 직접 수정" not in p1, "구 문구 잔존 0 (직접 수정)"),
            ("**Version**: 17" not in p1, "구 버전 잔존 0"),
        ]
        for cond, label in checks:
            report.append(f"[{'PASS' if cond else 'FAIL'}] {label}")
            ok &= cond
    report.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    OUT.write_text("\n".join(report), encoding="utf-8")
    print(f"written: {OUT} ({'ALL PASS' if ok else 'FAIL'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
