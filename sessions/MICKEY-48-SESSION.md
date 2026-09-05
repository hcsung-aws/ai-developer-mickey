# Mickey 48 Session

## Checkpoint [4/5]

## Session Meta
- Date: 2026-09-05
- Type: Self-Improvement (도구 환경 검증 + 보류 정리 + 파이프라인 개선)

## Session Goal
M47 인계 플랜 수행: ① Serena Option A(fail-closed) 첫 실측 검증 ② 기존 세션 종료 실측 ③ D-47-2 보류 정리 (serena_config.yml / work\kiro\.serena / 미아 세션 2건) ④ invoke_curator.py Base-Hash 자동 기입 코드화

## Purpose Alignment
- 기여 시나리오: Usage Scenario 2 (Mickey 자체 개선) — 도구 환경 fail-closed 전환 완주 + Curator 파이프라인 형식 계약 결함 해소
- 이번 세션 범위: M47 Next Steps 4항목 (사용자 합의 플랜 2026-09-05)

## Previous Context (M47)
- Serena 오지정 근본 원인 = 활성 agent JSON의 `--project C:\...\work\kiro` 하드코딩 (글로벌 mcp.json override, 7주+ 잠복)
- Option A 적용 완료: agent JSON + 글로벌 mcp.json에서 --project 제거, T1.5 v28 §19.3 신설
- Curator 검증 5/5 PASS → git diff 자동 보고 옵션화 확정
- 발견된 결함: Curator augment 번들 `Base-Hash: pending` → promote CONFLICT 오탐 (LLM은 해시 계산 불가)

## Current Tasks
- [x] Serena Option A 첫 실측 검증 | CC: 새 세션 serena가 프로젝트 미지정 기동 → activate_project 절대 경로 → 활성 확인. **완료** — fail-closed 에러 실측 + 활성화 성공 + cmdline --project 부재
- [x] 기존 세션 종료 실측 | CC: m47_serena_process_probe.py 결과에 자기 자신 외 kiro-cli/serena 프로세스 없음. **완료** — kiro-cli 1개(자신)뿐
- [x] D-47-2 보류 정리 | CC: serena_config.yml 쓰레기 등록 제거 + work\kiro\.serena 처분 + 미아 세션 2건 처분. **완료** — A1~A3 제거(A4 유지, 사용자 확정)+재독 검증, .serena 삭제, 미아 2건 비교 분석 후 삭제(양쪽 다 정식본이 후기 완결 상위집합, 사용자 승인)
- [x] invoke_curator.py Base-Hash 자동 기입 | CC: run 완료 후 augment 번들 pending이 실제 sha256으로 자동 대체, 테스트 통과, adaptive #16 재배포 세트 준수. **완료** — fill_pending_basehash 신설(drift 시 pending 유지로 CONFLICT 계약 보존), 테스트 6건 추가(25/25, 전체 167 passed), m43_deploy 재배포 ALL PASS

## Progress
### Completed
- 세션 시작 프로토콜 (T2/T3a/T1.5 로딩)
- **[1단계 PASS] Option A 첫 실측**: serena 미지정 기동(fail-closed 에러 확인) → activate_project 절대 경로 성공 → 활성 일치. 프로세스 cmdline에서 --project 부재 실측
- **[2단계 PASS] 구세션 종료 실측**: m47_serena_process_probe.py — kiro-cli는 자기 자신(pid 29132)뿐. Kiro.exe 다수는 IDE 프로세스(serena 자식 없음, 무관)
- **[3단계 A·B 완료]**: serena_config.yml에서 A1(work)/A2(work\kiro)/A3(Programs\Kiro) 제거 (A4 crew\workspace는 사용자 확정 유지). 백업 .bak-m48 + 재독 검증 통과, 잔여 17건. work\kiro\.serena 삭제 (memories 0건 재확인 후)
- **[3단계 C 분석 완료]**: 미아 세션 2건 모두 소속 프로젝트에 동명 파일 존재 — 양쪽 다 미아=세션 초 초안, 정식=같은 세션의 후기 완결본(상위집합). 근거: MICKEY-7 미아(19:20)<정식(19:36, 완료 마킹+교훈 추가), MICKEY-24 미아(08-26 스켈레톤)<정식(08-28 5/5 완결). 정식 파일 자체에 "create_text_file flush 실패→fs_write 재작성" 교훈 기록 — 미아는 오지정 루트에 남은 초안 사본으로 확정

### In Progress
(없음)

### 4단계 상세 (invoke_curator.py Base-Hash 코드화)
- `global_root()` 신설: promote_knowledge와 동일한 MICKEY_GLOBAL_ROOT env 규약 (테스트 격리 겸용)
- `fill_pending_basehash(staging, run_started)`: gd-*.md의 pending 마커를 대상 entry sha256으로 치환. 안전 조건 — entry mtime ≥ run_started면 타 세션 실제 drift로 판정, pending 유지 (promote CONFLICT 계약 보존). Entry-Path 검증은 promote와 동일 (entries/ 하위 + .. 금지)
- do_run 훅 위치: attempts 루프 종료 직후, 완주 판정 전 — 실패 시도의 부분 산출물도 직접 대행 경로에서 재사용되므로 성공 여부 무관 수행
- 검증: 신규 테스트 6건 (기입/drift 유지/대상 부재/pending 없음 스킵/경로 탈출 거부/run 통합), 전체 스위트 167 passed
- 재배포: m43_deploy_global_scripts.py ALL PASS (invoke_curator.py hash 705cdc132139, FILES 등재 실측 확인 — adaptive #17)

## Key Decisions
- D-48-1: serena_config.yml A4(.kiro\crew\workspace) 유지 — kirocrew 계속 사용 (사용자 확정 2026-09-05)
- D-48-2: 미아 세션 2건 이동이 아닌 삭제 — 비교 분석 결과 양쪽 다 미아=세션 초 초안, 정식=동일 세션 후기 완결본(상위집합). 이동 시 완결본 훼손/이중 로그 위험만 존재 (사용자 승인 2026-09-05)
- D-48-3: Base-Hash 자동 기입의 drift 안전 조건 = entry mtime ≥ run_started면 기입 거부 — 오탐(pending) 해소와 정탐(실제 drift CONFLICT) 보존을 분리

## Files Modified
- MICKEY-48-SESSION.md (신규)
- scripts/m48_serena_config_cleanup.py (신규 — 백업+정확일치 제거+재독 검증)
- scripts/m48_orphan_session_compare.py (신규 — Python 직접 utf-8 리포트 기록)
- scripts/invoke_curator.py (fill_pending_basehash + global_root 신설, do_run 훅 — 글로벌 재배포 완료)
- scripts/tests/test_invoke_curator.py (TestFillPendingBasehash 6건 추가)
- ~/.serena/serena_config.yml (A1~A3 제거, 백업: serena_config.yml.bak-m48)
- ~/.kiro/mickey/scripts/ (m43_deploy 재배포 4파일)
- 삭제: C:\Users\hcsung\work\kiro\.serena\, work\kiro\MICKEY-7-SESSION.md, work\kiro\MICKEY-24-SESSION.md

## Lessons Learned
- [Protocol] §22 원스트라이크 발동: PowerShell `>` 리다이렉트가 Python utf-8 stdout을 cp949로 재해석해 UTF-16 mojibake 리포트 생성 (adaptive #14의 신종 변형 — 콘솔 잘림이 아니라 리다이렉트 인코딩 파괴). 대응: 리포트는 Python이 직접 utf-8 파일로 기록, 잔여 셸 작업 스크립트 전용 전환 → adaptive #19 + 글로벌 augment로 승격됨
- [Protocol] serena execute_shell_command의 tool_timeout(240s)은 Curator run(6분+)보다 짧음 — invoke_curator는 execute_cmd 계열로 호출할 것. 호출 측이 끊겨도 자식 프로세스는 완주할 수 있으므로, 타임아웃 시 죽이지 말고 프로세스 생존 실측(m48_wait_curator.py) → 완주 대기 → 디스크 실측 판정이 정답 (락 owner.json state가 완주 증거)

## Session End 처리 결과
- Curator COMPLETED (exit 0, 376s) — Base-Hash 자동 기입 첫 실전 동작 확인 (augment 기입 / new 대상 없음 pending 유지)
- adaptive #19 직접 수정 승인 + context_rule/INDEX.md 반영 (18→19건)
- 글로벌 승격 2/2 PASS (incomputable-field-placeholder-backfill new 엣지+3 / windows-cp949-artifact-ascii-defense augment) — dangling 0, Backlink 2행 반영
- **augment가 자동 기입 해시로 통과 — M47 CONFLICT 오탐 루프 end-to-end 봉합 실증**
- curation 락 해제 완료
- auto_notes 변경: 이번 세션 없음

## Context Window Status
- 세션 종료 시점 중반 (~40% 추정)

## Next Steps
- **M49 순서 (사용자 지시 2026-09-05): 3→1→2**
  1. **(3) serena 최종 확인 + .bak-m48 삭제**: 새 세션에서 §19.3 활성화 규약 수행(미지정 기동 확인 → activate_project) + 정리된 serena_config.yml(17건)로 정상 동작 확인 → 안정 확인되면 `~/.serena/serena_config.yml.bak-m48` 삭제
  2. **(1) M47 백업 3종 삭제**: `~/.kiro/agents/ai-developer-mickey.json.bak-m47-serena`, `~/.kiro/settings/mcp.json.bak-m47-serena`, `~/.kiro/mickey/extended-protocols.md.bak-ai-developer-mickey-m47` — Option A 검증 완료(M48)로 삭제 시점 도래. 삭제 전 destructive-target-strict-matching 준수
  3. **(2) 노후 문서 갱신**: ENVIRONMENT.md(M37) — Code Analysis Tools에 §19.3 fail-closed 규약 반영, FILE-STRUCTURE.md(M35) — depth 2 트리 갱신
- kirocrew.json serena `--project .` 수정은 해당 agent 사용 시점에 (fail-wrong 내재)
