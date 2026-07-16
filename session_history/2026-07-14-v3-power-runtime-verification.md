# 2026-07-14 — v3 Power 런타임 실측 검증

- **계획서**: `VERIFICATION-PLAN-v3-power-runtime.md`
- **환경**: kiro-cli v3 런타임, 클라이언트 acp-client, Windows/cmd 계열 셸
- **선행 상태**: Phase 5 사실상 완료, 정적 검증 3종 기준값 일치 (7/7, 6/6, 25/25), 디스크 반영 4종 ALL-SYNCED

## 결과표

| # | 항목 | 판정 | 근거 |
|---|------|------|------|
| V1 | Power 등록 인식 | **PASS** | `kiro_powers list` 에 power-mickey 노출. 이름·설명·키워드·MCP 서버(aws-knowledge-mcp-server) 4필드 전부 v10 내용과 일치 |
| V2 | activate 동작 | **부분 PASS** | POWER.md 전문(v10, Phase 5, 2026-07-13) + steeringFiles 7종 목록 정상 반환. 단 toolsByServer 가 "(No tools available)" — MCP 도구가 proxy 로 노출되지 않음 (아래 V5 관측과 연결) |
| V3 | readSteering ×7 | **PASS (7/7)** | 7종 전부 전문 로드. 핵심 마커 확인: REMEMBER 12(mickey-core) · 4단계(session-protocol) · 3-Tier(knowledge-graph) · 10단계(problem-solving) · 11종 스키마(document-schema) · 50/70/90(context-window) · R/G/S 계약(knowledge-curator). front matter inclusion 도 always 6 + manual 1 정확 |
| V4 | 서빙본-정본 일치 | **PASS** | `scripts/verify_serving_sync.py` (신규) — 9파일 sha256 전부 일치, orphan/누락 0건 |
| V5 | MCP 동작 | **부분 PASS** | 직접 마운트 경로(`mcp_aws_knowledge_..._list_regions`) 정상 — 리전 37건 반환. `kiro_powers use` proxy 경로는 **FAIL**: "MCP server 'power-power-mickey-aws-knowledge-mcp-server' is not connected" |
| V6 | SessionStart hook 발화 | **미발화 (이 환경 기준)** | boot 스크립트는 사이드 이펙트 없는 stdout 리포트 구조(코드 확인) → 파일 산출물 판정 불가. 대신 v3 규격(exit 0 stdout → 컨텍스트 주입)을 관측 지점으로 삼음: 이번 세션 시작 컨텍스트에 Boot Report 미주입. 스크립트 자체는 verify_hooks 항목 5에서 exit 0 확인됨 → hook 트리거가 이 클라이언트(acp-client)에서 발화 안 한 것으로 판정 |
| V7 | steering inclusion 모드 | **자동 주입 없음 (관측)** | readSteering 이전에 에이전트가 REMEMBER 12 내용·Checkpoint 규약을 알지 못했음(간접 증거). `inclusion: always` 6종도 세션 시작·activate 시점에 자동 주입되지 않음. manual 1종 미주입은 확인. **POWER.md 의 "활성 시 자동 편입" 서술과 CLI v3 런타임 실측 불일치** |
| V8 | Stop hook 발화 | **이월** | 구조적으로 세션 종료 후에만 판정 가능. 다음 세션 시작 시 후속 확인 |

## 종합 해석 — v3 CLI 런타임의 실제 Power 소비 모델

실측으로 드러난 소비 모델은 POWER.md 가 가정한 모델과 다르다:

1. **steering 은 자동 주입되지 않는다.** always/manual 구분 없이 전부 `readSteering` on-demand pull 이다. list 시점에 노출되는 것은 POWER.md front matter 의 이름·설명·키워드뿐이고, activate 시점에 POWER.md 본문이 편입된다.
2. **MCP 는 proxy(`kiro_powers use`)가 아니라 직접 마운트로 서빙된다.** power 의 mcp.json 에 명시된 서버 도구가 에이전트 도구 목록에 `mcp_<server>_<tool>` 형태로 직접 올라온다. use 경로는 "not connected" — proxy 서버 인스턴스가 별도로 뜨지 않는 것으로 보인다.
3. **워크스페이스 hook(SessionStart)은 이 클라이언트(acp-client)에서 발화하지 않았다.** kiro-cli chat 단독 실행 환경과 다를 수 있음 — 회귀 ②(CLI v3 부팅)와는 다른 관측 축이므로 환경 축을 분리해서 봐야 한다.

## 영향 및 수정 후보 (사용자 확인 전 실행 금지)

| 후보 | 내용 | 성격 |
|------|------|------|
| F1 | POWER.md 의 "활성 시 steering 자동 편입" 서술을 실측 모델(전부 readSteering pull)로 정정. 세션 시작 절차에 "activate 후 always 6종을 즉시 readSteering 로 pull" 지시 추가 검토 | 문서·프로토콜 정정 |
| F2 | `kiro_powers use` 경로 실패를 전제로, POWER.md·steering 의 MCP 사용 안내를 직접 마운트 경로 기준으로 정정 | 문서 정정 |
| F3 | SessionStart hook 미발화 — 클라이언트(acp-client vs 터미널 v3 부팅) 축 분리 실측 필요. **주의: `kiro-cli chat` 기본 엔진은 v2** (`--help` 실측) → 반드시 `kiro-cli chat --agent-engine v3` 로 부팅해야 v3 hook 축을 검증할 수 있음 | 추가 실측 |
| F4 | V8(Stop hook) 다음 세션 시작 시 후속 확인 | 이월 |

## 신규 산출물

- `scripts/verify_serving_sync.py` — 서빙본-정본 sha256 비교 검증기 (재사용 가능)
- `scripts/check_disk_sync.py` — 세션 시작 시 디스크 반영 확인기 (재사용 가능)
- `VERIFICATION-PLAN-v3-power-runtime.md` — 본 검증 계획서

## 이번 세션 앞부분 요약 (시작 절차)

- 디스크 반영 4종 ALL-SYNCED / 인계 로딩 완료 / 회귀 3종 기준값 일치 (7/7, 6/6, 25/25)
- 작업 후보 A/B/C 제시 → 사용자가 런타임 실측 검증을 우선하기로 결정 → 본 검증 수행

## F1·F2 집행 결과 (2026-07-14, 사용자 승인 후)

수정 범위 사전 확인: steering 7종에는 자동 주입/`kiro_powers use` 서술이 없음(grep 확인) → 수정은 POWER.md 단독.

- **F1**: "활성화 후 즉시 로드되는 것 (Steering, 상시)" 절 → "활성화 직후 반드시 pull 할 것" 으로 개정. CLI v3 실측(자동 주입 없음) 명시 + P3 양쪽 분기(activate 직후 6종 즉시 pull / activate 이전 pull 금지). on-demand 절도 "pull 시점 차이" 기준으로 정정.
- **F2**: "MCP 서버" 절에 소비 경로 실측 추가 — 직접 마운트(`mcp_<서버명>_<도구명>`) 정상 경로, `kiro_powers use` proxy 사용 금지(not connected 실측), toolsByServer 공백은 정상.
- 푸터 Status/Last Updated 갱신 (2026-07-14).
- **검증**: `verify_power_structure.py` 7/7 유지 → `deploy_power.py` 재배포(백업 `power-mickey.bak-20260714-140049.zip`) → `verify_serving_sync.py` IN-SYNC (9파일).

## F3/V8 실측 준비 — 프로브 hook (2026-07-14, 사용자 승인 후)

앞선 F3 안내 오류 정정: `kiro-cli chat` 기본 엔진은 **v2** (`--help` 실측, `--agent-engine` 기본값 v2). 이전 세션의 "회귀 ② CLI v3 PASS" 도 `kiro_powers activate` 서빙 확인일 뿐, 터미널 v3 부팅에서의 hook 발화는 한 번도 측정된 적 없음.

**프로브 설계 (방법 B — 디스크 증거)**: boot/close 스크립트는 의도적으로 사이드 이펙트가 없어 발화를 디스크로 증명 불가, Stop 은 stdout 전달도 없는 트리거라 에이전트 자기보고로도 관측 불가 → append 전용 프로브로 관측.

- 신규(임시): `.kiro/scripts/hook_probe.py` — 호출 시 타임스탬프+트리거명 한 줄을 `.kiro/hook_probe.log` 에 append. 실패해도 exit 0 (hook 체인 무영향).
- 신규(임시): `.kiro/hooks/hook-probe.json` — SessionStart + Stop 두 트리거에서 프로브 호출.
- 스모크 테스트: 수동 호출 1회 → 로그 기록 확인 → 로그 삭제(측정 초기화).
- 회귀: `verify_hooks.py` 6/6 유지 (프로브 추가가 기존 hook 검사에 무영향).
- **관측 종료 후 프로브 2파일 제거 예정** (임시 자산).

판정 기준:
- SessionStart 줄 존재 → V6 재판정 "터미널 v3 발화, acp-client 축만 미발화" / 부재 → v3 전반 미발화로 원인 추적(파일 위치·트리거 표기·버전).
- Stop 줄 수: 응답마다 찍히면 per-response, 종료 시 1회면 per-session — V8 판정 겸 Stop 트리거 의미론 실측.

## F3/V8 실측 결과 (2026-07-15 판독, 사용자 터미널 실행)

**실행**: 사용자가 프로젝트 루트에서 `kiro-cli chat --agent-engine v3` 부팅 → 메시지 2회 → 종료.

**프로브 로그 원문 (판독 후 제거됨)**:

```
2026-07-15T02:08:56 | trigger=Stop | stdin_bytes=142 | cwd=C:\Users\hcsung\work\kiro\ai-developer-mickey
2026-07-15T02:10:48 | trigger=Stop | stdin_bytes=142 | cwd=C:\Users\hcsung\work\kiro\ai-developer-mickey
2026-07-15T02:12:31 | trigger=SessionStart | stdin_bytes=150 | cwd=C:\Users\hcsung\work\kiro\ai-developer-mickey
2026-07-15T02:12:47 | trigger=Stop | stdin_bytes=142 | cwd=C:\Users\hcsung\work\kiro\ai-developer-mickey
2026-07-15T02:13:03 | trigger=Stop | stdin_bytes=142 | cwd=C:\Users\hcsung\work\kiro\ai-developer-mickey
```

**교차검증**: 터미널 에이전트가 인용한 부팅 보고 값(PURPOSE-SCENARIO 존재 / HANDOFF 없음 / code_file_count=69 / serena user·graphify)이 `mickey_session_boot.py --json` 수동 실행값과 전부 일치 → 주입 실재, 환각 배제.

**판정**:

| 항목 | 판정 | 근거 |
|------|------|------|
| V6 재판정 | **터미널 v3 PASS** | SessionStart 발화 + stdout 컨텍스트 주입 규격대로 동작. 미주입은 acp-client 축 국한 |
| V8 | **발화 확인, 의미론 상이** | Stop 은 세션 종료가 아니라 **응답 종료마다** 발화 (메시지 2회 → Stop 2줄). 앞선 2줄은 acp-client 응답 시각과 부합 → **acp-client 도 Stop hook 은 실행** (SessionStart 주입만 안 됨) |

**신규 발견 F5 (설계 문제, 사용자 확인 대기)**: `mickey-session-stop.json` 은 세션 종료 close 프로토콜 의도인데 실측 Stop 의미론은 per-response → close 스크립트가 매 응답마다 실행 중. 사이드 이펙트 없어 무해하나 의도-트리거 불일치 + Stop stdout 은 컨텍스트 미전달이라 실질 효과 없음. hook 설계 재검토 필요 (예: 세션 종료 절차는 hook 이 아니라 사용자 "세션 정리" 요청 경로로 일원화하고 Stop hook 폐기, 또는 다른 트리거 검토).

**프로브 정리**: `.kiro/scripts/hook_probe.py` + `.kiro/hooks/hook-probe.json` + `.kiro/hook_probe.log` 제거 (임시 자산, 계획대로).

## F5 집행 + 문서 반영 (2026-07-15, 사용자 승인 후)

**F5 — stop hook 폐기 (WELC: 검증기 선개정)**:
- 삭제: `.kiro/hooks/mickey-session-stop.json`. close 스크립트(`mickey_session_close.py`)는 "세션 정리" 수동 호출 경로로 유지 (기능 삭제 아님, 트리거만 폐기).
- `scripts/verify_hooks.py` 개정: 항목 2 에서 stop hook 유효성 검사 제거 + **부재 가드** 추가 (재도입 회귀 방지, F5 근거 주석 병기). 기준값 6/6 유지 — 단 항목 2 의 의미가 "start 유효 + stop 부재"로 변경됨.
- `.kiro/hooks/README.md`: 파일 목록에서 stop 행 제거 + "폐기된 hook (F5)" 절 신설 (근거·대체 경로·재도입 가드 명시).
- 회귀: `verify_hooks.py` 6/6 PASS (stop 부재 가드 포함). steering·deploy 경로 무변경이므로 verify_power_structure/verify_deploy_power 재실행은 생략.

**문서 반영**:
- `PROJECT-OVERVIEW.md` Power Mickey 소절 전면 갱신 — 진행(런타임 실측 완료), 실측된 v3 소비 모델 4항(steering 수동 pull · MCP 직접 마운트 · SessionStart 터미널 발화/acp-client 미주입 · Stop per-response→폐기), 검증 기준값에 verify_serving_sync 추가 및 verify_hooks 항목 2 의미 변경 주석. Last Updated 2026-07-15.
- `FILE-STRUCTURE.md` hooks 줄 갱신 (hook 2→1 + F5 폐기 명시).



## 다음 세션 인계 (상세)

### 현재 위치 한 줄 요약

**v3 런타임 실측 검증 사이클 완결.** V1~V8 전 항목 닫힘, 문서 정정(F1·F2)·재배포·stop hook 폐기(F5)·구조 문서 반영까지 완료. 남은 것은 부채 3건(후보 B)과 IDE 묶음(후보 A, 최후순위).

### 이번 세션에서 완결된 상태 (다음 세션이 신뢰해도 되는 사실)

1. **홈 서빙본 = 정본 v10 정정판** (`verify_serving_sync.py` IN-SYNC 9파일, 배포 백업 `bak-20260714-140049.zip`).
2. **실측 확정된 v3 소비 모델** (추측 아님, 전부 디스크/교차검증 증거 있음):
   - steering 은 **자동 주입 안 됨**. always/manual 구분 없이 `readSteering` pull 만이 경로. POWER.md 에 "activate 직후 6종 즉시 pull" 지시 반영됨.
   - MCP 는 **직접 마운트** (`mcp_<서버>_<도구>` 형태로 도구 목록에 노출). `kiro_powers use` proxy 는 "not connected" 실패 — 사용 금지로 문서화됨.
   - **SessionStart hook 은 터미널 v3 에서 발화 + stdout 컨텍스트 주입** (프로브 로그 + code_file_count=69 교차검증). acp-client 축은 주입 안 됨 (단 Stop hook 은 acp-client 에서도 실행됐음).
   - **Stop 트리거는 per-response** (응답마다 발화). 세션 마감 의도와 불일치 → stop hook 폐기(F5). 세션 마감 = close 스크립트 수동 호출로 일원화.
3. **검증 기준값 (변경 있음, 주의)**: `verify_power_structure.py` 7/7 · `verify_hooks.py` 6/6 (**항목 2 의미 변경**: start 유효 + stop **부재** 가드) · `verify_deploy_power.py` 25/25 · `verify_serving_sync.py` IN-SYNC.
4. **kiro-cli 부팅 상식**: `kiro-cli chat` 기본 엔진은 **v2**. v3 는 `--agent-engine v3` 명시 필수. power 는 홈 글로벌 설치라 어디서든 뜨지만, hook 은 워크스페이스(`.kiro/hooks/`) 한정.
5. **문서 최신**: PROJECT-OVERVIEW(Power Mickey 소절 전면 갱신)·FILE-STRUCTURE·hooks README·POWER.md(F1·F2). changelog/docs-09 의 "hook 2건" 서술은 당시 사실 기록이므로 소급 수정 안 함(의도적).

### 다음 세션 작업 후보 (우선순위 순)

**후보 B — 부채 정리 사이클 (권장 착수점)**
1. registry `~/.kiro/powers/registries/user-added.json` 의 power-mickey source.path stale(`work\q\power-mickey`) → 현 경로로 정정. 서빙 무관(installed/ 물리본 서빙)이므로 저위험이나 사용자 확인 후 실행.
2. 영문 changelog `docs/07-changelog-en.md` v9.2 항목 백필 (한글판 v9.2 섹션 번역).
3. `mickey/domain/entries` 잔재 10건 처리 — 계획서 §8-a 권고 (ii) "seed 예시 재분류", 사용자 확인 필수.

**후보 A — IDE 묶음 (사용자 방침상 최후순위)**
- Kiro IDE steering 인식 실측 + IDE `.kiro.hook` 정식 규격 실측 → skeleton 2건 승격 → `verify_hooks.py` 항목 3 개정.
- 전제: 사용자가 Kiro IDE 를 띄울 수 있으면 진행 / 불가하면 건너뜀.

**후보 C — Phase 4-B (조건부 유보)**
- v3 `orchestrate_subagent` 가 커스텀 sub-agent 등록을 지원하면 curator sub-agent 승격 재검토 / 지원하지 않으면 계속 유보.

**소소한 개선 후보 (관찰 기록)**
- `mickey_session_close.py` 의 CURATOR-STAGING 분기가 **빈 디렉토리도 exists 로 판정** (이번 세션 실측). dangling 유무(내용물 존재)까지 봐야 정확. 저위험 수정 후보.

### 다음 세션 시작 절차 — Mickey Power 실사용 경로 (신규, 실측 검증됨)

이번 검증으로 power 실사용이 가능해졌다. 다음 세션은 아래 절차로 Mickey 를 실제로 태워서 시작하라:

1. **부팅**: 프로젝트 루트에서 `kiro-cli chat --agent-engine v3` (v2 로 뜨는 함정 주의). SessionStart hook 이 Boot Report(PURPOSE-SCENARIO/HANDOFF/BROWNFIELD/MCP-TOOLS 4분기)를 자동 주입한다 — 실측 확인됨.
2. **Power 활성**: `kiro_powers activate power-mickey` → **직후 반드시** always steering 6종(mickey-core·session-protocol·knowledge-graph·problem-solving·document-schema·context-window)을 `readSteering` 로 pull (F1 정정 반영된 POWER.md 지시). `knowledge-curator.md` 는 세션 종료 시에만 pull.
3. **MCP**: aws-knowledge 도구는 `mcp_aws_knowledge_mcp_server_...` 직접 마운트 도구를 호출. `kiro_powers use` 는 쓰지 말 것.
4. **디스크 반영 확인**: `python scripts/check_disk_sync.py` — 이번 세션 수정 파일 대상 갱신 필요 (아래 수정 파일 목록 참조).
5. **회귀 4종 분리 실행** (cmd 계열이라 `;` 연결 금지):
   - `python scripts/verify_power_structure.py` (7/7)
   - `python scripts/verify_hooks.py` (6/6, stop 부재 가드 포함)
   - `python scripts/verify_deploy_power.py` (25/25)
   - `python scripts/verify_serving_sync.py` (IN-SYNC)
6. **작업 확인**: 후보 B/A/C 요약 제시 후 사용자 선택 대기. 선택 전 파일 수정 금지.

### 이번 세션 수정/생성 파일 (다음 세션 디스크 반영 확인 대상)

| 파일 | 성격 |
|------|------|
| `session_history/2026-07-14-v3-power-runtime-verification.md` | 신규 — 본 로그 (결과표·프로브 원문·인계) |
| `VERIFICATION-PLAN-v3-power-runtime.md` | 신규 — 검증 계획서 |
| `scripts/check_disk_sync.py` | 신규 — 디스크 반영 확인기 (재사용) |
| `scripts/verify_serving_sync.py` | 신규 — 서빙본-정본 해시 비교기 (재사용, 회귀 4종에 편입) |
| `power-mickey/POWER.md` | 수정 — F1·F2 정정 (재배포 완료) |
| `scripts/verify_hooks.py` | 수정 — 항목 2 stop 부재 가드 |
| `.kiro/hooks/README.md` | 수정 — F5 폐기 절 신설 |
| `.kiro/hooks/mickey-session-stop.json` | **삭제** (F5) |
| `PROJECT-OVERVIEW.md`, `FILE-STRUCTURE.md` | 수정 — 실측 결과 반영 |
| 프로브 3건 (`hook_probe.py`·`hook-probe.json`·`hook_probe.log`) | 생성 후 **제거됨** (임시 자산, 원문은 본 로그에 보존) |

### 주의사항 (재확인된 함정)

- `python -c` one-liner 금지, 검증은 전량 `.py` 스크립트 (must-follow-rules).
- cmd 계열 셸: `;` 구분자 미지원, 명령 분리 실행.
- `power-mickey/**` 수정 후에는 반드시 `python scripts/deploy_power.py` 재배포 (자동 백업) + `verify_serving_sync.py` 확인.
- hook/steering 의 조건부 지시는 P3 양쪽 분기 병기 원칙 유지.

## 세션 컨텍스트 소모 상태

- 수행량: 시작 절차(디스크·인계·회귀) + 검증 계획서 + V1~V8 실측 + F1·F2 정정·재배포 + F3/V8 프로브 설계·판독 + F5 집행 + 구조 문서 반영 + 인계 마감.
- 소모율: 높음. 인계 완료 후 `/clear` 권장.

## Last Updated

2026-07-15 (세션 정리 — close 리포트 확인·인계 작성 완료)
