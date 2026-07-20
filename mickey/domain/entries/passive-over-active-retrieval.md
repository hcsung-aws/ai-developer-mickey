# Passive > Active 지식 활용

> **[Seed 예시]** 이 파일은 교육·데모용 seed 예시이다 (IMPROVEMENT-PLAN-v10 §8-a).
> 실제 지식 그래프는 각 사용자 홈 `~/.kiro/mickey/domain/`에서 Knowledge Curator가 축적하며,
> 이 예시는 새 사용자가 entry 형식(Core/Decision Context/Tags/Links/Content/Evidence)을 파악하는 참고용이다.

## Core
에이전트/사용자의 지식 활용은 Active 검색(의식적으로 찾아보기)이 아닌 Passive 발견(context window에 자연스럽게 노출)으로 설계해야 동작한다.

## Decision Context
Domain 지식을 저장했지만 실제 활용 0회. Active 검색을 기대했으나 실행되지 않음. Domain Backlink 메커니즘으로 전환 — 프로젝트 INDEX 파일에 역방향 링크를 삽입하여, 프로젝트 파일을 읽을 때 자연스럽게 domain 지식을 발견하도록 설계.

## Tags
agent-design, knowledge-management, retrieval, passive-discovery, context-window

## Links
- forced-breakpoint-execution | extends | 강제 중단점에서 passive 노출용 링크를 삽입하는 것이 구현 방식
- plan-before-execute | similar-to | 계획 문서도 실행 시 판단을 줄이는 passive 구조

## Content
### 문제
"필요할 때 검색하라"는 지시는 동작하지 않음. 검색 자체가 추가 판단+행동을 요구하기 때문.

### 해결 원칙
1. **Passive 노출 경로 설계**: 이미 읽는 파일(INDEX, 계획 문서)에 힌트/링크 삽입
2. **Active 검색 의존 제거**: "필요하면 찾아보라"는 설계를 신뢰하지 않음
3. **Backlink 패턴**: 지식 저장 시 관련 프로젝트 파일에 역방향 링크 자동 삽입

### 적용 사례
- Domain Backlink: domain entry 저장 → 프로젝트 INDEX에 링크 (Mickey 16)
- GRAPH.md Core 강화: 노드에 "언제 쓰는가" 힌트 추가 → 읽을 때 자연스럽게 리마인드
- common_knowledge 교차 참조: agent-design-patterns.md 본문에 domain entry 경로를 직접 삽입 → 패턴 읽을 때 상세 지식 자연 노출 (Mickey 19)
- machine-env.md 절차 상세화: "설치됨" 수준이 아닌 구체 실행 절차까지 기록 → 매 세션 되묻는 Active 질의 제거 (Mickey 19)

### 설계 함의
- 지식 저장소의 가치는 저장이 아니라 발견 경로에 있음
- 저장 시점에 발견 경로까지 함께 설계해야 함

## Source
ai-developer-mickey, Mickey 16, 2026-05-08
ai-developer-mickey, Mickey 19, 2026-05-14 (적용 사례 보강)
