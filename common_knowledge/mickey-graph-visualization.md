# Mickey 지식 그래프 시각화 도구

> `~/.kiro/mickey/domain/GRAPH.md` 를 중심으로 구축된 지식 그래프를 self-contained HTML 로 시각화하는 도구. 진화 루프 산출물(글로벌 domain) 진단 + 프로젝트별 지식 지도의 backlink 구조 확인에 사용.

## 개요

- **위치**: `scripts/mickey_graph/` (파이썬 패키지) + `scripts/mickey_graph_viz.py` (CLI 진입점)
- **결과물**: 완전 오프라인 self-contained HTML (vis-network 인라인, 파일 하나로 브라우저 오픈). 크기 700~800 KB
- **스코프**: 글로벌(`~/.kiro/mickey/`) + 프로젝트별 두 모드 지원

## 왜 필요한가

- **진화 루프 진단**: `domain/entries/` 가 flat 60~80개 축적 후 관찰이 어려움. 고립 노드, 밀도 이상, 재편 후보 클러스터를 시각적으로 식별
- **backlink 활용도 확인**: 프로젝트가 어떤 글로벌 entry 를 실제로 참조하는가 → cross-scope 엣지로 즉시 파악
- **카테고리 재편 근거**: 태그 chip 컨테이너의 chip 빈도 + Show all 로 전체 태그 카디널리티 실측 → progressive-domain-hierarchy 계획서의 클러스터 임계값(5개+) 판단 지원

## CLI 사용법

```powershell
# 글로벌 스코프 (~/.kiro/mickey/ 만)
python scripts/mickey_graph_viz.py --scope global

# 프로젝트 스코프 (프로젝트 지식 + 글로벌 통합)
python scripts/mickey_graph_viz.py --scope project --project-path <프로젝트루트>

# 렌더 후 브라우저 자동 열기
python scripts/mickey_graph_viz.py --scope global --open

# 사용자 지정 mickey_root (테스트/디버그)
python scripts/mickey_graph_viz.py --scope global --mickey-root <경로>
```

**산출물 위치 (기본)**: `scripts/output/mickey-graph-<scope>[-<프로젝트명>].html` (gitignored)

## 확장 UI (Phase 3, M35)

- **뷰 전환** (Project/Global/Combined): 상단 라디오
- **검색**: id/title/tag 부분 매칭 → 노드 선택 + focus
- **필터 바** (chip + checkbox):
  - **Tags**: 태그 chip 목록. 사용 빈도 내림차순 정렬 + count 표시. 클릭 토글. 다태그 데이터셋(380+) 대응 위해 기본은 count>=2 표시, `Show all (+N)` 로 전체 확장. `Hide singletons` 로 복귀. All/None 버튼
  - **Kinds**: 노드 kind 5종(entry/pattern/graduated/project_knowledge/unknown) 체크박스 (색상 swatch 병기)
  - **Edges**: 엣지 type 7종(applies-to/extends/similar-to/prerequisite/cross-scope/member-of/unknown) 체크박스 (색상 line swatch)
- **노드 클릭**: 상세 패널(제목/degree/kind/core/tags/source) + 1-hop 이웃 강조 (자신+이웃 opacity 1.0, 나머지 노드 0.15 / 엣지 0.05)
- **배경 클릭**: 강조 해제 + 상세 패널 초기화 (placeholder + hint 복귀)

## 시각적 매핑

| 요소 | 매핑 |
|------|------|
| 노드 색상 (kind) | entry=파랑 / pattern=주황 / graduated=회색 / project_knowledge=초록 / unknown=빨강 |
| 노드 shape (project subkind) | knowledge=dot / rule=triangle / note=square |
| 노드 크기 | 총 연결 수(in + out) 기반. min 10, max 40 |
| 노드 border 두께 | out_degree 기반. 굵을수록 나가는 링크 많음(탐색 허브) |
| 노드 border 색 (핑크) | 프로젝트가 backlink 로 참조한 글로벌 entry (project 스코프) |
| 엣지 색상 (type) | applies-to=파랑 / extends=보라(점선) / similar-to=초록 / prerequisite=노랑 / cross-scope=핑크(점선+굵음) / member-of=teal(점선, builder 합성) |
| 라벨 표시 | 총 연결 3+ 노드만 항상 표시. 나머지는 hover 시 표시 |

## 확장 계획 (Phase 4, 미구현)

**트리거 조건**: 그래프 뷰어 사용 후 md 편집 왕복 5회+ 실측. 아직 미도달.

**옵션 안**:
- **옵션 Z (최소)**: 노드 우클릭 → 원본 md 파일 열기. 편집은 사용자 에디터에 위임
- **옵션 Y (중간)**: 브라우저 편집 → draft JSON 저장 → CLI 로 병합(diff 검토 후 apply)
- **옵션 X (풀 GUI)**: 로컬 서버 + 자동 저장. single-artifact-deployment 원칙 위배

**추천**: 옵션 Z 부터 도입 (즉각 이익, 낮은 위험). 상세는 `scripts/mickey_graph/ROADMAP.md` Phase 4 참조.

## 관련 파일

- `scripts/mickey_graph/models.py` — Node/Edge/NodeKind/EdgeType dataclass
- `scripts/mickey_graph/parser.py` — md 표 파싱 + patterns/INDEX 해석
- `scripts/mickey_graph/graph_builder.py` — `build_global_graph`, `build_project_graph` + Graduated 흡수 EXTENDS 엣지 자동화 + degree 계산
- `scripts/mickey_graph/renderer.py` — 템플릿 placeholder 치환 (Jinja2 없이 최소 의존)
- `scripts/mickey_graph/templates/graph.html.tmpl` — vis-network + 필터 UI + 이웃 강조 로직 인라인 템플릿
- `scripts/mickey_graph/vendor/vis-network.min.js` — 9.1.9 (689 KB, gitignored)
- `scripts/mickey_graph_viz.py` — CLI thin wrapper
- `scripts/setup_vendor.py` — vendor 다운로드/검증 (최초 실행 시)
- `scripts/verify_offline.py` — 오프라인 렌더 검증
- `scripts/tests/test_{parser,graph_builder,renderer}.py` — WELC 회귀 테스트 101건
- `scripts/mickey_graph/ROADMAP.md` — Phase 별 상세 계획

## 재사용 원칙

- **Data-View 분리**: 데이터 계산은 Python(models/parser/builder), 시각화 로직은 JS(template). 필터 상태는 template 내부 완결
- **WELC harness**: 각 계층 유닛 테스트 + fixture 기반 스냅샷 회귀. renderer 변경 없이 UI 확장 가능 (JSON 직렬화에 필터 대상 필드 모두 포함)
- **오프라인 self-contained**: vendor 인라인, 네트워크 접근 없음 (single-artifact-deployment 도메인 패턴 준수)

## 계층화 표현 (M39)

§20 카테고리화(entries/{category}/ + anchor)의 membership은 md에 엣지로 존재하지 않고 파일 위치로만 표현되므로, builder가 하위 GRAPH 병합 시 `하위 entry → anchor` 방향의 **member-of 엣지를 합성**한다 (md는 불변, 데이터 파생). anchor가 상위 GRAPH에 없으면 member-of가 dangling 승격되어 UNKNOWN(빨강)으로 §20 계약 위반이 시각적으로 표면화된다 (health-scanner 겸용).

## Last Updated
2026-07-20 (Mickey 39 — member-of 계층 엣지 합성. 직전: M35 Phase 3 UI 등재)
