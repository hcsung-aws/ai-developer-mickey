# -*- coding: utf-8 -*-
"""
M28 — Curator 변형 I 적용 (옵션 B: includeMcpJson 추가 + useLegacyMcpJson 제거)

가설 (M28 외부 이슈 조사):
  Curator 의 `includeMcpJson` 누락 → default 동작으로 글로벌 ~/.kiro/settings/mcp.json
  의 3개 MCP server (aws-knowledge / aws-api / serena) 자동 attach →
  Anthropic claude-code Issue #17743 패턴 (MCP configured + subagent → 0 tool uses)
  으로 EmptyResponse 트리거.

변경 내용 (H → I):
  - useLegacyMcpJson  ← 제거 (매뉴얼 미명시 deprecated 필드)
  + includeMcpJson: false  ← 정식 필드, 글로벌 mcp.json 명시 차단

미변경 (H 그대로):
  mcpServers = {}, model = null,
  resources, tools, allowedTools, toolsSettings, prompt, hooks 등 모두 유지

4-step 안전 적용 (safe-batch-replace, M27 패턴 6세대):
  1. precondition: 현재 글로벌+repo 양쪽 hash 가 H (F65CAF62C5DBDD0F) + 두 키 상태 검증
  2. backup: .m28-bak (양쪽)
  3. apply: useLegacyMcpJson 제거 + includeMcpJson:false 추가 (메모리 일괄)
  4. post-check: 글로벌+repo hash 일치 + 두 키 상태 검증
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

EXPECTED_HASH_H = "F65CAF62C5DBDD0F"  # M27 H 적용 후 hash (precondition)
BAK_SUFFIX = ".m28-bak"


def file_hash(path: Path) -> str:
    """SHA-256 앞 16자 (M25/M26/M27 와 동일 형식)."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def load_curator(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_curator(path: Path, obj: dict) -> None:
    """원본 JSON 형식 보존 (indent=2, ensure_ascii=False, no trailing newline)."""
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")


def step1_precondition() -> str:
    """글로벌+repo hash 가 H 와 일치하고, useLegacyMcpJson 존재 + includeMcpJson 부재 확인."""
    print("[STEP 1] precondition — H hash + 두 키 상태 확인")
    h_global = file_hash(CURATOR_GLOBAL)
    h_repo = file_hash(CURATOR_REPO)
    print(f"  글로벌: {CURATOR_GLOBAL.name} hash = {h_global}")
    print(f"  repo  : {CURATOR_REPO.name} hash = {h_repo}")
    if h_global != EXPECTED_HASH_H:
        raise SystemExit(f"[ABORT] 글로벌 hash 가 H({EXPECTED_HASH_H}) 와 다름: {h_global}")
    if h_repo != EXPECTED_HASH_H:
        raise SystemExit(f"[ABORT] repo hash 가 H({EXPECTED_HASH_H}) 와 다름: {h_repo}")
    if h_global != h_repo:
        raise SystemExit("[ABORT] 글로벌 ↔ repo hash 불일치")

    # 두 키 상태 (의미적 검증)
    g = load_curator(CURATOR_GLOBAL)
    has_legacy = "useLegacyMcpJson" in g
    has_include = "includeMcpJson" in g
    print(f"  글로벌 useLegacyMcpJson 존재: {has_legacy}")
    print(f"  글로벌 includeMcpJson 존재  : {has_include}")
    if not has_legacy:
        raise SystemExit("[ABORT] useLegacyMcpJson 키가 없음 (제거 대상 부재)")
    if has_include:
        raise SystemExit("[ABORT] includeMcpJson 키가 이미 존재 (예상치 못한 상태)")

    print("  [OK] 양쪽 H + 두 키 상태 일치")
    return h_global


def step2_backup() -> None:
    """.m28-bak 생성 (양쪽)."""
    print()
    print(f"[STEP 2] backup — {BAK_SUFFIX} 생성")
    for src in (CURATOR_GLOBAL, CURATOR_REPO):
        dst = src.with_name(src.name + BAK_SUFFIX)
        if dst.exists():
            print(f"  [SKIP] 이미 존재: {dst.name}")
            continue
        shutil.copy2(src, dst)
        print(f"  [OK]   {src.name} → {dst.name} ({dst.stat().st_size} bytes)")


def transform(obj: dict) -> dict:
    """변형 I: useLegacyMcpJson 제거 + includeMcpJson:false 추가 (in-place)."""
    obj.pop("useLegacyMcpJson", None)
    # includeMcpJson 은 매뉴얼 정식 필드이므로 명시적으로 false 로 차단
    obj["includeMcpJson"] = False
    return obj


def step3_apply() -> None:
    """글로벌+repo 동시 변형 I 적용 (메모리에서 변환 후 한 번에 저장)."""
    print()
    print("[STEP 3] apply — useLegacyMcpJson 제거 + includeMcpJson:false 추가")
    g = transform(load_curator(CURATOR_GLOBAL))
    r = transform(load_curator(CURATOR_REPO))
    save_curator(CURATOR_GLOBAL, g)
    save_curator(CURATOR_REPO, r)
    print(f"  [OK]   글로벌 + repo 동시 적용")


def step4_post_check() -> None:
    """양쪽 hash 일치 + 두 키 상태 검증."""
    print()
    print("[STEP 4] post-check — hash 일치 + 두 키 상태")
    h_global = file_hash(CURATOR_GLOBAL)
    h_repo = file_hash(CURATOR_REPO)
    size_global = CURATOR_GLOBAL.stat().st_size
    size_repo = CURATOR_REPO.stat().st_size
    print(f"  글로벌: hash = {h_global}, size = {size_global}")
    print(f"  repo  : hash = {h_repo}, size = {size_repo}")
    if h_global != h_repo:
        raise SystemExit("[ABORT] 적용 후 글로벌 ↔ repo hash 불일치")

    g = load_curator(CURATOR_GLOBAL)
    r = load_curator(CURATOR_REPO)
    if "useLegacyMcpJson" in g or "useLegacyMcpJson" in r:
        raise SystemExit("[ABORT] useLegacyMcpJson 가 여전히 존재")
    if g.get("includeMcpJson") is not False:
        raise SystemExit(f"[ABORT] 글로벌 includeMcpJson 값 이상: {g.get('includeMcpJson')}")
    if r.get("includeMcpJson") is not False:
        raise SystemExit(f"[ABORT] repo includeMcpJson 값 이상: {r.get('includeMcpJson')}")

    print("  [OK] 양쪽 hash 일치 + useLegacyMcpJson 제거 + includeMcpJson=false")


def main() -> int:
    step1_precondition()
    step2_backup()
    step3_apply()
    step4_post_check()
    print()
    print("[DONE] 변형 I 적용 완료. 검증은 Mickey 29 부팅 후 ping.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
