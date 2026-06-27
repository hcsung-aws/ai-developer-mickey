# -*- coding: utf-8 -*-
"""
M27 — Curator 변형 H 적용 (전체 차이 흡수)

변경 내용 (G3 → H):
  + resources = ["file://AGENTS.md", "file://README.md"]
  + toolsSettings.execute_bash.allowedCommands = [5건, mickey 와 동일]
  + toolsSettings.subagent.availableAgents = []         (키 추가, 값 빈 배열)
  + toolsSettings.subagent.trustedAgents = []           (키 추가, 값 빈 배열)

미변경 (G3 그대로):
  - name, description, prompt, tools, allowedTools, toolAliases, hooks
  - mcpServers = {}, useLegacyMcpJson = false, model = null
  - toolsSettings.fs_write (Curator 자동 승인 경로)

4-step 안전 적용 (safe-batch-replace):
  1. precondition: 현재 글로벌+repo 양쪽 hash 가 G3 (5DF8F946DF56833F) 인지 확인
  2. backup: .m27-bak (양쪽)
  3. apply: 위 4개 항목 추가 (메모리에서 일괄 변환 → 한 번에 쓰기)
  4. post-check: 글로벌+repo hash 일치 + 키-값 일치 검증
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CURATOR_GLOBAL = Path.home() / ".kiro" / "agents" / "knowledge-curator.json"
CURATOR_REPO = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\examples\knowledge-curator.json")

EXPECTED_HASH_G3 = "5DF8F946DF56833F"  # M26 G3 적용 후 hash (precondition)


def file_hash(path: Path) -> str:
    """파일 내용의 SHA-256 앞 16자 (M25/M26 와 동일 형식)."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def load_curator(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_curator(path: Path, obj: dict) -> None:
    """원본 JSON 형식 보존 (indent=2, ensure_ascii=False, 줄바꿈 trailing newline 없음)."""
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")


def step1_precondition() -> tuple[str, str]:
    """글로벌+repo 양쪽 hash 가 G3 와 일치하는지 확인."""
    print("[STEP 1] precondition — G3 hash 확인")
    h_global = file_hash(CURATOR_GLOBAL)
    h_repo = file_hash(CURATOR_REPO)
    print(f"  글로벌: {CURATOR_GLOBAL.name} hash = {h_global}")
    print(f"  repo  : {CURATOR_REPO.name} hash = {h_repo}")
    if h_global != EXPECTED_HASH_G3:
        raise SystemExit(f"[ABORT] 글로벌 hash 가 G3({EXPECTED_HASH_G3}) 와 다름: {h_global}")
    if h_repo != EXPECTED_HASH_G3:
        raise SystemExit(f"[ABORT] repo hash 가 G3({EXPECTED_HASH_G3}) 와 다름: {h_repo}")
    if h_global != h_repo:
        raise SystemExit("[ABORT] 글로벌 ↔ repo hash 불일치")
    print("  [OK] 양쪽 모두 G3 상태")
    return h_global, h_repo


def step2_backup() -> None:
    """.m27-bak 생성 (양쪽)."""
    print()
    print("[STEP 2] backup — .m27-bak 생성")
    for src in (CURATOR_GLOBAL, CURATOR_REPO):
        dst = src.with_name(src.name + ".m27-bak")
        if dst.exists():
            print(f"  [SKIP] 이미 존재: {dst.name}")
            continue
        shutil.copy2(src, dst)
        print(f"  [OK]   {src.name} → {dst.name} ({dst.stat().st_size} bytes)")


def apply_variant_h(obj: dict) -> dict:
    """변형 H 적용 — resources + toolsSettings 의 execute_bash/subagent 키 추가."""
    # resources: mickey 와 동일
    obj["resources"] = ["file://AGENTS.md", "file://README.md"]

    # toolsSettings: 기존 fs_write 유지 + execute_bash + subagent 추가
    ts = obj.setdefault("toolsSettings", {})
    ts["execute_bash"] = {
        "allowedCommands": [
            "ls MICKEY-.*",
            "ls PROJECT-OVERVIEW\\.md.*",
            "cat MICKEY-.*-SESSION\\.md",
            "cat MICKEY-.*-HANDOFF\\.md",
            "cat PROJECT-OVERVIEW\\.md",
        ],
    }
    ts["subagent"] = {
        "availableAgents": [],
        "trustedAgents": [],
    }
    return obj


def step3_apply() -> None:
    """글로벌+repo 양쪽에 변형 H 적용."""
    print()
    print("[STEP 3] apply — 변형 H 적용")
    for path in (CURATOR_GLOBAL, CURATOR_REPO):
        obj = load_curator(path)
        before_keys = {
            "resources_len": len(obj.get("resources", [])),
            "toolsSettings_keys": list(obj.get("toolsSettings", {}).keys()),
        }
        obj = apply_variant_h(obj)
        save_curator(path, obj)
        after_keys = {
            "resources_len": len(obj["resources"]),
            "toolsSettings_keys": list(obj["toolsSettings"].keys()),
        }
        h = file_hash(path)
        size = path.stat().st_size
        print(f"  [OK] {path.name}")
        print(f"       hash = {h}, size = {size} bytes")
        print(f"       resources: {before_keys['resources_len']} → {after_keys['resources_len']}")
        print(f"       toolsSettings keys: {before_keys['toolsSettings_keys']} → {after_keys['toolsSettings_keys']}")


def step4_post_check() -> None:
    """글로벌+repo hash 일치 + 키-값 일치 검증."""
    print()
    print("[STEP 4] post-check — 글로벌 ↔ repo 일치 검증")
    h_global = file_hash(CURATOR_GLOBAL)
    h_repo = file_hash(CURATOR_REPO)
    print(f"  글로벌: hash = {h_global}, size = {CURATOR_GLOBAL.stat().st_size} bytes")
    print(f"  repo  : hash = {h_repo}, size = {CURATOR_REPO.stat().st_size} bytes")
    if h_global != h_repo:
        raise SystemExit("[FAIL] 글로벌 ↔ repo hash 불일치")
    if h_global == EXPECTED_HASH_G3:
        raise SystemExit("[FAIL] hash 가 G3 와 동일 — apply 누락")
    print("  [OK] 양쪽 일치 + G3 와 다름")

    # 추가 검증: H 의 4가지 변경 사항이 실제로 반영됐는지 키-값 확인
    obj = load_curator(CURATOR_GLOBAL)
    checks = [
        ("resources 길이=2", len(obj.get("resources", [])) == 2),
        ("toolsSettings.execute_bash 존재", "execute_bash" in obj.get("toolsSettings", {})),
        ("toolsSettings.subagent 존재", "subagent" in obj.get("toolsSettings", {})),
        ("toolsSettings.fs_write 보존", "fs_write" in obj.get("toolsSettings", {})),
        ("mcpServers={} (G3 유지)", obj.get("mcpServers") == {}),
        ("model=null (G3 유지)", obj.get("model") is None),
    ]
    for name, ok in checks:
        marker = "[OK]" if ok else "[FAIL]"
        print(f"  {marker} {name}")
        if not ok:
            raise SystemExit(f"[FAIL] 검증 실패: {name}")


def main() -> int:
    print("# M27 변형 H 적용 (Curator 전체 차이 흡수)")
    print(f"# 글로벌: {CURATOR_GLOBAL}")
    print(f"# repo  : {CURATOR_REPO}")
    print()
    step1_precondition()
    step2_backup()
    step3_apply()
    step4_post_check()
    print()
    print("=" * 60)
    print("[DONE] 변형 H 디스크 반영 완료. Mickey 28 부팅 후 ping 검증 인계.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
