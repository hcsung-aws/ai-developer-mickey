---
inclusion: always
---

<!--
v17 T1 원문 대응 (원본: examples/ai-developer-mickey.json / dump: scripts/output/v17_prompt.md):
- DOCUMENT SCHEMA: L89~L107 (11종 문서 필수 섹션 표)

이식 원칙 (IMPROVEMENT-PLAN-v10 §8-b):
- 원문 표 그대로 이식.
- P3: 조건부 섹션(FILE-STRUCTURE 필수/선택, [Protocol] 태그)은 양쪽 분기 병기.
- 참조 위치: session-protocol.md First Step 5, Continuing Step 3, End Step 5.
-->

# document-schema

Mickey 가 생성·유지하는 11종 문서의 필수 섹션. 내용은 프로젝트 분석 결과로 채운다. 스키마 준수 여부는 Curator lifecycle 과 엔트로피 체크의 기준이 된다.

## 공통 필수 사항

- 모든 문서는 마지막 줄에 `Last Updated` (날짜) 를 기록.
- 세션 로그 계열(`MICKEY-N-*`) 은 파일명 자체가 세션 번호를 포함.
- 파일 크기 상한은 `knowledge-graph.md` 의 이중 가드 표 참조.

## 11종 문서 필수 섹션

| 문서 | 필수 섹션 |
|------|----------|
| **PROJECT-OVERVIEW.md** | Project Name, Goal, Scope, Constraints, Success Criteria, Current Status, Last Updated |
| **PURPOSE-SCENARIO.md** | Ultimate Purpose, Usage Scenarios (목적 달성 시 실제 사용 흐름), Acceptance Criteria, Last Confirmed (날짜+Mickey#), Last Updated |
| **ENVIRONMENT.md** | OS, Current Directory, Project Type, Tools Detected, Version Control, Key Paths, Dependencies, Autonomy Preference, Last Updated |
| **FILE-STRUCTURE.md** | [필수] Directory Tree (depth 2), Mickey Docs Locations, Code Analysis Tools (§19 감지 결과), Steering Trigger, Last Updated. [선택] Key Files, File Statistics, Project Structure Pattern |
| **DECISIONS.md** | Decision Log (각 항목: Date, Mickey, Topic, Options+Pros/Cons/Time/Risk, Chosen, Reasoning, Status) |
| **context_rule/project-context.md** | Environment, Goal, Constraints, Key Decisions, Known Issues, Lessons Learned, Common Commands, Last Updated |
| **context_rule/INDEX.md** | Rule Map (트리거→파일→요약), Last Updated |
| **common_knowledge/INDEX.md** | Knowledge Map (트리거→파일→요약), Last Updated |
| **auto_notes/NOTES.md** | Note Map (카테고리→파일→요약), Last Updated |
| **MICKEY-N-SESSION.md** | Checkpoint [0/5], Session Meta, Session Goal, Purpose Alignment, Previous Context, Current Tasks, Progress, Key Decisions, Files Modified, Lessons Learned, Context Window Status, Next Steps |
| **MICKEY-N-HANDOFF.md** | Current Status (1~2줄 요약), Next Steps (1~2줄 요약), Important Context (SESSION.md/auto_notes 에 없는 것만), Protocol Feedback (선택적, 해당 시), Quick Reference (SESSION/auto_notes 경로 + context window 상태) |

## 문서별 주의사항

### FILE-STRUCTURE.md — 필수/선택 분기 (P3)

- **Tier 1 (Serena/Graphify) 또는 Tier 2 도구 감지 시**: [선택] 섹션(Key Files, File Statistics, Project Structure Pattern)은 그 도구가 제공하는 결과로 대체 가능하므로 **생략 가능**. Mickey 는 필수 섹션만 유지.
- **Tier 3 (Kiro CLI 내장 `code` baseline) 만 사용 시**: [선택] 섹션도 **유지 권장** (Tier 3 는 지도 정보를 별도로 제공하지 않으므로 Mickey 지도 필요).
- 두 경우 모두 `Code Analysis Tools` 필드에 현재 감지 상태를 기록 (§19 감지 결과, `session-protocol.md` First Step 4a).

### MICKEY-N-SESSION.md — 세부 필드 규약

- **Checkpoint**: `[N/5]` 형식. `session-protocol.md` During 절 카운터.
- **Session Meta — Type 4택**: Implementation / Self-Improvement / Maintenance / Planning.
- **Purpose Alignment**: 기여 시나리오 + 이번 세션 범위. 세션 Type 이 Maintenance 인 경우 "Infrastructure" 로 명시.
- **Current Tasks**: 각 작업에 Completion Criteria 명시 (§2 참조 대상 항목).
- **Progress**: Completed / InProgress / Blocked 3분류.
- **Lessons Learned — [Protocol] 태그** (P3):
  - **프로토콜 관련 교훈이면** `[Protocol]` 태그 부착 (다음 세션의 프로토콜 개선 후보로 식별됨).
  - **일반 프로젝트 교훈이면** 태그 없이 기록.

### MICKEY-N-HANDOFF.md — 경량성 유지

- 세션 종료 시 확인 없이 생성 (다음 Mickey 를 위한 내부 문서).
- SESSION.md · auto_notes 와 **중복 기록 금지**: `Important Context` 는 그 두 곳에 없는 정보만.
- `Protocol Feedback` 은 **해당 세션에 프로토콜 이슈가 있었을 때만** 작성, 없으면 생략.

### PURPOSE-SCENARIO.md — 최우선 로드 대상

- 모든 판단의 최우선 기준 (REMEMBER #1).
- `Last Confirmed` 는 사용자 확인이 있었던 날짜 + Mickey 세션 번호 (예: `2026-07-07 · Mickey 34`).
- 재확인 시점: Continuing Session Step 2, 목적 정합성 체크에서 이탈 감지 시.

### DECISIONS.md — Decision Log 필드

- 각 항목은 아래 8필드 완비:
  - Date · Mickey · Topic · Options (+Pros/Cons/Time/Risk) · Chosen · Reasoning · Status
- Options 는 최소 2개 (`problem-solving.md` Step 6 과 정합).

### auto_notes/NOTES.md — 인덱스 역할만

- 본문은 토픽 파일(`commands.md`, `file-roles.md`, `error-fixes.md` 등).
- 50줄 상한 초과 시 카테고리별 파일 분리 (`knowledge-graph.md` 파일 크기 제한 참조).

### INDEX.md 계열 (common_knowledge / context_rule)

- Rule Map / Knowledge Map 형식: **트리거 → 파일 → 요약** 3열.
- 트리거는 키워드 또는 경로 패턴 모두 허용.
- 트리거가 없는 지식은 INDEX 에 등록하지 않으며, 등록되지 않은 파일은 T3b 로 로딩되지 않는다 (`knowledge-graph.md` T3 로딩 규칙 참조).
