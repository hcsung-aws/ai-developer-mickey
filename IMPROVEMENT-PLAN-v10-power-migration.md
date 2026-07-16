# IMPROVEMENT-PLAN v10 — CLI v2 Agent → v3 Power 마이그레이션

- **작성일**: 2026-07-04
- **선행 문서**: `IMPROVEMENT-PLAN-v9.md`, `IMPROVEMENT-PLAN-v9-ADDENDUM.md`, `POSTMORTEM-2026-05-14.md`
- **트리거**: kiro-cli 2.10.0 에서 `--agent-engine {v1,v2,v3}` 삼중 엔진 도입. v3 엔진 부팅 시 agent JSON 의 `prompt` 필드가 무시되고 `power` 개념으로 프롬프트 확장 방식이 바뀜.

---

## 1. 배경

Mickey 는 v17 에 도달할 때까지 `examples/ai-developer-mickey.json` 을 정본으로 진화해 왔다. `kiro-cli` 가 2.10.0 에서 v3 엔진을 도입하면서 다음 사실이 관측됐다:

- v3 엔진(`--v3` 또는 `--agent-engine v3`)은 자체 시스템 프롬프트를 강제 로드하고 `kiro_powers`, `orchestrate_subagent`, `createHook` 등 신규 도구를 노출한다.
- v3 엔진에서도 `kiro-cli agent list` 는 `~/.kiro/agents/*.json` 을 그대로 인식하지만, agent JSON 의 `prompt` 필드는 시스템 프롬프트에 편입되지 않는다.
- Power 는 `~/.kiro/powers/installed/<name>/` 에 배치되며 `POWER.md` + `steering/` + `mcp.json` 삼합으로 구성된다. `installed.json` 이 등록 대장 역할을 한다.
- 기존 `power-mickey/` 는 Kiro IDE 0.7+ 시절 실험용으로 만든 유물이며, v17 프롬프트의 심도(3-Tier 로딩 · PURPOSE-SCENARIO · MICKEY-N-SESSION/HANDOFF · Curator subagent · REMEMBER 12)를 반영하지 못한 축약본이다.

## 2. 목표

CLI v2 Mickey 의 핵심 기능을 v3 Power 로 새로 지어, **CLI v3와 Kiro IDE 양쪽에서 실행 가능한 단일 Power 자산**을 확보한다. 옵션 B(v3 power 에 v2 자산을 적재해 심도 회복)를 이번 사이클에서 수행하고, v3 정식 공개 후 옵션 C(v3 native 재설계)로 이어간다.

## 3. 사용자 확정 방향 (2026-07-04)

1. 옵션 B → C 두 단계 전략. 지금은 B.
2. 기존 `power-mickey/` 는 재활용하지 않고 새로 짓는다.
3. `~/.kiro/mickey/` 를 v2·v3 공용 서고로 승격. **공용 도메인 지식 vs 프로젝트별 지식 분리**는 v2 규약 그대로 유지.
4. memorygraph MCP 배제. 지식 그래프는 파일 기반 `~/.kiro/mickey/`, 코드 관계 그래프는 Serena + Graphify.
5. Phase 4 는 4-A(Curator 로직을 steering 으로 흡수) 선행. 4-B(v3 sub-agent 등록)는 v3 정식 후 검토.
6. 세션 단위: Phase 0~1 → 이번 세션, Phase 2 이후 → 다음 세션부터 순차 진행.

## 4. 설계 원칙

| # | 원칙 | 근거 |
|---|------|------|
| P1 | 지식 서고 이원화 | v2 규약. 공용 = `~/.kiro/mickey/`, 프로젝트별 = `context_rule/`, `common_knowledge/`, `auto_notes/`, PURPOSE-SCENARIO. |
| P2 | 작은 조각 · 느슨한 결합 | Clean Architecture. steering 파일을 기능 단위로 분할해 개별 교체 가능. |
| P3 | 조건부 지시의 양쪽 분기 명시 | 사용자 must-follow-rules: "X이면 하라 + X 아니면 하지 마라" 병기. |
| P4 | Test Harness 선행 | WELC. 각 Phase 마다 검증 절차와 롤백 절차 사전 정의. |
| P5 | v3 신규 도구 약결합 | v3 API 미공개. `kiro_powers.readSteering`/`createHook`/`orchestrate_subagent` 없어도 파일 참조로 대체 가능하도록 설계. |
| P6 | 백업 후 삭제 없음 | 원본 유지, 사본 생성. 롤백은 사본 복원만으로 가능. |

## 5. 조사에서 확정된 실측 사실

| 항목 | 결과 |
|------|------|
| kiro-cli 버전 | 2.10.0 (2026-07-04) |
| v3 엔진 부팅 시 agent JSON prompt | **무시됨** (본 세션이 살아있는 증거) |
| `kiro-cli agent list` in v3 | 여전히 v2 agent JSON 8개 인식 |
| v3 Power 설치 위치 | `~/.kiro/powers/installed/<name>/` |
| v3 Power 등록 파일 | `~/.kiro/powers/installed.json` |
| `.serena/memories/` | 비어 있음 — 지식 그래프 정본 아님 |
| `~/.kiro/mickey/` 실체 | patterns 6 · domain entries 40+ · INDEX/GRAPH/PROFILE — 파일 기반 지식맵 |
| memorygraph MCP | 사용자 배제 결정 (Serena + Graphify 로 대체) |

## 6. 전체 Phase 계획

### Phase 0 — 사전 준비와 안전망

**산출물**
- `.gitignore` 에 `*.pre-v10-bak.zip`, `*.pre-v10-bak/` 추가
- `session_history/2026-07-04-mickey-v10-migration.md` 개시
- 백업 4건:
  - `power-mickey.pre-v10-bak.zip` (프로젝트 루트)
  - `~/.kiro/powers/installed/power-mickey.pre-v10-bak.zip`
  - `~/.kiro/agents/ai-developer-mickey.json.pre-v10-bak`
  - `~/.kiro/agents/knowledge-curator.json.pre-v10-bak`
- `scripts/backup_pre_v10.py` (idempotent 백업기)
- 본 계획서

**CC**: 위 산출물 모두 존재 + 백업 스크립트 재실행 시 [skip] 4건 나옴

**롤백**: 백업 파일 복원 만으로 원상 복귀. 이 Phase 는 원본 무변경.

### Phase 1 — 공용 서고(`~/.kiro/mickey/`) 재정렬

**산출물**
- `mickey/README.md` (프로젝트 원본, 서고 계약서)
- `~/.kiro/mickey/README.md` (수동 배치, Phase 5 자동화 전까지 임시)
- `scripts/verify_mickey_home.py` (Test Harness)

**변경 금지**: `extended-protocols.md`, `patterns/INDEX.md`, `domain/{INDEX.md, GRAPH.md, PROFILE.md, entries/*.md}` 내용 무변경

**CC**: verify_mickey_home.py 실행 시 필수 파일 존재 + README 신규 등장 확인

**롤백**: README 삭제만으로 복귀

### Phase 2 — 새 `power-mickey/` 골격 제작

**설계 재조정 (2026-07-07)**: 원안(steering 7개, T1.5 전량 흡수)을 **부정**하고, "Steering = 진입점 / T1.5·entries·patterns = 그래프 노드" 원칙으로 재설계함. 근거는 §8-b 참조.

**대응 매트릭스**: `docs/v2-to-v3-mapping.md` — T1(v17 prompt) 각 섹션이 어느 steering으로 이식되는지, T1.5 §1~§19가 어떤 트리거로 pull되는지 100% 추적.

**새 구조 (steering 6개)**:
```
power-mickey/
├── POWER.md                    # 활성화 시 로드되는 메타 · steering 6개 안내 · T1.5 트리거 목록
├── mcp.json                    # aws-knowledge 유지, memorygraph 제거
└── steering/
    ├── mickey-core.md          # Core Identity + Communication + REMEMBER 12 + Anti-Patterns
    ├── session-protocol.md     # First/Continuing/During/End Session 4단계 + Brownfield/§19/엔트로피 트리거
    ├── knowledge-graph.md      # 지식 그래프 접근 규약 (INDEX/GRAPH/PROFILE/entries/patterns/extended-protocols §N) + Curator 호출 규약 + 3-Tier 로딩
    ├── problem-solving.md      # 10단계 골격 + 심층 프로토콜(WELC/Backpressure/Behavioral) 트리거
    ├── document-schema.md      # 10종 문서 필수 스키마 표
    └── context-window.md       # 50/70/90 실행 규칙
```

**Phase 2 sub-단계**:
- **Phase 2a** — 골격 (매트릭스 · POWER.md · mcp.json · 계획서 재조정)
- **Phase 2b** — steering 6개 초안 작성
- **Phase 2c** — Test Harness (`scripts/verify_power_structure.py`) + 검증

**CC**:
- steering 파일 각각 200줄 이내
- POWER.md의 안내가 steering 6개 모두 커버
- v17 T1의 REMEMBER 12 · Session Protocol 4단계 · Document Schema 10종 · Problem-Solving 10단계가 대응 매트릭스로 100% 추적됨
- T1.5(`extended-protocols.md` §1~§19)는 **원본 유지, 이식 금지**. steering은 트리거 문장만 명시
- 지식 그래프 노드(`domain/entries/*`, `patterns/*`)는 **원본 유지, 이식 금지**. steering은 접근 규약만 명시
- 조건부 지시는 양쪽 분기 병기 (P3)

**Test Harness** (Phase 2c):
- `scripts/verify_power_structure.py` — 파일 존재 · front matter 유효성 · steering 매핑 완결성 · T1 100% 추적성 · T1.5 트리거 존재 · P3 양쪽 분기 병기 검증

### Phase 3 — 세션 관리 hook · 스크립트

**계층**
- CLI v3용: `.kiro/hooks/<id>.json` (`SessionStart`/`Stop`/`UserPromptSubmit`)
- IDE용: `.kiro/hooks/<name>.kiro.hook` (`preTaskExecution`/`postTaskExecution`)
- 공용 로직: `.kiro/scripts/mickey_session_boot.py`, `mickey_session_close.py` — hook 은 얇게 두고 로직은 파이썬 스크립트에 담아 재사용

**양쪽 분기 명시 필수 사례**
- PURPOSE-SCENARIO.md 존재 여부 → 로드 or 신규 질문
- Serena/Graphify 감지 여부 → INDEX Tool Links 등록 or Tier 3 baseline
- 이전 HANDOFF 존재 여부 → 로드 or Mickey 1 세션 취급
- Brownfield 감지 여부 → 온보딩 수행 or 스킵

**CC**: 스크립트 각각 hook 없이 단독 실행 가능 · v3/IDE 예시 파일 각각 존재

### Phase 4-A — Knowledge Curator 로직을 steering 으로 흡수

- `steering/knowledge-curator.md` 신규 (v2 `knowledge-curator.json` 프롬프트를 이식)
- 세션 종료 hook 이 이 steering 을 `readSteering` 하도록 지시
- Pre-staged Apply 패턴(`_curator-staging/`)은 v2 와 동일하게 동작

**옵션 4-B 로의 이관 조건**: v3 정식 공개 후 `orchestrate_subagent` 가 커스텀 sub-agent 등록을 지원하면 재검토

### Phase 5 — 배포 · 검증 · 문서화

**install 스크립트 개편**
- `install.ps1` / `install.sh`:
  - v2 agent JSON → `~/.kiro/agents/` 유지 (v2 엔진 사용자 계속 지원)
  - v3 power → `~/.kiro/powers/installed/power-mickey/` 배치 + `installed.json` 갱신
  - `~/.kiro/mickey/` 공용 서고 → README 포함 배치
- **kiro-cli 2.10 미만이면 v3 스킵 안내**, 이상이면 양쪽 설치 (P3)

**문서 갱신**
- README.md 에 CLI v2 / CLI v3 / IDE 세 사용 시나리오 표
- `docs/09-v3-power-migration.md` (한/영) 신규 — 마이그레이션 서사와 결정 이력
- `docs/07-changelog.md` v10 항목

**회귀 검증 시나리오**
1. `kiro-cli chat --agent ai-developer-mickey` (기본 v2 엔진) — v17 프롬프트 정상 로드
2. `kiro-cli chat --v3` + `kiro_powers activate power-mickey` — 신 POWER.md · steering 정상 로드
3. Kiro IDE 로 `power-mickey/` 열기 — steering 정상 인식

**Steering file 갱신**
- 이 마이그레이션으로 프로젝트 파일 10%↑ 변경 예상
- `PROJECT-OVERVIEW.md`, `FILE-STRUCTURE.md` 재분석 트리거 도달 → 갱신

## 7. 리스크 대장

| ID | 리스크 | 대응 |
|----|--------|------|
| R1 | v3 hook 규격 미확정 | Phase 3 hook 얇게, 실제 로직은 파이썬 스크립트로 격리. **[2026-07-10 해소]** `createHook` 도구 스펙으로 확정 (version/hooks/name/trigger/action). |
| R2 | IDE hook 형식 병존 유지 부담 | 예시 파일만 제공, 자동 설치는 사용자 선택 |
| R3 | Curator sub-agent v3 등록 방법 불투명 | 4-A 로 시작, 4-B 는 유보. **[2026-07-11 4-A 완료]** `knowledge-curator.md`(manual) + CURATOR-PROMPT.md pull 로 흡수. 4-B(sub-agent 승격)는 v3 정식 후. |
| R4 | v17 프롬프트 → 7 steering 분할 시 문맥 흐름 손실 | 대응 매트릭스(`docs/v2-to-v3-mapping.md`)로 추적성 확보 |
| R5 | `kiro_powers.activate` 시 자동 로드 범위 불투명 | POWER.md 에 `readSteering` 지시 명시. IDE 는 steering front matter 로 대체 가능 |
| R6 | 사용자 홈 자산 오조작 | `backup_pre_v10.py` idempotent 구조, 원본 삭제 없음 |
| **R7** | **프로젝트에 잔존한 개인 지식 파일 정리 정책 부재** (Phase 1 오독 정정 후 격하) | 부수 결정 사안 §8-a 참조. 이번 마이그레이션 사이클 밖에서 별도 처리. |

## 8-a. Phase 1 오독 정정과 확정된 방향

### 본좌의 초기 오독

Phase 1 verify 결과를 본좌가 "정본 불일치 = 서고 계약 위반 이슈"로 규정했으나, 이는 근거 조사 부족에서 온 오독이었다.

**정정 근거**:
- `examples/knowledge-curator.json` 확인: Curator 는 `~/.kiro/mickey/domain/**` 만 수정. 프로젝트 `mickey/` 는 절대 건드리지 않음.
- `install.ps1` 확인: 프로젝트 → 사용자 홈 단방향 seed 배포. 역방향 동기화 없음.
- git 커밋 이력: `Mickey 19: sync global to repo mickey/ (per-file direction)`, `Mickey 20 post-Curator: domain entries (선별 2건)` — 사용자가 손으로 선별 커밋하는 워크플로 존재.

즉 프로젝트와 사용자 홈이 divergence 하는 것은 설계된 정상 동작이다.

### 확정된 방향 (사용자 확인 완료, 2026-07-04)

- 프로젝트 `mickey/` = **모든 사용자에게 배포되는 seed 골격**
- 사용자 홈 `~/.kiro/mickey/` = **각 사용자의 개인 지식 그래프 실체**
- 개인 지식은 프로젝트에 커밋하지 않음 (예외: `extended-protocols.md` — T1 core protocol, 세대 관리 필요)
- 이 프로젝트 자신도 예외 아님. 초창기(지식 그래프가 프로젝트별로만 존재하던 시기)에 여기 축적된 잔재는 원칙적으로 정리 대상.

### 정정 완료 산출물 (Phase 1 재실행 2026-07-04)

1. `mickey/README.md`: "seed vs 개인 그래프" 분리 원칙 명시로 전면 재작성
2. `scripts/verify_mickey_home.py`: `--mode {home,seed,auto}` 분리. 프로젝트 원본은 seed 완결성만, 사용자 홈은 실제 축적 최소 개수 추가로 검증
3. 본 계획서 §7 R7 · §8-a: 잘못된 이분법 삭제, 오독 정정과 확정 방향으로 재작성
4. `session_history/2026-07-04-mickey-v10-migration.md` §5.1: 오독 → 정정 서사로 재기술

### 검증 결과

- `python scripts/verify_mickey_home.py` (기본, 사용자 홈): **PASS (home 모드)**
- `python scripts/verify_mickey_home.py --path mickey` (auto 판정): **PASS (seed 모드로 자동 판정)**

### 부수 결정 사안 (이번 마이그레이션 사이클 밖)

프로젝트에 이미 커밋되어 남아 있는 개인 지식 잔재 처리:
- `mickey/domain/entries/*.md` 10건 (Mickey 19~20 등에서 선별 커밋된 것)
- `mickey/patterns/INDEX.md` — 사용자 홈 최신 상태(6개 패턴)를 반영하나 실제 패턴 파일은 프로젝트에 없어 죽은 참조 상태

**선택지**:
- (i) 잔재 파일 git rm 완전 제거 + INDEX 를 seed 템플릿 상태로 되돌림 — 원칙에 가장 부합
- (ii) 교육 · 데모용 seed 예시로 재분류하여 유지 — 이 프로젝트가 교육용임을 고려한 실용안
- (iii) 일부만 선별 유지 (예: 대표적인 3~5건)

**본좌 권고**: (ii) 우선. 이 프로젝트가 "Mickey 활용 가이드" 성격을 지니므로 seed 예시 몇 건은 새 사용자가 감을 잡는 데 유용. 다만 명확히 "seed 예시"로 라벨링하고 README 에 그 취지를 명시해야 함. Phase 5 이후 별도 사이클에서 처리 권장.

## 8. 결정 이력

| 일자 | 결정 | 근거 |
|------|------|------|
| 2026-07-04 | 옵션 B → C 순차 | v3 미공개 상태에서 재설계 위험 |
| 2026-07-04 | 기존 `power-mickey/` 폐기 | IDE 시절 축약본, v17 심도 재현 불가 |
| 2026-07-04 | memorygraph MCP 배제 | 파일 기반 지식맵 + Serena + Graphify 로 대체 |
| 2026-07-04 | Phase 4-A 선행 | v3 sub-agent 규격 불투명 |
| 2026-07-04 | Phase 단위 진행 | 이번 세션은 0~1, 이후 세션 단위 |
| 2026-07-07 | **steering 7개 → 6개 재조정** | Steering=진입점, T1.5=그래프 노드 원칙. §8-b 참조 |
| 2026-07-07 | **T1.5 전량 이식 부정** | steering이 진입점 역할만 하고, T1.5 §1~§19는 원본 유지하여 필요 시 pull. §8-b 참조 |
| 2026-07-07 | **`knowledge-management.md` → `knowledge-graph.md` 대체** | 3-Tier 관리에 그래프 접근 규약 통합. INDEX/GRAPH/PROFILE/Curator 진입 통일 |
| 2026-07-07 | **`code-analysis-tools.md` 별도 파일 폐기** | §19 트리거를 `session-protocol.md` First Session Step 4a에 두는 것이 자연스러움. 별도 파일 유지 시 중복 발생 |
| 2026-07-07 | **Phase 2 sub-단계 분해 (2a/2b/2c)** | 컨텍스트 소모 제어. 골격/초안/검증을 분리해 세션 단위로 안전하게 진행 |
| 2026-07-09 | **P3 검증 사전 확장 (선택 갈래 대칭 포함)** | P3 원칙 원문은 "양쪽 분기 병기"로 긍정/부정 쌍뿐 아니라 선택 갈래 대칭도 포함. `document-schema.md` 원문 훼손 없이 검증기 사전에 자연스러운 갈래 2개 추가. 세션 로그 D-2c-1 참조 |
| 2026-07-10 | **`--read-stdin` 명시 플래그로 stdin 파싱 옵션화** | hook 자동 호출에서만 stdin JSON 파싱. `isatty()` 기반 자동 판정은 execute_pwsh 같은 non-tty pipe 환경에서 block 위험. hook JSON 은 `--read-stdin` 을 명시적으로 인자에 붙임 (세션 로그 D-3-1) |
| 2026-07-10 | **IDE hook skeleton + `_note` SKELETON 표기, Phase 5 실측 이월** | IDE `.kiro.hook` 규격 실측 부재. skeleton 만 두고 `_note` 필드로 사용자·검증기가 skeleton 임을 인지. Phase 5 회귀 검증에서 정식 규격으로 조정 (세션 로그 D-3-2) |
| 2026-07-10 | **Serena/Graphify 정적 감지 (편집 금지, 리포트만)** | 스크립트만으로는 MCP 런타임 활성 여부 확정 불가. `.kiro/settings/mcp.json` · `~/.kiro/settings/mcp.json` 정적 파싱으로 등록 여부만 리포트. INDEX 편집은 Mickey 판단 (세션 로그 D-3-3) |
| 2026-07-11 | **`knowledge-curator.md` = `inclusion: manual` (B 조합)** | Curator 규약은 세션 종료 시에만 필요. 상시 로드 시 progressive-disclosure 위배. `readSteering` 로 pull. 상시 6 + on-demand 1 구조 확정 (세션 로그 D-4A-1) |
| 2026-07-11 | **Curator 호출 규약을 `knowledge-graph.md`→`knowledge-curator.md` 이관 (A 조합)** | `knowledge-graph.md` 에 이미 존재하던 호출 규약이 신규 파일과 3중 중복. DRY·단일 책임 위해 `knowledge-curator.md` 로 이관, `knowledge-graph.md` 는 리다이렉트 + §17 트리거만 유지 (세션 로그 D-4A-2) |
| 2026-07-13 | **v3 배포 로직을 파이썬 단일 구현(`deploy_power.py`)에 위임 (A-2)** | 백업·clean-replace·installed.json 갱신을 셸 2벌 중복 시 동기화 부담·side effect. 단일 파이썬이 dry-run/harness 검증 용이·이식성 확보. install.ps1/.sh 는 얇게 호출 (세션 로그 D-5-1) |
| 2026-07-13 | **v3 배포는 full-dir clean-replace** | 홈에 구 pre-v10 steering(memory-protocol/self-improvement) 서빙 중. additive copy 는 orphan 잔존 → 잘못된 steering 로드. rmtree+copytree 로 차단, 직전 백업으로 복구 가능 (세션 로그 D-5-2) |
| 2026-07-13 | **버전 파싱 실패 시 보수적 스킵** | 버전 미확정 시 v3 강행 대신 v2 만 유지가 안전. 미검증 환경 홈 자산 변경 위험 차단 (세션 로그 D-5-3) |
| 2026-07-13 | **registry stale path 무처리 (B-1)** | kiro 는 installed/ 물리본 서빙 → registry path 서빙 무관. 이번 사이클 범위(installed 배치 + installed.json) 집중. path 정정은 부채 이월 (세션 로그 D-5-4) |

## 8-b. 2026-07-07 재조정 근거 (Steering ≠ T1.5 이식)

### 초기 접근의 오류

Phase 2 원안(§6, 2026-07-04 작성 시점)은 T1(v17 prompt)뿐 아니라 T1.5(`extended-protocols.md` §1~§19)까지 steering 7개에 흡수하는 방향이었다. Phase 2a 착수 시점에 본좌가 사용자에게 확인 요청 → 사용자가 다음 지침으로 정정:

> "steering을 시작으로 해서 현재 프로젝트에 필요한 지식들을 graph 형태로 연관성 위주로 '추가 참조'해서 mickey가 지식 그래프에 있는 지식들 중 지금 필요한 것들만 딱 읽어다 활용하게 하기 위함이야. (...) T1만 필수고 T1.5부터는 상황에 따라 그래프 형태로 연관된 지식들 중 필요한 것들만 필요할 때 참고하는 식으로 동작해야 해"

### 재조정 원칙

| 계층 | 이식 여부 | 근거 |
|------|----------|------|
| **T1** (v17 prompt, 278줄) | 필수 이식 (steering 6개로 분할) | 모든 세션에서 상시 필요한 뼈대 |
| **T1.5** (`extended-protocols.md` §1~§19) | **이식 금지, 원본 유지** | 상황별 심층 프로토콜. steering이 트리거만 명시하고 필요 시 §N pull |
| **지식 그래프 노드** (`domain/entries/*`, `patterns/*`) | **이식 금지, 원본 유지** | 이미 INDEX·GRAPH·PROFILE의 접근 규약이 성립. steering은 접근 경로만 명시 |
| **Curator** (`domain/CURATOR-PROMPT.md`) | 이식 금지, 원본 유지 | `knowledge-graph.md`가 호출 규약(입력·출력·5회 검증)만 요약 |

### 재조정 효과

- steering 파일 각 200줄 이하 유지 가능 (원안대로 T1.5 흡수 시 300~500줄 예상)
- 세션 시작 시 상시 로딩 부담 최소화 → context window 초기 소모 절감
- T1.5는 세션마다 진화 가능 (steering 재배포 없이 `~/.kiro/mickey/extended-protocols.md`만 갱신)
- 그래프 진화 루프(Curator)와 steering 배포 라이프사이클이 분리됨

## 9. 다음 세션 인계

**Phase 4-A 완료 (2026-07-11)**. 산출물:

- `power-mickey/steering/knowledge-curator.md` 신규 — `inclusion: manual` 얇은 진입점. Curator 호출 계약(입력·R/G/S 분기·자동승인 경로·5회 검증·출력·응답 프로토콜) 요약. 상세 절차는 `~/.kiro/mickey/domain/CURATOR-PROMPT.md` 를 pull 하도록 지시(그래프 노드 원칙, 이식 금지). P3 양쪽 분기 병기.
- `power-mickey/steering/knowledge-graph.md` — 기존 "Curator 호출 규약" 섹션을 `knowledge-curator.md` 로 이관하고 리다이렉트 + §17 트리거만 유지 (D-4A-2, 3중 중복 제거).
- `power-mickey/POWER.md` — 상시 6개 / on-demand 1개(`knowledge-curator.md`) 2계층 표기. "세션 정리" 절차 Step 2 를 readSteering 흐름으로 갱신. Version → Phase 4-A.
- `power-mickey/steering/session-protocol.md` — End Step 2 를 `knowledge-curator.md` readSteering 선행 흐름으로 갱신.
- `scripts/verify_power_structure.py` — steering 6→7개 확장. `ALWAYS_STEERING_FILES`/`ONDEMAND_STEERING_FILES` 분리, T15 트리거에 `knowledge-curator.md`(§12·§17·§18) 추가, 신규 `check_inclusion_modes`(항목 7) 로 always/manual 정합성 검증.

실행 결과:
- `python scripts\verify_power_structure.py` — PASS 7 / FAIL 0 / total 7. Exit 0.
- `python scripts\verify_hooks.py` 회귀 재확인 — PASS 6 / FAIL 0. hook 자산 무손상.

설계 결정:
- **B 조합** (D-4A-1): `knowledge-curator.md` = `inclusion: manual`. 세션 종료 시에만 readSteering 로 pull (progressive disclosure).
- **A 조합** (D-4A-2): 호출 규약 중복을 `knowledge-curator.md` 로 단일화. `knowledge-graph.md` 는 리다이렉트만.

세션 로그: `session_history/2026-07-11-mickey-v10-migration-phase-4a.md`.

**옵션 4-B 로의 이관 조건**: v3 정식 공개 후 `orchestrate_subagent` 가 커스텀 sub-agent 등록을 지원하면 `knowledge-curator.md` 를 sub-agent 프롬프트로 승격 재검토. 이번 사이클은 4-A 로 종료.

**Phase 5 진입** (다음 세션):

- **install 스크립트 개편** (`install.ps1`/`install.sh`): v2 agent JSON → `~/.kiro/agents/` 유지, v3 power → `~/.kiro/powers/installed/power-mickey/` 배치 + `installed.json` 갱신, `~/.kiro/mickey/` 공용 서고 README 포함 배치. kiro-cli 2.10 미만이면 v3 스킵 안내 / 이상이면 양쪽 설치 (P3).
- **IDE hook 정식 규격 실측**: Phase 3 에서 skeleton + `_note` 로 이월한 `.kiro.hook` 2건을 실측 규격으로 조정 (D-3-2).
- **문서 갱신**: README 에 CLI v2 / CLI v3 / IDE 3 시나리오 표, `docs/09-v3-power-migration.md`(한/영) 신규, `docs/07-changelog.md` v10 항목.
- **회귀 검증 3 시나리오**: ① `kiro-cli chat --agent ai-developer-mickey`(v2) v17 프롬프트 로드, ② `--v3` + `kiro_powers activate power-mickey` 신 POWER.md·steering 로드, ③ Kiro IDE 로 `power-mickey/` steering 인식.
- **Steering file 갱신**: 마이그레이션으로 프로젝트 파일 10%↑ 변경 → `PROJECT-OVERVIEW.md`·`FILE-STRUCTURE.md` 재분석 트리거 도달 여부 점검.

**Phase 5 (가) install 스크립트 개편 — 진행 (2026-07-13)**:

- 상태: **코드·test harness 완료. 실제 홈 배포는 사용자 확인 대기.**
- 산출물: `scripts/deploy_power.py`(신규, 배포 단일 구현) · `scripts/verify_deploy_power.py`(신규, harness 25/25) · `install.ps1`/`install.sh`(v3 호출 추가, v2 유지).
- 소비 모델 실증: kiro-cli 는 `~/.kiro/powers/installed/power-mickey/` 물리본 서빙. 현재 홈은 구 pre-v10 power(steering 5개·memorygraph) 서빙 중 → v10(7개) clean-replace 필요성 확인.
- 결정: A-2(파이썬 단일 구현) / B-1(registry 무처리, stale path 부채) / C(게이트 2.10) / D(dry-run). 상세 §8 D-5-1~D-5-4.
- 검증: `verify_deploy_power.py` 25/25, 실제 홈 배포 + `kiro_powers activate` v10 서빙 확인, 회귀 `verify_power_structure.py` 7/7·`verify_hooks.py` 6/6 유지. **회귀 3 시나리오: ① v2 PASS · ② v3 PASS (2026-07-13 실측) · ③ IDE 이월.**
- 세션 로그: `session_history/2026-07-13-mickey-v10-migration-phase-5-install.md`.
- 잔여: 실제 배포 실행 + 배포 후 `kiro_powers activate` 회귀 · 문서 갱신 · IDE hook 실측(최후순위).

**참고 원본**:
- `examples/ai-developer-mickey.json` (v17 T1), `mickey/extended-protocols.md` (T1.5)
- `mickey/domain/*.md`, `mickey/patterns/INDEX.md` (그래프 노드)
- `mickey/domain/CURATOR-PROMPT.md` (Curator 정본 · `knowledge-curator.md` 가 요약 참조)
- `install.ps1` / `install.sh` (Phase 5 개편 대상)

---

**Last Updated**: 2026-07-13 (Phase 5 (가) install 스크립트 개편 — 코드·harness 완료, 실제 배포 미결)
