# 지식 성격별 활용 경로 분기

> **[Seed 예시]** 이 파일은 교육·데모용 seed 예시이다 (IMPROVEMENT-PLAN-v10 §8-a).
> 실제 지식 그래프는 각 사용자 홈 `~/.kiro/mickey/domain/`에서 Knowledge Curator가 축적하며,
> 이 예시는 새 사용자가 entry 형식(Core/Decision Context/Tags/Links/Content/Evidence)을 파악하는 참고용이다.

## Core
지식을 단일 저장소로 묶지 않고, 성격(R=방식/판단, G=사실/구조, S=절차/동작)에 따라 활용 경로를 분리 설계한다.

## Decision Context
v8.1에서 모든 지식을 "저장소"로 묶어 동일 Skill/Curator로 처리한 것이 실패의 본질. R(헌법)은 항상 로딩되는 REMEMBER, G(연관 사실)는 그래프 passive 경로, S(절차)는 Skill 호출이 각각의 본체. 하나의 메커니즘으로 모든 성격을 커버하려는 시도가 0% 활용을 초래.

## Tags
knowledge-management, agent-design, routing, classification, retrieval

## Links
- passive-over-active-retrieval | extends | G(사실)의 활용 경로가 passive 발견
- forced-breakpoint-execution | applies-to | S(절차)의 실행 시점이 강제 중단점

## Content
- R (방식/판단): 항상 컨텍스트에 존재해야 함. REMEMBER, 시스템 프롬프트 수준. 변경 빈도 낮음, 위반 시 실패
- G (사실/구조): 필요할 때 발견되어야 함. 그래프, backlink, INDEX 트리거. 변경 빈도 중간, 누락 시 비효율
- S (절차/동작): 호출 시 실행되어야 함. Skill, 스크립트, 자동화. 변경 빈도 높음, 미실행 시 무의미
- 실패 패턴: 하나의 메커니즘(예: Curator subagent)으로 R+G+S 모두 처리 시도 → 어느 것도 제대로 작동 안 함
- 설계 원칙: 각 성격에 맞는 활용 경로를 별도 설계하고, 교차점만 연결

## Source
ai-developer-mickey (M20, 2026-05-14)
