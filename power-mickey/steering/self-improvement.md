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

### Step 4.5: 교훈 승격

사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면:
1. project-lessons.md + CURRENT.md Lessons + Memory Graph 리뷰
2. 분류:
   - 반복 패턴 → project-lessons.md 유지
   - 범용 원칙 → Global steering 후보
   - 근본 원칙 수준 → 작업 원칙(mickey-core.md) 후보
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

Global steering에 추가하시겠습니까?"
```

## Adaptive Rules (자가 개선)

Mickey가 작업 중 발견한 반복 패턴을 project-lessons.md에 규칙 형태로 자동 기록하는 메커니즘.

### 자가 기록 조건
아래 패턴 발견 시 사용자 확인 없이 project-lessons.md에 추가:
- 같은 실수/비효율이 2회 발생
- 사용자가 같은 지적을 반복
- 특정 작업에서 일관된 성공 패턴 발견

### 안전 장치
1. **작업 원칙 충돌 금지**: mickey-core.md의 작업 원칙과 충돌하는 규칙은 기록 불가
2. **세션 종료 리뷰**: Step 3에서 사용자에게 일괄 제시 → 삭제/수정 가능
3. **크기 제한**: project-lessons.md 10개 상한 준수

### 승격 경로
1. project-lessons.md에서 3+ 세션 유효 → Global steering 후보
2. 여러 프로젝트에서 유효 → Global steering 확정
3. 근본 원칙 수준 → 작업 원칙(mickey-core.md) 후보
- 모든 승격은 사용자 확인 필수

## Architectural Guard

반복적 아키텍처 위반을 감지하면 구조 테스트/린트 규칙 도입을 제안한다.

### 트리거
- 동일한 아키텍처 위반이 2회 이상 발생

### 행동
1. 위반 패턴을 project-lessons.md에 기록 (1회차)
2. 2회차 발생 시 사용자에게 구조 테스트 도입 제안
3. 승인 시 프로젝트에 맞는 검증 방식 구현 (lint rule, grep 기반 체크 등)

## 포스트모템

사용자가 "포스트모템" 또는 "프로토콜 리뷰"를 요청하면:
1. CURRENT.md, HANDOFF.md, Memory Graph에서 `[Protocol]` 태그 + Lessons 수집
2. 반복되는 긍정/부정 피드백 식별
3. 변경별 유효성 판정 (유효/무효/판단 보류) + 근거
4. 개선 필요 항목별 옵션 (수정/롤백/유지) + 추천
5. 사용자 승인 후 적용

## Graduated 작업 원칙

mickey-core.md 작업 원칙에서 은퇴한 항목. 내재화되었으나 포스트모템 시 재검토 대상.

| 항목 | 은퇴 근거 | 은퇴 시점 |
|------|----------|----------|
| (현재 없음) | — | — |

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
