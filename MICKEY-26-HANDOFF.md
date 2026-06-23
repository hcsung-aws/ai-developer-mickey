# Mickey 26 Handoff

## Current Status

Curator EmptyResponse 진단 사이클의 변형 G3 디스크 반영 완료. M25 의 A1 검증이 FAIL 후, **M25 측정 도구의 false negative (missing vs explicit null 미분리)** 발견 → 측정 확장으로 누락 JSON 키 3개 (`mcpServers`, `useLegacyMcpJson`, `model`) 식별 → G3 적용 (글로벌+repo hash 일치 `5DF8F946DF56833F`). **실제 효과 검증은 Mickey 27 부팅 후 첫 작업** — Kiro CLI agent 캐시로 본 세션 내 검증 불가.

## Next Steps (Mickey 27)

### 0순위 (이어짐) — 변형 G3 검증

**부팅 직후 첫 작업**. 검증 절차는 M25/M26 와 동일:

1. **ListAgents 확인**: knowledge-curator 노출 (변형 전과 동일하게 노출되어야 정상)
2. **짧은 ping query 호출**: `use_subagent` + `agent_name=knowledge-curator` + `query="test"` (minimal)
3. **결과 분기**:

| 결과 | 해석 | 다음 행동 |
|------|------|----------|
| **정상 응답** | G3 = 정답. 누락 JSON 키 3개가 EmptyResponse 의 진짜 원인 | Curator 검증 기간 1/5 카운트 시작 + 엔트로피 처리 진입 |
| **EmptyResponse 재현** | G3 도 기각. 변형 G1 (mcpServers 만 추가) 또는 변형 F/E 진입 | 백업 원복 또는 추가 측정 필요 |

### 1순위 (G3 검증 PASS 시) — 엔트로피 처리

**A. dangling staging 1건 결정 (5세션째 보류, 임계 초과)**

`~/.kiro/mickey/_curator-staging/pat-batch-confirm-autonomous-proceed.md` — M22→M26 = **5세션 보류**. T1.5 §17 의 "3세션 이상 보류 시 자동 폐기 후보" 임계 초과 (2주째).

Curator 정상 호출 가능 시 옵션:
- (a) Curator 호출 시 dangling 항목 머지 (정식 위치 이동) 결정
- (b) 자동 폐기 후보로 폐기
- (c) Curator 검증 절차의 첫 머지/폐기 사례로 활용 (5/5 카운트 첫 항목)

**B. SESSION 아카이빙 (M21~M26 6건)**

루트의 SESSION/HANDOFF 12건 (M21~M26) — 임계 3 초과. 사용자 확인 후 `sessions/` 로 이동.

**C. PROJECT-OVERVIEW / FILE-STRUCTURE 갱신**

Last Updated 2026-03-09 (3개월+). M22~M26 의 변경 (T1.5 §17/§18 신설, Curator 진화 루프 정립, 변형 진단 사이클) 반영.

### 2순위 (G3 검증 FAIL 시) — 추가 변형

| 변형 | 차이 | 위험 |
|------|------|------|
| **G1**: mcpServers 1개만 추가 | G3 의 가장 의심 키 단독 적용 | 저 |
| **G2**: mcpServers 에 정상 에이전트 값 그대로 복사 | aws-knowledge-mcp-server 활성화 | 중 (curator 가 MCP 도구 사용하지 않으나 의도와 다른 동작 가능) |
| **F**: description 길이 단축 | 202 → 80 chars | 저 |
| **E**: prompt 코드블록 제거 | 14쌍 → 0 | 중 (prompt 본문 변경) |

권장 순서: G1 → F → E (위험 대비 우월).

### 3순위 — Phase 3: 5/5 카운터 자동 호출 통합 (M25 인계 그대로)

ADDENDUM §5 Phase 3. Curator 정상화 후 진입.

### 4순위 — Phase 4 마이그레이션 (M25 인계 그대로, 점진)

ADDENDUM §6 보정본 우선순위 그대로:
1. `~/.kiro/mickey/patterns/INDEX.md` → domain 흡수 + 폐지
2. `common_knowledge/agent-design-patterns.md` → domain/entries 이전 + stub
3. `common_knowledge/progressive-disclosure.md` → domain/entries 이전 + stub
4. `context_rule/adaptive.md` → R/G/S 분기 + stub 또는 폐지
5. `~/.kiro/mickey/domain/PROFILE.md` → Curator 분기 판단 입력 명시

## Important Context

### M26 의 결정적 발견 — M25 측정 도구 한계

M25 의 `obj.get("model")` 이 missing key 와 explicit null 을 동일하게 보고하여, 정상 에이전트가 5개 키를 더 가진 사실이 통째로 가려졌음. 변형 가설 공간이 잘못 좁혀졌고, 변형 A1 / A2 / B 가 모두 헛된 시도로 끝남 (3세션 비용).

M26 측정 확장으로 발견된 차이:

| 키 | curator (A1) | ai-developer-mickey (정상) |
|----|-------------|---------------------------|
| `mcpServers` | **키 없음** | dict (2 servers) |
| `useLegacyMcpJson` | **키 없음** | bool false |
| `model` | **키 없음** | null (명시) |
| `resources` | `[]` | `["file://AGENTS.md", "file://README.md"]` |
| `toolsSettings` | fs_write only (1 key) | + subagent + execute_bash (3 keys) |

가장 의심 키: `mcpServers` (agent loop 초기화 시 MCP 컨텍스트 참조 가능성).

### G3 의 의미 — 키 패턴 일치만 (의도 미변경)

```json
// M26 G3 (적용)
"mcpServers": {},           // 빈 dict (curator 는 MCP 사용 안 함)
"useLegacyMcpJson": false,
"model": null
```

curator 의 의도(domain/adaptive.md 자동 수정 + Pre-staged 초안 작성) 는 그대로. 정상 에이전트의 키 패턴 12개만 일치시킴. 정상 동작 확인 후 의미 있는 값(예: model 명시, resources 추가) 보충 가능.

### 백업 위치 (롤백 흐름)

| 파일 | 변형 단계 | 크기 | 비고 |
|------|----------|------|------|
| `~/.kiro/agents/knowledge-curator.json.m24-bak` | 원본 | 11797 bytes | tools=4건 + allowedTools=4건 |
| `~/.kiro/agents/knowledge-curator.json.m25-bak` | A2 | 11748 bytes | tools=["*"] + allowedTools=4건 |
| `~/.kiro/agents/knowledge-curator.json.m26-bak` | A1 | 11688 bytes | tools=["*"] + allowedTools=[] |
| `examples/knowledge-curator.json.{m24,m25,m26}-bak` | 동일 | 동일 | repo 측 동일 보존 |
| 본체 (G3) | M26 적용 | 11757 bytes | + mcpServers={}, useLegacyMcpJson=false, model=null |

G3 기각 시:
- `.m26-bak` (A1) 으로 원복 → G1 (mcpServers 단독) → F (description) → E (코드블록) 순서

### Curator 검증 기간 카운트 정책 (변경 없음)

- 본 세션은 Curator 호출이 비정상이라 1/5 카운트 시작 안 함
- Mickey 27 가 G3 검증 PASS + 첫 정상 호출 발생 시점부터 1/5 카운트 시작
- 5회 동안 의도 외 변경 0건 → 신뢰 정착 (T1.5 §17 준수)

### dangling staging 5세션째 보류 — 임계 누적

T1.5 §17 의 "3세션 이상 보류 시 자동 폐기 후보" 임계를 2세션 초과. M27 진입 즉시 Curator 정상화 후 첫 작업으로 결정.

## Protocol Feedback

- [Protocol+] **session-resilience-prewrite 4세대째 안정 작동** — M23 자연 발현 → M24 의도 적용 → M25 사전 적용 → M26 사전 적용. 패턴 정착 완료. 작업 진행 중 SESSION 갱신 비용이 단순 체크박스 갱신으로 일관 유지.
- [Protocol+] **safe-batch-replace 4-step 패턴 2세대째 재사용** — M25 (A1 적용) → M26 (G3 적용). precondition 의 hash 검증 + 누락 키 사전 확인이 의도하지 않은 적용을 차단. common_knowledge/safe-batch-replace.md 의 가치 입증.
- [Protocol] **측정 도구 false negative 의 가설 공간 가림 효과** — M25 의 `obj.get("model")` 한계로 누락 키 5개 차이가 통째로 가려져 변형 A1/A2/B 가 헛된 시도로 끝남. 측정 도구는 항상 missing/present/value 3상태를 분리 보고해야 함. domain 의 `tool-precision-before-prompt-strengthening` entry 의 메타 적용 — "도구 정밀화 우선" 이 측정 도구 자체에도.
- [Protocol] **측정 확장의 비용 대비 효용** — 측정 도구를 9개 → 12개+per-key+raw bytes 로 확장한 비용 (~5분) 으로 변형 가설 공간 재정의 + 새 세션 부팅 1~2회 비용 회피. 측정 결과가 의도대로 분기를 정밀화하지 못하면 측정 도구의 사각지대를 우선 의심.

## Quick Reference

### 본 세션 메인
- `MICKEY-26-SESSION.md` (6 Completed, 4 Decisions, 5 Lessons)

### 변경 결과 (검증 대기)
- 글로벌+repo `knowledge-curator.json` — G3 적용 (hash `5DF8F946DF56833F`, size 11757)
- 백업: `.m26-bak` (A1, 11688 bytes) 양쪽 보존
- 백업 누적: `.m24-bak`, `.m25-bak`, `.m26-bak` 3단계 모두 보존

### Mickey 27 시작점
- HANDOFF 0순위 (변형 G3 검증) 부터
- 검증 PASS → 1순위 (엔트로피 처리: dangling staging + SESSION 아카이빙 + 구조 문서 갱신)
- 검증 FAIL → G1 (mcpServers 단독) → F (description) → E (코드블록) 순서

### 검증 / 적용 스크립트 (재사용 가능)
- `scripts/m26_compare_agent_json_extended.py` — M25 보다 측정 범위 확장 (top-level 키 + per-key summary + raw bytes + prompt 패턴)
- `scripts/m26_extract_missing_keys.py` — 정상 에이전트의 누락 키 실제 값 추출
- `scripts/m26_apply_curator_variant_g3.py` — 변형 G3 적용 + 4-step 검증 (precondition → backup → apply → post-check)

### Context window 인계 시점
~50% (검증 작업 분량 충분)

### 엔트로피 미처리 (M27 시작 시 재제시 대상)
- SESSION 아카이빙: M21~M26 6건 (임계 3 초과, 5세션째 미처리)
- PROJECT-OVERVIEW.md / FILE-STRUCTURE.md: Last Updated 2026-03-09 (3개월+)
- dangling staging: 1건 (5세션 보류, 임계 2세션 초과)
