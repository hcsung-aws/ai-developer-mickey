# File Structure

> 스키마: T1.5 §19. Mickey 는 first-step 지도 + Mickey 문서 위치 + 도구 감지 결과 유지. 상세 코드 분석은 Tier 1/2/3 도구에 위임.

## Directory Tree (depth 2)

```
ai-developer-mickey/
├── docs/                          # 핵심 가이드 문서 (한/영 페어) + case-study/, images/
├── sessions/                      # 세션 로그 아카이브 (MICKEY-N-SESSION/HANDOFF ~M45), packet-capture/, self/
├── session_history/               # 병렬 v10 마이그레이션 트랙 세션 로그 (파일명: YYYY-MM-DD-*)
├── examples/                      # 에이전트 JSON (ai-developer-mickey.json T1 v20, knowledge-curator.json)
├── context_rule/                  # 프로젝트 특화 규칙 (T3a→T3b) + adaptive.md (Curator 직접 수정, 19건)
├── common_knowledge/              # 범용 패턴 지식 (T3a→T3b)
├── auto_notes/                    # AI 자동 관찰 기록 (T3a)
├── mickey/                        # 글로벌 지식 저장소의 설치 seed 골격 (미러 아님 — mickey/README.md 계약, M44)
├── power-mickey/                  # v10 Power (POWER.md + mcp.json + steering/ 7개). 작업은 mickey-power 브랜치
├── _curator-staging/              # Curator staging (승격 초안 + invoke/promote 리포트, gitignored)
├── .kiro/                         # hooks/ (v10 SessionStart) + scripts/ (session boot/close) + settings/lsp.json
├── .serena/                       # Serena LSP 메모리 (Tier 1)
├── scripts/                       # 세션·배포 인프라 + 진단 스크립트 + mickey_graph/ 시각화 도구
│   ├── invoke_curator.py          # Curator 유일 진입점 (curation 락 + 재시도 + Base-Hash 자동 기입)
│   ├── promote_knowledge.py       # 글로벌 domain 승격 전담 (promote 락 + 무결성 검증/롤백)
│   ├── mickey_lock.py             # 공유 락 모듈 (curation/promote 공용)
│   ├── graph_audit.py             # 글로벌 그래프 무결성 감사 (§3-8 상비 도구)
│   ├── m43_deploy_global_scripts.py  # repo scripts/ → ~/.kiro/mickey/scripts/ 재배포 (adaptive #16)
│   ├── deploy_power.py            # v10 Phase 5: v3 power 배포
│   ├── mickey_graph/              # 지식 그래프 시각화 (models/parser/builder/renderer + templates/ + vendor/)
│   ├── tests/                     # WELC 회귀 테스트 (M48 시점 전체 167 passed)
│   └── m2x_~m4x_*.py              # 세션별 진단/적용 스크립트
├── install.sh / install.ps1       # 설치 스크립트 (agent JSON + 글로벌 가이드 + 스크립트 + v3 power)
├── PURPOSE-SCENARIO.md            # 최종 목적 + 사용 시나리오 (T2)
├── PROJECT-OVERVIEW.md            # 프로젝트 개요 (T2)
├── ENVIRONMENT.md                 # 환경 정보 (T2)
├── FILE-STRUCTURE.md              # 본 파일
├── DECISIONS.md                   # 의사결정 로그
├── GRAPH-HEALTH-BASELINE-2026-08-25.md   # 글로벌 그래프 건전성 baseline (M44 동결)
├── POSTMORTEM-2026-05-14.md / POSTMORTEM-2026-08-21.md   # 포스트모템 (M20 / M43)
├── IMPROVEMENT-PLAN-v{6.3,7,8,8.1,9,9-ADDENDUM,10-power-migration}.md   # 버전별 개선 계획
├── IMPROVEMENT-PLAN-{project-knowledge-index-sync,progressive-domain-hierarchy}.md
├── VERIFICATION-PLAN-v3-power-runtime.md   # v3 런타임 실측 검증 계획 (V1~V8 닫힘)
├── MICKEY-4x-{SESSION,HANDOFF}.md # 최근 세션 로그 (루트 3개 초과 시 sessions/로 아카이빙)
├── power-mickey.pre-v10-bak.zip   # v10 마이그레이션 전 power-mickey/ 백업
└── README.md / README-en.md       # 프로젝트 소개
```

## Mickey Docs Locations

| 유형 | 경로 | 로딩 시점 |
|------|------|----------|
| T2 자동 로딩 | `PURPOSE-SCENARIO.md`, `PROJECT-OVERVIEW.md`, `ENVIRONMENT.md`, `FILE-STRUCTURE.md`(본 파일), `DECISIONS.md`, `context_rule/project-context.md`, `context_rule/adaptive.md` | 세션 시작 |
| T3a 인덱스 | `context_rule/INDEX.md`, `common_knowledge/INDEX.md`, `auto_notes/NOTES.md` | 세션 시작 |
| 세션 로그 | 루트 `MICKEY-N-{SESSION,HANDOFF}.md` (최신), 과거분 `sessions/` | 최신 HANDOFF 자동 |
| 개선 계획/기준선 | `IMPROVEMENT-PLAN-v*.md`, `POSTMORTEM-*.md`, `GRAPH-HEALTH-BASELINE-*.md` | 참조 시 |
| 글로벌 seed | `mickey/extended-protocols.md` (세대 파일 — global과 hash 동기), `mickey/domain/`, `mickey/patterns/` | install로 `~/.kiro/mickey/` 배포 (seed 시맨틱) |
| 에이전트 설정 | `examples/ai-developer-mickey.json` (T1 v20), `examples/knowledge-curator.json` | install로 `~/.kiro/agents/` 배포 |

## Code Analysis Tools (§19 감지 결과, M49 갱신)

| Tier | 도구 | 감지 여부 | 비고 |
|------|------|----------|------|
| Tier 1 | Serena | `.serena/` 감지 | **§19.3 fail-closed 규약 (M47~48 검증)**: `--project` 기동 인자 없이 운용, 세션 시작 시 `activate_project` 의무 + 활성 확인 전 쓰기 금지 |
| Tier 1 | Graphify | `graphify-out/` 미감지 | 필요 시 `uv tool install graphifyy` + `/graphify .` 도입 가능 |
| Tier 3 | Kiro CLI 내장 `code` (baseline) | 항상 활성. LSP 활성 (`.kiro/settings/lsp.json`) | `/code init` 실 산출물 위치는 문서 표기와 불일치 (common_knowledge 참조) |

**권장 액션**: 정밀 코드 분석 시 Serena 우선, refactoring/diagnostics 는 내장 `code` LSP.

## Steering Trigger

- **기준값**: git 추적 파일 357 (Mickey 49, 2026-09-05 실측)
- **재분석 조건**: 전체 파일 중 10% 이상 변경/추가 (약 36 파일)
- **마지막 재분석**: Mickey 49 (2026-09-05) — 본 문서 + ENVIRONMENT.md 일괄 현행화 (M35 트리거 도달분 해소)

---

## 선택 섹션

### Key Files

| 파일 | 역할 |
|------|------|
| `examples/ai-developer-mickey.json` | 최신 시스템 프롬프트 (T1 v20) — install로 `~/.kiro/agents/` 배포 |
| `examples/knowledge-curator.json` | Knowledge Curator subagent (prompt SoT는 CURATOR-PROMPT.md, m37_sync 스크립트로 동기화) |
| `mickey/extended-protocols.md` | T1.5 글로벌 가이드 seed (v28, §1~§22) |
| `scripts/invoke_curator.py` | Curator 호출 유일 진입점 — curation 락 + 스로틀 재시도 + staging diff 실측 + Base-Hash 자동 기입 (M48) |
| `scripts/promote_knowledge.py` | 글로벌 domain 승격 전담 — promote 락 + 백업 + 무결성 검증/자동 롤백 |
| `scripts/mickey_lock.py` | 락 공유 모듈 (curation/promote 공용) |
| `scripts/graph_audit.py` | 글로벌 그래프 무결성 감사 (엔트로피 체크 §3-8 상비) |
| `scripts/m43_deploy_global_scripts.py` | repo scripts/ → 글로벌 재배포 (FILES 목록 등재 확인 — adaptive #17) |
| `scripts/deploy_power.py` + `verify_deploy_power.py` | v10 v3 power 배포 + 테스트 하니스 |
| `scripts/tests/` | WELC 회귀 테스트 (M48 시점 167 passed) |
| `context_rule/adaptive.md` | Curator 직접 수정 영역 (반복 패턴 19건) |
| `scripts/m21_measure_usage.py` | 활용도 baseline 측정 (§18 Activity Metrics) |
| `scripts/mickey_graph_viz.py` | 지식 그래프 시각화 CLI 진입점 (--scope global/project) |

### File Statistics

- **총 파일 수**: git 추적 357 (M49 실측)
- **주요 구성**: Markdown (가이드/세션 로그), JSON (에이전트), Python (인프라/진단 스크립트)

### Project Structure Pattern

**문서 중심 + 자기 개선 루프** — 에이전트 설정(JSON) + 가이드 문서(Markdown) + 세션 로그 + 인프라 스크립트가 함께 진화. SESSION/HANDOFF 임계 3 초과 시 `sessions/` 로 아카이빙하여 루트 가시성 유지. 상세 코드 관계 분석은 외부 도구(Serena/내장 code) 위임. 글로벌 지식 반영은 Curator(staging) → promote 스크립트(락) 이원 구조.

## Last Updated
2026-09-05 (Mickey 49 — 전면 현행화: 트리 갱신(_curator-staging, baseline/postmortem, 세션 인프라 스크립트), T1 v20/T1.5 v28 반영, Steering 기준값 357 재설정, §19.3 규약 반영)
