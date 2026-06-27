# Curator 진단 사이클 사실 데이터 (M22~M29)

> 본 사이클 7세대 진단 도중 발견된 재사용 가능한 사실 데이터.
> 향후 Kiro CLI 측 fix 적용 후 재검증 또는 다른 subagent 진단 시 참조.

## Last Verified
2026-06-26 (Mickey 29)

---

## 1. 글로벌 설정 파일 위치

| 파일 | 경로 | 용도 |
|------|------|------|
| 글로벌 mcp.json | `~/.kiro/settings/mcp.json` | MCP server 등록 (3개: aws-knowledge / aws-api / serena) |
| 글로벌 agents 디렉토리 | `~/.kiro/agents/` | 모든 활성 agent JSON 위치 |
| 글로벌 mickey patterns | `~/.kiro/mickey/patterns/` | patterns/INDEX.md + 개별 패턴 |
| 글로벌 mickey domain | `~/.kiro/mickey/domain/` | INDEX.md + GRAPH.md + entries/ |
| 글로벌 Curator staging | `~/.kiro/mickey/_curator-staging/` | 패턴/REMEMBER 후보 (Pre-staged Apply) |
| 글로벌 skills | `~/.kiro/skills/` | aws-cost-management 등 |
| Mickey 본체 prompt | `~/.kiro/agents/ai-developer-mickey.json` | system_prompt 본문 |
| Curator 본체 prompt | `~/.kiro/agents/knowledge-curator.json` | system_prompt 본문 |

## 2. 정상 동작 subagent 비교군 (M28 발견)

본 진단 사이클에서 정상 동작하는 비교군으로 활용된 agent.

| Agent | 핵심 차이 (Curator FAIL 대비) | 비고 |
|-------|----------------------------|------|
| kiro-learning-helper | `includeMcpJson:false` 명시 + mcpServers inline 2개 정의 | 정상 동작 |
| mockdb-test-agent | `includeMcpJson:false` 명시 + mcpServers inline 2개 정의 | 정상 동작 |
| ai-developer-mickey | `useLegacyMcpJson:false` + mcpServers inline 2개 정의 (`includeMcpJson` 미명시) | 정상 동작 |
| knowledge-curator (FAIL) | `mcpServers={}` + (M28 시점) `useLegacyMcpJson:false` 만 | EmptyResponse |

다중 비교군 분석 절차는 `scripts/m28_compare_all_agents_mcp.py` 에 자동화되어 재실행 가능.

## 3. 외부 이슈 트래커 매칭 회귀 (M28 발견)

| 출처 | 이슈 | 패턴 |
|------|------|------|
| Anthropic claude-code | Issue #17743 | "Task tool subagents fail with 0 tool uses when MCP servers configured" |
| Anthropic claude-code | Issue #10739 | "Subagents return empty response with zero tool uses" |
| Kiro | Issue #6163 | "subagent stuck 0 tool uses · 0.00s" |

본 사이클 종결 후에도 fix 모니터링 시 위 이슈들의 상태 변화 확인 필요.

## 4. Kiro CLI 매뉴얼 URL (M28 정독)

| 섹션 | 용도 |
|------|------|
| configuration-reference | agent JSON 정식 필드 (`includeMcpJson` 명시, `useLegacyMcpJson` 미명시 = deprecated) |
| chat/subagents | subagent 동작 모델 (non-interactive, fail fast) |
| troubleshooting | 일반 오류 처리 가이드 |
| examples | agent JSON 예시 |
| changelog 0.9 | 최신 변경 사항 |

## 5. Curator 변형 백업 누적 (.m24 ~ .m29-bak)

| 백업 | 변형 | 크기 | hash | 비고 |
|------|------|------|------|------|
| `.m24-bak` | 원본 | 11797 bytes | (구) | tools=4건 + allowedTools=4건 |
| `.m25-bak` | A2 | 11748 bytes | (구) | tools=["*"] + allowedTools=4건 |
| `.m26-bak` | A1 | 11688 bytes | (구) | tools=["*"] + allowedTools=[] |
| `.m27-bak` | G3 | 11757 bytes | (구) | + mcpServers={}, useLegacyMcpJson=false, model=null |
| `.m28-bak` | H | 12139 bytes | `F65CAF62C5DBDD0F` | + resources, toolsSettings.execute_bash, toolsSettings.subagent |
| `.m29-bak` | I | 12137 bytes | `45CAFB42A1152689` | useLegacyMcpJson 제거, includeMcpJson:false 추가 |
| 본체 (M29 원복 후) | **H** | 12139 bytes | `F65CAF62C5DBDD0F` | M27 검증된 변형 단계 |

위치: 글로벌 `~/.kiro/agents/` + repo `examples/` 양쪽.

## 6. safe-batch-replace 4-step 패턴 (7세대 안정)

본 사이클 도중 7세대 연속 안정 작동한 변형 적용/원복 절차.

### 절차
1. **Precondition**: 본체 hash + 시작점 백업 hash + size 사전 검증
2. **Backup**: 본체를 새 백업으로 보존 (역방향 변형도 추적성)
3. **Apply**: 시작점 백업 → 본체 양쪽 (글로벌 + repo)
4. **Post-check**: 본체 hash 양쪽 일치 + 목표 hash 일치 검증

### 적용 사례 (M25 ~ M29)
- M25 A1, M26 G3, M27 H, M28 I, M29 원복 (H 복원), 그 외

### 스크립트 패턴
- `scripts/mNN_apply_curator_variant_X.py` — 변형 적용
- `scripts/mNN_revert_to_X.py` — 원복 (역방향 변형)
- `scripts/mNN_precheck_revert.py` — 사전 진단 (선택적)

## 7. 진단 도구 스크립트 (M22~M29 누적)

| 스크립트 | 용도 |
|----------|------|
| `scripts/m28_compare_perm_fields.py` | mickey vs curator 권한 6필드 비교 |
| `scripts/m28_dump_curator_prompt.py` | Curator prompt + 메타 통계 dump |
| `scripts/m28_compare_all_agents_mcp.py` | ★ 글로벌 mcp.json + 모든 agent 의 MCP/legacy/include 비교 (다중 비교군 진단 핵심 도구) |
| `scripts/m29_precheck_revert.py` | 원복 전 디스크 6항목 사전 검증 |
| `scripts/m29_revert_to_h.py` | 변형 I → H 원복 (4-step) |

## 8. Curator 호출 상태 (외부 fix 대기 중)

- 본 시점 (M29) Curator subagent 호출은 모두 `AgentLoopError(EmptyResponse)` 반환
- 진화 루프는 prompt 흐름으로만 작동 (Mickey 본체가 직접 처리)
- 글로벌 `domain/` 직접 수정은 가능 (Curator 외 경로 — Mickey 본체 자율성 Level 2 권한)
- `_curator-staging/` Pre-staged Apply 흐름은 일시 정지

## 9. 글로벌 자산 동시 갱신 패턴 (M29 발견)

- 본 세션 도중 다른 프로젝트 (gamejob_crawler Mickey 32) 가 같은 `domain/INDEX.md` + `domain/GRAPH.md` 갱신
- Last Updated 줄에 양쪽 갱신 정보 보존 (세미콜론 구분) 패턴 적용
- 글로벌 자산 갱신 시 의무 절차: ① 디스크 재확인 → ② 충돌 회피 → ③ Last Updated 양쪽 보존

---

## Mickey 30+ 재검증 시작점

Kiro CLI 측 fix 적용 후 재검증 절차:
1. 본 시점 H 본체 (hash `F65CAF62C5DBDD0F`) 그대로 ping 시도
2. PASS 면 모든 변형 시도 무의미했음 (외부 회귀 단독 원인) → 7세대 종결 + Curator 검증 기간 1/5 카운트 시작
3. FAIL 이면 변형 I 재적용 (`.m29-bak` 그대로 사용, hash `45CAFB42A1152689`) 또는 다른 차원 진단
