# 세션 연속성 (Session Continuity)

> [English Version](03-session-continuity-en.md)

## 문제 정의

AI 어시스턴트는 세션이 끝나면 모든 것을 잊습니다. 대화는 휘발되지만, 파일은 남습니다.

```
[세션 1 - 오전]
사용자: "로깅 시스템을 추가해줘"
AI: 분석 → 설계 → 구현 시작 → Context 70% 도달

[세션 2 - 오후]
사용자: "이어서 진행해줘"
AI: "무엇을 이어서 진행할까요?"
→ 이전 컨텍스트 없음, 처음부터 설명 필요
```

Mickey는 이 문제를 **파일 기반 세션 프로토콜**로 해결합니다.

## 세션 프로토콜

### 왜 (WHY)

세션 연속성은 단순히 "이전 작업을 기억하는 것"이 아닙니다. **목적을 유지하고, 교훈을 축적하고, 다음 세션이 즉시 작업을 시작할 수 있게** 하는 것입니다. 프로토콜 없이는 매 세션이 "처음부터"가 됩니다.

### 무엇을 (WHAT)

Mickey의 세션은 4단계 생명주기를 따릅니다:

| 단계 | 시점 | 핵심 행동 |
|------|------|----------|
| **First Session** | Mickey 1 | 환경 스캔 → 목적 확인 → 초기 문서 생성 |
| **Continuing Session** | Mickey N+1 | 컨텍스트 로딩 → 목적 재확인 → 세션 로그 생성 |
| **During Session** | 작업 중 | 트리거 기반 로그 업데이트 + 목적 정합성 체크 |
| **Session End** | 세션 정리 | 자동 기록 리뷰 → 교훈 승격 → 핸드오프 생성 |

### 어떻게 (HOW)

#### First Session (Mickey 1)

Mickey 파일이 없는 프로젝트에서 처음 시작할 때:

```
1. 환경 스캔 (OS, 디렉토리, git)
2. "이 프로젝트가 완성되면 어떻게 사용하게 되나요?" → 목적 + 시나리오 확인
3. 자율성 수준 확인 (Conservative / Balanced / Autonomous)
4. 프로젝트 분석 → 초기 문서 생성
5. 사용자 확인 후 작업 시작
```

생성되는 문서: PURPOSE-SCENARIO.md, PROJECT-OVERVIEW.md, ENVIRONMENT.md, FILE-STRUCTURE.md, DECISIONS.md, MICKEY-1-SESSION.md

#### Continuing Session (Mickey N+1)

기존 Mickey 파일이 있는 프로젝트에서 이어갈 때:

```
1. 컨텍스트 로딩 (우선순위 순):
   PURPOSE-SCENARIO.md ← 최우선
   → Latest HANDOFF.md
   → Latest SESSION.md
   → PROJECT-OVERVIEW.md
   → context_rule/project-context.md
   → adaptive.md
   → INDEX 파일들 (지식 지도)

2. 목적 재확인 + 엔트로피 체크
3. MICKEY-(N+1)-SESSION.md 생성
4. 이전 세션 요약 + 작업 시작
```

#### During Session (작업 중)

세션 로그는 세션 종료 시 한 번에 쓰는 것이 아니라, **작업 단위로 업데이트**합니다:

| 트리거 | 행동 |
|--------|------|
| TODO 항목 완료 | 세션 로그 Progress 업데이트 |
| 에러 조사→수정→검증 완료 | Lessons Learned 기록 |
| 사용자와 의사결정 확정 | Key Decisions 기록 |
| 파일 3개 이상 수정 | Files Modified 업데이트 |
| context_rule/ 또는 common_knowledge/ 변경 | 세션 로그 + INDEX 업데이트 |

#### Session End (세션 정리)

```
1. 세션 로그 최종 확인 (트리거로 이미 최신이므로 최소 작업)
2. auto_notes/ + adaptive.md 변경 내역 일괄 제시 → 사용자 확인
3. 교훈 승격 리뷰 → 사용자 확인 후 적용
4. HANDOFF 경량 생성 (다음 Mickey를 위한 내부 문서)
```

## PURPOSE-SCENARIO: 목적 관리

### 왜 (WHY)

AI는 주어진 작업을 열심히 하지만, 그것이 **원래 목적에 최적인지** 판단하지 않습니다. 작업에 몰입할수록 전체 그림을 놓기기 쉽습니다. "목적"을 체크리스트 항목으로만 두면 형식적으로 확인하고 넘어갑니다.

### 무엇을 (WHAT)

`PURPOSE-SCENARIO.md`는 프로젝트의 **최종 목적과 사용 시나리오**를 독립 문서로 관리합니다:

```markdown
# PURPOSE-SCENARIO

## Ultimate Purpose
AI를 잘 사용하는 법을 자연스럽게 익히는 실전 가이드

## Usage Scenarios
1. 개발자가 자기 프로젝트에 Mickey를 적용 → 점진적 개선
2. 인프라 운영 중 문제를 Mickey와 대응 → 세션간 기억
3. Mickey 자체 개선 → 에이전트 시스템 진화

## Acceptance Criteria
...

## Last Confirmed
2026-03-01 (Mickey 5)
```

### 어떻게 (HOW)

- 세션 시작 시 **최우선으로 로딩** (T2 최상위)
- 작업 중 아래 상황 발생 시 사용자에게 알림:
  - 구현 방향이 사용 시나리오와 충돌
  - 기능 확장으로 원래 목적과 다른 방향 발견
  - 기술적 제약으로 목적 달성 방식 변경 필요
- `Last Confirmed` 필드로 마지막 확인 시점 추적

## 세션 로그와 핸드오프

### 왜 (WHY)

세션 로그(SESSION.md)는 **현재 세션의 상세 기록**이고, 핸드오프(HANDOFF.md)는 **다음 세션을 위한 요약 인수인계**입니다. 둘을 분리하면 다음 Mickey는 HANDOFF만 읽고 즉시 시작할 수 있고, 필요하면 SESSION을 참조할 수 있습니다.

### 세션 로그 (MICKEY-N-SESSION.md)

```markdown
# Mickey N Session Log

## Session Goal
이번 세션의 명확한 목표

## Previous Context
이전 세션에서 완료한 작업, 중요한 결정

## Current Tasks
- [ ] 작업 1 | CC: 완료 기준 명시
- [x] 작업 2 | CC: 완료 기준 명시

## Progress
### Completed
1. 기능 A 구현
### In Progress
2. 기능 B 디버깅 (80%)

## Key Decisions
- GDScript > C++: 19배 효율 차이

## Files Modified
- replay_logger.gd (신규)

## Lessons Learned
- Delta 동기화가 근본 해결책

## Context Window Status
65% — 안전 범위

## Next Steps
- 리플레이 검증 시스템 구현
```

핵심: 각 작업에 **Completion Criteria (CC)**를 명시하여 완료 기준을 명확히 합니다.

### 핸드오프 (MICKEY-N-HANDOFF.md)

```markdown
# Mickey N Handoff

## Current Status
리플레이 시스템 구현 완료. 검증 시스템 미착수.

## Next Steps
state_validator.gd 구현 → 배치 테스트 인프라 구축

## Important Context
SESSION.md/auto_notes에 없는 것만 기록

## Quick Reference
- 세션 로그: MICKEY-N-SESSION.md
- Context window: 65%
```

핸드오프는 **사용자 확인 없이 자동 생성**합니다 — 다음 Mickey를 위한 내부 문서입니다.

## 엔트로피 관리

### 왜 (WHY)

세션이 쌓이면 문서가 늘어나고, INDEX와 실제 파일의 불일치, 오래된 SESSION 파일 누적, auto_notes 비대화 등 **엔트로피가 증가**합니다. 방치하면 3-Tier 로딩의 효율이 떨어집니다.

### 무엇을 (WHAT)

Continuing Session 시작 시 엔트로피 체크를 수행합니다:

| 체크 항목 | 행동 |
|----------|------|
| INDEX 정합성 | INDEX에 없는 파일 발견 → INDEX 업데이트 |
| auto_notes 최신성 | 오래된/중복 메모 → 정리 또는 승격 |
| SESSION 아카이빙 | 오래된 SESSION/HANDOFF → `sessions/` 폴더로 이동 |
| 파일 크기 | T2/T3a 파일 줄 수 초과 → 축약/분리 |

### 어떻게 (HOW)

```
세션 시작
  ├─ 컨텍스트 로딩
  ├─ 엔트로피 체크:
  │    ├─ INDEX에 없는 지식 파일? → INDEX 업데이트
  │    ├─ auto_notes 50줄 초과? → 카테고리 분리
  │    ├─ MICKEY-1~N-3 SESSION 존재? → sessions/로 아카이빙
  │    └─ project-context.md Lessons 5개 초과? → context_rule/로 승격
  └─ 작업 시작
```

## 실전 적용 사례

### Godot 프로젝트: Mickey 1 → Mickey 2 전환

**Mickey 1 종료 시**:
```
Context 61% → 세션 로그 저장
완료: 엔진 분석, 로깅 시스템 설계
다음: 자동 테스트 스크립트 구현
```

**Context Overflow 발생** → Compact로 상세 정보 유실

**Mickey 2 시작**:
```
이전 SESSION.md 읽기 → 컨텍스트 복원
"Mickey 2로 시작합니다. 이전 세션에서 로깅 시스템 설계를 완료했습니다."
→ Compact로 유실된 정보를 세션 로그에서 복원
```

**인사이트**: "대화는 휘발되지만, 파일은 남는다."

### Mickey 자체 개선: 9세션 연속 작업

Mickey 프로젝트 자체가 세션 연속성의 실전 사례입니다:

```
Mickey 1~6: 기반 구축 (v2→v5)
  → 교훈 14건 분석, 3건 common_knowledge 승격
  → SESSION 파일 sessions/self/로 아카이빙

Mickey 7~9: v7.2 구현
  → 이전 교훈 참조하며 자율 실행, Backpressure 등 도입
  → PURPOSE-SCENARIO로 목적 이탈 방지
```

**인사이트**: "세션이 쌓일수록 지식이 두꺼워진다. 단, 엔트로피 관리를 해야."

## 모범 사례

### DO ✅

1. **작업 단위로 로그 업데이트**: 세션 종료 시 한 번에 쓰지 않기
2. **결정 사항은 이유와 함께**: "GDScript 선택" → "GDScript 선택 (C++ 대비 19배 효율)"
3. **실패도 기록**: 시도한 접근과 실패 이유가 다음 세션의 시간을 절약
4. **정기적 엔트로피 정리**: INDEX 정합성, SESSION 아카이빙

### DON'T ❌

1. **장황한 세션 로그**: 에세이 대신 결과/결정/이슈만
2. **HANDOFF에 SESSION 내용 복사**: HANDOFF는 1~2줄 요약만
3. **오래된 SESSION 방치**: 루트 디렉토리에 SESSION 파일 누적
4. **목적 확인 생략**: 작업에 몰입하다 PURPOSE-SCENARIO와 이탈

## 다음 단계

- [Prompt 엔지니어링](04-prompt-engineering.md) - 효과적인 프롬프트 구조화
- [지식 관리 시스템](05-knowledge-management.md) - 자동 메모리와 교훈 승격
- [프롬프트 진화](06-prompt-evolution.md) - v2.0 → v7.2 진화 과정
