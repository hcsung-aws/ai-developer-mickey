"""
M26 — Curator 변형 G3 적용 (누락 JSON 키 3개 보충).
4-step safe-batch-replace 패턴: precondition → backup → apply → post-check.

변형 G3:
- 추가: mcpServers = {}, useLegacyMcpJson = false, model = null
- 미변경: name, description, prompt, tools, toolAliases, allowedTools,
          toolsSettings, resources, hooks
- 결과: ai-developer-mickey 의 키 패턴 (12개 키) 완전 일치
"""

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(os.path.expandvars("%USERPROFILE%"))
REPO = Path(__file__).resolve().parent.parent

# 적용 대상: 글로벌 + repo
TARGETS = [
    HOME / ".kiro" / "agents" / "knowledge-curator.json",
    REPO / "examples" / "knowledge-curator.json",
]

# 변형 G3 — 추가할 키 (의도)
NEW_KEYS = {
    "mcpServers": {},
    "useLegacyMcpJson": False,
    "model": None,
}

EXPECTED_PRECONDITION_HASH = "545891F304E37943"  # M25 A1 적용 후 hash (앞 16자리)
EXPECTED_KEY_COUNT_BEFORE = 9
EXPECTED_KEY_COUNT_AFTER = 12


def short_hash(path: Path) -> str:
    """파일 hash 앞 16자리 — M25 와 동일한 식별 방식."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def step_precondition() -> bool:
    """1. 적용 전 상태 확인."""
    print("=== Step 1: Precondition ===")
    ok = True

    for path in TARGETS:
        if not path.exists():
            print(f"  ✗ NOT FOUND: {path}")
            ok = False
            continue

        h = short_hash(path)
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        keys = list(obj.keys())

        # hash 검증
        hash_ok = h == EXPECTED_PRECONDITION_HASH
        # 키 개수 검증
        count_ok = len(keys) == EXPECTED_KEY_COUNT_BEFORE
        # 누락 키 확인
        missing = [k for k in NEW_KEYS if k not in obj]
        missing_ok = sorted(missing) == sorted(NEW_KEYS.keys())

        marker_h = "✓" if hash_ok else "✗"
        marker_c = "✓" if count_ok else "✗"
        marker_m = "✓" if missing_ok else "✗"

        print(f"  [{path.relative_to(path.parent.parent.parent) if 'agents' in path.parts else path.relative_to(REPO)}]")
        print(f"    {marker_h} hash {h} (expect {EXPECTED_PRECONDITION_HASH})")
        print(f"    {marker_c} key count {len(keys)} (expect {EXPECTED_KEY_COUNT_BEFORE})")
        print(f"    {marker_m} missing keys {missing} (expect {sorted(NEW_KEYS.keys())})")

        if not (hash_ok and count_ok and missing_ok):
            ok = False

    print()
    return ok


def step_backup() -> bool:
    """2. .m26-bak 으로 백업."""
    print("=== Step 2: Backup ===")
    for path in TARGETS:
        backup = path.with_suffix(path.suffix + ".m26-bak")
        if backup.exists():
            print(f"  ✗ 백업 이미 존재: {backup} — 중단")
            return False
        shutil.copy2(path, backup)
        h = short_hash(backup)
        print(f"  ✓ {backup.name} ({backup.stat().st_size} bytes, hash {h})")
    print()
    return True


def step_apply() -> bool:
    """3. 누락 키 3개 추가."""
    print("=== Step 3: Apply ===")
    for path in TARGETS:
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        for key, value in NEW_KEYS.items():
            if key in obj:
                print(f"  ✗ {path.name} 에 이미 {key} 존재 — 중단")
                return False
            obj[key] = value

        # JSON 직렬화 (기존 indent=2, ensure_ascii=False 패턴 유지)
        new_raw = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
        path.write_text(new_raw, encoding="utf-8")
        print(f"  ✓ {path.name} ({path.stat().st_size} bytes)")
    print()
    return True


def step_post_check() -> bool:
    """4. 적용 후 상태 검증."""
    print("=== Step 4: Post-check ===")
    ok = True

    hashes = []
    for path in TARGETS:
        h = short_hash(path)
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        keys = list(obj.keys())

        # 키 개수 12개 검증
        count_ok = len(keys) == EXPECTED_KEY_COUNT_AFTER
        # 누락 키 모두 존재
        all_present = all(k in obj for k in NEW_KEYS)
        # 값 일치
        values_ok = all(obj[k] == v for k, v in NEW_KEYS.items())

        marker_c = "✓" if count_ok else "✗"
        marker_p = "✓" if all_present else "✗"
        marker_v = "✓" if values_ok else "✗"

        print(f"  [{path.name}] hash {h}")
        print(f"    {marker_c} key count {len(keys)} (expect {EXPECTED_KEY_COUNT_AFTER})")
        print(f"    {marker_p} new keys present: {all_present}")
        print(f"    {marker_v} new values match intent: {values_ok}")

        if not (count_ok and all_present and values_ok):
            ok = False
        hashes.append(h)

    # 글로벌 ↔ repo hash 일치
    if len(set(hashes)) == 1:
        print(f"  ✓ 글로벌 ↔ repo hash 일치: {hashes[0]}")
    else:
        print(f"  ✗ 글로벌 ↔ repo hash 불일치: {hashes}")
        ok = False

    print()
    return ok


def main() -> int:
    if not step_precondition():
        print("[FAIL] Precondition 미충족 — 적용 중단")
        return 1
    if not step_backup():
        print("[FAIL] Backup 단계 실패 — 적용 중단")
        return 2
    if not step_apply():
        print("[FAIL] Apply 단계 실패")
        return 3
    if not step_post_check():
        print("[FAIL] Post-check 실패 — 결과 확인 필요")
        return 4

    print("[OK] 변형 G3 적용 완료. Mickey 27 부팅 후 ListAgents → ping 검증 필요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
