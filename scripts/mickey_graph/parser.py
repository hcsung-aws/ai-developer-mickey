"""Markdown 표 파서 - md 파일에서 Node/Edge 원자 데이터 추출.

지원 파일:
- ~/.kiro/mickey/domain/GRAPH.md (## Nodes, ## Edges)
- ~/.kiro/mickey/patterns/INDEX.md (## Pattern Map, ## Graduated Patterns)

이 모듈은 파싱만 담당한다. 정합성 검증(dangling edge, 스코프 결합)은
graph_builder 계층의 책임이므로 여기서는 raw 추출에 집중한다.

중복 노드 처리:
- 같은 ID가 여러 번 등장하면 첫 번째 등장 노드를 유지하고 태그만 union
- 그 외 필드(title, core)는 첫 번째 값 보존
- WARNING 로그 남김 (호출자가 caplog 로 검증 가능)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

from .models import Edge, EdgeType, Node, NodeKind

logger = logging.getLogger(__name__)


# --- md 표 저수준 파싱 ---

# 표 행: | ... | (양쪽에 최소 하나의 |)
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
# 헤더-데이터 구분선: |---|---|
_TABLE_SEPARATOR_RE = re.compile(r"^\|[\s\-:|]+\|\s*$")


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    """섹션 텍스트의 표(들)을 파싱하여 list of dict 반환.

    설계 요점:
        - 같은 논리적 표를 빈 줄로 여러 블록으로 나눠도 하나로 병합
          (실제 GRAPH.md 처럼 시각적 편의로 분리한 경우 지원)
        - 헤더 라인 여부는 lookahead 로 판정 (다음 라인이 |---|---| 구분선)
        - 첫 표 종료 이후 등장하는 다른 표는 무시 (섹션당 하나의 논리적 표 가정)
        - 빈 셀은 빈 문자열, 헤더 케이스는 원본 유지

    Args:
        text: md 섹션 텍스트.

    Returns:
        데이터 행 목록. 표가 없으면 빈 리스트.
    """
    lines = text.splitlines()
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    in_table = False

    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip()

        # 빈 줄: 표 안팎 상관없이 대기 (표 블록 사이 gap 허용)
        if not stripped:
            i += 1
            continue

        row_match = _TABLE_ROW_RE.match(stripped)
        if not row_match:
            # non-row + non-empty 라인
            if in_table:
                break  # 표 종료 신호
            i += 1
            continue

        # 구분선 자체는 헤더가 앞서 처리했어야 함 → 여기서 만나면 스킵
        if _TABLE_SEPARATOR_RE.match(stripped):
            i += 1
            continue

        # 다음 라인이 구분선이면 이 라인은 헤더
        next_line = lines[i + 1].rstrip() if i + 1 < len(lines) else ""
        is_header_line = bool(_TABLE_SEPARATOR_RE.match(next_line))

        cells = [c.strip() for c in row_match.group(1).split("|")]

        if is_header_line:
            # 첫 헤더면 확정, 이후 재등장 헤더는 스킵 (여러 블록 병합)
            if header is None:
                header = cells
                in_table = True
            i += 2  # 헤더 + 구분선 스킵
            continue

        if header is None:
            # 헤더 없이 데이터 만난 케이스 (비정형) → 무시
            i += 1
            continue

        row = {h: (cells[j] if j < len(cells) else "") for j, h in enumerate(header)}
        rows.append(row)
        i += 1

    return rows


def extract_section(text: str, heading: str, heading_level: int = 2) -> str:
    """지정 heading 아래의 섹션 텍스트 추출.

    Args:
        text: md 전체 텍스트.
        heading: '## Nodes' 의 'Nodes' 부분 (heading 이름).
        heading_level: 2 → '## Nodes'. 다음 동일/상위 level heading 앞까지가 섹션.

    Returns:
        해당 섹션 텍스트. heading 없으면 빈 문자열.
    """
    prefix = "#" * heading_level + " "
    heading_line = prefix + heading

    lines = text.splitlines()
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == heading_line:
            start = i + 1
            break

    if start == -1:
        return ""

    # 다음 heading 앞까지 (동일 또는 상위 level)
    stop_re = re.compile(r"^#{1," + str(heading_level) + r"}\s")
    end = len(lines)
    for i in range(start, len(lines)):
        if stop_re.match(lines[i]):
            end = i
            break

    return "\n".join(lines[start:end])


# --- 태그/문자열 헬퍼 ---

def parse_tags(raw: str) -> list[str]:
    """콤마 구분 태그 문자열을 리스트로 변환. 빈 태그 제거 + strip."""
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


# --- 고수준 파서: GRAPH.md ---

def parse_nodes_from_graph(text: str, source: str = "") -> list[Node]:
    """GRAPH.md 의 `## Nodes` 표를 파싱하여 Node 리스트 반환.

    중복 ID: 첫 번째 등장 노드 유지 + 이후 태그를 union. WARNING 로그.
    모든 노드는 NodeKind.ENTRY 로 태깅 (glob domain entry 기본값).
    """
    section = extract_section(text, "Nodes")
    rows = parse_markdown_table(section)

    by_id: dict[str, Node] = {}
    for row in rows:
        node_id = row.get("ID", "").strip()
        if not node_id:
            continue

        title = row.get("Title", "").strip()
        tags = parse_tags(row.get("Tags", ""))
        core = row.get("Core", "").strip()

        if node_id in by_id:
            logger.warning("Duplicate node id: %s (merging tags)", node_id)
            by_id[node_id].merge_tags(tags)
            continue

        by_id[node_id] = Node(
            id=node_id,
            title=title,
            tags=tags,
            core=core,
            kind=NodeKind.ENTRY,
            source=source,
        )

    return list(by_id.values())


def parse_edges_from_graph(text: str) -> list[Edge]:
    """GRAPH.md 의 `## Edges` 표를 파싱하여 Edge 리스트 반환.

    - From/To 가 비어 있으면 스킵
    - 알 수 없는 Type 은 EdgeType.UNKNOWN 으로 강등
    - 정합성 검증(노드 존재 여부)은 이 계층에서 수행하지 않음 → graph_builder 담당
    """
    section = extract_section(text, "Edges")
    rows = parse_markdown_table(section)

    edges: list[Edge] = []
    for row in rows:
        from_id = row.get("From", "").strip()
        to_id = row.get("To", "").strip()
        raw_type = row.get("Type", "").strip()
        reason = row.get("Reason", "").strip()

        if not from_id or not to_id:
            continue

        edges.append(Edge(
            from_id=from_id,
            to_id=to_id,
            type=EdgeType.from_raw(raw_type),
            reason=reason,
        ))

    return edges


# --- 고수준 파서: patterns/INDEX.md ---

def parse_patterns_index(text: str, source: str = "") -> tuple[list[Node], list[Node]]:
    """patterns/INDEX.md 를 파싱하여 (active_patterns, graduated_patterns) 반환.

    - Active: `## Pattern Map` 표 → NodeKind.PATTERN
    - Graduated: `## Graduated Patterns` 표 → NodeKind.GRADUATED
    """
    active = _parse_pattern_map(
        extract_section(text, "Pattern Map"), source, NodeKind.PATTERN
    )
    graduated = _parse_pattern_map(
        extract_section(text, "Graduated Patterns"), source, NodeKind.GRADUATED
    )
    return active, graduated


# --- Graduated 흡수 엣지 추출 ---

# `domain/entries/foo.md`, `entries/foo.md`, 또는 백틱 감싸진 형태에서 entry ID 추출
_ENTRY_REF_RE = re.compile(r"(?:domain/)?entries/([\w\-]+)\.md")


def _extract_entry_references(text: str) -> list[str]:
    """텍스트에서 `entries/xxx.md` 형태의 참조 ID(파일명 stem) 추출.

    같은 텍스트에 여러 참조가 있으면 등장 순서대로 반환. 중복은 제거하지 않음
    (호출자가 필요 시 dedupe).
    """
    return _ENTRY_REF_RE.findall(text)


def extract_body_domain_references(text: str) -> list[str]:
    """프로젝트 지식 파일 본문에서 글로벌 domain entry 참조 ID 추출.

    프로젝트 지식 파일 (common_knowledge/, context_rule/, auto_notes/) 본문에는
    `## Related` 섹션이나 "교차 참조" 문구로 관련 글로벌 domain entry 를 참조하는
    관행이 있음. 이 함수는 파일 전체에서 그런 참조를 모두 추출.

    지원 패턴 (모두 정규식 매칭):
        - `~/.kiro/mickey/domain/entries/foo.md`
        - `domain/entries/foo.md`
        - `entries/foo.md`
        - 백틱 감싸진 경우 (`` `domain/entries/foo.md` ``)

    중복 제거 + 등장 순서 유지.
    """
    refs = _ENTRY_REF_RE.findall(text)
    seen: set[str] = set()
    result: list[str] = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            result.append(r)
    return result


def parse_graduated_absorption_edges(text: str) -> list[Edge]:
    """Graduated Patterns 표에서 흡수 관계 엣지 자동 생성.

    각 Graduated 행의 "흡수 위치" 컬럼(2번째)에서 `entries/xxx.md` 참조를 모두
    추출하여, 해당 graduated 노드에서 각 entry 로 EXTENDS 엣지 생성.

    - Graduated 노드 ID 는 _parse_pattern_map 과 동일한 규칙으로 슬러그
    - self-loop (from == to) 는 제외
    - 중복 (동일 from-to 쌍) 은 제외

    Args:
        text: patterns/INDEX.md 전체 텍스트.

    Returns:
        Graduated → entry EXTENDS 엣지 리스트.
    """
    section = extract_section(text, "Graduated Patterns")
    rows = parse_markdown_table(section)

    edges: list[Edge] = []
    seen: set[tuple[str, str]] = set()

    for row in rows:
        values = list(row.values())
        if len(values) < 2:
            continue

        name = values[0].strip()
        absorbed_into = values[1].strip()
        if not name or not absorbed_into:
            continue

        graduated_id = _slugify_pattern(name, absorbed_into)
        referenced_ids = _extract_entry_references(absorbed_into)

        for target_id in referenced_ids:
            if target_id == graduated_id:
                continue  # self-loop 제외
            key = (graduated_id, target_id)
            if key in seen:
                continue
            seen.add(key)
            edges.append(Edge(
                from_id=graduated_id,
                to_id=target_id,
                type=EdgeType.EXTENDS,
                reason="graduated absorbed into",
            ))

    return edges


def _parse_pattern_map(section: str, source: str, kind: NodeKind) -> list[Node]:
    """Pattern Map / Graduated Patterns 표를 Node 리스트로 변환.

    각 표의 컬럼 이름이 언어별로 다를 수 있으므로 위치 기반으로 접근:
        col[0] = 패턴 이름
        col[1] = 파일 경로 또는 흡수 위치
        col[2] = 요약 (선택)
    ID 는 파일명 slug 를 우선 사용, 없으면 이름 slug.
    """
    rows = parse_markdown_table(section)
    nodes: list[Node] = []
    seen: set[str] = set()

    for row in rows:
        values = list(row.values())
        if len(values) < 2:
            continue

        name = values[0].strip()
        file_or_location = values[1].strip()
        summary = values[2].strip() if len(values) >= 3 else ""

        if not name:
            continue

        node_id = _slugify_pattern(name, file_or_location)
        if node_id in seen:
            continue
        seen.add(node_id)

        nodes.append(Node(
            id=node_id,
            title=name,
            tags=[],
            core=summary,
            kind=kind,
            source=source,
        ))

    return nodes


def _slugify_pattern(name: str, file_ref: str) -> str:
    """패턴 이름 또는 파일 참조에서 안정적 ID 생성.

    - 파일 참조가 `*.md` 형태면 파일명(확장자 제거) 사용
    - 그 외 (예: '(INDEX 내 기술)') 는 이름을 slug 화
    """
    if file_ref and file_ref.endswith(".md"):
        return Path(file_ref).stem

    # 이름 slug: 알파벳/숫자/한글 유지, 그 외는 하이픈
    slug = re.sub(r"[^\w\-]+", "-", name.lower(), flags=re.UNICODE)
    return slug.strip("-") or "unknown"


# --- 파일 로더 ---

def load_graph_file(path: Path) -> str:
    """md 파일 텍스트 읽기. BOM 자동 제거 (utf-8-sig)."""
    return path.read_text(encoding="utf-8-sig")


# --- 프로젝트 스코프 파서 (Phase 2) ---

def parse_project_knowledge_map(text: str, source: str = "") -> list[Node]:
    """common_knowledge/INDEX.md 의 `## Knowledge Map` 표 → PROJECT_KNOWLEDGE 노드.

    각 행: | 트리거 | 파일 | 요약 |
    subkind='knowledge', ID='pk:<file_stem>'.
    """
    return _parse_project_index_map(
        extract_section(text, "Knowledge Map"),
        source=source,
        subkind="knowledge",
        id_prefix="pk",
        tags_from_first_column=True,
    )


def parse_project_rule_map(text: str, source: str = "") -> list[Node]:
    """context_rule/INDEX.md 의 `## Rule Map` 표 → PROJECT_KNOWLEDGE 노드 (subkind=rule).

    ID='pr:<file_stem>'.
    """
    return _parse_project_index_map(
        extract_section(text, "Rule Map"),
        source=source,
        subkind="rule",
        id_prefix="pr",
        tags_from_first_column=True,
    )


def parse_project_note_map(text: str, source: str = "") -> list[Node]:
    """auto_notes/NOTES.md 의 `## Note Map` 표 → PROJECT_KNOWLEDGE 노드 (subkind=note).

    첫 컬럼은 '카테고리' 라 콤마 분리 대신 단일 태그.
    ID='pn:<file_stem>'.
    """
    return _parse_project_index_map(
        extract_section(text, "Note Map"),
        source=source,
        subkind="note",
        id_prefix="pn",
        tags_from_first_column=False,
    )


def _parse_project_index_map(
    section: str,
    source: str,
    subkind: str,
    id_prefix: str,
    tags_from_first_column: bool,
) -> list[Node]:
    """프로젝트 INDEX 3종 파서 공통 로직.

    표 컬럼 위치:
        col[0] = 트리거 or 카테고리 (태그 원본)
        col[1] = 파일명 (`foo.md`)
        col[2] = 요약 (선택)
    """
    rows = parse_markdown_table(section)
    nodes: list[Node] = []
    seen_ids: set[str] = set()

    for row in rows:
        values = list(row.values())
        if len(values) < 2:
            continue

        trigger_or_category = values[0].strip()
        file_ref = values[1].strip()
        summary = values[2].strip() if len(values) >= 3 else ""

        if not file_ref.endswith(".md"):
            continue

        file_stem = Path(file_ref).stem
        if not file_stem:
            continue

        node_id = f"{id_prefix}:{file_stem}"
        if node_id in seen_ids:
            continue
        seen_ids.add(node_id)

        tags = (
            parse_tags(trigger_or_category)
            if tags_from_first_column
            else ([trigger_or_category] if trigger_or_category else [])
        )

        nodes.append(Node(
            id=node_id,
            title=file_stem,
            tags=tags,
            core=summary,
            kind=NodeKind.PROJECT_KNOWLEDGE,
            source=source,
            subkind=subkind,
        ))

    return nodes


@dataclass
class DomainLink:
    """Domain Links 표 한 행. 태그 매칭을 위한 원자 정보."""
    keywords: list[str]
    entry_id: str
    hint: str


def parse_domain_links(text: str) -> list["DomainLink"]:
    """common_knowledge/INDEX.md 의 `## Domain Links` 표 파싱.

    각 행: | 키워드 | Domain Entry | 힌트 |
    Domain Entry 는 `~/.kiro/mickey/domain/entries/foo.md` 등 경로 → 파일 stem 을 entry_id 로.
    """
    section = extract_section(text, "Domain Links")
    rows = parse_markdown_table(section)

    links: list[DomainLink] = []
    for row in rows:
        values = list(row.values())
        if len(values) < 2:
            continue

        keyword_raw = values[0].strip()
        entry_ref = values[1].strip()
        hint = values[2].strip() if len(values) >= 3 else ""

        keywords = parse_tags(keyword_raw)

        # entry_ref 에서 파일 stem 추출: 절대/상대 경로 모두 지원
        refs = _extract_entry_references(entry_ref)
        if refs:
            entry_id = refs[0]
        elif entry_ref.endswith(".md"):
            entry_id = Path(entry_ref).stem
        else:
            continue  # entry 참조 없음

        links.append(DomainLink(keywords=keywords, entry_id=entry_id, hint=hint))

    return links
