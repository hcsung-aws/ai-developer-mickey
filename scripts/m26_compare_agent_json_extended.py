"""
M26 — Curator vs ai-developer-mickey 확장 정밀 비교.
M25 측정에서 빠진 차원을 점검하기 위한 확장판.
A1 (allowedTools=[]) 적용 후에도 EmptyResponse 재현 — 남은 차이 식별.
"""

import json
import os
import sys
from pathlib import Path

# Windows cp949 환경 대응 (adaptive.md Rule #8)
sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(os.path.expandvars("%USERPROFILE%"))
GLOBAL_AGENTS = HOME / ".kiro" / "agents"

TARGETS = {
    "curator (비정상)": GLOBAL_AGENTS / "knowledge-curator.json",
    "ai-developer-mickey (정상)": GLOBAL_AGENTS / "ai-developer-mickey.json",
}


def measure_raw(label: str, path: Path) -> dict:
    """파일 raw 측정 — 인코딩, BOM, line ending 등 JSON 파싱 전 차원."""
    raw_bytes = path.read_bytes()
    has_bom = raw_bytes.startswith(b"\xef\xbb\xbf")  # UTF-8 BOM
    crlf = raw_bytes.count(b"\r\n")
    lf_only = raw_bytes.count(b"\n") - crlf
    return {
        "size_bytes": len(raw_bytes),
        "bom": has_bom,
        "crlf_count": crlf,
        "lf_count": lf_only,
    }


def measure_json(label: str, path: Path) -> dict:
    """JSON 파싱 후 구조적 측정 — top-level 키, prompt 내부 통계."""
    raw = path.read_text(encoding="utf-8-sig")  # BOM tolerant
    obj = json.loads(raw)

    prompt = obj.get("prompt", "")
    keys = list(obj.keys())

    # prompt 라인별 통계
    lines = prompt.split("\n")
    max_line_len = max((len(line) for line in lines), default=0)
    blank_lines = sum(1 for line in lines if not line.strip())

    # 특수 패턴 카운트
    pattern_counts = {
        "triple_backtick": prompt.count("```"),
        "single_backtick": prompt.count("`") - prompt.count("```") * 3,
        "asterisk_bold": prompt.count("**") // 2,
        "headers_h1": prompt.count("\n# ") + (1 if prompt.startswith("# ") else 0),
        "headers_h2": prompt.count("\n## "),
        "headers_h3": prompt.count("\n### "),
        "list_dash": prompt.count("\n- "),
        "list_numbered": sum(1 for line in lines if line.lstrip()[:2].rstrip(".").isdigit()),
        "table_pipes": prompt.count("|"),
        "tab_chars": prompt.count("\t"),
        "non_breaking_space": prompt.count("\u00a0"),
        "zero_width": prompt.count("\u200b") + prompt.count("\ufeff"),
    }

    return {
        "top_level_keys": keys,
        "key_count": len(keys),
        "prompt_length": len(prompt),
        "prompt_lines": len(lines),
        "prompt_max_line": max_line_len,
        "prompt_blank_lines": blank_lines,
        "patterns": pattern_counts,
        "name": obj.get("name", ""),
        "description_length": len(obj.get("description", "")),
        "tools": obj.get("tools", []),
        "allowedTools": obj.get("allowedTools", []),
        "model": obj.get("model"),
    }


def per_key_summary(obj: dict) -> dict:
    """JSON top-level 각 키의 값 유형/크기 요약."""
    summary = {}
    for key, value in obj.items():
        if isinstance(value, str):
            summary[key] = f"str (len={len(value)})"
        elif isinstance(value, list):
            summary[key] = f"list (n={len(value)})"
        elif isinstance(value, dict):
            summary[key] = f"dict (keys={len(value)})"
        elif value is None:
            summary[key] = "null"
        else:
            summary[key] = f"{type(value).__name__} (={value})"
    return summary


def render_diff(label_a: str, data_a: dict, label_b: str, data_b: dict) -> None:
    print(f"=== Diff: {label_a} vs {label_b} ===")
    keys = sorted(set(data_a.keys()) | set(data_b.keys()))
    for k in keys:
        v_a = data_a.get(k, "<missing>")
        v_b = data_b.get(k, "<missing>")
        marker = "  " if v_a == v_b else "★ "
        print(f"  {marker}{k}: {v_a}  |  {v_b}")
    print()


def main() -> int:
    if any(not p.exists() for p in TARGETS.values()):
        for label, path in TARGETS.items():
            if not path.exists():
                print(f"[{label}] NOT FOUND: {path}")
        return 1

    raw_results = {}
    json_results = {}
    key_summaries = {}

    for label, path in TARGETS.items():
        raw_results[label] = measure_raw(label, path)
        json_results[label] = measure_json(label, path)
        key_summaries[label] = per_key_summary(
            json.loads(path.read_text(encoding="utf-8-sig"))
        )

    # 1. Raw 측정 비교
    labels = list(TARGETS.keys())
    render_diff(labels[0], raw_results[labels[0]], labels[1], raw_results[labels[1]])

    # 2. JSON top-level 키 비교
    print("=== Top-level Keys ===")
    for label in labels:
        keys = json_results[label]["top_level_keys"]
        print(f"  {label}: {keys}")
    print()

    # 3. 각 키의 값 유형/크기
    print("=== Per-Key Summary ===")
    all_keys = sorted(set().union(*(s.keys() for s in key_summaries.values())))
    for k in all_keys:
        a = key_summaries[labels[0]].get(k, "<missing>")
        b = key_summaries[labels[1]].get(k, "<missing>")
        marker = "  " if a == b else "★ "
        print(f"  {marker}{k}: {a}  |  {b}")
    print()

    # 4. JSON 구조 측정 비교
    print("=== JSON Structure ===")
    for k in ("key_count", "prompt_length", "prompt_lines", "prompt_max_line",
              "prompt_blank_lines", "description_length"):
        a = json_results[labels[0]].get(k)
        b = json_results[labels[1]].get(k)
        marker = "  " if a == b else "★ "
        print(f"  {marker}{k}: {a}  |  {b}")
    print()

    # 5. tools/allowedTools/model 비교
    print("=== Tool Config ===")
    for k in ("tools", "allowedTools", "model"):
        a = json_results[labels[0]].get(k)
        b = json_results[labels[1]].get(k)
        marker = "  " if a == b else "★ "
        print(f"  {marker}{k}: {a}  |  {b}")
    print()

    # 6. Prompt 패턴 비교
    print("=== Prompt Patterns ===")
    pat_a = json_results[labels[0]]["patterns"]
    pat_b = json_results[labels[1]]["patterns"]
    pat_keys = sorted(set(pat_a.keys()) | set(pat_b.keys()))
    for k in pat_keys:
        a = pat_a.get(k, 0)
        b = pat_b.get(k, 0)
        marker = "  " if a == b else "★ "
        print(f"  {marker}{k}: {a}  |  {b}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
