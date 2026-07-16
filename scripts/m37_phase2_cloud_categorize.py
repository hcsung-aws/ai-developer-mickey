# -*- coding: utf-8 -*-
"""M37 Phase 2: entries/cloud/ 카테고리화 수술 (§20 Step 3 파이프라인 5단계).

동작 (--apply 없으면 dry-run):
1. GRAPH.md / INDEX.md 백업 (.m37-phase2-bak)
2. 포함 18개 entry 파일을 entries/cloud/ 로 이동
3. 상위 GRAPH: 18개 노드 행 제거 + cloud [ANCHOR] 행 추가
4. 하위 GRAPH(entries/cloud/GRAPH.md) 생성: 18노드(Path 갱신) + 내부 엣지 이관
5. 상위 GRAPH: 내부 엣지 제거(하위로 이관), cross-category 엣지 유지
6. INDEX.md Anchors § 갱신 + 양쪽 Last Updated M37 명의
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

DOMAIN = Path(r"C:\Users\hcsung\.kiro\mickey\domain")
GRAPH = DOMAIN / "GRAPH.md"
INDEX = DOMAIN / "INDEX.md"
ENTRIES = DOMAIN / "entries"
CLOUD = ENTRIES / "cloud"

# 파이프라인 3단계에서 엄선 + 4단계 사용자 승인 완료된 구성원 (M37 계획)
CLOUD_MEMBERS = [
    "agentcore-direct-invocation",
    "auth-rejection-message-generalization",
    "token-rejection-message-generalization",
    "aws-security-scan-preemption",
    "aws-states-language-flatten-pattern",
    "bedrock-inference-profile-only",
    "bedrock-client-timeout-config",
    "boto3-sync-invoke-retry-side-effect",
    "cdk-bootstrap-role-assume-pattern",
    "cdk-lib-caret-nag-drift",
    "cdk-cjs-over-esm-in-monorepo",
    "cli-direct-lambda-deploy",
    "iam-role-description-ascii-only",
    "idempotent-infra-setup",
    "terraform-ternary-no-lazy-eval",
    "terraform-ssm-default-sensitive",
    "terraform-validate-plan-apply-ladder",
    "terraform-output-json-structure",
]

ANCHOR_ROW = (
    "| cloud | Cloud/AWS/IaC 카테고리 [ANCHOR] | "
    "cdk, aws, terraform, cognito, bedrock, boto3, lambda, iam, agentcore, infrastructure, category-anchor | "
    "AWS/Cloud 인프라 도메인 지식 18건 → 하위 그래프에서 탐색 | entries/cloud/GRAPH.md |"
)

TODAY = "2026-07-16"
SIGNER = f"{TODAY} (ai-developer-mickey Mickey 37 — 트랙 A Phase 2: cloud 카테고리 신설, 18 entries 이동/anchor 등록)"


def parse_table_rows(lines, start, end):
    """구간 내 표 데이터 행(헤더/구분선 제외)을 (줄번호, 셀리스트) 로 반환."""
    rows = []
    seen_header = False
    for i in range(start, end):
        ln = lines[i]
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not seen_header:
            seen_header = True  # 헤더 행
            continue
        if set(ln.replace("|", "").strip()) <= {"-", " ", ":"}:
            continue  # 구분선
        rows.append((i, cells))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 적용 (기본 dry-run)")
    args = ap.parse_args()
    apply = args.apply
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== M37 Phase 2 cloud 카테고리화 [{mode}] ===\n")

    text = GRAPH.read_text(encoding="utf-8")
    lines = text.splitlines()
    nodes_i = lines.index("## Nodes")
    edges_i = lines.index("## Edges")
    last_i = lines.index("## Last Updated")

    node_rows = parse_table_rows(lines, nodes_i, edges_i)
    edge_rows = parse_table_rows(lines, edges_i, last_i)
    all_ids = {c[0] for _, c in node_rows}
    print(f"상위 GRAPH: 노드 {len(node_rows)}, 엣지 {len(edge_rows)}")

    # ── 사전 검증: 구성원 전원이 노드/파일로 존재하는가 ──
    missing = [m for m in CLOUD_MEMBERS if m not in all_ids]
    missing_files = [m for m in CLOUD_MEMBERS if not (ENTRIES / f"{m}.md").exists()]
    if missing or missing_files:
        print(f"[ABORT] 노드 누락: {missing} / 파일 누락: {missing_files}")
        return 1

    member_set = set(CLOUD_MEMBERS)
    moved_node_lines = {}   # id -> 갱신된 행
    remove_line_nos = set()
    for i, cells in node_rows:
        if cells[0] in member_set:
            new_path = f"entries/cloud/{cells[0]}.md"
            new_row = "| " + " | ".join(cells[:4] + [new_path]) + " |"
            moved_node_lines[cells[0]] = new_row
            remove_line_nos.add(i)

    internal_edges, cross_edges_kept = [], []
    for i, cells in edge_rows:
        frm, to = cells[0], cells[1]
        if frm in member_set and to in member_set:
            internal_edges.append("| " + " | ".join(cells) + " |")
            remove_line_nos.add(i)
        elif frm in member_set or to in member_set:
            cross_edges_kept.append((frm, to))

    print(f"이동 노드: {len(moved_node_lines)} / 내부 엣지 이관: {len(internal_edges)} / cross 엣지 상위 유지: {len(cross_edges_kept)}")

    # ── 상위 GRAPH 재구성 ──
    new_lines = []
    for i, ln in enumerate(lines):
        if i in remove_line_nos:
            continue
        new_lines.append(ln)
    # anchor 행: Nodes 표 구분선 바로 다음에 삽입 (카테고리를 최상단 노출)
    out = []
    inserted = False
    in_nodes = False
    for ln in new_lines:
        out.append(ln)
        if ln.strip() == "## Nodes":
            in_nodes = True
        if in_nodes and not inserted and set(ln.replace("|", "").strip()) <= {"-", " ", ":"} and ln.strip().startswith("|"):
            out.append(ANCHOR_ROW)
            inserted = True
    # Last Updated 교체
    li = out.index("## Last Updated")
    out = out[: li + 1] + [SIGNER] + [""]

    new_graph = "\n".join(out).rstrip() + "\n"
    # 연속 빈 줄 정리 (행 제거 잔여물)
    new_graph = re.sub(r"\n{3,}", "\n\n", new_graph)

    # ── 하위 GRAPH 생성 ──
    sub_lines = [
        "# Knowledge Graph — cloud (AWS/Cloud/IaC)",
        "",
        "> 상위: `domain/GRAPH.md` 의 `cloud [ANCHOR]`. cross-category 엣지는 상위 GRAPH에 유지.",
        "",
        "## Nodes",
        "",
        "| ID | Title | Tags | Core | Path |",
        "|----|-------|------|------|------|",
    ]
    for m in CLOUD_MEMBERS:
        sub_lines.append(moved_node_lines[m])
    sub_lines += ["", "## Edges", "| From | To | Type | Reason |", "|------|----|------|--------|"]
    sub_lines += internal_edges
    sub_lines += ["", "## Last Updated", SIGNER, ""]
    sub_graph = "\n".join(sub_lines)

    # ── INDEX Anchors § 갱신 ──
    idx = INDEX.read_text(encoding="utf-8")
    anchor_placeholder = "> (카테고리 생성 시 `{category} → entries/{category}/GRAPH.md` 형태로 목록화. 현재 flat, 유보.)"
    anchor_new = (
        "| 카테고리 | 하위 GRAPH | 범위 |\n"
        "|---------|-----------|------|\n"
        "| cloud | entries/cloud/GRAPH.md | AWS/Cloud/IaC 도메인 18 entries (cdk, aws, terraform, cognito, bedrock, boto3, lambda, iam, agentcore) |"
    )
    if anchor_placeholder not in idx:
        print("[ABORT] INDEX Anchors placeholder 미발견 — 수동 확인 필요")
        return 1
    idx_new = idx.replace(anchor_placeholder, anchor_new)
    idx_new = re.sub(
        r"## Last Updated\n.*?$",
        f"## Last Updated\n{SIGNER}\n",
        idx_new, flags=re.DOTALL,
    )

    if not apply:
        print("\n--- [dry-run] 상위 GRAPH anchor 행 ---")
        print(ANCHOR_ROW)
        print(f"\n--- [dry-run] 하위 GRAPH 미리보기 (노드 {len(CLOUD_MEMBERS)}, 내부 엣지 {len(internal_edges)}) ---")
        print("\n".join(sub_lines[:12]) + "\n...")
        print("\n--- [dry-run] cross 엣지 유지 목록 ---")
        for frm, to in cross_edges_kept:
            print(f"  {frm} -> {to}")
        print("\ndry-run 완료. --apply 로 실행.")
        return 0

    # ── APPLY ──
    shutil.copy2(GRAPH, GRAPH.with_name("GRAPH.md.m37-phase2-bak"))
    shutil.copy2(INDEX, INDEX.with_name("INDEX.md.m37-phase2-bak"))
    CLOUD.mkdir(exist_ok=True)
    for m in CLOUD_MEMBERS:
        shutil.move(str(ENTRIES / f"{m}.md"), str(CLOUD / f"{m}.md"))
    GRAPH.write_text(new_graph, encoding="utf-8")
    (CLOUD / "GRAPH.md").write_text(sub_graph, encoding="utf-8")
    INDEX.write_text(idx_new, encoding="utf-8")
    print("\n[OK] 적용 완료: 파일 18 이동 + 상위/하위 GRAPH + INDEX Anchors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
