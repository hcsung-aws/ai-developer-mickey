# Mickey 43 Session

## Checkpoint
[0/5]

## Session Meta
- Type: Self-Improvement (Curator 호출 코드화 + curation 락 + M42 크래시 잔여 정리)
- Date: 2026-08-21 ~ 2026-08-22
- Track: CLI (master 브랜치)

## Session Goal
M42 포스트모템 개선 후보 2건 반영: ① Curator 호출을 코드(invoke_curator.py)로 전환하여 동시 큐레이션 락을 코드 경로에 내장 ② PowerShell 원스트라이크 규약 명문화. + M42 크래시(HANDOFF 미생성)로 남은 미커밋 잔여물 정리

## Purpose Alignment
Infrastructure (자기 개선) — 세션 종료 프로토콜의 Curator 경로를 지시 기반에서 코드 기반으로 강화. M41(쓰기 격리) → M42(전송 전환) → M43(호출 코드화 + 상호 배제)의 연속선

## Previous Context (M42 SESSION 요약 — HANDOFF 부재, 크래시)
- M42 작업 자체는 완료 (커밋 e16f3c0): delegate→use_subagent 전환, §17 v24, T1 v19, 경량 포스트모템
- 크래시로 미완: 개선 후보 2건 사용자 결정, 미커밋 4건, 세션 종료 프로토콜 (Curator 실전 1회차 미수행)
- M42 미커밋 잔여: MICKEY-42-SESSION.md 수정분, POSTMORTEM-2026-08-21.md, scripts/m42_measure_usage.py, examples JSON 백업 1건

## Current Tasks
- [ ] M42 잔여물 커밋 | CC: git status clean (백업 파일 처분 포함)
- [ ] mickey_lock.py + promote 리팩토링 | CC: 기존 test_promote_knowledge.py 전체 통과
- [ ] invoke_curator.py | CC: 락 획득→headless 호출→staging diff→리포트 왕복 + 경합/강제 진입 테스트 통과
- [ ] §17 v25 + T1 v20 | CC: 글로벌+repo 미러 hash match, 검증 스크립트 ALL PASS
- [ ] PowerShell 원스트라이크 규약 | CC: 문서 반영 + 별도 커밋
- [ ] 글로벌 배포 | CC: ~/.kiro/mickey/scripts/ 3파일 동기화 실측

## Progress
### Completed
- **범위 확인 + 재검증** (사용자 질의 대응):
  - 동시 큐레이션 문제는 같은 프로젝트 한정 확인 (§17 v24 453행). 타 프로젝트 병렬은 구조적 안전
  - crosstalk 원흉은 delegate의 전역 랑데부 저장소(.subagents + user_notified 선점)이지 subprocess가 아님을 기록(M37/M42)으로 재확인
  - m43_probe_headless_transport.py 실측: kiro-cli chat --no-interactive는 in-band(stdout 파이프) + .subagents 무변화 — ALL PASS (scripts/output/m43_probe.txt)
- promote 락 실체 확인: promote_knowledge.py 198~228행, ~/.kiro/mickey/.promote.lock/ mkdir 원자성 + owner.json + 10분 stale 자동 회수. 글로벌 배포본 ~/.kiro/mickey/scripts/
- **M42 잔여물 커밋** (de999db): POSTMORTEM + m42_measure_usage.py + SESSION 수정분. *.bak-* gitignore 처리
- **mickey_lock.py + promote 리팩토링** (커밋 3483449): mkdir 원자성 락 공유 모듈 (auto_reclaim/force 파라미터화). promote 락부는 시그니처 보존 얇은 래퍼로 위임 — 기존 테스트 20개 무수정 통과
- **invoke_curator.py** (동일 커밋): run/acquire/release/status. 락 위치 {staging}/.curation.lock/, 자동 회수 없음 + --force만(human-in-the-loop), run 성공 시 state=awaiting-merge 유지, 타임아웃/실패 시 락 held 유지(직접 대행 폴백), 완주 판정 staging diff 디스크 실측 + 리포트 파일. 신규 테스트 16개 — 총 36/36 통과
- **§17 v25 + T1 v20** (동일 커밋): Session End 2단계 = invoke_curator.py run 유일 진입점, 3단계 후 release 의무. apply 스크립트 ALL PASS, 글로벌==repo 해시 동일
- **§22 PowerShell 원스트라이크** (커밋 87eeab9, v26): 인라인 함정 1회 위반 → 세션 잔여 .py 전용 전환. 기존 규칙의 강제 장치로 명문화 (별도 커밋)
- **글로벌 배포** (커밋 7cff8a8): install.ps1/sh 배포 목록에 2파일 추가 + m43_deploy_global_scripts.py로 3파일 sha256 검증 ALL PASS + 배포본 status 스모크 테스트 통과

### In Progress
- (없음)

### Blocked
- (없음)

## Key Decisions
- D-43: Curator 호출 코드화 — invoke_curator.py가 유일 진입점 (사용자 승인). 프로젝트 로컬 curation 락(mkdir 원자성, 자동 회수 없음 — human-in-the-loop --force만) + headless 전송(kiro-cli chat --no-interactive) + 완주 판정 디스크 실측 내장. mickey_lock.py로 promote 락과 코드 통합 (락 파일은 스코프별 분리 유지). D-42-1의 use_subagent 전송을 대체하되 in-band 안전 속성은 probe로 동등성 실측 완료. 잔여 리스크: "스크립트 실행" 지시 자체는 여전히 프롬프트 기반 — 다만 실수 표면이 "여러 절차의 올바른 순서"에서 "스크립트 하나 실행"으로 축소

## Files Modified
- MICKEY-43-SESSION.md (신규)
- scripts/m43_probe_headless_transport.py (신규)

## Lessons Learned
- [Protocol] "X가 문제였다"는 기억은 메커니즘 수준으로 재검증해야 한다 — crosstalk의 원인을 "subprocess"로 일반화하면 in-band subprocess까지 오배제. 원인은 항상 구체 메커니즘(전역 저장소 + 폴링 회수)으로 기록·인용할 것
- 셸 응답 표면에서 `[`로 시작하는 출력 라인이 소실됨 (probe에서 재현, 파일 리다이렉트로 교차 확인) — tool-constraints 기록 후보
- [Protocol] §22 위반 실측 2건 (본 세션): `&&` 파서 오류 1회 + python -c one-liner 1회 (agent JSON 확인 시). 위반 후 .py 전용 전환 — 원스트라이크 규약의 필요성을 명문화 당일에 자체 실증
- 기존 테스트가 참조하는 공개 시그니처를 보존하는 얇은 래퍼 위임은 리팩토링 검증 비용을 0으로 만든다 (promote 락 → mickey_lock 이관, 테스트 무수정 20/20)

## Context Window Status
~55% (전 작업 완료 시점)

## Next Steps
- **Curator 실전 1회차** (D-43 검증 조건): 세션 종료 시 invoke_curator.py run 경로로 수행 — 락→headless→diff 실측→리포트 전 과정 첫 실전. 완료 후 release 필수
- T1 v20은 다음 세션 부팅부터 활성 (M23 캐시 제약) — 이번 세션 종료는 본좌가 v20 절차 수동 준수
- M41/M42 인계 잔여: power 트랙 steering 개정 (mickey-power 세션 소관), 글로벌 .bak-m41/m42 백업 정리 (안정 확인 후)
- auto_notes/tool-constraints.md에 `[` 라인 소실 기록 (세션 종료 일괄 확인 시)
