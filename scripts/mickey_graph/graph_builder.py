"""Graph Builder - scope 별 그래프 구성.

파서 계층이 raw md → Node/Edge 를 반환하면, 이 계층은:
    1. 여러 소스(GRAPH.md, patterns/INDEX.md, 프로젝트 INDEX 등)를 통합
    2. 노드 ID 정합성 검증 (dangling edge → UNKNOWN 노드 자동 추가)
    3. 통계 집계 (kind 분포, 노드/엣지 수)

Phase 1: 글로벌 스코프만 구현.
Phase 2 에서 project scope 추가 예정 (프로젝트 INDEX + Domain Links backlink).
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .models import Edge, EdgeType, Node, NodeKind
from .parser import (
    extract_body_domain_references,
    load_graph_file,
    parse_domain_links,
    parse_edges_from_graph,
    parse_graduated_absorption_edges,
    parse_nodes_from_graph,
    parse_patterns_index,
    parse_project_knowledge_map,
    parse_project_note_map,
    parse_project_rule_map,
)

logger = logging.getLogger(__name__)


# --- 데이터 클래스 ---

@dataclass
class GraphData:
    """빌더가 산출하는 통합 그래프.

    nodes: 중복 제거된 노드 목록 (id 기준 unique).
    edges: 원본 순서 유지된 엣지 목록.
    in_degrees: 노드 id → 받은 엣지 수 (참조된 횟수).
    out_degrees: 노드 id → 나가는 엣지 수 (허브 강도).
    backlinked_entry_ids: 프로젝트가 Domain Links 로 참조한 글로벌 entry ID 집합
                         (프로젝트 스코프에서만 채워짐. 뷰 필터/강조용).
    project_node_ids: 프로젝트 지식 노드 ID 집합 (뷰 필터용).
    """
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    in_degrees: dict[str, int] = field(default_factory=dict)
    out_degrees: dict[str, int] = field(default_factory=dict)
    backlinked_entry_ids: set[str] = field(default_factory=set)
    project_node_ids: set[str] = field(default_factory=set)


@dataclass
class GraphBuildStats:
    """빌드 결과 통계. CLI/로그 표시용."""
    node_count: int
    edge_count: int
    dangling_edges_promoted: int   # dangling → UNKNOWN 노드로 자동 승격된 수
    kind_distribution: dict[str, int]


# --- 글로벌 스코프 빌더 ---

def build_global_graph(mickey_root: Path) -> tuple[GraphData, GraphBuildStats]:
    """글로벌 지식 그래프 구성.

    입력 소스:
        <mickey_root>/domain/GRAPH.md   → NodeKind.ENTRY + edges
        <mickey_root>/patterns/INDEX.md → NodeKind.PATTERN + NodeKind.GRADUATED

    정합성:
        엣지가 참조하는 노드 ID 가 노드 목록에 없으면 NodeKind.UNKNOWN 으로 자동 추가.
        참조를 끊는 대신 시각화에서 보이도록 두어 사용자가 원인 판단 가능.

    Args:
        mickey_root: ~/.kiro/mickey/ 절대 경로.

    Returns:
        (GraphData, GraphBuildStats)
    """
    graph_file = mickey_root / "domain" / "GRAPH.md"
    patterns_file = mickey_root / "patterns" / "INDEX.md"

    nodes: list[Node] = []
    edges: list[Edge] = []

    if graph_file.exists():
        text = load_graph_file(graph_file)
        nodes.extend(parse_nodes_from_graph(text, source=str(graph_file)))
        edges.extend(parse_edges_from_graph(text))
    else:
        logger.warning("graph file not found: %s", graph_file)

    # 하위 카테고리 GRAPH (extended-protocols §20 Step 3):
    # domain/entries/{category}/GRAPH.md 를 재귀 스캔하여 상위 그래프에 병합.
    # 상위에는 anchor 행만 남으므로, 하위 노드를 로딩해야 cross-category 엣지가 dangling 되지 않는다.
    # 또한 §20의 membership(파일 위치 = 카테고리 소속)은 md에 엣지로 존재하지 않으므로,
    # 시각화에서 계층이 보이도록 "하위 entry → anchor" member-of 엣지를 여기서 합성한다 (M39).
    for sub_graph_file in sorted((mickey_root / "domain" / "entries").rglob("GRAPH.md")):
        text = load_graph_file(sub_graph_file)
        sub_nodes = parse_nodes_from_graph(text, source=str(sub_graph_file))
        nodes.extend(sub_nodes)
        edges.extend(parse_edges_from_graph(text))
        # anchor ID = 카테고리 디렉토리명 (상위 GRAPH의 anchor 행 ID와 §20 규약상 일치)
        anchor_id = sub_graph_file.parent.name
        edges.extend(
            Edge(
                from_id=n.id,
                to_id=anchor_id,
                type=EdgeType.MEMBER_OF,
                reason=f"entries/{anchor_id}/ 소속 (builder 합성)",
            )
            for n in sub_nodes
            if n.id != anchor_id  # anchor 자기 참조 방지
        )

    if patterns_file.exists():
        text = load_graph_file(patterns_file)
        active, graduated = parse_patterns_index(text, source=str(patterns_file))
        nodes.extend(active)
        nodes.extend(graduated)
        # G1: Graduated → 흡수 entry EXTENDS 엣지 자동 생성 (외곽 표류 방지)
        edges.extend(parse_graduated_absorption_edges(text))
    else:
        logger.warning("patterns file not found: %s", patterns_file)

    # 중복 노드 제거 (예: patterns 표에 있는 것이 GRAPH.md 노드와 겹치는 경우)
    # 우선순위: ENTRY > PATTERN > GRADUATED (GRAPH.md 를 진실 소스로 취급)
    nodes = _dedupe_nodes_by_id_prefer_entry(nodes)

    # dangling edge 처리 - 없는 참조를 UNKNOWN 노드로 승격
    node_ids = {n.id for n in nodes}
    dangling_ids: set[str] = set()
    for e in edges:
        if e.from_id not in node_ids:
            dangling_ids.add(e.from_id)
        if e.to_id not in node_ids:
            dangling_ids.add(e.to_id)

    for dangling_id in dangling_ids:
        logger.warning("Promoting dangling reference to UNKNOWN node: %s", dangling_id)
        nodes.append(Node(
            id=dangling_id,
            title=dangling_id,
            tags=[],
            core="(referenced by edge but not defined)",
            kind=NodeKind.UNKNOWN,
            source="",
        ))

    stats = GraphBuildStats(
        node_count=len(nodes),
        edge_count=len(edges),
        dangling_edges_promoted=len(dangling_ids),
        kind_distribution=_count_kinds(nodes),
    )

    # G3: degree 계산 (시각화에서 노드 크기/border/라벨 결정에 사용)
    in_deg, out_deg = _compute_degrees(nodes, edges)

    return GraphData(
        nodes=nodes,
        edges=edges,
        in_degrees=in_deg,
        out_degrees=out_deg,
    ), stats


# --- 헬퍼 ---

def _compute_degrees(nodes: list[Node], edges: list[Edge]) -> tuple[dict[str, int], dict[str, int]]:
    """각 노드의 in-degree / out-degree 계산.

    in_degree: 노드로 향하는 엣지 수 → 참조 많이 받는 정도 (실제 활용도).
    out_degree: 노드에서 나가는 엣지 수 → 다른 지식으로의 관문 (탐색 시작점).
    """
    in_deg: dict[str, int] = {n.id: 0 for n in nodes}
    out_deg: dict[str, int] = {n.id: 0 for n in nodes}
    for e in edges:
        if e.from_id in out_deg:
            out_deg[e.from_id] += 1
        if e.to_id in in_deg:
            in_deg[e.to_id] += 1
    return in_deg, out_deg


# --- 프로젝트 스코프 빌더 (Phase 2) ---

def build_project_graph(
    project_root: Path,
    mickey_root: Path,
) -> tuple[GraphData, GraphBuildStats]:
    """프로젝트 지식 그래프 구성.

    입력 소스:
        <project_root>/common_knowledge/INDEX.md → Knowledge Map + Domain Links
        <project_root>/context_rule/INDEX.md → Rule Map
        <project_root>/auto_notes/NOTES.md → Note Map
        <mickey_root>/domain/GRAPH.md + patterns/INDEX.md → 전체 글로벌 그래프

    CROSS_SCOPE 엣지 생성 규칙:
        Domain Links 키워드 ↔ 프로젝트 노드 태그 자동 매칭.
        교집합이 있으면 (매칭된 프로젝트 노드) → (backlink entry) EdgeType.CROSS_SCOPE.
        매칭 안 되어도 backlink entry 는 backlinked_entry_ids 집합에 기록 (뷰 강조용).

    Args:
        project_root: 대상 프로젝트 루트 절대 경로.
        mickey_root: ~/.kiro/mickey/ 절대 경로 (글로벌 데이터 로드용).

    Returns:
        (GraphData, GraphBuildStats)
    """
    # 1. 전체 글로벌 그래프 로드 (기존 재사용)
    global_graph, _ = build_global_graph(mickey_root)

    project_nodes: list[Node] = []
    cross_scope_edges: list[Edge] = []
    backlinked_ids: set[str] = set()

    # 2. 프로젝트 3개 INDEX 로드
    for filename, subdir, parse_fn in [
        ("INDEX.md", "common_knowledge", parse_project_knowledge_map),
        ("INDEX.md", "context_rule", parse_project_rule_map),
        ("NOTES.md", "auto_notes", parse_project_note_map),
    ]:
        path = project_root / subdir / filename
        if not path.exists():
            logger.warning("project index missing: %s", path)
            continue
        text = load_graph_file(path)
        project_nodes.extend(parse_fn(text, source=str(path)))

    # 3. Domain Links → CROSS_SCOPE 엣지 (프로젝트 태그 매칭 기반) + backlink 기록
    common_index = project_root / "common_knowledge" / "INDEX.md"

    # 프로젝트 노드 → 매칭된 backlink target 집합 (자동 SIMILAR_TO 엣지 산출용)
    project_to_backlinks: dict[str, set[str]] = {n.id: set() for n in project_nodes}

    if common_index.exists():
        text = load_graph_file(common_index)
        domain_links = parse_domain_links(text)
        for link in domain_links:
            backlinked_ids.add(link.entry_id)
            matched_projects = _match_project_nodes_by_keywords(project_nodes, link.keywords)
            for proj_node in matched_projects:
                project_to_backlinks[proj_node.id].add(link.entry_id)
                cross_scope_edges.append(Edge(
                    from_id=proj_node.id,
                    to_id=link.entry_id,
                    type=EdgeType.CROSS_SCOPE,
                    reason=f"domain link: {link.hint or ', '.join(link.keywords)}",
                ))

    # 3-b. 프로젝트 파일 본문에서 domain entry 참조 추출 → CROSS_SCOPE 엣지 추가
    # (INDEX Domain Links 표에는 없지만 파일 본문 `## Related` / "교차 참조" 문구로 명시된 관계)
    subkind_to_subdir = {
        "knowledge": "common_knowledge",
        "rule": "context_rule",
        "note": "auto_notes",
    }
    existing_edges: set[tuple[str, str]] = {
        (e.from_id, e.to_id) for e in cross_scope_edges
    }
    index_link_targets_by_node: dict[str, set[str]] = {}   # 노드 → INDEX Domain Links 로 이미 잡힌 targets
    for e in cross_scope_edges:
        index_link_targets_by_node.setdefault(e.from_id, set()).add(e.to_id)

    body_only_matches: list[tuple[str, list[str]]] = []   # 진단용: (파일, INDEX에 없는 참조들)

    for node in project_nodes:
        subdir = subkind_to_subdir.get(node.subkind)
        if not subdir:
            continue
        # 노드 ID 형식 "pX:<file_stem>" 에서 파일명 복원
        _, _, file_stem = node.id.partition(":")
        if not file_stem:
            continue
        file_path = project_root / subdir / f"{file_stem}.md"
        if not file_path.exists():
            continue

        body = load_graph_file(file_path)
        body_refs = extract_body_domain_references(body)
        if not body_refs:
            continue

        new_targets_for_node: list[str] = []
        for entry_id in body_refs:
            backlinked_ids.add(entry_id)
            key = (node.id, entry_id)
            if key in existing_edges:
                continue
            existing_edges.add(key)
            project_to_backlinks[node.id].add(entry_id)
            cross_scope_edges.append(Edge(
                from_id=node.id,
                to_id=entry_id,
                type=EdgeType.CROSS_SCOPE,
                reason="body reference (## Related / 교차 참조)",
            ))
            if entry_id not in index_link_targets_by_node.get(node.id, set()):
                new_targets_for_node.append(entry_id)

        if new_targets_for_node:
            body_only_matches.append((str(file_path.name), new_targets_for_node))

    # 진단 로그: INDEX 에 없지만 본문에 있는 참조들
    if body_only_matches:
        logger.warning(
            "INDEX Domain Links out-of-sync — %d files have body refs missing from INDEX:",
            len(body_only_matches),
        )
        for fname, targets in body_only_matches:
            logger.warning("  %s: %s", fname, ", ".join(targets))

    # 3-c. 프로젝트 노드 간 SIMILAR_TO 자동 엣지 (같은 backlink 공유) - 재계산
    project_similar_edges = _build_project_similar_edges(project_to_backlinks)

    # 4. 통합
    all_nodes = list(global_graph.nodes) + project_nodes
    all_edges = list(global_graph.edges) + cross_scope_edges + project_similar_edges

    # backlink 대상이 글로벌 그래프에 없으면 UNKNOWN 노드로 승격 (매칭 여부와 무관)
    # → 프로젝트 뷰에서 backlink 대상을 항상 표시하기 위함
    node_ids = {n.id for n in all_nodes}
    for entry_id in backlinked_ids:
        if entry_id not in node_ids:
            logger.warning("Backlink target not in global graph: %s", entry_id)
            all_nodes.append(Node(
                id=entry_id,
                title=entry_id,
                tags=[],
                core="(backlink target not defined in GRAPH.md)",
                kind=NodeKind.UNKNOWN,
                source="",
            ))
            node_ids.add(entry_id)

    in_deg, out_deg = _compute_degrees(all_nodes, all_edges)

    stats = GraphBuildStats(
        node_count=len(all_nodes),
        edge_count=len(all_edges),
        dangling_edges_promoted=0,   # 프로젝트 빌드는 dangling 처리를 이미 포함
        kind_distribution=_count_kinds(all_nodes),
    )

    return GraphData(
        nodes=all_nodes,
        edges=all_edges,
        in_degrees=in_deg,
        out_degrees=out_deg,
        backlinked_entry_ids=backlinked_ids,
        project_node_ids={n.id for n in project_nodes},
    ), stats


def _match_project_nodes_by_keywords(
    project_nodes: list[Node],
    keywords: list[str],
) -> list[Node]:
    """Domain Links 키워드와 프로젝트 노드 태그의 부분 문자열 매칭.

    정확 일치 대신 부분 문자열(substring, 양방향) + 정규화(lowercase strip) 사용.
    이유: 프로젝트 트리거는 여러 어구를 담고 있고 Domain Links 키워드는 짧은 단어라
    정확 일치는 매우 드물다. 부분 일치가 자연스러운 매칭을 만든다.

    매칭 규칙 (하나라도 성립 시 매칭):
        - keyword 가 project tag 에 substring 포함
        - project tag 가 keyword 에 substring 포함

    빈 문자열은 무시.
    """
    normalized_keywords = [k.lower().strip() for k in keywords if k.strip()]
    if not normalized_keywords:
        return []

    matched: list[Node] = []
    for node in project_nodes:
        node_tags = [t.lower().strip() for t in node.tags if t.strip()]
        if _has_substring_match(node_tags, normalized_keywords):
            matched.append(node)
    return matched


def _has_substring_match(tags: list[str], keywords: list[str]) -> bool:
    """어느 태그와 어느 키워드가 서로 부분 문자열 포함 관계인지 검사."""
    for t in tags:
        for k in keywords:
            if k in t or t in k:
                return True
    return False


def _build_project_similar_edges(project_to_backlinks: dict[str, set[str]]) -> list[Edge]:
    """프로젝트 노드 간 자동 SIMILAR_TO 엣지 생성.

    두 프로젝트 노드가 같은 backlink target(글로벌 domain entry) 을 공유하면
    관련성이 있다고 판단하여 SIMILAR_TO 엣지 자동 생성.

    - 같은 backlink 대상을 여러 개 공유해도 엣지는 1개 (reason 에 개수 명시)
    - 무향 관계지만 vis-network 렌더 위해 단방향으로 표기
    - self-loop 방지 위해 i < j 조합만
    """
    edges: list[Edge] = []
    node_ids = list(project_to_backlinks.keys())
    for i in range(len(node_ids)):
        for j in range(i + 1, len(node_ids)):
            a, b = node_ids[i], node_ids[j]
            shared = project_to_backlinks[a] & project_to_backlinks[b]
            if shared:
                edges.append(Edge(
                    from_id=a,
                    to_id=b,
                    type=EdgeType.SIMILAR_TO,
                    reason=f"shared backlinks ({len(shared)}): {', '.join(sorted(shared))}",
                ))
    return edges

_KIND_PRIORITY: dict[NodeKind, int] = {
    NodeKind.ENTRY: 0,
    NodeKind.PATTERN: 1,
    NodeKind.GRADUATED: 2,
    NodeKind.PROJECT_KNOWLEDGE: 3,
    NodeKind.UNKNOWN: 4,
}


def _dedupe_nodes_by_id_prefer_entry(nodes: list[Node]) -> list[Node]:
    """같은 ID 노드가 여러 kind 로 등장하면 우선순위 낮은 kind 승자.

    예: 'welc-test-harness' 가 GRAPH.md(ENTRY) 와 patterns/INDEX.md(GRADUATED) 양쪽에 있으면
    ENTRY 를 유지 (더 상세 정보 보유).
    """
    by_id: dict[str, Node] = {}
    for node in nodes:
        existing = by_id.get(node.id)
        if existing is None:
            by_id[node.id] = node
            continue

        if _KIND_PRIORITY[node.kind] < _KIND_PRIORITY[existing.kind]:
            # 새 노드가 더 우선순위 높음 → 태그 union 후 교체
            node.merge_tags(existing.tags)
            by_id[node.id] = node
        else:
            # 기존 노드 유지 + 태그 union
            existing.merge_tags(node.tags)

    return list(by_id.values())


def _count_kinds(nodes: list[Node]) -> dict[str, int]:
    """kind 별 노드 수 집계 (Enum value 를 문자열 키로)."""
    counter: Counter[str] = Counter(n.kind.value for n in nodes)
    return dict(counter)
