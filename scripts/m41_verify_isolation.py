# -*- coding: utf-8 -*-
"""M41: Curator 격리 적용 상태 재검증 (콘솔 잘림 회피 — 리포트 파일 직접 기록)."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SOT = Path.home() / ".kiro" / "mickey" / "domain" / "CURATOR-PROMPT.md"
HOME_JSON = Path.home() / ".kiro" / "agents" / "knowledge-curator.json"
REPO = Path(__file__).resolve().parent.parent
REPO_JSON = REPO / "examples" / "knowledge-curator.json"
REPO_MD = REPO / "mickey" / "domain" / "CURATOR-PROMPT.md"
OUT = Path(__file__).resolve().parent / "output" / "m41_verify_isolation.txt"

EXPECTED_ALLOWED = ["**/context_rule/adaptive.md", "**/_curator-staging/**"]

lines, ok = [], True

def check(cond, label):
    global ok
    ok &= cond
    lines.append(f"[{'PASS' if cond else 'FAIL'}] {label}")

md = SOT.read_text(encoding="utf-8")
for target in (HOME_JSON, REPO_JSON):
    data = json.loads(target.read_text(encoding="utf-8"))
    tag = "HOME" if target == HOME_JSON else "REPO"
    check(data["prompt"] == md, f"{tag} prompt == SoT")
    allowed = data["toolsSettings"]["fs_write"]["allowedPaths"]
    check(allowed == EXPECTED_ALLOWED, f"{tag} allowedPaths == 기대값 (실제: {allowed})")
    check("domain/**" not in json.dumps(data.get("toolsSettings", {})),
          f"{tag} toolsSettings에 domain/** 잔존 없음")
    check("격리 원칙" in data.get("description", ""), f"{tag} description 갱신됨")
check(REPO_MD.read_bytes() == SOT.read_bytes(), "repo seed md == SoT")
for kw in ("격리 원칙", "글로벌 쓰기 금지", "gd- 승격 번들 형식", "promote_knowledge.py",
           "세션 경계 (Session Boundary)", "전체 변경 목록 (누락 금지)"):
    check(kw in md, f"SoT 키워드 존재: {kw}")
for stale in ("Last Updated 명의 = 호출 세션", "domain/ 수정 (크로스 프로젝트 지식)"):
    check(stale not in md, f"폐기 지시 잔존 없음: {stale}")
# 백업 존재 확인 (adaptive #10)
for p in (SOT, HOME_JSON, REPO_JSON, REPO_MD):
    bak = p.with_suffix(p.suffix + ".bak-ai-developer-mickey-m41")
    check(bak.exists(), f"백업 존재: {bak.name}")

lines.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"written: {OUT} ({'ALL PASS' if ok else 'FAIL'})")
sys.exit(0 if ok else 1)
