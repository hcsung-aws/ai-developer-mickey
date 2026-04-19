# 검증 대상과 도구 동시 발전

## Core
테스트 대상과 테스트 도구를 함께 개선하여, 대상이 복잡해질수록 도구도 더 정교한 검증이 가능해지게 한다.

## Decision Context
packet-capture 프로젝트에서 mmorpg_simulator(검증 대상)에 채팅/인벤토리/상점/NPC를 추가하면서 동시에 packet-capture-agent(도구)의 파싱/시나리오 조립 기능도 확장. 한쪽만 발전시키면 검증 범위가 제한된다는 판단. 사용자의 "점진적 확장" 성향이 도구와 대상 양쪽에 동시 적용된 사례.

## Tags
testing, coevolution, tooling, verification, incremental

## Links
- phase-based-decomposition | similar-to | 둘 다 점진적 발전이지만 분해 vs 동시 발전의 차이
- welc-test-harness | extends | WELC는 이 패턴의 검증 측면을 구체화

## Content
- 대상에 새 기능 추가 → 도구에 해당 기능 검증 능력 추가 → 더 복잡한 시나리오 테스트 가능
- 도구만 발전시키면 검증할 대상이 단순해서 의미 없음
- 대상만 발전시키면 검증 없이 진행하게 되어 품질 저하
- 이 패턴은 "검증 기반 진행" 성향의 자연스러운 확장

## Source
packet-capture-log-agent (M6~M14)
