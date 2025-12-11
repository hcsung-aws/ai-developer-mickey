# Prompt 엔지니어링

## Mickey 프롬프트 진화 과정

Mickey의 시스템 프롬프트는 작업을 거듭하면서 지속적으로 개선되었습니다.

### 초기 버전 (Mickey 1)

```
각 세션마다의 성공 및 실패 기록들을 계속 다음 세션으로 참고하여 
이어갈 수 있게 파일로 저장하며 지속적인 개선을 통해 문제를 해결하는 에이전트
```

**특징**: 간단하고 핵심만 담음

### 개선 버전 (Mickey 3 이후)

Godot 엔진 분석 과정에서 context window 한계 문제를 겪으면서 **지식 관리** 섹션 추가:

```
KNOWLEDGE MANAGEMENT:
- Store reusable knowledge for future Mickey sessions in ./common_knowledge/ directory
- Structure information in semantic units that minimize context window usage when loaded
- Add cross-references between documents
```

**추가된 이유**: 거대한 코드베이스 분석 시 효율적인 정보 구조화 필요

### 최종 버전 (현재)

```
You are an AI developer agent 'Mickey', that maintains session continuity 
by saving records to files and carrying them forward to subsequent sessions.

Your primary goal is to solve problems through continuous improvement by:
1. Saving session records, progress, and learnings to persistent files
2. Loading and reviewing previous session data at the start of new sessions
3. Building upon previous work and insights
4. Tracking problem-solving approaches and their effectiveness
5. Iteratively improving solutions based on accumulated knowledge
6. Monitoring context window usage and alerting when a new session is needed

KNOWLEDGE MANAGEMENT:
- Store reusable knowledge in ./common_knowledge/ directory
- Structure information in semantic units
- Add cross-references between documents

CONTEXT RULES:
- Document repeated failures in ./context_rule/ directory
- Store as actionable guidelines
- Organize by semantic meaning

IMPORTANT: If context window lacks sufficient space, inform the user 
to restart the session. Save all progress before recommending restart.
```

## 핵심 프롬프트 원칙

### 1. 명확한 역할 정의

```
You are an AI developer agent 'Mickey'
```

**왜 중요한가**: AI가 자신의 역할을 명확히 이해해야 일관된 행동 가능

### 2. 구체적인 행동 지침

```
1. Saving session records...
2. Loading and reviewing...
3. Building upon...
```

**왜 중요한가**: 추상적인 목표보다 구체적인 행동이 실행 가능

### 3. 제약 조건 명시

```
IMPORTANT: If context window lacks sufficient space, inform the user...
```

**왜 중요한가**: 문제 상황에서의 행동 규칙 필요

## 효과적인 사용자 프롬프트

### DO ✅

#### 1. 맥락 제공

**나쁜 예**:
```
"에러 고쳐줘"
```

**좋은 예**:
```
"Godot Pong 게임의 리플레이 시스템에서 Ball 위치 검증 시 
Frame 139에서 velocity diff=209.45 에러가 발생합니다. 
이전 Mickey 4가 Delta 동기화로 position 에러를 해결했는데, 
velocity 에러도 비슷한 원인일 수 있습니다. 분석해주세요."
```

#### 2. 단계별 확인 요청

**나쁜 예**:
```
"전부 구현해줘"
```

**좋은 예**:
```
"먼저 현재 구현을 분석하고, 문제점을 파악한 후, 
해결 방안을 제안해주세요. 각 단계마다 확인받겠습니다."
```

#### 3. 이전 작업 참조

**좋은 예**:
```
"이전 Mickey가 알려준 내용이랑 지침을 확인하라고"
"기존 구현에서 문제 없는지 전부 분석해서 확인하고 알려줘"
```

### DON'T ❌

#### 1. 모호한 지시

```
"잘 해줘"
"알아서 해줘"
"좋게 만들어줘"
```

#### 2. 맥락 없는 요청

```
"에러 났어"
"안 돼"
"이상해"
```

#### 3. 한 번에 너무 많은 요구

```
"A도 하고 B도 하고 C도 하고 D도 하고 E도 해줘"
→ 단계별로 나누기
```

## 실전 프롬프트 패턴

### 패턴 1: 분석 → 제안 → 확인

```
사용자: "현재 구현에서 기존에 동작 잘 하던 것들에 문제는 없을지 
        한번 전부 분석해서 확인하고 알려줘"

Mickey: [분석 수행]
        "다음 문제가 발견되었습니다:
         1. SimpleAI가 replay 모드에서 간섭
         2. 해결 방법: replay_mode 체크 추가
         수정하시겠습니까?"

사용자: "그래, 수정해줘"
```

### 패턴 2: 맥락 제공 → 작업 요청

```
사용자: "지금 Phase 3-1 진행 중이야. 
        Left와 Right 패들 모두 AI로 제어하고,
        다양한 시나리오(잘 쫓아가기, 실수로 골 먹기)를 
        만들 수 있어야 해. 
        현재 구현과 내 요구사항을 종합해서 제안해줘"

Mickey: [분석 후 제안]
```

### 패턴 3: 문제 상황 → 이전 해결책 참조

```
사용자: "Total frames played: 0이 혹시 초기화 과정에서 
        값이 0이 되어 버려서 생긴 문제일 수 있는지 
        기존 구현 분석해서 알려줘"

Mickey: [코드 분석]
        "ReplayInput.disable_replay()에서 _current_frame = 0으로 
         리셋됩니다. 이는 정상 동작입니다."
```

## 프롬프트 개선 사례

### 사례 1: 파일 경로 찾기

**초기 시도** (실패):
```
사용자: "Windows 경로 찾아줘"
Mickey: [전체 디렉토리 검색 시도] → 취소됨
```

**개선된 시도** (성공):
```
사용자: "이전 Mickey들의 기록이나 지침 참고해서 
        Windows 환경에서 어디 pong.tscn이 있는지 찾아서 계속 진행해"
Mickey: [context_rule/project-context.md 확인]
        "C:\Users\hcsung\work\q\ai-developer-mickey\pong\ 발견"
```

**교훈**: 기존 지식 활용 유도

### 사례 2: 설정 확인

**초기 시도** (불충분):
```
사용자: "테스트해줘"
Mickey: [테스트 실행] → 실패
```

**개선된 시도** (성공):
```
사용자: "BatchTestRunner 실행하기 위한 설정이 다 되어 있지 않은 것 같아.
        이전 Mickey에게 들었던 내용 확인해서 수정 필요한 것들 알려줘"
Mickey: [이전 기록 확인]
        "ReplayLogger: enable_logging = false 필요
         BatchTestRunner: auto_start = true 필요"
```

**교훈**: 구체적인 문제 상황 설명

## 다음 단계

- [지식 관리 시스템](05-knowledge-management.md) - 재사용 가능한 지식 구축
- [실전 사례](case-study/godot-replay-system.md) - Godot 프로젝트 적용 사례
