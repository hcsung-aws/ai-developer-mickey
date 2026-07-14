# Mickey 36 Session Log

## Checkpoint [5/5]

> 0순위(M35 커밋/push 이미 완료 확인 + v10 트랙 v3 위임) → 지식 그래프 완료 검증(WELC 101, E2E OK) → 트랙 A Phase 1 완료(프로토콜 설치 + 데이터 정리 + 검증). Phase 2(실제 카테고리화)는 다음 세션. 병렬 v10 트랙과 파일 격리 유지.

## Session Meta
- Type: Maintenance (M35 지식 그래프 작업 완료 검증)
- Mickey: 36
- Date: 2026-07-13 ~
- Autonomy: Level 2 (Balanced) + batch-confirm-autonomous-proceed 유효

## Session Goal
M35에서 완결한 지식 그래프 시각화(D 트랙) 작업이 온전히 완료되었는지 실측 검증. (v10 트랙 커밋·배포는 v3 트랙 소관으로 본 세션 범위 제외 — 사용자 지시)

## Purpose Alignment
- Scenario 2 (Mickey 자체 개선) Infrastructure: 진화 루프 진단 도구(그래프 시각화)의 완료 상태를 검증하여 다음 세션이 신뢰하고 활용할 수 있도록 정합성 보증.

## Previous Context

### M35 인계 요약
- 그래프 시각화 D 트랙 완결 (Phase 3 UI: 태그 chip + kind/edge 필터 + 이웃 1-hop 강조). WELC 101 tests passed. renderer.py 무변경.
- CLI 트랙 M31~M35 5개 세션 분리 커밋 완결 (커밋 a549daa 가 M35).
- Curator 4세션 우회 후 첫 정식 응답. `data-view-preseeding-immutability` 글로벌 domain entry 승격 + adaptive.md #9 추가.

### git 실측 (M36 진입, 2026-07-13)
- 최신 커밋: **a549daa (M35)** — master. M31~M35 모두 커밋 완료.
- 작업트리 미커밋 = **전부 병렬 v10 트랙 파일** (power-mickey/steering/** 재구성, install.{ps1,sh}, deploy_power.py, verify_*.py, mickey/README.md, PROJECT-OVERVIEW/FILE-STRUCTURE 수정분, session_history/, IMPROVEMENT-PLAN-v10/progressive-domain-hierarchy)
- master 직접 push 여부 미확정 → 사용자 결정 대기 (0순위)

## Entropy Check (세션 시작 시)
- INDEX 정합성: ✅ common_knowledge + context_rule 양쪽 M35 갱신 유효
- auto_notes 최신성: ⚠️ M29(2026-06-26) 이후 무변경 17일+ — 정리 세션 후보
- SESSION 아카이빙: ✅ 프로젝트 루트 clean (M36 신규 생성만)
- 구조 문서: PROJECT-OVERVIEW ✅ 2026-07-13 갱신됨(v10 트랙) / ENVIRONMENT ⚠️ M18(2026-05-13) 노후 지속
- §19.2 감지 마커: ⚠️ lsp.json 후보 불일치 (M33부터 미해결, 4순위)
- Curator staging: ✅ 프로젝트/글로벌 모두 비어 있음
- 병렬 v10 트랙: 작업트리에 대량 미커밋 — v3 트랙이 별도 관리 (본 CLI 트랙과 파일 격리 원칙)
- 포스트모템 트리거: ⏳ 미도달 (2026-06-19 baseline + 5주 = 2026-07-24 이후)

## Current Tasks
- [x] 0순위: M35 커밋/push 상태 실측 → 이미 커밋+push 완료 (a549daa = origin/master, 0 ahead/behind)
- [x] 0순위: 병렬 v10 트랙 상황 확인 → Phase 5 (가) 코드·harness 완료, 실제 배포·커밋은 v3 트랙 소관(사용자 지시로 본 세션 제외)
- [x] 지식 그래프 작업 완료 검증 (아래 Progress 참조)

## Progress
### Completed
- 컨텍스트 로딩 + git 실측 + 엔트로피 체크
- **0순위 결론**: M35(a549daa)는 커밋+push 모두 완료. HANDOFF "push 미실행" 기록은 냉동본이었음(adaptive #9 재확인). v10 트랙은 v3 소관으로 미개입.
- **지식 그래프 작업 완료 검증 (전항목 PASS)**:
  1. 구조 온전: `scripts/mickey_graph/{models,parser,graph_builder,renderer}.py` + templates/graph.html.tmpl + vendor + tests 모두 존재
  2. WELC 테스트: **101 passed in 0.95s** (M35 기록 재현)
  3. git 추적: 소스·테스트·템플릿 19개 파일 모두 커밋됨. vendor/ + output/ 은 .gitignore 의도적 제외(M34 결정, setup_vendor.py 재생성)
  4. E2E 렌더: `--scope project` 정상 (exit 0, 92 nodes/227 edges, 806KB HTML 생성)

### 검증 중 표면화된 지식베이스 엔트로피 (도구 버그 아님 — 진단 기능이 정상 작동한 결과)
- domain INDEX 중복 노드 3건: powershell-curl-escape, packager-vs-monorepo-hoisting, decision-implementation-supersede-pattern (INDEX에 동일 entry 2행)
- dangling reference 1건: `external-source-digest-separation` (본문 참조하나 entry 파일 부재 → UNKNOWN 승격)
- INDEX Domain Links out-of-sync 3파일: windows-user-path-extension.md / kiro-cli-lsp-init-settings-location.md / project-context.md 의 body ref가 INDEX에 누락
- → 2순위 엔트로피 정리 세션 후보 (INDEX/domain 수정은 사용자 확인 필요, 본 세션 범위 밖)

### InProgress
- (없음 — 검증 완료)

### Blocked
- (없음)

## Key Decisions
- **D-36-1**: 이번 세션 범위 = M35 지식 그래프 작업 완료 검증만. v10 트랙 커밋·배포는 v3 트랙에 위임(사용자 명시 지시). 근거: 병렬 트랙 파일 격리 원칙(adaptive #4) + 사용자가 v3 소관임을 명확히 함.
- **D-36-2 (트랙 A Phase 1 파라미터 확정)**: LINE 상한 200/400, 클러스터 임계값 **7**, Categorization Rule (a) 지금 명시, Path 컬럼 시작 시 일괄(α). Alternative(임계값 3): 거부 — 실측상 66 고유 노드에서 임계값 3은 24개 클러스터 초과 → 즉시 빅뱅 재편. 임계값 7은 2개(verification, cdk)만 트리거 → "1~2개 먼저" 의도 부합.
- **D-36-3 (aspect 태그 제외 목록 폐기)**: 제외 목록 하드코딩 대신 "판단 지침 한 줄"로 대체. 근거: ①유지보수 부채(adaptive #6 안티패턴) ②aspect/domain 이분법이 미래 유효 도메인 억압 위험 ③Step 3은 이미 "사용자 확인 필수"이므로 트리거는 notify만 하면 되고 판단은 확인 시점에 두는 것이 옳음. 오검출 비용 = 사용자 "skip" 한마디로 저렴.

## Aspect/Domain 태그 분류 분석 (Task 0, Phase 2 재편 설계 근거)

> 근거 데이터: `scripts/m36_tag_cluster_count.py` 실행 결과 (66 고유 노드, 393 고유 태그). 중복 ID 병합 후 집계.

**핵심 통찰**: 태그 빈도 1위 `verification`(14)는 순수 횡단 관점(모든 도메인의 검증 성격). 최대 응집 도메인은 `cdk`(7). 임계값 7에서 {verification, cdk} 트리거 → verification skip(관점) + cdk 카테고리화(도메인) = 가장 깨끗한 검증 케이스.

### 응집 도메인 (카테고리 후보 — entries/{category}/ 적합)
- **Cloud/AWS/IaC 계열** (최대·최응집, Phase 2 첫 후보): cdk(7) · aws(6) · cognito(4) · infrastructure(4) · terraform(4) · agentcore(3) · boto3(3) · deployment(3) + bedrock(2) · iam(2) · lambda(2) · botocore(2) · serverless(2) · provisioning(2) · cdk-nag(2) · ci-cd(2)
- **MCP 계열**: mcp(6)
- **Mickey 메타/에이전트 계열**: agent-design(6) · self-improvement(4) · knowledge-management(2) · tool-precision(2)
- **JS/Node 빌드 계열**: monorepo(3) · esm(2) · node(2) · node22(2) · typescript(2) · lockfile(2)
- **약한 도메인(언어/플랫폼)**: python(3) · powershell(2) · windows(2) · regex(2)

### 횡단 관점 aspect (카테고리 부적합 — 여러 도메인 관통, Step 3 시 skip 판단)
verification(14) · architecture(5) · testing(5) · distrust(4) · trap(4) · evaluation-loop(4) · measurement(3) · planning(3) · debugging(3) · json(3) + validation·refactoring·simplicity·resilience·incremental·completion-criteria·acceptance-criteria·automation·side-effect·false-positive·workaround·external-verification·cross-check·quantitative·retry·config·sensitive·output·quoting·shell-escape·unit-test·dependency-isolation·pipeline·protocol·protocol-design·documentation·retrieval·breaking-change (각 2~3)

### 경계(borderline — 확인 시 문맥 판단)
- security(3): 보안 도메인 vs 보안 관점
- llm(2): LLM 도메인 vs LLM 관점
- jwt(2)·oauth(2)·token-validation(2): 인증(auth) 계열 — 소규모 도메인 후보이나 임계값 미달

### Phase 2 함의
- 임계값 7 첫 재편 = cdk. 다만 cdk는 Cloud/AWS/IaC 대계열의 일부 → Phase 2 설계 시 "cdk만 vs cloud 대계열 통합" 판단 필요 (계층 `entries/cloud/{cdk,terraform,...}` 가능성)
- aspect 태그는 카테고리가 아니라 GRAPH의 "관점 인덱스"로 별도 활용 여지 (Phase 2 이후 검토)

## Files Modified
### 프로젝트 (repo 추적)
- `sessions/MICKEY-36-SESSION.md` (본 로그)
- `scripts/m36_tag_cluster_count.py` (태그 클러스터 집계 — 임계값 결정 근거)
- `scripts/m36_graph_cleanup.py` (GRAPH 병합+orphan+Path, 백업 내장, dry-run 기본)
- `scripts/output/*.html` (E2E 검증 렌더 재생성 — gitignore 대상)

### 글로벌 ~/.kiro/mickey/ (git 미추적, repo 미러 stale — 위 "미결" 참조)
- `extended-protocols.md` (§3 엔트로피 #6/#7, §20 신설, v17→18)
- `domain/CURATOR-PROMPT.md` (Path 컬럼+§20 연동, Category 필드, 100줄 문구 대체)
- `domain/INDEX.md` (Categorization Rule §, Anchors §, orphan 트리거, Last Updated)
- `domain/GRAPH.md` (중복 3 병합, orphan 등록, Path 컬럼 66행)
- `domain/GRAPH.md.m36-bak-20260714-134517` (백업)

## Lessons Learned
- **그래프 시각화 도구가 진단 도구로서 이중 기능 확인** — 완료 검증 목적의 E2E 렌더가 지식베이스 엔트로피(INDEX 중복 3 + dangling 1)를 부수적으로 표면화. 도구 실행 자체가 knowledge health 스캔.
- **[Protocol] adaptive #9 재확인** — M35 HANDOFF "push 미실행"이 실제 원격(push 완료)과 불일치. git fetch 실측이 냉동 기록 정정.
- **dangling 원인 = graduated 미반영** — external-source-digest-separation는 patterns/INDEX.md에서 domain/entries/로 graduated 되었으나 "GRAPH 갱신 다음 Curator 호출 시 반영 예정"으로 미뤄진 채 노드 미등록. 파일 존재≠노드 등록. 빌더 로직(parse_graduated_absorption_edges) 확인으로 근본 원인 규명 (추측 금지).
- **임계값은 실측 후 결정** — "1~2개 먼저" 의도를 태그 빈도 실측(m36_tag_cluster_count.py) 없이 감으로 정했으면 오판. verification(14)=최대이나 aspect. 최대 도메인 cdk(7)=임계값 7의 근거.
- **[Protocol] aspect 제외 목록 대신 판단 지침** — 사용자 "제외 조항 문제 없나" 질문이 핵심. Step 3이 이미 사용자 확인 필수 → 트리거는 notify만, 판단은 확인 시점에. 정적 제외 목록은 유지부채(adaptive #6)+미래 도메인 억압 위험. 오검출 비용=사용자 skip 한마디로 저렴.
- **[Protocol] 글로벌 편집은 백업 필수** — ~/.kiro/mickey/ 는 git 미추적. GRAPH.md 수술 전 m36-bak 백업 생성. 되돌림 안전장치 확보. (Curator가 adaptive #10으로 규칙화)

## ⚠️ Curator 오작동 사건 (M36 검증 기간 — 중대)

세션 종료 Curator 호출에서 **의도 외 변경 3종을 검증 기간(첫 5회 git diff 보고) 프로토콜이 포착**:
1. **세션 오귀속 + 스코프 오판**: M36 Curator가 anjin-llm-scenario-poc M3의 프로젝트 레벨 지식 2건(silent-ignore-static-prevalidation, llm-temperature-determinism)을 글로벌 domain에 무단 생성. anjin M3 HANDOFF 확인 결과 anjin은 이를 D-011/R-009 프로젝트 레벨로 유지(글로벌 승격 의도 없음).
2. **보고 누락**: 위 2건을 Curator 출력에 보고하지 않음 (verification-tool 1건만 보고). GRAPH 노드 +3/엣지 +12 vs 보고 +1/+3 불일치로 발각.
3. **Last Updated 클로버링**: domain/GRAPH.md + INDEX.md 의 Last Updated 를 anjin M3 Curator 명의로 덮어씀 (M36 갱신 소실).

**대응 (사용자 결정 B)**: anjin 2건 노드·엣지·entry파일·INDEX트리거 revert (scripts/m36_revert_anjin.py, 백업 GRAPH.md.m36-revert-bak-20260715-021451). 지식 소실 없음 — anjin 원본(SESSION/DECISIONS/코드) 온전, anjin이 프로젝트 레벨로 보유. Last Updated 2곳 M36 명의 복원. 검증: 재렌더 entry 68 dangling=0.

**유지된 정상 M36 산출물**: verification-tool-as-health-scanner entry+노드+트리거+Domain Backlink, quantitative-usage-measurement 보강, adaptive.md #10.

**[Protocol] 검증 기간 판정**: 이번 회차 **실패** (의도 외 변경 발견). fs_write 자동 승인 신뢰 정착 카운트 리셋. Curator 프롬프트 보정 필요: ① 세션 경계 엄수(현재 세션 SESSION.md 범위만) ② 전체 변경 보고 의무 ③ Last Updated 명의 = 호출 세션. → 포스트모템/차기 세션 Curator 개선 대상.
- **[Protocol] Curator 출력 불신 → 실측 교차검증** — Curator "직접 수정 완료" 보고를 그대로 믿지 않고 git diff + entries 타임스탬프 + 재렌더 노드수로 실측 → 미보고 변경 발각. deploy-output-distrust 원칙이 subagent 결과에도 적용. anjin M3 HANDOFF도 동일 사건("Curator delegate 에러 응답 vs 실제 완료 불일치") 독립 관찰.

## 미결/인계 (repo 동기화 — v10 트랙 소관)
⚠️ **repo `mickey/` 미러가 극도로 stale**: repo `mickey/domain/` 은 8 entries(May 14) vs 글로벌 66. 본 세션 글로벌 편집분(§20, Categorization Rule, GRAPH Path 컬럼 등)이 repo에 미반영. **install 실행 시 stale repo → global 덮어쓰기로 누적 지식 손실 위험**(adaptive #2/#3). 이 정합화는 v10/install 트랙 소관. 본 CLI 트랙에서 건드리지 않음 (파일 격리 원칙). T1.5 extended-protocols Version 17→18 도 repo 및 T1 agent JSON과 divergence — 차기 reconciliation 대상.

## Context Window Status
~50%

## Next Steps
- **트랙 A Phase 1 완료.** Phase 2(실제 첫 카테고리화)는 다음 세션:
  - 임계값 7 트리거 대상 = verification(aspect→skip) + cdk(도메인). 첫 재편 = cdk/Cloud 계열
  - Phase 2 설계 논점: "cdk만 vs Cloud/AWS/IaC 대계열 통합"(`entries/cloud/{cdk,terraform,agentcore,...}`)
  - Phase 2 전 repo mickey/ 동기화 상태 확인 필요 (install 위험)
- 2순위: 엔트로피 정리 — 프로젝트 common_knowledge INDEX Domain Links out-of-sync 3파일 + auto_notes + ENVIRONMENT.md
- 글로벌 domain/INDEX.md 중복 트리거 행(powershell-curl-escape 등)은 무해(다른 키워드→동일 entry)로 미정리, 필요 시 정리

## Last Updated
2026-07-13 (Mickey 36 초입)
