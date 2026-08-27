# M45: repo scripts/ <-> global ~/.kiro/mickey/scripts/ 동기 상태 확인 (adaptive #2 — 방향 판정)
import sys, hashlib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

repo = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\scripts")
glob_ = Path.home() / ".kiro" / "mickey" / "scripts"

for name in ["invoke_curator.py", "promote_knowledge.py", "mickey_lock.py", "graph_audit.py"]:
    r, g = repo / name, glob_ / name
    if not r.exists() or not g.exists():
        print(f"{name}: repo={r.exists()} global={g.exists()}")
        continue
    rh = hashlib.sha256(r.read_bytes()).hexdigest()[:12]
    gh = hashlib.sha256(g.read_bytes()).hexdigest()[:12]
    print(f"{name}: {'SAME' if rh == gh else 'DIFF'} (repo {rh} / global {gh})")
