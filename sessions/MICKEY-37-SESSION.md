# Mickey 37 Session Log

## Checkpoint [2/5]

## Session Meta
- Type: Self-Improvement (0순위: install seed 시맨틱 + Curator 보정) + Maintenance (1순위: 트랙 A Phase 2)
- Mickey: 37
- Date: 2026-07-15 ~
- Autonomy: Level 2 (Balanced) + batch-confirm-autonomous-proceed 유효

## Session Goal
M36 인계 0순위(repo mickey/ stale 해소 + Curator 프롬프트 보정 3항목) → 1순위(트랙 A Phase 2 cdk/Cloud 카테고리화) 순차 수행

## Purpose Alignment
- Scenario 2 (Mickey 자체 개선) Infrastructure: 진화 루프의 배포 파이프라인(install) 안전화 + Curator 신뢰성 보정 + domain 계층화(§20 Step 3 첫 실행)

## Previous Context

### M36 인계 요약
- 트랙 A Phase 1 완결: Progressive Domain Hierarchy 프로토콜 설치(§20, v18) + 글로벌 domain 정리 (entry 68, dangling 0)
- 확정 파라미터: LINE 200/400, 클러스터 임계값 7, Categorization Rule(판단 지침), Path 컬럼
- Curator 오작동 3종 포착(세션 오귀속 + 보고 누락 + Last Updated 클로버링) → revert 완료. 검증 기간 실패 판정, fs_write 신뢰 카운트 리셋
- M35 지식 그래프 완료 검증 PASS (WELC 101, E2E OK)

### M36 Next Steps (인계)
- 0순위: ① repo `mickey/` stale 해소 (install 시 글로벌 덮어쓰기 위험) ② Curator 프롬프트 보정 3항목
- 1순위: 트랙 A Phase 2 (cdk/Cloud 계열 첫 카테고리화) + anjin staging 2건 고려
- 2순위: 엔트로피 정리 (INDEX Domain Links out-of-sync 3파일, auto_notes, ENVIRONMENT.md)

## Entropy Check (세션 시작 시)
- INDEX 정합성: ⚠️ common_knowledge INDEX Domain Links out-of-sync 3파일 (M36 인계, 2순위)
- auto_notes 최신성: ⚠️ M29(2026-06-26) 이후 무변경 — 정리 후보 지속
- SESSION 아카이빙: ✅ 루트 clean, sessions/ 정리됨
- 구조 문서: ⚠️ ENVIRONMENT.md M18(2026-05-13) 노후 지속
- Curator staging: ✅ 글로벌 비어 있음 (실측). anjin 2건은 anjin 프로젝트 소유 — 본 프로젝트 결정 불가 (ownership)
- repo `mickey/` 미러: ⚠️ stale 확인 (extended-protocols Jul 1 = v17 시점 vs 글로벌 Jul 14 = v18, domain/ Apr 19 vs 글로벌 68 entries) — 0순위 인계 유효
- §19.2 감지 마커: `.kiro/settings/` 존재 (lsp.json 후보 불일치 이슈 M33부터 미해결)
- 포스트모템 트리거: ⏳ 미도달 (2026-07-24 이후)

## Current Tasks
- [x] 0순위-①: repo mickey/ stale 해소 (Option A: install seed 시맨틱) | CC: E2E harness 전항목 PASS + repo extended-protocols hash 일치 → **18/18 PASS**
- [x] 0순위-②: Curator 프롬프트 보정 3항목 | CC: CURATOR-PROMPT.md에 세션 경계/전체 보고/Last Updated 명의 반영 + repo 동기화 → **ALL PASS (3곳 동기화)**
- [ ] 1순위: 트랙 A Phase 2 (cdk/Cloud 카테고리화) | CC: §20 Step 3 절차 완료 + 링크 재검증(dangling 0)

## Progress
### Completed
- 컨텍스트 로딩 (T2 + T3a + T1.5) + 엔트로피 실측
- **0순위-① repo mickey/ stale 해소 (Option A, 사용자 확인)**:
  - diff 실측(`scripts/m37_mickey_mirror_diff.py`): DIFF 10(전부 GLOBAL 최신) / GLOBAL_ONLY 63(copy라 소실 없음) / REPO_ONLY 0. **실위험 = install 시 DIFF 10 롤백**(GRAPH/INDEX/extended-protocols 등)
  - **프레임 충돌 발견**: M36 HANDOFF "repo=배포 미러" vs v10 §8-a 확정(2026-07-04) "repo=seed 골격, ~/.kiro/mickey/=개인 지식 실체, 개인 지식 커밋 금지(예외: extended-protocols.md)". 근본 원인 = install이 seed 원칙 미구현(-Force 무조건 덮어쓰기)
  - install.ps1/.sh seed 시맨틱 수정: 세대 관리 파일(extended-protocols.md + domain/CURATOR-PROMPT.md) 항상 갱신, 나머지 seed는 **대상 미존재 시에만** 복사
  - repo extended-protocols.md ← 글로벌 v18 동기화 (hash 일치 확인)
  - E2E harness `scripts/m37_test_install_seed.py`: 임시 USERPROFILE/HOME 리다이렉트로 실홈 미접촉. **18/18 PASS** (ps1 신규설치/재설치 보호/세대 갱신 + sh Git bash 동일)

- **0순위-② Curator 프롬프트 보정 (사용자 확인)**:
  - 보정 3항목 적용: ① "세션 경계 (Session Boundary)" 섹션 신설 (전달된 SESSION.md 항목만 승격, 0단계 로딩 파일은 상태 파악 용도, 타 프로젝트 파일 접근 금지, 외부 Source staging 불가침) ② 출력 형식에 "전체 변경 목록 (누락 금지)" 필수 섹션 + 미보고=검증 실패 사유 ③ Last Updated 명의 = 호출 세션 강제
  - **중대 발견: 런타임 Curator는 agent JSON 내장 prompt 사용, CURATOR-PROMPT.md 미참조** — md만 수정하면 런타임 미전파. 내장본은 M36 수정(Path 컬럼 등)도 미반영된 구본이었음
  - 대응: `scripts/m37_sync_curator_prompt.py` — md(SoT) → `~/.kiro/agents/knowledge-curator.json` + `examples/knowledge-curator.json` prompt 주입(타 필드 보존) + repo seed md 복사. 검증 ALL PASS (3곳 hash/내용 일치 + 보정 키워드 3종 존재)
  - 백업: 글로벌 `CURATOR-PROMPT.md.m37-bak-20260716` + `~/.kiro/agents/knowledge-curator.json.m37-bak` 유지, repo 쪽 임시 백업은 git 안전망 있어 정리

### InProgress
- 1순위: 트랙 A Phase 2 설계

### Blocked
- (없음)

## Key Decisions
- **D-37-1 (Option A: install seed 시맨틱)**: 미러 전체 동기화(B) 대신 install을 seed 시맨틱으로 수정. 근거: v10 §8-a 확정 방향과 정합 + 덮어쓰기 위험 구조적 영구 제거. B는 개인 지식 68 entries public repo 커밋 + §8-a 정면 충돌로 거부. C(최소 조치)는 근본 원인 미해결로 거부. 사용자 확인 완료.

## Files Modified
- sessions/MICKEY-37-SESSION.md (본 로그)

## Lessons Learned
- **[Protocol] 프롬프트 문서 수정 ≠ 런타임 반영 — 로딩 경로 실측 필수**: CURATOR-PROMPT.md는 SoT 문서일 뿐, 런타임 Curator는 agent JSON 내장 prompt를 사용. M36 수정분(Path 컬럼 등)도 런타임에 미전파 상태였음. 프롬프트/설정류 수정 시 "실제로 무엇이 로딩되는가"를 먼저 실측해야 함 (project-context "3곳 동기화 필수" 교훈의 재발 변형 — Curator에도 md+활성JSON+repoJSON 3곳 존재)
- **install 위험의 실체는 실측으로 재정의됨**: M36 인계는 "GLOBAL_ONLY 63건 소실 위험"을 암시했으나, install은 copy만 하므로 실위험은 DIFF 10건의 stale 롤백이었음. diff 실측(adaptive #2)이 해결 방향(미러링→seed 시맨틱)을 바꿈

## Context Window Status
~20% (추정)

## Next Steps
- (세션 진행 후 기재)

## Last Updated
2026-07-15 (Mickey 37 초입)
