# M44: 글로벌 지식 그래프 성장 과정 분석
#
# 소스: ~/.kiro/mickey/.promote-backups/{ts}-{owner}/ 의 pre-promote GRAPH.md 스냅샷 (M41 도입 이후)
#      + 현재 GRAPH.md (최종 상태)
# 산출:
#   1) 스냅샷별 노드/엣지/평균 차수/orphan 수 추이 — 성장하면서 연결 밀도가 유지되는가
#   2) 연속 스냅샷 diff — 새 노드가 "엣지와 함께" 추가되었는가 (0-엣지 추가 = 연결 방치 신호)
# 출력: scripts/output/m44_growth_report.txt
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

# 감사 스크립트의 파서 재사용 (동일 디렉토리 import)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from graph_audit import parse_graph  # noqa: E402

MICKEY = Path.home() / ".kiro" / "mickey"
BACKUPS = MICKEY / ".promote-backups"
CURRENT = MICKEY / "domain" / "GRAPH.md"
OUT = Path(__file__).resolve().parent / "output" / "m44_growth_report.txt"


def snapshot_graphs() -> list[tuple[str, str, Path]]:
    """백업 디렉토리에서 (타임스탬프, 소유자, GRAPH 경로) 목록을 시간순으로 수집."""
    snaps = []
    for d in sorted(BACKUPS.iterdir()):
        if not d.is_dir():
            continue
        m = re.match(r"(\d{8}-\d{6})-(.+)", d.name)
        if not m:
            continue
        graphs = sorted(d.glob("*GRAPH.md"))
        if graphs:
            snaps.append((m.group(1), m.group(2), graphs[0]))
    return snaps


def stats(path: Path):
    nodes, _, edges, _, _ = parse_graph(path.read_text(encoding="utf-8"))
    deg = {n: 0 for n in nodes}
    for f, t, _ in edges:
        if f in deg:
            deg[f] += 1
        if t in deg:
            deg[t] += 1
    # anchor(cloud)는 하위 그래프 이관으로 차수 0이 정상이므로 orphan 카운트에서 제외
    orphans = [n for n, d in deg.items() if d == 0 and "category-anchor" not in ",".join(nodes[n][0])]
    avg = sum(deg.values()) / len(nodes) if nodes else 0
    return nodes, edges, orphans, avg


def main() -> int:
    lines: list[str] = []
    series = snapshot_graphs() + [("current", "(현재)", CURRENT)]
    prev_nodes: dict | None = None
    prev_label = ""
    lines.append(f"{'시점':<17} {'소유자':<40} {'노드':>4} {'엣지':>4} {'평균차수':>7} {'orphan':>6}  신규노드(엣지수)")
    zero_edge_events = []
    for ts, owner, gpath in series:
        nodes, edges, orphans, avg = stats(gpath)
        new_info = ""
        if prev_nodes is not None:
            new_nodes = [n for n in nodes if n not in prev_nodes]
            if new_nodes:
                per_new = []
                for n in new_nodes:
                    cnt = sum(1 for f, t, _ in edges if f == n or t == n)
                    per_new.append(f"{n}({cnt})")
                    if cnt == 0:
                        zero_edge_events.append((ts, owner, n))
                new_info = ", ".join(per_new)
        lines.append(f"{ts:<17} {owner:<40} {len(nodes):>4} {len(edges):>4} {avg:>7.2f} {len(orphans):>6}  {new_info}")
        prev_nodes, prev_label = nodes, ts
    lines.append(f"\n[0-엣지로 추가된 노드 이벤트]: {len(zero_edge_events)}")
    for ts, owner, n in zero_edge_events:
        lines.append(f"  - {ts} {owner}: {n}")
    report = "\n".join(lines)
    OUT.write_text(report, encoding="utf-8")
    print(f"[RESULT] 리포트 저장: {OUT}")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
