---
inclusion: manual
---

<!--
이식 원본:
- v2 Curator agent: examples/knowledge-curator.json (prompt 필드)
- 정본 그래프 노드: ~/.kiro/mickey/domain/CURATOR-PROMPT.md
- 이 둘은 내용 동일. CURATOR-PROMPT.md 가 정본이며 세대 관리 대상.

이식 원칙 (IMPROVEMENT-PLAN-v10 §8-b, Phase 4-A B-A 조합):
- inclusion: manual — 상시 로드 금지. 세션 종료 시 readSteering 로만 pull (progressive disclosure).
- CURATOR-PROMPT.md 원문은 이식 금지(그래프 노드 원칙). 여기는 호출 계약(입력·출력·5회 검증)만 요약.
- 상세 실행 절차(0~5단계·entry 형식·staging 파일 형식)는 CURATOR-PROMPT.md 를 pull 하여 사용.
- knowledge-graph.md 의 기존 "Curator 호출 규약" 은 이 파일로 이관됨. knowledge-graph.md 는 리다이렉트만 유지.
- P3: 조건부 지시는 양쪽 분기 병기.
-->

# knowledge-curator

Knowledge Curator 호출 진입점. **상시 로드되지 않는다.** 세션 종료("세션 정리") 시 `session-protocol.md` End Step 2 에서 이 steering 을 `readSteering` 로 pull 하여 사용한다. 평상시(세션 진행 중)에는 pull 하지 않는다.

## 활성 시점 (양쪽 분기)

- **세션 종료 요청 시** → 이 파일 pull + 정본 절차 pull + Curator 실행.
- **세션 종료가 아닐 때** → pull 하지 않음. 지식 그래프 접근은 `knowledge-graph.md` 규약으로 충분.

## 정본 절차 위치 (원본 유지, 이식 금지)

Curator 의 상세 실행 절차는 그래프 노드에 있다. **필요 시 pull 한다.**

- `~/.kiro/mickey/domain/CURATOR-PROMPT.md` — 0~5단계 실행 절차, entry 형식, staging 파일 형식, 출력 형식의 **정본**.
- 이 steering 은 그 절차를 복제하지 않는다. 호출 계약(입력·분기·자동승인·검증·응답)만 요약한다.
- CURATOR-PROMPT.md **존재 시** 그것을 pull 하여 실행. **미존재 시**(공용 서고 미배치) 아래 요약 계약만으로 축약 실행하고 사용자에게 서고 부재를 알린다.

## 입력 계약

Curator 실행 시 전달하는 것:

1. 대상 `MICKEY-N-SESSION.md` 내용 (결정·교훈·진행 상황).
2. 프로젝트 루트 경로.
3. (선택) 사용자 지시 문구 — "교훈 승격", "패턴 정리" 등. **문구 있으면** 해당 의도 우선, **없으면** 세션 맥락 전반을 스캔.

## 라우팅 분기 (R / G / S)

식별된 각 항목을 세 갈래로 분류한다.

| 분기 | 조건 | 동작 |
|------|------|------|
| **R (Reject)** | 프로젝트 특화 사실·단순 작업 기록·일회성 디버깅·기존 내용 반복 | 저장 안 함. 이유만 회신 |
| **G (Graduate)** | 크로스 프로젝트 가치(`domain/`) 또는 프로젝트 반복 패턴(`adaptive.md`, 2회+) | **직접 수정** (자동 승인 경로 내) |
| **S (Stage)** | `common_knowledge/`·`context_rule/`·`patterns/`·REMEMBER 승격 후보 | `_curator-staging/` 에 **Pre-staged 초안** 작성 |

`~/.kiro/mickey/domain/PROFILE.md` 의 Decision Style·Relationship Preferences 를 분기 판단 입력으로 참조한다. PROFILE **존재 시** 반영, **미존재 시** 기본 보수 판단(precision > recall).

## 자동 승인 경로 (fs_write 마찰 최소화)

아래 경로만 확인 없이 직접 수정한다. 그 외 경로는 반드시 staging 을 거친다.

- `~/.kiro/mickey/domain/**`
- `**/context_rule/adaptive.md`
- `**/_curator-staging/**`
- `common_knowledge/INDEX.md`·`context_rule/INDEX.md` 의 Domain Links 섹션 (역방향 링크 한정)

거부 경로(`.git/`, `node_modules/`, `.venv/`, `credentials*`, `.env*`, `*.key`, `*.pem`)는 어떤 경우에도 쓰지 않는다.

## Pre-staged Apply 패턴 (S 분기)

staging 위치는 대상 영역으로 갈린다 (상세 판정은 CURATOR-PROMPT.md §4).

- `common_knowledge/`·`context_rule/` → 프로젝트 staging. 루트에 `MICKEY-*-SESSION.md` **직접 있으면** `{프로젝트}/_curator-staging/`, `.kiro/mickey/` **하위에 있으면** `{프로젝트}/.kiro/_curator-staging/`.
- `patterns/`·REMEMBER (글로벌) → `~/.kiro/mickey/_curator-staging/`.
- staging 디렉토리 **없으면** 자동 생성(저위험), **있으면** 재사용. 파일명 충돌 시 `-YYYYMMDD-HHMM` suffix.

staging 파일은 정식 위치와 동일 형식으로 작성한다 — 머지 시 단순 이동만으로 끝나야 한다.

## 검증 기간 (5회 가드)

- **첫 5회 호출 동안** → 실행 후 git diff 결과를 사용자에게 자동 보고 (의도 외 변경 가드).
- **6회부터** → 정식 운영. diff 보고 축약 가능.

## 출력·응답 프로토콜

Curator 출력 형식은 CURATOR-PROMPT.md "출력 형식" 을 따른다. Mickey 는 결과를 받아 사용자에게 단일 응답을 요청한다.

| 사용자 응답 | Mickey 동작 |
|------------|------------|
| "전체" | 모든 staging 을 본문 명시 절차대로 정식 위치로 이동 + staging 청소 |
| "1,3" 등 번호 | 해당 번호만 이동 + 나머지 폐기 |
| "없음" | 모든 staging 폐기 |
| "보류" | staging 유지 (다음 세션 시작 시 dangling 으로 재제시) |

dangling 항목이 3세션 이상 보류되면 "자동 폐기 후보" 로 알린 후 폐기.

## 연결 참조

- `session-protocol.md` End Step 2 — Curator 호출 트리거.
- `knowledge-graph.md` — 지식 그래프 접근 규약(상시). Curator 상세 규약은 이 파일로 이관됨.
- `~/.kiro/mickey/extended-protocols.md` §17 (Knowledge Lifecycle) — 심층 절차. §18 (Activity Metrics)·§12 (Global Knowledge) 는 승격 판단 시 pull.
