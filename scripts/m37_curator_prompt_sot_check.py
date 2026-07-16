# -*- coding: utf-8 -*-
"""M37: Curator 프롬프트 SoT 관계 확인.

- examples/knowledge-curator.json vs ~/.kiro/agents/knowledge-curator.json 동일 여부
- agent JSON 내장 prompt가 CURATOR-PROMPT.md 를 참조하는지 (런타임 로딩 여부)
- 내장 prompt와 글로벌 CURATOR-PROMPT.md 의 차이 규모
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

repo_json = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\examples\knowledge-curator.json")
home_json = Path(r"C:\Users\hcsung\.kiro\agents\knowledge-curator.json")
prompt_md = Path(r"C:\Users\hcsung\.kiro\mickey\domain\CURATOR-PROMPT.md")

rj = json.loads(repo_json.read_text(encoding="utf-8"))
print(f"repo JSON == home JSON: {repo_json.read_bytes() == home_json.read_bytes() if home_json.exists() else 'home 없음'}")

p = rj["prompt"]
print(f"내장 prompt 길이: {len(p)} chars")
print(f"내장 prompt에 'CURATOR-PROMPT' 참조: {'CURATOR-PROMPT' in p}")

md = prompt_md.read_text(encoding="utf-8")
print(f"글로벌 CURATOR-PROMPT.md 길이: {len(md)} chars (보정 후)")

# 내장 prompt의 0단계 로딩 목록 추출
import re
m = re.search(r"### 0단계.*?### 1단계", p, re.DOTALL)
if m:
    print("\n--- 내장 prompt 0단계 (로딩 목록) ---")
    print(m.group(0)[:600])

# agent JSON 의 도구/권한 확인
for k in ("tools", "allowedTools", "toolsSettings", "includeMcpJson"):
    if k in rj:
        print(f"\n{k}: {json.dumps(rj[k], ensure_ascii=False)[:300]}")
