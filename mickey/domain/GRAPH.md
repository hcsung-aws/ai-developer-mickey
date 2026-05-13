# Knowledge Graph

## Nodes
| ID | Title | Tags | Core |
|----|-------|------|------|
| phase-based-decomposition | Phase 기반 점진적 분해 | planning, incremental, verification, decomposition | 큰 목표/복잡한 작업 시 → Phase→Step 분해, 각 단계 E2E 검증 후 진행 |
| welc-test-harness | WELC Test Harness | testing, safety, refactoring, verification, legacy-code | 기존 코드 수정/리팩토링 시 → 수정 전 동작을 테스트로 캡처하여 회귀 방지 |
| plan-before-execute | 계획 문서 선행 | planning, execution, efficiency, decision-cost | 영향 범위 넓은 변경 시 → 상세 계획 문서 먼저 작성, 구현 시 판단 제거 |
| external-benchmarking | 외부 벤치마킹 → 선별 채택 | benchmarking, adoption, external-analysis, selective | 외부 기술/도구 도입 시 → 자기 맥락에서 재해석하여 선별 채택 |
| tool-and-target-coevolution | 검증 대상과 도구 동시 발전 | testing, coevolution, tooling, verification, incremental | 테스트/도구 개선 시 → 대상과 도구를 함께 발전시켜 검증 범위 확장 |
| script-to-library-extraction | Script→Library 추출 | architecture, pipeline, library, orchestration, refactoring, reuse | 스크립트 3개+ 조합 필요 시 → 핵심 로직을 함수 추출, 오케스트레이터에서 조합 |
| passive-over-active-retrieval | Passive > Active 지식 활용 | agent-design, knowledge-management, retrieval, passive-discovery | 지식 활용 설계 시 → Active 검색 의존 제거, Passive 발견 경로(backlink, 힌트) 설계 |
| forced-breakpoint-execution | 강제 중단점 실행 패턴 | agent-design, automation, execution-timing, breakpoint | 자동화 작업 실행 안 될 때 → 판단 제거, 자연스러운 중단점에 배치 |

## Edges
| From | To | Type | Reason |
|------|----|------|--------|
| phase-based-decomposition | welc-test-harness | applies-to | Phase별 수정 시 각 단계에서 WELC로 기존 동작 보호 |
| phase-based-decomposition | plan-before-execute | prerequisite | Phase 분해 자체가 계획 문서에서 수행됨 |
| phase-based-decomposition | tool-and-target-coevolution | similar-to | 둘 다 점진적 발전이지만 분해 vs 동시 발전의 차이 |
| welc-test-harness | tool-and-target-coevolution | extends | 테스트 도구 자체도 검증 대상과 함께 발전 |
| external-benchmarking | plan-before-execute | extends | 벤치마킹 결과가 계획 문서의 입력이 됨 |
| script-to-library-extraction | welc-test-harness | prerequisite | 추출 전 기존 동작을 하네스 테스트로 보호 |
| script-to-library-extraction | phase-based-decomposition | applies-to | 스크립트별 순차 추출 → 각 단계 검증 후 진행 |
| forced-breakpoint-execution | passive-over-active-retrieval | prerequisite | 강제 중단점에서 passive 노출용 링크를 삽입하는 것이 구현 방식 |
| passive-over-active-retrieval | plan-before-execute | similar-to | 계획 문서도 실행 시 판단을 줄이는 passive 구조 |
| forced-breakpoint-execution | plan-before-execute | similar-to | 둘 다 실행 전 구조화이지만 시점 선택 vs 내용 구조화 |

## Last Updated
2026-05-08 (Mickey 16)
