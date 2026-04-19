# WELC Test Harness

## Core
수정 전 기존 동작을 테스트로 캡처(Characterization test)한 뒤 수정하여 사이드이펙트를 즉시 감지한다.

## Decision Context
packet-capture M9에서 리팩토링 중 기존 동작이 깨지는 문제 발생. "변경 전에 현재 동작을 먼저 테스트로 감싸라"는 WELC(Working Effectively with Legacy Code) 접근법을 채택. 사용자의 "검증 기반 진행" 성향과 "실수에서 배움" 성향이 결합된 결과.

## Tags
testing, safety, refactoring, verification, legacy-code

## Links
- phase-based-decomposition | applies-to | Phase별 수정 시 각 단계에서 WELC 적용
- tool-and-target-coevolution | extends | 테스트 도구 자체도 검증 대상과 함께 발전

## Content
- Characterization test: 현재 동작을 있는 그대로 캡처하는 테스트 (의도가 아닌 실제 동작 기록)
- 수정 후 Characterization test 실행 → 깨지면 사이드이펙트 발생 의미
- 추측으로 "괜찮을 것"이라고 넘어가지 않음 — 테스트 통과 + 실제 환경 검증 후에만 완료 선언
- Brownfield 프로젝트에서 특히 유효 (기존 코드의 동작을 모를 때)

## Source
packet-capture-log-agent (M9), REMEMBER #9
