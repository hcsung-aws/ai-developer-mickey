# v10: CLI Agent에서 Kiro v3 Power로

> [English Version](09-v3-power-migration-en.md)

> Mickey를 CLI v2 agent(JSON 프롬프트)에서 Kiro v3 Power 형식으로 옮긴 마이그레이션의 서사와 설계 결정을 기록합니다.

## 왜 옮기는가

Mickey는 원래 Kiro CLI의 agent JSON(`examples/ai-developer-mickey.json`) 한 파일에 v17까지 진화한 프롬프트를 담아 동작했습니다. 이 방식은 단순하지만 두 가지 한계가 있었습니다.

- **상시 로드 부담**: 278줄 규모의 프롬프트 전체가 매 세션 컨텍스트에 상주. 세션이 시작되자마자 context window의 상당 부분이 소모됩니다.
- **IDE 통합 부재**: Kiro IDE 사용자는 CLI agent를 쓸 수 없습니다. IDE의 Power 형식(steering + POWER.md)이 필요합니다.

v3 Power는 이 둘을 동시에 해결합니다. steering을 **진입점**으로 삼고, 상세 지식은 **필요할 때만 pull**하는 구조(progressive disclosure)로 재편하면 초기 소모를 줄이면서 CLI와 IDE 양쪽에서 동작하게 만들 수 있습니다.

## 핵심 설계 원칙: 진입점과 그래프 노드의 분리

마이그레이션의 가장 중요한 결정은 **"무엇을 steering에 넣고 무엇을 원본에 남길 것인가"**였습니다.

| 계층 | 이식 여부 | 이유 |
|------|----------|------|
| **T1** (v17 프롬프트 골격, 278줄) | steering 6개로 분할 | 모든 세션에서 상시 필요한 뼈대 |
| **T1.5** (`extended-protocols.md` §1~§19) | 이식 금지, 원본 유지 | 상황별 심층 프로토콜. steering은 트리거만 명시하고 필요 시 §N만 pull |
| **지식 그래프 노드** (`domain/entries/*`, `patterns/*`) | 이식 금지, 원본 유지 | INDEX/GRAPH/PROFILE 접근 규약이 이미 성립. steering은 접근 경로만 명시 |
| **Curator 정본** (`CURATOR-PROMPT.md`) | 이식 금지, 원본 유지 | `knowledge-curator.md`가 호출 계약만 요약 |

이 원칙 덕분에 각 steering 파일은 200줄 이하의 얇은 진입점으로 유지되고, T1.5나 그래프 지식은 세션마다 진화하더라도 steering을 재배포할 필요가 없습니다. **진화 루프와 배포 라이프사이클이 분리**되는 것입니다.

## v2와 v3의 구조 비교

| 항목 | CLI v2 (agent JSON) | Kiro v3 Power |
|------|--------------------|---------------|
| 프롬프트 형식 | 단일 JSON `prompt` 필드 | `POWER.md` + `steering/*.md` |
| 로딩 방식 | 전체 상주 | steering 상시 6 + on-demand 1 + 그래프 노드 pull |
| 지식 그래프 | memorygraph MCP (초기) / 파일 기반 | 파일 기반 (`~/.kiro/mickey/`) |
| 세션 관리 | 수동 / hook | CLI v3 hook(`SessionStart`/`Stop`) + 스크립트 |
| MCP | agent별 | `mcp.json` (aws-knowledge만, Serena/Graphify는 전역 재활용) |
| 사용 | `kiro-cli chat --agent ai-developer-mickey` | `kiro-cli chat` (power-mickey 자동 인식) / Kiro IDE |

두 경로는 **병행 유지**됩니다. v2 엔진 사용자는 계속 agent JSON을 쓰고, v3 사용자는 Power를 씁니다.

## steering 구성 (상시 6 + on-demand 1)

**상시 로드 (`inclusion: always`)**

| Steering | 역할 |
|----------|------|
| `mickey-core.md` | Core Identity + REMEMBER 12 + Anti-Patterns |
| `session-protocol.md` | First/Continuing/During/End Session 4단계 + 그래프 트리거 |
| `knowledge-graph.md` | 지식 그래프 접근 규약 + 3-Tier 로딩 |
| `problem-solving.md` | 10단계 골격 + 심층 프로토콜 트리거 |
| `document-schema.md` | 10종 문서 필수 스키마 |
| `context-window.md` | 50/70/90 관리 실행 규칙 |

**on-demand (`inclusion: manual`)**

| Steering | 언제 pull |
|----------|----------|
| `knowledge-curator.md` | 세션 종료("세션 정리") 시에만 `readSteering`로 pull. 세션 종료가 아니면 pull하지 않음 |

Curator 규약을 상시 로드하지 않는 이유는 명확합니다. 세션 종료 시에만 필요한 규약을 매 세션 상주시키면 progressive disclosure 원칙에 어긋나기 때문입니다.

## Phase별 진행

- **Phase 0~2**: 기존 실험본(Kiro IDE 0.7 시절) 폐기 후 골격 재건. v17 → steering 6개 분할. 이식 매트릭스(`docs/v2-to-v3-mapping.md`)로 100% 추적성 확보.
- **Phase 3**: 세션 관리 hook/스크립트. CLI v3 hook 2건은 얇게, 로직은 `mickey_session_boot.py`/`mickey_session_close.py`로 격리. IDE `.kiro.hook`은 규격 실측 전까지 skeleton으로 이월.
- **Phase 4-A**: Knowledge Curator 로직을 `knowledge-curator.md`(manual)로 흡수. 정본 절차는 원본 유지 pull. 호출 규약 3중 중복 제거.
- **Phase 5**: install 스크립트 개편 + 문서 갱신.

## 배포 파이프라인 (Phase 5)

v3 Power를 사용자 홈에 배치하려면, kiro-cli가 실제로 무엇을 읽는지 알아야 했습니다. 실측 결과 kiro-cli는 **`~/.kiro/powers/installed/power-mickey/`의 물리 복사본**을 서빙했습니다. registry의 source path는 provenance 메타데이터일 뿐이었습니다.

이 사실이 배포 설계를 결정했습니다. `scripts/deploy_power.py`가 배포 핵심 로직을 단일 책임으로 담당합니다.

1. **버전 게이트** — `kiro-cli --version`을 파싱해 2.10 이상일 때만 v3 배포. 미달/파싱 실패 시 v3만 건너뛰고 정상 종료(v2는 유지).
2. **백업** — 기존 설치본을 `power-mickey.bak-<타임스탬프>.zip`으로 백업.
3. **clean-replace** — 디렉토리를 통째로 교체(rmtree + copytree). 이는 필수였습니다. 실측에서 홈에 구 pre-v10 steering(memory-protocol, self-improvement)이 남아 있었고, 단순 덮어쓰기로는 이 orphan이 잔존해 kiro가 잘못된 steering을 로드하기 때문입니다.
4. **installed.json 보장** — 항목이 없으면 추가, 있으면 무변경(idempotent).

`install.ps1`/`install.sh`는 기존 v2 배포(agents JSON + `~/.kiro/mickey` 서고)를 유지한 채 `deploy_power.py` 호출만 추가합니다. **v2는 항상, v3는 조건부**입니다.

## 왜 memorygraph를 제거했나

초기 실험본은 memorygraph MCP로 장기 기억을 관리했습니다. v10에서는 이를 제거하고 파일 기반 지식 그래프(`~/.kiro/mickey/`의 INDEX/GRAPH/PROFILE/entries)로 일원화했습니다.

- MCP 의존이 사라져 설치·이식이 단순해집니다.
- 지식이 markdown 파일로 남아 git으로 버전 관리·리뷰가 가능합니다.
- Windows에서 memorygraph의 hang 버그(project 파라미터 필수) 같은 런타임 제약에서 자유로워집니다.

## 검증

test harness로 회귀 방어선을 세웠습니다.

- `verify_power_structure.py` **7/7** — steering 존재·front matter·POWER 매핑·T1 추적성·트리거·P3 양쪽 분기·inclusion 모드
- `verify_hooks.py` **6/6** — 세션 hook/스크립트
- `verify_deploy_power.py` **25/25** — 버전 파싱·게이트·dry-run 무변경·orphan 제거·idempotent·게이트 미달 스킵 (임시 홈 사용으로 실제 홈 무손상)

## 교훈

- **추측 대신 실증**: registry vs installed 소비 모델을 코드 추측으로 넘기지 않고 실제 활성화로 확인한 덕분에 clean-replace의 필요성을 발견했습니다.
- **진입점과 원본의 분리**가 progressive disclosure의 핵심입니다. steering에 모든 것을 넣으려는 유혹을 참는 것이 v10의 본질이었습니다.
- **test harness 우선**: 홈 자산을 변경하는 로직은 실제 홈에 돌리기 전에 임시 디렉토리 harness로 방어했습니다 (Working Effectively with Legacy Code).

## 참고

- 계획서: [`IMPROVEMENT-PLAN-v10-power-migration.md`](../IMPROVEMENT-PLAN-v10-power-migration.md)
- 이식 매트릭스: [`docs/v2-to-v3-mapping.md`](v2-to-v3-mapping.md)
- 변경 이력: [변경 이력 문서](07-changelog.md)
- 세션 로그: `session_history/2026-07-04~13-mickey-v10-migration-*.md`
