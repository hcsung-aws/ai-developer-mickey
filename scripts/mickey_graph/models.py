"""도메인 모델 - Node, Edge, NodeKind, EdgeType.

Mickey 지식 그래프의 순수 데이터 구조. 외부 의존성 없이 표준 라이브러리만 사용.
파서/빌더/렌더러가 공유하는 최소 인터페이스이며, 변경 시 각 계층 영향도 검토 필요.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class NodeKind(str, Enum):
    """노드 유형. 시각화 색상 매핑의 기준이 된다."""
    ENTRY = "entry"                   # 글로벌 domain/entries/ 항목
    PATTERN = "pattern"               # 글로벌 patterns/ 활성 항목
    GRADUATED = "graduated"           # patterns Graduated 표에 속한 항목
    PROJECT_KNOWLEDGE = "project_knowledge"  # 프로젝트 common_knowledge/context_rule/auto_notes
    UNKNOWN = "unknown"               # dangling edge 참조로만 존재하는 노드


class EdgeType(str, Enum):
    """엣지 유형. 시각화에서 색상/스타일 구분 기준."""
    APPLIES_TO = "applies-to"
    EXTENDS = "extends"
    SIMILAR_TO = "similar-to"
    PREREQUISITE = "prerequisite"
    CROSS_SCOPE = "cross-scope"       # 프로젝트 지식 → 글로벌 domain entry backlink
    MEMBER_OF = "member-of"           # 하위 카테고리 entry → anchor 노드 소속 (builder가 파일 위치에서 합성)
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(cls, raw: str) -> "EdgeType":
        """md 표 원본 값(예: 'applies-to', 'Applies To')을 안전 변환.

        정규화 규칙: strip → lower → 공백을 '-' 로 치환.
        일치 항목 없으면 UNKNOWN 반환 (파서는 raise 하지 않음).
        """
        normalized = raw.strip().lower().replace(" ", "-")
        for member in cls:
            if member.value == normalized:
                return member
        return cls.UNKNOWN


@dataclass
class Node:
    """지식 그래프 노드.

    Attributes:
        id: 고유 식별자 (md 표의 ID 컬럼 또는 파일명 slug).
        title: 표시용 제목.
        tags: 태그 리스트 (중복 제거).
        core: 한 줄 요약 (호버/상세 패널 표시용).
        kind: 노드 유형.
        source: 원본 md 파일 경로 (디버깅 및 링크용, 선택).
        subkind: PROJECT_KNOWLEDGE 내부 세분화 ('knowledge'/'rule'/'note'/'').
                 시각화에서 shape 매핑에만 사용. 다른 kind 에서는 빈 문자열.
    """
    id: str
    title: str
    tags: list[str] = field(default_factory=list)
    core: str = ""
    kind: NodeKind = NodeKind.UNKNOWN
    source: str = ""
    subkind: str = ""

    def merge_tags(self, extra: list[str]) -> None:
        """중복 노드 발견 시 태그를 union. 순서 보존 + 중복 제거."""
        seen = set(self.tags)
        for tag in extra:
            if tag not in seen:
                self.tags.append(tag)
                seen.add(tag)


@dataclass
class Edge:
    """지식 그래프 엣지.

    Attributes:
        from_id: 출발 노드 ID.
        to_id: 도착 노드 ID.
        type: 관계 유형.
        reason: 관계 설명 (호버 텍스트).
    """
    from_id: str
    to_id: str
    type: EdgeType
    reason: str = ""
