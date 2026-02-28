# 자기 개선 프로토콜

## 세션 종료 시 ("세션 정리" 요청)

### Step 1: 세션 로그 완료
- `.kiro/sessions/CURRENT.md` 업데이트 (작업 단위 트리거로 이미 최신이므로 최소 작업)
- 완료 작업, 수정 파일, 다음 단계 기록

### Step 2: 핸드오프 문서 생성
- `.kiro/sessions/HANDOFF.md` 생성/업데이트

### Step 2.5: 목적 정합성 리뷰
- PURPOSE-SCENARIO.md와 이번 세션 작업 결과를 대조
- 목적/시나리오와 실제 구현 방향이 일치하는지 확인
- 불일치 발견 시 사용자에게 보고하고 PURPOSE-SCENARIO.md 조정 여부 확인

### Step 3: 교훈 분석 및 분류

세션 중 발견한 교훈을 두 가지로 분류:

**A. 프로젝트 교훈** (이 프로젝트에만 적용)
- 프로젝트 특정 패턴, 규칙, 주의사항
- → `.kiro/steering/project-lessons.md`에 추가

**B. 범용 원칙** (모든 프로젝트에 적용)
- 일반적인 개발 원칙, 베스트 프랙티스
- → 사용자에게 제안 (Global steering 수정 권장)

### Step 4: 프로젝트 교훈 저장

`.kiro/steering/project-lessons.md` 파일을 직접 수정:

```markdown
## [YYYY-MM-DD] - [주제]
**문제**: [발생한 문제]
**원인**: [근본 원인]
**해결**: [해결 방법]
**교훈**: [앞으로 적용할 점]
```

> **항목 수 제한**: project-lessons.md는 최대 10개 항목 유지. 초과 시 오래된 항목은 Memory Graph에만 보존하고 파일에서 제거.

### Step 4.5: 교훈 승격 (세션 중에도 가능)

사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면:
1. project-lessons.md + CURRENT.md Lessons + Memory Graph 리뷰
2. 반복 패턴 → project-lessons.md, 범용 원칙 → Global steering 후보로 분류
3. 항목별 승격 제안 (내용, 근거, 대상) → 사용자 확인
4. 승인 시 반영 + 원본에서 "승격 완료" 표시

### Step 5: Memory Graph 저장 (사용 중인 경우)
중요한 교훈은 Memory Graph에도 저장:
```json
{
  "tool": "store_memory",
  "content": "[교훈 내용]",
  "memory_type": "solution",
  "tags": ["lesson", "project-name", "topic"]
}
```

### Step 6: 사용자에게 보고

```
"세션 정리 완료:

✅ 세션 로그: .kiro/sessions/CURRENT.md
✅ 핸드오프: .kiro/sessions/HANDOFF.md
✅ 프로젝트 교훈 추가: [N]개

## 범용 원칙 제안 (Global steering 추가 권장)
1. [원칙 1]: [설명]
2. [원칙 2]: [설명]

Global steering에 추가하시겠습니까?"
```

## 교훈 발견 기준

다음 상황에서 교훈 추출:
- 같은 실수를 2번 이상 반복
- 사용자가 빠트린 부분 지적
- 예상과 다른 결과
- 새로운 패턴/안티패턴 발견
- 효과적인 해결책 발견

## 프로젝트 교훈 형식

```markdown
## [YYYY-MM-DD] - [주제]
**Mickey Session**: [세션 날짜]
**문제**: [발생한 문제]
**원인**: [근본 원인]
**해결**: [해결 방법]
**교훈**: [앞으로 적용할 점]
**관련 파일**: [파일 목록]
```
