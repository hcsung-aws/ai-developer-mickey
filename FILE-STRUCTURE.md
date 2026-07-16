# File Structure

> 스키마: T1.5 §19 (v17). Mickey 는 first-step 지도 + Mickey 문서 위치 + 도구 감지 결과 유지. 상세 코드 분석은 Tier 1/2/3 도구에 위임.

## Directory Tree (depth 2)

```
ai-developer-mickey/
├── docs/                          # 핵심 가이드 문서 (한/영 페어) + case-study/, images/
├── sessions/                      # 세션 로그 아카이브 (MICKEY-N-SESSION/HANDOFF), packet-capture/, self/
├── session_history/               # 병렬 v10 마이그레이션 트랙 세션 로그 (파일명: YYYY-MM-DD-*)
├── examples/                      # 에이전트 JSON + 예시 (ai-developer-mickey.json v17, knowledge-curator.json)
├── context_rule/                  # 프로젝트 특화 규칙 (T3a→T3b)
├── common_knowledge/              # 범용 패턴 지식 (T3a→T3b)
├── auto_notes/                    # AI 자동 관찰 기록 (T3a)
├── mickey/                        # 글로벌 가이드 원본 (install.sh → ~/.kiro/mickey/)
├── power-mickey/                  # v10 Power 재건 (POWER.md + mcp.json + steering/ 7개: 상시 6 + manual 1). 구 실험본은 .pre-v10-bak.zip
├── .kiro/hooks/                   # v10 Phase 3: CLI v3 hook 1(SessionStart, 발화 실측 확인) + IDE skeleton 2 + README. Stop hook 은 F5 로 폐기(per-response 실측)
├── .kiro/scripts/                 # v10 Phase 3: mickey_session_boot.py / mickey_session_close.py (hook 얇게, 로직은 여기)
├── scripts/                       # 진단/적용 스크립트 + mickey_graph/ 시각화 도구
│   ├── mickey_graph/              # 지식 그래프 시각화 (models/parser/builder/renderer + templates/ + vendor/)
│   ├── mickey_graph_viz.py        # CLI 진입점 (--scope global/project)
│   ├── setup_vendor.py            # vis-network 다운로드/검증
│   ├── verify_offline.py          # 오프라인 렌더 검증
│   ├── tests/                     # WELC 회귀 테스트 (parser/builder/renderer, 101 passed)
│   ├── output/                    # 렌더 산출물 (gitignored)
│   ├── backup/                    # PATH/설정 백업 (M33+)
│   └── m2x_*.py, m3x_*.py         # 세션별 진단/적용 스크립트
├── .serena/                       # Serena LSP 메모리 (M35 시점 프로젝트 루트에 등장)
├── install.sh / install.ps1       # 설치 스크립트 (bash + PowerShell)
├── PURPOSE-SCENARIO.md            # 최종 목적 + 사용 시나리오 (T2)
├── PROJECT-OVERVIEW.md            # 프로젝트 개요 (T2)
├── ENVIRONMENT.md                 # 환경 정보 (T2)
├── FILE-STRUCTURE.md              # 본 파일
├── DECISIONS.md                   # 의사결정 로그
├── IMPROVEMENT-PLAN-v{6.3,7,8,8.1,9,9-ADDENDUM,10-power-migration}.md   # 버전별 개선 계획
├── IMPROVEMENT-PLAN-{project-knowledge-index-sync,progressive-domain-hierarchy}.md   # 최근 개선안
├── POSTMORTEM-2026-05-14.md       # M20 v8.1 활용도 진단
├── power-mickey.pre-v10-bak.zip   # v10 마이그레이션 전 power-mickey/ 백업
└── README.md / README-en.md       # 프로젝트 소개
```

## Mickey Docs Locations

| 유형 | 경로 | 로딩 시점 |
|------|------|----------|
| T2 자동 로딩 | `PURPOSE-SCENARIO.md`, `PROJECT-OVERVIEW.md`, `ENVIRONMENT.md`, `FILE-STRUCTURE.md`(본 파일), `DECISIONS.md`, `context_rule/project-context.md`, `context_rule/adaptive.md` | 세션 시작 |
| T3a 인덱스 | `context_rule/INDEX.md`, `common_knowledge/INDEX.md`, `auto_notes/NOTES.md` | 세션 시작 |
| 세션 로그 | `sessions/MICKEY-N-{SESSION,HANDOFF}.md` (M31, 진행중 M32) | 최신 HANDOFF 자동 |
| 개선 계획 | `IMPROVEMENT-PLAN-v*.md`, `POSTMORTEM-*.md` | 참조 시 |
| 글로벌 미러 | `mickey/extended-protocols.md` (v17), `mickey/domain/`, `mickey/patterns/` | install.sh 로 `~/.kiro/mickey/` 배포 |
| 에이전트 설정 | `examples/ai-developer-mickey.json` (v17), `examples/knowledge-curator.json` | install.sh 로 `~/.kiro/agents/` 배포 |

## Code Analysis Tools (§19 감지 결과, Mickey 35)

| Tier | 도구 | 감지 여부 | 비고 |
|------|------|----------|------|
| Tier 1 | Serena | 프로젝트 루트 `.serena/` **감지 (M35 시점)** | M32 이후 등록 완료. 상세 메모리는 `.serena/memories/` 확인 |
| Tier 1 | Graphify | `graphify-out/` 미감지 | 필요 시 `uv tool install graphifyy` + `graphify install` + `/graphify .` 로 도입 가능 |
| Tier 3 | Kiro CLI 내장 `code` (baseline) | 항상 활성. Pyright + TS + clangd LSP 활성(M33) | `/code init` 실 산출물 = `.kiro/settings/lsp.json` (§19.2 표기와 불일치 — 감지 마커 보정 후보) |

**권장 액션**: Tier 1 Serena 감지 확정 → 정밀 코드 분석 시 Serena 우선 활용. Tier 3 pyright 로 python 파일 diagnostics 즉시 확인 가능.

## Steering Trigger

- **기준값**: 총 파일 수 ~140 (Mickey 27 시점 기록)
- **재분석 조건**: 전체 파일 중 10% 이상 변경/추가 (약 14 파일)
- **마지막 재분석**: Mickey 27 (2026-06-23)
- **M32~M35 누적 변경분**: scripts/mickey_graph/** (Python 5 + template 1 + vendor 1 + tests 5 + fixtures 5), scripts/mickey_graph_viz.py, setup_vendor.py, verify_offline.py, m33_*.py 6, m34_*.py 4, common_knowledge/ 신규 3, session_history/ 3, IMPROVEMENT-PLAN 3, sessions/ 신규 10, .serena/ 등록, 각종 백업 → **총 50+ 파일 신규/변경**. **10% 크게 초과, 재분석 트리거 도달**
- **재분석 계획**: 별도 유지보수 세션에서 전체 문서(PROJECT-OVERVIEW/ENVIRONMENT/FILE-STRUCTURE) 일괄 갱신 예정. M35 는 CLI 트랙 정합성 복원 스코프 한정 최소 갱신

---

## 선택 섹션 (Tier 3 만 사용 중 → 유지 권장, §19.3 참조)

### Key Files

| 파일 | 역할 |
|------|------|
| `examples/ai-developer-mickey.json` | 최신 시스템 프롬프트 (v17) — `install.sh/ps1` 로 `~/.kiro/agents/` 배포 |
| `examples/knowledge-curator.json` | Knowledge Curator subagent (M27 변형 H 이후 유지) |
| `mickey/extended-protocols.md` | T1.5 글로벌 가이드 (v17, §1~§19) |
| `install.sh` / `install.ps1` | Agent JSON + 글로벌 가이드 설치 (3 파일 동기화) |
| `power-mickey/POWER.md` | v10 Power 온보딩 지침 (steering 매핑 + 활성화 트리거 + 세션 정리 흐름) |
| `power-mickey/steering/knowledge-curator.md` | Curator 호출 계약 (inclusion: manual, 세션 종료 시 readSteering) |
| `scripts/verify_power_structure.py` | v10 power 구조 검증기 (steering 7 · front matter · T1 추적성 · P3 · inclusion 모드, 7/7) |
| `scripts/verify_hooks.py` | v10 세션 hook/스크립트 검증기 (6/6) |
| `scripts/deploy_power.py` | v10 Phase 5: v3 power 배포 단일 구현 (버전 게이트 2.10 · 백업 · clean-replace · installed.json · --dry-run) |
| `scripts/verify_deploy_power.py` | v10 Phase 5: deploy_power 테스트 하니스 (임시 홈, 25/25) |
| `context_rule/adaptive.md` | Curator 직접 수정 영역 (반복 패턴 8건) |
| `common_knowledge/safe-batch-replace.md` | 10세대 재사용 검증 (M22→M32) |
| `common_knowledge/mickey-graph-visualization.md` | 그래프 시각화 도구 사용법 + 시각적 매핑 + Phase 4 계획 (M35) |
| `scripts/m21_measure_usage.py` | 활용도 baseline 측정 스크립트 |
| `scripts/mickey_graph_viz.py` | 지식 그래프 시각화 CLI 진입점 (--scope global/project) |
| `scripts/mickey_graph/graph_builder.py` | 글로벌/프로젝트 그래프 빌더 (Graduated 흡수 + degree 계산) |
| `scripts/mickey_graph/templates/graph.html.tmpl` | vis-network + 필터 UI + 이웃 강조 인라인 템플릿 (M35 Phase 3) |
| `scripts/mickey_graph/ROADMAP.md` | Phase별 계획 (1/1.5/2/3 완료, 4 계획 중) |

### File Statistics

- **총 파일 수 (근사)**: ~150 (M32 시점, 디렉토리 제외)
- **주요 구성**: Markdown (가이드/세션 로그), JSON (에이전트), Python (진단/적용 스크립트)
- **백업 파일**: `examples/knowledge-curator.json.{m24,m25,m26,m27,m28,m29}-bak` (Curator 진단 6단계) + `extended-protocols.md.{m30,m31,m32}-bak` + `ai-developer-mickey.json.m32-bak`

### Project Structure Pattern

**문서 중심 + 자기 개선 루프** — 에이전트 설정(JSON) + 가이드 문서(Markdown) + 세션 로그 + 진단 스크립트가 함께 진화. SESSION/HANDOFF 임계 3 초과 시 `sessions/` 로 아카이빙하여 루트 가시성 유지. M32 이후 외부 코드 분석 도구(Serena/Graphify/내장 code) 통합으로 상세 코드 관계 분석은 도구 위임.

## Last Updated
2026-07-11 (Mickey 35 CLI 트랙 + v10 Power Migration Phase 4-A 반영: power-mickey/ 재건 · .kiro/hooks·scripts 트리 추가 · Key Files 검증기 4건)
