# -*- coding: utf-8 -*-
# 목적: 글로벌 mcp.json + 모든 agent JSON 의 MCP/legacy 관련 필드 한눈에 비교
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME = Path.home()
MCP_JSON = HOME / ".kiro" / "settings" / "mcp.json"
AGENTS_DIR = HOME / ".kiro" / "agents"


def safe_read_json(p: Path):
    """비-JSON 또는 missing 도 안전하게 처리"""
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return f"<parse error: {e}>"


def main() -> int:
    print("=" * 80)
    print("GLOBAL mcp.json")
    print("=" * 80)
    mcp = safe_read_json(MCP_JSON)
    if isinstance(mcp, dict):
        servers = mcp.get("mcpServers") or {}
        print(f"keys: {sorted(mcp.keys())}")
        print(f"mcpServers count: {len(servers)}")
        for name, cfg in servers.items():
            disabled = cfg.get("disabled") if isinstance(cfg, dict) else None
            cmd = cfg.get("command") if isinstance(cfg, dict) else None
            print(f"  - {name}: disabled={disabled}, command={cmd}")
    else:
        print(repr(mcp))

    print()
    print("=" * 80)
    print("AGENT JSON SUMMARY (MCP / legacy / mcp.json inclusion)")
    print("=" * 80)
    rows = []
    for f in sorted(AGENTS_DIR.iterdir()):
        if not f.name.endswith(".json"):
            continue
        if ".bak" in f.name or "example" in f.name:
            continue
        j = safe_read_json(f)
        if not isinstance(j, dict):
            rows.append((f.name, "<error>", "", "", "", ""))
            continue
        mcp_keys = list((j.get("mcpServers") or {}).keys())
        legacy = j.get("useLegacyMcpJson")
        include = j.get("includeMcpJson")
        tools = j.get("tools")
        allowed = j.get("allowedTools")
        rows.append((
            f.name,
            ",".join(mcp_keys) if mcp_keys else "(empty)",
            str(legacy),
            str(include),
            str(tools),
            str(allowed),
        ))
    header = ("file", "mcpServers", "useLegacy", "includeMcp", "tools", "allowedTools")
    width = [max(len(str(r[i])) for r in [header] + rows) for i in range(6)]
    print(" | ".join(h.ljust(width[i]) for i, h in enumerate(header)))
    print("-+-".join("-" * w for w in width))
    for r in rows:
        print(" | ".join(str(c).ljust(width[i]) for i, c in enumerate(r)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
