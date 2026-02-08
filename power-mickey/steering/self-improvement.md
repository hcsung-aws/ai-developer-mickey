# 자기 개선 프로토콜

## 세션 종료 시 ("세션 정리" 요청)

### Step 1: 세션 로그 완료
- `.kiro/sessions/CURRENT.md` 업데이트
- 완료 작업, 수정 파일, 다음 단계 기록

### Step 2: 핸드오프 문서 생성
- `.kiro/sessions/HANDOFF.md` 생성/업데이트

### Step 3: 교훈 분석 및 이중 저장

세션 중 발견한 교훈을 두 곳에 저장:

**A. project-lessons.md** (사람이 읽을 수 있는 형태)
```markdown
## [YYYY-MM-DD] - [주제]
**문제**: [발생한 문제]
**원인**: [근본 원인]
**해결**: [해결 방법]
**교훈**: [앞으로 적용할 점]
```

**B. Memory Graph** (AI 검색 최적화)
```json
{
  "tool": "store_memory",
  "content": "[교훈 내용]",
  "memory_type": "solution",
  "tags": ["lesson", "project-name", "topic"]
}
```

### Step 4: REMEMBER 승격 프로세스

범용 원칙 발견 시 사용자에게 제안:
1. **프로젝트 교훈** → `.kiro/steering/project-lessons.md`에 직접 추가
2. **범용 원칙** → Global steering (mickey-core.md 또는 해당 steering) 수정 제안

```
"세션 정리 완료:
✅ 세션 로그 / 핸드오프
✅ 프로젝트 교훈 추가: [N]개

## 범용 원칙 제안 (Global steering 추가 권장)
1. [원칙]: [설명] → [대상 steering 파일]

Global steering에 추가하시겠습니까?"
```

## 교훈 발견 기준

- 같은 실수를 2번 이상 반복
- 사용자가 빠트린 부분 지적
- 예상과 다른 결과
- 새로운 패턴/안티패턴 발견
- 효과적인 해결책 발견

## 분산 REMEMBER (맥락별 원칙)

mickey-core.md의 핵심 5개 외, 이 steering 로딩 시 적용:
- **전제조건 우선 검증**: 구현 전 핵심 자원/조건 확보 확인
- **문서 작성 시 핵심 메시지 먼저**: 사용자 여정 기반 구조화
- **점진적 도입**: 최소 기능 시작 + 피드백 기반 확장만
- **작업 단위별 테스트 필수**: 구현 후 실제 환경에서 검증, 추측으로 넘어가지 말 것
- **테스트 기반 완료 처리**: 테스트 작성/통과/문서화 후에만 완료 선언
