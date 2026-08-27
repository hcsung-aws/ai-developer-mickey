# M45: staging의 augment 번들에서 Base-Hash: pending 을 대상 entry의 실제 sha256으로 스탬프
# (CURATOR-PROMPT 규약 — Curator는 pending으로 두고 Mickey가 승격 직전 스탬프)
import sys, hashlib, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

STAGING = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey\_curator-staging")
DOMAIN = Path.home() / ".kiro" / "mickey" / "domain"

for f in sorted(STAGING.glob("gd-*.md")):
    text = f.read_text(encoding="utf-8")
    if "Base-Hash: pending" not in text:
        continue
    m = re.search(r"^Entry-Path:\s*(.+)$", text, re.MULTILINE)
    if not m:
        print(f"[FAIL] {f.name}: Entry-Path 없음")
        continue
    entry = DOMAIN / m.group(1).strip()
    if not entry.exists():
        print(f"[FAIL] {f.name}: 대상 entry 부재 ({entry})")
        continue
    h = hashlib.sha256(entry.read_bytes()).hexdigest()
    f.write_text(text.replace("Base-Hash: pending", f"Base-Hash: {h}"), encoding="utf-8")
    print(f"[OK] {f.name}: Base-Hash = {h[:12]}... ({m.group(1).strip()})")
