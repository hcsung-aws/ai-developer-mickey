# 강제 중단점 실행 패턴

> **[Seed 예시]** 이 파일은 교육·데모용 seed 예시이다 (IMPROVEMENT-PLAN-v10 §8-a).
> 실제 지식 그래프는 각 사용자 홈 `~/.kiro/mickey/domain/`에서 Knowledge Curator가 축적하며,
> 이 예시는 새 사용자가 entry 형식(Core/Decision Context/Tags/Links/Content/Evidence)을 파악하는 참고용이다.

## Core
판단+다단계 실행이 필요한 자동화 작업은 '세션 중 자동 호출'이 아닌 자연스러운 중단점(세션 종료, 커밋 등)에 배치해야 실제로 동작한다.

## Decision Context
TMI-agent와 Knowledge Curator 모두 '세션 중 자동 호출' 설계에서 실패. 6개 프로젝트에서 호출 0회. 근본 원인은 판단 병목(judgment bottleneck) + 실행 마찰. 점진적 검증 성향에 따라 실패 증거 기반으로 설계 전환.

## Tags
agent-design, automation, execution-timing, breakpoint, protocol

## Links
- passive-over-active-retrieval | prerequisite | 강제 중단점은 passive 활용 원칙의 실행 시점 구현
- plan-before-execute | similar-to | 둘 다 '실행 전 구조화'이지만, 이것은 '실행 시점 선택'에 초점

## Content
### 문제
프롬프트에 "X 상황에서 Y를 호출하라"고 적어도, 판단(언제?)과 다단계 실행(어떻게?)이 동시에 필요하면 실행되지 않음.

### 해결 원칙
1. **자연스러운 중단점 식별**: 세션 종료, 커밋, PR 생성 등 이미 흐름이 끊기는 지점
2. **배치 처리**: 중단점에서 축적된 맥락을 한 번에 처리
3. **판단 제거**: 중단점 도달 = 무조건 실행. "해야 하나?" 판단을 제거

### 적용 사례
- Knowledge Curator: 세션 중 호출 → 세션 종료 배치 (Mickey 16)
- TMI-agent: 동일 실패 패턴 확인

### 안티패턴
- "적절한 시점에 자동으로 호출" — 적절한 시점의 판단 자체가 병목
- "N분마다 체크" — 시간 기반 트리거는 맥락 없이 발동하여 노이즈

## Source
ai-developer-mickey, Mickey 16, 2026-05-08
