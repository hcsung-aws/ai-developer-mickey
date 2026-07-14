# Mickey 36 Handoff

## Current Status

트랙 A Phase 1 완결 — Progressive Domain Hierarchy 프로토콜 설치 + 글로벌 domain 데이터 정리. 확정 파라미터: LINE 200/400, 클러스터 임계값 7, Categorization Rule(제외 목록 없이 판단 지침), Path 컬럼. M35 지식 그래프 완료 검증(WELC 101, E2E OK)도 완료. 세션 종료 Curator 호출에서 **오작동 3종(anjin M3 지식 무단 글로벌 승격 + 보고 누락 + Last Updated 클로버링)**을 검증 기간 프로토콜이 포착 → 사용자 결정으로 revert 완료. 최종 글로벌 domain: entry 68, dangling 0.

## Next Steps (Mickey 37)

### 0순위 — Phase 2 착수 전 필수 선결
- **repo `mickey/` 미러 stale 해소**: repo `mickey/domain/` 8 entries(May14) vs 글로벌 68. 본 세션 글로벌 편집분(§20, Categorization Rule, GRAPH Path, verification-tool entry)이 repo에 미반영. **install 실행 시 stale repo→global 덮어쓰기로 누적 지식 소실 위험**(adaptive #2/#3). v10/install 트랙과 조율하여 repo 동기화 방향 확정 필요.
- **Curator 프롬프트 보정**: M36 오작동 재발 방지. ① 세션 경계 엄수(현재 SESSION.md 범위만) ② 전체 변경 보고 의무 ③ Last Updated 명의=호출 세션. CURATOR-PROMPT.md 주의사항에 추가 검토.

### 1순위 — 트랙 A Phase 2 (실제 첫 카테고리화)
- 임계값 7 트리거 = verification(15, aspect→skip) + cdk(7, 도메인). 첫 재편 = **cdk/Cloud 계열**
- 설계 논점: "cdk만 vs Cloud/AWS/IaC 대계열 통합"(`entries/cloud/{cdk,terraform,agentcore,cognito,...}`). SESSION.md Aspect/Domain 분석 참조
- **anjin `_curator-staging/` 2건**(editor-script-asset-generation, upm-testables-scene-reuse, Unity 계열)이 트랙 A 계획서 확정 대기 중(anjin M3 HANDOFF 명시) — Phase 2에서 함께 처리 고려

### 2순위 — 엔트로피 정리
- 프로젝트 common_knowledge INDEX Domain Links out-of-sync 3파일(windows-user-path-extension, kiro-cli-lsp-init-settings-location, project-context) + auto_notes(M29 이후) + ENVIRONMENT.md(M18)

## Important Context (SESSION/auto_notes에 없는 것만)

- **글로벌 편집 vs repo 미러 divergence**: extended-protocols.md 글로벌 Version 17→18(§20 추가). repo mickey/ 및 T1 agent JSON은 v17 — 차기 reconciliation 대상. 글로벌이 SoT(live 동작), repo는 배포 미러.
- **Curator 오작동 사건 전문**: MICKEY-36-SESSION.md "Curator 오작동 사건" 섹션. 검증 기간 이번 회차 실패 판정 → fs_write 자동 승인 신뢰 카운트 리셋. anjin M3 HANDOFF도 독립적으로 "Curator delegate 에러 응답 vs 실제 완료 불일치" 관찰 — Curator 신뢰성 이슈가 교차 프로젝트로 확인됨.
- **글로벌 백업 파일**: `~/.kiro/mickey/domain/GRAPH.md.m36-bak-20260714-134517`(정리 전), `GRAPH.md.m36-revert-bak-20260715-021451`(revert 전). 정리되면 삭제 가능.
- **프로젝트 git 미커밋**: M36 산출물(sessions/MICKEY-36-*, scripts/m36_*.py) 미커밋. 병렬 v10 트랙 파일과 격리 유지. 커밋/push는 사용자 결정.

## Protocol Feedback

- [Protocol-] **Curator 세션 경계·보고·명의 오작동** — subagent가 다른 프로젝트 지식을 현재 세션 명의로 무단 승격 + 미보고 + Last Updated 클로버링. 검증 기간 git diff+실측(타임스탬프/노드수)이 포착. Curator 프롬프트 3항목 보정 필요.
- [Protocol+] **검증 기간 프로토콜 실효성 입증** — "첫 5회 git diff 자동 보고 + 실측 교차검증"이 실제 의도 외 변경을 잡아냄. deploy-output-distrust(도구 출력 불신)가 subagent 결과에도 적용됨을 실증.
- [Protocol+] **aspect 제외 목록 대신 판단 지침** — Step 3이 이미 사용자 확인 필수 → 트리거는 notify, 판단은 확인 시점. 정적 목록의 유지부채(adaptive #6) 회피.

## Quick Reference

- 세션 메인: `sessions/MICKEY-36-SESSION.md` (Checkpoint 5/5, 트랙 A Phase 1 + Curator 사건 + Aspect/Domain 분석)
- 스크립트: `scripts/m36_tag_cluster_count.py`(클러스터 집계), `m36_graph_cleanup.py`(병합+Path), `m36_revert_anjin.py`(anjin revert) — 모두 백업+dry-run 내장, 재사용 가능
- 글로벌 편집: `~/.kiro/mickey/extended-protocols.md`(§20, v18), `domain/{GRAPH.md, INDEX.md, CURATOR-PROMPT.md}`
- Context window: 세션 종료 시점 ~60%. Mickey 37은 fresh context 권장
