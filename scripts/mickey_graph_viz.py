"""Mickey Knowledge Graph Visualization - CLI 진입점.

사용법:
    # 글로벌 지식 그래프 (Phase 1)
    python scripts/mickey_graph_viz.py --scope global

    # 결과 자동 열기
    python scripts/mickey_graph_viz.py --scope global --open

    # 커스텀 mickey_root 지정 (테스트용)
    python scripts/mickey_graph_viz.py --scope global --mickey-root /path/to/mickey

Phase 1: --scope global 만 동작.
Phase 2: --scope project --project-path 지원 예정.
"""

from __future__ import annotations

import argparse
import logging
import sys
import webbrowser
from pathlib import Path

# 자기 자신의 부모 디렉토리(scripts/)를 sys.path 에 추가 → mickey_graph 임포트 가능
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from mickey_graph.graph_builder import build_global_graph, build_project_graph  # noqa: E402
from mickey_graph.renderer import render_html, write_html  # noqa: E402


def _ensure_stdout_utf8() -> None:
    """Windows cp949 환경에서 non-ASCII 출력 안전 (adaptive #8)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def _default_mickey_root() -> Path:
    """~/.kiro/mickey 절대 경로."""
    return Path.home() / ".kiro" / "mickey"


def _default_output(scope: str, project_name: str = "") -> Path:
    """기본 출력 경로: scripts/output/mickey-graph-<scope>[-<project>].html"""
    suffix = f"-{project_name}" if project_name else ""
    return _SCRIPTS_DIR / "output" / f"mickey-graph-{scope}{suffix}.html"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mickey 지식 그래프 시각화 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--scope", choices=("global", "project"), required=True,
        help="시각화 범위. global=~/.kiro/mickey/, project=지정 프로젝트+글로벌 통합",
    )
    parser.add_argument(
        "--project-path", type=Path, default=None,
        help="project 스코프에서 대상 프로젝트 루트 (Phase 2)",
    )
    parser.add_argument(
        "--output", type=Path, default=None,
        help="결과 HTML 저장 경로 (기본: scripts/output/mickey-graph-<scope>[-<name>].html)",
    )
    parser.add_argument(
        "--open", action="store_true", dest="auto_open",
        help="렌더 후 결과 파일을 기본 브라우저로 자동 열기",
    )
    parser.add_argument(
        "--mickey-root", type=Path, default=None,
        help="~/.kiro/mickey 대체 경로 (테스트/디버그용)",
    )
    return parser.parse_args(argv)


def run_global(mickey_root: Path, output: Path, auto_open: bool) -> int:
    """글로벌 스코프 실행: 빌드 → 렌더 → 파일 저장 → (옵션) 브라우저 열기."""
    print(f"[mickey_graph] scope=global mickey_root={mickey_root}")

    if not mickey_root.exists():
        print(f"[mickey_graph] ERROR: mickey_root 없음: {mickey_root}",
              file=sys.stderr)
        return 1

    graph, stats = build_global_graph(mickey_root)
    print(f"[mickey_graph] nodes={stats.node_count} edges={stats.edge_count} "
          f"dangling_promoted={stats.dangling_edges_promoted}")
    print(f"[mickey_graph] kind distribution: {stats.kind_distribution}")

    if stats.node_count == 0:
        print("[mickey_graph] WARN: 노드가 없음. GRAPH.md/patterns/INDEX.md 확인 필요",
              file=sys.stderr)

    html = render_html(graph, page_title="global")
    size = write_html(html, output)
    print(f"[mickey_graph] wrote {output} ({size:,} bytes)")

    if auto_open:
        uri = output.resolve().as_uri()
        print(f"[mickey_graph] opening: {uri}")
        webbrowser.open(uri)

    return 0


def run_project(project_root: Path, mickey_root: Path, output: Path, auto_open: bool) -> int:
    """프로젝트 스코프 실행: 프로젝트 지식 + 전체 글로벌 통합 렌더."""
    project_name = project_root.name
    print(f"[mickey_graph] scope=project project={project_root}")
    print(f"[mickey_graph] mickey_root={mickey_root}")

    if not project_root.exists():
        print(f"[mickey_graph] ERROR: project_root 없음: {project_root}",
              file=sys.stderr)
        return 1
    if not mickey_root.exists():
        print(f"[mickey_graph] ERROR: mickey_root 없음: {mickey_root}",
              file=sys.stderr)
        return 1

    graph, stats = build_project_graph(project_root, mickey_root)
    print(f"[mickey_graph] nodes={stats.node_count} edges={stats.edge_count}")
    print(f"[mickey_graph] kind distribution: {stats.kind_distribution}")
    print(f"[mickey_graph] project_nodes={len(graph.project_node_ids)} "
          f"backlinked_entries={len(graph.backlinked_entry_ids)}")

    # 엣지 타입 분포 진단
    from collections import Counter
    edge_type_counts = Counter(e.type.value for e in graph.edges)
    cross_scope_count = edge_type_counts.get("cross-scope", 0)
    # 프로젝트 노드 간 SIMILAR_TO 만 카운트
    project_similar = sum(
        1 for e in graph.edges
        if e.type.value == "similar-to"
        and e.from_id in graph.project_node_ids
        and e.to_id in graph.project_node_ids
    )
    print(f"[mickey_graph] edge types: {dict(edge_type_counts)}")
    print(f"[mickey_graph] cross_scope_edges={cross_scope_count} "
          f"project_similar_edges={project_similar}")

    html = render_html(graph, page_title=f"project: {project_name}")
    size = write_html(html, output)
    print(f"[mickey_graph] wrote {output} ({size:,} bytes)")

    if auto_open:
        uri = output.resolve().as_uri()
        print(f"[mickey_graph] opening: {uri}")
        webbrowser.open(uri)

    return 0


def main(argv: list[str] | None = None) -> int:
    _ensure_stdout_utf8()
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    args = _parse_args(argv if argv is not None else sys.argv[1:])
    mickey_root = args.mickey_root or _default_mickey_root()

    if args.scope == "global":
        output = args.output or _default_output("global")
        return run_global(mickey_root, output, args.auto_open)

    # scope == "project"
    if args.project_path is None:
        print("[mickey_graph] ERROR: --scope project 는 --project-path 필수",
              file=sys.stderr)
        return 2
    project_root = args.project_path.resolve()
    output = args.output or _default_output("project", project_root.name)
    return run_project(project_root, mickey_root, output, args.auto_open)


if __name__ == "__main__":
    sys.exit(main())
