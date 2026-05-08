# Decisions

## Decision Log

### 2026-05-08 | Mickey 16 | Knowledge Curator 전체 지식 관리자 확장 + Domain Backlink
- **Options**:
  - A) 세션 중 자동 호출 유지 (기존 v14)
    - 장점: 실시간 지식 구조화
    - 단점: 6개 프로젝트에서 호출 0회 — 구조적 실패 증명
  - B) 세션 종료 배치 + Domain Backlink (채택)
    - 장점: 자연스러운 중단점에 배치, passive 활용 경로 확보
    - 단점: 실시간성 포기
- **Chosen**: B
- **Reasoning**: Active 활용(의식적 검색)은 구조적으로 실패. Passive 활용(context window에 있으면 자연스럽게 참조)만 동작. Domain Backlink로 프로젝트 INDEX → domain entry 직접 링크를 삽입하여 passive 발견 경로 확보.
- **검증 시점**: 2026-06-08 (1개월 후). 3개+ 프로젝트에서 세션 종료 시 Curator 호출 여부 + Domain Backlink가 실제 참조된 사례 확인.
- **Status**: Active — 검증 대기

### 2026-05-08 | Mickey 16 | adaptive.md 역할 재정의
- **Options**:
  - A) 모든 행동에 참조되는 규칙 (기존 설계)
  - B) 승격을 위한 스테이징 영역 (채택)
- **Chosen**: B
- **Reasoning**: adaptive.md는 축적→전환(승격)을 위한 지식. 모든 행동에 참조될 필요 없음. 3+ 세션 유효 시 프로토콜 직접 삽입 또는 context_rule/ 승격이 핵심 가치.
- **검증 시점**: 2026-06-08. adaptive.md → 프로토콜/context_rule 승격이 실제 발생했는지 확인.
- **Status**: Active — 검증 대기

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
