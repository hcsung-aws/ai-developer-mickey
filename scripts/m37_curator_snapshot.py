# -*- coding: utf-8 -*-
"""M37: Curator 호출 전/후 글로벌 domain 스냅샷 비교 (검증 기간 교차검증).

사용: --pre 로 스냅샷 저장, --post 로 저장본과 현재 상태 diff 출력.
대상: ~/.kiro/mickey/ 전체 (파일 경로, mtime, size) + 프로젝트 adaptive.md/_curator-staging.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

MICKEY = Path(r"C:\Users\hcsung\.kiro\mickey")
PROJECT = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")
SNAP = PROJECT / "scripts" / "output" / "m37_curator_snapshot.json"

def scan():
    state = {}
    for root, prefix in ((MICKEY, "global"), (PROJECT / "context_rule", "cr"), (PROJECT / "_curator-staging", "staging"), (PROJECT / "common_knowledge", "ck")):
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file():
                st = p.stat()
                state[f"{prefix}:{p.relative_to(root).as_posix()}"] = [st.st_mtime, st.st_size]
    return state

ap = argparse.ArgumentParser()
ap.add_argument("--pre", action="store_true")
ap.add_argument("--post", action="store_true")
a = ap.parse_args()

if a.pre:
    SNAP.parent.mkdir(exist_ok=True)
    SNAP.write_text(json.dumps(scan()), encoding="utf-8")
    print(f"[OK] 스냅샷 저장: {SNAP} ({datetime.now().isoformat()})")
elif a.post:
    before = json.loads(SNAP.read_text(encoding="utf-8"))
    after = scan()
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
    print(f"=== Curator 전후 diff === 추가 {len(added)} / 삭제 {len(removed)} / 변경 {len(changed)}")
    for k in added:
        print(f"  [ADD] {k}")
    for k in removed:
        print(f"  [DEL] {k}")
    for k in changed:
        print(f"  [MOD] {k}")
