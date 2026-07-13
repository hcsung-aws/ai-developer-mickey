"""Parser WELC 회귀 테스트.

fixture md 파일을 정답 스냅샷으로 삼는다. parser 변경 시 이 테스트가
회귀를 즉시 감지하는 안전망이다. 각 테스트는 하나의 명확한 검증 목표.
"""

from __future__ import annotations

import logging
from pathlib import Path

from mickey_graph.models import EdgeType, NodeKind
from mickey_graph.parser import (
    extract_section,
    parse_edges_from_graph,
    parse_markdown_table,
    parse_nodes_from_graph,
    parse_patterns_index,
    parse_tags,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    """fixture md 파일 읽기 헬퍼."""
    return (FIXTURES / name).read_text(encoding="utf-8")


# --- 저수준 표 파서 ---

class TestParseMarkdownTable:
    def test_basic_table(self):
        text = "| a | b |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n"
        rows = parse_markdown_table(text)
        assert rows == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]

    def test_empty_input_returns_empty(self):
        assert parse_markdown_table("") == []

    def test_no_table_returns_empty(self):
        assert parse_markdown_table("no table\njust prose\n") == []

    def test_empty_cell_preserved_as_empty_string(self):
        text = "| a | b |\n|---|---|\n|  | 2 |\n"
        rows = parse_markdown_table(text)
        assert rows == [{"a": "", "b": "2"}]

    def test_stops_at_first_non_row_line_after_table(self):
        text = "| a |\n|---|\n| 1 |\n\nother content\n| x |\n|---|\n| 99 |\n"
        rows = parse_markdown_table(text)
        # 첫 표만 파싱: [{a: 1}]. 이후 prose 로 종료
        assert rows == [{"a": "1"}]

    def test_multiple_blocks_same_header_merged(self):
        """빈 줄로 분리된 여러 표 블록이 동일 헤더면 하나로 병합 처리.

        GRAPH.md 처럼 시각적 편의로 표를 여러 블록으로 나눈 실제 케이스.
        """
        text = (
            "| id | v |\n"
            "|---|---|\n"
            "| a | 1 |\n"
            "\n"
            "| b | 2 |\n"
            "| c | 3 |\n"
            "\n"
            "| d | 4 |\n"
        )
        rows = parse_markdown_table(text)
        assert rows == [
            {"id": "a", "v": "1"},
            {"id": "b", "v": "2"},
            {"id": "c", "v": "3"},
            {"id": "d", "v": "4"},
        ]

    def test_repeated_header_line_is_skipped(self):
        """블록 사이에 헤더가 반복 등장해도 하나의 표로 병합."""
        text = (
            "| id | v |\n"
            "|---|---|\n"
            "| a | 1 |\n"
            "\n"
            "| id | v |\n"
            "|---|---|\n"
            "| b | 2 |\n"
        )
        rows = parse_markdown_table(text)
        assert rows == [{"id": "a", "v": "1"}, {"id": "b", "v": "2"}]


# --- 섹션 추출 ---

class TestExtractSection:
    def test_extracts_target_section_only(self):
        text = "# Title\n\n## Nodes\ncontent A\n\n## Edges\ncontent B\n"
        section = extract_section(text, "Nodes")
        assert "content A" in section
        assert "content B" not in section

    def test_missing_section_returns_empty(self):
        assert extract_section("# Title\n\nno section here", "Nodes") == ""

    def test_stops_at_higher_level_heading(self):
        text = "## Nodes\nnode content\n# Top Heading\nfurther content"
        section = extract_section(text, "Nodes")
        assert "node content" in section
        assert "further content" not in section


# --- 태그 파싱 ---

class TestParseTags:
    def test_comma_separated(self):
        assert parse_tags("a, b, c") == ["a", "b", "c"]

    def test_empty_input(self):
        assert parse_tags("") == []

    def test_extra_whitespace_and_empty_items(self):
        assert parse_tags("  a ,  b ,   ") == ["a", "b"]


# --- GRAPH.md Nodes 파서 ---

class TestParseNodesFromGraph:
    def test_parses_three_unique_nodes(self):
        text = _read_fixture("sample-graph.md")
        nodes = parse_nodes_from_graph(text, source="fixture")
        ids = [n.id for n in nodes]
        assert ids == ["alpha", "beta", "gamma"]

    def test_duplicate_id_merges_tags_with_warning(self, caplog):
        text = _read_fixture("sample-graph.md")
        with caplog.at_level(logging.WARNING):
            nodes = parse_nodes_from_graph(text)

        alpha = next(n for n in nodes if n.id == "alpha")
        assert set(alpha.tags) == {"tag-a", "tag-b", "tag-d"}
        # 첫 등장 title/core 유지
        assert alpha.title == "Alpha Node"
        assert alpha.core == "Core desc A"
        # WARNING 로그 확인
        assert any("Duplicate node id" in r.message for r in caplog.records)

    def test_all_nodes_tagged_as_entry_kind(self):
        text = _read_fixture("sample-graph.md")
        nodes = parse_nodes_from_graph(text)
        assert all(n.kind == NodeKind.ENTRY for n in nodes)

    def test_source_field_propagated(self):
        text = _read_fixture("sample-graph.md")
        nodes = parse_nodes_from_graph(text, source="test/path.md")
        assert all(n.source == "test/path.md" for n in nodes)


# --- GRAPH.md Edges 파서 ---

class TestParseEdgesFromGraph:
    def test_parses_all_three_edges(self):
        text = _read_fixture("sample-graph.md")
        edges = parse_edges_from_graph(text)
        assert len(edges) == 3

    def test_type_conversion_to_enum(self):
        text = _read_fixture("sample-graph.md")
        edges = parse_edges_from_graph(text)
        types = {(e.from_id, e.to_id): e.type for e in edges}
        assert types[("alpha", "beta")] == EdgeType.APPLIES_TO
        assert types[("beta", "gamma")] == EdgeType.EXTENDS
        assert types[("alpha", "ghost")] == EdgeType.SIMILAR_TO

    def test_dangling_edge_preserved_for_builder_layer(self):
        """정합성 검증은 graph_builder 책임. parser 는 dangling 도 그대로 반환."""
        text = _read_fixture("sample-graph.md")
        edges = parse_edges_from_graph(text)
        dangling = [e for e in edges if e.to_id == "ghost"]
        assert len(dangling) == 1

    def test_unknown_type_downgraded(self):
        text = "## Edges\n| From | To | Type | Reason |\n|---|---|---|---|\n| a | b | mystery | rr |\n"
        edges = parse_edges_from_graph(text)
        assert edges[0].type == EdgeType.UNKNOWN


# --- patterns/INDEX.md 파서 ---

class TestParsePatternsIndex:
    def test_separates_active_and_graduated(self):
        text = _read_fixture("sample-patterns-index.md")
        active, graduated = parse_patterns_index(text, source="fixture")
        assert len(active) == 2
        assert len(graduated) == 1

    def test_kind_tagging(self):
        text = _read_fixture("sample-patterns-index.md")
        active, graduated = parse_patterns_index(text)
        assert all(n.kind == NodeKind.PATTERN for n in active)
        assert all(n.kind == NodeKind.GRADUATED for n in graduated)

    def test_file_based_id_for_md_reference(self):
        text = _read_fixture("sample-patterns-index.md")
        active, _ = parse_patterns_index(text)
        # 'pat-a.md' → id 'pat-a'
        assert any(n.id == "pat-a" for n in active)

    def test_name_slug_id_when_no_file_reference(self):
        """'(INDEX 내 기술)' 처럼 파일 참조가 아닌 경우 이름 slug 사용."""
        text = _read_fixture("sample-patterns-index.md")
        active, _ = parse_patterns_index(text)
        pattern_b = next(n for n in active if n.title == "Pattern B")
        assert pattern_b.id == "pattern-b"

    def test_graduated_uses_absorption_path(self):
        text = _read_fixture("sample-patterns-index.md")
        _, graduated = parse_patterns_index(text)
        # 'entries/foo.md' → id 'foo'
        assert graduated[0].id == "foo"


# --- Graduated 흡수 엣지 추출 ---

class TestExtractEntryReferences:
    def test_single_reference(self):
        from mickey_graph.parser import _extract_entry_references
        assert _extract_entry_references("entries/foo.md") == ["foo"]

    def test_with_domain_prefix(self):
        from mickey_graph.parser import _extract_entry_references
        assert _extract_entry_references("`domain/entries/bar.md`") == ["bar"]

    def test_multiple_references(self):
        from mickey_graph.parser import _extract_entry_references
        text = "`domain/entries/foo.md` + `domain/entries/bar.md` 등"
        refs = _extract_entry_references(text)
        assert refs == ["foo", "bar"]

    def test_no_reference(self):
        from mickey_graph.parser import _extract_entry_references
        assert _extract_entry_references("no md references here") == []


class TestParseGraduatedAbsorptionEdges:
    def test_creates_extends_edge_for_each_entry_reference(self):
        from mickey_graph.parser import parse_graduated_absorption_edges
        from mickey_graph.models import EdgeType

        text = (
            "## Graduated Patterns\n"
            "| 패턴 | 흡수 위치 | Graduated 시점 | 사유 |\n"
            "|---|---|---|---|\n"
            "| Old Pattern | `domain/entries/foo.md` + `domain/entries/bar.md` 결합 "
            "| 2026-01-01 | reason |\n"
        )
        edges = parse_graduated_absorption_edges(text)
        # Old Pattern 이름 slug + '`domain/entries/foo.md` + ...' 는 .md 로 안 끝나서 fallback slug
        # graduated_id 는 name slug 됨: 'old-pattern' (혹은 유니코드 slug)
        # 참조 entries: foo, bar → 2개 엣지
        assert len(edges) == 2
        assert all(e.type == EdgeType.EXTENDS for e in edges)
        target_ids = {e.to_id for e in edges}
        assert target_ids == {"foo", "bar"}

    def test_self_loop_excluded(self):
        """graduated 이름이 흡수 entry 와 같으면 self-loop 제외."""
        from mickey_graph.parser import parse_graduated_absorption_edges

        text = (
            "## Graduated Patterns\n"
            "| 패턴 | 흡수 위치 | Graduated 시점 | 사유 |\n"
            "|---|---|---|---|\n"
            "| Phase Decomposition | entries/phase-decomposition.md | 2026-01 | r |\n"
        )
        edges = parse_graduated_absorption_edges(text)
        # graduated_id = 'phase-decomposition' (file_ref endswith .md → Path.stem)
        # 참조: phase-decomposition → self-loop → 제외
        assert edges == []

    def test_duplicate_edges_deduped(self):
        """같은 from-to 쌍이 여러 번 나와도 하나만."""
        from mickey_graph.parser import parse_graduated_absorption_edges

        text = (
            "## Graduated Patterns\n"
            "| 패턴 | 흡수 위치 | Graduated 시점 | 사유 |\n"
            "|---|---|---|---|\n"
            "| Old | `entries/foo.md` and `entries/foo.md` again | 2026-01 | r |\n"
        )
        edges = parse_graduated_absorption_edges(text)
        assert len(edges) == 1

    def test_empty_section(self):
        from mickey_graph.parser import parse_graduated_absorption_edges
        assert parse_graduated_absorption_edges("") == []


# --- 엣지 케이스 ---

class TestEmptyInputs:
    def test_empty_file_yields_no_nodes(self):
        assert parse_nodes_from_graph("") == []

    def test_empty_file_yields_no_edges(self):
        assert parse_edges_from_graph("") == []

    def test_empty_file_yields_empty_pattern_tuples(self):
        active, graduated = parse_patterns_index("")
        assert active == []
        assert graduated == []


# --- 프로젝트 스코프 파서 (Phase 2) ---

class TestParseProjectKnowledgeMap:
    def test_parses_knowledge_nodes_with_prefix(self):
        from mickey_graph.parser import parse_project_knowledge_map
        text = _read_fixture("sample-project-common-knowledge.md")
        nodes = parse_project_knowledge_map(text, source="fixture")
        assert len(nodes) == 2
        ids = {n.id for n in nodes}
        assert ids == {"pk:knowledge-a", "pk:knowledge-b"}

    def test_kind_and_subkind_tagging(self):
        from mickey_graph.parser import parse_project_knowledge_map
        text = _read_fixture("sample-project-common-knowledge.md")
        nodes = parse_project_knowledge_map(text)
        for n in nodes:
            assert n.kind == NodeKind.PROJECT_KNOWLEDGE
            assert n.subkind == "knowledge"

    def test_trigger_column_becomes_tags(self):
        from mickey_graph.parser import parse_project_knowledge_map
        text = _read_fixture("sample-project-common-knowledge.md")
        nodes = parse_project_knowledge_map(text)
        node_a = next(n for n in nodes if n.id == "pk:knowledge-a")
        assert set(node_a.tags) == {"trigger-a", "tag-x"}


class TestParseProjectRuleMap:
    def test_parses_rule_nodes_with_prefix(self):
        from mickey_graph.parser import parse_project_rule_map
        text = _read_fixture("sample-project-context-rule.md")
        nodes = parse_project_rule_map(text, source="fixture")
        assert len(nodes) == 2
        ids = {n.id for n in nodes}
        assert ids == {"pr:rule-alpha", "pr:rule-beta"}

    def test_subkind_tagging(self):
        from mickey_graph.parser import parse_project_rule_map
        text = _read_fixture("sample-project-context-rule.md")
        nodes = parse_project_rule_map(text)
        assert all(n.subkind == "rule" for n in nodes)


class TestParseProjectNoteMap:
    def test_parses_note_nodes_with_prefix(self):
        from mickey_graph.parser import parse_project_note_map
        text = _read_fixture("sample-project-auto-notes.md")
        nodes = parse_project_note_map(text, source="fixture")
        assert len(nodes) == 2
        ids = {n.id for n in nodes}
        assert ids == {"pn:commands", "pn:error-fixes"}

    def test_category_as_single_tag(self):
        """note 표의 첫 컬럼 '카테고리' 는 콤마 분리 안 하고 단일 태그로."""
        from mickey_graph.parser import parse_project_note_map
        text = _read_fixture("sample-project-auto-notes.md")
        nodes = parse_project_note_map(text)
        node = next(n for n in nodes if n.id == "pn:commands")
        assert node.tags == ["commands"]


class TestParseDomainLinks:
    def test_parses_all_links(self):
        from mickey_graph.parser import parse_domain_links
        text = _read_fixture("sample-project-common-knowledge.md")
        links = parse_domain_links(text)
        assert len(links) == 2

    def test_entry_id_extracted_from_full_path(self):
        from mickey_graph.parser import parse_domain_links
        text = _read_fixture("sample-project-common-knowledge.md")
        links = parse_domain_links(text)
        entry_ids = {l.entry_id for l in links}
        assert entry_ids == {"passive-over-active-retrieval", "forced-breakpoint-execution"}

    def test_keywords_parsed_as_list(self):
        from mickey_graph.parser import parse_domain_links
        text = _read_fixture("sample-project-common-knowledge.md")
        links = parse_domain_links(text)
        passive = next(l for l in links if l.entry_id == "passive-over-active-retrieval")
        assert set(passive.keywords) == {"passive", "backlink"}

    def test_empty_section(self):
        from mickey_graph.parser import parse_domain_links
        assert parse_domain_links("") == []


# --- 본문 domain entry 참조 추출 ---

class TestExtractBodyDomainReferences:
    def test_related_section_with_full_path(self):
        from mickey_graph.parser import extract_body_domain_references
        text = (
            "## Related\n"
            "- `~/.kiro/mickey/domain/entries/foo.md` 관련성 설명\n"
            "- `~/.kiro/mickey/domain/entries/bar.md` 다른 설명\n"
        )
        assert extract_body_domain_references(text) == ["foo", "bar"]

    def test_cross_reference_inline(self):
        from mickey_graph.parser import extract_body_domain_references
        text = "본문 안 - 교차 참조: `~/.kiro/mickey/domain/entries/baz.md`"
        assert extract_body_domain_references(text) == ["baz"]

    def test_dedupes_same_reference(self):
        from mickey_graph.parser import extract_body_domain_references
        text = "entries/foo.md 그리고 나중에 entries/foo.md 다시"
        assert extract_body_domain_references(text) == ["foo"]

    def test_preserves_order(self):
        from mickey_graph.parser import extract_body_domain_references
        text = "entries/first.md ... entries/second.md ... entries/third.md"
        assert extract_body_domain_references(text) == ["first", "second", "third"]

    def test_empty_input(self):
        from mickey_graph.parser import extract_body_domain_references
        assert extract_body_domain_references("") == []

    def test_no_references(self):
        from mickey_graph.parser import extract_body_domain_references
        assert extract_body_domain_references("no domain refs\njust prose") == []
