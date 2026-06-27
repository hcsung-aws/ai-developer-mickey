# Mickey 28 Handoff

## Current Status

Curator EmptyResponse 진단 사이클 7세대. M27 인계 변형 H 검증 FAIL → 매뉴얼 정독 + 외부 이슈 조사로 가설 공간을 "agent JSON 안의 키 비교" 에서 "agent JSON 외부 자동 포함 메커니즘" 으로 외부 확장. **변형 I (옵션 B: `includeMcpJson:false` 추가 + `useLegacyMcpJson` 제거) 디스크 반영 완료** (글로벌+repo hash `45CAFB42A1152689`, size 12137). 실제 검증은 Mickey 29 부팅 후 첫 작업 — Kiro CLI agent 캐시(M23) 원칙.

## Next Steps (Mickey 29)

### 0순위 — 변형 I 검증

**부팅 직후 첫 작업**:

1. **ListAgents 확인**: knowledge-curator 정상 노출
2. **짧은 ping query 호출**: `use_subagent` + `agent_name=knowledge-curator` + `query="test"` 또는 정형 입력
3. **결과 분기**:

| 결과 | 해석 | 다음 행동 |
|------|------|----------|
| **정상 응답** | N5 (글로벌 mcp.json 자동 attach) 가설 확정. 본 진단 사이클 7세대 종료 | (1) 메타 교훈 글로벌 도메인 entry 승격 — `subagent-mcp-config-trap` 또는 `agent-json-implicit-mcp-inheritance` (2) Curator 검증 기간 1/5 카운트 시작 (3) dangling staging 2건 처리 (4) M22~M27 의 5건 백업 (.m24~.m28-bak) 압축 정리 검토 |
| **EmptyResponse 재현** | N5 도 기각. M22~M28 의 모든 변형 + 외부 자료 조사도 가설 공간 못 도달 | 진단 종료 (옵션 W) 또는 Curator subagent 분리 설계 재검토 (옵션 R). Kiro CLI 자체 회귀 (#6163) 로 결론 가능성 — 본 issue 댓글 추적 또는 새 이슈 등록 검토 |

### 1순위 (I 검증 PASS 시) — 메타 교훈 글로벌 승격 + 정리 작업

#### A. 글로벌 도메인 entry 승격 (강력 추천)

본 진단 사이클의 메타 교훈은 다른 프로젝트의 자가 개선 루프 진단에서도 직접 적용 가능. 두 후보:

1. **`subagent-mcp-config-trap`** (또는 `agent-json-implicit-mcp-inheritance`)
   - Core: subagent 의 agent JSON 에 `includeMcpJson:false` 누락 시 글로벌 mcp.json 의 MCP server 가 자동 attach → Anthropic claude-code 회귀 패턴 (#17743) 트리거 → 0 tool uses 즉시 종료
   - Tags: kiro, subagent, mcp, agent-config, silent-fail, anthropic-issue, configuration-trap
   - Source: ai-developer-mickey M22~M28 (7세대 진단)
   - Links: tool-precision-before-prompt-strengthening, iterative-measurement-deepening, deploy-output-distrust 가족

2. **(선택) `external-issue-tracker-first`** 또는 `manual-and-issue-search-before-variation`
   - Core: 자가 진단 사이클 시작 시 외부 issue tracker 검색을 1세대에서 병행 — 알려진 회귀 발견 시 가설 공간 우회. 비용 5분 미만, 효용 N세대 가설 공간 절약
   - Source: M28 매뉴얼 정독 + Anthropic/Kiro 이슈 검색 5분 = M22~M27 6세대 우회

#### B. Curator 검증 기간 1/5 카운트 시작
- 본 ping 검증 PASS 후 첫 정상 호출로 카운트 시작
- 다음 4회 호출에서 git diff 자동 보고 (의도 외 변경 가드, T1.5 §17 준수)

#### C. dangling staging 2건 처리

`~/.kiro/mickey/_curator-staging/` 의 2개 파일 (Jun 23 11:34/11:35):
- `pat-handoff-unresolved-trigger-marker.md`
- `pat-solution-bypass-vs-formal-resolution-separation.md`

처리 절차:
1. 두 파일 읽기 → 출처 (어떤 프로젝트의 어떤 세션) + 내용 확인
2. 사용자에게 보고 + 단일 응답 요청 ("전체"/"1,3"/"없음"/"보류")
3. 응답에 따라 patterns/ 정식 위치 이동 또는 폐기

#### D. 백업 정리 검토

5건 누적 (.m24~.m28-bak, 양쪽) — Curator 정상화 후 1주 안정 확인 시 .m24~.m26-bak 일괄 압축 또는 archive 폴더 이동 검토. .m27-bak (G3, 직전 단계) + .m28-bak (H, I 의 직전) 은 보존.

### 2순위 (I 검증 FAIL 시) — 진단 종료

| 옵션 | 행동 |
|------|------|
| **W (대기)** | 변형 I 원복 (.m28-bak), Curator 분리 설계 그대로 두고 Kiro CLI 안정화 대기. M22~M28 누적 비용 회수 X 이지만 안전 |
| **R (설계 변경)** | Curator subagent 분리 포기 → Mickey 본체에 Curator prompt 흡수. v9.1 ADDENDUM 재설계. 진화 루프 자체는 prompt 흐름으로 유지 가능 |
| **외부 이슈 등록** | Kiro 측에 본 진단 결과 보고 (#6163 의 추가 사례로 댓글 또는 새 이슈) — 본 7세대 진단 자체가 외부 가치 가능 |

권장: I 검증 FAIL 시 W (Kiro 안정화 대기) + 외부 이슈 보고. R 은 v9.1 ADDENDUM 의 핵심 가치(권한 분리)를 잃어 권장 안 함.

### 3순위 — Phase 3 (5/5 카운터 자동 호출 통합)

ADDENDUM §5 Phase 3. Curator 정상화 + 검증 기간 1/5 카운트 완료 후 진입.

## Important Context

### M28 의 결정적 발견 — 가설 공간 외부 확장의 메타 교훈

M22~M27 6세대는 "agent JSON 안의 키 차이" 라는 단일 차원에 갇혀 있었다. M28 의 매뉴얼 정독 + 외부 이슈 조사 5분이 가설 공간을 "agent JSON 외부의 자동 포함 메커니즘" 으로 확장:

1. **Kiro 매뉴얼**: `includeMcpJson` 만 정식 필드, `useLegacyMcpJson` 매뉴얼 미명시 (deprecated 가능성)
2. **Anthropic claude-code Issue #17743**: "Task tool subagents fail with 0 tool uses when MCP servers configured" — 정확히 우리 케이스
3. **Anthropic Issue #10739**: "Subagents return empty response with zero tool uses" — 동일 클래스
4. **Kiro Issue #6163**: "subagent stuck 0 tool uses · 0.00s" — Kiro 측 동일 패턴
5. **글로벌 mcp.json**: `~/.kiro/settings/mcp.json` 에 3개 MCP server (aws-knowledge / aws-api / serena) 등록되어 있음
6. **정상 동작 비교군**: kiro-learning-helper, mockdb-test-agent 모두 `includeMcpJson:false` 명시 차단 — Curator 만 누락

### 변형 I 의 안전성 평가

- 변경 자체가 매우 작음 (1줄 제거 + 1줄 추가)
- 정상 동작 비교군의 검증된 패턴 (kiro-learning-helper, mockdb-test-agent) 적용
- Curator 의 의도 (MCP 사용 안 함) 와 부합
- 5건의 백업 누적 — 즉시 원복 가능
- safe-batch-replace 4-step 6세대 안정

### Curator 검증 기간 카운트 정책 (변경 없음)

- 본 세션은 Curator 호출이 비정상이라 1/5 카운트 시작 안 함
- Mickey 29 가 I 검증 PASS + 첫 정상 호출 발생 시점부터 1/5 카운트 시작
- 5회 동안 의도 외 변경 0건 → 신뢰 정착 (T1.5 §17 준수)

### 본 세션 dangling staging 2건의 출처

`~/.kiro/mickey/_curator-staging/` 에 M27 종료(11:43) 직전(11:34, 11:35) 등록된 2개 파일. 본 세션 진입 시 발견. M27 인계의 "0건" 과 불일치. **M27 의 `[Protocol] 인계는 그 시점 관찰` 교훈이 다음 세션에서 즉각 재현된 사례** — 진입 시 디스크 재스캔 의무화 패턴 8세대째 누적. 다른 프로젝트가 M27 시점 이후 글로벌 staging 에 추가한 것으로 추정 (파일명: `pat-handoff-unresolved-trigger-marker.md`, `pat-solution-bypass-vs-formal-resolution-separation.md`).

### 백업 위치 (롤백 흐름)

| 파일 | 변형 단계 | 크기 | 비고 |
|------|----------|------|------|
| `.m24-bak` | 원본 (M24 변형 전) | 11797 bytes | tools=4건 + allowedTools=4건 |
| `.m25-bak` | A2 | 11748 bytes | tools=["*"] + allowedTools=4건 |
| `.m26-bak` | A1 | 11688 bytes | tools=["*"] + allowedTools=[] |
| `.m27-bak` | G3 | 11757 bytes | + mcpServers={}, useLegacyMcpJson=false, model=null |
| `.m28-bak` | H | 12139 bytes | + resources, toolsSettings.execute_bash, toolsSettings.subagent |
| 본체 | I (M28 적용 후) | 12137 bytes | useLegacyMcpJson 제거, includeMcpJson:false 추가 |

I 기각 시:
- `.m28-bak` (H) 으로 원복 → 진단 종료 (W 옵션) 또는 설계 변경 (R 옵션) 진입

### Mickey 본체 JSON 의 useLegacyMcpJson:false 도 정리 검토 대상

매뉴얼 미명시 deprecated 필드. mickey 본체는 자체 mcpServers inline 정의 때문에 정상 동작 추정 — `useLegacyMcpJson:false` 효과는 미상. Curator 가 정상화되고 신뢰 정착 후, mickey 본체에도 `includeMcpJson:false` 명시 + `useLegacyMcpJson` 제거를 검토 가능. 단 즉시 변경은 권장 안 함 (정상 작동 중 변경의 위험).

## Protocol Feedback

- [Protocol+] **safe-batch-replace 4-step 패턴 6세대째 안정** — M25(A1) → M26(G3) → M27(H) → M28(I). precondition (hash + 키 검증) 의 사전 차단이 의도 외 적용을 6회 연속 막음.
- [Protocol+] **session-resilience-prewrite 6세대째 안정** — M23 자연 발현 → M24~M28. SESSION.md 사전 기록 후 작업이 단순 체크박스 갱신으로 일관 유지.
- [Protocol+] **batch-confirm-autonomous-proceed 패턴 2회차 적용** — 사용자 "B로 진행" 짧은 응답을 옵션 B 의 두 변경 (includeMcpJson 추가 + useLegacyMcpJson 제거) 일괄 채택으로 해석. 3조건(CC 명확+rollback 가능+검증 가능) 충족 → 자율 진행. M27(첫 적용) 이후 2번째 사례.
- [Protocol] **자가 진단 사이클의 외부 자료 조사 의무화** — M22~M27 6세대가 매뉴얼 정독 + GitHub 이슈 검색 없이 진행되어 Anthropic / Kiro 측의 알려진 subagent 회귀 이슈를 6세대 동안 못 발견. M28 이 5분 미만 검색으로 정확히 일치하는 회귀 패턴 발견. 자가 개선 진단의 1세대에서 외부 자료 조사 병행 의무화 필요 — 글로벌 도메인 entry 승격 강력 추천.
- [Protocol] **단일 비교 vs 다중 비교군** — mickey vs curator 의 1:1 비교는 6세대 누적해도 N5 도출 못 함. 다른 정상 agent 4개를 동시 비교하니 `includeMcpJson:false` 패턴 즉시 발견. Brownfield 진단의 표준 절차로 다중 비교군 우선 — 글로벌 도메인 entry 승격 후보.

## Quick Reference

### 본 세션 메인
- `MICKEY-28-SESSION.md` (10 Completed, 6 Decisions, 8 Lessons, Files Modified 풀 목록)

### 변경 결과 (검증 대기)
- 글로벌+repo `knowledge-curator.json` — 변형 I 적용 (hash `45CAFB42A1152689`, size 12137)
- 백업: `.m28-bak` (H, 12139 bytes) 양쪽 보존
- 백업 누적: `.m24-bak`, `.m25-bak`, `.m26-bak`, `.m27-bak`, `.m28-bak` 5단계 모두 보존

### 신규 스크립트 (재사용 가능)
- `scripts/m28_compare_perm_fields.py` — mickey vs curator 권한 6필드 비교
- `scripts/m28_dump_curator_prompt.py` — Curator prompt + 메타 통계 dump
- `scripts/m28_compare_all_agents_mcp.py` — 글로벌 mcp.json + 모든 agent 의 MCP/legacy/include 비교 (★ 다중 비교군 진단의 핵심 도구)
- `scripts/m28_apply_curator_variant_i.py` — 변형 I 적용 (4-step safe-batch-replace, M27 패턴 6세대)

### Mickey 29 시작점
- HANDOFF 0순위 (변형 I 검증) 부터
- 검증 PASS → 1순위 (메타 교훈 글로벌 승격 + 정리 작업)
- 검증 FAIL → 2순위 (진단 종료 W 또는 R)

### Context window 인계 시점
~70% (작업 완료 + 정리 후)

### M29 시작 시 엔트로피 체크 결과 (예상)
- INDEX 정합성: ✅ (M27 갱신, M28 미수정)
- auto_notes 최신성: 2026-06-20 (M21 기준, 7세션 이내 — 임박)
- SESSION 아카이빙: M27, M28 루트에 잔존 (2건, 임계 미달)
- 구조 문서 최신성: ✅ (M27 갱신)
- dangling staging: ⚠️ 2건 (M28 진입 시 발견, Curator 정상화 후 처리)
- 포스트모템 트리거: 미확인 (M21 baseline 후 충분한 데이터 미확보)

### 본 진단 사이클 7세대 누적 통계

| 세대 | 세션 | 변형 | 결과 |
|------|------|------|------|
| 1 | M22 | (없음, 첫 발견) | EmptyResponse 발생 |
| 2 | M23 | (없음, 진단) | query/일시환경 가설 기각 + Kiro CLI 캐시 발견 |
| 3 | M24 | A2 | FAIL |
| 4 | M25 | A1 | FAIL |
| 5 | M26 | G3 | FAIL |
| 6 | M27 | H | FAIL |
| 7 | **M28** | **I (옵션 B)** | **검증 대기 (M29)** |

7세대 누적이라는 사실 자체가 [Protocol] 메타 교훈의 강력한 근거. PASS/FAIL 무관하게 본 진단 사이클의 학습 가치는 글로벌 도메인 entry 1~2건 승격 가치 충족.
