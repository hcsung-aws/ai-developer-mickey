# Mickey 33 Session Log

## Checkpoint [1/5]

> §19 Tier 3 baseline 활성화의 첫 실행. `/code init` 결과의 미설치 LSP 4종(cpp/rust/typescript/python) 조사 → typescript/python 즉시 자율 설치 + clangd 단독 자율 설치 + Pyright PATH 확장. Rust 는 건너뜀.

## Session Meta
- Type: Infrastructure (개발 환경 셋업, Tier 3 LSP 활성화 지원)
- Mickey: 33
- Date: 2026-07-01 ~ 07-02
- Autonomy: Level 2 (Balanced) + batch-confirm-autonomous-proceed (사용자 "바로 설치 가능하면 직접 설치" 승인)

## Session Goal
Kiro CLI 내장 `code` 도구(Tier 3 baseline) 의 LSP 기능을 실용 수준으로 활성화하기 위해, 사용자 환경에 미설치된 LSP 서버 4종(cpp/rust/typescript/python)의 설치 방법을 파악하고 자율 가능한 것은 직접 설치한다.

## Purpose Alignment
- 기여 시나리오: **Scenario 1** (소프트웨어 개발 지원 인프라). 본 프로젝트는 Python/JSON/Markdown 중심이라 실제로는 Pyright 우선. 다만 §19 감지 로직의 실전 검증도 겸함 → Scenario 2 (Mickey 자체 개선) 부수 성과.

## Previous Context
- Mickey 32 (2026-07-01 14:40 인계): T1.5 §19 External Code Analysis Integration 신설 + §1 Brownfield Phase 2 도구 위임 축소 + T1 SESSION PROTOCOL 4a 추가 + FILE-STRUCTURE 스키마 필수/선택 분리. Kiro CLI `code` 도구 baseline (Tier 3) 확정.
- M32 인계 0순위: "본 세션 결과 안정, 다음 세션(=M33) 자연 적용". 프로토콜 신규 적용 첫 세션.
- M30~M31 미처리 항목 (3순위): adaptive #9 이식 검토, `iterative-measurement-deepening` 트리거 확장, `m21_measure_usage.py --exclude-meta`, HANDOFF Curator 사전 분류 표준화.
- Curator EmptyResponse 는 외부 fix 대기 (Anthropic #17743 / Kiro #6163).

## Entropy Check (세션 시작 시)
- INDEX 정합성: ✅ context_rule/INDEX.md, common_knowledge/INDEX.md, auto_notes/NOTES.md 모두 실재 파일과 일치
- auto_notes 최신성: ⚠️ NOTES.md Last Updated = 2026-06-26 (M29). M30~M32 4세션 동안 auto_notes 변경 없음. 세션 진행 중 필요 시 갱신
- SESSION 아카이빙: ✅ 프로젝트 루트에는 세션 파일 없음. 모두 `sessions/` 아래
- 구조 문서 최신성: ⚠️ PROJECT-OVERVIEW.md Last Updated = 2026-06-23 (M27). ENVIRONMENT.md Last Updated = 2026-05-13 (M18). FILE-STRUCTURE.md 는 M32에 새 스키마로 갱신 완료. 다음 갱신 여부는 작업 결정 후 판단
- 코드 분석 도구 감지 (§19 첫 자연 적용):
  - Tier 1 Serena: 프로젝트 루트 `.serena/` 미감지. 상위 `C:\Users\hcsung\work\kiro\.serena/` 존재 (M32 확인분 유지)
  - Tier 1 Graphify: `graphify-out/` 미감지
  - Tier 3 Kiro CLI 내장 `code`: 항상 활성. `.kiro/lsp.json` 미존재 → `/code init` 미실행 상태. 필요 시 사용자에게 실행 안내
  - FILE-STRUCTURE.md "Code Analysis Tools" 항목 M32 감지 결과 유효
- Curator staging: 글로벌 `~/.kiro/mickey/_curator-staging/` 1건(`pat-parameterized-script-reuse.md`, 2026-07-01 14:40 갱신) — 본 프로젝트 source 여부 확인 필요. Source 외부면 skip + 카운트
- 포스트모템 트리거: 변경 효과 검증은 2026-09-19 이후. 일반 트리거(10세션)도 미도달

## Current Tasks

### T1. LSP 의존성 조사 (Python 스크립트)
- [x] `scripts/m33_probe_lsp_deps.py` 작성/실행 | CC: 런타임/서버/컴파일러 존재 여부 표 산출

### T2. 즉시 자율 설치 (사용자 승인 이미 있음)
- [x] `npm install -g typescript-language-server typescript` | CC: `Get-Command` 로 실행 파일 감지 (5.3.0)
- [x] `pip install --user pyright` | CC: `pyright-langserver.exe` LSP 응답 확인

### T3. 사용자 결정 대기 → 결정 반영
- [x] 결정 수집: Pyright PATH = B / Rust = skip / C++ = C1
- [x] C++ 결정 논거 확인: clangd 는 clang 파서를 내장하므로 별도 컴파일러 불필요 → C1 확정

### T4. C1: clangd 단독 자율 설치
- [x] `scripts/m33_install_clangd.py` 작성/실행 | CC: `%USERPROFILE%\.local\clangd\clangd_22.1.6\bin\clangd.exe --version` = 22.1.6

### T5. B: 사용자 PATH 확장 (Pyright + clangd bin)
- [x] `scripts/m33_backup_user_path.py` — 원본 PATH 백업 (rollback 대비)
- [x] `scripts/m33_extend_user_path.py` — winreg + WM_SETTINGCHANGE broadcast
- [x] `scripts/m33_verify_path_registry.py` — Registry 재조회 검증 | CC: 두 항목 [OK] 확인 (12 entries, type=REG_EXPAND_SZ)

### T6. §19 감지 마커 이슈 기록
- [x] Kiro CLI 실 산출물 위치는 `.kiro/settings/lsp.json` — 프로토콜 §19.2 (`.kiro/lsp.json` 또는 `lsp.json`) 감지 로직 보정 후보

## Progress

### Completed
- T0 (SESSION 사전 기록, 엔트로피 체크)
- T1~T6 전부

### InProgress
- 없음

### Blocked
- 없음 (kiro-cli 재시작은 사용자 액션이라 세션 외 처리)

## Key Decisions

- **D-33-1**: LSP 서버 4종 설치 자율성 판정 — Node 있으면 typescript-language-server 자율(rollback 명확), pip 있으면 pyright 자율(--user 스코프), Rust/C++는 규모/PATH 변경 이슈로 사용자 확인 필수. 사용자 응답 기반 최종 결정: TS+Py 자율 완료, Rust skip, C++ 는 clangd 단독(C1)
- **D-33-2**: Pyright PATH 조치 — 프로젝트 로컬(lsp.json 절대경로) vs 사용자 PATH 확장 중 B(PATH) 선택. 근거: `/code init -f` 재실행 시 lsp.json 덮어쓸 위험 회피 + pipx 등 부산물도 즉시 활성
- **D-33-3**: C1(clangd 단독) 확정 — clangd 는 clang 파서를 실행 파일에 내장하므로 LSP 기능(diagnostics/hover/refs/rename)에는 별도 컴파일러 불필요. 시스템 헤더 참조가 필요해지면 그때 LLVM 툴체인 추가
- **D-33-4**: PATH 수정은 winreg + WM_SETTINGCHANGE broadcast (Python 표준 라이브러리) 사용. `setx` 1024자 잘림 위험 회피 + registry 타입(REG_EXPAND_SZ) 유지
- **D-33-5**: batch-confirm-autonomous-proceed 적용 13+회 누적 — 사용자 "바로 설치 가능하면 직접 설치" 응답 기반. 3조건(CC 명확 + rollback 파일/스크립트 존재 + `--version`/registry 재조회 검증 가능) 충족

## Files Modified

### 신규 (repo)
- `scripts/m33_probe_lsp_deps.py` — LSP 런타임/서버/컴파일러 존재 조사
- `scripts/m33_install_clangd.py` — GitHub Releases 최신 clangd Windows zip 다운로드/압축 해제
- `scripts/m33_backup_user_path.py` — HKCU\Environment\Path 백업
- `scripts/m33_extend_user_path.py` — 사용자 PATH 에 Pyright/clangd bin 추가 + WM_SETTINGCHANGE broadcast
- `scripts/m33_verify_path_registry.py` — Registry 재조회 검증
- `scripts/m33_cleanup_staging.py` — 처리된 Pre-staged 3건 삭제
- `scripts/backup/user-path-m33-20260702-001352.txt` — 원본 사용자 PATH 백업 (rollback 소스)
- `common_knowledge/windows-user-path-extension.md` — Windows 사용자 PATH 확장 표준 조합 (Curator 승인분)
- `common_knowledge/kiro-cli-lsp-init-settings-location.md` — Kiro CLI `/code init` 산출물 실제 위치 (Curator 승인분)
- `sessions/MICKEY-33-SESSION.md` (본 파일)

### 변경 (repo)
- `common_knowledge/INDEX.md` — 신규 2건 등재, Last Updated → 2026-07-02 (Mickey 33)

### 변경 (글로벌)
- `~/.kiro/mickey/machine-env.md` — "Installed LSP Servers" 섹션 append (Curator 승인분 3)

### 시스템 상태 변경 (repo 외부)
- `C:\Users\hcsung\AppData\Roaming\npm\` — typescript-language-server + typescript 전역 설치
- `C:\Users\hcsung\AppData\Roaming\Python\Python313\Scripts\` — pyright + pyright-langserver + nodeenv (pip --user)
- `C:\Users\hcsung\.local\clangd\clangd_22.1.6\` — clangd 22.1.6 단독 배치
- **HKCU\Environment\Path** — 2 entries 추가 (Pyright Scripts + clangd bin), 12 entries total, REG_EXPAND_SZ 유지

## Lessons Learned

- [Protocol] **§19 감지 마커 위치 불일치** — 프로토콜 §19.2 는 `.kiro/lsp.json` 또는 `lsp.json` 을 확인하지만 Kiro CLI `/code init` 실제 산출물은 `.kiro/settings/lsp.json` (2026-07-01 실측, Kiro CLI). §19 감지 로직 보정 후보. 다음 세션에서 프로토콜 정정 검토 필요 (Mickey 33)

- [Protocol] **Windows 사용자 PATH 확장 = winreg + WM_SETTINGCHANGE 표준 조합** — `setx` 는 1024자 잘림 위험. `[Environment]::SetEnvironmentVariable('Path',..,'User')` 는 PowerShell 인용부호 지옥. Python `winreg.SetValueEx` + `ctypes.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, ...)` 조합이 최적 — 원본 타입(REG_EXPAND_SZ) 유지 + 새 프로세스 즉시 반영. 재사용 스크립트로 정형화 (Mickey 33)

- [Protocol] **LSP 서버 `--version` 응답 형태의 정상 오류 인식** — pyright-langserver 는 stdio/socket 지정 없이 실행하면 "Connection input stream is not set" 에러 반환하며 exit 1. 이는 정상 로드 신호로 해석해야 함. `--version` 만으로 판단 금지 — 실제 실행 가능성은 로드된 스택 트레이스로 판정 (Mickey 33)

- [Protocol] **batch-confirm-autonomous-proceed 13+회 누적** — 다양한 시스템 변경(pip 설치, npm 전역 설치, GitHub 다운로드, Windows registry 수정)에도 3조건 충족 시 유효. 이 세션의 5단계(설치/다운로드/PATH/broadcast/검증) 자율 진행 (Mickey 33)

## Context Window Status
~35% (Curator 반영 + staging 정리 + machine-env append 후 추정)

## Curator 결과 (본체 우회 판단, EmptyResponse 외부 fix 대기 중)

**직접 수정 영역**: 없음 (신규 지식 항목은 승인 경로 경유가 안전, `adaptive.md` 는 반복 위반 아님)

**Pre-staged 초안 3건 → 사용자 결정: "1,2,3 다 승인 / 1·2는 글로벌 대신 이 프로젝트 common_knowledge/"**

| # | 초안 | 최종 이동 위치 | 상태 |
|---|------|--------------|------|
| 1 | `dom-windows-user-path-extension.md` | **`common_knowledge/windows-user-path-extension.md`** (사용자 지정, 원안: 글로벌 `domain/entries/`) | ✅ 이동 완료 |
| 2 | `dom-kiro-cli-lsp-init-settings-location.md` | **`common_knowledge/kiro-cli-lsp-init-settings-location.md`** (사용자 지정) | ✅ 이동 완료 |
| 3 | `machine-env-lsp-servers.md` | `~/.kiro/mickey/machine-env.md` (섹션 append) | ✅ append 완료 |

**부수 갱신**:
- `common_knowledge/INDEX.md` — 신규 2건 등재, Last Updated 2026-07-02 (Mickey 33)
- 글로벌 `domain/INDEX.md`, `GRAPH.md` — 사용자 결정으로 글로벌 승격 없어 갱신 불필요
- staging 3건 삭제 완료 (`scripts/m33_cleanup_staging.py`), staging 비어 있음

**사용자 결정 해석**: 이 두 지식은 Kiro CLI/Windows PATH 라는 특정 도구/OS 함정으로 아직 다른 프로젝트 확산이 즉시 필요하지 않다고 판단. 이후 다른 프로젝트에서 유사 요구 발생 시 글로벌 승격 재검토 후보.

**auto_notes 변경 내역**: 없음 (본 세션에서 `auto_notes/` 미변경)

## Next Steps

### 사용자 후속 액션 (kiro-cli 세션 재시작 필수)

1. **kiro-cli 재시작**: 현재 세션은 옛 PATH 상속 상태. 종료 후 새 세션 열어야 pyright/clangd 자동 감지
2. **`/code init -f`** 실행: LSP 재초기화 → 지원 언어별 초기화 상태 재확인
   - 기대 결과: `✓ pyright (python) initialized`, `✓ typescript-language-server (typescript) initialized`, `✓ clangd (cpp) initialized`, `○ rust-analyzer not installed`, 나머지 not installed
3. 필요 시 `/code status` 로 상태 확인

### 프로토콜 개선 후보 (다음 세션 협의)

- **§19.2 감지 마커 보정**: `.kiro/settings/lsp.json` 추가. 현 세션의 lessons `[Protocol]` 태그로 기록됨
- clangd 버전 폴더명 안정화(`clangd_current` symlink 등) — 오버엔지니어링 여부는 사용자 판단

### 보류

- 인계 미처리 4항목(adaptive #9, iterative-measurement-deepening 트리거 확장, --exclude-meta, Curator 후보 사전 분류) — 다음 세션 결정
- `_curator-staging/pat-parameterized-script-reuse.md` (외부 source, skip 유지)
