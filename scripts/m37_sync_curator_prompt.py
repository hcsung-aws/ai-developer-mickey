# -*- coding: utf-8 -*-
"""M37: CURATOR-PROMPT.md (SoT) → agent JSON prompt 필드 동기화.

배경: 런타임 Curator(delegate)는 ~/.kiro/agents/knowledge-curator.json 의 내장 prompt 를
사용하며 CURATOR-PROMPT.md 를 참조하지 않는다. md 수정이 런타임에 전파되려면
JSON prompt 필드를 재주입해야 한다.

동기화 대상 (md = SoT):
1. ~/.kiro/agents/knowledge-curator.json  (활성 런타임)
2. {repo}/examples/knowledge-curator.json (install 배포원)
3. {repo}/mickey/domain/CURATOR-PROMPT.md (seed/세대 관리 — install이 항상 갱신)

각 대상은 수정 전 .m37-bak 백업 생성 (adaptive #10). prompt 외 필드는 보존.
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SOT = Path(r"C:\Users\hcsung\.kiro\mickey\domain\CURATOR-PROMPT.md")
HOME_JSON = Path(r"C:\Users\hcsung\.kiro\agents\knowledge-curator.json")
REPO = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")
REPO_JSON = REPO / "examples" / "knowledge-curator.json"
REPO_MD = REPO / "mickey" / "domain" / "CURATOR-PROMPT.md"

def backup(p: Path):
    bak = p.with_suffix(p.suffix + ".m37-bak")
    shutil.copy2(p, bak)
    return bak

def inject_prompt(json_path: Path, prompt_text: str):
    """prompt 필드만 교체, 나머지 필드(권한/도구 설정) 보존."""
    data = json.loads(json_path.read_text(encoding="utf-8"))
    data["prompt"] = prompt_text
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    md = SOT.read_text(encoding="utf-8")
    print(f"SoT: {SOT} ({len(md)} chars)")

    for target in (HOME_JSON, REPO_JSON):
        bak = backup(target)
        inject_prompt(target, md)
        print(f"[OK] prompt 주입: {target} (백업: {bak.name})")

    backup(REPO_MD)
    shutil.copy2(SOT, REPO_MD)
    print(f"[OK] seed 동기화: {REPO_MD}")

    # 검증: 3곳 모두 SoT 와 일치하는지
    ok = True
    for target in (HOME_JSON, REPO_JSON):
        loaded = json.loads(target.read_text(encoding="utf-8"))["prompt"]
        match = loaded == md
        ok &= match
        print(f"[{'PASS' if match else 'FAIL'}] {target.name} prompt == SoT")
    match = REPO_MD.read_bytes() == SOT.read_bytes()
    ok &= match
    print(f"[{'PASS' if match else 'FAIL'}] repo seed md == SoT")

    # 보정 3항목 키워드 존재 검증
    for kw in ("세션 경계 (Session Boundary)", "전체 변경 목록 (누락 금지)", "Last Updated 명의 = 호출 세션"):
        present = kw in md
        ok &= present
        print(f"[{'PASS' if present else 'FAIL'}] 보정 키워드: {kw}")

    print(f"\n결과: {'ALL PASS' if ok else 'FAIL 존재'}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
