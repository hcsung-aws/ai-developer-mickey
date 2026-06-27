# -*- coding: utf-8 -*-
"""
M27 — Curator vs ai-developer-mickey JSON Deep Diff

목적: M26 의 12개+per-key 측정에서 미흡했던 deep nested 차이를 모두 key path 로 출력.
변형 H (전체 차이 흡수) 의 정확한 변경 목록을 결정하기 위한 정밀 측정 도구.

비교 대상:
  - 비정상: ~/.kiro/agents/knowledge-curator.json (G3 적용 후)
  - 정상:   ~/.kiro/agents/ai-developer-mickey.json (현재 본좌가 사용 중)

출력:
  1. Top-level 키 차이 (M26 동일)
  2. Deep leaf 차이 (key path 단위, 신규)
  3. resources / toolsSettings / hooks 본문 비교 (신규)
  4. prompt raw bytes/라인/패턴 비교 (M26 동일 + 추가 항목)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Windows cp949 환경에서 비-ASCII 출력 시 UnicodeEncodeError 회피 (adaptive.md #8)
sys.stdout.reconfigure(encoding="utf-8")

CURATOR_PATH = Path.home() / ".kiro" / "agents" / "knowledge-curator.json"
MICKEY_PATH = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"


def load_json(path: Path) -> tuple[dict, bytes]:
    """JSON 객체 + raw bytes 반환."""
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def flatten(obj, prefix: str = "") -> dict[str, object]:
    """nested dict/list 를 key path 로 평탄화. 리스트는 [i] 인덱스 사용."""
    out: dict[str, object] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            child = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                out.update(flatten(v, child))
            else:
                out[child] = v
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            child = f"{prefix}[{i}]"
            if isinstance(v, (dict, list)):
                out.update(flatten(v, child))
            else:
                out[child] = v
    else:
        out[prefix] = obj
    return out


def summarize_value(v: object) -> str:
    """leaf 값을 짧게 요약 (긴 문자열은 prefix + 길이)."""
    if isinstance(v, str):
        if len(v) > 60:
            return f"str({len(v)}): {v[:50]!r}…"
        return f"str: {v!r}"
    if isinstance(v, (int, float, bool)) or v is None:
        return f"{type(v).__name__}: {v!r}"
    return f"{type(v).__name__}: {v!r}"


def diff_top_level(a: dict, b: dict, label_a: str, label_b: str) -> None:
    """Top-level 키 차이."""
    keys_a = set(a.keys())
    keys_b = set(b.keys())
    only_a = sorted(keys_a - keys_b)
    only_b = sorted(keys_b - keys_a)
    common = sorted(keys_a & keys_b)
    print("=" * 70)
    print("[1] TOP-LEVEL KEY DIFF")
    print("=" * 70)
    print(f"  {label_a} 전용 키 ({len(only_a)}): {only_a}")
    print(f"  {label_b} 전용 키 ({len(only_b)}): {only_b}")
    print(f"  공통 키 ({len(common)}): {common}")


def diff_leaves(a: dict, b: dict, label_a: str, label_b: str) -> None:
    """Deep leaf 차이 (key path 단위)."""
    flat_a = flatten(a)
    flat_b = flatten(b)
    paths_a = set(flat_a.keys())
    paths_b = set(flat_b.keys())
    only_a = sorted(paths_a - paths_b)
    only_b = sorted(paths_b - paths_a)
    common = paths_a & paths_b
    diff_value = sorted(p for p in common if flat_a[p] != flat_b[p])

    print()
    print("=" * 70)
    print("[2] DEEP LEAF DIFF (key path 단위)")
    print("=" * 70)
    print(f"  {label_a} 전용 path ({len(only_a)}):")
    for p in only_a:
        print(f"    - {p} = {summarize_value(flat_a[p])}")
    print(f"  {label_b} 전용 path ({len(only_b)}):")
    for p in only_b:
        print(f"    + {p} = {summarize_value(flat_b[p])}")
    print(f"  공통 path 중 값 다름 ({len(diff_value)}):")
    for p in diff_value:
        print(f"    ~ {p}")
        print(f"        {label_a}: {summarize_value(flat_a[p])}")
        print(f"        {label_b}: {summarize_value(flat_b[p])}")


def diff_specific_section(a: dict, b: dict, key: str, label_a: str, label_b: str) -> None:
    """특정 섹션 (resources/toolsSettings/hooks) 의 본문 비교."""
    print()
    print("=" * 70)
    print(f"[3] SECTION DIFF — {key}")
    print("=" * 70)
    va = a.get(key, "<key 없음>")
    vb = b.get(key, "<key 없음>")
    print(f"  {label_a}:")
    print(f"    {json.dumps(va, ensure_ascii=False, indent=4) if va != '<key 없음>' else va}")
    print(f"  {label_b}:")
    print(f"    {json.dumps(vb, ensure_ascii=False, indent=4) if vb != '<key 없음>' else vb}")


def diff_prompt(a: dict, b: dict, label_a: str, label_b: str) -> None:
    """prompt 본문의 raw 메트릭 비교."""
    pa = a.get("prompt", "") or ""
    pb = b.get("prompt", "") or ""
    print()
    print("=" * 70)
    print("[4] PROMPT METRICS")
    print("=" * 70)
    metrics = [
        ("char count", len, ""),
        ("byte count (utf-8)", lambda s: len(s.encode("utf-8")), ""),
        ("line count", lambda s: s.count("\n") + 1, ""),
        ("max line length", lambda s: max((len(line) for line in s.splitlines()), default=0), ""),
        ("blank line count", lambda s: sum(1 for line in s.splitlines() if not line.strip()), ""),
        ("'```' (code fence) count", lambda s: s.count("```"), ""),
        ("'`' (single backtick) count", lambda s: s.count("`") - s.count("```") * 3, "single backtick only"),
        ("'**' (bold) count", lambda s: s.count("**"), ""),
        ("'#' (heading) count", lambda s: sum(1 for line in s.splitlines() if line.lstrip().startswith("#")), ""),
        ("list item ('- ' or '* ') count", lambda s: sum(1 for line in s.splitlines() if line.lstrip()[:2] in ("- ", "* ")), ""),
        ("table pipe ('|') count", lambda s: s.count("|"), ""),
    ]
    for name, fn, note in metrics:
        va = fn(pa)
        vb = fn(pb)
        marker = "  " if va == vb else "★ "
        suffix = f"  ({note})" if note else ""
        print(f"  {marker}{name}: {label_a}={va}, {label_b}={vb}{suffix}")


def main() -> int:
    if not CURATOR_PATH.exists():
        print(f"[ERR] curator file not found: {CURATOR_PATH}", file=sys.stderr)
        return 1
    if not MICKEY_PATH.exists():
        print(f"[ERR] mickey file not found: {MICKEY_PATH}", file=sys.stderr)
        return 1

    cur, cur_raw = load_json(CURATOR_PATH)
    mck, mck_raw = load_json(MICKEY_PATH)
    label_cur = "curator"
    label_mck = "mickey "

    print(f"# M27 Deep Diff: {label_cur} vs {label_mck}")
    print(f"# curator: {CURATOR_PATH} ({len(cur_raw)} bytes)")
    print(f"# mickey : {MICKEY_PATH} ({len(mck_raw)} bytes)")
    print()

    diff_top_level(cur, mck, label_cur, label_mck)
    diff_leaves(cur, mck, label_cur, label_mck)
    for key in ("resources", "toolsSettings", "hooks", "tools", "allowedTools", "toolAliases"):
        diff_specific_section(cur, mck, key, label_cur, label_mck)
    diff_prompt(cur, mck, label_cur, label_mck)

    print()
    print("=" * 70)
    print("[DONE] 변형 H 구성 입력으로 사용")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
