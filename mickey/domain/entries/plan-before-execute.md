# 계획 문서 선행

## Core
상세 계획 문서(IMPROVEMENT-PLAN)를 먼저 작성하고, 구현 세션에서는 판단 비용을 제거한 채 실행에 집중한다.

## Decision Context
ai-developer-mickey M4→M5에서 v6.3 구현 시, M4에서 IMPROVEMENT-PLAN을 상세히 작성한 덕분에 M5에서 판단 없이 빠르게 구현 완료. "계획의 구체성이 실행 속도를 결정한다"는 교훈. 단, 작고 명확한 작업(gamejob_crawler 2세션 완료)에서는 계획 없이 즉시 실행이 더 효율적 — 영향 범위와 되돌리기 난이도로 판단.

## Tags
planning, execution, efficiency, decision-cost

## Links
- phase-based-decomposition | prerequisite | Phase 분해 자체가 계획 문서에서 수행됨
- external-benchmarking | extends | 벤치마킹 결과가 계획 문서의 입력이 됨

## Content
- 큰 변경: IMPROVEMENT-PLAN 수준의 구체적 계획 → 다음 세션에서 구현
- 작은/명확한 작업: 빠른 실행 우선
- 계획 문서에 포함할 것: Phase 분해, 각 Phase의 완료 기준, 열린 질문, 리스크
- 계획 없이 큰 변경을 시작하면 세션 중간에 방향 전환이 발생하여 context window 낭비

## Source
ai-developer-mickey (M4→M5, M7→M8, M14→M15)
