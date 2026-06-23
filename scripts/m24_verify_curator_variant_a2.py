"""
Mickey 24 — knowledge-curator.json 변형 A2 적용 후 JSON 유효성 검증.
글로벌 + repo 양쪽을 파싱하여 tools/allowedTools 형식이 의도대로 변경되었는지 확인.
"""
import sys
import json
from pathlib import Path

# Windows cp949 회피 — 비-ASCII 출력을 위해 utf-8 강제
sys.stdout.reconfigure(encoding="utf-8")

TARGETS = [
    Path.home() / ".kiro/agents/knowledge-curator.json",
    Path("C:/Users/hcsung/work/kiro/ai-developer-mickey/examples/knowledge-curator.json"),
]

EXPECTED_TOOLS = ["*"]
EXPECTED_ALLOWED = {"fs_read", "fs_write", "grep", "glob"}


def verify(p: Path) -> dict:
    """단일 파일을 파싱하여 변형 A2 적용 결과를 검증."""
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    return {
        "path": str(p),
        "json_valid": True,
        "tools": data.get("tools"),
        "allowedTools": data.get("allowedTools"),
        "tools_match": data.get("tools") == EXPECTED_TOOLS,
        "allowed_match": set(data.get("allowedTools") or []) == EXPECTED_ALLOWED,
        "model": data.get("model"),
        "name": data.get("name"),
    }


def main() -> int:
    """모든 대상에 대해 검증 후 1건이라도 실패하면 비-제로 종료."""
    failed = 0
    for t in TARGETS:
        try:
            r = verify(t)
            ok = r["tools_match"] and r["allowed_match"]
            print(f"[{'OK' if ok else 'FAIL'}] {r['path']}")
            print(f"    tools       = {r['tools']}")
            print(f"    allowedTools= {r['allowedTools']}")
            print(f"    model       = {r['model']}")
            if not ok:
                failed += 1
        except Exception as e:
            print(f"[ERROR] {t}: {e}")
            failed += 1
    print(f"\nResult: {len(TARGETS) - failed}/{len(TARGETS)} OK")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
