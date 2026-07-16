# -*- coding: utf-8 -*-
"""M37 Phase 2 후속 수정 2건.

1. INDEX.md Domain Map: 이동한 18개의 `entries/{id}.md` → `entries/cloud/{id}.md`
2. GRAPH.md: batch-confirm-autonomous-proceed 노드 Path 정정
   (patterns/ 소속인데 M36 Path 일괄 생성 시 entries/ 로 오기재 — 기존 이슈)
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DOMAIN = Path(r"C:\Users\hcsung\.kiro\mickey\domain")
INDEX = DOMAIN / "INDEX.md"
GRAPH = DOMAIN / "GRAPH.md"

MOVED = [
    "agentcore-direct-invocation", "auth-rejection-message-generalization",
    "token-rejection-message-generalization", "aws-security-scan-preemption",
    "aws-states-language-flatten-pattern", "bedrock-inference-profile-only",
    "bedrock-client-timeout-config", "boto3-sync-invoke-retry-side-effect",
    "cdk-bootstrap-role-assume-pattern", "cdk-lib-caret-nag-drift",
    "cdk-cjs-over-esm-in-monorepo", "cli-direct-lambda-deploy",
    "iam-role-description-ascii-only", "idempotent-infra-setup",
    "terraform-ternary-no-lazy-eval", "terraform-ssm-default-sensitive",
    "terraform-validate-plan-apply-ladder", "terraform-output-json-structure",
]

# 1. INDEX 경로 치환
idx = INDEX.read_text(encoding="utf-8")
n = 0
for m in MOVED:
    old, new = f"entries/{m}.md", f"entries/cloud/{m}.md"
    c = idx.count(old)
    idx = idx.replace(old, new)
    n += c
INDEX.write_text(idx, encoding="utf-8")
print(f"[OK] INDEX 경로 치환: {n}건")

# 2. GRAPH batch-confirm Path 정정 (domain/ 기준 상대 경로)
g = GRAPH.read_text(encoding="utf-8")
old_row = "entries/batch-confirm-autonomous-proceed.md"
new_row = "../patterns/batch-confirm-autonomous-proceed.md"
assert g.count(old_row) == 1, f"예상 1건, 실제 {g.count(old_row)}건"  # count-1 guard
g = g.replace(old_row, new_row)
GRAPH.write_text(g, encoding="utf-8")
print(f"[OK] GRAPH batch-confirm Path 정정: {old_row} -> {new_row}")
