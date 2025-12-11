# Mickey 소개

> [English Version](01-introduction-en.md)

## Mickey란?

**Mickey**는 세션 연속성을 유지하며 지속적으로 개선하는 AI 개발자 에이전트입니다. Kiro CLI의 agent 기능을 활용하여 만들어졌으며, 복잡한 소프트웨어 개발 프로젝트에서 발생하는 context window 한계와 세션 간 일관성 문제를 해결합니다.

## 핵심 개념

### 1. 세션 연속성 (Session Continuity)

Mickey는 각 세션이 끝날 때 작업 내용, 결정 사항, 학습한 내용을 파일로 저장합니다. 다음 세션이 시작되면 이전 세션의 기록을 읽어 작업을 이어갑니다.

```
Mickey 1 → [세션 로그 저장] → Mickey 2 → [세션 로그 저장] → Mickey 3 ...
```

### 2. 지속적 개선 (Continuous Improvement)

각 Mickey는 이전 Mickey들의 경험을 바탕으로 더 나은 결정을 내립니다:

- 성공한 접근 방식 재사용
- 실패한 시도 회피
- 새로운 패턴 학습 및 적용

### 3. 명명 규칙 (Naming Convention)

Mickey는 세션마다 번호를 증가시킵니다:
- 첫 세션: **Mickey 1**
- 두 번째 세션: **Mickey 2**
- 세 번째 세션: **Mickey 3**
- ...

이를 통해 각 세션의 작업을 명확히 추적할 수 있습니다.

## Mickey 에이전트 설정

### 기본 설정

```json
{
  "name": "ai-developer-mickey",
  "description": "각 세션마다의 성공 및 실패 기록들을 계속 다음 세션으로 참고하여 이어갈 수 있게 파일로 저장하며 지속적인 개선을 통해 문제를 해결하는 에이전트",
  "prompt": "You are an AI developer agent 'Mickey'...",
  "tools": ["*"],
  "resources": [
    "file://AGENTS.md",
    "file://README.md"
  ]
}
```

### 시스템 프롬프트 (핵심 부분)

```
You are an AI developer agent 'Mickey', that maintains session continuity 
by saving records to files and carrying them forward to subsequent sessions. 
Your primary goal is to solve problems through continuous improvement by:

1. Saving session records, progress, and learnings to persistent files
2. Loading and reviewing previous session data at the start of new sessions
3. Building upon previous work and insights
4. Tracking problem-solving approaches and their effectiveness
5. Iteratively improving solutions based on accumulated knowledge
6. Monitoring context window usage and alerting the user when a new session is needed

Always maintain detailed logs of your work, decisions made, and lessons learned. 
Use file operations to ensure continuity across sessions and provide comprehensive 
problem-solving through persistent memory. You should increase postfix 1 by 1 after 
your name from 1. For example, first you is 'Mickey 1', and in the next session, 
you can read your previous postfix and set your name 'Mickey 2'.
```

## 디렉토리 구조

Mickey는 다음과 같은 디렉토리 구조를 사용합니다:

```
project-root/
├── MICKEY-1-SESSION.md      # Mickey 1의 세션 로그
├── MICKEY-2-SESSION.md      # Mickey 2의 세션 로그
├── MICKEY-3-SESSION.md      # Mickey 3의 세션 로그
├── common_knowledge/        # 재사용 가능한 지식
│   ├── INDEX.md            # 지식 인덱스
│   ├── godot/              # Godot 관련 지식
│   └── testing/            # 테스팅 관련 지식
└── context_rule/           # 컨텍스트 규칙
    ├── project-context.md  # 프로젝트 컨텍스트
    └── troubleshooting.md  # 트러블슈팅 가이드
```

## 세션 로그 형식

각 Mickey는 다음 형식으로 세션 로그를 작성합니다:

```markdown
# Mickey N Session Log
Date: YYYY-MM-DDTHH:MM:SS+09:00

## Session Goal
이번 세션의 목표

## Previous Context (Mickey N-1)
이전 세션에서 완료한 작업

## Current Tasks
현재 진행 중인 작업 목록

## Progress
- [x] 완료된 작업
- [ ] 진행 중인 작업

## Key Decisions
중요한 결정 사항

## Lessons Learned
배운 교훈

## Next Steps
다음 세션을 위한 작업
```

## 실제 사용 예시

### Mickey 1 → Mickey 2 전환

**상황**: Context window가 61%에 도달하여 세션 재시작 필요

**Mickey 1의 마지막 작업**:
```
Context Window Usage: 61%
→ 세션 로그 저장
→ 사용자에게 세션 재시작 권장
```

**Mickey 2의 시작**:
```
1. 이전 세션 로그 읽기 (MICKEY-1-SESSION.md)
2. 작업 컨텍스트 복원
3. "Mickey 2로 시작하겠습니다" 선언
4. 작업 이어가기
```

## 장점

### 1. Context Window 효율성
- 필요한 정보만 선택적으로 로드
- 세션 간 정보 압축 및 요약

### 2. 작업 연속성
- 세션 재시작 시에도 작업 흐름 유지
- 이전 결정 사항 참고 가능

### 3. 지식 축적
- 프로젝트별 지식 체계화
- 재사용 가능한 패턴 구축

### 4. 투명성
- 모든 결정 과정 기록
- 문제 해결 과정 추적 가능

## 다음 단계

- [Context Window 관리](02-context-management.md) - 컨텍스트 효율적 활용 방법
- [세션 연속성](03-session-continuity.md) - 세션 간 일관성 유지 전략
- [실전 사례](case-study/godot-replay-system.md) - Godot 프로젝트 적용 사례
