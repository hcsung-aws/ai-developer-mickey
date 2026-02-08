# 세션 관리 프로토콜

## 세션 시작 시
1. Hook이 자동으로 이전 세션 아카이브 및 새 세션 로그 생성
2. `.kiro/sessions/CURRENT.md` 확인
3. `.kiro/sessions/HANDOFF.md` 확인 (있으면)
4. 이전 컨텍스트 요약 후 사용자에게 보고
5. Memory Graph 있으면 `recall_memories`로 프로젝트 기억 조회

## 세션 중
- 주요 작업 완료 시 CURRENT.md 업데이트
- 중요 결정 시 기록
- 수정한 파일 목록 유지

## /compact 후 새 세션 시작 시
1. agentSpawn hook이 자동으로 세션 전환 처리
2. /compact된 context에서 이전 작업 내용 확인
3. HANDOFF.md 참고
4. 새 세션 로그에 목표 설정 후 작업 계속

## Context Window Management

| 사용률 | 행동 |
|--------|------|
| **50%** | 세션 로그 정리 제안 (완료 작업 요약, 시행착오 제거, 결과/결정/이슈만 유지) |
| **70%** | 현재 작업 완료 후 새 세션 권장, 핸드오프 준비 |
| **90%** | 즉시 새 세션, 핸드오프 생성 |

## 3-Tier Context Loading

| Tier | 매체 | 로딩 | 내용 |
|------|------|------|------|
| T1 | mickey-core.md (always steering) | 자동 | 핵심 원칙 |
| T2 | Memory Graph | `recall_memories` | 프로젝트 컨텍스트, 결정, 이슈 |
| T3 | steering + project-lessons.md | 맥락별 | 상세 프로토콜, 교훈 |

- T2: 세션 시작 시 recall로 필요한 컨텍스트 확보 (파일 읽기 최소화)
- T3: 해당 상황의 steering만 로딩 (전부 읽지 않음)

## Document Schema (경량화)

Mickey가 관리하는 핵심 파일:

| 파일 | 역할 |
|------|------|
| `.kiro/sessions/CURRENT.md` | 현재 세션 로그 (Hook 자동 생성) |
| `.kiro/sessions/HANDOFF.md` | 세션 간 인수인계 |
| `.kiro/steering/project-lessons.md` | 프로젝트 교훈 (사람이 읽을 수 있는 형태) |

나머지 정보 (프로젝트 개요, 환경, 결정 등)는 Memory Graph에 저장하여 recall로 조회.

## 세션 로그 형식 (CURRENT.md)

```markdown
# Session Log

## 목표
[세션 목표]

## 진행 상황
- [x] 완료 작업
- [ ] 진행 중

## 주요 결정
- [결정 내용과 이유]

## 수정 파일
- [파일 목록]

## 다음 단계
- [다음 작업]
```

## 핸드오프 형식 (HANDOFF.md)

```markdown
# Handoff

## 현재 상태
[완료된 것, 진행 중인 것]

## 즉시 다음 단계
1. [Step 1]
2. [Step 2]

## 중요 컨텍스트
- [알아야 할 것들]

## 유용한 명령어
```bash
[자주 사용한 명령어]
```
```
