# Mickey 25 Handoff

## Current Status

Curator EmptyResponse 진단 사이클의 변형 A1 디스크 반영 완료. M24 의 A2 (`tools=["*"]` + `allowedTools=4건`) 검증이 FAIL 후, 정밀 비교 측정으로 변형 B (prompt 길이) 기각 + 변형 A1 (`allowedTools=[]`) 가설 부각. 글로벌+repo 양쪽에 A1 적용 (hash 일치 `545891F304E37943...`). **실제 효과 검증은 Mickey 26 부팅 후 첫 작업** — M23 의 Kiro CLI 캐시 발견에 따라 본 세션 내 검증 불가.

## Next Steps (Mickey 26)

### 0순위 (이어짐) — 변형 A1 검증

**부팅 직후 첫 작업**. 검증 절차는 M24 와 동일:

1. **ListAgents 확인**: knowledge-curator 노출 여부 (변형 전과 동일하게 노출되어야 정상)
2. **짧은 ping query 호출**: `use_subagent` + `agent_name=knowledge-curator` + `query="test"` (minimal)
3. **결과 분기**:

| 결과 | 해석 | 다음 행동 |
|------|------|----------|
| **정상 응답** | A1 = 정답. `allowedTools=4건` 이 EmptyResponse 의 진짜 원인 | Curator 검증 기간 1/5 카운트 시작 + 자동 승인 손실 보완 논의 진입 |
| **EmptyResponse 재현** | A1 도 기각. 다른 가설 (변형 E: 코드블록 / 변형 F: description) | 백업 원복 (`.m25-bak` → 본체) + 변형 E/F 정밀화 |

### 1순위 (A1 검증 PASS 시) — 자동 승인 손실 보완 논의

A1 적용으로 자동 승인 4건 (`fs_read`, `grep`, `glob`, `fs_write`) 의도 손실. 보완 옵션:

| 옵션 | 방법 | 마찰 |
|------|------|------|
| 1. CLI `--trust-tools` 플래그 | 사용자 측 환경 설정 | Mickey 가 런타임에 변경 불가, 사용자 매뉴얼 필요 |
| 2. 마찰 수용 | 매 호출 사용자 확인 | Pre-staged Apply 흐름에 매 호출 마찰 |
| 3. 다른 메커니즘 발굴 | Kiro CLI 문서 재조사 | 시간 비용 |

PURPOSE-SCENARIO 의 "Pre-staged Apply" 흐름과의 정합성을 가장 우선해 결정 필요.

### 2순위 — dangling staging 처리

`~/.kiro/mickey/_curator-staging/pat-batch-confirm-autonomous-proceed.md` — **4세션 보류** (M22→M23→M24→M25). T1.5 §17 의 "3세션 이상 보류 시 자동 폐기 후보" 임계 초과.

Curator 정상화 후 사용자에게 명확한 결정 요청:
- (a) 정식 위치로 머지 (검토 후 patterns/ 또는 REMEMBER 후보로 채택)
- (b) 폐기 (Pre-staged Apply 의 자정 작용)
- (c) Curator 검증 절차에 본 항목 머지/폐기 흐름을 첫 사례로 활용

### 3순위 — Phase 3: 5/5 카운터 자동 호출 통합 (M24 인계 1순위 그대로)

ADDENDUM §5 Phase 3. `m21_measure_usage.py` 를 Mickey 본체가 자동 실행하도록 통합. Curator 정상화 + dangling 정리 후 진입.

### 4순위 — Phase 4 마이그레이션 (M24 인계 2순위 그대로, 점진)

ADDENDUM §6 보정본 우선순위 그대로:
1. `~/.kiro/mickey/patterns/INDEX.md` → domain 흡수 + 폐지
2. `common_knowledge/agent-design-patterns.md` → domain/entries 이전 + stub
3. `common_knowledge/progressive-disclosure.md` → domain/entries 이전 + stub
4. `context_rule/adaptive.md` → R/G/S 분기 + stub 또는 폐지
5. `~/.kiro/mickey/domain/PROFILE.md` → Curator 분기 판단 입력 명시

### 5순위 — PROJECT-OVERVIEW.md / FILE-STRUCTURE.md 갱신

M22 인계분 (Last Updated 2026-03-09, 3개월+). Phase 2~5 진행 시점 종합 갱신 권장.

## Important Context

### A1 의 의미 (M24→M25 정밀화 결과)

M24 의 A2 는 "ai-developer-mickey 패턴 모방" 이었으나 `tools` 필드만 변경하고 `allowedTools` 는 4건 유지 → 절반만 모방. M25 정밀 측정으로 정상 패턴은 `tools=["*"]` + `allowedTools=[]` (두 필드 동시) 임이 확인됨.

```json
// 변형 전 (M24 적용 후 = A2)
"tools": ["*"],
"allowedTools": ["fs_read", "grep", "glob", "fs_write"]

// 변형 후 (M25 적용 = A1)
"tools": ["*"],
"allowedTools": []
```

자동 승인 4건 의도는 손실. Curator 호출 자체 동작이 우선.

### 백업 위치 (롤백 흐름)

| 파일 | 백업 | 비고 |
|------|------|------|
| `~/.kiro/agents/knowledge-curator.json.m24-bak` | 11797 bytes | 원본 (tools=4건 + allowedTools=4건) |
| `~/.kiro/agents/knowledge-curator.json.m25-bak` | 11748 bytes | A2 (tools=["*"] + allowedTools=4건) |
| `examples/knowledge-curator.json.m24-bak` | 11797 bytes | 동일 |
| `examples/knowledge-curator.json.m25-bak` | 11748 bytes | 동일 |
| 본체 (A1) | 11688 bytes | tools=["*"] + allowedTools=[] |

A1 기각 시 `.m25-bak` 으로 원복 후 변형 E/F 시도. 더 이전 단계로 가려면 `.m24-bak`.

### 변형 E / F 가설 (A1 기각 시 후순위)

| 가설 | 차이 | 검증 방법 | 위험 |
|------|------|----------|------|
| **E**: prompt 내 markdown 코드블록 | curator 7쌍 vs 정상 0쌍 | minimal prompt (코드블록 제거 버전) 임시 교체 + 새 세션 → ping | 중 (prompt 본문 백업 필수) |
| **F**: description 길이 | curator 202 vs 정상 80 | description 단축 (예: 80 chars 이하) | 저 |

A1 기각 가능성은 낮으나, 기각 시 F → E 순서가 위험 대비 우월.

### Curator 검증 기간 카운트 정책 (변경 없음)

- 본 세션은 Curator 호출이 비정상이라 1/5 카운트 시작 안 함
- Mickey 26 가 A1 검증 PASS + 첫 정상 호출 발생 시점부터 1/5 카운트 시작
- 5회 동안 의도 외 변경 0건 → 신뢰 정착 (T1.5 §17 준수)

### dangling staging 4세션 보류 — 임계 초과

T1.5 §17 의 "3세션 이상 보류 시 자동 폐기 후보" 임계를 본 세션에서 초과. M26 진입 즉시 사용자에게 명확한 결정 요청 필요.

## Protocol Feedback

- [Protocol+] **session-resilience-prewrite 사전 기록의 누적 효과** — M23 자연 발현 → M24 의도 적용 → M25 사전 적용. 작업 진행 중 SESSION 갱신 비용이 단순 체크박스 갱신으로 일관 유지. (3세대째 안정 작동)
- [Protocol+] **정밀 비교 측정이 변형 가설의 헛됨을 사전 차단** — M25 의 정밀 측정 단계가 변형 B 를 기각하고 A1 을 부각함. 측정 1회의 비용 (스크립트 작성 + 실행 = 약 5분) 으로 새 세션 부팅 1회 비용 (수십 분 + context 비용) 회피. M24 인계대로 변형 B 를 시도했다면 동일하게 FAIL 했을 가능성 높음.
- [Protocol] **PowerShell `ConvertFrom-Json` 의 cp949 + 큰 JSON 한계** — adaptive.md Rule #8 의 stdout 인코딩 가설을 입력 측 (JSON 파싱) 으로 확장 적용 후보. agent JSON 측정/검증 시 항상 Python 우선 사용 — adaptive.md 후보.

## Quick Reference

### 본 세션 메인
- `MICKEY-25-SESSION.md` (7 Completed, 4 Decisions, 5 Lessons)

### 변경 결과 (검증 대기)
- 글로벌+repo `knowledge-curator.json` — A1 적용 (hash `545891F304E37943...`, size 11688)
- 백업: `.m24-bak` (원본) + `.m25-bak` (A2) 양쪽 보존

### Mickey 26 시작점
- HANDOFF 0순위 (변형 A1 검증) 부터
- 검증 PASS → 1순위 (자동 승인 보완) + 2순위 (dangling 처리)
- 검증 FAIL → 변형 F (description) → 변형 E (코드블록) 순서

### 검증 / 적용 스크립트 (재사용 가능)
- `scripts/m25_compare_agent_json.py` — Curator vs ai-developer-mickey 정밀 비교 (변형 가설 정밀화용)
- `scripts/m25_apply_curator_variant_a1.py` — A1 적용 + 4-step 검증 (precondition → backup → apply → post-check)

### Context window 인계 시점
~60% (검증 작업 분량 충분)

### 엔트로피 미처리 (M26 시작 시 재제시 대상)
- SESSION 아카이빙: M21~M25 5건 (임계 3 초과, 4세션째 미처리)
- PROJECT-OVERVIEW.md / FILE-STRUCTURE.md: Last Updated 2026-03-09 (3개월+)
- dangling staging: 1건 (4세션 보류, 임계 초과)
