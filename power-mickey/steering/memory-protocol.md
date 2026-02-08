# Memory Graph 프로토콜

Memory Graph MCP를 사용한 장기 기억 관리입니다.
사용 여부는 프로젝트/상황에 따라 선택적으로 결정합니다.

## 3-Tier에서의 역할 (T2)

Memory Graph는 세션 시작 시 T2 역할을 담당:
- `recall_memories`로 프로젝트 컨텍스트 자동 조회
- 파일 읽기 없이 의미 기반 검색으로 필요한 정보 확보
- PROJECT-OVERVIEW, ENVIRONMENT, DECISIONS 등의 정보를 저장/조회

## 지식 저장소 구분

**common_knowledge/** (project-lessons.md): 프로젝트 특화 교훈
- 반복 실패 방지, 환경 설정, 트러블슈팅, 알려진 이슈
- 사람이 읽을 수 있는 형태로 유지

**Memory Graph**: 구조화된 지식
- 태그, 관계 포함 저장 (AI 검색 최적화)
- 프로젝트 간 지식 공유 가능
- 의사결정 추적 (BUILDS_ON, SUPERSEDED_BY 관계)

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
