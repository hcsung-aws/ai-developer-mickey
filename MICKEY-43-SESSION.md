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

### In Progress
- 구현 착수 (사용자 승인 완료)

### Blocked
- (없음)

## Key Decisions
- D-43 (예정): Curator 호출 코드화 — invoke_curator.py가 유일 진입점. 프로젝트 로컬 curation 락(mkdir 원자성, 자동 회수 없음 — human-in-the-loop --force만) + headless 전송(kiro-cli chat --no-interactive) + 완주 판정 디스크 실측 내장. mickey_lock.py로 promote 락과 코드 통합 (락 파일은 스코프별 분리 유지). D-42-1의 use_subagent 전송을 대체하되 in-band 안전 속성은 probe로 동등성 실측 완료

## Files Modified
- MICKEY-43-SESSION.md (신규)
- scripts/m43_probe_headless_transport.py (신규)

## Lessons Learned
- [Protocol] "X가 문제였다"는 기억은 메커니즘 수준으로 재검증해야 한다 — crosstalk의 원인을 "subprocess"로 일반화하면 in-band subprocess까지 오배제. 원인은 항상 구체 메커니즘(전역 저장소 + 폴링 회수)으로 기록·인용할 것
- 셸 응답 표면에서 `[`로 시작하는 출력 라인이 소실됨 (probe에서 재현, 파일 리다이렉트로 교차 확인) — tool-constraints 기록 후보

## Context Window Status
~30% (구현 착수 시점)

## Next Steps
- TODO 순서대로: 잔여 커밋 → mickey_lock → invoke_curator → 문서 개정 → PowerShell 규약 → 배포/커밋
- 세션 종료 시 Curator 실전 1회차는 invoke_curator.py 경로로 수행 (D-42-1 검증 조건을 D-43 경로로 승계)
