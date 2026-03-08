# Mickey 소개

> [English Version](01-introduction-en.md)

## Mickey란?

**Mickey**는 세션 연속성을 유지하며 지속적으로 개선하는 AI 개발자 에이전트입니다. Kiro CLI의 agent 기능을 활용하여 만들어졌으며, 복잡한 소프트웨어 개발 프로젝트에서 발생하는 문제들을 해결합니다.

### 왜 Mickey가 필요한가?

AI 코딩 어시스턴트를 써본 사람이라면 이런 경험이 있을 것입니다:

| 문제 | 원인 | Mickey의 해결 |
|------|------|-------------|
| 어제 설명한 것을 오늘 다시 설명 | 세션 간 기억 없음 | 파일 기반 세션 연속성 |
| 작업에 몰입하다 원래 목적에서 이탈 | 목적 추적 메커니즘 없음 | PURPOSE-SCENARIO 기반 목적 관리 |
| 프로젝트가 커질수록 AI가 전체 그림을 놓침 | Context window 한계 | 3-Tier Context Loading |
| 같은 실수를 반복 | 교훈 축적 시스템 없음 | 지식 관리 + 자동 메모리 |
| 매번 "이것 기록해"라고 지시해야 함 | 자율성 없음 | Adaptive Rules + Autonomy Preference |

## 핵심 개념

### 1. 세션 연속성 (Session Continuity)

**왜**: AI는 세션이 끝나면 모든 것을 잊습니다. 대화는 휘발되지만, 파일은 남습니다.

**무엇을**: 각 세션의 작업 내용, 결정 사항, 교훈을 파일로 저장하고, 다음 세션에서 자동으로 로딩합니다.

**어떻게**:
```
Mickey 1 → [SESSION.md + HANDOFF.md 저장] → Mickey 2 → [이전 기록 로딩 + 작업 이어가기] → ...
```

### 2. 지속적 개선 (Continuous Improvement)

**왜**: 같은 실수를 반복하는 것은 시간 낭비입니다.

**무엇을**: 실패 경험을 체계적으로 기록하고, 다음 세션에서 자동으로 참고합니다.

**어떻게**:
- `auto_notes/`: AI가 관찰한 사실을 자동 기록 (빌드 명령, 에러 해결법 등)
- `context_rule/`: 검증된 규칙 (반복 실패 방지, 환경 설정)
- `context_rule/adaptive.md`: AI가 스스로 학습한 행동 규칙 (자가 개선)

### 3. 목적 우선 (Purpose-First)

**왜**: AI는 주어진 작업을 열심히 하지만, 그것이 목적에 최적인지 판단하지 않습니다.

**무엇을**: 프로젝트의 최종 목적과 사용 시나리오를 독립 문서로 관리하고, 모든 판단의 기준으로 삼습니다.

**어떻게**: `PURPOSE-SCENARIO.md`를 세션 시작 시 최우선으로 로딩하고, 작업 중 목적과의 정합성을 지속 체크합니다.

### 4. 명명 규칙

Mickey는 세션마다 번호를 증가시킵니다: Mickey 1, Mickey 2, Mickey 3, ...
이를 통해 각 세션의 작업을 명확히 추적할 수 있습니다.

## Mickey의 구조 (v7.2)

### 시스템 프롬프트 구성

Mickey의 행동은 계층적으로 구성됩니다:

| 계층 | 위치 | 역할 | 로딩 시점 |
|------|------|------|----------|
| **T1** | 시스템 프롬프트 | 핵심 정체성, 범용 원칙, 세션 프로토콜 | 항상 |
| **T1.5** | `~/.kiro/mickey/` | 상세 실행 지침 (Brownfield, 자율성, Backpressure 등) | 세션 시작 |
| **T2** | 프로젝트 루트 | PURPOSE-SCENARIO, PROJECT-OVERVIEW, HANDOFF, adaptive.md | 세션 시작 |
| **T3a** | INDEX 파일들 | 지식 지도 (어떤 지식이 있는지) | 세션 시작 |
| **T3b** | 개별 지식 파일 | 상세 지식 (필요할 때만) | 작업 중 |

**왜 이렇게 나누는가?** Context window는 유한합니다. 모든 정보를 한 번에 넣으면 정작 필요한 정보를 놓칩니다. "지도를 주되, 백과사전을 주지 마라" — 필요한 것만 필요한 때에 로딩합니다.

### 핵심 원칙 (REMEMBER)

```
1.  목적 우선: PURPOSE-SCENARIO.md가 모든 판단의 최우선 기준
2.  단순함 우선: 복잡한 솔루션보다 단순한 대안 먼저
3.  Session log FIRST, then work
4.  Analysis BEFORE implementation
5.  에러 로그 즉시 확인 (추측 금지)
6.  User confirmation BEFORE changes (auto_notes/adaptive.md는 자동)
7.  Root cause OVER quick fixes
8.  복잡도 과도 시 대안 제안
9.  전제조건 우선 검증
10. 문서 작성 시 핵심 메시지 먼저
11. 점진적 도입: 최소 기능 시작 + 피드백 기반 확장
12. 작업 단위별 테스트 필수
13. 테스트 기반 완료 처리
14. 자율 실행 조건: CC 명확 + rollback 가능 + 검증 가능
15. Backpressure: 검증 실패 시 다음 단계 진행 금지
```

### 자율성 수준 (Autonomy Preference)

Mickey는 첫 세션에서 사용자에게 자율성 수준을 물어봅니다:

| 수준 | 이름 | Mickey 행동 |
|------|------|------------|
| 1 | Conservative | 모든 파일 변경 전 확인 |
| 2 | Balanced (기본) | 메모/로그는 자율, 그 외는 확인 |
| 3 | Autonomous | 완료 기준 명확한 작업은 자율 실행 |

사용자는 언제든 "자율성 조정"으로 변경할 수 있습니다.

## 디렉토리 구조

Mickey가 프로젝트에서 생성하는 파일들:

```
project-root/
├── PURPOSE-SCENARIO.md          # 최종 목적 + 사용 시나리오
├── PROJECT-OVERVIEW.md          # 프로젝트 개요
├── ENVIRONMENT.md               # 환경 정보 + 자율성 수준
├── FILE-STRUCTURE.md            # 파일 구조
├── DECISIONS.md                 # 의사결정 로그
├── MICKEY-N-SESSION.md          # 세션 로그 (작업 기록)
├── MICKEY-N-HANDOFF.md          # 핸드오프 (다음 세션 인수인계)
├── context_rule/                # 프로젝트 특화 규칙
│   ├── INDEX.md                 # 규칙 지도
│   ├── project-context.md       # 환경/목표/제약/교훈
│   └── adaptive.md              # 🆕 AI 자가 생성 규칙
├── common_knowledge/            # 범용 재사용 패턴
│   └── INDEX.md                 # 지식 지도
└── auto_notes/                  # AI 자동 관찰 기록
    └── NOTES.md                 # 메모 인덱스
```

## 빠른 시작

### 설치

```bash
# Kiro CLI 설치 후 (https://github.com/aws/kiro-cli)
git clone https://github.com/hcsung-aws/ai-developer-mickey.git
cd ai-developer-mickey
./install.sh
```

### 실행

```bash
cd <프로젝트 디렉토리>
kiro-cli chat --agent ai-developer-mickey
```

자율성 수준에 따라 CLI 플래그를 추가할 수 있습니다:
```bash
# Balanced (파일 읽기/쓰기 자동 승인)
kiro-cli chat --agent ai-developer-mickey --trust-tools=fs_read,fs_write

# Autonomous (대부분 자동 승인)
kiro-cli chat --agent ai-developer-mickey --trust-tools=fs_read,fs_write,execute_bash,grep,glob,code
```

### Mickey가 자동으로 수행하는 것

1. 프로젝트 분석 및 초기 문서 생성
2. 자율성 수준 확인
3. 세션 로그 작성 (MICKEY-N-SESSION.md)
4. 교훈 기록 및 다음 세션 인수인계
5. 관찰 사실 자동 기록 (auto_notes/)
6. 행동 규칙 자가 학습 (adaptive.md)

## 장점

### 1. Context Window 효율성
- 3-Tier 로딩으로 필요한 정보만 선택적 로드
- INDEX 지도 패턴으로 "어디에 뭐가 있는지"만 먼저 파악

### 2. 작업 연속성
- 세션 재시작 시에도 작업 흐름 유지
- PURPOSE-SCENARIO로 목적 이탈 방지

### 3. 지식 축적
- auto_notes/로 관찰 사실 자동 기록
- adaptive.md로 행동 규칙 자가 학습
- 교훈 승격 경로: auto_notes → context_rule → common_knowledge → 시스템 프롬프트

### 4. 사용자 제어
- Autonomy Preference로 자율성 수준 조절
- 세션 종료 시 자동 기록 일괄 리뷰
- 고위험 결정은 항상 사용자 확인

## 다음 단계

- [Context Window 관리](02-context-management.md) - 3-Tier 로딩과 INDEX 패턴
- [세션 연속성](03-session-continuity.md) - 세션 프로토콜과 목적 관리
- [Prompt 엔지니어링](04-prompt-engineering.md) - 효과적인 프롬프트 구조화
- [지식 관리 시스템](05-knowledge-management.md) - 자동 메모리와 교훈 승격
- [프롬프트 진화](06-prompt-evolution.md) - v2.0 → v7.2 진화 과정
- [진화 인사이트](08-evolution-insight.md) - "AI를 잘 쓰는 법"이 어떻게 진화해 왔는가
