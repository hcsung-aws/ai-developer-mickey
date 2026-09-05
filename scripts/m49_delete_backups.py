# -*- coding: utf-8 -*-
"""M49 백업 삭제 (destructive-target-strict-matching 준수)

대상: 명시 목록 4건만 — 패턴/glob 매칭 금지, 정확 경로만 삭제.
근거:
- .bak-m48: M49 serena 검증 PASS (m49_serena_verify.py) → 삭제 시점 도래
- M47 백업 3종: Option A 검증 완료 (M48 HANDOFF Next Steps 1항)
절차: 삭제 전 존재 실측 → 삭제 → 부재 실측 (이중 확인)
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME = Path.home()

# 삭제 대상 — 명시 목록만 (여기 없는 파일은 절대 건드리지 않음)
TARGETS = [
    HOME / ".serena" / "serena_config.yml.bak-m48",
    HOME / ".kiro" / "agents" / "ai-developer-mickey.json.bak-m47-serena",
    HOME / ".kiro" / "settings" / "mcp.json.bak-m47-serena",
    HOME / ".kiro" / "mickey" / "extended-protocols.md.bak-ai-developer-mickey-m47",
]


def main() -> int:
    print("=== M49 backup deletion ===")
    failed = False
    for t in TARGETS:
        if not t.exists():
            print(f"[SKIP] not found: {t}")
            continue
        size = t.stat().st_size
        t.unlink()
        gone = not t.exists()  # 삭제 후 부재 실측
        print(f"[{'DELETED' if gone else 'FAIL'}] {t} ({size} bytes)")
        if not gone:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
