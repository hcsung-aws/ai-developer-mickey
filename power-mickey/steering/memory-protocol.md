# Memory Graph 프로토콜

Memory Graph MCP를 사용한 장기 기억 관리입니다.
사용 여부는 프로젝트/상황에 따라 선택적으로 결정합니다.

## 언제 사용하나?
- 장기 프로젝트에서 의사결정 추적이 필요할 때
- 복잡한 문제 해결 과정을 기록할 때
- 프로젝트 간 지식 공유가 필요할 때

## 세션 시작 시
```
recall_memories 도구로 프로젝트 관련 기억 조회
- 프로젝트명, 기술 스택, 최근 작업 키워드로 검색
```

## 자동 저장 트리거

| 상황 | Memory 타입 | 관계 |
|------|-------------|------|
| 버그 수정 | problem + solution | SOLVES |
| 아키텍처 결정 | decision | - |
| 패턴 발견 | code_pattern | APPLIES_TO |
| 에러 해결 | error + fix | ADDRESSES |

## Memory 타입
- **solution**: 작동하는 해결책
- **problem**: 발생한 문제
- **code_pattern**: 재사용 가능한 패턴
- **decision**: 아키텍처/기술 결정
- **error**: 특정 에러
- **fix**: 에러 해결책

## 관계 타입
- **SOLVES**: 해결책 → 문제
- **CAUSES**: 원인 → 결과
- **BUILDS_ON**: 새 접근 → 이전 접근
- **APPLIES_TO**: 패턴 → 프로젝트
- **SUPERSEDED_BY**: 이전 방식 → 새 방식

## 사용 예시

### 기억 저장
```json
{
  "tool": "store_memory",
  "content": "Redis 타임아웃은 connection pool을 50으로 늘려서 해결",
  "memory_type": "solution",
  "tags": ["redis", "timeout", "connection-pool"]
}
```

### 기억 조회
```json
{
  "tool": "recall_memories",
  "query": "redis timeout"
}
```

### 관계 생성
```json
{
  "tool": "create_relationship",
  "from_memory_id": "solution_123",
  "to_memory_id": "problem_456",
  "relationship_type": "SOLVES"
}
```
