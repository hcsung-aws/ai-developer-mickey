# IMPROVEMENT PLAN: 프로젝트 지식 파일 관계 명시 표준화 + INDEX 동기화

> Source: Mickey 34 (2026-07-02) — 지식 그래프 시각화 도구 개발 중 발견
> Target: Mickey 35 이후 착수 예정 (옵션 B, `IMPROVEMENT-PLAN-v9.1` 계열 별도 개편)

## 배경

### 발견된 상태

Mickey 34에서 프로젝트 지식 그래프 시각화 도구를 구축하는 과정에서, 프로젝트 지식 파일들의 관계 정보가 **파일 본문과 INDEX.md 표 사이 out-of-sync** 상태임이 실측 확인됨.

**본 프로젝트(ai-developer-mickey) 실측**:
```
파일 본문 domain 참조: 9건
├─ common_knowledge/agent-design-patterns.md: 2건 (교차 참조 문구)
├─ common_knowledge/windows-user-path-extension.md: 3건 (## Related 섹션)
├─ common_knowledge/kiro-cli-lsp-init-settings-location.md: 3건 (## Related 섹션)
└─ context_rule/project-context.md: 1건 (Lessons Learned 안)

INDEX.md Domain Links 표 등록: 6건
→ M33 신규 파일 2개의 6개 참조 + project-context 1건 = 7건 미등록
```

### 근본 원인

1. **Document Schema 결여**: 현재 프로토콜 (T1 Document Schema) 에서 `common_knowledge/INDEX.md` 필수 섹션은 `Knowledge Map` + `Last Updated` 만. Domain Links 는 선택사항이며 표준 형식도 없음.
2. **Curator 지침 결여**: 새 지식 파일 승격 시 파일 본문 `## Related` 를 INDEX Domain Links 로 동기화하는 규칙이 CURATOR-PROMPT.md 에 없음.
3. **자연 형식 발달**: M33 에서 `## Related` 섹션이 신규 파일에 자연 도입됐지만 프로토콜화 안 됨.

### 왜 지금 개선해야 하는가

- **시각화 도구(Mickey 34) 완성으로 도구가 관계를 그래프로 렌더** → out-of-sync 가 즉시 눈에 보임
- **본문 파싱을 통해 자동 진단 가능** — 도구가 out-of-sync 를 리포트하므로 승격 시 확인 절차에 편입 가능
- **Passive > Active 원칙 강화** — 관계가 본문에도 있어야 파일을 여는 사용자/에이전트가 자연 발견

## 목표 (Acceptance Criteria)

1. **T1 Document Schema 갱신**: `common_knowledge/INDEX.md` 필수 섹션에 `Domain Links` 추가. 표 형식(트리거/entry/힌트) 명시
2. **`## Related` 섹션 표준화**: 지식 파일 신규 생성/수정 시 이 섹션 필수. 형식은 `common_knowledge/knowledge-file-relation-annotation.md` 참조
3. **CURATOR-PROMPT.md 갱신**: staging → 정식 위치 이동 시 (a) 파일 본문 `## Related` 확인 (b) INDEX Domain Links 표 동시 갱신
4. **엔트로피 체크에 out-of-sync 진단 추가**: 세션 시작 시 `scripts/mickey_graph_viz.py --scope project` 실행 후 WARNING 로그 확인 (또는 별도 진단 스크립트)
5. **본 프로젝트의 out-of-sync 3파일 7건 정리**: 진단된 항목들을 INDEX 에 등록

## Phase 분해

### Phase 1 — 프로토콜 문서 갱신 (T1 Document Schema)

**대상**: `examples/ai-developer-mickey.json` (repo) + `~/.kiro/agents/ai-developer-mickey.json` (활성) + `mickey/extended-protocols.md` (repo) + `~/.kiro/mickey/extended-protocols.md` (활성)

**변경**:
- Document Schema 표에서 `common_knowledge/INDEX.md` 필수 섹션 확장: `Knowledge Map`, `Domain Links (선택 시 표 형식)`, `Last Updated`
- Domain Links 표 형식 명시: `| 트리거 | Domain Entry | 힌트 |`

**패턴**: `safe-batch-replace` 11세대 (4-step + post-check)

### Phase 2 — CURATOR-PROMPT 갱신

**대상**: `mickey/domain/CURATOR-PROMPT.md` (repo) + `~/.kiro/mickey/domain/CURATOR-PROMPT.md` (활성)

**변경**:
- staging → 정식 위치 이동 절차에 "본문 `## Related` 파싱 → INDEX Domain Links 갱신" 단계 추가
- Anti-pattern 예시 (관계 한 곳에만 두는 케이스)

### Phase 3 — 지식 파일 표준 형식 문서화

**대상**: `common_knowledge/knowledge-file-relation-annotation.md` (Mickey 34 pre-staged)

**변경**: 사용자 승인 후 정식 위치로 이동

### Phase 4 — 엔트로피 체크 확장

**대상**: T1 SESSION PROTOCOL Continuing Session Step 1b (엔트로피 체크)

**변경**:
- "INDEX Domain Links 동기화 상태" 항목 추가
- 진단 방법: `python scripts/mickey_graph_viz.py --scope project --project-path .` WARNING 로그 확인
- 또는 별도 lightweight 스크립트 (out-of-sync 검사 전용)

### Phase 5 — 본 프로젝트 정리 (out-of-sync 해소)

**대상**: 본 프로젝트 `common_knowledge/INDEX.md` Domain Links 표

**변경**: Mickey 34 진단 결과 7건 등록
- `agent-design-patterns.md`: forced-breakpoint-execution, passive-over-active-retrieval (이건 이미 INDEX 있는지 재확인 후)
- `windows-user-path-extension.md`: powershell-curl-escape, cli-help-output-distrust, deploy-output-distrust
- `kiro-cli-lsp-init-settings-location.md`: cli-help-output-distrust, empty-scan-distrust, llm-path-normalization
- `project-context.md`: iterative-measurement-deepening (이건 context_rule 이므로 별도 결정)

## 리스크 및 대안

| 리스크 | 완화 |
|--------|------|
| 프로토콜 편집 실수로 이전 지시 깨짐 | safe-batch-replace 4-step + hash 검증 (반복 검증 패턴) |
| 기존 지식 파일들의 대량 out-of-sync 발견 → 정리 부담 | Phase 5 는 발견되는 대로 정리, 신규 파일부터 표준 준수 |
| `## Related` 섹션 자연스러움 유지 vs 강제 필수 사이 균형 | Curator 가 승격 시 확인, 사용자 최종 승인 흐름 유지 |
| CURATOR-PROMPT 갱신이 EmptyResponse 이슈로 검증 어려움 | Mickey 본체가 승격 처리 (M22~M33 우회 흐름 유지). Curator fix 후 재검증 |

## 착수 조건

1. Mickey 34 종료 후 사용자가 정식 착수 결정
2. Mickey 35 세션 시작 시 이 문서를 T2 로 로딩하여 계획 참조
3. safe-batch-replace 11세대 (4-step) 로 프로토콜 편집 수행

## Last Updated
2026-07-02 (Mickey 34)
