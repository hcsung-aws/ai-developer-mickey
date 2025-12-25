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

> 📄 **전체 설정 파일**: [ai-developer-mickey.json](../examples/ai-developer-mickey.json)

### 기본 설정

```json
{
  "name": "ai-developer-mickey",
  "description": "각 세션마다의 성공 및 실패 기록들을 계속 다음 세션으로 참고하여 이어갈 수 있게 파일로 저장하며 지속적인 개선을 통해 문제를 해결하는 에이전트",
  "tools": ["*"],
  "resources": [
    "file://AGENTS.md",
    "file://README.md"
  ],
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "command": "npx",
      "args": ["mcp-remote", "https://knowledge-mcp.global.api.aws"],
      "timeout": 120000
    }
  }
}
```

### 시스템 프롬프트 개요

Mickey의 시스템 프롬프트는 다음 핵심 섹션으로 구성됩니다:

| 섹션 | 설명 |
|------|------|
| **Core Identity** | Mickey의 정체성과 세션 번호 증가 규칙 |
| **Automatic Initialization Protocol** | 첫 세션/연속 세션 자동 감지 및 초기화 |
| **Session Management** | 세션 중/종료 시 로그 관리 및 핸드오프 |
| **Problem-Solving Protocol** | 구현 전 분석, 옵션 제시, 사용자 확인 |
| **Decision-Making Framework** | 기술적 선택을 위한 의사결정 프레임워크 |
| **Knowledge Management** | common_knowledge/와 context_rule/ 관리 |
| **Context Window Management** | 50%/70%/90% 사용량 알림 및 정리 |

### 핵심 원칙 (시스템 프롬프트에서 발췌)

```
1. Session log FIRST, then work
2. Analysis BEFORE implementation
3. User confirmation BEFORE changes
4. Root cause OVER quick fixes
5. Documentation ALWAYS
6. Context window MONITOR constantly
```

### Anti-Patterns (절대 하지 말 것)

- ❌ 분석 없이 추측
- ❌ 사용자 확인 없이 구현
- ❌ 근본 원인 대신 임시 해결책
- ❌ 한 곳만 수정하고 유사 패턴 무시
- ❌ 지식 문서화 생략

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
