"""Mickey 22 Step 5 — T1 시스템 프롬프트 5건 변경 일괄 적용

활성 agent JSON과 repo agent JSON 양쪽을 동시에 갱신한다.
- 5건의 search/replace 패턴 (A, B, C, D, E)
- 각 패턴은 정확히 1건 매칭되어야 함 (검증)
- 변경 전 prompt를 _m22_prompt_before.md, 변경 후를 _m22_prompt_after.md 에 dump
- 활성/repo 양쪽 동시 저장 + hash 일치 검증
"""
import hashlib
import json
import sys
from pathlib import Path

# Windows cp949 stdout 우회 — em dash 등 비-ASCII 출력 가능하도록 utf-8 재설정
sys.stdout.reconfigure(encoding='utf-8')

ACTIVE = Path.home() / '.kiro' / 'agents' / 'ai-developer-mickey.json'
REPO = Path(r'C:\Users\hcsung\work\kiro\ai-developer-mickey\examples\ai-developer-mickey.json')
DUMP_DIR = Path(r'C:\Users\hcsung\work\kiro\ai-developer-mickey\scripts')


# 5건의 변경 정의 — (id, old, new)
REPLACEMENTS = [
    # A. Continuing Session 1b 엔트로피 체크
    (
        'A',
        '1b. **엔트로피 체크**: INDEX 정합성, auto_notes 최신성, 오래된 SESSION 아카이빙 필요 여부, **포스트모템 트리거 조건** 확인 (T1.5 상세 규칙 참조)',
        '1b. **엔트로피 체크**: INDEX 정합성, auto_notes 최신성, 오래된 SESSION 아카이빙 필요 여부, `_curator-staging/` dangling 항목, **포스트모템 트리거 조건** 확인 (T1.5 §3 + §17 + §9 참조)',
    ),
    # B. Session End 단계 2~3
    (
        'B',
        '2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 delegate. Curator가 domain/ 저장 + adaptive.md 갱신을 직접 수행하고, common_knowledge/context_rule/patterns/REMEMBER 승격 제안을 반환\n3. **Curator 결과 제시**: 직접 수정분 알림 + 제안분을 사용자에게 확인 요청',
        '2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 delegate. 보정된 권한(fs_write 자동 승인 경로 한정)으로 마찰 최소화. Curator가 ① domain/ + adaptive.md + INDEX Domain Links 직접 수정, ② common_knowledge/context_rule/patterns/REMEMBER 후보를 staging 디렉토리에 Pre-staged 초안 작성. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)\n3. **Curator 결과 제시**: 직접 수정분 보고 + Pre-staged 항목 목록 제시. 사용자에게 단일 응답 요청: "전체" / 번호 ("1,3" 등) / "없음" / "보류". 응답에 따라 staging → 정식 위치 이동 또는 폐기',
    ),
    # C. 자동 메모리 표 adaptive.md 행
    (
        'C',
        '| context_rule/adaptive.md | 적응형 규칙 (자가 생성) | 세션 종료 시 일괄 확인 | T2 |',
        '| context_rule/adaptive.md | 적응형 규칙 (Curator 직접 수정) | 세션 종료 시 git diff 검증 (첫 5회) | T2 |',
    ),
    # D. 교훈 승격 단순화
    (
        'D',
        '### 교훈 승격\n\n사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면:\n1. auto_notes/, 현재 SESSION.md Lessons, 직전 HANDOFF.md 리뷰\n2. 반복 패턴 → context_rule/, 범용 패턴 → common_knowledge/, 근본 원칙 → REMEMBER 후보로 분류\n3. 항목별 승격 제안 (내용, 근거, 대상) → 사용자 확인\n4. 승인 시 반영 + auto_notes/에서 제거 또는 "승격 완료" 표시',
        '### 교훈 승격\n\n사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면 Knowledge Curator를 호출 (Session End와 동일 흐름). Curator가 R/G/S 분기 판단 + 직접 수정 + Pre-staged 초안 작성을 수행한다. 상세 절차는 T1.5 §17 참조.',
    ),
    # E. 푸터
    (
        'E',
        '**Version**: 15\n**Last Updated**: 2026-05-08\n**Changes**: Knowledge Curator 전체 지식 관리자로 확장 (세션 중 호출 제거 → 세션 종료 배치)',
        '**Version**: 16\n**Last Updated**: 2026-06-20\n**Changes**: Curator delegate 시 Pre-staged Apply 흐름 + 단일 응답 명시 (Session End 2~3), Continuing Session 엔트로피 체크에 staging dangling 추가, 교훈 승격 Curator 자동 분류로 단순화 (T1.5 §17 + §18 신설과 연동)',
    ),
]


def apply_replacements(prompt: str) -> str:
    """5건의 변경을 순차 적용. 각 패턴은 정확히 1건 매칭되어야 함."""
    result = prompt
    for rid, old, new in REPLACEMENTS:
        count = result.count(old)
        if count != 1:
            raise RuntimeError(f'[{rid}] expected exactly 1 match, found {count}')
        result = result.replace(old, new, 1)
        print(f'[{rid}] OK — replaced 1 occurrence')
    return result


def main():
    # 1. 활성 JSON 로드 (활성/repo 동일 가정 — verify 스크립트로 이미 확인)
    active_obj = json.loads(ACTIVE.read_text(encoding='utf-8'))
    repo_obj = json.loads(REPO.read_text(encoding='utf-8'))

    # 사전 일치 검증 (방어)
    if active_obj['prompt'] != repo_obj['prompt']:
        raise RuntimeError('Active and repo prompts differ before edit — abort')

    before_prompt = active_obj['prompt']
    (DUMP_DIR / '_m22_prompt_before.md').write_text(before_prompt, encoding='utf-8')

    # 2. 변경 적용
    after_prompt = apply_replacements(before_prompt)
    (DUMP_DIR / '_m22_prompt_after.md').write_text(after_prompt, encoding='utf-8')

    # 3. 양쪽 dict에 prompt 적용
    active_obj['prompt'] = after_prompt
    repo_obj['prompt'] = after_prompt

    # 4. 양쪽 저장 (indent=2, ensure_ascii=False)
    active_text = json.dumps(active_obj, indent=2, ensure_ascii=False) + '\n'
    repo_text = json.dumps(repo_obj, indent=2, ensure_ascii=False) + '\n'

    ACTIVE.write_text(active_text, encoding='utf-8')
    REPO.write_text(repo_text, encoding='utf-8')

    # 5. hash 일치 검증
    a_hash = hashlib.sha256(ACTIVE.read_bytes()).hexdigest()
    r_hash = hashlib.sha256(REPO.read_bytes()).hexdigest()

    print()
    print(f'Active sha256: {a_hash}')
    print(f'Repo sha256:   {r_hash}')
    print('OK: hash match' if a_hash == r_hash else 'FAIL: hash mismatch')

    # 6. 변경 통계
    before_lines = before_prompt.count('\n') + 1
    after_lines = after_prompt.count('\n') + 1
    print(f'\nPrompt: {before_lines} lines → {after_lines} lines')
    print(f'Prompt: {len(before_prompt)} chars → {len(after_prompt)} chars')


if __name__ == '__main__':
    main()
