# 2026-07-13 · Mickey v10 마이그레이션 · Phase 5 (가) install 스크립트 개편

**세션 목표**: Phase 5 진입. (가) install 스크립트 개편 — v2 agent 배포는 유지하고 v3 power 배포를 추가한다. kiro-cli 버전 게이트(2.10)로 조건부 설치, CLI/IDE 호환 유지. 홈 자산 안전(R6)을 위한 백업·clean-replace·idempotent 보장 + test harness.

## 착수 배경

- Phase 4-A(2026-07-11) 완료 상태에서 진입. `power-mickey/` v10 골격(steering 상시 6 + on-demand 1), `.kiro/hooks`·`.kiro/scripts`, `knowledge-curator.md` 흡수 완료. 검증기 `verify_power_structure.py` 7/7, `verify_hooks.py` 6/6.
- 사용자 지시: (가) 먼저. IDE 는 최후순위. CLI/IDE 호환 유지.

## 사전 실측 (task #1)

- **kiro-cli 버전**: `kiro-cli --version` → `kiro-cli-chat 2.12.0`. 게이트 2.10 이상 → v3 설치 대상.
- **installed.json 형식**: `{version, installedPowers:[{name, registryId}], dismissedAutoInstalls}`. `power-mickey` 이미 등록(registryId `user-added`).
- **registries/user-added.json**: `powers:[{name, description, source:{type:'local', path}}]`. 현재 path 가 stale(`work\q\power-mickey`, 존재하지 않는 옛 경로).
- **소비 모델 실증** (`kiro_powers activate power-mickey`): kiro-cli 는 `~/.kiro/powers/installed/power-mickey/` **물리 복사본**을 서빙. registry path 는 provenance 메타데이터일 뿐.
- **결정적 발견 — 현재 설치본은 구 pre-v10 power**: steering 5개(memory-protocol, mickey-core, problem-solving, self-improvement, session-protocol), mcp.json 에 memorygraph, IDE onboarding POWER.md. 프로젝트 v10 세트(steering 7개, mcp.json 은 aws-knowledge-mcp-server 만)와 불일치. → **단순 additive copy 시 orphan(self-improvement.md 등) 잔존 → kiro 가 잘못된 steering 로드**. clean-replace 필수.
- install.ps1/install.sh 둘 다 v2 전용(`~/.kiro/mickey` 서고 + `~/.kiro/agents` JSON 2개), parity 유지 중.

## 사용자 확정 방향 (설계 분기, task #2)

본좌가 결정 4건을 제시하고 사용자 확인:

- **A-2**: 배포 핵심 로직을 공용 `scripts/deploy_power.py`(파이썬 단일 구현)에 두고 install.ps1/.sh 는 얇게 호출. (셸 2벌 중복 회피 · test harness 용이 · 이식성)
- **B-1**: registry(`user-added.json`) stale path 는 손대지 않음. 소비 모델상 서빙 무관. stale path 정정은 부채로 이월(아래 §부채).
- **C**: 버전 게이트 임계값 **2.10 유지**.
- **D**: `deploy_power.py --dry-run` 플래그로 무변경 시뮬레이션 → test harness 가 검증.

## 산출물

### 신규 (3건)

- `scripts/deploy_power.py` — v3 power 배포 단일 구현. 단일 책임 함수 분리:
  - `parse_minor_version` / `version_meets_gate` / `get_kiro_version` — 버전 파싱·게이트(파싱 실패 시 보수적 스킵).
  - `backup_existing_power` — 기존 설치본을 `power-mickey.bak-YYYYMMDD-HHMMSS.zip` 으로 백업(대상 없으면 스킵).
  - `deploy_power_files` — full-dir rmtree + copytree 로 clean-replace(orphan 원천 차단).
  - `ensure_installed_json_entry` — installed.json 항목 보장(없으면 골격 생성, 있으면 무변경 idempotent).
  - `deploy` — 오케스트레이션. 게이트 미달 시 `(skipped=True, [gate 안내])` 반환하고 정상 종료(v2 는 install 스크립트가 이미 배포). BRANCH 주석으로 게이트 분기 표기.
  - 인자: `--power-src` / `--powers-home` / `--kiro-version` / `--min-version` / `--dry-run` (전량 테스트 주입 가능).
- `scripts/verify_deploy_power.py` — test harness. 임시 tempdir 를 powers-home 으로 삼아 실제 홈 무손상 검증. 6개 그룹 25개 체크.
- `session_history/2026-07-13-mickey-v10-migration-phase-5-install.md` — 본 세션 로그.

### 변경 (2건)

- `install.ps1` — agent 설치 후 `python scripts\deploy_power.py` 호출 추가(스크립트 없으면 WARN 후 v2 만 설치). 사용법 안내를 CLI v2 / CLI v3 2줄로 분리.
- `install.sh` — 동일 호출 추가. `python3` 우선 `python` 폴백 감지(플랫폼별 인터프리터 명 차이 흡수).

### 미변경 (원본 자산 무손상)

- `power-mickey/**`, `mickey/**`, `examples/**`, `.kiro/hooks/**`, `.kiro/scripts/**`.
- `~/.kiro/powers/**` (실제 홈) — 이번 세션은 dry-run 까지만. 실제 배포는 사용자 확인 대기(§미결).

## 검증 결과

### `scripts/verify_deploy_power.py` (신규)

```
Summary: PASS 25 / FAIL 0 / total 25
Exit Code: 0
```

| 그룹 | 검증 | 결과 |
|------|------|------|
| 1 | 버전 파싱(정상/경계/빈문자열/숫자없음) | PASS 4 |
| 2 | 버전 게이트(2.12 통과·2.10 경계·2.9.9 미달·1.99 미달·None 미달) | PASS 5 |
| 3 | dry-run 무변경(installed/·installed.json 미생성) | PASS 3 |
| 4 | 실제 배포 + orphan 제거(구 steering 2개 제거·v10 배치·POWER/mcp 배치·백업 zip) | PASS 7 |
| 5 | installed.json 항목 추가 + 재실행 중복 없음 | PASS 2 |
| 6 | 게이트 미달 시 v3 스킵(배포 안 함·안내 메시지) | PASS 4 |

### 실제 홈 대상 dry-run (`deploy_power.py --dry-run`)

계획 출력 확인: 백업 예정 → 기존 제거 예정 → v10 7 steering + POWER.md + mcp.json 복사 예정 → installed.json 항목 이미 존재 스킵. **실제 변경 없음.**

### 회귀 (무변경 재확인)

- `verify_power_structure.py`: PASS 7 / 7
- `verify_hooks.py`: PASS 6 / 6

## 결정 이력

- **D-5-1**: 배포 핵심 로직을 파이썬 단일 구현(`deploy_power.py`)에 두고 install.ps1/.sh 는 얇게 위임 (A-2) (2026-07-13). 근거: 백업·clean-replace·installed.json 갱신을 셸 2벌로 중복하면 동기화 부담·side effect 위험. 단일 파이썬 구현이 dry-run/test harness 로 검증하기 쉽고 플랫폼 문제에서 자유롭다. Alternative: 셸 네이티브 2벌 구현(거부: 중복·검증 난이도).
- **D-5-2**: v3 배포는 full-dir clean-replace (2026-07-13). 근거: 실측 결과 홈에 구 pre-v10 steering(memory-protocol/self-improvement)이 서빙 중. additive copy 는 orphan 을 남겨 kiro 가 잘못된 steering 을 로드. rmtree + copytree 로 원천 차단하되 직전 백업으로 복구 가능(R6). Alternative: steering 디렉토리만 선택 삭제(거부: POWER.md/mcp.json 도 구본이라 전체 교체가 일관적).
- **D-5-3**: 버전 게이트 파싱 실패 시 보수적 스킵(False) (2026-07-13). 근거: 버전을 확정할 수 없으면 v3 배포를 강행하지 않고 v2 만 유지하는 것이 안전. Alternative: 파싱 실패 시 배포 강행(거부: 미검증 환경에 홈 자산 변경 위험).
- **D-5-4**: registry stale path 무처리(B-1) (2026-07-13). 근거: kiro 는 installed/ 물리본을 서빙하므로 registry path 는 서빙에 무관. 이번 사이클 범위(installed 배치 + installed.json)에 집중. Alternative: registry path 정정 포함(보류, 부채로 이월).

## 반성 사항

- **one-liner 재발 방지 성공**: `python -c` 를 사용하지 않음. 모든 검증은 `.py` 스크립트(`deploy_power.py --dry-run`, `verify_deploy_power.py`) 정식 경로로 수행. must-follow-rules 준수.
- **소비 모델 추측 대신 실증**: registry vs installed 소비 모델을 코드 추측으로 넘기지 않고 `kiro_powers activate` 로 직접 확인 → 구 power 서빙 사실 발견. 이 발견이 clean-replace 설계의 근거가 됨.
- **test harness 우선**: 홈 자산 변경 로직을 실제 홈에 돌리기 전에 tempdir harness 로 orphan 제거·idempotent·게이트를 25개 체크로 방어. Working Effectively with Legacy Code 원칙 적용.

## 미결 (다음 세션 인계)

### 1. 실제 배포 실행 여부 (사용자 확인 대기)

현재 홈에는 구 pre-v10 power 가 서빙 중. `python scripts/deploy_power.py`(dry-run 없이) 실행 시 v10 로 교체됨(직전 백업 생성). 사용자 승인 후 실행하고, 실행 후 `kiro_powers activate power-mickey` 로 steering 7개·mcp.json(aws-knowledge)·POWER.md 가 v10 으로 바뀌었는지 회귀 검증 필요.

### 2. Phase 5 잔여 작업

- **문서 갱신**: README 에 CLI v2 / CLI v3 / IDE 3 시나리오 표, `docs/09-v3-power-migration.md`(한/영) 신규, changelog v10 항목.
- **IDE hook 정식 규격 실측**: Phase 3 D-3-2 이월분. (사용자 방침상 최후순위)
- **회귀 시나리오**: v2/v3/IDE 3 시나리오 실측.

### 3. 부채

- registry `user-added.json` 의 `power-mickey` source.path 가 stale(`work\q\power-mickey`). 서빙 무관하나 provenance 정정이 필요하면 별도 사이클에서 B-2 로 처리.

## 문서 갱신 (Phase 5 후속, 같은 날)

### 실제 배포 실행 (사용자 승인)

- `python scripts/deploy_power.py` 실행 → 백업(`power-mickey.bak-20260713-152221.zip`) → clean-replace → v10 서빙 확인(`kiro_powers activate`: steering 7 · aws-knowledge mcp · v10 POWER.md).
- 원본 POWER.md 푸터 Version/Status/Last Updated 를 Phase 5 로 갱신 후 재배포(`bak-20260713-224949.zip`). `verify_power_structure.py` 7/7 유지.

### 문서 산출물

- `docs/07-changelog.md` / `07-changelog-en.md` — 요약 표 v10 행 + 상세 섹션. (발견: 영문 changelog 는 v9.2 도 누락된 기존 부채 → v10 만 추가, v9.2 백필은 부채로 기록)
- `docs/09-v3-power-migration.md` / `-en.md` — 신규. 마이그레이션 서사(왜/설계 원칙/v2-v3 비교/steering 6+1/Phase 진행/배포 파이프라인/memorygraph 제거/검증/교훈).
- `README.md` / `README-en.md` — 설치 안내에 v3 배포 추가, CLI v2/v3/IDE 3 시나리오 표, 구 "실험적 Kiro IDE Power" 섹션(memory-protocol/self-improvement/Memory Graph/IDE 0.7+)을 v10 사실로 전면 교체, 프롬프트 진화 표 v10 행, 문서 목록에 09 링크.
- 검증: README 한/영에서 구 pre-v10 잔재(grep: memory-protocol|self-improvement.md|Memory Graph|IDE 0.7) 0건. `verify_power_structure.py` 7/7 회귀 유지.

### 회귀 검증 3 시나리오 실측 결과

- **① CLI v2** (`kiro-cli chat --agent ai-developer-mickey`, 새 부팅 세션): **PASS** (2026-07-13). 프로브 질문("REMEMBER 몇 개 + 1/11/12번") 실측 — 12개 + 상한·은퇴 규칙 / 1번 목적 우선(PURPOSE-SCENARIO) / 11번 Backpressure(Mickey 8 출처) / 12번 동작 시나리오 확인 필수(Mickey 7-packet 출처). 출처 표기까지 정확 → v17 원문 로드 확증. 음성 기준(steering/POWER.md/memorygraph 언급 없음)도 통과. 참고: v2 는 부팅 시 자동 발화 없음(agent JSON 에는 SessionStart 메커니즘 없음, `.kiro/hooks` 는 v3 전용) — 첫 사용자 입력 후 절차 수행이 정상.
- **② CLI v3** (`kiro_powers activate power-mickey`): **PASS** (2026-07-13). v10 서빙 확인(steering 7 · aws-knowledge mcp · v10 POWER.md).
- **③ Kiro IDE**: 미실측. 사용자 방침상 최후순위, IDE 작업 사이클로 이월.

### 추가 부채

- 영문 changelog v9.2 항목 백필 (기존 누락).

## 다음 세션 인계 (상세)

### 현재 위치 한 줄 요약

**v10 Power Migration Phase 5 사실상 완료.** 남은 것은 IDE 묶음(③ IDE 인식 + IDE hook 실측, 사용자 방침상 최후순위)과 부채 3건.

### 이번 세션에서 완결된 상태 (다음 세션이 신뢰해도 되는 사실)

- 홈 `~/.kiro/powers/installed/power-mickey/` 는 **v10 서빙 중** (steering 7 · aws-knowledge mcp · Phase 5 POWER.md). 백업 zip 2건 존재(`bak-20260713-152221`, `bak-20260713-224949` + 기존 `pre-v10-bak`).
- 회귀 시나리오 **① CLI v2 PASS · ② CLI v3 PASS** (본 로그 "회귀 검증 3 시나리오" 절 참조).
- 문서(changelog·docs/09·README 한/영) 최신. PROJECT-OVERVIEW/FILE-STRUCTURE/계획서 §8·§9 최신.

### 다음 세션 작업 후보 (우선순위 순)

**후보 A — IDE 묶음 (Phase 5 완전 종결)**
- ③ Kiro IDE 로 `power-mickey/` 열어 steering 7개 인식 + `inclusion` 모드(always 6/manual 1) 동작 확인.
- IDE `.kiro.hook` 정식 규격 실측 → `.kiro/hooks/mickey-pre-task.kiro.hook`·`mickey-post-task.kiro.hook` skeleton 을 실측 규격으로 승격 → `verify_hooks.py` 항목 3(SKELETON 표기 검사)을 정식 규격 검사로 개정.
- **전제 분기**: 사용자가 Kiro IDE 를 띄울 수 있으면 진행 / 띄울 수 없으면 이 후보를 건너뛰고 후보 B 로.

**후보 B — 부채 정리 사이클**
1. registry `~/.kiro/powers/registries/user-added.json` 의 power-mickey source.path stale(`work\q\power-mickey`) → 현 프로젝트 경로로 정정 (B-2 승격, 사용자 확인 후).
2. 영문 changelog `docs/07-changelog-en.md` v9.2 항목 백필 (한글판 v9.2 섹션 번역).
3. `mickey/domain/entries` 잔재 10건 처리 — 계획서 §8-a, 권고 (ii) "seed 예시 재분류", 사용자 확인 필수.

**후보 C — Phase 4-B (조건부 유보)**
- v3 의 `orchestrate_subagent` 가 커스텀 sub-agent 등록을 지원**하면** `knowledge-curator.md` → sub-agent 승격 재검토 / 지원하지 **않으면** 계속 유보.

### 다음 세션 시작 시 확인 절차

1. 이전 세션 수정 파일의 디스크 반영 확인 (에디터 버퍼 vs 디스크 불일치 함정). 대상: `session_history/2026-07-13-*.md`, `PROJECT-OVERVIEW.md`, `docs/09-*.md`, `README*.md`.
2. 회귀 3종: `verify_power_structure.py` 7/7 · `verify_hooks.py` 6/6 · `verify_deploy_power.py` 25/25.
3. 기준값과 다르면 원인 파악 우선 / 같으면 작업 후보 확인으로 진행.

### 주의사항 (이번 세션에서 재확인된 함정)

- **셸이 cmd 계열**: `;` 구분자·`$LASTEXITCODE` 미지원. 명령 분리 실행 (Phase 4-A 관측 재현).
- **`python -c` one-liner 금지** (must-follow-rules). 검증은 전량 `.py` 스크립트.
- **agent JSON 검증은 새 부팅 세션 필수** (M23 캐시). v2 는 부팅 시 자동 발화 없음(agent JSON 에 SessionStart 메커니즘 없음) — 첫 사용자 입력 후 절차 수행이 정상.
- **kiro 소비 모델**: `installed/` 물리본 서빙. 프로젝트 `power-mickey/**` 수정 후 홈 반영은 `python scripts/deploy_power.py` 재실행(자동 백업).

### 핵심 파일 지도

| 용도 | 경로 |
|------|------|
| 계획서 (인계 §9 · 결정 §8) | `IMPROVEMENT-PLAN-v10-power-migration.md` |
| 진입 문서 | `PROJECT-OVERVIEW.md`, `FILE-STRUCTURE.md` |
| 배포 | `scripts/deploy_power.py`, `install.ps1`, `install.sh` |
| 검증기 | `scripts/verify_power_structure.py`, `verify_hooks.py`, `verify_deploy_power.py` |
| 마이그레이션 서사 | `docs/09-v3-power-migration.md`(한/영) |
| IDE skeleton (후보 A 대상) | `.kiro/hooks/mickey-pre-task.kiro.hook`, `mickey-post-task.kiro.hook` |

## 이번 세션 컨텍스트 소모 상태

- 인계 파악 · 홈 powers 실측(소비 모델 실증) · 설계 4결정 합의 · deploy_power.py + harness 구현 · 실제 배포 2회 · 문서 6종 갱신 · 회귀 ①② 실측 · 인계 마감.
- 소모율: 높음. HANDOFF 후 `/clear` 권장.

## Last Updated

2026-07-13 (Phase 5 (가) install 개편 + 실제 배포 + 문서 갱신 + 회귀 ①② + 인계 완료)
