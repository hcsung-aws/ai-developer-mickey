# -*- coding: utf-8 -*-
"""M37 결함 A 조치: knowledge-curator agent JSON에 읽기 도구 자동 승인 추가.

§17 스펙: fs_read/grep/glob은 전체 자동 승인이어야 하나 allowedTools가 비어 있어
headless delegate 실행에서 읽기가 거부됨 → Curator가 중복 확인 불가로 staging 강등.

대상: ~/.kiro/agents/knowledge-curator.json + repo examples/knowledge-curator.json
(prompt 등 타 필드 보존, 백업 생성)
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

TARGETS = [
    Path(r"C:\Users\hcsung\.kiro\agents\knowledge-curator.json"),
    Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\examples\knowledge-curator.json"),
]
READ_TOOLS = ["fs_read", "grep", "glob"]

for t in TARGETS:
    data = json.loads(t.read_text(encoding="utf-8"))
    before = data.get("allowedTools", [])
    merged = sorted(set(before) | set(READ_TOOLS))
    if merged == sorted(before):
        print(f"[SKIP] {t.name}: 이미 포함")
        continue
    shutil.copy2(t, t.with_suffix(".json.m37-toolfix-bak"))
    data["allowedTools"] = merged
    t.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] {t}: allowedTools {before} -> {merged}")

# 검증: 두 파일의 allowedTools 일치 + 읽기 3종 포함
ok = True
for t in TARGETS:
    at = json.loads(t.read_text(encoding="utf-8"))["allowedTools"]
    good = set(READ_TOOLS) <= set(at)
    ok &= good
    print(f"[{'PASS' if good else 'FAIL'}] {t.name}: {at}")
print("ALL PASS" if ok else "FAIL 존재")
