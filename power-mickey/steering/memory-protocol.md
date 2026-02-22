# Memory Graph 프로토콜

Memory Graph MCP를 사용한 장기 기억 관리입니다.
사용 여부는 프로젝트/상황에 따라 선택적으로 결정합니다.

## 언제 사용하나?
- 장기 프로젝트에서 의사결정 추적이 필요할 때
- 복잡한 문제 해결 과정을 기록할 때
- 프로젝트 간 지식 공유가 필요할 때

## 세션 시작 시 (지식 지도 패턴)

Context window 절약을 위해 2단계로 조회한다:

**1단계 — 지식 지도 로딩 (세션 시작)**
```
search_memories로 기억 제목/태그 목록만 조회
→ "어떤 지식이 있는지" 파악 (상세 내용은 읽지 않음)
⚠️ recall_memories는 project_path 필터링 버그가 있어 항상 0건을 반환한다.
   project_path 필터가 필요한 경우 반드시 search_memories를 사용하라.
```

**2단계 — 상세 조회 (작업 중 on-demand)**
```
작업 중 관련 기억이 필요하면 해당 기억의 상세 내용을 조회
→ 필요한 것만, 필요할 때 로딩
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
  "tool": "search_memories",
  "project_path": "<workspace 절대 경로>",
  "tags": ["redis", "timeout"]
}
```

> **참고**: `recall_memories`는 `project_path` 필터링 버그가 있으므로, project 범위 조회 시 `search_memories`를 사용한다. `recall_memories`는 project_path 필터 없이 자연어 검색할 때만 사용한다.

### 관계 생성
```json
{
  "tool": "create_relationship",
  "from_memory_id": "solution_123",
  "to_memory_id": "problem_456",
  "relationship_type": "SOLVES"
}
```
