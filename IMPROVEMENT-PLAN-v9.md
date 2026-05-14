# IMPROVEMENT-PLAN-v9: 도메인 지식 중심 + Kiro Skill 통합

> 분석 근거: `POSTMORTEM-2026-05-14.md` (76세션 활용도 측정 + 외부 트렌드 비교)
> 작성: Mickey 20 (2026-05-14)
> Status: 사용자 승인 → Phase 1부터 진행

## 배경 (1줄 요약)

v8.1까지 누적된 지식 구조가 **자기 개선 외 활용 0건**임을 확인 (POSTMORTEM 참조). 이를 **3-Tier 단순화 + 도메인 지식 중심 + Kiro Skill 통합**의 점진적 진화 루프로 재설계한다.

## 핵심 변화 요약

| 영역 | 기존 (v8.1) | 신규 (v9) |
|------|------------|-----------|
| 지식 분류 | 4종+ 분산 (auto_notes/common/context_rule/patterns/domain) | **3-Tier** (R/G/S) |
| 지식 본체 위치 | 프로젝트 분산 | **글로벌 `~/.kiro/mickey/domain/`** |
| 프로젝트 내부 | 일반 + 특화 혼재 | **완전 특화 사실만** (git/환경 등) |
| 큐레이션 | Curator subagent (호출 0회) | **knowledge-organization Skill** (5/5 카운터 자동 호출) |
| 외부 표준 통합 | 검토 안 함 | **Kiro Skill 위치(~/.kiro/skills/) 활용**, CLAUDE.md/AGENTS.md는 배제 (Mickey는 Kiro 한정) |
| 승격 결과 | 본문 잔존 (중복) | **승격 시 원본은 stub만** (참조 정보) |

---

## 1. 새 PURPOSE-SCENARIO 초안

### Ultimate Purpose (재정의)

**프로젝트 진행 중 누적되는 사용자의 결정/판단/특화 경험을 점진적으로 구조화하여, 도메인 지식 → Kiro Skill로 진화시키는 자기 강화 루프를 만든다.** Kiro CLI/IDE 생태계 안에서, 사용자가 매번 같은 판단을 반복하지 않도록 최종 활용 단계(Skill, REMEMBER)에서는 자동으로 적용된다.

### Usage Scenarios

1. **소프트웨어 개발 / 인프라 운영 / 일반 작업**: 세션 진행 중 결정과 학습이 누적 → 분석/구조화 → 도메인 지식 그래프 → 성숙 시 Skill/REMEMBER로 승격 → 이후 자동 적용
2. **Mickey 자체 개선**: AI 기술 발전 + 외부 트렌드 분석 → 본 진화 루프 자체에 반영

### Acceptance Criteria

"충분"은 없음. 다만 진화 루프의 **건강 지표**를 측정 가능하게 함:
- 매 N세션마다 활용도 메트릭 자동 측정 (저장소별 참조율)
- knowledge-organization Skill 호출 빈도 + 승격 결과
- < 10% 활용도 항목은 분기 검토 대상

### Last Updated
2026-05-14 (Mickey 20)

---

## 2. 새 지식 구조

### 글로벌 (`~/.kiro/mickey/`)
```
extended-protocols.md          R (T1.5)
machine-env.md                 머신 특화
domain/                        G 본체 ← 일반화 가능한 모든 지식의 종착지
├── INDEX.md                   계층화 (작업유형 → 도메인 → 키워드)
├── GRAPH.md                   관계 맵 (Nodes + Edges)
├── PROFILE.md                 사용자 성향 (Skill 분기 판단 입력)
└── entries/*.md               개별 지식
```

### 글로벌 Skills (`~/.kiro/skills/`)
```
knowledge-organization/SKILL.md    ← 자기 정리 Skill (5/5 자동 호출)
<기타-skill>/SKILL.md              ← 도메인 지식에서 승격된 동작 절차
```

### 프로젝트 (특화 사실만, 최소화)
```
PURPOSE-SCENARIO / PROJECT-OVERVIEW / ENVIRONMENT / DECISIONS / FILE-STRUCTURE
context_rule/
├── project-context.md         좁게: git/커밋/특화 환경
└── INDEX.md                   간소: 글로벌 domain backlink 위주
auto_notes/                    G의 신선한 입구
MICKEY-N-SESSION.md / HANDOFF.md
.kiro/skills/<project-skill>/  프로젝트 특화 Skill (필요 시)

(deprecated 점진 폐기)
common_knowledge/              ← 새 추가 금지, 기존은 stub 변환
context_rule/adaptive.md       ← 분기 판단 후 R/G/S 흡수 또는 폐기
```

---

## 3. Tier 정의 + 라이프사이클

### Tier 정의

| Tier | 사용자 정의 | 위치 | 활용 |
|------|------------|------|------|
| **R** (Rule) | 판단/추론 방식 — "내가 생각하는 것처럼 해야 하는 것" | T1 REMEMBER, T1.5 핵심 | 시스템 프롬프트 내재화, 상시 |
| **G** (Knowledge) | 작업 중 알게 된 지식 + 프로젝트 구조 — "단순 지식" | `auto_notes/` (입구) → 글로벌 `domain/entries` + `GRAPH.md` (본체) | INDEX 계층화 매칭 + GRAPH backlink로 passive 노출 |
| **S** (Skill) | R+G를 활용한 동작 — "구체적인 방법" | `~/.kiro/skills/` 또는 프로젝트 `.kiro/skills/` | Kiro Skill 트리거 매칭 호출 |

### 라이프사이클

```
세션 발견 → auto_notes (G 입구, 프로젝트 내)
         ↓ knowledge-organization Skill (5/5 카운터 시 자동 호출)
         ↓ 분기 판단 (아래 §4 기준)
         ├─ 프로젝트 완전 특화 사실 → context_rule/project-context.md
         ├─ 일반화 가능한 도메인 지식 → 글로벌 domain/entries (대다수 케이스)
         ├─ 판단/추론 방식 → R 승격 (REMEMBER/T1.5)
         └─ 동작 절차 → S 승격 (Kiro Skill)

승격 결과: 본문 흡수 + 원본은 stub (참조 정보만)
미승격: G에 영구 거주 (backlink로 passive 노출)
```

### Stub 형식

```markdown
# (이전: WELC Test Harness)

→ **R로 승격**: T1.5 §15 / REMEMBER #9
또는
→ **Skill로 승격**: `~/.kiro/skills/welc-test-harness/`
또는
→ **글로벌 domain 이전**: `~/.kiro/mickey/domain/entries/welc-test-harness.md`

이전일: 2026-XX-XX (Mickey N)
트리거 (참조용): 리팩토링, harness, 레거시 코드
```

---

## 4. knowledge-organization Skill 명세

### 위치
`~/.kiro/skills/knowledge-organization/SKILL.md`

### Frontmatter
```yaml
---
name: knowledge-organization
description: Mickey 5/5 체크포인트 도달 시 또는 사용자가 "지식 정리"/"포스트모템"을 요청할 때 호출. 누적된 auto_notes 및 SESSION 학습을 R/G/S Tier로 분기 판단하여 승격 후보를 제안한다.
---
```

### 입력 (Mickey가 전달)
1. 직전 5세션의 SESSION.md + HANDOFF.md
2. `auto_notes/` 전체
3. 글로벌 `domain/INDEX.md` + `GRAPH.md` + `PROFILE.md`
4. (있다면) `common_knowledge/`, `context_rule/adaptive.md` 잔존분

### 분기 판단 기준 (Skill 내부 로직)

| 신호 | 분류 | 위치 |
|------|------|------|
| "~~하는 방식이 좋다", "이렇게 판단해야 한다", 메타 원칙 | **R** | REMEMBER 또는 T1.5 |
| 사실, 구조, 환경, 명령, 패턴 (다른 프로젝트도 적용 가능) | **G (글로벌)** | `~/.kiro/mickey/domain/entries` |
| 사실인데 이 프로젝트에만 해당 (git URL, 커밋 절차 등) | **G (프로젝트)** | `context_rule/project-context.md` |
| "이 작업은 이 단계로", 도구 호출 시퀀스, 절차 | **S** | Kiro Skill (글로벌 또는 프로젝트) |
| 위 어디에도 강하게 매칭되지 않음 | **보류** | auto_notes에 유지, 다음 호출에 재검토 |

### 출력 (Skill이 반환)
1. **분기 후보 목록** (각 항목: Tier, 제안 위치, 근거 1줄)
2. **승격 시 자동 작업 내역**: SKILL.md 또는 entries/*.md 또는 REMEMBER 항목 초안
3. **Stub 변환 대상**: 원본 위치 + stub 내용
4. **INDEX/GRAPH 갱신 필요 항목**: backlink 추가, 키워드 확장

### 호출 흐름

```
Mickey: 체크포인트 5/5 도달
  ↓ "체크포인트 5회 도달. 정리 후 /clear?"
  ↓ 사용자 OK
  ↓
Mickey: knowledge-organization Skill 호출 (입력 전달)
  ↓
Skill: 분기 판단 + 후보 목록 + 자동 작업 내역 반환
  ↓
Mickey: 사용자에게 후보 목록 제시 → 항목별 승인/거부/수정
  ↓ 승인
  ↓
Mickey: SKILL.md 생성, REMEMBER 추가, entries 추가, stub 변환, INDEX/GRAPH 갱신
  ↓
Mickey: HANDOFF + /clear 안내
```

---

## 5. T1 / T1.5 변경 항목

### T1 (시스템 프롬프트)

| 위치 | 기존 | 신규 |
|------|------|------|
| Continuing Session | `common_knowledge/INDEX.md` 로딩 | **글로벌 `domain/INDEX.md` 로딩** (계층화) |
| During Session | "domain/ 지식 참조: GRAPH 스캔" | **변경 없음** (이미 G의 본체가 글로벌이라 자연 일관성) |
| Session End | "Knowledge Curator 호출" | **"5/5 도달 시 knowledge-organization Skill 자동 호출"** |
| Session End | Curator 결과 제시 | Skill 결과 제시 (구조 동일) |

### T1.5 (extended-protocols.md)

- §8 Adaptive Rules: 폐지 또는 "G의 가벼운 입구"로 격하 (knowledge-organization Skill이 흡수)
- §9 포스트모템: 자동 트리거 조건 + 본 진단을 baseline으로 명시
- §12 Global Knowledge: domain/ 중심으로 재작성 (patterns/ 폐지 반영)
- §16 Machine Constraints: 변경 없음
- **신규 §17 Knowledge Lifecycle**: 본 PLAN의 라이프사이클 + 분기 판단 기준 명문화
- **신규 §18 Activity Metrics**: 활용도 메트릭 자동 측정 절차 (grep 기반)

---

## 6. Phase 분해

### Phase 1: 정의 + 명문화 (1세션)
- [ ] 새 PURPOSE-SCENARIO.md 갱신
- [ ] T1.5 §17 (Knowledge Lifecycle) + §18 (Activity Metrics) 작성
- [ ] T1 변경 (Continuing Session 로딩, Session End Curator → Skill)
- [ ] Tier R/G/S 정의를 README/docs에 반영
- [ ] CC: 문서들이 새 구조를 명시, agent JSON v16 install

### Phase 2: knowledge-organization Skill 구현 (1~2세션)
- [ ] `~/.kiro/skills/knowledge-organization/SKILL.md` 작성
- [ ] CURATOR-PROMPT.md → SKILL.md 변환 (분기 판단 로직 강화)
- [ ] Mickey가 5/5 체크포인트에서 Skill을 명시 호출하도록 T1 보강
- [ ] E2E 테스트: 직전 5세션 입력 → 분기 후보 출력 검증
- [ ] CC: Skill 호출 → 출력 형식 일관 + 사용자 확인 흐름 동작

### Phase 3: 활용도 메트릭 자동 측정 (1세션)
- [ ] grep 기반 측정 스크립트 (또는 Mickey 내부 절차)
- [ ] 세션 시작 엔트로피 체크에 메트릭 출력 포함
- [ ] CC: 매 세션 시작 시 메트릭이 자동 표시됨

### Phase 4: 마이그레이션 (점진, 여러 세션)
- [ ] `~/.kiro/mickey/patterns/INDEX.md` 5개 패턴 → 글로벌 domain/entries 흡수 (이미 일부 entries 존재) → patterns/ 폐지
- [ ] `common_knowledge/agent-design-patterns.md` (M19 보강) → domain/entries → 원본 stub
- [ ] `common_knowledge/progressive-disclosure.md` → domain/entries → 원본 stub
- [ ] `context_rule/adaptive.md` 5개 규칙 → R/G/S 분기 검토 후 흡수 또는 폐기
- [ ] `~/.kiro/mickey/domain/CURATOR-PROMPT.md` → Skill 본체로 변환 후 폐지
- [ ] CC: 마이그레이션 진행률 추적 (5/5 카운터마다 1~3건씩)

### Phase 5: 실전 검증 (다음 5세션)
- [ ] 다른 프로젝트(skr-poc, gamejob 등) 세션에서 knowledge-organization Skill 자동 호출 + 승격 사례 발생
- [ ] 활용도 메트릭에서 < 10% 항목 추적 + 추가 폐지 결정
- [ ] CC: Skill 호출 누적 3회 이상 + 승격 1건 이상 in 다른 프로젝트

---

## 7. 마이그레이션 우선순위

| 순위 | 자산 | 작업 | 근거 |
|------|------|------|------|
| 1 | `~/.kiro/mickey/patterns/INDEX.md` | domain 흡수 + 폐지 | 활용도 0 + entries로 이미 분산됨 |
| 2 | `~/.kiro/mickey/domain/CURATOR-PROMPT.md` | knowledge-organization Skill 본체로 변환 | 핵심 변경의 진입점 |
| 3 | `common_knowledge/agent-design-patterns.md` | domain/entries 이전 + stub | 가장 최근 보강된 자산 |
| 4 | `common_knowledge/progressive-disclosure.md` | domain/entries 이전 + stub | INDEX 패턴 표준 — 도메인 지식 |
| 5 | `context_rule/adaptive.md` | R/G/S 분기 + stub 또는 폐기 | M19 시점 5개 규칙 |
| 6 | `~/.kiro/mickey/domain/PROFILE.md` | 유지하되 Skill 분기 판단 시 입력 명시 | 사용자 성향 추적 |

---

## 8. 리스크 + 완화책

| 리스크 | 가능성 | 완화책 |
|--------|--------|-------|
| Skill 자동 호출도 실패 (M14 함정 반복) | 중 | 5/5 카운터 외에 사용자 명시 호출도 병행. Phase 5에서 호출 빈도 메트릭 측정. |
| 마이그레이션 중 정보 유실 | 저 | 모든 승격은 stub로 추적 + git 커밋 단위 분리. 롤백 가능. |
| INDEX 계층화로 너무 복잡 | 중 | 컬럼 1개 추가만. 단순한 형태로 시작. |
| 프로젝트 간 도메인 충돌 | 저 | 글로벌 domain/INDEX는 단일 SoT. 프로젝트별 매핑은 backlink로만. |
| R 승격이 여전히 안 일어남 | 중 | knowledge-organization Skill에 R 승격 분기를 분명히 명시. PROFILE.md 입력으로 사용자 성향 활용. |

---

## 9. 결정/보류 항목

### 본 세션에서 결정
- 3-Tier(R/G/S) 채택
- 글로벌 domain/이 G의 본체
- Skills는 ~/.kiro/skills/ 표준 위치 활용 (Mickey 자체 형식 만들지 않음)
- knowledge-organization Skill + 5/5 카운터 자동 호출
- common_knowledge/, patterns/, adaptive.md 점진 폐지 (stub 정책)
- M16의 2026-06-08 Curator 검증 종료 (본 PLAN으로 대체)

### 보류 (Phase 5 검증 후 결정)
- AGENTS.md 통합 ❌ 배제 (Kiro 한정)
- Claude Auto Memory 비교 — 현재는 Kiro CLI에 해당 기능 없으므로 auto_notes/ 유지
- patterns/ 폐지 vs 글로벌 domain의 sub-category화 — Phase 4에서 판단

---

**Status**: 사용자 승인 → Phase 1부터 진행
**Created**: 2026-05-14 (Mickey 20)
**Supersedes**: IMPROVEMENT-PLAN-v8.md, IMPROVEMENT-PLAN-v8.1.md (이전 도입 의도는 본 PLAN의 진단 입력으로 흡수)
