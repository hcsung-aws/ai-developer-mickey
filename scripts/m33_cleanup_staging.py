# -*- coding: utf-8 -*-
"""
m33_cleanup_staging.py
Mickey 33 세션 종료 시 처리된 Pre-staged 초안 파일 3건을 삭제한다.
사용자 승인 반영 후 정식 위치로 이동 완료된 항목만 대상.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STAGING = pathlib.Path.home() / ".kiro" / "mickey" / "_curator-staging"
TARGETS = [
    "dom-windows-user-path-extension.md",
    "dom-kiro-cli-lsp-init-settings-location.md",
    "machine-env-lsp-servers.md",
]

for name in TARGETS:
    path = STAGING / name
    if path.exists():
        path.unlink()
        print(f"[DEL]  {path}")
    else:
        print(f"[SKIP] not found: {path}")

# 남은 staging 항목 확인 (ownership 가드용)
remaining = list(STAGING.glob("*"))
print(f"[REMAIN] {len(remaining)} items in staging")
for item in remaining:
    print(f"  - {item.name}")
