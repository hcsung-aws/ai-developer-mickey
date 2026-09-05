# M47: gd- 번들 Base-Hash 보정
# 배경: Curator가 augment 번들에 Base-Hash를 "pending"으로 남겨 promote가 CONFLICT 스킵.
#       실제 타 세션 변경 여부를 mtime으로 검증한 뒤, 현재 entry sha256을 번들에 기입한다.
import hashlib
import sys
import io
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

GLOBAL_ENTRIES = Path.home() / ".kiro" / "mickey" / "domain" / "entries"
STAGING = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\_curator-staging")
CURATION_TIME = datetime(2026, 9, 5, 12, 4)  # Curator 실행 시각 (리포트 기준)

# 번들 파일명 → 대상 entry 파일명
BUNDLES = {
    "gd-tool-implicit-root-path-trap.md": "tool-implicit-root-path-trap.md",
    "gd-prompt-doc-vs-runtime-loading.md": "prompt-doc-vs-runtime-loading.md",
}

ok = True
for bundle_name, entry_name in BUNDLES.items():
    entry = GLOBAL_ENTRIES / entry_name
    bundle = STAGING / bundle_name

    # 1) 동시 변경 검증: entry 최종 수정이 큐레이션 시각 이후면 실제 drift — 중단
    mtime = datetime.fromtimestamp(entry.stat().st_mtime)
    if mtime > CURATION_TIME:
        print(f"[STOP] {entry_name}: 큐레이션({CURATION_TIME}) 이후 수정됨({mtime}) — 실제 drift, 재큐레이션 필요")
        ok = False
        continue

    # 2) 현재 sha256 계산 후 번들의 "Base-Hash: pending" 치환
    digest = hashlib.sha256(entry.read_bytes()).hexdigest()
    text = bundle.read_text(encoding="utf-8")
    if "Base-Hash: pending" not in text:
        print(f"[SKIP] {bundle_name}: 'Base-Hash: pending' 없음 (이미 보정?)")
        continue
    bundle.write_text(text.replace("Base-Hash: pending", f"Base-Hash: {digest}"), encoding="utf-8")
    print(f"[FIXED] {bundle_name}: entry mtime={mtime} (큐레이션 이전 OK), Base-Hash={digest[:16]}...")

sys.exit(0 if ok else 1)
