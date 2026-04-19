# Knowledge Graph

## Nodes
| ID | Title | Tags | Core |
|----|-------|------|------|
| phase-based-decomposition | Phase 기반 점진적 분해 | planning, incremental, verification, decomposition | 큰 목표를 Phase→Step으로 분해, 각 단계 E2E 검증 후 진행 |
| welc-test-harness | WELC Test Harness | testing, safety, refactoring, verification, legacy-code | 수정 전 기존 동작을 테스트로 캡처한 뒤 수정하여 사이드이펙트 즉시 감지 |
| plan-before-execute | 계획 문서 선행 | planning, execution, efficiency, decision-cost | 상세 계획 문서를 먼저 작성하고 구현 세션에서는 실행에 집중 |
| external-benchmarking | 외부 벤치마킹 → 선별 채택 | benchmarking, adoption, external-analysis, selective | 외부 기술을 자기 맥락에서 재해석하여 선별 채택 |
| tool-and-target-coevolution | 검증 대상과 도구 동시 발전 | testing, coevolution, tooling, verification, incremental | 테스트 대상과 도구를 함께 개선하여 검증 범위 확장 |

## Edges
| From | To | Type | Reason |
|------|----|------|--------|
| phase-based-decomposition | welc-test-harness | applies-to | Phase별 수정 시 각 단계에서 WELC로 기존 동작 보호 |
| phase-based-decomposition | plan-before-execute | prerequisite | Phase 분해 자체가 계획 문서에서 수행됨 |
| phase-based-decomposition | tool-and-target-coevolution | similar-to | 둘 다 점진적 발전이지만 분해 vs 동시 발전의 차이 |
| welc-test-harness | tool-and-target-coevolution | extends | 테스트 도구 자체도 검증 대상과 함께 발전 |
| external-benchmarking | plan-before-execute | extends | 벤치마킹 결과가 계획 문서의 입력이 됨 |

## Last Updated
2026-04-19 (Mickey 15)
