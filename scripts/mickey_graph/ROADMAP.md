# Mickey Graph Viz — Roadmap

> 지식 그래프 시각화 도구의 확장 계획. Phase 1 · 1.5 (M34), Phase 2 (M34), Phase 3 (M35) 구현 완료. Phase 4 는 사용자 확인 기반으로 진행.

## 현재 상태 (M35 종료 시점)

- ✅ Phase 1: 글로벌 스코프 self-contained HTML 렌더 (~/.kiro/mickey/domain/GRAPH.md + patterns/INDEX.md)
- ✅ Phase 1.5:
  - G1: Graduated → 흡수 entry EXTENDS 엣지 자동 생성
  - G2: 물리 옵션 튜닝 + zoom-to-fit + 라벨 표시 임계
  - G3: 연결 중심성(in/out degree) 기반 노드 크기 / border 두께 / 라벨 표시 규칙
- ✅ Phase 2 (M34 실 구현, M35 실측 확인): 프로젝트 스코프. `build_project_graph`, `--scope project --project-path` CLI 지원. 프로젝트 노드(subkind knowledge/rule/note) + 글로벌 domain entry backlink cross-scope 엣지 렌더
- ✅ Phase 3 (M35): 확장 UI
  - T2a 태그 chip 필터 (chip 목록, 빈도순 정렬, count 표시, All/None 버튼)
  - T2b 노드 kind + edge type 체크박스 필터 (색상 swatch 병기)
  - T2c 이웃 1-hop 강조 (클릭 노드 + 이웃 opacity 1.0, 나머지 노드 0.15/엣지 0.05. 배경 클릭 시 원상복구)
  - B 개선: 다태그 데이터셋 대응 — chip 컨테이너 max-height 스크롤 + count>=2 임계값 + "Show all/Hide singletons" 토글
  - T2d 노드 그룹핑: 재평가 결과 생략 (태그 chip과 UX 중복 + kind legend 색상 충돌 위험)

## Phase 2 — 프로젝트 스코프 (완료, M34)

**구현 요약**: `build_project_graph` 는 프로젝트 지식(common_knowledge / context_rule / auto_notes)을 project_knowledge 노드로 편입 + subkind(knowledge/rule/note) 별 vis-network shape 매핑(dot/triangle/square). Domain Links 표 + 본문 노드 ID 참조를 스캔하여 CROSS_SCOPE 엣지 생성. 프로젝트 노드 간 SIMILAR_TO 엣지는 공통 backlink 기반.

**CLI**:
```
python scripts/mickey_graph_viz.py --scope project --project-path <path>
```

**뷰 전환**: 상단 라디오 `Project` / `Global` / `Combined` — 프로젝트 노드만 / 전 글로벌만 (backlink 강조) / 전부.

## Phase 3 — 확장 UI (완료, M35)

**구현 요약** (M35 상세, 회귀 테스트 101 passed):
- **태그 chip 필터** — 사용 빈도 내림차순 정렬 + count 표시. white-list 방식(활성 태그만 통과, OR 매칭). All/None 버튼. **B 개선**: count>=2 기본 표시 + `Show all (+N)` / `Hide singletons` 토글 + max-height 110px 스크롤 컨테이너 (다태그 380+ 데이터셋 UX 대응)
- **노드 kind 필터** — 5종(entry/pattern/graduated/project_knowledge/unknown) 체크박스. 색상 swatch 병기
- **엣지 type 필터** — 6종(applies-to/extends/similar-to/prerequisite/cross-scope/unknown) 체크박스. 색상 line swatch
- **이웃 1-hop 강조** — 노드 클릭 시 자신 + 1-hop 이웃만 opacity 1.0, 나머지 노드 0.15 / 엣지 0.05 dim. 관련 엣지는 opacity 1.0. 배경 클릭 시 원상복구 + 상세 패널 초기화

**UI 배치**:
```
<header> Mickey Graph | view-switch(Project/Global/Combined) | search | legend | stats </header>
<filter-bar> Tags(chip container) | Kinds(checks) | Edges(checks) </filter-bar>
<main> #graph | #detail(상세 패널 + hint) </main>
```

**설계 결정**:
- 필터 로직 전부 template 의 JS 로 처리. `renderer.py` 무변경 (JSON 직렬화에 이미 tags/kind/type 포함)
- 필터 상태 = `filterState` 객체 (activeTags/Kinds/EdgeTypes Set + showAllTags bool). white-list 방식으로 초기값 = 모두 활성
- `applyView(view)` 함수가 뷰 + 3중 필터 통합 → 노드/엣지 hidden 필드 batch 갱신 + stats 표시

## Phase 4 — 그래프 기반 편집 (계획, 구현 시점 미확정)

### 목적
브라우저에서 그래프를 보다가 즉시 편집(노드 추가/삭제, 태그 수정, 엣지 연결)을 하고 md 파일에 반영. 지식 관리의 마찰 최소화.

### 접근 옵션

#### 옵션 Z: 편집 위임 (마찰 최소, 위험 최소)
- 노드 우클릭 → "원본 md 파일 열기" 버튼 → 사용자의 기본 에디터로 파일 열기
- 웹은 순수 뷰어 유지. 실제 편집은 사용자가 md 를 직접 수정
- **장점**: md 원본 순서/포맷 보존, 다중 세션 충돌 없음, 구현 매우 간단
- **단점**: 편집 흐름이 도구 밖으로 나감 (UX 약함)
- 구현 규모: HTML 링크 + 파일 프로토콜 (`file://` scheme) 지원 or Kiro CLI 명령 트리거

#### 옵션 Y: Draft 병합 (중간)
- 브라우저에서 편집 → "Draft" 로 임시 저장 (JSON 로컬 저장 or POST → 로컬 서버)
- 파이썬 CLI(`mickey_graph_apply.py`) 실행 → draft 를 원본 md 와 병합 → 사용자 검토(diff) → 승인 시 md 파일 갱신
- **장점**: 편집 UI + 안전 워크플로우(diff 검토), Curator 흐름과 유사
- **단점**: 로컬 서버 or 파일 저장 UX 결정 필요, md 병합 로직 복잡 (표 위치 유지, 부수 텍스트 보존)
- 구현 규모: 클라이언트 JS + 서버 스크립트 + md 병합기 (safe-batch-replace 패턴 재사용 가능)

#### 옵션 X: 완전 GUI 편집 (풀 편집기, 위험 큼)
- 브라우저에서 편집 즉시 md 반영. 로컬 서버 필수 (자동 저장)
- **장점**: UX 매끄러움
- **단점**: single-artifact-deployment 패턴 완전 위배, 서버 의존, 자동 저장 실수 시 복구 어려움
- 구현 규모: FastAPI/Flask 서버 + WebSocket + 파일 감시 + 롤백 관리

### 추천 착수 순서

1. **옵션 Z 먼저** — 즉각 이익, 낮은 위험. "노드 클릭 → md 파일 위치 콘솔 출력 or 클립보드 복사" 부터 시작
2. Z 로 부족하면 **옵션 Y** — 편집 시나리오가 잦으면 draft 병합. 로컬 CLI 흐름 유지
3. **옵션 X 는 신중** — 사용자가 편집 도구로 정말 원한다면. 그 전에 옵션 Y 로 6개월 이상 사용해 요구사항 확립

### 위험 요소

| 위험 | 완화 |
|------|------|
| md 원본 순서/포맷 손실 | 병합 시 dry-run diff 필수, 사용자 승인 후 apply |
| 다중 편집 세션 충돌 | 파일 잠금(lock file) or 낙관적 병합(diff base 확인) |
| Curator 워크플로우와 중복/충돌 | 편집 결과를 Curator staging 형태로 두고 승인 흐름 통합 |
| 웹 UI 편집 실수의 파괴적 결과 | 항상 git commit 상태 확인, 편집 전 자동 백업 |
| 오프라인 정책 위배 (서버 옵션 X/Y) | Y 는 로컬 CLI 로 대체 가능, X 만 서버 필수 → X 는 최후 |

### 트리거 조건 (Phase 4 착수 시점)

- 그래프 뷰어 사용 후 md 편집 필요성이 명확히 반복 (예: 사용자가 5회 이상 뷰어 → 에디터 왕복)
- 편집 후 브라우저 재렌더의 마찰이 실측 문제
- Phase 2/3 안정화 완료

---

## 새 Phase 추가 규칙

- 아이디어는 이 문서에 우선 기록 (구현 여부와 무관)
- 사용자가 착수 결정하면 SESSION.md Current Tasks 로 승격
- 완료 시 이 문서의 해당 항목에 ✅ 표시 + 완료 세션 참조

## Last Updated
2026-07-11 (Mickey 35) — Phase 2/3 완료 표시 + B 개선(다태그 UX) 반영 + 노드 그룹핑 재평가 결과 (생략)
