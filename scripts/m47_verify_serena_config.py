# M47: Option A 적용 검증 — 수정된 JSON 2건의 파싱 유효성 + serena args 실측 확인
import json
import sys
import io
from pathlib import Path

# Windows cp949 콘솔 UnicodeEncodeError 방지 (adaptive #8)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HOME = Path.home()
TARGETS = [
    HOME / ".kiro" / "agents" / "ai-developer-mickey.json",
    HOME / ".kiro" / "settings" / "mcp.json",
]

ok = True
for path in TARGETS:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] {path.name}: JSON 파싱 실패 — {e}")
        ok = False
        continue
    # serena args를 실제 파싱 결과에서 추출하여 --project 잔존 여부 확인
    servers = data.get("mcpServers", {})
    serena = servers.get("serena", {})
    args = serena.get("args", [])
    has_project = "--project" in args
    print(f"[{'FAIL' if has_project else 'PASS'}] {path.name}: serena args = {args}")
    if has_project:
        ok = False

sys.exit(0 if ok else 1)
