# Mickey 42 Session

## Checkpoint
[2/5]

## Session Meta
- Type: Self-Improvement (멀티 세션 Curator 결과 crosstalk 버그 조사)
- Date: 2026-08-19
- Track: CLI (master 브랜치. power 작업은 mickey-power 디렉토리 소관 — D-38-1)

## Session Goal
멀티 세션 환경에서 Curator delegate 결과가 호출 세션이 아닌 타 세션에 출력되는 버그의 원인 규명 (+ 해결)

## Purpose Alignment
Infrastructure (자기 개선) — 진화 루프의 Curator 호출 경로(세션 종료 프로토콜) 신뢰성 확보. M41 격리(쓰기 측)의 후속 — 이번엔 전송(transport) 측

## Previous Context (M41 HANDOFF 요약)
- M41: 멀티 세션 격리(옵션 A) 구현·검증 완료 — Curator 로컬 staging + promote_knowledge.py(락+Base-Hash+롤백). Curator 검증 3회차 PASS
- 인계: ① 포스트모템 트리거 도달 (07-24 이후 → 오늘 08-19) ② power 트랙 steering 개정 (mickey-power 세션 소관) ③ Curator 검증 4회차 (세션 종료 시) ④ 글로벌 .bak-ai-developer-mickey-m41 3건 정리 후보

## Entropy Check (진입 시 실측, 2026-08-19)
- git clean, M41 커밋 2건(de70ab2, a0fa90f) 확인. 프로젝트 staging 비어 있음
- 글로벌 staging dangling 1건: remember-inline-shell-ban.md (unreal-mcp-demo 소유 — skip, 카운트만)
- 글로벌 백업: .bak-ai-developer-mickey-m41 3건 (본 프로젝트 인계 — 안정 확인 후 삭제 후보) + 타 프로젝트 2건 (anjin m9, epic-lore m17 — 그쪽 소관)
- **extended-protocols.md drift**: 글로벌 v23 (2026-08-08, 타 프로젝트가 §22/§23 추가) vs repo mickey/ 미러 v21 (07-23) — repo 동기화 필요 (adaptive #3, 방향: global→repo)
- **포스트모템 트리거 도달**: 07-24 조건 경과 26일 — §18 Activity Metrics 실측 + M21 baseline 대조 필요
- GRAPH/INDEX Last Updated 2026-08-19 (anjin promote 경유 — 격리 구조 정상 가동 중)

## Current Tasks
- [x] delegate 결과 crosstalk 원인 규명 | CC: 상태 저장 위치 + 라우팅 메커니즘을 디스크 실측/공식 문서로 확정, 추측 아닌 증거 기반 보고
- [x] use_subagent 병렬 안전성 검증 | CC: probe 실측 + 전역 상태 전후 비교 + 외부 이슈 트래커 확인
- [x] 옵션 A 구현 (delegate→use_subagent 전환) | CC: 적용 스크립트 2건 exit 0 + 검증 ALL PASS + 4개 파일 동기화

## Progress
### Completed
- **crosstalk 원인 규명 (실측 + 공식 문서 교차 확인)**:
  - 상태 저장 실체 발견: `C:\Users\hcsung\AppData\Local\kiro-cli\.subagents\` — **머신 전역 단일 디렉토리** (프로젝트별/세션별 격리 없음). M40 당시 "lock 실체 미확인"이었던 것을 이번에 확정
  - 공식 문서 확인: delegate storage는 "application data directory". 세션/프로젝트 스코프 개념 자체가 없음
  - 상태 파일 구조: agent 이름 키 + 세션 식별자 부재 + `user_notified` 선점 플래그 — **먼저 status 조회한 세션이 결과를 가로챔**. launch 시 타 세션 작업 replace도 문서 명시 동작
  - 결론: 버그가 아니라 delegate 설계 자체가 session-agnostic. 우리 프로토콜의 "호출 세션에 결과가 돌아온다" 가정과 충돌
- **use_subagent 병렬 안전성 검증 (D-42-1 근거)**:
  - probe 실측: 결과 in-band 반환 (마커 PROBE-M42-TRANSPORT-OK 왕복) + 전역 .subagents 전후 무변화 + 실행 아티팩트 UUID 키 (cli-checkouts/run-receipts) — crosstalk 구조적 불가
  - 잔여 단서 (완주 계열, 라우팅 아님): Kiro #6765 응답 채널 60~95초 절단, #6163 MCP 조합 무한 대기 (기존 domain entry 보유) — 폴백(직접 대행)으로 수용
  - 같은 프로젝트 동시 큐레이션은 staging/adaptive.md 공유로 여전히 회피 대상 (§17 v24에 명기)
- **옵션 A 구현 (전 검증 ALL PASS)**:
  - 선행: 글로벌 extended-protocols v23 → repo 미러 동기화 (drift 해소, hash match) + 백업 .bak-ai-developer-mickey-m42
  - m42_apply_protocols_v24.py: §17 "Curator 호출 전송 규약 (M42)" 소절 신설 + 다이어그램 개정 + v24 푸터 — 글로벌+repo, RESULT: ALL PASS
  - m42_apply_t1_v19.py: Session End 2단계 delegate→use_subagent + 완주 디스크 실측 + Changes 갱신 — 활성 JSON+repo JSON, RESULT: ALL PASS
  - auto_notes/tool-constraints.md: M42 실측 2건 기록 (crosstalk 실체, Format-Table 출력 소실) + NOTES.md 갱신

### In Progress
- (없음)

### Blocked
- (없음)

### Blocked
- (없음)

## Key Decisions
- D-42-1: Curator 호출 전송을 delegate → use_subagent(동기)로 전환 (사용자 승인). 근거: ① delegate는 전역 상태(agent 이름 키 + user_notified 선점)로 crosstalk/replace 구조적 발생 ② use_subagent는 in-band 반환 + UUID 키로 랑데부 저장소 부재 (probe 실측) ③ M41 쓰기 격리로 delegate lock의 직렬화 이점 불필요. 조건부: Kiro #6765(60~95초 채널 절단) 대비 실전 1회차 완주 검증 + 완주 판정은 staging 디스크 실측

## Files Modified
- MICKEY-42-SESSION.md (신규)
- ~/.kiro/mickey/extended-protocols.md + mickey/extended-protocols.md (v23 동기화 → v24 적용)
- ~/.kiro/agents/ai-developer-mickey.json + examples/ai-developer-mickey.json (T1 v19)
- scripts/m42_apply_protocols_v24.py, scripts/m42_apply_t1_v19.py (신규)
- auto_notes/tool-constraints.md, auto_notes/NOTES.md
- 글로벌 백업: extended-protocols.md/agents JSON에 .bak-ai-developer-mickey-m42 생성

## Lessons Learned
- [Protocol] delegate crosstalk의 근본은 "도구가 세션을 인지한다"는 무근거 가정 — 도구의 상태 저장 위치·키 구조·수신 경로를 실측하면 멀티 세션 안전성을 사전 판정 가능 (M40 lock 관찰 때 저장소 실체까지 파고들었으면 1세션 먼저 발견했을 것)
- Format-Table 파이프가 항목 존재(count 2)에도 빈 출력 — empty-scan-distrust 재현. 첫 스캔 빈 결과는 카운트 교차 확인 후 문자열 직접 조립으로 재조회 (tool-constraints 기록)

## Context Window Status
~45% (구현 완료 시점)

## Next Steps
- **Curator 실전 1회차 완주 검증** (D-42-1 조건): 이번 세션 종료 시 use_subagent 경로로 실행, staging 파일 디스크 실측으로 완주 판정. #6765 절단 발생 시 직접 대행 폴백 + 기록
- T1 v19은 다음 세션 부팅부터 활성 (M23 메인 agent 캐시 제약) — 이번 세션 종료는 본좌가 v19 절차를 수동 준수
- M41 인계 잔여: 포스트모템 (§18 실측), power 트랙 steering 개정 (mickey-power 세션 소관 — session-protocol.md delegate 참조 1건 포함), 글로벌 .bak-m41 3건 정리
