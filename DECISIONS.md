# Decisions

## Decision Log

### 2026-02-19 | Mickey 1 | Power Mickey Hook 타입 변경
- **Options**:
  - A) agentSpawn + runCommand (기존)
    - 장점: 자동 실행
    - 단점: Kiro IDE에서 동작 안 함 (userTriggered는 askAgent만 지원)
  - B) userTriggered + askAgent (채택)
    - 장점: 실제 동작 확인됨
    - 단점: 수동 트리거 필요
- **Chosen**: B
- **Reasoning**: 실제 Kiro IDE 테스트에서 A가 동작하지 않음 확인
- **Status**: 완료

### 2026-02-19 | Mickey 1 | 하이브리드 Context Loading 도입
- **Options**:
  - A) 전부 로딩 (기존) — context ~3,100-6,500 토큰
  - B) 완전 on-demand — context ~550-750 토큰, 지식 활용도 낮음
  - C) 하이브리드 (지식 지도 패턴) — context ~800-1,100 토큰, 지식 활용도 유지
- **Chosen**: C
- **Reasoning**: context window ~75% 절감하면서 "뭘 알고 있는지" 파악 가능. CLI의 T3a INDEX 패턴과 동일 원리
- **Status**: 완료
