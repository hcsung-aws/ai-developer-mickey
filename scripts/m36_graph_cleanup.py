# M36 Task 1+2: 글로벌 domain/GRAPH.md 정리 스크립트.
# 1) 중복 노드 ID 3건(2행씩) 병합 — 첫 행의 Title/Core 유지, 태그는 합집합.
# 2) orphan entry external-source-digest-separation 노드 등록 (dangling 해소).
# 3) Nodes 표에 Path 컬럼 신설 + 전체 노드 entries/{id}.md 일괄 기입.
# 라인 레벨 변환으로 기존 포맷(빈 줄 그룹핑, Edges 섹션)을 보존한다.
# --apply 없으면 dry-run(백업/쓰기 안 함, 변경 요약만 출력).
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 회피 (adaptive #8)

GRAPH = Path.home() / ".kiro" / "mickey" / "domain" / "GRAPH.md"

# 등록할 orphan 노드 (external-source-digest-separation.md 내용 기반)
ORPHAN_ID = "external-source-digest-separation"
ORPHAN_ROW_COLS = [
    ORPHAN_ID,
    "External Source Digest Separation",
    "external-source, digest, citation, benchmark, evaluation, documentation, licensing, traceability",
    "외부 1차 자료 정독 결과를 별도 digest 문서로 분리 + 산출물은 요약표+출처 ID 참조 → 문서 비대화 방지 + 출처 추적성",
]


def is_separator(cols):
    return all(set(c) <= set("-: ") and c for c in cols)


def parse_row(line):
    # "| a | b | c | d |" -> ['a','b','c','d']
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 쓰기(미지정 시 dry-run)")
    args = ap.parse_args()

    text = GRAPH.read_text(encoding="utf-8")
    if "## Nodes" not in text or "## Edges" not in text:
        print("ERROR: Nodes/Edges 섹션을 찾을 수 없음")
        return 1

    head, rest = text.split("## Nodes", 1)
    nodes_body, edges_part = rest.split("## Edges", 1)

    lines = nodes_body.splitlines()

    # 1차 스캔: id -> 태그 합집합, id별 출현 횟수, 첫 출현 행 cols
    tags_union = defaultdict(list)
    first_cols = {}
    seen_count = defaultdict(int)
    warnings = []
    for ln in lines:
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cols = parse_row(ln)
        if len(cols) < 4 or cols[0] in ("ID", "") or is_separator(cols):
            continue
        if len(cols) != 4:
            warnings.append(f"열 개수 {len(cols)} (기대 4): {cols[0]}")
        nid = cols[0]
        seen_count[nid] += 1
        # 태그 합집합 (순서 보존)
        for t in [x.strip() for x in cols[2].split(",") if x.strip()]:
            if t not in tags_union[nid]:
                tags_union[nid].append(t)
        if nid not in first_cols:
            first_cols[nid] = cols

    dup_ids = [nid for nid, c in seen_count.items() if c > 1]

    # 2차: 재작성
    out = ["## Nodes"]
    emitted = set()
    for ln in lines:
        s = ln.strip()
        if not s.startswith("|"):
            out.append(ln)
            continue
        cols = parse_row(ln)
        # 헤더 행
        if cols[0] == "ID":
            out.append("| ID | Title | Tags | Core | Path |")
            continue
        # 구분선
        if is_separator(cols):
            out.append("|----|-------|------|------|------|")
            continue
        nid = cols[0]
        if nid in emitted:
            # 중복 2번째 이상 → 스킵
            continue
        emitted.add(nid)
        merged_tags = ", ".join(tags_union[nid])
        title = first_cols[nid][1]
        core = first_cols[nid][3]
        out.append(f"| {nid} | {title} | {merged_tags} | {core} | entries/{nid}.md |")

    # orphan 노드 등록 (미등록 시에만)
    orphan_added = False
    if ORPHAN_ID not in emitted:
        out.append("")
        out.append(
            f"| {ORPHAN_ROW_COLS[0]} | {ORPHAN_ROW_COLS[1]} | {ORPHAN_ROW_COLS[2]} | {ORPHAN_ROW_COLS[3]} | entries/{ORPHAN_ID}.md |"
        )
        orphan_added = True

    new_nodes_body = "\n".join(out)
    if nodes_body.endswith("\n") and not new_nodes_body.endswith("\n"):
        new_nodes_body += "\n"
    new_text = head + new_nodes_body + "\n## Edges" + edges_part

    # 요약 출력
    total = len(first_cols) + (1 if orphan_added else 0)
    print(f"고유 노드 수(병합 후): {len(first_cols)} + orphan {1 if orphan_added else 0} = {total}")
    print(f"중복 병합 대상: {dup_ids}")
    for nid in dup_ids:
        print(f"  - {nid}: {seen_count[nid]}행 → 1행, 태그 {len(tags_union[nid])}개 합집합")
    print(f"orphan 노드 등록: {ORPHAN_ID} = {orphan_added}")
    print("Path 컬럼: 전체 노드 entries/<id>.md 기입")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  " + w)

    if not args.apply:
        print("\n[DRY-RUN] --apply 없어 쓰지 않음. 새 Nodes 헤더/처음 3행 미리보기:")
        preview = [l for l in new_nodes_body.splitlines() if l.strip().startswith("|")][:4]
        for p in preview:
            print("  " + p)
        return 0

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = GRAPH.parent / f"GRAPH.md.m36-bak-{stamp}"
    shutil.copy2(GRAPH, bak)
    GRAPH.write_text(new_text, encoding="utf-8")
    print(f"\n[APPLIED] 백업: {bak.name}")
    print(f"[APPLIED] 갱신: {GRAPH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
