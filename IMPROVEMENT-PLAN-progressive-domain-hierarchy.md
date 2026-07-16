# IMPROVEMENT-PLAN: Progressive Domain Knowledge Hierarchy

> **위상**: Mickey 프로토콜 개선 계획서
> **작성 배경**: `anjin-llm-scenario-poc` Mickey 1 세션(2026-07-08~09)에서 Unity·Anjin 관련 domain 지식 승격 후보 2건이 발생하며, 향후 특정 도메인에 한정된 지식이 축적될 때 flat `entries/`의 스캔 부담을 어떻게 완화할지 논의된 결과.
> **작성자 소속 세션**: `anjin-llm-scenario-poc` Mickey 1 (2026-07-09)
> **실행 대상 프로젝트**: `ai-developer-mickey` (다음 Mickey 세션이 검토 후 실행)

## 1. 배경과 계기

### 1-1. 발단
`anjin-llm-scenario-poc` Mickey 1 세션에서 두 domain 지식이 Curator staging에 pre-staged 되었다:
- `upm-testables-scene-reuse` — UPM 패키지의 씬을 파일 복사 없이 `testables` + 정확 경로로 참조
- `editor-script-asset-generation` — ScriptableObject asset을 Editor 스크립트로 프로그래매틱 생성

두 지식 모두 **Unity 엔진에 한정된 지식**이라 다른 도메인 프로젝트에서는 무의미. 즉시 flat `~/.kiro/mickey/domain/entries/`에 배치할 수도 있으나, 사용자가 "특정 도메인 지식은 계층화된 구조로 정돈되면 좋겠다"는 방향 제기.

### 1-2. 현재 상태 진단
- `~/.kiro/mickey/domain/entries/`에 flat 60개 축적. **상한 없음** (patterns/ 7개, REMEMBER 12개 상한과 대조)
- `domain/GRAPH.md`가 60개 노드 flat 나열. 향후 계속 증가 시 스캔 부담 예상
- 계층화의 필요성은 CURATOR-PROMPT.md 주의사항에 이미 힌트 있음 ("GRAPH.md 100줄 초과 시 카테고리별 서브그래프 분리 필요") — 다만 명시된 절차 없음

### 1-3. 사용자 요구사항 (최종 확정)
1. **당장 카테고리 신설 안 함** — 오늘 승격 후보 2개는 기존 방식(flat entries/)에 배치. 즉시 실행 강제 아님
2. **Mickey 동작 지침으로 프로토콜화** — 향후 자연 성장 과정에서 계층화가 트리거 기반으로 발생하도록
3. **3단계 성장 규칙**: Step 1 지식 추가 → Step 2 파일 분할 → Step 3 카테고리 이관
4. **링크 안정성 유지** — 파일 경로 하드코딩 금지, 노드 ID 기반 링크로 이동 시 자동 유지

## 2. 3단계 프로토콜 (핵심 제안)

### Step 1 — 지식 추가 (현재 방식 유지)

**트리거**: Curator가 승격 대상 식별

**절차**:
1. `entries/{id}.md` 생성 (flat 배치)
2. `GRAPH.md` Nodes 표에 새 행 추가 — **`Path` 컬럼 신설** (기존 60개는 순차 채움, 신규는 즉시 채움)
3. `INDEX.md` 트리거 표에 새 행 추가
4. Entry Links §에 관계 등록 — **노드 ID만 사용**, 파일 경로 하드코딩 금지

**변경점**: 기존 방식에 `Path` 컬럼만 추가. 나머지는 그대로.

### Step 2 — 파일 분할 (지식 응집성 유지)

**트리거**: 단일 `entries/{id}.md`가 LINE 상한 초과

**LINE 기준** (권장):
- 소프트 상한: **300줄** — 감시 대상
- 하드 상한: **500줄** — 분할 강력 권장
- **판단은 논리 응집성 우선**: 300줄이라도 하나의 원칙이면 분할 불필요, 200줄이라도 두 원칙이 혼재면 분할 검토

**분할 절차**:
1. 파일 내 논리 경계 식별 (섹션·태그·다른 결정 맥락)
2. 각 논리 단위를 새 entry 파일로 분리 (`entries/{new-id-1}.md`, `entries/{new-id-2}.md`)
3. GRAPH.md의 기존 노드 행 제거 → 새 노드 행 2개+ 추가
4. Edges 중 원본 노드 참조 → 분할된 노드 중 관련 노드로 재지정
5. 다른 entry들의 Links §에서 원본 노드 ID 참조 검색 → 분할 후 적절한 노드 ID로 재지정
6. INDEX.md 트리거 표 갱신

**사용자 확인 필수** (자동 아님)

### Step 3 — 카테고리 계층화 (재편)

**트리거**: `GRAPH.md`의 Nodes 표에서 동일 태그 클러스터가 **5개 노드 이상** 축적

**클러스터 판정 예시**:
- `unity`, `unreal`, `upm`, `editor-script` 등이 5개+ 노드에서 반복 → **game-engine 카테고리 후보**
- `aws`, `bedrock`, `agentcore`, `cdk` 등이 5개+ → **cloud/aws 카테고리 후보**
- `terraform`, `hcl`, `tfstate` 등이 5개+ → **iac/terraform 카테고리 후보**

**계층화 절차** (사용자 확인 필수):
1. **디렉토리 신설**: `entries/{category}/` 생성 (필요 시 세분화 `entries/{category}/{sub}/`)
2. **파일 이동**: 관련 md 파일들을 `entries/{category}/` 아래로 이동
3. **하위 GRAPH 생성**: `entries/{category}/GRAPH.md` 신설
   - 이동된 노드들의 Nodes 행 복제 (Path 컬럼은 새 위치로 갱신)
   - 이동된 노드들 간의 Edges 복제
4. **상위 GRAPH 갱신**:
   - 이동된 노드 행 제거
   - 카테고리 anchor 노드 한 행 추가: `{category} [ANCHOR] | ... | Path=entries/{category}/GRAPH.md`
   - Cross-Category Edges 유지: 이동된 노드가 flat 노드와 관계 있으면 anchor→flat 형태로 갱신
5. **링크 재검증**: 전체 GRAPH들과 entry Links §에서 이동된 노드 ID 참조를 스캔 → 무결성 확인
6. **INDEX.md 갱신**: Anchors § 추가 (없으면 신설), 이동된 트리거 삭제 + 카테고리 트리거 신설

## 3. 링크 정책 (계층화 대비 안정성)

### 규칙 1: Links §는 **노드 ID만** 사용
```markdown
## Links
- phase-based-decomposition | applies-to | Phase 분해도 이 원칙 적용
- welc-test-harness | similar-to | 검증 기반 진행 공통
```
**금지**: `../entries/phase-based-decomposition.md` 같은 파일 경로 하드코딩

### 규칙 2: 실 경로 조회는 항상 GRAPH.md의 Path 필드
- 노드 ID로 노드 찾기 → Path 필드 확인 → 파일 접근
- 파일 이동 시 Path 컬럼만 갱신 → 링크 자동 유지

### 규칙 3: 계층화 시 Path 필드 일괄 갱신
- Step 3 진행 시 이동된 노드의 Path를 새 위치로 갱신
- 다른 파일에서 그 노드 ID를 참조해도 새 Path 조회로 자연 해결

### 규칙 4 (선택 도입): 카테고리 힌트 노드 ID
- 필요 시 노드 ID에 카테고리 접두 도입: `game-engine.upm-testables-scene-reuse`
- 이동해도 ID 자체가 카테고리를 표현 → path 조회 실패 시에도 유추 가능
- 기존 60개 flat ID는 그대로 유지 (파괴 변경 회피). 카테고리 이관 시에만 신규 규칙 적용 검토

## 4. Mickey 동작 조정

### 4-1. 세션 시작 (Continuing Session Step 1b 엔트로피 체크 확장)

두 항목 신규 추가:
- **파일 크기 스캔**: `entries/*.md`에서 500줄 초과 파일 목록 → 있으면 사용자에게 Step 2 제안
- **카테고리 클러스터 스캔**: GRAPH.md Nodes 표의 Tags 클러스터링 → 5개+ 노드 클러스터 발견 시 사용자에게 Step 3 제안

두 항목 모두 발견 시에도 즉시 재편 강제 아님. 사용자에게 알리고 이번 세션 종료 시 or 별도 세션에서 처리.

### 4-2. 세션 종료 (Curator 호출)

Curator가 승격 시:
- 승격 대상의 Tags를 GRAPH.md의 기존 클러스터와 매칭
- 이미 카테고리 존재하면 자동으로 카테고리 내부에 배치 (예: unity tag → `entries/game-engine/unity/`)
- 카테고리 없으면 flat entries/ 배치. 5개+ 클러스터 예상되면 "카테고리 신설 제안" Pre-staged 생성

## 5. `CURATOR-PROMPT.md` 갱신 지점

라우팅 판단표에 다음 컬럼/절차 추가:

| 대상 | 판단 | 카테고리 처리 |
|------|------|-------------|
| entries/ 신규 승격 | 다른 프로젝트 재사용 | 기존 카테고리 매칭 시 그 안으로. 미매칭이면 flat |
| Step 2 파일 분할 | 500줄 초과 or 논리 혼재 | 사용자 확인 후 분할 |
| Step 3 계층화 | Tags 클러스터 5개+ | 사용자 확인 후 카테고리 신설·이관·GRAPH 재구성 |

Entry 형식에 필드 추가 (카테고리 소속 entry만):
```markdown
## Category (선택)
game-engine/unity
```

주의사항 갱신:
- 기존 "GRAPH.md 100줄 초과 시 카테고리별 서브그래프 분리 필요"를 본 프로토콜의 Step 3로 대체

## 6. `domain/GRAPH.md` 구조 (Step 1 즉시 적용분)

Nodes 표에 **Path 컬럼 도입**:

```markdown
## Nodes
| ID | Title | Tags | Core | Path |
|----|-------|------|------|------|
| phase-based-decomposition | ... | ... | ... | entries/phase-based-decomposition.md |
| welc-test-harness | ... | ... | ... | entries/welc-test-harness.md |
| ... (기존 60개, Path 컬럼 순차 채움 or 신규 승격 때 함께 정정) |
```

Step 3 발생 후 Nodes 표에서 anchor 표기 예:
```markdown
| game-engine [ANCHOR] | 게임 엔진 통합 지식 | unity, unreal, upm, editor | 하위 GRAPH: 5 entries | entries/game-engine/GRAPH.md |
```

## 7. 실행 순서 (다음 Mickey가 진행)

### 검토 단계 (Session Start)
1. 본 계획서 정독
2. `~/.kiro/mickey/domain/` 현재 상태 재확인 (60개 flat, GRAPH.md 크기, CURATOR-PROMPT.md 기존 문구)
3. 사용자와 세부 사항 확정:
   - LINE 상한 300/500 or 다른 수치
   - 카테고리 클러스터 5개 or 다른 수치
   - Categorization Rule § 도입 시점 (지금 vs 첫 카테고리 도입 시)

### 실행 단계
4. `~/.kiro/mickey/domain/CURATOR-PROMPT.md` 갱신 (§4 Step 1/2/3 정의 추가)
5. `~/.kiro/mickey/extended-protocols.md` 갱신 (§"점진적 지식 그래프 계층화" 신설 + 엔트로피 체크에 §19처럼 추가)
6. `~/.kiro/mickey/domain/GRAPH.md` 갱신 (Path 컬럼 신설. 기존 60개는 즉시 or 점진 채움)
7. `~/.kiro/mickey/domain/INDEX.md` 갱신 (원칙 명시, 필요 시 Anchors § 신설 유보)

### 계기 프로젝트 정리
8. `anjin-llm-scenario-poc/_curator-staging/`에 2건의 Pre-staged 파일 존재:
   - `upm-testables-scene-reuse.md`
   - `editor-script-asset-generation.md`
9. 프로토콜 확정 후 원 프로젝트 Mickey에게 회신하거나, 직접 `~/.kiro/mickey/domain/entries/`로 이동 (Step 1 방식). 이관 시 프로젝트의 `common_knowledge/INDEX.md`에 Domain Backlink도 추가

## 8. 향후 시나리오 (예시)

- **T=1 (지금 시점)**: Unity 관련 2개 → flat entries/ 배치
- **T=N (Unity 3~4개)**: Curator가 세션 종료 시 "unity tag 클러스터 3개+ 감지" 알림 (5개 미달로 강제 아님)
- **T=M (Unity 5개+)**: Step 3 트리거 → 사용자 확인 → `entries/game-engine/unity/` 신설 → 이관
- **동시 다발 시나리오**: 기존 flat 60개 중 `aws-*` 이미 8개, `terraform-*` 5개 감지되어 있음. 자연 재편 후보 대기

## 9. 결정 대기 항목 (다음 Mickey가 사용자와 확정)

1. **LINE 상한**: 소프트 300 / 하드 500 확정 여부. 대안: 200/400, 400/750
2. **카테고리 클러스터 임계값**: 5개 확정 여부. 대안: 3개(조기 재편), 7개(더 축적 후)
3. **Categorization Rule § 도입 시점**:
   - (a) 지금 `domain/INDEX.md`에 지침만 명시 (미래 참조용)
   - (b) 실제 첫 카테고리 도입 시 명시
4. **기존 60개 flat entries의 Path 컬럼 채움 방식**:
   - (α) Step 1 프로토콜 도입 즉시 일괄 채움 (60행 반복 작업)
   - (β) 점진적 — 각 노드가 다음 편집될 때 채움 + 신규 승격은 즉시

## 10. 자기 완결적 참조 자료

### 계기 세션 문서 (필요 시 참조)
- `anjin-llm-scenario-poc/MICKEY-1-SESSION.md` — 계기 세션 요약
- `anjin-llm-scenario-poc/MICKEY-1-HANDOFF.md` — Mickey 2 진입 가이드
- `anjin-llm-scenario-poc/session_history/mickey-1-session-log.md` — 라운드별 대화 로그
- `anjin-llm-scenario-poc/_curator-staging/upm-testables-scene-reuse.md` — 승격 후보 1
- `anjin-llm-scenario-poc/_curator-staging/editor-script-asset-generation.md` — 승격 후보 2

### Mickey 시스템 관련 참조 (본 계획서 실행 시 이해 필요)
- `~/.kiro/mickey/domain/CURATOR-PROMPT.md` — 현행 Curator 판정 프롬프트
- `~/.kiro/mickey/domain/INDEX.md` — 현행 Domain Map + 접근 경로 §
- `~/.kiro/mickey/domain/GRAPH.md` — 현행 flat 60개 노드
- `~/.kiro/mickey/domain/PROFILE.md` — 사용자 성향 (판단 근거)
- `~/.kiro/mickey/extended-protocols.md` — Mickey 확장 프로토콜 (§19 코드 분석 도구 통합 등)

## Last Updated
2026-07-09 (anjin-llm-scenario-poc Mickey 1 세션 종료 직전)
