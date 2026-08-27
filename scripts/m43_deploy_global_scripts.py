# -*- coding: utf-8 -*-
"""M43: 글로벌 스크립트 배포 + 해시 검증.

repo scripts/ 의 3파일(promote_knowledge, mickey_lock, invoke_curator)을
~/.kiro/mickey/scripts/ 로 세대 관리 배포하고 sha256 동일성을 실측한다.
"""
import hashlib
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_SCRIPTS = Path(__file__).resolve().parent
GLOBAL_SCRIPTS = Path.home() / ".kiro" / "mickey" / "scripts"
FILES = ["promote_knowledge.py", "mickey_lock.py", "invoke_curator.py", "graph_audit.py"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def main() -> int:
    GLOBAL_SCRIPTS.mkdir(parents=True, exist_ok=True)
    ok = True
    for name in FILES:
        src, dst = REPO_SCRIPTS / name, GLOBAL_SCRIPTS / name
        shutil.copy2(src, dst)
        match = sha(src) == sha(dst)
        ok &= match
        print(f"[{'PASS' if match else 'FAIL'}] {name}: {sha(dst)}")
    print(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
