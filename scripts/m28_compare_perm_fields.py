# -*- coding: utf-8 -*-
# 목적: mickey 본체 + curator 의 JSON 권한 관련 필드 비교 추출
# 출력은 시각적으로 비교 가능한 표 형태
import sys
import json
from pathlib import Path

# Windows cp949 콘솔에서 비-ASCII 출력 안전화 (M22 교훈)
sys.stdout.reconfigure(encoding="utf-8")

HOME = Path.home()
MICKEY_PATH = HOME / ".kiro" / "agents" / "ai-developer-mickey.json"
CURATOR_PATH = HOME / ".kiro" / "agents" / "knowledge-curator.json"


def load(p: Path) -> dict:
    """JSON 파일을 dict 로 로딩 — 권한 필드 추출 전제"""
    return json.loads(p.read_text(encoding="utf-8"))


def perm_view(name: str, j: dict) -> dict:
    """권한 모델 비교에 필요한 필드만 추출"""
    return {
        "name": name,
        "tools": j.get("tools"),
        "allowedTools": j.get("allowedTools"),
        "toolsSettings.subagent": (j.get("toolsSettings") or {}).get("subagent"),
        "toolsSettings.execute_bash": (j.get("toolsSettings") or {}).get("execute_bash"),
        "toolsSettings.fs_write": (j.get("toolsSettings") or {}).get("fs_write"),
        "resources": j.get("resources"),
        "hooks_keys": list((j.get("hooks") or {}).keys()),
    }


def main() -> int:
    """양 JSON 의 권한 필드를 동일 키 순서로 dump"""
    mickey = perm_view("ai-developer-mickey", load(MICKEY_PATH))
    curator = perm_view("knowledge-curator", load(CURATOR_PATH))

    print("=" * 80)
    print("PERMISSION FIELDS COMPARE")
    print("=" * 80)
    for key in mickey:
        if key == "name":
            continue
        print(f"\n--- {key} ---")
        print("[mickey]   ", json.dumps(mickey[key], ensure_ascii=False, indent=2))
        print("[curator]  ", json.dumps(curator[key], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
