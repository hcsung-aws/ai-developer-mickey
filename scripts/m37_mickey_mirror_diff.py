# -*- coding: utf-8 -*-
"""M37: repo mickey/ vs 글로벌 ~/.kiro/mickey/ 파일별 diff 실측.

목적: install(repo→global -Force 복사) 실행 시 어떤 글로벌 파일이 stale repo 본으로
덮어써질지, 파일별 방향(최신본 위치)을 판정한다. (adaptive #2/#4)

판정 기준:
- 내용 hash 동일 → SAME
- repo에만 존재 → REPO_ONLY (install 시 global에 추가됨)
- global에만 존재 → GLOBAL_ONLY (install이 삭제하지는 않음 — copy만 하므로 생존)
- 양쪽 존재 + hash 다름 → DIFF (mtime 비교로 어느 쪽이 최신인지 표시)
"""
import hashlib
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: Windows cp949 대비

REPO = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\mickey")
GLOBAL = Path(r"C:\Users\hcsung\.kiro\mickey")

# 백업 파일(.bak)은 배포 대상 아님 — 비교에서 제외하되 카운트만 보고
def collect(root: Path):
    files = {}
    for p in root.rglob("*"):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            files[rel] = p
    return files

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]

def mtime(p: Path) -> str:
    return datetime.fromtimestamp(p.stat().st_mtime).strftime("%m-%d %H:%M")

repo_files = collect(REPO)
global_files = collect(GLOBAL)

# _curator-staging 은 런타임 영역, 배포 대상 아님
def is_excluded(rel: str) -> bool:
    return rel.startswith("_curator-staging/") or ".bak" in rel or "-bak" in rel

repo_keys = {k for k in repo_files if not is_excluded(k)}
global_keys = {k for k in global_files if not is_excluded(k)}

same, diff, repo_only, global_only = [], [], [], []
for rel in sorted(repo_keys | global_keys):
    r, g = repo_files.get(rel), global_files.get(rel)
    if r and g:
        if sha256(r) == sha256(g):
            same.append(rel)
        else:
            newer = "GLOBAL" if g.stat().st_mtime > r.stat().st_mtime else "REPO"
            diff.append((rel, mtime(r), mtime(g), newer))
    elif r:
        repo_only.append((rel, mtime(r)))
    else:
        global_only.append((rel, mtime(g)))

print(f"=== repo mickey/ vs 글로벌 ~/.kiro/mickey/ diff (백업/.staging 제외) ===")
print(f"SAME: {len(same)} / DIFF: {len(diff)} / REPO_ONLY: {len(repo_only)} / GLOBAL_ONLY: {len(global_only)}")

print(f"\n--- DIFF ({len(diff)}) : install 시 global이 repo 본으로 덮어써짐 ---")
for rel, rm, gm, newer in diff:
    print(f"  {rel}  (repo {rm} vs global {gm}) → 최신: {newer}")

print(f"\n--- REPO_ONLY ({len(repo_only)}) : install 시 global에 추가됨 ---")
for rel, rm in repo_only:
    print(f"  {rel}  ({rm})")

print(f"\n--- GLOBAL_ONLY ({len(global_only)}) : install copy로는 생존 (삭제 없음) ---")
for rel, gm in global_only:
    print(f"  {rel}  ({gm})")

print(f"\n--- SAME ({len(same)}) ---")
for rel in same:
    print(f"  {rel}")

# 제외된 항목 카운트
excluded_g = [k for k in global_files if is_excluded(k)]
excluded_r = [k for k in repo_files if is_excluded(k)]
print(f"\n(제외: repo 백업 {len(excluded_r)}건, global 백업/staging {len(excluded_g)}건)")
