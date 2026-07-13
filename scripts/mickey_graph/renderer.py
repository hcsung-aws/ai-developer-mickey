"""HTML Renderer - 템플릿에 vendor JS + 그래프 JSON 을 인라인 삽입.

의존성 최소화를 위해 Jinja2 등 템플릿 엔진 대신 placeholder 치환 사용.
결과 HTML 은 완전 self-contained (인터넷 접속 불필요).

Placeholders:
    __VIS_NETWORK_JS__   → vendor/vis-network.min.js 내용
    __GRAPH_DATA_JSON__  → GraphData 를 JSON 직렬화한 문자열
    __PAGE_TITLE__       → 헤더 표시용 스코프 라벨 (예: 'global')
"""

from __future__ import annotations

import json
from pathlib import Path

from .graph_builder import GraphData
from .models import Edge, Node

# --- 경로/상수 ---

_PACKAGE_ROOT = Path(__file__).parent
TEMPLATE_PATH = _PACKAGE_ROOT / "templates" / "graph.html.tmpl"
VENDOR_PATH = _PACKAGE_ROOT / "vendor" / "vis-network.min.js"

PLACEHOLDER_VIS = "__VIS_NETWORK_JS__"
PLACEHOLDER_DATA = "__GRAPH_DATA_JSON__"
PLACEHOLDER_TITLE = "__PAGE_TITLE__"


# --- 공개 API ---

def render_html(graph: GraphData, page_title: str) -> str:
    """GraphData 를 완전 self-contained HTML 문자열로 렌더링.

    vendor JS 가 존재하지 않으면 FileNotFoundError. setup_vendor.py 최초 실행 필요.
    """
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    if not VENDOR_PATH.exists():
        raise FileNotFoundError(
            f"vendor bundle missing: {VENDOR_PATH}. "
            "Run `python scripts/setup_vendor.py` first."
        )
    vendor_js = VENDOR_PATH.read_text(encoding="utf-8")
    data_json = json.dumps(graph_to_dict(graph), ensure_ascii=False)

    # Placeholder 순서: title → vendor → data (vendor 텍스트가 매우 크므로 나중)
    html = template.replace(PLACEHOLDER_TITLE, page_title)
    html = html.replace(PLACEHOLDER_VIS, vendor_js)
    html = html.replace(PLACEHOLDER_DATA, data_json)
    return html


def write_html(html: str, output_path: Path) -> int:
    """HTML 문자열을 파일로 저장. 부모 디렉토리 자동 생성. 파일 크기(bytes) 반환."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path.stat().st_size


# --- 직렬화 헬퍼 ---

def graph_to_dict(graph: GraphData) -> dict:
    """GraphData → JSON 직렬화 가능한 dict.

    dataclass asdict 대신 명시적 변환 (Enum → value, degree 및 flag 병합).
    """
    return {
        "nodes": [
            _node_to_dict(
                n,
                in_deg=graph.in_degrees.get(n.id, 0),
                out_deg=graph.out_degrees.get(n.id, 0),
                is_project=n.id in graph.project_node_ids,
                is_backlinked=n.id in graph.backlinked_entry_ids,
            )
            for n in graph.nodes
        ],
        "edges": [_edge_to_dict(e) for e in graph.edges],
    }


def _node_to_dict(
    node: Node,
    in_deg: int = 0,
    out_deg: int = 0,
    is_project: bool = False,
    is_backlinked: bool = False,
) -> dict:
    return {
        "id": node.id,
        "title": node.title,
        "tags": list(node.tags),
        "core": node.core,
        "kind": node.kind.value,
        "subkind": node.subkind,
        "source": node.source,
        "in_degree": in_deg,
        "out_degree": out_deg,
        "is_project": is_project,
        "is_backlinked": is_backlinked,
    }


def _edge_to_dict(edge: Edge) -> dict:
    return {
        "from_id": edge.from_id,
        "to_id": edge.to_id,
        "type": edge.type.value,
        "reason": edge.reason,
    }
