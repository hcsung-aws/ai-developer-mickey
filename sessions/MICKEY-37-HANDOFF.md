# Mickey 37 Handoff

## Current Status

M36 인계 0/1/2순위 전체 완결 + 세션 정리 완료. ① install seed 시맨틱(D-37-1, E2E 18/18) ② Curator 프롬프트 보정 3항목 + **런타임은 agent JSON 내장 prompt 사용 발견** → md(SoT)→JSON 동기화 확립 + allowedTools 읽기 3종 추가 ③ 트랙 A Phase 2: `entries/cloud/` 카테고리 신설(18 이동, §20 파이프라인 v19 명문화, 검증 14/14) + 렌더러 하위 GRAPH 재귀 병합(102 tests) ④ 엔트로피(ENVIRONMENT/INDEX/백업) + 커밋 push. Curator 검증 기간 **1회차 PASS**(의도 외 변경 0) + Pre-staged 4건 전체 머지. 최종 글로벌: nodes 83 / edges 225 / dangling 0.

## Next Steps (Mickey 39 — CLI 트랙)

- **Curator 검증 기간 2회차 계속**: 다음 호출 시 스냅샷(--pre/--post) + git diff 보고. 이번에 읽기 도구가 열렸으므로(allowedTools) 직접 수정 동작이 처음 발현될 것 — 세션 경계/전체 보고/명의 3항목 준수 확인
- **트랙 A Phase 2 후속 관찰**: cloud/ 내부 클러스터가 임계값 7 재도달 시 §20 재귀 (당장 아님). Curator가 "기존 카테고리 매칭 시 그 안으로" 규칙을 실제 따르는지 다음 cloud 계열 승격 때 확인
- 포스트모템 트리거: 2026-07-24 이후 (M21 baseline + 5주)
- 잔여 소소: anjin `_curator-staging/` 2건은 anjin 소유(ownership) — 본 프로젝트 관여 불가. §8-a 잔재(repo mickey/domain/entries 10건 seed 예시 라벨링)는 별도 사이클

## Important Context (SESSION/auto_notes에 없는 것만)

- **트랙-브랜치 분리 후 첫 세션**: master=CLI 트랙 전용, power 작업은 `mickey-power` 브랜치/디렉토리 (D-38-1, M38 수행). 이 디렉토리에서 power-mickey/ 파일 수정 금지
- **글로벌 SoT 병렬 수정 주의**: anjin 등 타 프로젝트 Curator가 글로벌 GRAPH/INDEX를 동시 수정함 (이번에 anjin M4 승격 + dangling 부작용 1건 → 제거 조치). Curator 호출 전 `scripts/m37_curator_snapshot.py --pre` 스냅샷이 변경 주체 판별의 유일한 증거
- **delegate status API 3회차 불안정**: 상태 조회 실패해도 Curator는 정상 완료일 수 있음 — 디스크 실측(staging 목록, mtime)으로 판정
- **글로벌 백업 잔존**: m37 계열 백업 6종(extended-protocols, CURATOR-PROMPT, GRAPH×3, INDEX×2, coevolution) — 다음 세션 안정 확인 후 정리 가능

## Protocol Feedback

- [Protocol+] **검증 기간 + 스냅샷 교차검증이 병렬 세션 간섭을 정확 분리** — 검증 FAIL 4건을 "본 Curator 오작동"으로 오판하지 않고 anjin M4 소행으로 판별. mtime 스냅샷이 결정적
- [Protocol+] **보정 프롬프트의 방어적 강등** — 읽기 차단 시 Curator가 직접 수정 강행 대신 staging 강등 + 사유 명시 (M36 무단 수정과 정반대)
- [Protocol-] **Curator agent JSON allowedTools 누락이 4세션+ 잠복** — §17 스펙("읽기 전체 자동")과 실제 설정 불일치. 스펙 문서와 실행 설정의 정합 검증 절차 부재였음 (prompt-doc-vs-runtime-loading과 동족 이슈)

## Quick Reference

- 세션 메인: `sessions/MICKEY-37-SESSION.md` (Checkpoint 5/5)
- 핵심 스크립트: `m37_curator_snapshot.py`(Curator 전후 검증), `m37_sync_curator_prompt.py`(프롬프트 3곳 동기화), `m37_phase2_verify.py`(GRAPH 정합), `m37_test_install_seed.py`(install E2E)
- 글로벌 신설: `domain/entries/cloud/`(18+GRAPH), `entries/installer-seed-semantics.md`, `entries/prompt-doc-vs-runtime-loading.md`
- Context window: 종료 시점 ~70%. Mickey 39는 fresh context 권장
