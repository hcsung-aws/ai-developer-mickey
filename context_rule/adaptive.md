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
