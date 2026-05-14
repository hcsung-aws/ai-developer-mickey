# POSTMORTEM-2026-05-14: Mickey 지식 구조화 + 활용 진단

> Mickey 20 (2026-05-14) — 19세션 누적 + 다른 활성 프로젝트(skr-reverse-poc 40세션, gamejob_crawler 18세션) 표본 종합 분석.
> 작성 의도: v6.3 → v8.1 까지 누적된 지식 구조 변경의 실측 활용도 평가 + 외부 트렌드 대비 개선 방향 제안.

---

## TL;DR (1페이지 요약)

**진단**: Mickey의 지식 구조는 의도와 실측 사이에 큰 갭이 있다. v8.1(글로벌 지식 + Curator)은 자기 개선 프로젝트(이 repo) 외에서는 사실상 비활성 상태이며, adaptive.md/common_knowledge도 휴면 또는 거의 미사용. **유일하게 안정적으로 작동하는 것은 auto_notes/** (모든 프로젝트 80~100% 활용).

**원인**: Mickey 14가 본인 입으로 정확히 진단함 — *"자기 실행 안 되는 프로토콜을 고치려고 프로토콜을 더 추가하면 같은 문제 반복"*. v8.1까지의 변경은 이 함정을 답습.

**외부 트렌드와의 위치**: 2025~2026년에 Mickey가 자체 구현한 패턴(INDEX 트리거, auto memory, knowledge graph)은 외부에서 표준 형식으로 정착됨 (Claude Skills의 SKILL.md, AGENTS.md, Claude Auto Memory). **Mickey만의 비표준 형식이 다른 도구와의 지식 공유를 막는 비용이 발생하기 시작**. 사용자의 머신에서 이미 kiro-dashboard가 Kiro Skills + Claude Skills + CLAUDE.md + AGENTS.md를 동시 사용 중.

**추천 (Option C, Hybrid)**:
1. **즉시 (이번 또는 다음 1세션)**: 활용도 < 10% 저장소를 추적 대상으로 명시. M16에서 예정한 2026-06-08 검증을 앞당겨 종료(Curator 호출 0의 원인이 트리거 구조 문제임을 인정).
2. **단기 (2~3세션)**: Curator 호출 트리거를 사용자 명시 의존 → 강제 중단점(체크포인트 5/5 또는 `/clear` 직전)에 결합.
3. **중기 (3~6세션)**: domain/entries → SKILL.md 호환 형식 마이그레이션 (frontmatter `description` 트리거). PROJECT-OVERVIEW + ENVIRONMENT + project-context → AGENTS.md 통합 검토.

---

## 1. 활용도 측정 결과 (76세션 표본)

### 1-1. 표본 구성

| 프로젝트 | SESSION 수 | 시작 | 최근 | 성격 |
|----------|-----------|------|------|------|
| ai-developer-mickey | 19 (+ self/ 9개 백업) | 2026-02 | 2026-05-13 | Self-Improvement |
| skr-reverse-poc | 40 | 2026-04-10 | 2026-05-12 | Implementation 메인 |
| gamejob_crawler | 18 | 2026-04-25 | 2026-05-13 | Implementation/Maintenance |

### 1-2. 저장소별 언급 빈도 (세션 비율)

| 저장소 | ai-mickey 19s | skr-poc 40s | gamejob 18s | 평가 |
|--------|--------------|-------------|-------------|------|
| `auto_notes/` | 활발 | 80% (32/40) | 100% (18/18) | ✅ 정상 작동 |
| `context_rule/project-context` | 활발 | 23% (9/40) | 17% (3/18) | △ 보통 |
| `PURPOSE-SCENARIO` | 활발 | 12% (5/40) | 5% (1/18) | △ 의식적 참조 부족 |
| `common_knowledge/` | 변경 위주 | 10% (4/40) | 5% (1/18) | ❌ 거의 미사용 |
| `adaptive.md` | 활발 | 15% (6/40) | **0% (0/18)** | ❌ 휴면 |
| **글로벌**: `domain/`, `GRAPH.md`, `PROFILE.md`, `Curator` | 자기 개선만 | **0% (0/40)** | **0% (0/18)** | ❌ 비활성 |
| `[Protocol]` 태그 | 21건/12세션 (63%) | 17건/13세션 (33%) | 7건/5세션 (28%) | △ 외부 프로젝트는 30% 미만 |

### 1-3. 결정적 사례

- **skr-reverse-poc M37** (2026-04-19): v8.1 IMPROVEMENT-PLAN이 작성된 그날 진행된 실제 구현 세션. Curator/domain/GRAPH 0회 언급. [Protocol] 태그 0건.
- **skr-reverse-poc M40** (2026-05-12): Maintenance 세션. 프로토콜상 Curator 호출 대상이지만 호출 0회.
- **gamejob_crawler M18** (2026-05-13): D-024~026 의사결정 + Lessons 4건 + [Protocol] 태그 1건 — 풍부한 학습 신호. **Curator 미호출로 글로벌 지식 형성 0**.

---

## 2. 과거 변경 의도 vs 실측 (포스트모템 본체)

| 버전 | 도입 시점 | 의도 | 실측 결과 | 판정 |
|------|----------|------|----------|------|
| v6.3 (M5) | 2026-03-01 | auto_notes 자동 메모리 (사실 vs 규칙 분리) | 80~100% 활용 | ✅ **유효 — 유지** |
| v7 (M8) | 2026-03-08 | 자율 실행 + Backpressure + Brownfield | Brownfield 검증 부족, 자율 실행은 부분 작동 | △ **부분 유효** |
| v7.1 (M9) | 2026-03-09 | adaptive.md 자가 규칙화 | gamejob 0건, skr 15% — 트리거 약함 | ❌ **재설계 필요** |
| v7.2 (M9) | 2026-03-09 | Autonomy Preference | 사용자 명시 의존 | △ **부분 유효** |
| v8 (M12) | 2026-03-26 | patterns/ + domain/ 글로벌 지식. "65세션 분석에서 패턴 수렴" + "이식성" | patterns/INDEX는 만들어졌으나 다른 프로젝트에서 0회 참조 | ❌ **이식성 측면에서 비유효** |
| v8.1 (M14-15) | 2026-04-19 | Curator + domain/{GRAPH,PROFILE,entries} | Curator 호출 0회 (M16에서 자기 발견) | ❌ **트리거 구조 결함** |
| v15 (M16) | 2026-05-08 | Curator를 세션 중 → 세션 종료 배치로 전환. 검증 2026-06-08 예정 | M16 이후 외부 프로젝트 세션 4건 (skr 37~40, gamejob 17~18) 모두 호출 0회 | ⚠️ **재검증 필요 (사실상 실패)** |

### 핵심 인용 (Mickey 자기 발견)

- **M14**: *"자기 실행 안 되는 프로토콜을 고치려고 프로토콜을 더 추가하면 같은 문제 반복. 이미 실행되는 행동에 편승하는 것이 유일한 해법."*
- **M16**: *"6개 프로젝트에서 Curator 호출 0회, adaptive.md 생성 0건, domain/ 갱신 0회. 근본 원인: 세션 중 자동 호출은 판단 병목 + 실행 마찰로 동작 불가."*

→ M14가 진단한 함정을 v8 도입 시 인지하고 있었음에도 v8/v8.1까지 같은 패턴(추가) 반복. M16의 "세션 종료 배치" 전환은 부분적 진보지만, **세션 종료 트리거 자체가 사용자 명시("세션 정리하자") 의존**이라 동일 결함 잔존.

---

## 3. 외부 트렌드 대비 (2025~2026)

### 3-1. Mickey 패턴이 외부에서 표준화됨

| Mickey 자체 형식 | 외부 표준 (출시) | 비고 |
|-----------------|-----------------|------|
| INDEX 트리거 + T3a/T3b 로딩 | **Claude Skills** SKILL.md + frontmatter `description` (2025-10) | Progressive Disclosure 패턴이 표준화. Mickey가 같은 컨셉을 더 일찍 자체 구현. |
| project-context.md + PROJECT-OVERVIEW + ENVIRONMENT | **AGENTS.md** / CLAUDE.md (cross-platform) | Codex CLI, Claude Code, Gemini CLI 동시 지원. |
| auto_notes/ | **Claude Auto Memory** (2025-10) | Claude Code에 내장. AGENTS.md와 병행. |
| ~/.kiro/mickey/extended-protocols.md | Claude Code home-level CLAUDE.md | 4-tier hierarchy: agent/brand/agent context/project. |
| ~/.kiro/mickey/domain/{GRAPH,PROFILE,entries} | **GraphRAG / MAGMA / Hierarchical Agentic Memory** | 학계 활발. Mickey 단일 GRAPH.md는 단순화된 버전. |
| 포스트모템 [Protocol] 태그 + Curator | **Agent Stability Index (ASI)** — 12차원 drift 메트릭 (2025) | 정량적 anomaly detection. Mickey는 정성적 단계. |
| Knowledge Curator subagent | Claude Skills + Subagents 조합 | Claude의 specialized agent 패턴이 표준. |

### 3-2. 사용자의 실제 도구 환경 (kiro-dashboard 발견)

이 머신의 kiro-dashboard 프로젝트는 다음을 동시 사용:
- `.kiro/skills/` (Kiro Skills, SKILL.md 형식)
- `.claude/skills/` (Claude Skills, SKILL.md 형식)
- `AGENTS.md` (프로젝트 전체 개요 — Codex/Claude/Gemini 모두 인식)
- `CLAUDE.md` (Claude Code 메모리)
- `.kiro/steering/` (Kiro IDE 자동 로딩 규칙)

→ **사용자는 이미 다중 AI 도구 환경**. Mickey가 자체 형식을 고수하면 같은 지식을 두 군데 적어야 하는 비용 발생.

### 3-3. 트렌드 정렬 진단

| 영역 | Mickey 위치 | 외부 위치 |
|------|-------------|-----------|
| 지식 트리거 + Progressive Disclosure | ✅ 일찍 도입 | 표준화됨 (SKILL.md) |
| Auto Memory | ✅ v6.3에서 도입 | 도구 내장됨 |
| Knowledge Graph 메모리 | △ 단순 형태 | 학계 활발, 도구 미내장 |
| Cross-tool 호환성 | ❌ 자체 형식 | AGENTS.md 표준 |
| 정량 drift 메트릭 | ❌ 정성적 | ASI 등 등장 |
| Goal/Purpose tracking | ✅ PURPOSE-SCENARIO | 학계 Goal Drift 측정 도입기 |

---

## 4. 문제 분류

### 4-1. 누락 (Missing — 있어야 할 곳에 없음)

- **외부 프로젝트에서 글로벌 지식 활용 0건** — Curator 호출이 트리거되지 않아 글로벌 지식이 형성/참조되지 않음.
- **활용도 메트릭 자동 측정 부재** — 매 포스트모템마다 수동 grep이 필요.

### 4-2. 휴면 (Dormant — 만들었으나 거의 안 쓰임)

- `adaptive.md`: gamejob 0건, skr 15%. "같은 실수 2회" 트리거 조건이 약함. Curator 미호출과 결합되어 휴면.
- `common_knowledge/`: 외부 프로젝트 5~10%. 작성은 되지만 다른 세션에서 의식적 참조 거의 없음.
- `~/.kiro/mickey/patterns/`: 7개 패턴이 INDEX에 등록되어 있으나 외부 프로젝트 0건 참조.

### 4-3. 충돌 (Collision — 외부 표준과 비호환)

- Mickey의 `mickey/extended-protocols.md` ↔ Claude Code home-level CLAUDE.md
- Mickey의 `context_rule/project-context.md` ↔ AGENTS.md / CLAUDE.md
- Mickey의 `domain/entries/*.md` ↔ Claude/Kiro Skills SKILL.md
- 같은 프로젝트(kiro-dashboard)에서 두 형식이 공존 — 지식 분리 비용 발생.

### 4-4. 접근성 (Accessibility — 존재하나 발견 안 됨)

- `PURPOSE-SCENARIO`: 로딩되지만 의식적 참조 5~12%. "최우선" 가이드라는 위상에 비해 낮음.
- `domain/INDEX.md`: 트리거가 있어도 작업 키워드와 매칭률 낮음 (M16에서 backlink로 보강했으나 실측 0건).
- `[Protocol]` 태그: 외부 프로젝트 30% 미만. 자기 개선 프로젝트에서만 활발 → 포스트모템 입력이 정상 형성되지 않음.

---

## 5. 개선 옵션 비교

### Option A — 정량 검증 + 점진 폐지 (보수적)

| 단계 | 내용 | 시간 |
|------|------|------|
| 1 | 활용도 메트릭 자동 측정 스크립트 (grep 기반) | 1세션 |
| 2 | < 10% 항목을 "은퇴 대기"로 분류 | — |
| 3 | 2개월 시범 후 활용 0건이면 폐지 (Curator/patterns/domain/adaptive 후보) | 시간 경과 |
| 4 | T1/T1.5 슬림화 | 1세션 |

**Pros**: 리스크 최저. 실측 기반. Mickey 14의 "추가하지 않기" 원칙 충실. 
**Cons**: 외부 트렌드(Skills/AGENTS.md) 따라잡기 부족. 사용자가 다른 도구와 같이 쓸 때 불편 그대로. 
**리스크**: 폐지 후 정작 필요해지면 재구축 비용. 단, "0건 사용"이라는 강한 신호가 있으므로 낮음.

### Option B — Skills 표준화 + 자체 구조 통합 (전향적)

| 단계 | 내용 | 시간 |
|------|------|------|
| 1 | `domain/entries/*.md` → SKILL.md 형식 변환 (frontmatter `description` 추가) | 2세션 |
| 2 | `~/.kiro/skills/` 하위로 이동 (Kiro Skills 위치 표준) | 1세션 |
| 3 | `PROJECT-OVERVIEW + ENVIRONMENT + project-context` → `AGENTS.md` 통합 | 1세션 |
| 4 | `mickey/extended-protocols.md` → 홈 CLAUDE.md 또는 AGENTS.md로 분산 | 2세션 |
| 5 | Curator를 Claude Code Auto Memory와 비교 검토 → 폐지 또는 차별점 명시 | 1세션 |
| 6 | Mickey JSON 프롬프트에서 Skills/AGENTS.md 로딩 규칙 반영 | 1세션 |

**Pros**: 외부 표준 호환. 다른 도구 사용자도 활용 가능. 사용자의 다중 도구 환경에 부합. 
**Cons**: 큰 리팩토링. 기존 자산 마이그레이션 비용. install.sh 재설계. Power Mickey 동기화 비용. 
**리스크**: 표준 자체가 진화 중이라 또 변경 가능성. M14의 함정(추가만 함) 다시 빠질 수 있음.

### Option C — Hybrid (추천)

#### 즉시 (이번 또는 다음 1세션)
- M16의 검증 시점(2026-06-08)을 본 진단으로 종료. **결론: Curator/글로벌 지식은 트리거 구조 실패, 추가 1개월 관찰로 해결되지 않음**.
- 활용도 메트릭을 SESSION 시작 엔트로피 체크에 추가 — `grep -c` 기반 간단 통계 (T1.5 §3 보강).

#### 단기 (2~3세션)
- **Curator 호출 강제 중단점화**: 
  - 현재: 사용자가 "세션 정리"라고 말해야 발동
  - 변경: 체크포인트 5/5 도달 또는 사용자 첫 `/clear` 의도 표시 시 자동 호출 (Mickey 14의 "강제 중단점" 원칙 적용)
- **adaptive.md 트리거 재설계**: "같은 실수 2회" → "Lessons Learned 항목 작성 시 자동 1줄 추가" (auto_notes 패턴 차용)
- **정량 메트릭**: 다음 N세션 동안 메트릭 누적 → 채택/폐지 결정

#### 중기 (3~6세션)
- **domain/entries/*.md → SKILL.md 호환 형식**: frontmatter `description` 추가만으로 호환 가능 (구조 변경 최소). Kiro Skills + Claude Skills 양쪽에서 인식.
- **AGENTS.md 도입 검토**: PROJECT-OVERVIEW + ENVIRONMENT의 핵심을 AGENTS.md에 미러링 (cross-platform). 단 Mickey 자체 형식은 SoT(source of truth) 유지.
- **Curator vs Claude Auto Memory 비교**: Curator의 차별점(관계 설정, GRAPH)이 진짜 필요한지 정량 검증.

#### 장기 (6세션+)
- v8.1 결과(M16의 6월 검증) 대신 본 포스트모템을 새 baseline으로 → IMPROVEMENT-PLAN-v9 작성 검토
- patterns/ + domain/ 합병 또는 폐지 결정

**Pros**: 단계적 + 외부 표준 점진 도입 + 즉시 적용 가능 부분 있음. M14의 함정 회피 (먼저 폐지/메트릭, 추가는 마지막). 
**Cons**: 일정 길음. 변경 누적 위험은 있으나 "메트릭 → 결정" 사이클로 완화. 
**리스크**: 중간 단계에서 또 멈출 가능성 — 명확한 체크리스트가 있어야 함.

---

## 6. 추천

**Option C 채택을 추천**. 이유:

1. **Option A는 외부 트렌드 무시 비용** — kiro-dashboard처럼 다중 도구 환경에서 Mickey만 자체 형식을 고수하면 사용자 불편 누적.
2. **Option B는 한 번에 너무 큰 변경** — Mickey 14의 함정(추가만)을 또 답습할 위험. "자기 개선 프로토콜을 또 만든다"는 패턴.
3. **Option C는 Mickey 14 원칙 충실** — 측정 → 폐지 검토 → 외부 표준 점진 도입. 각 단계에 명확한 결정 기준.

### 첫 결정 (사용자에게 즉시 필요)

- (a) 본 진단을 IMPROVEMENT-PLAN-v9로 격상 → 다음 세션부터 Option C 단기 단계 시작
- (b) 본 진단만 기록하고 보류 → 이번 세션은 SESSION/HANDOFF만 정리
- (c) 부분 채택 → "즉시" 단계만 이번 세션에 반영 (Curator 검증 종료 + 메트릭 측정 도입)

---

## 7. 부록

### 7-1. 활용도 측정 방법

```
grep -r --include="MICKEY-*.md" -c "<keyword>" <project_root>
```

키워드별 매칭 수를 세션 수로 나눈 값을 활용도로 사용.

### 7-2. 외부 트렌드 출처 (요약)

- Claude Skills (2025-10-16, Anthropic): SKILL.md + frontmatter, progressive disclosure
- Claude Auto Memory (2025-10): Claude Code 내장 자동 누적
- AGENTS.md cross-platform: Codex, Claude Code, Gemini CLI 공통 지원
- GraphRAG / MAGMA (arxiv 2025~2026): multi-graph agentic memory, policy-guided retrieval
- Agent Stability Index (arxiv 2026): 12차원 drift 메트릭

### 7-3. 데이터 원본

- `MICKEY-20-SESSION.md`의 grep 결과 + `MICKEY-12,14,15,16-SESSION.md` 핵심 인용
- 외부 프로젝트 표본: `C:\Users\hcsung\work\kiro\skr-reverse-poc\` (40세션), `C:\Users\hcsung\work\gamejob_crawler\` (18세션), `C:\Users\hcsung\work\kiro-dashboard\` (Mickey 미사용, Skills/AGENTS.md 사용 사례)

---

**End of postmortem.**
