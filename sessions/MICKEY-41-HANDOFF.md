# Mickey 41 Handoff

## Current Status

멀티 세션 격리(옵션 A) 구현·검증 완료: Curator는 프로젝트 로컬만 쓰고(gd- 번들 + adaptive.md), 글로벌 반영은 promote_knowledge.py(락 + Base-Hash + 무결성 롤백)가 전담. Curator 검증 3회차 PASS (글로벌 쓰기 0건, 타 프로젝트 promote 실전 가동도 교차 확인). 문서 3계층 동기화 완료 (CURATOR-PROMPT / agent JSON×2 / §17 v21 / T1 v18 / install).

## Next Steps (Mickey 42)

- **포스트모템 트리거**: 2026-07-24 이후 도달 (내일) — §18 Activity Metrics 실측 + M21 baseline 대조
- **power 트랙 인계**: power-mickey/steering/knowledge-curator.md + session-protocol.md가 구 구조(Curator 직접 수정) 기술 — v21 격리 구조로 개정 필요. D-38-1에 따라 mickey-power 디렉토리 세션에서 수행
- Curator 검증 4회차 (5회 중 3회 완료) — 다음 세션 종료 시
- 글로벌 백업 정리 후보: .bak-ai-developer-mickey-m41 3건 (extended-protocols, CURATOR-PROMPT, PROFILE) — 안정 확인 후 삭제. 타 세션 .m058f5f-bak 4건은 그쪽 소관

## Important Context (SESSION/auto_notes에 없는 것만)

- promote 스크립트는 이미 back-to-basic-modernize 세션이 같은 날 2회 실전 사용 — 격리 체계가 프로젝트 간 즉시 확산됨. 다른 활성 프로젝트의 열린 세션은 구 프롬프트로 부팅된 상태이나, delegate subagent는 launch 시점 로딩이므로 Curator 동작은 어느 세션에서든 신규 격리 구조로 실행됨 (메인 세션 T1만 다음 부팅부터)
- 글로벌 staging dangling: remember-inline-shell-ban.md (unreal-mcp-demo 소유) — ownership상 본 프로젝트 처분 불가, 엔트로피 체크 시 카운트만

## Protocol Feedback

- [Protocol] delegate status 폴링이 validation 오류를 간헐 반복 ("expected map with a single key") — 완료 판정은 디스크 정지 실측(staging mtime + git status)으로 우회 가능. 재발 시 tool-constraints 승격 후보

## Quick Reference

- 세션 메인: `MICKEY-41-SESSION.md` (분석·구현·검증 전 과정)
- 검증 산출물: `scripts/output/m41_*.txt` + `promote-report-20260723-234142.txt` (gitignore 영역)
- 신규 글로벌 entry: `staged-promotion-write-isolation` (신규), `prompt-doc-vs-runtime-loading` (보강)
- Context window: 종료 시점 ~75%. Mickey 42는 fresh context 권장
