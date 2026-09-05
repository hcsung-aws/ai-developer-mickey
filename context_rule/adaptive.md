# Adaptive Rules

> Mickey가 작업 중 발견한 반복 패턴을 규칙화한 것. 세션 종료 시 사용자 확인.

## Rules

1. **'세션 중 자동 호출' 설계는 실패한다 — 판단+다단계 실행 작업은 강제 중단점에 배치** — Mickey 16, TMI-agent + Curator 동일 실패 (2회)
2. **덮어쓰기 방향 실행 전 소스/대상 diff 필수 — 최신본이 어디인지 확인 없이 install/deploy 금지** — Mickey 18, global→repo 방향 오판 시 최신 domain entry 손실 위험
3. **global `~/.kiro/mickey/` 수정 시 repo `mickey/` 동기화 확인 — 누락 시 install이 오래된 내용 배포** — Mickey 18, domain entry 3개 + 6파일 불일치 발견
4. **저장소 동기화는 파일별 방향 판정 — 일괄 스크립트(install.sh 등)는 모든 파일이 동일 방향일 때만 안전** — Mickey 19, "global이 최신" 일괄 판정으로 CURATOR-PROMPT v2 손실 위험 (3회차: #2,#3 + 이번)
5. **세션 종료 시 HANDOFF.md가 실제로 git add/commit 되었는지 확인 — untracked로 남으면 원격 배포 누락** — Mickey 19, Mickey 18 HANDOFF가 untracked로 남아 다음 세션에서 발견
6. **프로토콜/규칙 추가 전 기존 체계의 폐지/검토를 먼저 수행 — "더 추가"는 같은 실패 반복** — Mickey 20, M14 원칙이 v8/v8.1 자기 자신에게 위반됨 (3회차: v8 추가→v8.1 추가→동일 실패)
7. **자기 개선 진단 시 사용자의 실제 도구 환경 스캔을 첫 단계로 수행 — 환경 불일치가 설계 결함의 근본 원인일 수 있음** — Mickey 20, 다중 AI 도구 환경(Kiro+Claude+AGENTS.md) 발견이 v8.1 실패 진단의 결정적 입력
8. **Python 자동화 스크립트에 `sys.stdout.reconfigure(encoding='utf-8')` 필수 — Windows cp949 환경에서 비-ASCII 출력(em dash, 한글 요약 등) 시 UnicodeEncodeError 발생** — Mickey 22, m22_apply_t1_changes.py 첫 실행 실패 후 수정
9. **SESSION 문서 냉동 상태와 디스크 실측을 분리 취급 — SESSION.md가 최종 갱신되지 않은 채 세션이 종료될 수 있으므로, 진입 시 파일 존재/테스트 통과/산출물 크기 등 디스크 실측을 SESSION 내용보다 우선** — Mickey 35, M34 SESSION 냉동(Phase 2 미기록) vs 실제 디스크 Phase 2 완료(pytest 89 passed) 불일치 발견
10. **git 미추적 글로벌 파일(~/.kiro/mickey/) 편집 전 동일 디렉토리에 백업 파일 생성 필수 — 되돌리기 안전장치 없으면 수술 실패 시 복원 불가** — Mickey 36, GRAPH.md 병합+orphan 수술 전 .m36-bak 생성으로 안전 확보 (M35 domain entry 편집 시도와 동일 패턴 2회차)
11. **프롬프트/설정류 수정 전 런타임 로딩 경로를 실측하라 — SoT 문서 수정 ≠ 런타임 반영** — Mickey 37, CURATOR-PROMPT.md(SoT) 수정분(M36 포함)이 agent JSON 내장 prompt에 미전파 상태였음. md→JSON 동기화 스크립트(m37_sync_curator_prompt.py)를 수정 파이프라인에 포함할 것
12. **인계받은 위험 서술은 diff 실측으로 재정의 후 해법을 정하라** — Mickey 37, M36 인계의 "GLOBAL_ONLY 63건 소실" 추정이 실측(copy-only + DIFF 10건 stale 롤백)으로 뒤집혀 해결 방향 자체(미러링→seed 시맨틱)가 바뀜
13. **파일 쓰기 도구의 취소/실패 보고도 디스크 실측으로 확인 — 취소 보고된 쓰기가 실제 적용된 사례 존재, str_replace 재시도 전 grep으로 디스크 상태 우선 확인** — Mickey 39, adaptive #9(SESSION 냉동 vs 디스크)와 동일한 "보고≠디스크" 계열의 역방향 변형 (3회차)
14. **cp949 콘솔에서 execute_cmd 한글 출력이 잘려 보일 수 있음 — PASS/FAIL 판정은 콘솔 출력이 아닌 파일 리다이렉트 후 실측** — Mickey 39, cp949 계열 2회차 (#8 UnicodeEncodeError → 이번 출력 잘림)
15. **경로 상태를 가진 도구(serena 등)는 세션 시작 시 활성 컨텍스트를 명시 확인 + 첫 쓰기 후 OS 레벨 위치 검증** — Mickey 41, serena create_text_file이 활성 프로젝트 루트(work\kiro 상위)에 오배치 (tool-implicit-root-path-trap 재현 — M44 activate_project 누락으로 3회차 재현, 실행 실패로 즉시 발각)
16. **repo `scripts/` 수정 시 글로벌 재배포(m43_deploy_global_scripts.py) 실행을 세트로 — 수정만 하고 배포 누락 시 글로벌이 구버전으로 동작** — Mickey 44, 개선 A 반영 후 재배포 누락 (#3 global↔repo 동기화 계열의 역방향 변형)
17. **"글로벌 배포" 기록/주장 시 deploy 스크립트(m43_deploy_global_scripts.py)의 FILES 목록 등재를 실측 확인 — 목록 미등재 스크립트는 install 경유로만 배포되어 기록과 실상이 어긋남** — Mickey 45, M44가 배포했다고 기록한 graph_audit.py가 FILES 미등재 (#16 계열의 목록 최신성 사각지대)
18. **설정/도구 동작 진단 시 활성 agent JSON(~/.kiro/agents/)을 3자 대조(repo SoT ↔ 글로벌 설정 ↔ agent JSON)에 포함 + 실효 설정은 실행 중 프로세스 cmdline 실측으로 확정** — Mickey 47, agent JSON의 serena --project 절대 경로 하드코딩(repo SoT 부재 drift, 7주+ 잠복)이 글로벌 mcp.json을 통째 override (#11 런타임 로딩 계열의 역방향 변형)
19. **Python 출력의 파일화에 PowerShell 셸 리다이렉트(`>`) 사용 금지 — utf-8 stdout이 cp949로 재해석된 뒤 UTF-16으로 저장되어 mojibake 리포트 생성. 리포트/산출물은 Python이 직접 utf-8 파일로 기록 (#14의 "파일 리다이렉트 후 실측"은 이 방식으로 대체)** — Mickey 48, cp949 계열 3회차 (#8 UnicodeEncodeError → #14 콘솔 잘림 → 리다이렉트 인코딩 파괴)
