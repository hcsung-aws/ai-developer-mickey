# Decisions

## Decision Log

### 2026-07-17 | 세션 b3d7e1 | D-0717-1: 세션 기록 규약 (날짜+UID)
- **배경**: 같은 프로젝트에서 세션이 여러 개 동시에 열리는 IDE 상황 + CLI 연속성 공백(boot hook이 매번 "Mickey 1" 오판) 해소 필요.
- **Options**:
  - A) 기존 규약 유지 (`YYYY-MM-DD-<주제>.md`)
    - 장점: 변경 비용 없음
    - 단점: 동일 날짜 다중 세션 구분 불가, handoff 자동 탐지 시 세션 식별 모호
  - B) 날짜+UID 규약 (채택)
    - 로그 `YYYY-MM-DD-<UID>-log.md` / handoff `YYYY-MM-DD-<UID>-handoff.md`, UID는 6자리 hex
    - 장점: 다중 세션 유일 식별, 채팅 응답에 UID를 남겨 IDE에서 세션 선택 가능, 기계 탐지 용이(`*-handoff.md` glob)
    - 단점: UID 생성 절차 추가 (스크립트로 완화: `.kiro/scripts/gen_session_uid.py`)
  - C) MICKEY-N 세션 번호 도입
    - 단점: `sessions/MICKEY-N-*`은 master(CLI 트랙) 소유 — 번호 충돌 위험, v3 통합 시 병합 위험
- **Chosen**: B
- **Reasoning**: IDE 다중 세션과 CLI 연속성 공백을 동시에 해결하는 유일한 안. 이어가기 절차는 양쪽 분기 명시 — IDE: UID 지정 시 해당본 로드 / 미지정 시 최신본 제시 후 확인. CLI: 최신 log+handoff 탐지 → 사용자 확인 후 진행 (자동 진행 금지).
- **부속 결정**: power steering(session-protocol.md)으로의 일반화는 v3 통합 시점 판단으로 보류. 사용자 재확인 전 steering 수정 금지.
- **성문화**: kickoff 문서 §2 (2026-07-19, 세션 551c3f)
- **Status**: Active — b3d7e1부터 적용 중 (첫 적용 사례: b3d7e1 자체, 두 번째: 551c3f)

### 2026-07-17 | 세션 b3d7e1 | D-0717-2: hook 처리 방침 (삭제 후 완전 개정)
- **배경**: IDE 1.0이 legacy `.kiro.hook`(when/then)을 로딩하지 않음 확정 (kiro.dev/docs/whats-new-1-0.md 실측). 신규격은 CLI v3와 동일한 v1 JSON — SessionStart가 IDE에도 존재하므로 hook 하나로 양쪽 커버 가능.
- **Options**:
  - A) 기존 hook 부분 수정
    - 단점: 무효 규격(.kiro.hook) 잔존, boot 스크립트의 오판 로직(트랙 미인지, 대문자 HANDOFF glob) 유지
  - B) 삭제 후 완전 개정 (채택)
    - 삭제: `mickey-pre-task.kiro.hook`, `mickey-post-task.kiro.hook` (양쪽 규격에서 무효), `mickey-session-start.json` (boot 스크립트 개정과 함께 재작성)
    - 장점: 무효 자산 정리 + 새 규약(D-0717-1) 기준 일관 재설계
- **Chosen**: B
- **Reasoning**: legacy 규격은 IDE 1.0에서 로딩 자체가 안 되므로 부분 수정의 실익 없음. IDE 런타임 실증은 규약 성문화 + hook 개정 완료 후 수행.
- **Status**: Active — 2026-07-19 세션 551c3f에서 집행

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
- **Status**: **무효 (Superseded, 2026-07-19)** — IDE 1.0에서 userTriggered/askAgent를 포함한 legacy `.kiro.hook` 규격 자체가 폐기됨 (로딩되지 않음, upgrade badge만 표시). 신규격은 v1 JSON (D-0717-2 참조). Manual 트리거는 manual steering 파일(슬래시 커맨드)로 대체됨.

### 2026-02-19 | Mickey 1 | 하이브리드 Context Loading 도입
- **Options**:
  - A) 전부 로딩 (기존) — context ~3,100-6,500 토큰
  - B) 완전 on-demand — context ~550-750 토큰, 지식 활용도 낮음
  - C) 하이브리드 (지식 지도 패턴) — context ~800-1,100 토큰, 지식 활용도 유지
- **Chosen**: C
- **Reasoning**: context window ~75% 절감하면서 "뭘 알고 있는지" 파악 가능. CLI의 T3a INDEX 패턴과 동일 원리
- **Status**: 완료
