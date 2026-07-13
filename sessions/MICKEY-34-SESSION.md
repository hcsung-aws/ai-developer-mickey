# Mickey 34 Session Log

## Checkpoint [0/5]

> Mickey 지식 그래프 시각화 도구 구현. 완전 로컬 self-contained HTML 산출. WELC 테스트 harness. 글로벌+프로젝트 두 스코프 지원. 최소→확장 Phase 분해.

## Session Meta
- Type: Implementation (Mickey 자체 도구 신규 구축)
- Mickey: 34
- Date: 2026-07-02 ~
- Autonomy: Level 2 (Balanced) + batch-confirm-autonomous-proceed (3조건 충족 시 자율 진행)

## Session Goal

`~/.kiro/mickey/domain/GRAPH.md` 를 중심으로 구축된 지식 그래프를, 웹 브라우저에서 상호작용 가능한 형태로 시각화하는 Mickey 전용 도구를 구현한다. 결과물은 완전 오프라인(vis-network 인라인) self-contained HTML. 글로벌 스코프와 프로젝트 스코프 두 종을 지원한다.

## Purpose Alignment

- **Scenario 2 (Mickey 자체 개선)** 직접 기여: 진화 루프의 결과물(글로벌 domain 그래프)을 시각적으로 확인 가능 → 고립 노드/밀도 이상/누락 연결 진단 도구
- **Scenario 1 (다른 프로젝트)** 파생 이익: 프로젝트별 지식 지도의 backlink 구조 시각화 → 지식 활용 경로 개선 근거

## Previous Context

- Mickey 33 (2026-07-02 인계): Kiro CLI Tier 3 LSP baseline 활성화 완료 (TS/Pyright/clangd 3종 + PATH 확장)
- M33 인계 1순위 §19.2 감지 마커 보정은 이번 세션 범위에서 제외 (사용자 결정 — 다른 주제 우선)
- 재사용 스크립트 자산 (M33): PATH 백업/확장/검증 스크립트 5종 + safe-batch-replace 패턴 활용 경험

## Entropy Check (세션 시작 시)

- INDEX 정합성: ✅ common_knowledge/INDEX.md 는 M33 신규 2건 등재 완료
- auto_notes 최신성: ⚠️ M29(2026-06-26) 이후 무변경, 5세션 초과. 본 세션 도구 자체에는 영향 없음 (별도 후속 세션에서 정리)
- SESSION 아카이빙: ✅ 프로젝트 루트 clean, 모두 `sessions/` 하위
- 구조 문서 최신성: ⚠️ PROJECT-OVERVIEW(M27), ENVIRONMENT(M18) 노후. 이번 세션에서 도구 추가 시 FILE-STRUCTURE 함께 갱신 필요
- §19.2 감지 마커: ⚠️ 불일치 상태 유지 (다음 세션 후보)
- Curator staging: ✅ 프로젝트 비어 있음
- 포스트모템 트리거: ⏳ 미도달

## Current Tasks

### T1. 방향 확정 + 세션 기록 (사전 기록)
- [x] 옵션 A(vis-network 로컬 인라인) 확정
- [x] Phase 분해 3단계 확정
- [x] session-resilience-prewrite: 본 세션 골격 사전 기록
- [ ] 재확인 2건 (파일 구조, vendor 준비 방식) 사용자 승인 | CC: 사용자 응답 수령

### T2. Phase 1 — 글로벌 스코프 최소 기능

#### T2a. Models + Parser + WELC 테스트
- [ ] `scripts/mickey_graph/models.py` — Node, Edge dataclass | CC: dataclass import 성공, __repr__ 확인
- [ ] `scripts/mickey_graph/parser.py` — md 표 파싱기 | CC: fixture md에서 예상 Node/Edge 수 반환
- [ ] `scripts/tests/fixtures/sample-graph.md` — 최소 fixture (3 nodes + 2 edges)
- [ ] `scripts/tests/test_parser.py` — WELC 테스트 (표 파싱, 중복 병합, dangling edge 경고) | CC: `pytest scripts/tests/` 전 통과

#### T2b. Vendor 준비
- [ ] `scripts/setup_vendor.py` — vis-network min bundle 다운로드 + 검증 | CC: `scripts/mickey_graph/vendor/vis-network.min.js` 존재, 최소 크기 100KB 이상
- [ ] `.gitignore` — vendor/ + output/ 추가 | CC: `git status` 에서 vendor 파일 미표시

#### T2c. Graph Builder (글로벌)
- [ ] `scripts/mickey_graph/graph_builder.py` — GRAPH.md + patterns/INDEX.md → Node/Edge 집합. 중복 병합 정책 적용 | CC: 글로벌 데이터로 실행 시 예상 노드 수(55±)/엣지 수(100±) 산출

#### T2d. Renderer + Template
- [ ] `scripts/mickey_graph/templates/graph.html.tmpl` — vis-network 인라인 + JSON 인라인 + 검색 박스 최소 UI
- [ ] `scripts/mickey_graph/renderer.py` — 템플릿 렌더링 | CC: HTML 결과 파일 크기 300KB~700KB, `<script>` 태그에 vis-network + JSON 모두 포함

#### T2e. CLI + 실 데이터 검증
- [ ] `scripts/mickey_graph_viz.py` — CLI thin wrapper (argparse: --scope, --project-path, --open)
- [ ] 실 데이터 렌더: `python scripts/mickey_graph_viz.py --scope global` | CC: HTML 생성
- [ ] 오프라인 검증: 네트워크 차단 상태에서 브라우저로 열어 그래프 렌더 성공 | CC: 노드/엣지 시각화, 검색 박스 동작, 노드 클릭 → 상세 패널

### T3. Phase 2 — 프로젝트 스코프
- [ ] `graph_builder.py` 프로젝트 모드 추가 (프로젝트 INDEX + Domain Links backlink → cross-scope 엣지)
- [ ] CLI `--scope project --project-path <path>` 지원
- [ ] 렌더 검증 (ai-developer-mickey 프로젝트로 실행) | CC: cross-scope 엣지 점선 표시 확인

### T4. Phase 3 — 확장 UI
- [ ] 태그 필터, 타입 필터, 이웃 강조 (1-hop) | CC: 각 UI 요소 브라우저 동작 확인

### T5. 문서화 + 지식 반영
- [ ] `common_knowledge/INDEX.md` — 새 도구 등재 (트리거: 그래프 시각화, 지식 지도, 진단 도구)
- [ ] `FILE-STRUCTURE.md` — `scripts/mickey_graph/` 추가
- [ ] 필요 시 `context_rule/project-context.md` Key Decisions 갱신

## Progress

### Completed
- (없음, 세션 시작 시점)

### InProgress
- T1: 재확인 2건 사용자 승인 대기

### Blocked
- (없음)

## Key Decisions

- **D-34-1**: 라이브러리 = vis-network. cytoscape.js/d3 대비 학습 곡선 낮고 현재 규모(55~200 노드)에 적합. Alternative: cytoscape.js (알고리즘 다양성 크지만 오버킬)
- **D-34-2**: 배포 방식 = 완전 self-contained 단일 HTML (인라인). CDN 옵션 제외 — 사용자 지시 "네트워크 접근 필요 없게" 준수. `single-artifact-deployment` domain pattern 부합
- **D-34-3**: 구현 순서 = Phase 1(글로벌 최소) → Phase 2(프로젝트) → Phase 3(확장 UI). phase-based-decomposition + plan-implement-verify-trisection 원칙 부합
- **D-34-4**: 테스트 방식 = WELC. Parser/Builder/Renderer 각 계층에 유닛 테스트 + fixture 기반 스냅샷 회귀. Alternative: 통합 테스트만 (거부 이유: 파서 회귀 감지 지연)

## Files Modified

### 신규 (예정)
- `scripts/mickey_graph_viz.py`
- `scripts/mickey_graph/__init__.py`
- `scripts/mickey_graph/models.py`
- `scripts/mickey_graph/parser.py`
- `scripts/mickey_graph/graph_builder.py`
- `scripts/mickey_graph/renderer.py`
- `scripts/mickey_graph/templates/graph.html.tmpl`
- `scripts/setup_vendor.py`
- `scripts/tests/__init__.py`
- `scripts/tests/fixtures/sample-graph.md`
- `scripts/tests/test_parser.py`
- `scripts/tests/test_graph_builder.py`
- `scripts/tests/test_renderer.py`
- `.gitignore` (append: `scripts/mickey_graph/vendor/`, `scripts/output/`)

### 변경 (예정)
- `common_knowledge/INDEX.md` — 도구 등재
- `FILE-STRUCTURE.md` — 구조 반영

## Lessons Learned

(세션 진행 중 기록)

## Context Window Status
~15% (시작 시점, 컨텍스트 로딩 + 옵션 협의 후)

## Next Steps
- 사용자 재확인 2건 응답 → T1 완료 → T2a 착수

## Last Updated
2026-07-02 (Mickey 34)
