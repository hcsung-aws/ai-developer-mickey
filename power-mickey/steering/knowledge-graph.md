---
inclusion: always
---

<!--
v17 T1 원문 대응 (원본: examples/ai-developer-mickey.json / dump: scripts/output/v17_prompt.md):
- KNOWLEDGE MANAGEMENT: L156~L242
  - 3-Tier Context Loading: L158~L175
  - 자동 메모리 (auto_notes/): L177~L202
  - 파일 크기 제한: L204~L218
  - 지식 저장소: L220~L228
  - 교훈 승격: L230~L232
  - 교훈 추출 기준: L234~L242
- 지식 그래프 접근 경로: v17 During Session L74~L76 함축 → 여기서 명시적 3경로로 확장
- Curator 호출 규약: session-protocol.md End Step 2 에서 위임

이식 원칙 (IMPROVEMENT-PLAN-v10 §8-b):
- T1.5 §N은 트리거만 명시. 상세는 ~/.kiro/mickey/extended-protocols.md 에서 pull.
- P3: 조건부 지시는 양쪽 분기 병기.
- 지식 그래프 노드(domain/entries/*, patterns/*)는 원본 유지. 접근 경로만 이식.
- Curator 로직은 ~/.kiro/mickey/domain/CURATOR-PROMPT.md 원본 유지. 호출 상세 규약은 knowledge-curator.md 로 이관(Phase 4-A). 여기는 리다이렉트만.
-->

# knowledge-graph

지식 저장·회수·승격의 규약. 세션마다 어떤 지식이 어디 있고 어떻게 접근하는지 정의한다. Curator 호출 진입점이기도 하다.

## 3-Tier Context Loading

context window 를 효율적으로 사용하기 위해 정보를 계층별로 로딩한다.

| Tier | 로딩 시점 | 내용 |
|------|----------|------|
| **T1** | 시스템 프롬프트 (항상) | 범용 원칙, 세션 프로토콜 (steering 6종) |
| **T1.5** | 세션 시작 | `~/.kiro/mickey/` 상세 실행 지침 (`extended-protocols.md`, `patterns/INDEX.md`, `domain/INDEX.md`, `domain/GRAPH.md`) |
| **T2** | 세션 시작 (자동) | `PURPOSE-SCENARIO.md`, `PROJECT-OVERVIEW.md`, 최신 `HANDOFF`, `project-context.md`, `adaptive.md` |
| **T3a** | 세션 시작 (지식 지도) | `common_knowledge/INDEX.md`, `context_rule/INDEX.md`, `auto_notes/NOTES.md` |
| **T3b** | 필요 시 (INDEX 트리거 매칭) | INDEX 에서 식별한 특정 파일만 |

### T3 로딩 규칙

- T3a(INDEX)를 세션 시작 시 읽어 "어떤 지식이 있는지" 파악.
- 작업 중 INDEX 의 트리거 조건에 **매칭 시** 해당 T3b 파일 로딩, **미매칭 시** 로딩 안 함 (INDEX 업데이트 우선).
- INDEX 트리거는 키워드 또는 경로 패턴 모두 가능 (예: `power-mickey/*` 파일 수정 시 매칭).

## 지식 그래프 진입 (`~/.kiro/mickey/`)

`~/.kiro/mickey/` **존재 시** T1.5 세션 시작 로딩으로 아래 4개 진입 인덱스를 확보한다 (`session-protocol.md` First/Continuing Step 1a). **미존재 시** 로딩 스킵 (첫 프로젝트).

- `patterns/INDEX.md` — 도메인 무관 접근법 패턴 (상한 7개)
- `domain/INDEX.md` — 도메인 지식 트리거 매핑
- `domain/GRAPH.md` — 노드 + 엣지 관계 맵
- `domain/PROFILE.md` — 사용자 성향·판단 기준

### 접근 경로 (그래프 원본은 유지, steering 은 경로만 정의)

1. **주 경로 (1홉)**: `GRAPH.md` Tags/Title 스캔 → Core 컬럼의 "언제" 힌트로 즉시 판단 → `domain/entries/` 해당 파일 상세.
2. **관계 탐색 (2홉)**: entry 내부의 Links 로 연결 entry 이동. 3홉 이상은 원칙적으로 지양.
3. **트리거 매칭**: INDEX 트리거 키워드가 현재 작업과 매칭 시 entry 직접 로딩. 매칭 없으면 로딩하지 않고 상위 GRAPH 로 되돌아감.

사용자가 "이전에 비슷한 거 했었나?" 요청 시 GRAPH.md 전체 스캔.

## 지식 저장소 4종

| 저장소 | 성격 | 확인 | 로딩 |
|--------|------|------|------|
| `auto_notes/` | 관찰한 사실 (서술적) | 세션 종료 시 일괄 확인 | T3a (`NOTES.md`) |
| `context_rule/adaptive.md` | 적응형 규칙 (Curator 직접 수정) | 세션 종료 시 git diff 검증 (첫 5회) | T2 |
| `context_rule/` | 검증된 규칙 (규범적, 프로젝트 특화) | 즉시 사용자 확인 | T3a→T3b |
| `common_knowledge/` | 범용 패턴 (규범적, 프로젝트 무관) | 즉시 사용자 확인 | T3a→T3b |

### auto_notes/ 자동 기록 대상 (사용자 확인 불필요, REMEMBER #5 예외)

- 빌드/테스트/린트 커맨드
- 파일 경로와 역할
- 도구 버전, 환경 상세
- 검증 완료된 에러 해결법
- API 엔드포인트와 용도

구조: `NOTES.md` = 인덱스. 토픽 파일 = `commands.md`, `file-roles.md`, `error-fixes.md` 등. `NOTES.md` 는 인덱스 역할만 유지 (본문은 토픽 파일).

### context_rule/ vs common_knowledge/ 분기 판단

- `context_rule/`: 반복 실패 방지, 환경 설정, 트러블슈팅, 알려진 이슈. **프로젝트 특화**.
- `common_knowledge/`: 기술 비교, 아키텍처 패턴, 구현 패턴, 범용 솔루션. **프로젝트 무관**.
- 승격 판단: 같은 관찰이 여러 프로젝트에서 반복되면 → §12 (Global Knowledge) 참조. 단일 프로젝트에 한정된 관찰이면 §12 pull 불필요.

### adaptive.md 관련 참고

`context_rule/adaptive.md` 는 Curator 가 직접 수정하는 유일한 규범 파일이다. 규약 자체는 Curator lifecycle 의 일부이므로 → §17 (Knowledge Lifecycle) 참조. (구 §8 Adaptive Rules 는 §17 로 흡수됨.)

## 파일 크기 제한 (이중 가드)

세션 시작 시 로딩되는 파일은 줄 수 + 항목 수 이중 가드를 준수한다.

| 파일 | 줄 수 제한 | 항목 수 제한 |
|------|-----------|-------------|
| T2 파일 (각각) | 50줄 (`project-context.md` 만 80줄) | 핵심 섹션 최대 5개 항목 |
| T3a 인덱스 (각각) | 50줄 | — |
| `auto_notes/NOTES.md` | 50줄 | — |

**초과 시** 아래 조치, **초과 안 하면** 유지:

- 축약, 오래된 항목 승격/제거, 상세 내용 분리.
- `project-context.md` Lessons Learned: 최대 5개, 오래된 것은 `context_rule/` 로 승격.
- `INDEX.md`: 유사 트리거 통합.
- 파일 수정 시 줄 수 확인 → 초과 임박하면 즉시 정리.

## 교훈 추출 · 승격

### 추출 기준 (아래 중 하나 이상 부합 시 추출, 모두 미부합이면 세션 종료까지 추출 시도 안 함)

- 같은 실수 2번 이상 반복
- 사용자가 누락 지적
- 예상과 다른 결과
- 새 패턴/안티패턴 발견
- 효과적 해결책 발견

### 승격 절차

사용자가 "교훈 승격" 또는 "패턴 정리" 요청 시, 또는 Session End Step 2 에서 Curator 호출 (`session-protocol.md` 참조). 상세 규약은 아래 "Curator 호출 규약" 참조.

## Curator 호출 (상세 규약은 이관됨)

Curator 호출 계약(입력·R/G/S 분기·자동승인 경로·5회 검증·응답 프로토콜)의 상세는 `knowledge-curator.md` 로 이관되었다. 이 파일은 지식 그래프 접근 규약(상시)만 담고, Curator 실행 규약은 세션 종료 시에만 필요하므로 on-demand steering 으로 분리한다.

- **세션 종료 시** → `knowledge-curator.md` 를 `readSteering` 로 pull + `~/.kiro/mickey/domain/CURATOR-PROMPT.md` 정본 절차 pull. → §17 (Knowledge Lifecycle) 참조.
- **세션 종료가 아닐 때** → Curator 규약 pull 불필요. 그래프 접근은 위 규약으로 충분.

호출 트리거는 `session-protocol.md` Session End Step 2, 응답 처리는 End Step 3 에 정의.

## Activity Metrics · 포스트모템 연동

- 5/5 Checkpoint 도달 시 또는 포스트모템 트리거 시 → §18 (Activity Metrics) 참조. 평상 시에는 §18 pull 불필요.
- 포스트모템 트리거(10세션 경과 또는 3개월 잠복) → §9 참조. `session-protocol.md` Continuing Step 1b 에서 감지.
