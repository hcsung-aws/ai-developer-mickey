"""Renderer WELC 회귀 테스트.

- JSON 직렬화 정확성
- Placeholder 치환 완료 (남아있는 __*__ 없음)
- 결과 HTML 에 vis-network 라이브러리, 그래프 데이터, 검색 UI 포함
- 파일 쓰기 및 부모 디렉토리 자동 생성
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mickey_graph.graph_builder import GraphData
from mickey_graph.models import Edge, EdgeType, Node, NodeKind
from mickey_graph.renderer import (
    PLACEHOLDER_DATA,
    PLACEHOLDER_TITLE,
    PLACEHOLDER_VIS,
    VENDOR_PATH,
    graph_to_dict,
    render_html,
    write_html,
)


@pytest.fixture
def sample_graph() -> GraphData:
    """최소 그래프: 2 nodes + 1 edge. 렌더링 검증용."""
    nodes = [
        Node(id="a", title="Node A", tags=["t1"], core="core a", kind=NodeKind.ENTRY),
        Node(id="b", title="Node B", tags=[], core="core b", kind=NodeKind.PATTERN),
    ]
    edges = [Edge(from_id="a", to_id="b", type=EdgeType.APPLIES_TO, reason="reason")]
    return GraphData(nodes=nodes, edges=edges)


# vendor 파일이 없으면 render_html 이 FileNotFoundError. setup_vendor.py 실행 전제.
vendor_ready = pytest.mark.skipif(
    not VENDOR_PATH.exists(),
    reason="vendor bundle missing - run `python scripts/setup_vendor.py`",
)


# --- 직렬화 ---

class TestGraphToDict:
    def test_serializes_nodes(self, sample_graph):
        d = graph_to_dict(sample_graph)
        assert len(d["nodes"]) == 2
        assert d["nodes"][0]["id"] == "a"
        # Enum → value 문자열
        assert d["nodes"][0]["kind"] == "entry"

    def test_serializes_edges_with_type_value(self, sample_graph):
        d = graph_to_dict(sample_graph)
        assert d["edges"][0]["type"] == "applies-to"
        assert d["edges"][0]["from_id"] == "a"

    def test_output_is_json_serializable(self, sample_graph):
        # 예외 발생하지 않아야 함
        json.dumps(graph_to_dict(sample_graph), ensure_ascii=False)

    def test_node_includes_degree_fields(self, sample_graph):
        """G3: JSON 노드에 in_degree/out_degree 필드 포함."""
        # sample_graph fixture 에는 degree dict 가 비어있으므로 기본 0
        # degree 를 채우려면 GraphData 에 명시적으로 넣거나 build 를 거쳐야 함
        sample_graph.in_degrees = {"a": 0, "b": 1}
        sample_graph.out_degrees = {"a": 1, "b": 0}
        d = graph_to_dict(sample_graph)
        node_a = next(n for n in d["nodes"] if n["id"] == "a")
        node_b = next(n for n in d["nodes"] if n["id"] == "b")
        assert node_a["out_degree"] == 1
        assert node_b["in_degree"] == 1
        assert node_a["in_degree"] == 0
        assert node_b["out_degree"] == 0


# --- 렌더링 ---

@vendor_ready
class TestRenderHtml:
    def test_all_placeholders_substituted(self, sample_graph):
        html = render_html(sample_graph, page_title="Test")
        assert PLACEHOLDER_VIS not in html
        assert PLACEHOLDER_DATA not in html
        assert PLACEHOLDER_TITLE not in html

    def test_contains_vis_network_library_signature(self, sample_graph):
        html = render_html(sample_graph, "Test")
        # vis-network UMD 번들의 특징: 'vis' 전역 노출
        assert "vis" in html
        # 실제 라이브러리 크기가 반영됨 (템플릿만 있는 경우와 구분)
        assert len(html) > 100_000

    def test_contains_graph_data(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert '"id":"a"' in html or '"id": "a"' in html
        assert '"kind":"entry"' in html or '"kind": "entry"' in html

    def test_contains_search_ui(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'id="search"' in html

    def test_page_title_substituted(self, sample_graph):
        html = render_html(sample_graph, page_title="MyScope")
        assert "MyScope" in html


# --- 파일 쓰기 ---

@vendor_ready
class TestWriteHtml:
    def test_writes_file_and_returns_size(self, sample_graph, tmp_path):
        html = render_html(sample_graph, "Test")
        out = tmp_path / "out.html"
        size = write_html(html, out)
        assert out.exists()
        assert size > 100  # 최소 유효 크기
        assert size == out.stat().st_size

    def test_creates_missing_parent_directory(self, sample_graph, tmp_path):
        html = render_html(sample_graph, "Test")
        out = tmp_path / "nested" / "deep" / "out.html"
        write_html(html, out)
        assert out.exists()


# --- Phase 3 UI: 태그 chip / kind·edge 체크박스 / 이웃 강조 ---

@vendor_ready
class TestPhase3FilterBar:
    """Phase 3 확장 UI 회귀 방지 — 필터 바 DOM 요소 + JS 로직."""

    def test_contains_filter_bar_section(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'id="filter-bar"' in html

    def test_contains_tag_filter_container(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'id="tag-filter"' in html
        # 태그 All/None 버튼
        assert 'id="tag-all"' in html
        assert 'id="tag-none"' in html

    def test_contains_kind_filter_container(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'id="kind-filter"' in html

    def test_contains_edge_type_filter_container(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'id="edge-type-filter"' in html


@vendor_ready
class TestPhase3JsLogic:
    """Phase 3 JS 로직 — 함수 정의 + 필터 상태 객체가 렌더 HTML에 포함."""

    def test_filter_state_defined(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'filterState' in html
        # white-list 방식임을 나타내는 세트 필드
        assert 'activeTags' in html
        assert 'activeKinds' in html
        assert 'activeEdgeTypes' in html

    def test_filter_pass_functions_defined(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'passesTagFilter' in html
        assert 'passesKindFilter' in html
        assert 'passesEdgeTypeFilter' in html

    def test_render_functions_defined(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'renderTagChips' in html
        assert 'renderKindChecks' in html
        assert 'renderEdgeTypeChecks' in html

    def test_neighbor_highlight_functions_defined(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'highlightNeighbors' in html
        assert 'clearNeighborHighlight' in html
        assert 'computeNeighborSet' in html


@vendor_ready
class TestPhase3TagSingletonToggle:
    """B 개선 회귀 방지 — 다태그 데이터셋에서 chip 목록을 count>=2 로 접기 + Show all 토글."""

    def test_tag_min_count_constant_defined(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'TAG_MIN_COUNT' in html

    def test_show_all_tags_state_field(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'showAllTags' in html

    def test_show_all_button_present(self, sample_graph):
        html = render_html(sample_graph, "Test")
        assert 'id="tag-show-all"' in html

    def test_chip_container_has_scroll_style(self, sample_graph):
        """B 개선: chip-container 는 max-height + overflow-y 로 스크롤."""
        html = render_html(sample_graph, "Test")
        assert '.chip-container' in html
        assert 'max-height' in html
        assert 'overflow-y' in html
