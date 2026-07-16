# 2026-07-11 · Mickey v10 마이그레이션 · Phase 4-A

**세션 목표**: v10 power migration Phase 4-A — Knowledge Curator 로직을 steering 으로 흡수. v2 Curator agent(`examples/knowledge-curator.json`) 를 v3 power 의 on-demand steering(`power-mickey/steering/knowledge-curator.md`) 으로 이식. 원본 그래프 노드(`mickey/domain/CURATOR-PROMPT.md`) 는 이식 금지, 호출 계약만 요약. 검증기 확장까지 완료.

## 착수 배경

- Phase 3(2026-07-10) 산출물: 세션 관리 스크립트 2건 · CLI v3 hook 2건 · IDE skeleton 2건 · `verify_hooks.py`. 모두 PASS.
- 계획서 §9 인계 지점: `knowledge-curator.md` 신규 + POWER.md 확장 + 검증기 갱신.
- 사전 실측:
  - `examples/knowledge-curator.json` 이 정본(`.m24`~`.m29` 6세대 백업 존재). `prompt` 필드 == `mickey/domain/CURATOR-PROMPT.md` **내용 동일** 확인.
  - `power-mickey/steering/knowledge-graph.md` 에 이미 "Curator 호출 규약" 섹션 존재 → 신규 파일과 3중 중복 위험 식별.

## 사용자 확정 방향 (2026-07-11)

세션 시작 시 본좌가 설계 분기점 2개를 제시하고 사용자 확인:

- **결정 1 (inclusion 모드)**: **B** — `knowledge-curator.md` = `inclusion: manual`. 세션 종료 시에만 `readSteering` 로 pull.
- **결정 2 (중복 제거)**: **A** — `knowledge-graph.md` 의 Curator 호출 규약을 `knowledge-curator.md` 로 이관, `knowledge-graph.md` 는 리다이렉트 + §17 트리거만 유지.

→ **B-A 조합** 확정.

## 진행 원칙

- steering 은 얇은 진입점. Curator 상세 절차(0~5단계·entry 형식·staging 형식)는 `~/.kiro/mickey/domain/CURATOR-PROMPT.md` 정본 유지, pull on demand (그래프 노드 원칙, §8-b).
- P3 양쪽 분기 병기.
- 중복 제거(DRY)·단일 책임(Clean Architecture).
- 원본 자산(`mickey/**`, `examples/**`) 무변경.

## 산출물

### 신규 (2건)

- `power-mickey/steering/knowledge-curator.md` — `inclusion: manual` 진입점. 활성 시점(양쪽 분기) · 정본 절차 위치(CURATOR-PROMPT.md pull) · 입력 계약 · R/G/S 라우팅 · 자동 승인 경로 · Pre-staged Apply 패턴 · 5회 검증 · 출력·응답 프로토콜 · 연결 참조(§17·§18·§12).
- `session_history/2026-07-11-mickey-v10-migration-phase-4a.md` — 본 세션 로그.

### 변경 (7건)

- `power-mickey/steering/knowledge-graph.md` — "Curator 호출 규약"(입력·R/G/S·자동승인·검증·응답 5개 서브섹션) → "Curator 호출 (상세 규약은 이관됨)" 리다이렉트로 축약. §17 트리거·§8→§17 흡수 언급 보존. 상단 주석 이관 사실 반영.
- `power-mickey/POWER.md` — "상시 로드 6개" 표 유지 + "on-demand steering(readSteering)" 표 신설(`knowledge-curator.md`, manual). "세션 정리" 절차 Step 2 를 readSteering 흐름으로. Version → Phase 4-A / Last Updated 2026-07-11.
- `power-mickey/steering/session-protocol.md` — End Step 2 를 `knowledge-curator.md` readSteering 선행 흐름으로 갱신.
- `scripts/verify_power_structure.py` — `ALWAYS_STEERING_FILES`(6)/`ONDEMAND_STEERING_FILES`(1) 분리, `STEERING_INCLUSION_MODES` 정답지 추가, T15 트리거에 `knowledge-curator.md`(§12·§17·§18) 추가, 신규 `check_inclusion_modes`(항목 7) 등록, docstring 갱신.
- `IMPROVEMENT-PLAN-v10-power-migration.md` — §8 결정 이력 D-4A-1/D-4A-2 추가, §7 R3 상태 4-A 완료 표기, §9 Phase 4-A 완료·Phase 5 인계로 재작성.
- `PROJECT-OVERVIEW.md` — Current Status "Power Mickey (v10 Power Migration 트랙)" 소절로 갱신(Phase 0~4-A 완료·Phase 5 예정·검증 기준값), Last Updated 2026-07-11. (다음 세션 진입 문서가 M27 상태에 머물러 v10 트랙을 놓치는 부채 해소.)
- `FILE-STRUCTURE.md` — 트리에 `power-mickey/` 재건(steering 7) + `.kiro/hooks`·`.kiro/scripts`(Phase 3) 반영, Key Files 에 `knowledge-curator.md`·`verify_power_structure.py`·`verify_hooks.py`·POWER.md 갱신, Last Updated. (M35 CLI 트랙 갱신본이 v10 트랙 산출물을 누락한 부채 해소.)

### 미변경 (원본 자산 무손상)

- `mickey/domain/CURATOR-PROMPT.md`, `examples/knowledge-curator.json`(+세대 백업), `mickey/**`.
- `.kiro/hooks/**`, `.kiro/scripts/**` (Phase 3 자산).

## 검증 결과

### `scripts/verify_power_structure.py`

```
Summary: PASS 7 / FAIL 0 / total 7
Exit Code: 0
```

| # | 검증 항목 | 결과 | 세부 |
|---|---------|------|------|
| 1 | 파일 존재 | PASS | steering 7개(6+1) + POWER.md + mcp.json |
| 2 | Front matter 유효성 | PASS | POWER 3키 + steering 7개 inclusion 키 |
| 3 | POWER→steering 매핑 | PASS | 7개 모두 POWER.md 언급 |
| 4 | T1 100% 추적성 | PASS | REMEMBER 12·Session 4·Document 11·PS 10 |
| 5 | T1.5 §N 트리거 | PASS | knowledge-curator.md §12·§17·§18 포함 |
| 6 | P3 양쪽 분기 병기 | PASS | knowledge-curator.md 대칭 쌍 2개 |
| 7 | inclusion 모드 정합성 | PASS | 상시 6=always, Curator=manual |

### 회귀 — `scripts/verify_hooks.py`

```
Summary: PASS 6 / FAIL 0 / total 6
Exit Code: 0
```

Phase 3 hook 자산 무변경 재확인.

## 결정 이력

- **D-4A-1**: `knowledge-curator.md` = `inclusion: manual` (B 조합) (2026-07-11). 근거: Curator 규약은 세션 종료 시에만 필요. 상시 로드 시 매 세션 context window 를 불필요하게 소모(progressive-disclosure 위배). `readSteering` 로 종료 시점에만 pull. POWER.md 를 "상시 6 + on-demand 1" 2계층으로 재편. Alternative: `inclusion: always` 로 기존 6개와 균질화 (거부: 세션 종료 전용 규약을 상시 적재하는 낭비).

- **D-4A-2**: Curator 호출 규약을 `knowledge-graph.md`→`knowledge-curator.md` 이관 (A 조합) (2026-07-11). 근거: `knowledge-graph.md` 에 이미 있던 호출 규약 + 신규 `knowledge-curator.md` + 정본 `CURATOR-PROMPT.md` 로 3중 중복 발생. DRY·단일 책임 위해 호출 규약을 `knowledge-curator.md` 로 단일화. `knowledge-graph.md` 는 리다이렉트 한 문단 + §17 트리거만 유지(검증기 T15 통과 보존). Alternative: 양쪽 유지하며 역할 분리(Mickey측/Curator측) (거부: 중복 잔존, 편집 시 두 곳 동기화 부담).

## 반성 사항

- **one-liner 재발 방지 성공**: Phase 2b·3 에서 반복 지적된 `python -c "..."` one-liner 를 이번 세션에서는 사용하지 않음. JSON·구조 검증은 전량 `verify_power_structure.py` 정식 경로로만 수행. must-follow-rules 준수.
- **셸 구분자 오작동 관측**: `python ...; echo $LASTEXITCODE` 실행 시 `;` 가 파일명에 붙어 실패. 현재 셸이 cmd 계열로 `;`·`$LASTEXITCODE` 미지원. 명령을 분리 실행하여 회피. (다음 세션: 종료코드 확인이 필요하면 별도 실행 또는 PowerShell 명시 호출.)
- **설계 분기 사전 합의**: 코드 작성 전 3중 중복 위험을 식별하고 사용자에게 B/A 조합을 제시하여 확정받음. must-follow-rules "모든 중요한 결정은 사용자 확인" 준수. 재작업 없이 첫 구현에 7/7 PASS.

## Phase 5 인계 (다음 세션)

### 다음 세션 목표

Phase 5 — 배포·검증·문서화. install 스크립트 개편(v2 agent + v3 power 양쪽), IDE hook 정식 규격 실측(Phase 3 이월), 문서 갱신, v2/v3/IDE 3 시나리오 회귀 검증.

### 사전 실측 필요 항목

- `install.ps1` / `install.sh` 현재 배포 로직 (v2 → `~/.kiro/agents/` 단방향 seed).
- `~/.kiro/powers/installed.json` 등록 대장 형식.
- kiro-cli 버전 게이트(2.10 미만 시 v3 스킵) 구현 방식.
- IDE `.kiro.hook` 정식 규격 (Phase 3 D-3-2 이월분).

### 검증 방식

- `verify_power_structure.py`·`verify_hooks.py` 회귀 유지.
- Phase 5 신규 검증기: install dry-run 검증 후보.

### 후속

- Phase 4-B(v3 sub-agent 등록): v3 정식 공개 후 `knowledge-curator.md` → sub-agent 프롬프트 승격 재검토(유보).

## 이번 세션 컨텍스트 소모 상태

- 인계 파악 · 사전 실측(6파일) · 설계 분기 합의 · steering 1건 신규 · 4개 파일 편집 · 검증기 확장 · 양쪽 검증 · 계획서·로그 마감.
- 소모율: 중간. Phase 5 는 스크립트 개편 중심이라 실측 부담 있음 → HANDOFF 후 `/clear` 권장.

## Last Updated

2026-07-11 (Phase 4-A 완료)
