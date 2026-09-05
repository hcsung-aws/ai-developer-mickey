# Mickey 47 Session

## Checkpoint [3/5] — 세션 종료

## Session Meta
- Date: 2026-09-04
- Type: Self-Improvement (도구 환경 진단)

## Session Goal
M46 인계 최상위 과제: Serena 활성 프로젝트 오지정(work\kiro 상위 낙착) 원인 규명 + 다중 세션(1~10 동시) 환경에서의 현실적 설정 방안 분석

## Purpose Alignment
- 기여 시나리오: Usage Scenario 2 (Mickey 자체 개선) — 도구 환경 함정(tool-implicit-root-path-trap 계열)의 근본 해결
- 이번 세션 범위: 사용자 확인 후 확정

## Previous Context (M46)
- 엔트로피 정리 완주: SESSION M39~45 아카이빙 + changelog 백필 + 글로벌 .bak 정리 + INDEX 중복 병합 수술
- Curator 검증 4/5회차 PASS, 승격 3/3
- 최상위 인계: Serena `--project .` 상대 경로가 MCP 기동 cwd 기준으로 해석되어 활성 프로젝트가 조상 디렉토리(work\kiro)로 낙착 → workshop M8 세션 파일 유실 실피해

## 세션 시작 엔트로피 체크 (2026-09-04)
- INDEX 정합성: OK (Curator 유지 관리 상태 양호)
- 루트 SESSION: M46만 존재 (M46이 아카이빙 완료) — OK
- curation 락: 미보유 (M46 release 정상 수행) — OK
- 프로젝트 staging: dangling 없음 (리포트 파일만 잔존) — OK
- 글로벌 staging 잔존물 1건: remember-inline-shell-ban.md (Source: unreal-mcp-demo M1 — 외부 소속, skip. §22 v26으로 사실상 supersede된 것으로 보이나 처분 권한은 Source 프로젝트)
- 구조 문서 노후: FILE-STRUCTURE.md (M35), ENVIRONMENT.md (M37) — 3세션 이상 경과, 갱신 후보
- M45 인계 잔여 중 "자율성 수준 기록"은 이미 해소 확인 (ENVIRONMENT.md에 Level 2 기록 실존)
- 그래프 감사: 불변 조건 전부 통과 (dangling 0 / Path 결손 0 / malformed 0). INDEX 중복 1 (powershell-curl-escape — M46 기대값과 일치)
  - 정리 후보: orphan `cloud` 앵커 노드 (차수 0), [M] cloud Path 노드 5건 하위 그래프 미이관, 중복 엣지 쌍 6건, Edges 표 빈 줄 1
  - 규모: 상위 142 + 하위(cloud) 26 = 168 노드 / 엣지 492
- 미아 세션 파일 2건 여전히 잔존: work\kiro\MICKEY-7-SESSION.md (bvt-anjin-comparison), MICKEY-24-SESSION.md (epic-lore-benchmark)

## Current Tasks
- [x] Serena 오지정 원인 규명 | CC: 활성 프로젝트가 work\kiro로 낙착되는 메커니즘을 실측 증거로 특정
- [x] Option A 적용 | CC: agent JSON + 글로벌 mcp.json에서 --project 제거 (파싱+args 실측 PASS), T1.5 v28 규약 신설 + repo 동기화 (hash 일치), 본 세션 activate_project 성공
- [ ] 새 세션 실측 검증 (사용자 재시작 필요) | CC: 새 세션의 serena가 활성 프로젝트 없이 기동 → activate_project 후 정상 동작

## Progress
### Completed
- 세션 시작 프로토콜 + 엔트로피 체크 + 그래프 감사
- **Serena 오지정 원인 규명 완료** (아래 Key Decisions 근거 참조)

### 원인 규명 증거 사슬 (M47 실측)
1. 본 세션도 재현 중: cwd=ai-developer-mickey(등록된 프로젝트)인데 active project=kiro(work\kiro) → "미등록이라서"가 아님
2. 프로세스 실측 (m47_serena_process_probe.py, psutil): 동시 실행 kiro-cli 세션 7개+ 전부의 serena 프로세스 cmdline이 `--project C:\Users\hcsung\work\kiro` **절대 경로** — 글로벌 mcp.json의 `--project .`가 아님
3. 출처 특정: `~/.kiro/agents/ai-developer-mickey.json` mcpServers.serena.args에 `C:\\Users\\hcsung\\work\\kiro` **하드코딩** — agent JSON의 mcpServers가 글로벌 mcp.json 정의를 override (런타임 cmdline == agent JSON args 일치로 입증)
4. 유입 시점: 최소 2026-07-21 백업(bak-m2)부터 존재 — pre-v10-bak, bak-skill-resources-20260826 모두 동일
5. repo SoT(examples/ai-developer-mickey.json)에는 serena 정의 자체가 없음 — 활성 agent JSON에만 존재하는 로컬 drift
6. M46 인계 가설("`.` 상대 경로가 MCP 기동 cwd 기준 해석") **기각** — 글로벌 mcp.json의 `.`는 agent JSON에 가려져 런타임에 도달한 적 없음. 단, kiro-cli가 MCP spawn 시 cwd=세션 cwd로 넘기는 것은 실측 확인 (cmd.exe 부모 체인 cwd = 각 세션 프로젝트)
7. 부수 발견: 모든 세션의 serena가 work\kiro 전체를 인덱싱 — roslyn(dotnet) 인스턴스 다수 + clangd가 work\kiro 트리 대상으로 중복 기동 (자원 낭비). serena_config.yml에 쓰레기 등록 다수 (work, work\kiro, AppData\Programs\Kiro, workspace 등)
8. kirocrew.json의 serena는 `--project .` 사용 (별도 agent, 이번 수정 범위 밖이나 동일 계열 점검 대상)

### In Progress
- 다중 세션 환경 Serena 설정 방안 옵션 제시 (사용자 결정 대기)

## Key Decisions
- **D-47-1: Serena 설정 Option A (fail-closed) 채택** — `--project` 기동 인자 폐지 + 세션 시작 activate_project 의무화. B(--project . 복원)는 프로젝트 루트 밖 기동 시 fail-wrong(이번 사고 계열 재발), C(프로젝트별 mcp.json)는 10개 프로젝트 유지비 + agent JSON override 우선순위 재검증 부담. A는 위반 시 시끄럽게 실패하여 오배치 불가능 (사용자 승인 2026-09-04)
- **D-47-2: serena_config.yml 쓰레기 등록 정리는 연기** — 실행 중인 serena 프로세스 7개+가 등록 이벤트 시 config를 메모리 사본으로 재기록할 수 있어(shared-file-session-drift 계열), 동시 세션이 정리된 후 수행

## Files Modified
- MICKEY-47-SESSION.md (신규)
- scripts/m47_serena_process_probe.py (신규 — 프로세스 cwd/cmdline 실측 프로브)
- scripts/m47_verify_serena_config.py (신규 — JSON 파싱 + args 검증)
- ~/.kiro/agents/ai-developer-mickey.json (serena --project 하드코딩 제거, 백업: .bak-m47-serena)
- ~/.kiro/settings/mcp.json (serena --project . 제거, 백업: .bak-m47-serena)
- ~/.kiro/mickey/extended-protocols.md (v27→v28, §19.3 Serena 활성화 규약 신설, 백업: .bak-ai-developer-mickey-m47)
- mickey/extended-protocols.md (repo 세대 파일 동기화, hash 일치 검증)

## Lessons Learned
- [Protocol] §22 위반 1회: 세션 초반 `&` 체이닝 인라인 명령 실패 (5회째 재발 패턴) → 원스트라이크 발동, 잔여 셸 작업 단순 단일 명령/스크립트 파일 전용 전환
- 인계 가설(상대 경로 "." 해석)을 검증 전 전제하지 않고 프로세스 실측부터 시작한 것이 유효 — 실제 원인은 설정 계층 override(agent JSON > 글로벌 mcp.json)였음. adaptive #12(인계 위험 서술 diff 실측 재정의) 패턴의 재확인 사례
- [Protocol] Curator augment 번들이 `Base-Hash: pending`으로 산출 → promote가 CONFLICT 오탐 스킵. Curator(LLM)는 sha256을 계산할 수 없으므로 번들 형식 계약과 Curator 능력이 불일치 — **invoke_curator.py에 run 완료 후 Base-Hash 자동 기입 단계를 코드화**하는 것이 정공 (LLM 결정론적 하이브리드 패턴). 이번엔 m47_fix_bundle_basehash.py로 수동 보정 (mtime으로 실 drift 아님을 검증 후 기입)

## Session End 처리 결과
- Curator 5/5 검증 회차 PASS (의도 외 변경 0) → **git diff 자동 보고 옵션화 확정**
- adaptive #18 직접 수정 승인 + context_rule/INDEX.md 반영 (17→18건)
- 글로벌 승격 2/2 PASS (tool-implicit-root-path-trap augment + prompt-doc-vs-runtime-loading augment, 엣지 +2, dangling 0)
- curation 락 해제 완료
- auto_notes 변경: 이번 세션 없음

## Context Window Status
- 원인 규명 완료 시점 ~55% 추정

## Next Steps
- **M48 시작 직후 순서 (사용자 합의 플랜, 2026-09-05)**:
  1. 새 세션 serena 기동 상태 확인 — Option A 첫 실측 검증 (프로젝트 미지정 기동이 정상) → `activate_project <절대 경로>` → 활성 확인
  2. 기존 세션 종료 실측: `scripts/m47_serena_process_probe.py` 재실행 → kiro-cli/serena 프로세스가 자기 자신 것만 남았는지 확인 (눈대중 금지)
  3. 확인 후 보류 정리 (D-47-2) — **자기 serena도 config 공유자이므로 다른 등록 이벤트 전 세션 초반에 수행 + 편집 후 파일 재독 확인**:
     - serena_config.yml 쓰레기 등록 제거 (work, work\kiro, AppData\Programs\Kiro, .kiro\crew\workspace, workspace 등 — 실 프로젝트 여부 사용자 확인 후)
     - work\kiro\.serena\ 처분 (memories 내용 확인 후)
     - 미아 세션 파일 2건 처분 (MICKEY-7 → bvt-anjin-comparison, MICKEY-24 → epic-lore-benchmark)
- kirocrew.json serena도 `--project .` 사용 중 (fail-wrong 내재) — 해당 agent 사용 시점에 동일 수정 권장
- FILE-STRUCTURE.md(M35)/ENVIRONMENT.md(M37) 노후 갱신 (ENVIRONMENT는 Code Analysis Tools에 M47 fail-closed 규약 반영 겸)
