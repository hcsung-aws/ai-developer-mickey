# Phase 기반 점진적 분해

## Core
큰 목표를 Phase→Step으로 분해하고, 각 단계를 E2E 검증한 뒤 다음으로 진행한다.

## Decision Context
packet-capture 프로젝트에서 4단계 로드맵(구조 분석→캡처+파싱→시나리오 조립→부하 테스트)을 설계할 때, 한꺼번에 구현하면 실패 지점을 특정할 수 없다는 판단으로 채택. "작게 시작해서 점진적으로 확장"하는 사용자 성향이 직접 반영된 패턴.

## Tags
planning, incremental, verification, decomposition

## Links
- welc-test-harness | applies-to | Phase별 수정 시 각 단계에서 WELC로 기존 동작 보호
- plan-before-execute | prerequisite | Phase 분해 자체가 계획 문서에서 수행됨
- tool-and-target-coevolution | similar-to | 둘 다 점진적 발전을 추구하지만 분해 vs 동시 발전의 차이

## Content
- Phase 1→2→3→... 순서로 진행, 각 Phase 완료 후 E2E 검증
- Phase 내부도 Step으로 세분화 가능 (예: Phase 4를 Step 1 동기→Step 2 async→Step 3 멀티에이전트)
- 검증 실패 시 다음 Phase 진행 금지 (Backpressure 원칙과 결합)
- 작은 프로젝트에서는 Phase 없이 빠른 실행도 가능 — 영향 범위와 되돌리기 난이도로 판단

## Source
packet-capture-log-agent (M1~M14), ai-agent-automation-platform (M1~M32)
