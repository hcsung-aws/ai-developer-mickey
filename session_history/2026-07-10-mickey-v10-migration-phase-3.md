# 2026-07-10 · Mickey v10 마이그레이션 · Phase 3

**세션 목표**: v10 power migration Phase 3 — 세션 관리용 공용 파이썬 스크립트 2건 · CLI v3 hook 예시 2건 · IDE hook skeleton 2건 · 별도 검증기 1건 제작. 계획서 §6 Phase 3 CC 4개 항목 자동 검증까지 완료.

## 착수 배경

- Phase 2c(2026-07-09) 산출물: `scripts/verify_power_structure.py` PASS 6/6. steering·POWER·mcp 구조 무손상. 이번 세션 진입 시 재실행하여 온전성 재확인.
- 계획서 §9 인계 지점: hook 계층 3분(CLI v3 · IDE · 공용 로직).
- 사전 실측 결과: `.kiro/hooks/`, `.kiro/scripts/` 부재. CLI v3 hook 규격은 `createHook` 도구 스펙으로 사실상 확정(R1 해소). IDE `.kiro.hook` 은 프로젝트 내 예시 부재.

## 사용자 확정 방향 (2026-07-10)

1. **Power 이전 우선**. v3 에서 power 로 사용 가능한 상태. IDE 는 우선순위 낮음.
2. **Hook 자체는 급하지 않음**. 스크립트가 있으면 명시 호출도 가능. hook 는 skeleton 예시로 남김.
3. Q1(a) — `UserPromptSubmit` hook 생략. 로직 명확성 성립할 때까지 유보.
4. Q2(a) — Serena/Graphify 감지는 `.kiro/settings/mcp.json` · `~/.kiro/settings/mcp.json` 정적 파싱으로 등록 여부만 리포트. INDEX 편집은 하지 않음.
5. Q3(a) — IDE hook 은 skeleton 만 작성, `_note` 필드에 Phase 5 실측 이월 표기.
6. Q4 — 파이썬 스크립트에 P3 분기 4개를 단일책임 함수로 분리, BRANCH 마커 주석으로 검증기가 추적.

## 진행 원칙

- 스크립트 · hook · 검증기 각각 단일 책임 · 느슨한 결합 (Clean Architecture).
- 스크립트는 hook 없이 단독 실행 가능 (`python .kiro/scripts/<name>.py [--project-root PATH]`).
- 표준 출력의 마커는 ASCII only, 자연어 설명은 한글 병기.
- 파일 내용은 UTF-8.
- 사이드 이펙트 없음. 파일 편집·네트워크 접근 없음.
- 원본 자산(power-mickey/, mickey/, examples/) 무변경.

## 산출물

### 신규 (9건)

- `.kiro/scripts/mickey_session_boot.py` — 4개 P3 분기 판정 스크립트. BRANCH 마커: `PURPOSE-SCENARIO`/`HANDOFF`/`BROWNFIELD`/`MCP-TOOLS`. `--project-root`/`--json`/`--read-stdin`/`--brownfield-threshold` 옵션.
- `.kiro/scripts/mickey_session_close.py` — 3개 실측 스크립트. BRANCH 마커: `HANDOFF-SESSION-END`/`SESSION-HISTORY`/`CURATOR-STAGING`. `--project-root`/`--json`/`--read-stdin`/`--today` 옵션.
- `.kiro/hooks/mickey-session-start.json` — CLI v3 `SessionStart` → boot.
- `.kiro/hooks/mickey-session-stop.json` — CLI v3 `Stop` → close.
- `.kiro/hooks/mickey-pre-task.kiro.hook` — IDE `preTaskExecution` → boot (skeleton, `_note` 표기).
- `.kiro/hooks/mickey-post-task.kiro.hook` — IDE `postTaskExecution` → close (skeleton, `_note` 표기).
- `.kiro/hooks/README.md` — 사이드카. hook 목록·활성화 양쪽 분기·스크립트 단독 호출 방법.
- `scripts/verify_hooks.py` — Phase 3 정식 Test Harness. 6개 검증 함수(SRP).
- `session_history/2026-07-10-mickey-v10-migration-phase-3.md` — 본 세션 로그.

### 변경 (2건)

- `IMPROVEMENT-PLAN-v10-power-migration.md`:
  - §8 결정 이력 D-3-1/D-3-2/D-3-3 추가.
  - §7 R1 상태 `[2026-07-10 해소]` 표기.
  - §9 Phase 3 완료 표기 및 Phase 4-A 인계 상세로 재작성.
- `session_history/2026-07-10-mickey-v10-migration-phase-3.md` — 본 로그 마감(결정·반성·인계).

### 미변경 (원본 자산 무손상)

- `power-mickey/POWER.md`, `mcp.json`, `steering/*.md` 6개.
- `mickey/**`, `examples/**` 원본.

## 검증 결과

### `scripts/verify_hooks.py`

```
Summary: PASS 6 / FAIL 0 / total 6
Exit Code: 0
```

| # | 검증 항목 | 결과 | 세부 |
|---|---------|------|------|
| 1 | Session scripts exist | PASS | 파이썬 스크립트 2건 파일 존재 |
| 2 | CLI v3 hooks valid | PASS | JSON 파싱 · version/hooks/trigger/action.type=command/command hint 매치 |
| 3 | IDE hooks skeleton | PASS | JSON 파싱 · trigger 매치 · `_note` 안 SKELETON 표기 |
| 4 | Scripts `--help` exit 0 | PASS | 두 스크립트 모두 exit 0 |
| 5 | Scripts run exit 0 | PASS | `--project-root .` 실 실행 exit 0 |
| 6 | P3 BRANCH markers present | PASS | boot 4개 · close 3개 stdout 등장 |

### 회귀 검증 — `scripts/verify_power_structure.py`

```
Summary: PASS 6 / FAIL 0 / total 6
Exit Code: 0
```

Phase 2c 검증기 재실행하여 steering·POWER 자산 회귀 없음 재확인.

### 스크립트 단독 실행 실측

- `python .kiro/scripts/mickey_session_boot.py --json` — 4개 BRANCH 모두 출력. MCP-TOOLS 는 `serena: [user]`(사용자 홈 mcp.json 감지)·`graphify: []` 실측 반영.
- `python .kiro/scripts/mickey_session_close.py --today 2026-07-10 --json` — SESSION-HISTORY 가 오늘자 로그(`2026-07-10-mickey-v10-migration-phase-3.md`) 정확히 감지. CURATOR-STAGING 은 `~/.kiro/mickey/_curator-staging` 실측.

## 결정 이력

- **D-3-1**: `--read-stdin` 명시 플래그로 stdin 파싱 옵션화 (2026-07-10). 근거: 초기 구현은 `sys.stdin.isatty()` 로 tty 여부 판정. execute_pwsh · CI 같은 non-tty pipe 환경에서 stdin close 지연 시 `read()` 가 block. hook JSON 에서만 `--read-stdin` 을 붙여 명시 활성 → block 위험 원천 차단. Alternative: `select`/`msvcrt` 로 non-blocking read (거부: Windows/POSIX 이식성 저하 · 복잡도 증가).

- **D-3-2**: IDE hook 은 skeleton + `_note` SKELETON 표기, Phase 5 실측 이월 (2026-07-10). 근거: `.kiro.hook` 규격이 이번 세션에 확정되지 않음. skeleton 을 명시적으로 표기해 사용자·검증기·미래 개발자가 skeleton 임을 즉시 인지. Alternative: IDE 규격 실측을 이번 세션에 완료 (거부: 사용자 방침 "Power 이전 우선, IDE 후순위").

- **D-3-3**: Serena/Graphify 정적 감지 (편집 금지, 리포트만) (2026-07-10). 근거: 스크립트만으로는 MCP 런타임 활성 여부 확정 불가. `.kiro/settings/mcp.json` · `~/.kiro/settings/mcp.json` 정적 파싱으로 등록 여부만 리포트. INDEX 편집은 Mickey 가 사용자 확인 후 결정. Alternative: `kiro_powers.activate` 결과 파싱 (거부: v3 도구 API 안정성 미확정 · 스크립트가 kiro 프로세스에 의존하지 않아야 함).

## 반성 사항

- **must-follow-rules 위반 재발**: hook 파일 JSON 유효성 즉시 확인용으로 `python -c "..."` one-liner 사용. `must-follow-rules` 에 명시된 금지 사항이며 Phase 2b 반성 항목이었음에도 이번 세션에서 재발. PowerShell 이스케이프 충돌로 실패. **재발 방지**: JSON 검증은 검증기(`verify_hooks.py`) 안으로 옮겨 정식 검증 경로로만 수행. 즉시 확인이 필요한 경우 `python -m json.tool <file>` 처럼 인수 형태로 호출 (one-liner 금지).

- **로컬 자정 이슈 조기 감지**: close 스크립트 실측 중 로컬 시각이 이미 2026-07-11 로 넘어간 것을 발견. HANDOFF/session_history 날짜 판정에서 오탐 위험. `--today` 옵션을 미리 추가해 대응. hook 자동 호출 시에는 `--today` 없이 로컬 오늘로 판정하므로 자정 근방 세션은 사용자가 인지해야 함 — 다음 사이클에서 정책 검토 후보.

- **subprocess 인코딩 사전 대응**: 검증기가 자식 파이썬 프로세스 stdout 을 캡처할 때 Windows cp949 mojibake 발생 위험을 사전에 인지하고 `PYTHONIOENCODING=utf-8` · `PYTHONUTF8=1` 강제. 재작업 없이 첫 실행에 PASS.

## Phase 4-A 인계 (다음 세션)

### 다음 세션 목표

Phase 4-A — Knowledge Curator 로직을 steering 으로 흡수. v2 `examples/knowledge-curator.json` 프롬프트를 `power-mickey/steering/knowledge-curator.md` 로 이식.

### 계획서 §6 Phase 4-A 요약

- `steering/knowledge-curator.md` 신규. 원본 `mickey/domain/CURATOR-PROMPT.md` 는 이식 금지(그래프 노드 원칙). steering 은 호출 규약(입력·출력·5회 검증)만 요약.
- POWER.md 안내 목록에 `knowledge-curator.md` 추가 (steering 이 6개 → 7개로 확장).
- 세션 종료 hook 이 이 steering 을 `readSteering` 하도록 흐름 명시.
- Pre-staged Apply 패턴(`_curator-staging/`)은 v2 와 동일 동작 유지 (close 스크립트가 이미 감지 중).

### 사전 실측 필요 항목

- `examples/knowledge-curator.json` 최신본 확정. `.m24-bak` · `.m25-bak` · `.m26-bak` · `.m27-bak` 세대 파일 다수 → 정본 파일 확정 필요.
- `mickey/domain/CURATOR-PROMPT.md` 최신본 내용 실측. steering 이 이를 요약하되 이식하지 않음.
- `verify_power_structure.py` 스펙 업데이트 예정 (steering 개수 · 매핑 검증 확장).

### 검증 방식

- `verify_power_structure.py` 확장: steering 6개 → 7개 대응. POWER.md 안내 매핑 완결성에 `knowledge-curator.md` 포함.
- `verify_hooks.py` 는 무변경 (hook 자산 무변경).

### 후속 Phase 예고

- Phase 4-B: v3 sub-agent 등록 (v3 정식 공개 후 재검토, 유보).
- Phase 5: install 스크립트 개편 + 문서 갱신 + 회귀 검증 (v2/v3/IDE 3 시나리오).

## 이번 세션 컨텍스트 소모 상태

- 세션 진입 시 인계 파악 · Phase 2c 산출물 온전성 재확인 · 파이썬 스크립트 2건 작성·검증 · hook 4건 작성 · README 1건 · 검증기 1건 작성·검증 · 계획서·세션 로그 마감.
- 소모율: 중간. 다음 세션(Phase 4-A) 은 steering 1건 작성 + POWER.md 조정 + 검증기 확장 예정 → 여유 충분. HANDOFF 후 `/clear` 는 판단에 맡김.

## Last Updated

2026-07-10 (Phase 3 완료)
