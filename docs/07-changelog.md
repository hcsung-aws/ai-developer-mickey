# Mickey 프롬프트 변경 이력

> Mickey 시스템 프롬프트의 버전별 변경사항을 기록합니다.

## 버전 요약

| 버전 | 날짜 | 프로젝트 | 핵심 변화 |
|------|------|----------|----------|
| v2.0 | 2024-12 | Godot 리플레이 시스템 | 세션 연속성, 지식 관리 체계 확립 |
| v5.0 | 2025-01 | 패킷 캡처 에이전트 | 목적 우선, 체크리스트, 자동화 |
| v5.1 | 2026-01 | AI Agent 자동화 플랫폼 | 전제조건 검증, Agent Builder 연동 |
| v5.2 | 2026-02 | AI Agent 자동화 플랫폼 | 문서화 패턴, 점진적 도입 원칙 |
| v5.3 | 2026-02 | AI Agent 자동화 플랫폼 | 세션 종료 프로토콜, 자동 개선 제안 |
| v5.4 | 2026-02 | AI Agent 자동화 플랫폼 | 필수 테스트 프로토콜 |
| v6.0 | 2026-02 | 프롬프트 경량화 | 도메인 특화 제거, 스키마 전환, 3-Tier 로딩 |
| v6.1 | 2026-02 | Mickey 자기 개선 | T3 계층화 - INDEX 지도 패턴, Power steering 진화 |
| v6.2 | 2026-02 | Mickey 자기 개선 | PURPOSE-SCENARIO 기반 목적 관리 체계 도입 |
| v6.3 | 2026-03 | Mickey 자기 개선 | Auto Memory 패턴 (자동 메모리 이원화) |
| v7 | 2026-03 | Mickey 자기 개선 | 자율 실행 + Subagent 협업 + Brownfield 온보딩 |
| v7.1 | 2026-03 | Mickey 자기 개선 | Adaptive Rules (자가 개선 sub-prompt) |
| v7.2 | 2026-03 | Mickey 자기 개선 | Autonomy Preference (사용자별 자율성 수준) |

---

## v7.2 (2026-03-09)

**프로젝트**: Mickey 자기 개선 (Mickey 9)

### 핵심 변화: Autonomy Preference (사용자별 자율성 수준)

사용자마다 원하는 자율성 수준이 다른 문제를 해결. 첫 세션에서 자율성 수준을 확인하고 ENVIRONMENT.md에 기록.

### 주요 변경

1. **3단계 자율성 수준**
   - Conservative: 모든 파일 변경 전 확인
   - Balanced (기본): 메모/로그는 자율, 그 외는 확인
   - Autonomous: CC 명확한 작업은 자율 실행

2. **CLI 연계**: `--trust-tools` 플래그로 자율성 수준에 맞는 도구 자동 승인

3. **T1.5 섹션 4 확장**: 자율성 수준별 상세 가이드

---

## v7.1 (2026-03-09)

**프로젝트**: Mickey 자기 개선 (Mickey 9)

### 핵심 변화: Adaptive Rules (자가 개선 sub-prompt)

프로젝트마다 다른 행동 규칙을 사용자가 일일이 알려줘야 하는 문제를 해결.

### 주요 변경

1. **context_rule/adaptive.md**: AI가 자가 수정 가능한 sub-prompt
   - 작업 중 패턴 발견 시 스스로 규칙 추가
   - 세션 종료 시 사용자 일괄 확인

2. **안전장치**: 기존 context_rule/ 파일은 수정 불가, adaptive.md만 자가 수정

3. **승격 경로**: adaptive.md → context_rule/ → common_knowledge/ → REMEMBER

4. **T1.5 섹션 8**: Adaptive Rules 상세 지침

---

## v7 (2026-03-08)

**프로젝트**: Mickey 자기 개선 (Mickey 8-9)

### 핵심 변화: 자율 실행 + Subagent 협업 + Brownfield 온보딩

단일 에이전트의 한계를 극복하기 위한 자율성 확보와 협업 체계 도입.

### 주요 변경

1. **자율 실행 조건**
   - Completion Criteria 명확 + rollback 가능 + 검증 가능 시 자율 진행
   - REMEMBER #14로 추가

2. **Backpressure**
   - 검증 실패 시 다음 단계 진행 금지
   - 수정 → 재검증 통과 후에만 진행
   - REMEMBER #15로 추가

3. **Brownfield 온보딩**
   - 기존 코드베이스 감지 시 자동 분석 절차
   - T1.5에 상세 온보딩 프로토콜

4. **T1.5 계층 도입**
   - `~/.kiro/mickey/extended-protocols.md`로 상세 지침 분리
   - `install.sh`로 배포 자동화

5. **Subagent 협업 가이드**
   - T1.5에 subagent 위임 지침 추가

---

## v6.3 (2026-03-01)

**프로젝트**: Mickey 자기 개선 (Mickey 5)

### 핵심 변화: Auto Memory 패턴 (자동 메모리 이원화)

"사용자가 작성하는 규칙"과 "AI가 기록하는 관찰 사실"을 분리.

### 주요 변경

1. **auto_notes/ 도입**
   - AI가 관찰한 사실을 자동 기록 (사용자 확인 불필요)
   - NOTES.md 인덱스 + 토픽별 파일 (commands.md, file-roles.md 등)
   - 세션 종료 시 일괄 확인

2. **파일 크기 제한**
   - T2 파일: 50줄 (project-context만 80줄)
   - T3a 인덱스: 50줄
   - 초과 시 축약/승격/분리

3. **작업 단위 트리거**
   - 세션 로그를 세션 종료 시가 아닌 작업 단위로 업데이트
   - 5가지 트리거 조건 정의

4. **교훈 승격 경로**
   - auto_notes → context_rule → common_knowledge → REMEMBER
   - 승격 기준: 같은 실수 2회 이상, 범용 패턴 발견, 근본 원칙 수준

---

## v6.2 (2026-02-21)

**프로젝트**: Mickey 자기 개선 (Mickey 14)

### 핵심 변화: PURPOSE-SCENARIO 기반 목적 관리 체계

v6.1까지 "목적"이 체크리스트 수준에 머물러 있어, 작업에 몰입할수록 전체 그림과의 정합성을 놓치는 문제를 해결.

### 주요 변경

1. **PURPOSE-SCENARIO.md 독립 문서 도입**
   - 필수 섹션: Ultimate Purpose, Usage Scenarios, Acceptance Criteria, Last Confirmed
   - T2 최우선 로딩 대상으로 지정

2. **세션 프로토콜 강화**
   - First Session: "이 프로젝트가 완성되면 어떻게 사용하게 되나요?" 질문 → PURPOSE-SCENARIO.md 생성
   - Continuing Session: PURPOSE-SCENARIO.md 최우선 로딩 + 목적 재확인
   - During Session: 목적 정합성 체크 (충돌/이탈/기술 제약 시 사용자에게 알림)

3. **문제 해결 프로토콜 구체화**
   - #1 목적 재확인 → PURPOSE-SCENARIO.md의 사용 시나리오와 대조

4. **REMEMBER #1 격상**
   - "목적 우선" → "PURPOSE-SCENARIO.md가 모든 판단의 최우선 기준. 충돌/이탈 감지 시 즉시 사용자에게 알림"

### Power Mickey 동시 반영
- steering 4개 파일 + POWER.md hook prompt에 PURPOSE-SCENARIO 체계 적용
- Hook은 Power와 독립 동작하므로 hook prompt에 직접 로딩 지시 포함

---

## v6.1 (2026-02-19)

**프로젝트**: Mickey 자기 개선 (Mickey 13)

### 핵심 변화: T3 계층화 및 Power steering 진화

3-Tier Context Loading의 T3를 세분화하고, Kiro IDE Power 형태의 Mickey를 실전 테스트 기반으로 개선.

### 주요 변경

1. **T3 계층화 — INDEX 지도 패턴**
   - T3a(지식 지도): 세션 시작 시 INDEX.md만 로딩하여 "어떤 지식이 있는지" 파악
   - T3b(상세): 작업 중 INDEX 트리거 매칭 시 해당 파일만 로딩
   - INDEX에 없는 파일은 로딩하지 않음 (INDEX 업데이트 우선)

2. **Power Mickey 실전 테스트 반영**
   - 하이브리드 context loading: SESSION-BRIEF(스크립트 생성 요약) + memorygraph(제목/태그만)
   - Hook 버전 업그레이드: 세션 초기화/종료 hook의 prompt 정교화
   - memorygraph Windows hang 버그 대응 (project 파라미터 필수)

3. **context_rule/INDEX.md, common_knowledge/INDEX.md 도입**
   - 트리거 → 파일 → 요약 매핑 테이블
   - 작업 중 트리거 조건에 매칭되면 해당 T3b 파일만 로딩

---

## v6.0 (2026-02-08)

**프로젝트**: 시스템 프롬프트 경량화/최적화 (Mickey 12)

### 핵심 변화: 경량화 및 자립형 설계

v5.x에서 누적된 도메인 특화 내용을 제거하고, 프롬프트 하나만으로 어떤 프로젝트에서든 동작하도록 재설계.

### 주요 변경

1. **템플릿 → Document Schema 전환**
   - 8개 템플릿 전문(~200줄) → Schema 테이블 1개(~10줄)
   - Mickey가 프로젝트 분석 결과로 내용을 채워 생성

2. **도메인 특화 내용 제거**
   - Async/Callback Pattern Checklist (C++ 특화)
   - Multiplayer State Sync Checklist (게임 서버 특화)
   - Windows Build Checklist (MSVC 특화)
   - 프로젝트 유형별 상세 분석 분기 (Unity/Unreal/Godot/Web/Data Science)

3. **3-Tier Context Loading 도입**
   - T1(항상): 시스템 프롬프트 - 범용 원칙, 세션 프로토콜
   - T2(세션 시작): PROJECT-OVERVIEW, latest HANDOFF, project-context
   - T3(필요 시): 특정 knowledge 파일, 과거 세션 로그

4. **REMEMBER 정리**: 24개 → 13개 (범용 원칙만 유지)

### 설계 원칙
- 시스템 프롬프트에는 범용 원칙만 포함
- 도메인/기술 특화 교훈은 프로젝트별 context_rule/에서 관리
- 프롬프트 1개만으로 어떤 프로젝트에서든 자립 가능

---

## v5.4 (2026-02-05)

**프로젝트**: AI Agent 자동화 플랫폼 (Mickey 11)

### 추가된 섹션
- **MANDATORY TESTING PROTOCOL**: 모든 구현은 테스트 검증 후 완료 처리

### REMEMBER 추가
```
24. **테스트 기반 완료 처리**: 모든 구현은 테스트 작성/통과/문서화 후에만 완료 선언 (Mickey 11)
```

### 핵심 원칙
- 새 기능 구현 시 테스트 필수 작성
- 기존 기능 수정 시 관련 테스트 유지보수
- tests/README.md에 테스트 목록 문서화
- TDD 워크플로우 권장

---

## v5.3 (2026-02-04)

**프로젝트**: AI Agent 자동화 플랫폼 (Mickey 9)

### 추가된 섹션
- **SESSION END PROTOCOL**: 세션 종료 시 교훈 분석 및 자동 개선 프로세스

### 핵심 변화
1. **교훈 분류 체계**
   - 범용 원칙 → 시스템 프롬프트에 추가
   - 프로젝트 지침 → context_rule/에 추가

2. **자동 개선 제안**
   - 세션 중 발견한 패턴을 사용자에게 제안
   - 승인 후 자동으로 프롬프트/지침에 반영

---

## v5.2 (2026-02-02)

**프로젝트**: AI Agent 자동화 플랫폼 (Mickey 8)

### 추가된 섹션
- **DOCUMENTATION PATTERN**: 문서 작성 시 핵심 메시지 정의, 사용자 여정 기반 구조화
- **INCREMENTAL ADOPTION PRINCIPLE**: 최소 기능 시작, 피드백 기반 확장

### REMEMBER 추가
```
20. **문서 작성 시 핵심 메시지 먼저**: 사용자 여정 기반 구조화 (Mickey 8)
21. **점진적 도입**: 최소 기능 시작 + 피드백 기반 확장만 (Mickey 8)
```

---

## v5.1 (2026-01-31)

**프로젝트**: AI Agent 자동화 플랫폼 (Mickey 7)

### 추가된 섹션
- **전제조건 검증**: 구현 시작 전 목적 달성에 필요한 핵심 자원/조건 확보 여부 확인

### REMEMBER 추가
```
19. **전제조건 우선 검증**: 구현 시작 전 목적 달성에 필요한 핵심 자원/조건 확보 여부 확인 (Mickey 10)
22. **WSL2 성능 주의**: LLM/ML 추론 시 WSL2는 SIMD 성능 90% 손실, 네이티브 실행 권장 (Mickey 7)
23. **작업 단위별 테스트 필수**: 구현 후 반드시 실제 환경에서 테스트/검증 (Mickey 7)
```

---

## v5.0 (2025-01)

**프로젝트**: 패킷 캡처 에이전트 (Mickey 1-12)

### 핵심 변화
1. **5가지 핵심 원칙**
   - 목적 우선
   - 단순함 우선
   - 근본 원인 우선
   - 빌드 시스템 확인
   - 조기 방향 전환

2. **체크리스트 기반 접근**
   - TOOL/SOLUTION SELECTION CHECKLIST
   - BUILD SYSTEM CHECKLIST
   - ERROR HANDLING PROTOCOL
   - PROBLEM-SOLVING PROTOCOL

3. **REMEMBER 섹션**
   - 핵심 원칙을 번호로 정리
   - 세션 중 빠르게 참조 가능

자세한 내용: [프롬프트 진화 가이드](06-prompt-evolution.md)

---

## v2.0 (2024-12)

**프로젝트**: Godot 리플레이 시스템 (Mickey 1-6)

### 핵심 구조
1. **세션 연속성**
   - MICKEY-N-SESSION.md 로그
   - MICKEY-N-HANDOFF.md 인수인계

2. **지식 관리**
   - common_knowledge/: 범용 지식
   - context_rule/: 프로젝트별 규칙

3. **Context Window 관리**
   - 50%/70%/90% 알림
   - 정리 및 핸드오프 프로토콜

자세한 내용: [핵심 가이드 문서](01-introduction.md)

---

## 프롬프트 파일

최신 프롬프트는 [examples/ai-developer-mickey.json](../examples/ai-developer-mickey.json)에서 확인할 수 있습니다.
