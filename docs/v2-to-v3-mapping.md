# v2 → v3 Mapping Matrix

- **작성일**: 2026-07-07 (Phase 2a)
- **목적**: v17 (agent JSON prompt 278줄, T1) + T1.5 (extended-protocols.md 19개 섹션) + 지식 그래프 노드가 v3 Power 자산으로 어떻게 이식·참조되는지 100% 추적성 확보
- **선행 문서**: `IMPROVEMENT-PLAN-v10-power-migration.md`
- **원본 dump**: `scripts/output/v17_prompt.md` (Phase 2a 정찰 산출)

---

## 1. 대응 원칙

| 원칙 | 내용 |
|------|------|
| **T1 = Steering** | v17 prompt 각 섹션은 v3 steering 6개 파일에 이식. 항상 로드되는 진입 계층 |
| **T1.5 = 그래프 노드** | `~/.kiro/mickey/extended-protocols.md` §1~§19는 원본 유지. steering은 트리거만 명시하고 필요 시 §N 참조 pull |
| **domain/patterns = 그래프 노드** | `~/.kiro/mickey/domain/entries/*.md`, `patterns/*.md`는 그대로 유지. steering은 INDEX·GRAPH 접근 규약만 명시 |
| **memorygraph 제거** | v10에서 memorygraph MCP 완전 배제. Curator는 파일 기반 그래프(INDEX + GRAPH + entries)를 직접 편집 |
| **code 관계 = 외부 도구 위임** | Serena + Graphify + Kiro CLI 내장 `code`가 코드 관계 그래프 담당 |

## 2. v3 Power 구조

```
power-mickey/
├── POWER.md                    # front matter + 활성화 트리거 + steering readSteering 매핑
├── mcp.json                    # aws-knowledge 유지, memorygraph 제거
└── steering/
    ├── mickey-core.md          # Core Identity + Communication + REMEMBER 12
    ├── session-protocol.md     # First/Continuing/During/End Session + Brownfield/§19/엔트로피 트리거
    ├── knowledge-graph.md      # 지식 그래프 접근 규약 (INDEX/GRAPH/PROFILE/entries/patterns/extended-protocols §N) + Curator 호출 규약
    ├── problem-solving.md      # 10단계 골격 + 심층 프로토콜(WELC/Backpressure/Behavioral) 트리거
    ├── document-schema.md      # 문서 스키마 표 (PURPOSE-SCENARIO 등)
    └── context-window.md       # 50/70/90 실행 규칙
```

## 3. T1 (v17 prompt) → Steering 매핑

| v17 섹션 | v17 줄 번호 | 이식 대상 steering | 비고 |
|---------|------------|-------------------|------|
| Core Identity | 3~8 | `mickey-core.md` | 그대로 이식. Postfix 넘버링 규약 포함 |
| COMMUNICATION PRINCIPLES (4개) | 10~17 | `mickey-core.md` | 그대로 이식 |
| SESSION PROTOCOL — First Session (Step 1~6) | 21~39 | `session-protocol.md` | T1.5 §1(Brownfield), §4(자율성), §19(코드 분석 도구) 트리거 유지 |
| SESSION PROTOCOL — Continuing Session (Step 1~4) | 41~55 | `session-protocol.md` | T1.5 §3(엔트로피), §9(포스트모템), §17(Curator), §19 트리거 유지 |
| SESSION PROTOCOL — During Session | 57~76 | `session-protocol.md` | 체크포인트 5/5 트리거. §13(세션 로그 품질), §10(Behavioral Scenario) 트리거 |
| SESSION PROTOCOL — Session End | 78~87 | `session-protocol.md` | §17 Curator 호출 규약 요약 + `knowledge-graph.md` 로 상세 위임 |
| DOCUMENT SCHEMA | 89~107 | `document-schema.md` | 10종 문서 스키마 표 그대로 이식 |
| PROBLEM-SOLVING — Before Implementation (10단계) | 111~127 | `problem-solving.md` | §2(Completion Criteria), §5(Subagent), §10(Behavioral) 트리거 |
| PROBLEM-SOLVING — Error Handling | 129~133 | `problem-solving.md` | §14(실행 중 이상 감지) 트리거 |
| PROBLEM-SOLVING — Anti-Patterns | 135~143 | `problem-solving.md` | 그대로 이식 |
| TOOL/SOLUTION SELECTION | 145~154 | `problem-solving.md` | 짧으므로 problem-solving 하위 절로 편입 |
| KNOWLEDGE MGMT — 3-Tier Loading | 158~175 | `knowledge-graph.md` | 표 그대로 이식. §12(Global Knowledge) 트리거 |
| KNOWLEDGE MGMT — 자동 메모리 (auto_notes/) | 177~202 | `knowledge-graph.md` | 저장소 성격 표 이식 |
| KNOWLEDGE MGMT — 파일 크기 제한 | 204~218 | `knowledge-graph.md` | 이중 가드 표 이식 |
| KNOWLEDGE MGMT — 지식 저장소 | 220~228 | `knowledge-graph.md` | common_knowledge/context_rule 정의 |
| KNOWLEDGE MGMT — 교훈 승격 | 230~232 | `knowledge-graph.md` | §17 Curator 진입점 명시 |
| KNOWLEDGE MGMT — 교훈 추출 기준 | 234~242 | `knowledge-graph.md` | 5가지 기준 이식 |
| CONTEXT WINDOW MANAGEMENT | 244~252 | `context-window.md` | 50/70/90 표 이식 |
| REMEMBER (12개 항목) | 254~267 | `mickey-core.md` | 12개 전부 이식. §11(Graduated REMEMBER) 트리거 |
| REMEMBER 크기 관리 | 269~271 | `mickey-core.md` | 12개 상한 + 은퇴 규칙 |

### 3.1 REMEMBER 12개 상세 추적 (계획서 CC)

| # | REMEMBER 원문 (요약) | steering 위치 | 연결 T1.5 §  |
|---|--------------------|--------------|-------------|
| 1 | 목적 우선 (PURPOSE-SCENARIO 최우선) | mickey-core.md | — |
| 2 | 단순함 우선 | mickey-core.md | — |
| 3 | Analysis BEFORE implementation | mickey-core.md | §10 (Behavioral Scenario) |
| 4 | 에러 로그 즉시 확인 | mickey-core.md | §14 (이상 감지) |
| 5 | User confirmation BEFORE changes | mickey-core.md | §4 (자율성 모드) |
| 6 | Root cause OVER quick fixes | mickey-core.md | — |
| 7 | 전제조건 우선 검증 | mickey-core.md | — |
| 8 | 점진적 도입 | mickey-core.md | — |
| 9 | 검증 기반 완료 (WELC) | mickey-core.md | §15 (Test Harness) |
| 10 | 자율 실행 조건 (AHOTL 3조건) | mickey-core.md | §4 (자율성 모드) |
| 11 | Backpressure | mickey-core.md | §6 (Backpressure) |
| 12 | 동작 시나리오 확인 필수 | mickey-core.md | §10 (Behavioral Scenario) |

### 3.2 Session Protocol 4단계 상세 추적 (계획서 CC)

| 단계 | v17 줄 | steering 위치 | 연결 T1.5 §  |
|------|--------|--------------|-------------|
| First Session | 21~39 | session-protocol.md #First-Session | §1 Brownfield / §4 자율성 / §19 코드 분석 |
| Continuing Session | 41~55 | session-protocol.md #Continuing-Session | §3 엔트로피 / §9 포스트모템 / §17 Curator / §19 |
| During Session | 57~76 | session-protocol.md #During-Session | §10 Behavioral / §13 세션 로그 품질 / §16 Machine Constraints |
| Session End | 78~87 | session-protocol.md #Session-End | §17 Curator (상세는 knowledge-graph.md에서 재확장) |

### 3.3 Problem-Solving 10단계 상세 추적 (계획서 CC)

| 단계 | v17 줄 | steering 위치 | 연결 T1.5 §  |
|------|--------|--------------|-------------|
| 1. 목적 재확인 | 112 | problem-solving.md | — (REMEMBER #1) |
| 2. 전제조건 검증 | 114 | problem-solving.md | — (REMEMBER #7) |
| 3. 데이터 구조 분석 | 116 | problem-solving.md | — |
| 4. 부작용 분석 | 118 | problem-solving.md | §7 Architectural Guard |
| 5. 유사 패턴 검색 | 120 | problem-solving.md | — |
| 6. 옵션 제시 (2개 이상) | 121 | problem-solving.md | §2 Completion Criteria |
| 6a. 동작 시나리오 확인 | 122~126 | problem-solving.md | §10 Behavioral Scenario |
| 7. 사용자 확인 | 127 | problem-solving.md | §4 자율성 모드 |
| 8. 최소 코드 구현 | 128 | problem-solving.md | — |
| 9. 버그 전파 확인 | 129 | problem-solving.md | — |
| 10. 검증 및 교훈 기록 | 130 | problem-solving.md | §15 Test Harness |

### 3.4 Document Schema 10종 상세 추적 (계획서 CC)

| 문서 | steering 위치 | 비고 |
|------|--------------|------|
| PROJECT-OVERVIEW.md | document-schema.md | 필수 섹션 7개 |
| PURPOSE-SCENARIO.md | document-schema.md | 최우선 로딩 대상 |
| ENVIRONMENT.md | document-schema.md | Autonomy Preference · Code Analysis Tools 포함 |
| FILE-STRUCTURE.md | document-schema.md | 필수/선택 섹션 분리 (§19 연동) |
| DECISIONS.md | document-schema.md | Options+Pros/Cons/Time/Risk |
| context_rule/project-context.md | document-schema.md | Lessons Learned 5개 상한 |
| context_rule/INDEX.md | document-schema.md | Rule Map 트리거 |
| common_knowledge/INDEX.md | document-schema.md | Knowledge Map 트리거 + Domain Links |
| auto_notes/NOTES.md | document-schema.md | 50줄 상한 |
| MICKEY-N-SESSION.md | document-schema.md | Checkpoint [0/5] + Purpose Alignment |
| MICKEY-N-HANDOFF.md | document-schema.md | 경량 문서 |

## 4. T1.5 (extended-protocols.md) — 그래프 노드로 유지

**원칙**: `~/.kiro/mickey/extended-protocols.md`는 그대로 유지. steering에는 트리거 문장만 두고 실제 상세는 세션 진행 중 필요할 때 pull.

| T1.5 § | 제목 | 트리거 위치 (steering) | 트리거 예시 |
|--------|------|---------------------|-----------|
| §1 | Brownfield 온보딩 | session-protocol.md | 기존 자산 감지 시 First Session Step 1b |
| §2 | Completion Criteria | problem-solving.md | Step 6 옵션 제시 시 |
| §3 | 엔트로피 관리 | session-protocol.md | Continuing Session Step 1b |
| §4 | 자율성 모드 (HITL/OHOTL/AHOTL) | mickey-core.md, session-protocol.md | 사용자 확인 여부 판단 시 |
| §5 | Subagent Delegation | problem-solving.md | 병렬 작업 2개↑ 감지 시 |
| §6 | Backpressure | problem-solving.md | 검증 실패 시 (REMEMBER #11) |
| §7 | Architectural Guard | problem-solving.md | 동일 아키텍처 위반 2회 감지 시 |
| §8 | Adaptive Rules (§17로 흡수됨) | knowledge-graph.md | 참조 리다이렉트 유지 |
| §9 | 포스트모템 프로토콜 | session-protocol.md, knowledge-graph.md | 10세션 경과 또는 3개월 잠복 후 |
| §10 | Behavioral Scenario Check | problem-solving.md, mickey-core.md | 구현 전 (REMEMBER #12) |
| §11 | Graduated REMEMBER | mickey-core.md | 포스트모템 시 재검토 |
| §12 | Global Knowledge | knowledge-graph.md | 승격 판단 시 |
| §13 | 세션 로그 기록 품질 | session-protocol.md | 설계 논의 기록 시 |
| §14 | 실행 중 이상 감지 | problem-solving.md | 도구 실행 중 warning 감지 시 |
| §15 | Test Harness (WELC) | problem-solving.md, mickey-core.md | 기존 코드 수정 시 (REMEMBER #9) |
| §16 | Machine Constraints Checkpoint | session-protocol.md | git push/deploy 명령 전 |
| §17 | Knowledge Lifecycle (Curator) | knowledge-graph.md, session-protocol.md | Session End Step 2 |
| §18 | Activity Metrics | knowledge-graph.md | 5/5 체크포인트 또는 포스트모템 시 |
| §19 | External Code Analysis Integration | session-protocol.md | First Session Step 4a, Continuing 엔트로피 체크 |

## 5. 지식 그래프 노드 (domain/patterns) — 원본 유지

**원칙**: steering은 **접근 규약**만 담고, 실제 노드는 사용자 홈에 그대로.

### 5.1 진입 인덱스 (T3a로 세션 시작 시 로딩)
- `~/.kiro/mickey/patterns/INDEX.md` — 도메인 무관 접근법 패턴 (6개, 상한 7)
- `~/.kiro/mickey/domain/INDEX.md` — 도메인 지식 (10개 entry)
- `~/.kiro/mickey/domain/GRAPH.md` — 노드 10개 + 엣지 14개 관계 맵
- `~/.kiro/mickey/domain/PROFILE.md` — 사용자 성향·판단 기준

### 5.2 접근 규약 (INDEX.md 정의, `knowledge-graph.md`에 이식)
1. **주 경로**: GRAPH.md Tags/Title 스캔 → Core 컬럼으로 즉시 판단 → entries/ 상세 (1홉)
2. **관계 탐색**: entry의 Links → 연결 entry (2홉)
3. **트리거 매칭**: INDEX 트리거 키워드 매칭 시 entry 직접 로딩

### 5.3 그래프 관리자 (Curator)
- `~/.kiro/mickey/domain/CURATOR-PROMPT.md` — Curator 프롬프트 원본 유지
- `knowledge-graph.md`는 Curator 호출 규약(입력·출력 형식·5회 검증 기간) 요약만 담고 상세는 CURATOR-PROMPT.md 참조

## 6. mcp.json 변환

### 6.1 기존 (`power-mickey/mcp.json`)
```json
{
  "mcpServers": {
    "memorygraph": { "command": "memorygraph", "args": ["--profile", "extended"] }
  }
}
```

### 6.2 신규 (v10)
```json
{
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "url": "https://knowledge-mcp.global.api.aws",
      "type": "http",
      "disabled": false
    }
  }
}
```

**변경 근거**:
- `memorygraph` 제거: 사용자 결정(2026-07-04). 파일 기반 그래프로 대체
- `aws-knowledge-mcp-server` 유지: 사용자 홈 전역에도 등록돼 있지만, Power 활성 시 명시적으로 로드 보장
- `serena`, `graphify-mcp`: 사용자 홈 전역 mcp.json에 이미 등록. Power에는 미포함(도구 발견은 코드 프로젝트에서 감지 시 자동)

## 7. 폐기 항목 (Phase 2b 실행 시 대체)

| 파일 | 상태 | 대체 |
|------|------|------|
| `power-mickey/POWER.md` (기존 IDE 시절) | 폐기 예정 | 새 POWER.md |
| `power-mickey/steering/mickey-core.md` (기존) | 폐기 예정 | 새 mickey-core.md |
| `power-mickey/steering/session-protocol.md` (기존) | 폐기 예정 | 새 session-protocol.md |
| `power-mickey/steering/problem-solving.md` (기존) | 폐기 예정 | 새 problem-solving.md |
| `power-mickey/steering/memory-protocol.md` (기존) | 폐기 예정 | `knowledge-graph.md`로 대체 |
| `power-mickey/steering/self-improvement.md` (기존) | 폐기 예정 | `knowledge-graph.md` 로 흡수 (Curator 호출 규약) |
| `power-mickey/mcp.json` (기존, memorygraph) | 폐기 예정 | 새 mcp.json |

**백업**: `power-mickey.pre-v10-bak.zip` (Phase 0에서 완료). 롤백 시 압축 해제만.

## 8. 검증 계획 (Phase 2c)

`scripts/verify_power_structure.py` (Test Harness) 항목:
1. **파일 존재**: POWER.md + mcp.json + steering/*.md 6개
2. **front matter 유효성**: POWER.md name/description/keywords 존재
3. **readSteering 매핑 완결성**: POWER.md 안내가 steering 6개 모두 커버
4. **T1 추적성**: v17 prompt 원문 dump(`scripts/output/v17_prompt.md`)의 핵심 키워드가 steering 어딘가에 존재
   - REMEMBER 12개 (핵심 키워드 검색)
   - Session Protocol 4단계 헤딩
   - Document Schema 10종 파일명
   - Problem-Solving 10단계 번호
5. **T1.5 트리거 존재**: 본 매트릭스 §4 표의 트리거 예시 문구가 지정 steering에 존재
6. **양쪽 분기 병기** (P3): 조건부 지시 문구 검색 시 부정 조건도 함께 존재

## 9. 회귀 안전망

- v2 CLI 엔진 (`--agent-engine v2`)은 계속 v17 agent JSON을 사용하므로 이 마이그레이션의 영향 없음
- v3 Power는 별도 자산이므로 v2와 병존
- 사용자 홈 `~/.kiro/mickey/*` 는 v2/v3 공용 서고 (변경 금지)

---

**Last Updated**: 2026-07-07 (Phase 2a)
