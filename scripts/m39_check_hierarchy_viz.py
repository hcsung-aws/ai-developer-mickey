# M39: 렌더 산출 HTML에서 계층화(anchor↔하위) 가시성 실측 스크립트
# 목적: mickey-graph-global.html 내 직렬화된 그래프 JSON을 추출하여
#       ① cloud anchor 노드 존재 ② anchor의 degree(연결 수) ③ 하위 18개 노드 포함 여부
#       ④ anchor↔하위 엣지 존재 여부를 판정한다.
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

HTML = Path(__file__).resolve().parent / "output" / "mickey-graph-global.html"


def extract_json(name: str, text: str):
    """템플릿에 인라인된 `const <name> = [...];` JSON을 추출한다."""
    m = re.search(rf"const {name} = (\[.*?\]);", text, re.DOTALL)
    return json.loads(m.group(1)) if m else None


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    # 그래프 데이터는 `const MICKEY_GRAPH = {...};` 객체로 인라인됨
    m = re.search(r"const MICKEY_GRAPH = (\{.*?\});\n", text, re.DOTALL)
    if not m:
        print("[FAIL] MICKEY_GRAPH 추출 실패")
        return 1
    payload = json.loads(m.group(1))
    print(f"MICKEY_GRAPH keys: {list(payload.keys())}")
    nlist = payload.get("nodes", [])
    elist = payload.get("edges", [])
    nodes = ("MICKEY_GRAPH.nodes", nlist)
    edges = ("MICKEY_GRAPH.edges", elist)

    if not nlist or not elist:
        print("[FAIL] 그래프 JSON 추출 실패")
        return 1

    nname, nlist = nodes
    ename, elist = edges
    print(f"노드 배열: {nname} ({len(nlist)}) / 엣지 배열: {ename} ({len(elist)})")

    # ① anchor 존재
    anchor = next((n for n in nlist if n["id"] == "cloud"), None)
    print(f"\n① cloud anchor 노드: {'존재' if anchor else '없음'}")
    if anchor:
        keys_of_interest = {k: anchor.get(k) for k in ("id", "kind", "tags", "source") if k in anchor}
        print(f"   속성: {keys_of_interest}")

    # ② anchor degree (직렬화 필드는 from_id/to_id — from/to 아님 주의)
    deg = sum(1 for e in elist if e.get("from_id") == "cloud" or e.get("to_id") == "cloud")
    print(f"② cloud anchor 연결 엣지 수: {deg}")

    # ③ 하위 노드 포함 여부
    sub_ids = [
        "agentcore-direct-invocation", "idempotent-infra-setup", "bedrock-inference-profile-only",
        "terraform-ternary-no-lazy-eval", "cdk-bootstrap-role-assume-pattern",
    ]
    present = [i for i in sub_ids if any(n["id"] == i for n in nlist)]
    print(f"③ 하위 노드 표본 {len(present)}/{len(sub_ids)} 포함: {present}")

    # ④ anchor↔하위 엣지 (member-of 합성 포함)
    sub_edges = [e for e in elist if e.get("from_id") == "cloud" or e.get("to_id") == "cloud"]
    print(f"④ anchor↔하위 엣지: {len(sub_edges)}건")
    for e in sub_edges[:5]:
        print(f"   {e.get('from_id')} -[{e.get('type')}]-> {e.get('to_id')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
