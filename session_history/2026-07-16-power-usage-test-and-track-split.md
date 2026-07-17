# 2026-07-16 — v10 Power 실사용 테스트 + 트랙 분리

> **트랙**: v10 Power (M10). 당초 CLI 트랙 Mickey 38로 오귀속되어 `sessions/MICKEY-38-SESSION.md`로 기록·커밋(`78f87ab`)됨 → 본 파일로 이관, **번호 38은 CLI 트랙에 반환** (다음 CLI 세션 = Mickey 38).

## 세션 목표

설치 완료된 power-mickey(v10)의 실사용 테스트 + 2트랙 동거 혼선 해소(트랙-브랜치 분리).

## 실사용 테스트 결과 (acp-client)

- activate → steering 상시 6종 readSteering pull → T1.5 인덱스 로딩 → Continuing Session 프로토콜 수행 — 전부 정상
- MCP 직접 마운트 실호출: `list_regions` → 37 리전 정상 반환
- 정적 검증: verify_power_structure 7/7, verify_hooks 6/6, verify_serving_sync IN-SYNC(9파일), verify_mickey_home PASS
- 알려진 제약 재확인: SessionStart hook 은 acp-client 미발화 (V6) — 터미널 `--agent-engine v3` 전용

## 트랙 분리 실행 (사용자 결정)

- **결정 (구 D-38-1 표기)**: master = v2 CLI agent mickey 트랙 / 신규 `mickey-power` 브랜치 = power 작업(M10) 전용, 별도 clone. v3 정식 출시 시 완전 통합. 양 트랙은 글로벌 `~/.kiro/mickey/`(SoT) 공유 — 분리로 인한 지식 이슈 없음이 정상. bak 파일 gitignore 보류.
- 커밋 A `66a72d3`: v10 Power Migration 산출물 44파일 (master)
- 커밋 B `78f87ab`: CLI 트랙 산출물 19파일 (master) — MICKEY-37/38 세션 로그 포함
- push + `mickey-power` 브랜치 생성·push → `c:\Users\hcsung\work\kiro\mickey-power` fresh clone
- `.kiro/hooks`+`.kiro/scripts` gitignore 누락 → `scripts/m38_copy_kiro_workspace.py`로 수동 이식 (정식 해결 = gitignore 부분 해제 검토, mickey-power 인계)
- clone 검증 3종 전부 PASS
- kickoff 문서 작성·push: `session_history/2026-07-16-mickey-power-kickoff.md` (mickey-power `9f5ea8e`)

## Lessons Learned

- **[Protocol] 세션 진입 시 첫 read 도 stale 일 수 있음** — MICKEY-37-SESSION.md 첫 read가 "빈 세션" 냉동본 반환 → 사용자 지적 후 재독+디스크 실측으로 정정. adaptive #9가 "현 세션의 첫 read"에도 적용됨. 인계 판단 전 산출물 디스크 실측을 기본 절차로.
- **[Protocol] 2트랙 동거 디렉토리의 인계 혼선** — CLI 트랙(MICKEY-N)과 v10 트랙(session_history/)이 동거하면 Continuing Session이 어느 인계를 따를지 모호. 세션 초입 CLI 트랙 오판 → 사용자 정정. 브랜치+디렉토리 분리로 구조적 해소.
- **[Protocol] 세션 정체성 오귀속** — 트랙 정정을 받고도 CLI 번호 체계(M38)를 계속 사용, 사용자 재정정으로 본 파일 이관. 트랙 정정 시 세션 로그의 기록 규약(번호 vs 날짜)까지 함께 전환해야 함.

## Next Steps

- **(mickey-power 디렉토리/브랜치)**: kickoff 문서 따라 진행 — gitignore 부분 해제 검토, IDE 묶음 실측, registry stale path, changelog 백필, entries 잔재. **세션 정리(Curator 포함)도 그쪽에서 수행.**
- **(이 디렉토리/master)**: CLI 트랙 잔여 — Curator 프롬프트 보정 3항목(M37 0순위-②), 트랙 A Phase 2, 엔트로피 정리. 다음 CLI 세션 = Mickey 38.

## Last Updated
2026-07-16
