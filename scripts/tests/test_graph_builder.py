"""Graph Builder WELC 회귀 테스트.

fixture md 파일을 임시 mickey_root 디렉토리 구조에 배치하여
build_global_graph 를 실 파일 IO 로 검증한다.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from mickey_graph.graph_builder import build_global_graph, build_project_graph
from mickey_graph.models import EdgeType, NodeKind

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fake_mickey_root(tmp_path: Path) -> Path:
    """가짜 ~/.kiro/mickey/ 디렉토리 구조 생성.

    - domain/GRAPH.md ← sample-graph.md fixture 복사
    - patterns/INDEX.md ← sample-patterns-index.md fixture 복사
    """
    domain_dir = tmp_path / "domain"
    patterns_dir = tmp_path / "patterns"
    domain_dir.mkdir()
    patterns_dir.mkdir()

    shutil.copy(FIXTURES / "sample-graph.md", domain_dir / "GRAPH.md")
    shutil.copy(FIXTURES / "sample-patterns-index.md", patterns_dir / "INDEX.md")
    return tmp_path


class TestBuildGlobalGraph:
    def test_returns_expected_node_count(self, fake_mickey_root: Path):
        """3 nodes (graph) + 2 active patterns + 1 graduated + 1 dangling(ghost) = 7."""
        graph, stats = build_global_graph(fake_mickey_root)
        assert stats.node_count == 7

    def test_sub_category_graph_merged(self, fake_mickey_root: Path):
        """§20 Step 3 하위 카테고리 GRAPH 병합: entries/{cat}/GRAPH.md 노드/엣지가 합류하고
        cross-category 엣지(상위 노드 → 하위 노드)가 dangling 승격되지 않아야 한다."""
        sub_dir = fake_mickey_root / "domain" / "entries" / "cloudx"
        sub_dir.mkdir(parents=True)
        (sub_dir / "GRAPH.md").write_text(
            "# Sub Graph\n\n"
            "## Nodes\n"
            "| ID | Title | Tags | Core | Path |\n"
            "|----|-------|------|------|------|\n"
            "| sub-one | Sub One | tag-x | core X | entries/cloudx/sub-one.md |\n"
            "| sub-two | Sub Two | tag-y | core Y | entries/cloudx/sub-two.md |\n\n"
            "## Edges\n"
            "| From | To | Type | Reason |\n"
            "|------|----|------|--------|\n"
            "| sub-one | sub-two | extends | internal edge |\n",
            encoding="utf-8",
        )
        # 상위 GRAPH에 cross-category 엣지 추가 (alpha → sub-one)
        top = fake_mickey_root / "domain" / "GRAPH.md"
        text = top.read_text(encoding="utf-8")
        text = text.replace(
            "| alpha | ghost | similar-to | dangling target for test |",
            "| alpha | ghost | similar-to | dangling target for test |\n"
            "| alpha | sub-one | applies-to | cross-category edge |",
        )
        top.write_text(text, encoding="utf-8")

        graph, stats = build_global_graph(fake_mickey_root)
        node_ids = {n.id for n in graph.nodes}
        assert {"sub-one", "sub-two"} <= node_ids, "하위 GRAPH 노드 병합"
        assert any(e.from_id == "sub-one" and e.to_id == "sub-two" for e in graph.edges), "하위 내부 엣지 병합"
        # sub-one 은 실노드로 로딩되므로 UNKNOWN 승격 대상은 기존 ghost 1건만
        unknown = [n for n in graph.nodes if n.kind == NodeKind.UNKNOWN]
        assert [n.id for n in unknown] == ["ghost"], "cross-category 엣지 dangling 승격 없음"

    def test_returns_expected_edge_count(self, fake_mickey_root: Path):
        """3 edges (graph). Graduated 'Old Pattern' → foo 는 self-loop 이므로 흡수 엣지 미생성."""
        graph, stats = build_global_graph(fake_mickey_root)
        assert stats.edge_count == 3

    def test_graduated_absorption_edge_present(self, fake_mickey_root: Path):
        """Graduated 'Old Pattern' → 'foo' EXTENDS 엣지 자동 생성 확인."""
        graph, _ = build_global_graph(fake_mickey_root)
        # graduated id = _slugify_pattern('Old Pattern', 'entries/foo.md') = 'foo' (file stem)
        # → self-loop 되므로 실제로는 엣지 생성되지 않음.
        # 이 fixture 는 self-loop 케이스 검증용.
        # 다른 fixture 로 non-self-loop 케이스 검증은 별도.
        edges_from_graduated = [e for e in graph.edges if e.to_id == "foo" and e.from_id != "foo"]
        # self-loop 이므로 0 예상
        assert edges_from_graduated == []

    def test_dangling_edge_promoted_to_unknown_node(self, fake_mickey_root: Path):
        graph, stats = build_global_graph(fake_mickey_root)
        assert stats.dangling_edges_promoted == 1

        ghost = next((n for n in graph.nodes if n.id == "ghost"), None)
        assert ghost is not None
        assert ghost.kind == NodeKind.UNKNOWN

    def test_kind_distribution(self, fake_mickey_root: Path):
        """3 ENTRY + 2 PATTERN + 1 GRADUATED + 1 UNKNOWN"""
        graph, stats = build_global_graph(fake_mickey_root)
        dist = stats.kind_distribution
        assert dist.get(NodeKind.ENTRY.value) == 3
        assert dist.get(NodeKind.PATTERN.value) == 2
        assert dist.get(NodeKind.GRADUATED.value) == 1
        assert dist.get(NodeKind.UNKNOWN.value) == 1

    def test_missing_graph_file_logs_warning(self, tmp_path: Path, caplog):
        """domain/GRAPH.md 가 없어도 예외 없이 진행."""
        # patterns 만 있는 구조
        patterns_dir = tmp_path / "patterns"
        patterns_dir.mkdir()
        shutil.copy(FIXTURES / "sample-patterns-index.md", patterns_dir / "INDEX.md")

        import logging
        with caplog.at_level(logging.WARNING):
            graph, stats = build_global_graph(tmp_path)

        assert stats.node_count == 3   # 2 active + 1 graduated
        assert stats.edge_count == 0
        assert any("graph file not found" in r.message for r in caplog.records)

    def test_empty_mickey_root(self, tmp_path: Path):
        """domain/, patterns/ 모두 없어도 빈 그래프 반환."""
        graph, stats = build_global_graph(tmp_path)
        assert stats.node_count == 0
        assert stats.edge_count == 0


class TestDedupePreferEntry:
    """같은 ID 가 여러 kind 로 등장하면 ENTRY 우선 유지 (더 상세 정보 보유)."""

    def test_entry_wins_over_graduated(self, tmp_path: Path):
        """
        시나리오: GRAPH.md 에 'foo' entry(태그 tag-a) + patterns Graduated 에
        'entries/foo.md' 참조 → 같은 ID 'foo' 로 슬러그되어 충돌.
        결과: ENTRY 유지, 태그는 union.
        """
        domain_dir = tmp_path / "domain"
        patterns_dir = tmp_path / "patterns"
        domain_dir.mkdir()
        patterns_dir.mkdir()

        (domain_dir / "GRAPH.md").write_text(
            "## Nodes\n"
            "| ID | Title | Tags | Core |\n"
            "|---|---|---|---|\n"
            "| foo | Foo Entry | tag-a | entry core |\n"
            "\n"
            "## Edges\n"
            "| From | To | Type | Reason |\n"
            "|---|---|---|---|\n",
            encoding="utf-8",
        )
        (patterns_dir / "INDEX.md").write_text(
            "## Graduated Patterns\n"
            "| 패턴 | 흡수 위치 | Graduated 시점 | 사유 |\n"
            "|---|---|---|---|\n"
            "| Foo Pattern | entries/foo.md | 2026-01-01 | absorbed |\n",
            encoding="utf-8",
        )

        graph, stats = build_global_graph(tmp_path)
        foo = next(n for n in graph.nodes if n.id == "foo")
        assert foo.kind == NodeKind.ENTRY
        assert foo.title == "Foo Entry"    # ENTRY title 유지
        assert "tag-a" in foo.tags


class TestGraduatedAbsorptionEdgeIntegration:
    """Graduated 노드 → 흡수 entry 로 EXTENDS 엣지 자동 생성 (실 케이스 모사)."""

    def test_creates_extends_edge_when_targets_differ(self, tmp_path: Path):
        """
        시나리오: Graduated 이름 slug 와 흡수 entry ID 가 다르면 실제 엣지 생성.
        Graduated 'Complex Pattern' + 흡수 위치 backtick 감싼 참조 → self-loop 아님.
        """
        domain_dir = tmp_path / "domain"
        patterns_dir = tmp_path / "patterns"
        domain_dir.mkdir()
        patterns_dir.mkdir()

        (domain_dir / "GRAPH.md").write_text(
            "## Nodes\n"
            "| ID | Title | Tags | Core |\n"
            "|---|---|---|---|\n"
            "| target-entry | Target Entry | t1 | c1 |\n"
            "\n"
            "## Edges\n"
            "| From | To | Type | Reason |\n"
            "|---|---|---|---|\n",
            encoding="utf-8",
        )
        (patterns_dir / "INDEX.md").write_text(
            "## Graduated Patterns\n"
            "| 패턴 | 흡수 위치 | Graduated 시점 | 사유 |\n"
            "|---|---|---|---|\n"
            "| Complex Pattern | `domain/entries/target-entry.md` 그리고 설명 | 2026 | r |\n",
            encoding="utf-8",
        )

        graph, stats = build_global_graph(tmp_path)
        # graduated_id = _slugify_pattern('Complex Pattern', '`domain/entries/target-entry.md`...') 
        # file_ref 는 .md 로 안 끝나므로(뒤에 텍스트 있음) → name slug → 'complex-pattern'
        # target 참조: 'target-entry'
        # 결과: 'complex-pattern' → 'target-entry' EXTENDS 엣지
        extends_edges = [e for e in graph.edges if e.type.value == "extends"]
        assert len(extends_edges) == 1
        assert extends_edges[0].from_id == "complex-pattern"
        assert extends_edges[0].to_id == "target-entry"


class TestComputeDegrees:
    """G3: in-degree / out-degree 계산 검증."""

    def test_degrees_reflect_edge_counts(self, fake_mickey_root: Path):
        graph, _ = build_global_graph(fake_mickey_root)
        # fixture: alpha→beta, beta→gamma, alpha→ghost
        assert graph.out_degrees.get("alpha") == 2   # → beta, → ghost
        assert graph.out_degrees.get("beta") == 1    # → gamma
        assert graph.in_degrees.get("beta") == 1     # ← alpha
        assert graph.in_degrees.get("gamma") == 1    # ← beta
        assert graph.in_degrees.get("ghost") == 1    # ← alpha (dangling → UNKNOWN 노드)

    def test_isolated_node_has_zero_degrees(self, fake_mickey_root: Path):
        """엣지 없는 pattern 노드는 in/out 모두 0."""
        graph, _ = build_global_graph(fake_mickey_root)
        # 'pat-a' 는 Pattern Map 표에서 나옴, 엣지는 GRAPH.md 에만 있으니 0
        assert graph.in_degrees.get("pat-a", -1) == 0
        assert graph.out_degrees.get("pat-a", -1) == 0


# --- 프로젝트 스코프 (Phase 2) ---

@pytest.fixture
def fake_project(tmp_path: Path, fake_mickey_root: Path) -> tuple[Path, Path]:
    """가짜 프로젝트 디렉토리 구조 생성.

    - <project>/common_knowledge/INDEX.md ← sample-project-common-knowledge.md
    - <project>/context_rule/INDEX.md ← sample-project-context-rule.md
    - <project>/auto_notes/NOTES.md ← sample-project-auto-notes.md
    - mickey_root: 별도 fixture 재사용
    """
    proj_root = tmp_path / "fake-project"

    ck_dir = proj_root / "common_knowledge"
    cr_dir = proj_root / "context_rule"
    an_dir = proj_root / "auto_notes"
    ck_dir.mkdir(parents=True)
    cr_dir.mkdir(parents=True)
    an_dir.mkdir(parents=True)

    shutil.copy(FIXTURES / "sample-project-common-knowledge.md", ck_dir / "INDEX.md")
    shutil.copy(FIXTURES / "sample-project-context-rule.md", cr_dir / "INDEX.md")
    shutil.copy(FIXTURES / "sample-project-auto-notes.md", an_dir / "NOTES.md")

    return proj_root, fake_mickey_root


class TestBuildProjectGraph:
    def test_project_nodes_added(self, fake_project):
        proj_root, mickey_root = fake_project
        graph, stats = build_project_graph(proj_root, mickey_root)

        # 프로젝트 노드 = 2(K) + 2(R) + 2(N) = 6개
        project_nodes = [n for n in graph.nodes if n.kind == NodeKind.PROJECT_KNOWLEDGE]
        assert len(project_nodes) == 6

    def test_project_subkinds_all_present(self, fake_project):
        proj_root, mickey_root = fake_project
        graph, _ = build_project_graph(proj_root, mickey_root)
        subkinds = {n.subkind for n in graph.nodes if n.kind == NodeKind.PROJECT_KNOWLEDGE}
        assert subkinds == {"knowledge", "rule", "note"}

    def test_global_nodes_included(self, fake_project):
        """전체 글로벌 그래프도 포함되어야 함."""
        proj_root, mickey_root = fake_project
        graph, _ = build_project_graph(proj_root, mickey_root)
        entry_nodes = [n for n in graph.nodes if n.kind == NodeKind.ENTRY]
        # fake_mickey_root fixture 는 3 entry nodes (alpha/beta/gamma)
        assert len(entry_nodes) == 3

    def test_backlinked_entry_ids_captured(self, fake_project):
        """Domain Links 참조 entry ID 가 backlinked set 에 기록됨."""
        proj_root, mickey_root = fake_project
        graph, _ = build_project_graph(proj_root, mickey_root)
        assert "passive-over-active-retrieval" in graph.backlinked_entry_ids
        assert "forced-breakpoint-execution" in graph.backlinked_entry_ids

    def test_backlinked_targets_promoted_when_missing_global(self, fake_project):
        """backlink 대상이 글로벌 그래프에 없으면 UNKNOWN 노드로 자동 승격."""
        proj_root, mickey_root = fake_project
        graph, _ = build_project_graph(proj_root, mickey_root)
        # fake mickey 에는 passive-over-active-retrieval 노드가 없음 → UNKNOWN 승격
        passive_node = next(
            (n for n in graph.nodes if n.id == "passive-over-active-retrieval"), None
        )
        assert passive_node is not None
        assert passive_node.kind == NodeKind.UNKNOWN

    def test_project_node_ids_set(self, fake_project):
        proj_root, mickey_root = fake_project
        graph, _ = build_project_graph(proj_root, mickey_root)
        assert graph.project_node_ids == {
            "pk:knowledge-a", "pk:knowledge-b",
            "pr:rule-alpha", "pr:rule-beta",
            "pn:commands", "pn:error-fixes",
        }

    def test_cross_scope_edges_generated_by_keyword_match(self, fake_project):
        """Domain Links 키워드 ↔ 프로젝트 노드 태그 매칭으로 CROSS_SCOPE 엣지 생성.

        fixture 데이터:
        - Domain Link 'passive, backlink' → passive-over-active-retrieval
        - 프로젝트 knowledge 태그 = 'trigger-a', 'tag-x' + 'trigger-b'
        → 매칭 없음 (교집합 empty). CROSS_SCOPE 엣지 = 0.
        """
        proj_root, mickey_root = fake_project
        graph, _ = build_project_graph(proj_root, mickey_root)
        cross_edges = [e for e in graph.edges if e.type == EdgeType.CROSS_SCOPE]
        # fixture 데이터로는 태그 교집합이 없어 매칭 실패 → 엣지 0
        assert len(cross_edges) == 0
        # 그러나 backlinked_entry_ids 는 여전히 채워짐 (뷰 강조용)
        assert len(graph.backlinked_entry_ids) == 2

    def test_cross_scope_edge_when_tags_match(self, tmp_path, fake_mickey_root):
        """태그가 실제로 매칭되면 CROSS_SCOPE 엣지 생성."""
        proj_root = tmp_path / "match-project"
        ck_dir = proj_root / "common_knowledge"
        ck_dir.mkdir(parents=True)

        (ck_dir / "INDEX.md").write_text(
            "## Knowledge Map\n"
            "| 트리거 | 파일 | 요약 |\n"
            "|---|---|---|\n"
            "| passive discovery, backlink | my-knowledge.md | summary |\n"
            "\n"
            "## Domain Links\n"
            "| 키워드 | Domain Entry | 힌트 |\n"
            "|---|---|---|\n"
            "| passive, backlink | entries/passive-over-active-retrieval.md | hint |\n",
            encoding="utf-8",
        )

        graph, _ = build_project_graph(proj_root, fake_mickey_root)
        cross_edges = [e for e in graph.edges if e.type == EdgeType.CROSS_SCOPE]
        # 'backlink' 태그가 양쪽에 있어 매칭 성공
        assert len(cross_edges) == 1
        assert cross_edges[0].from_id == "pk:my-knowledge"
        assert cross_edges[0].to_id == "passive-over-active-retrieval"

    def test_substring_matching_extends_matches(self, tmp_path, fake_mickey_root):
        """개선된 substring 매칭: 프로젝트 태그가 키워드를 포함하면 매칭.

        예: 프로젝트 태그 'passive 발견' + 키워드 'passive' → 부분 문자열 매칭 성공.
        기존 정확 일치 규칙에서는 실패했을 케이스.
        """
        proj_root = tmp_path / "substring-project"
        ck_dir = proj_root / "common_knowledge"
        ck_dir.mkdir(parents=True)

        (ck_dir / "INDEX.md").write_text(
            "## Knowledge Map\n"
            "| 트리거 | 파일 | 요약 |\n"
            "|---|---|---|\n"
            "| passive 발견 경로, backlink 설계 | design-doc.md | summary |\n"
            "\n"
            "## Domain Links\n"
            "| 키워드 | Domain Entry | 힌트 |\n"
            "|---|---|---|\n"
            "| passive, backlink | entries/passive-over-active-retrieval.md | hint |\n",
            encoding="utf-8",
        )

        graph, _ = build_project_graph(proj_root, fake_mickey_root)
        cross_edges = [e for e in graph.edges if e.type == EdgeType.CROSS_SCOPE]
        # 부분 매칭으로 성공
        assert len(cross_edges) == 1

    def test_project_similar_edges_from_shared_backlinks(self, tmp_path, fake_mickey_root):
        """두 프로젝트 노드가 같은 backlink target 공유하면 자동 SIMILAR_TO 엣지."""
        proj_root = tmp_path / "similar-project"
        ck_dir = proj_root / "common_knowledge"
        ck_dir.mkdir(parents=True)

        (ck_dir / "INDEX.md").write_text(
            "## Knowledge Map\n"
            "| 트리거 | 파일 | 요약 |\n"
            "|---|---|---|\n"
            "| passive design | doc-a.md | A summary |\n"
            "| backlink pattern | doc-b.md | B summary |\n"
            "\n"
            "## Domain Links\n"
            "| 키워드 | Domain Entry | 힌트 |\n"
            "|---|---|---|\n"
            "| passive | entries/passive-over-active-retrieval.md | hint1 |\n"
            "| backlink | entries/passive-over-active-retrieval.md | hint2 |\n",
            encoding="utf-8",
        )

        graph, _ = build_project_graph(proj_root, fake_mickey_root)
        # doc-a 는 'passive' 링크에 매칭, doc-b 는 'backlink' 링크에 매칭
        # 둘 다 같은 entry 'passive-over-active-retrieval' 참조 → SIMILAR_TO 엣지 생성
        similar_edges = [
            e for e in graph.edges
            if e.type == EdgeType.SIMILAR_TO
            and e.from_id.startswith("pk:")
            and e.to_id.startswith("pk:")
        ]
        assert len(similar_edges) == 1
        endpoints = {similar_edges[0].from_id, similar_edges[0].to_id}
        assert endpoints == {"pk:doc-a", "pk:doc-b"}


class TestBodyReferenceParsing:
    """옵션 A: 파일 본문의 domain entry 참조를 자동으로 CROSS_SCOPE 엣지로."""

    def test_body_reference_creates_cross_scope_edge(self, tmp_path, fake_mickey_root):
        """INDEX 에는 없지만 파일 본문에 있는 참조도 CROSS_SCOPE 엣지로 승격."""
        proj_root = tmp_path / "body-ref-project"
        ck_dir = proj_root / "common_knowledge"
        ck_dir.mkdir(parents=True)

        # INDEX 는 knowledge 노드 등록만, Domain Links 는 비움
        (ck_dir / "INDEX.md").write_text(
            "## Knowledge Map\n"
            "| 트리거 | 파일 | 요약 |\n"
            "|---|---|---|\n"
            "| my trigger | my-doc.md | summary |\n",
            encoding="utf-8",
        )

        # 실제 파일 본문에 domain entry 참조 (## Related 섹션)
        (ck_dir / "my-doc.md").write_text(
            "# My Document\n\n"
            "본문 내용...\n\n"
            "## Related\n"
            "- `~/.kiro/mickey/domain/entries/target-x.md` 관련성\n"
            "- `~/.kiro/mickey/domain/entries/target-y.md` 다른 관련성\n",
            encoding="utf-8",
        )

        graph, _ = build_project_graph(proj_root, fake_mickey_root)
        cross_edges = [
            e for e in graph.edges
            if e.type == EdgeType.CROSS_SCOPE and e.from_id == "pk:my-doc"
        ]
        targets = {e.to_id for e in cross_edges}
        assert targets == {"target-x", "target-y"}

    def test_body_reference_dedupes_with_index_links(self, tmp_path, fake_mickey_root):
        """INDEX Domain Links 와 본문 참조가 겹치면 중복 엣지 미생성."""
        proj_root = tmp_path / "dedupe-project"
        ck_dir = proj_root / "common_knowledge"
        ck_dir.mkdir(parents=True)

        # INDEX 에 이미 링크 등록됨
        (ck_dir / "INDEX.md").write_text(
            "## Knowledge Map\n"
            "| 트리거 | 파일 | 요약 |\n"
            "|---|---|---|\n"
            "| overlap trigger | overlap-doc.md | summary |\n"
            "\n"
            "## Domain Links\n"
            "| 키워드 | Domain Entry | 힌트 |\n"
            "|---|---|---|\n"
            "| overlap | entries/shared-target.md | hint |\n",
            encoding="utf-8",
        )

        # 같은 참조가 본문에도 있음
        (ck_dir / "overlap-doc.md").write_text(
            "# Overlap Doc\n\n"
            "## Related\n"
            "- `entries/shared-target.md`\n",
            encoding="utf-8",
        )

        graph, _ = build_project_graph(proj_root, fake_mickey_root)
        cross_edges = [
            e for e in graph.edges
            if e.type == EdgeType.CROSS_SCOPE
            and e.from_id == "pk:overlap-doc"
            and e.to_id == "shared-target"
        ]
        # dedupe 로 하나만
        assert len(cross_edges) == 1

    def test_body_reference_warning_when_index_out_of_sync(self, tmp_path, fake_mickey_root, caplog):
        """INDEX 에 없지만 본문에 있는 참조 발견 시 WARNING 로그."""
        import logging
        proj_root = tmp_path / "outofsync-project"
        ck_dir = proj_root / "common_knowledge"
        ck_dir.mkdir(parents=True)

        (ck_dir / "INDEX.md").write_text(
            "## Knowledge Map\n"
            "| 트리거 | 파일 | 요약 |\n"
            "|---|---|---|\n"
            "| trigger | doc.md | summary |\n",
            encoding="utf-8",
        )
        (ck_dir / "doc.md").write_text(
            "## Related\n"
            "- `entries/only-in-body.md`\n",
            encoding="utf-8",
        )

        with caplog.at_level(logging.WARNING):
            build_project_graph(proj_root, fake_mickey_root)

        assert any(
            "out-of-sync" in r.message.lower() or "only-in-body" in r.message
            for r in caplog.records
        )
