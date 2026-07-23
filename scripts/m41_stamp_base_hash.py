# -*- coding: utf-8 -*-
"""M41: augment 승격 번들에 Base-Hash 스탬프 — 낙관적 동시성 검증 전제 확정.

Curator는 승격 시점의 대상 entry 해시를 알 수 없으므로 'pending'으로 두고,
Mickey가 promote 실행 직전에 디스크 실측 해시로 교체한다 (§17 락 규약).
"""
import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BUNDLE = Path(__file__).resolve().parent.parent / "_curator-staging" / "gd-prompt-doc-vs-runtime-loading-augment.md"
TARGET = Path.home() / ".kiro" / "mickey" / "domain" / "entries" / "prompt-doc-vs-runtime-loading.md"

digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
text = BUNDLE.read_text(encoding="utf-8")
n = text.count("Base-Hash: pending")
if n != 1:
    print(f"[FAIL] 'Base-Hash: pending' count={n} (기대 1)")
    sys.exit(1)
BUNDLE.write_text(text.replace("Base-Hash: pending", f"Base-Hash: {digest}"),
                  encoding="utf-8")
print(f"[OK] Base-Hash 스탬프: {digest[:16]}... → {BUNDLE.name}")
