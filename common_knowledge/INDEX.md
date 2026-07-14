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
2026-07-13 (Mickey 35 — mickey-graph-visualization.md 추가 + Domain Backlink data-view-preseeding-immutability 추가)


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
