# Script-to-Library Extraction

## Core
독립 스크립트의 핵심 로직을 함수로 추출하여 라이브러리화하고, 오케스트레이터에서 import하여 "설정 하나로 전체 파이프라인"을 실현한다.

## Decision Context
시뮬레이션 파이프라인 설계 시 Option A(별도 스크립트 호출) vs Option B(라이브러리화) 비교. Option B 채택 — 파일 수정 없이 런타임 주입으로 YAML 하나로 전체 파이프라인 제어 가능. 사용자의 "점진적 확장" 성향 반영: 기존 스크립트를 깨지 않고 run_* 함수만 추출.

## Tags
architecture, pipeline, library, orchestration, refactoring, reuse

## Links
- welc-test-harness | prerequisite | 추출 전 기존 동작을 하네스 테스트로 보호한 뒤 추출 수행
- phase-based-decomposition | applies-to | 스크립트별 순차 추출 → 각 단계 검증 후 진행

## Content
- 패턴: 기존 스크립트에서 `run_*` 함수 추출 → 오케스트레이터가 import하여 호출
- 장점: 기존 스크립트 단독 실행 유지 + 파이프라인 조합 가능 (양립)
- 핵심: 파일 수정 없이 런타임 주입으로 설정 기반 제어
- 적용 조건: 스크립트가 3개+ 이고 순차/병렬 조합이 필요할 때
- WELC와 결합: 추출 전 하네스 테스트 → 추출 후 회귀 확인 → 사이드이펙트 0 보장

## Source
skr-reverse-poc (Mickey 36-37), 2026-04-17~19
