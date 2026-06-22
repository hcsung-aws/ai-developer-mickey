# Mickey 23 Handoff

## Current Status

Curator EmptyResponse 진단 1차 라운드 완료. **query 길이/내용 가설 기각, 일시 환경 가설 기각**, 남은 가설 = prompt inline 본문 / tools-allowedTools 필드 중복. **결정적 발견: Kiro CLI agent 캐시는 세션 부트 시점에만 로딩** — 본 세션 내에서는 추가 분리 불가. 사용자 결정 β 로 본 세션 변경 모두 원복 완료. 다음 세션 Mickey 24 가 깨끗한 상태에서 재진단 사이클 진행.

## Next Steps (Mickey 24)

### 0순위 (이어짐) — Curator EmptyResponse 재진단

진단 사이클: "디스크 변경 → 새 세션 부팅 → 검증". 새 세션은 본 세션 변경이 모두 원복된 상태에서 시작.

권장 절차:
1. **인프라 정상성 확인**: `curator-ping-test` minimal agent JSON 작성 + `ai-developer-mickey.json` 화이트리스트에 추가 → **세션 재시작 (`/clear` + 새 chat)** → ping 호출 → 정상 응답 시 인프라 PASS, EmptyResponse 시 인프라 자체 문제로 좁혀짐
2. **knowledge-curator 변형 검증** (인프라 PASS 시):
   - 변형 A: `tools` 또는 `allowedTools` 한 쪽 제거 → 새 세션 → ping → 결과 분리
   - 변형 B: prompt 를 minimal 로 임시 교체 (백업 후) → 새 세션 → ping → 결과 분리
   - 변형 C: 모델 명시 (`model: "claude-opus-4.7"` 등) → 새 세션 → ping → 결과 분리
3. **정상화 후**: knowledge-curator 권한 보정 v2 + 정상 동작 확인 → Curator 검증 기간 1/5 카운트 시작 → Phase 3 (1순위) 착수

각 변형마다 새 세션 부팅이 강제되므로, Mickey 24 한 세션 안에 모든 변형을 끝내려 하지 말고 **변형 A (필드 중복) 가설부터 시작 → 결과에 따라 분기**.

### 1순위 (Curator 정상화 후) — Phase 3: 5/5 카운터 자동 호출 통합

ADDENDUM §5 Phase 3 — `m21_measure_usage.py` 를 5/5 체크포인트 도달 시 Mickey 본체가 자동 실행하도록 통합. T1 시스템 프롬프트의 5/5 처리 로직 + (선택적) T1.5 §18 측정 시점 1번. 1세션 분량.

**Curator 호출과는 독립** — Phase 3 자체는 Curator 정상화가 prerequisite 아님. 다만 검증 기간 1/5 가 Curator 정상 동작 후 시작되어야 하므로 Phase 3 진입 전 Curator 정상화가 자연스러운 흐름.

### 2순위 — Phase 4 마이그레이션 (점진, 여러 세션)

ADDENDUM §6 보정본 우선순위:
1. `~/.kiro/mickey/patterns/INDEX.md` → domain 흡수 + 폐지
2. ~~CURATOR-PROMPT → Skill 변환~~ (M21 완료, 보정 적용)
3. `common_knowledge/agent-design-patterns.md` → domain/entries 이전 + stub
4. `common_knowledge/progressive-disclosure.md` → domain/entries 이전 + stub
5. `context_rule/adaptive.md` → R/G/S 분기 + stub 또는 폐지
6. `~/.kiro/mickey/domain/PROFILE.md` → Curator 분기 판단 입력 명시 (역할 동일, 명칭만 변경)

### 3순위 — PROJECT-OVERVIEW.md / FILE-STRUCTURE.md 갱신

M22 인계분 (Last Updated 2026-03-09, 3개월+). Phase 2~5 진행 시점에 종합 갱신 권장.

## Important Context

### Kiro CLI agent 캐시 = 세션 부트 시점 단일 로딩 (본 세션 발견)

- agent JSON 추가/수정 + agent 본체의 `toolsSettings.subagent.availableAgents` 변경 — **모두 새 세션 부팅 후에야 반영**
- 진단 사이클 비용: 변형 1건 시도 = 새 세션 1회 + 컨텍스트 재로딩
- Mickey 24 는 변형 시도 시 매번 SESSION.md + HANDOFF 작성 비용을 고려하여 작업 단위를 작게 (변형 1건/세션)

### 진단 가설 좁혀진 상태 (남은 후보)

| 가설 | 검증 방법 | 위험 |
|------|----------|------|
| `tools` + `allowedTools` 필드 중복 (현재 둘 다 동일 4건) | 한 쪽만 남기고 새 세션 → ping | 저 (백업 후 복원) |
| `prompt` inline 본문 (10520+ bytes, markdown 코드블록 다수) | minimal prompt 로 임시 교체 + 새 세션 → ping | 중 (본문 백업 필수) |
| 모델 지정 부재 (`model: null`) | 명시 모델 추가 + 새 세션 → ping | 저 (knowledge-curator 만 시도) |

ai-developer-mickey 자신은 `model: null` 로 정상 동작하므로 모델 가설은 가능성이 낮다 — 후순위.

### 변형 A (필드 중복) 가설을 추천하는 이유

- 가장 저위험 (한쪽만 제거, 백업 후 즉시 복원)
- 가장 그럴 듯한 원인 (`tools` 와 `allowedTools` 의 의미 차이가 Kiro CLI 문서에 명시되지 않음 — 둘 다 정의 시 어떤 동작이 표준인지 불명확)
- 검증 비용이 적음 (단순 JSON 편집 + 새 세션 + ping)

### M22 의 인계 사항 (변동 없음)

- ADDENDUM 우선 (충돌 시 IMPROVEMENT-PLAN-v9.md 보다 IMPROVEMENT-PLAN-v9-ADDENDUM.md)
- v9 PLAN Phase 1 정착 완료 (M22), Phase 2~5 잔여
- 활용도 메트릭 baseline (T1.5 §18): domain 참조 2.45/세션, Curator 호출 2.65/세션, auto_notes 참조 5.55/세션, [Protocol] 태그 2.03/세션
- Curator 검증 기간 (첫 5회 호출): 본 세션 미진입 (Curator 비정상). Mickey 24 정상화 시점부터 1회차 카운트 시작 후보

### dangling staging (M22 부터 잔존)

- `~/.kiro/mickey/_curator-staging/pat-batch-confirm-autonomous-proceed.md` — 1건 (보류 1세션, 본 세션 처리 X). Mickey 24 가 Curator 정상화 후 자연스럽게 처리 흐름에 흡수.

### Curator 검증 기간 카운트 정책

- 본 세션은 Curator 호출이 비정상이라 1/5 카운트 시작 안 함
- Mickey 24 가 Curator 정상화 + 첫 정상 호출 발생 시점부터 1/5 카운트 시작
- 5회 동안 의도 외 변경 0건 → 신뢰 정착 (T1.5 §17 준수)

## Protocol Feedback

- [Protocol+] **session-resilience-prewrite 패턴이 본 세션 진단 사이클에서 효과적** — Goal + Purpose Alignment + Current Tasks 사전 기록이 진단 한계 도달 시점에서 정리 비용을 크게 줄임. M22 의 패턴 적용이 자연스러운 발현.
- [Protocol+] **사용자 결정 우선 원칙의 자연스러운 발현** — α 추천 vs β 선택. 본좌의 추천이 거부될 때 자세한 설명 없이 즉시 β 흐름으로 전환. communication principle 4 의 실 적용 사례.
- [Protocol] **Kiro CLI 의 agent 캐시 정책이 도구 발견의 근본 원인** — 향후 agent 진단/변경 작업의 표준 절차로 "변경 → /clear → 새 세션 → 검증" 을 명문화 권장. T1 또는 T1.5 의 자율성 가이드에 추가 후보.
- [Protocol] **diagnostic 자체의 메타 비용 인식** — agent 진단 시 변형 1건당 새 세션 1회 + SESSION 갱신 비용. 변형 후보를 5건 가지고 있다면 5세션 비용. Phase 분담 표 (M22 의 ADDENDUM §5) 와 같은 사전 분담 설계가 진단 사이클에도 적용됨.

## Quick Reference

### 본 세션 메인
- `MICKEY-23-SESSION.md` (7 Completed, 4 Decisions, 5 Lessons)

### 변경 결과 (모두 원복 완료)
- `~/.kiro/agents/ai-developer-mickey.json` — 변경 후 원복 (디스크 0줄 차이)
- `~/.kiro/agents/curator-ping-test.json` — 생성 후 삭제 (현재 미존재)
- `~/.kiro/agents/knowledge-curator.json` — 미수정 (보존)

### Mickey 24 시작점
- 본 HANDOFF + SESSION.md 의 "변형 A (필드 중복) 가설" 부터 진행 권장
- 진단 사이클 1건 = 1세션 분량으로 작업 단위 설정 권장

### Context window 인계 시점
~50% (Mickey 24 가 컨텍스트 로딩 + 진단 사이클 1건 + 정리 + HANDOFF 까지 충분)
