# Common Knowledge INDEX

## Knowledge Map

| 트리거 | 파일 | 요약 |
|--------|------|------|
| progressive disclosure, INDEX 설계, 지식 지도, AGENTS.md | progressive-disclosure.md | INDEX=목차 패턴: 범위 확장(지식→프로젝트 파일), 자동 갱신, Verify/Update/Suggest 원칙 |
| context window 절약, 시간 트리거, 계획 문서, 에이전트 설계, 자동 호출, 강제 중단점, passive 발견, backlink | agent-design-patterns.md | 스크립트 위임, 이벤트 기반 트리거, 계획 구체성→실행 속도, 강제 중단점 실행, Passive>Active 지식 활용 |
| 일괄 변경, search replace, 자동화, count-1, 부분 적용 방지, hash 검증, 동기화 | safe-batch-replace.md | 복수 패턴 일괄 적용 시 count-1 guard + 메모리 내 수행 + hash 검증 |
| Windows PATH 확장, winreg, setx 함정, WM_SETTINGCHANGE, 사용자 환경 변수, REG_EXPAND_SZ, PATH 백업 | windows-user-path-extension.md | winreg 직접 쓰기 + WM_SETTINGCHANGE broadcast — setx 1024자 잘림/PowerShell 인용부호 지옥 회피 |
| Kiro CLI, /code init, lsp.json 위치, LSP 감지 마커, .kiro/settings, 문서 drift | kiro-cli-lsp-init-settings-location.md | `/code init` 실 산출물 = `.kiro/settings/lsp.json` (문서 표기와 불일치). 감지 로직은 3개 후보 스캔 |
| 그래프 시각화, 지식 지도 시각화, 진단 도구, vis-network, 태그 chip 필터, 이웃 1-hop 강조, self-contained HTML, 클러스터 발견 | mickey-graph-visualization.md | Mickey 지식 그래프 시각화 도구 (`scripts/mickey_graph/`). 글로벌/프로젝트 스코프 self-contained HTML 렌더. Phase 3 필터 UI(태그 chip + kind/edge 체크박스 + 이웃 강조). WELC 101 tests |

## Last Updated
2026-07-21 (Mickey 40 — Domain Links 2건 추가: normative-example-list-trap + degree-corrected-cluster-cohesion. 직전: Mickey 39 Curator)


## Domain Links

| 키워드 | Domain Entry | 힌트 |
|--------|-------------|------|
| 지식 활용, 검색 vs 발견, backlink | ~/.kiro/mickey/domain/entries/passive-over-active-retrieval.md | Active 검색 실패 → Passive 발견 경로 설계 |
| 자가 진단, 가설 평탄화, 외부 회귀, 이슈 트래커, 진단 사이클 탈출 | ~/.kiro/mickey/domain/entries/external-regression-hypothesis.md | 자가 진단 N세대 평탄화 시 외부 이슈 트래커 검색 우선 |
| 자동 호출 실패, 실행 시점, 중단점 | ~/.kiro/mickey/domain/entries/forced-breakpoint-execution.md | 판단 병목 제거 → 자연스러운 중단점에 배치 |
| 활용도 측정, grep, 포스트모템, 정량 진단 | ~/.kiro/mickey/domain/entries/quantitative-usage-measurement.md | 프로토콜 효과를 실측으로 판단, 0%=설계 결함 |
| 지식 분류, R/G/S, 활용 경로, 저장소 설계 | ~/.kiro/mickey/domain/entries/knowledge-type-routing.md | 지식 성격(방식/사실/절차)별 활용 경로 분리 |
| SoT 중복 회피, 참조, 본문 중복, § 번호 유지 | ~/.kiro/mickey/domain/entries/sot-deduplication-by-reference.md | 동일 지식 1곳만 본문, 나머지 참조. 번호 재배정 금지 |
| data-view 분리, renderer 불변, JSON pre-seeding, UI 확장 비용 | ~/.kiro/mickey/domain/entries/data-view-preseeding-immutability.md | 데이터 직렬화에 UI 필드 사전 포함 → UI 확장 시 데이터 계층 무변경 |
| 검증 도구, health scan, 부수적 진단, 엔트로피 발견 | ~/.kiro/mickey/domain/entries/verification-tool-as-health-scanner.md | 완료 검증 목적 도구 실행이 시스템 상태 이상을 부수적으로 표면화 |
| PowerShell curl escape, 인용부호, JSON body | ~/.kiro/mickey/domain/entries/powershell-curl-escape.md | PowerShell 인용부호 지옥 → body 파일/스크립트 분리 회피 |
| CLI --help 불신, 문서 drift | ~/.kiro/mickey/domain/entries/cli-help-output-distrust.md | --help 출력을 실행 검증 전 신뢰 금지 |
| 배포 출력 불신, 외부 신호 교차 검증 | ~/.kiro/mickey/domain/entries/deploy-output-distrust.md | 도구 "성공" 출력을 외부 신호로 교차 검증 |
| 빈 스캔 불신, 경로 후보 재확인 | ~/.kiro/mickey/domain/entries/empty-scan-distrust.md | 첫 스캔 빈 결과 → 명령어/경로 오류 우선 의심 |
| 경로 정규화, 다중 후보 전략 | ~/.kiro/mickey/domain/entries/llm-path-normalization.md | 산출물 경로 다중 후보 전략 |
| 측정 정밀도 반복 심화, 진단 도구 한계 | ~/.kiro/mickey/domain/entries/iterative-measurement-deepening.md | 측정 도구 정밀도는 반복 깊이 확장으로 정정 |
| install seed 시맨틱, E2E harness, 홈 리다이렉트 | ~/.kiro/mickey/domain/entries/installer-seed-semantics.md | 세대 파일만 갱신 + HOME 리다이렉트 테스트 |
| Curator 프롬프트 동기화, agent JSON, SoT 런타임 | ~/.kiro/mickey/domain/entries/prompt-doc-vs-runtime-loading.md | SoT→런타임 동기화 실측 교훈 |
| 검증 스크립트 기준값, EXPECTED_TOTAL, 무결성 vs 스냅샷 | ~/.kiro/mickey/domain/entries/invariant-vs-snapshot-verification.md | 성장 시스템에서 불변 조건과 고정 카운트 검증 구분 해석 |
| 계층 시각화, member-of 합성, builder 파생 엣지, 병합됨 보임 | ~/.kiro/mickey/domain/entries/data-merge-vs-view-visibility.md | 데이터 병합 ≠ 뷰 표현 — builder 파생 엣지 합성(SoT 불변) |
| 지침 예시, 예시 목록 오독, 규범 문서 설계, 측정 가능 기준 | ~/.kiro/mickey/domain/entries/normative-example-list-trap.md | 규범 문서의 괄호 예시는 LLM에게 분류 규칙으로 소비됨 — 예시 대신 측정 가능 기준 |
| 클러스터 응집도, 허브 효과, aspect 판정, 우연 기대치 | ~/.kiro/mickey/domain/entries/degree-corrected-cluster-cohesion.md | 내부 밀도는 허브 왜곡 — 응집률 vs (k−1)/(N−1) 비교로 aspect/domain 변별 |
