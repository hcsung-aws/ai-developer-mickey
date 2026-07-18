# Mickey 37 Session Log

## Checkpoint [5/5] (세션 종료 — 카운터 종결)

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
- [x] 1순위: 트랙 A Phase 2 (cdk/Cloud 카테고리화) | CC: §20 Step 3 절차 완료 + 링크 재검증(dangling 0) → **검증 14/14 + 재렌더 dangling 0 + pytest 102 PASS**

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

- **1순위 트랙 A Phase 2 (사용자 확인 2회: 파이프라인 명문화 + Option C 계획)**:
  - **§20 Step 3 카테고리화 파이프라인 고정 명문화** (사용자 지시): ① 트리거 notify → ② 연관 태그 합집합 실측으로 경계 판단 → ③ 구성원 엄선(확실한 것만, 애매한 것 flat 잔류) → ④ 계획 사용자 검증(생략 불가, 자의성 통제) → ⑤ 분할 이동+그래프 구축. 글로벌 extended-protocols v18→**v19** + repo 동기화(hash 일치). 백업 .m37-bak
  - **Option C 실행**: `entries/cloud/` 신설, 18개 이동(AgentCore/인증 4 + Bedrock/boto3 3 + CDK 3 + Terraform 4 + 기타 AWS 4), 제외 5(deploy-output-distrust 횡단 허브, external-param-pre-validation, single-artifact-deployment, node24, packager — flat 잔류). 수술: `m37_phase2_cloud_categorize.py` (dry-run→apply, 백업 내장) — 내부 엣지 19 하위 이관, cross 48 상위 유지, anchor 행 + INDEX Anchors 표
  - 후속 수정 2건 (`m37_phase2_fixup.py`): INDEX Domain Map 경로 18건 cloud/로 갱신(본좌 수술 누락분) + **batch-confirm-autonomous-proceed Path 오기재 정정**(patterns/ 소속인데 M36 일괄 생성 시 entries/로 기재 — 기존 이슈 표면화, `../patterns/`로 정정). "M36 노드 68 = entry 파일 67 + patterns 노드 1"임도 규명
  - **렌더러 보강 (WELC)**: graph_builder에 `entries/**/GRAPH.md` 재귀 병합 추가 + 하위 GRAPH 병합 테스트 신규 1건. baseline 101 → **102 passed**. 글로벌 재렌더: nodes=80, edges=220, **dangling=0** (보강 전 17 UNKNOWN 강등 → 해소)
  - 검증: `m37_phase2_verify.py` **14/14 PASS** (파일 배치/상하위 GRAPH Path 정합/엣지 dangling 0/엣지 총수 212 보존/INDEX 경로 전수 실존)

- **2순위 엔트로피 정리 + git 커밋**:
  - **병렬 세션 발견**: M38(v10 트랙)이 본 세션과 병행 — 트랙-브랜치 분리(D-38-1: master=CLI 트랙, mickey-power 브랜치=Power 트랙) 수행 + 본좌 중간 산출물을 커밋 78f87ab에 선반영. git log 실측으로 파악
  - ENVIRONMENT.md 갱신 (M18→M37): 브랜치 전략, Code Analysis Tools(§19: Serena 감지 + lsp.json 활성), Autonomy Preference, seed 시맨틱 반영
  - common_knowledge INDEX Domain Links out-of-sync 6건 정합 (windows-user-path-extension 3 + kiro-cli-lsp 3 + project-context 1, 중복 제외)
  - auto_notes 검토: curator-diagnosis-references는 Curator 이슈 현재진행형이라 유지, v8 분석 3건 역사 자료로 유지 (변경 없음)
  - 백업 정리: 글로벌 m30/31/32 extended-protocols bak + m36 GRAPH bak 2종 삭제 (검증 완료로 불필요), repo 잔존 bak 3종 삭제. **m37 백업 4종은 유지**
  - 커밋 8391e9c push 완료 (GitDefender dry-run 통과 → push, origin 동기화 확인)

- **세션 정리 (Curator 검증 기간 1회차 = PASS)**:
  - Curator delegate 호출 → delegate status API 불안정(anjin M3/M36과 동일 증상 3회차) → 디스크 실측(스냅샷 diff + 타임스탬프)으로 교차검증
  - **본좌 M37 Curator의 의도 외 변경 0건** — 읽기 도구 차단 상태를 인지하고 직접 수정 영역까지 staging으로 보수적 강등 (보정 프롬프트 작동 확인)
  - GRAPH/INDEX 변경(7/16 21:15)은 **병렬 anjin M4 Curator 소행**으로 판별 — llm-flat-graph-id-schema 승격(사용자 확인 완료, 보정 3항목 준수). 부작용: anjin 프로젝트 레벨 지식 참조 엣지 1건 dangling
  - **결함 조치 A**: Curator agent JSON `allowedTools`에 fs_read/glob/grep 추가 (홈+repo, §17 스펙 준수) — 읽기 차단 근본 해소
  - **결함 조치 B**: anjin 측 미해결 실측 확인(silent-ignore는 anjin 프로젝트 레벨 유지 방침) 후 dangling 엣지 1행 제거 + entry Links에 프로젝트 레벨 주석으로 참조 보존
  - **Pre-staged 4건 전체 머지 (사용자 승인)**: ① installer-seed-semantics 신설 ② prompt-doc-vs-runtime-loading 신설 (각각 GRAPH 노드/엣지 + INDEX 트리거 + 프로젝트 Backlink) ③ tool-and-target-coevolution M37 실증 보강 ④ adaptive.md #11(런타임 로딩 경로 실측), #12(인계 위험 diff 실측 재정의)
  - 최종 검증: 재렌더 nodes 83 / edges 225 / **dangling 0**, staging 청소 완료

### InProgress
- HANDOFF 생성 중

### Blocked
- (없음)

## Key Decisions
- **D-37-1 (Option A: install seed 시맨틱)**: 미러 전체 동기화(B) 대신 install을 seed 시맨틱으로 수정. 근거: v10 §8-a 확정 방향과 정합 + 덮어쓰기 위험 구조적 영구 제거. B는 개인 지식 68 entries public repo 커밋 + §8-a 정면 충돌로 거부. C(최소 조치)는 근본 원인 미해결로 거부. 사용자 확인 완료.
- **D-37-2 (§20 카테고리화 파이프라인 고정)**: 사용자 지시로 "임계값 초과→경계 판단→구성원 엄선→계획 검증(생략 불가)→분할 이동" 5단계를 무조건 따를 파이프라인으로 명문화. 자의적 구성원 판정은 4단계 사용자 검증이 통제 장치. extended-protocols v19.
- **D-37-3 (Phase 2 Option C: cloud 대계열 + 구성원 엄선 18/5)**: cdk만(A)은 응집도 낮음(7개 중 3개 주 도메인 상이) + 재트리거 반복, 전체 23(B)은 횡단 허브/타 도메인 오분류로 거부. "주 도메인이 AWS/Cloud 인프라인가" 기준 18 포함 / 5 flat 잔류. 하위 구조 단층 — cloud/ 내부 재트리거 시 §20 재귀. 사용자 확인 완료.

## Files Modified
### 프로젝트 (repo 추적)
- sessions/MICKEY-37-SESSION.md (본 로그)
- install.ps1, install.sh (seed 시맨틱)
- mickey/extended-protocols.md (v19 동기화), mickey/domain/CURATOR-PROMPT.md (보정 동기화)
- examples/knowledge-curator.json (prompt 재주입)
- scripts/mickey_graph/graph_builder.py (하위 GRAPH 재귀 병합), scripts/tests/test_graph_builder.py (+1 테스트)
- scripts/m37_*.py 7종 (diff/설치테스트/SoT체크/prompt동기화/클러스터실측/카테고리수술/검증/픽스업)

### 글로벌 ~/.kiro/mickey/ (git 미추적, 백업 생성됨)
- extended-protocols.md (§20 파이프라인, v19) — 백업 .m37-bak
- domain/CURATOR-PROMPT.md (보정 3항목) — 백업 .m37-bak-20260716
- domain/GRAPH.md (18행 제거 + anchor + batch-confirm Path 정정) — 백업 .m37-phase2-bak
- domain/INDEX.md (Anchors 표 + 경로 18건) — 백업 .m37-phase2-bak
- domain/entries/cloud/ 신설 (entry 18 + GRAPH.md)
- ~/.kiro/agents/knowledge-curator.json (prompt 재주입) — 백업 .m37-bak

## Lessons Learned
- **[Protocol] 프롬프트 문서 수정 ≠ 런타임 반영 — 로딩 경로 실측 필수**: CURATOR-PROMPT.md는 SoT 문서일 뿐, 런타임 Curator는 agent JSON 내장 prompt를 사용. M36 수정분(Path 컬럼 등)도 런타임에 미전파 상태였음. 프롬프트/설정류 수정 시 "실제로 무엇이 로딩되는가"를 먼저 실측해야 함 (project-context "3곳 동기화 필수" 교훈의 재발 변형 — Curator에도 md+활성JSON+repoJSON 3곳 존재)
- **install 위험의 실체는 실측으로 재정의됨**: M36 인계는 "GLOBAL_ONLY 63건 소실 위험"을 암시했으나, install은 copy만 하므로 실위험은 DIFF 10건의 stale 롤백이었음. diff 실측(adaptive #2)이 해결 방향(미러링→seed 시맨틱)을 바꿈
- **[Protocol] 카테고리화 파이프라인의 검증 단계가 기존 결함을 표면화**: Phase 2 검증(14항목 전수)이 본 수술 누락(INDEX 경로 18건)뿐 아니라 기존 이슈(batch-confirm Path 오기재 — M36 일괄 생성 잔재)까지 발견. verification-tool-as-health-scanner 패턴 재확인
- **구조 변경과 도구는 동시 진화 필요 (tool-and-target-coevolution 실증)**: GRAPH 계층화(대상 변경)가 렌더러 파서(도구)의 암묵 가정(단일 GRAPH.md)을 깨뜨림 — E2E 재렌더에서 17 dangling으로 즉시 검출, 파서 재귀 병합 보강 + 테스트 추가로 동시 갱신
- **[Protocol] delegate status API 불신 → 디스크 실측 대체 경로 확보**: delegate 상태 조회가 반복 실패(3회차 관찰: anjin M3, M36, M37)해도 스냅샷 diff(m37_curator_snapshot.py --pre/--post) + 타임스탬프 실측으로 Curator 결과를 완전 검증 가능. subagent 검증은 도구 응답이 아닌 디스크 증거 기반으로
- **[Protocol] 병렬 세션의 글로벌 자원 동시 수정은 스냅샷 mtime+명의로 분리 판별**: M37 검증 FAIL 4건이 본좌 Curator가 아닌 병렬 anjin M4 승격분으로 판명. pre-스냅샷의 mtime 기록이 결정적 증거. 글로벌 SoT 공유 구조에서 Curator 호출 전 스냅샷을 표준 절차로
- **[Protocol] Curator 보정 프롬프트의 방어적 강등 확인**: 읽기 차단(allowedTools 누락) 예외 상황에서 Curator가 직접 수정을 강행하지 않고 staging 강등 + 사유 명시. M36 오작동(무단 수정)과 정반대의 안전 동작

## Context Window Status
~55% (추정)

## Next Steps
- 2순위 엔트로피 정리 잔존: auto_notes(M29 이후) + ENVIRONMENT.md(M18) 노후 — 다음 세션 후보
- 프로젝트 git 커밋: M37 산출물 미커밋 (v10 트랙 미커밋분과 혼재 주의 — 파일 격리 원칙, 커밋은 사용자 결정)
- 글로벌 백업 파일 누적: m30/31/32/36/37 bak 다수 — 정리 세션 후보
- §8-a 부수 결정(repo mickey/domain/entries 잔재 10건의 seed 예시 라벨링)은 여전히 별도 사이클

## Last Updated
2026-07-15 (Mickey 37 초입)
