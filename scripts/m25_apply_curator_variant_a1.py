"""
M25 — Curator 변형 A1 적용 + 검증.
A2(현재) → A1: `allowedTools=[]` 만 변경 (ai-developer-mickey 정상 패턴 완전 모방).
글로벌+repo 양쪽 동시 변경 + hash 일치 검증 (safe-batch-replace.md 패턴).
"""

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

# Windows cp949 환경 대응 (adaptive.md Rule #8)
sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(os.path.expandvars("%USERPROFILE%"))
GLOBAL_PATH = HOME / ".kiro" / "agents" / "knowledge-curator.json"
REPO_PATH = Path("examples") / "knowledge-curator.json"

EXPECTED_BEFORE_HASH = (
    "F81E9F2401FD16906986A11BBDA284D5F0B437640C08866FB9D231CE29235820"
)
EXPECTED_BEFORE_SIZE = 11748
EXPECTED_BEFORE_ALLOWED = ["fs_read", "grep", "glob", "fs_write"]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_before(label: str, path: Path) -> bool:
    """변경 전 상태가 A2 (M24 적용 후) 와 일치하는지 검증."""
    if not path.exists():
        print(f"[{label}] NOT FOUND: {path}")
        return False
    h = file_sha256(path)
    s = path.stat().st_size
    obj = json.loads(path.read_text(encoding="utf-8"))
    tools = obj.get("tools")
    allowed = obj.get("allowedTools")
    print(f"[{label}] before: hash={h[:16]}... size={s}")
    print(f"  tools={tools} allowedTools={allowed}")
    ok = (
        h == EXPECTED_BEFORE_HASH
        and s == EXPECTED_BEFORE_SIZE
        and tools == ["*"]
        and allowed == EXPECTED_BEFORE_ALLOWED
    )
    if not ok:
        print(f"[{label}] PRECONDITION FAIL")
    return ok


def backup_a2(label: str, path: Path) -> Path:
    """A2 상태를 .m25-bak 으로 백업."""
    bak = path.with_suffix(path.suffix + ".m25-bak")
    shutil.copy2(path, bak)
    print(f"[{label}] backup: {bak.name} ({bak.stat().st_size} bytes)")
    return bak


def apply_a1(label: str, path: Path) -> str:
    """A1 적용: allowedTools=[] 로 변경. dict 직접 수정 후 동일 들여쓰기로 직렬화."""
    raw_before = path.read_text(encoding="utf-8")
    obj = json.loads(raw_before)
    obj["allowedTools"] = []
    # 기존 파일 들여쓰기 추정: 2 spaces (Kiro CLI agent JSON 표준)
    new_raw = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    path.write_text(new_raw, encoding="utf-8")
    h_after = file_sha256(path)
    s_after = path.stat().st_size
    print(f"[{label}] after:  hash={h_after[:16]}... size={s_after}")
    print(f"  tools={obj['tools']} allowedTools={obj['allowedTools']}")
    return h_after


def main() -> int:
    targets = [("global", GLOBAL_PATH), ("repo  ", REPO_PATH)]

    # Step 1. 변경 전 상태 검증
    print("=== Step 1: precondition check (A2 state) ===")
    for label, path in targets:
        if not verify_before(label, path):
            print("ABORT: precondition mismatch")
            return 1

    # Step 2. A2 백업 (.m25-bak)
    print("\n=== Step 2: backup A2 → .m25-bak ===")
    for label, path in targets:
        backup_a2(label, path)

    # Step 3. A1 적용 (allowedTools=[])
    print("\n=== Step 3: apply A1 (allowedTools=[]) ===")
    after_hashes = []
    for label, path in targets:
        after_hashes.append(apply_a1(label, path))

    # Step 4. hash 일치 + 형식 검증
    print("\n=== Step 4: post-check ===")
    if after_hashes[0] != after_hashes[1]:
        print("FAIL: global vs repo hash mismatch")
        return 2

    print(f"PASS: global == repo (hash={after_hashes[0][:16]}...)")

    # 형식 재검증
    obj = json.loads(GLOBAL_PATH.read_text(encoding="utf-8"))
    if obj.get("tools") != ["*"]:
        print(f"FAIL: tools changed unexpectedly: {obj.get('tools')}")
        return 3
    if obj.get("allowedTools") != []:
        print(f"FAIL: allowedTools not []: {obj.get('allowedTools')}")
        return 3

    print("PASS: tools=['*'], allowedTools=[]")
    print("\n=== M25 A1 application complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
