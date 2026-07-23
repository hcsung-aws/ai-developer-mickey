# -*- coding: utf-8 -*-
"""M41: Curator 격리 적용 — CURATOR-PROMPT.md(SoT) 동기화 + fs_write 권한 축소.

옵션 A (멀티 세션 충돌 해소):
1. SoT prompt → 활성 JSON + repo JSON 주입 (m37_sync_curator_prompt.py 로직 계승)
2. 양 JSON의 toolsSettings.fs_write.allowedPaths에서 `~/.kiro/mickey/domain/**` 제거
   → Curator의 글로벌 쓰기 자동 승인 회수 (프롬프트 지시 + 권한 이중 차단)
3. repo seed md 동기화 + description 갱신
4. 검증: prompt 일치 + allowedPaths 기대값 + 격리 키워드 존재

백업: 각 대상에 .bak-ai-developer-mickey-m41 (신규 네이밍 규약)
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SOT = Path.home() / ".kiro" / "mickey" / "domain" / "CURATOR-PROMPT.md"
HOME_JSON = Path.home() / ".kiro" / "agents" / "knowledge-curator.json"
REPO = Path(__file__).resolve().parent.parent
REPO_JSON = REPO / "examples" / "knowledge-curator.json"
REPO_MD = REPO / "mickey" / "domain" / "CURATOR-PROMPT.md"

BAK_SUFFIX = ".bak-ai-developer-mickey-m41"

# 격리 후 기대 allowedPaths (domain/** 제거)
EXPECTED_ALLOWED = ["**/context_rule/adaptive.md", "**/_curator-staging/**"]
REMOVED_PATH = "~/.kiro/mickey/domain/**"

NEW_DESCRIPTION = (
    "Mickey 세션 종료 시 호출되는 지식 관리 에이전트. 글로벌 영역은 쓰지 않는다(격리 원칙, M41) — "
    "adaptive.md 는 직접 수정, 글로벌 domain/ 후보는 gd- 승격 번들, 그 외 (common_knowledge/, "
    "context_rule/, patterns/, REMEMBER) 는 프로젝트 _curator-staging/ 에 초안 작성. "
    "글로벌 반영은 사용자 승인 후 promote_knowledge.py(락 직렬화)가 수행한다."
)


def backup(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + BAK_SUFFIX)
    if not bak.exists():  # 재실행 시 원본 백업 보존
        shutil.copy2(p, bak)
    return bak


def apply_json(json_path: Path, prompt_text: str):
    """prompt 주입 + allowedPaths 축소 + description 갱신. 나머지 필드 보존."""
    backup(json_path)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    data["prompt"] = prompt_text
    data["description"] = NEW_DESCRIPTION
    fs = data.setdefault("toolsSettings", {}).setdefault("fs_write", {})
    fs["allowedPaths"] = [p for p in fs.get("allowedPaths", []) if p != REMOVED_PATH]
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")


def main() -> int:
    md = SOT.read_text(encoding="utf-8")
    print(f"SoT: {SOT} ({len(md)} chars)")

    for target in (HOME_JSON, REPO_JSON):
        apply_json(target, md)
        print(f"[OK] prompt 주입 + 권한 축소: {target}")

    backup(REPO_MD)
    shutil.copy2(SOT, REPO_MD)
    print(f"[OK] seed 동기화: {REPO_MD}")

    # ── 검증 ──────────────────────────────────────────────────────
    ok = True

    def check(cond: bool, label: str):
        nonlocal ok
        ok &= cond
        print(f"[{'PASS' if cond else 'FAIL'}] {label}")

    for target in (HOME_JSON, REPO_JSON):
        data = json.loads(target.read_text(encoding="utf-8"))
        check(data["prompt"] == md, f"{target.name}: prompt == SoT")
        allowed = data["toolsSettings"]["fs_write"]["allowedPaths"]
        check(allowed == EXPECTED_ALLOWED,
              f"{target.name}: allowedPaths == {EXPECTED_ALLOWED} (실제 {allowed})")
        check(REMOVED_PATH not in json.dumps(data["toolsSettings"]),
              f"{target.name}: domain/** 잔존 없음")
    check(REPO_MD.read_bytes() == SOT.read_bytes(), "repo seed md == SoT")

    # 격리 프롬프트 키워드 (기존 보정 3항목 + 신규 격리 항목)
    for kw in ("격리 원칙", "글로벌 쓰기 금지", "gd- 승격 번들 형식",
               "promote_knowledge.py", "세션 경계 (Session Boundary)",
               "전체 변경 목록 (누락 금지)"):
        check(kw in md, f"SoT 키워드: {kw}")
    # 폐기된 지시 잔존 검사
    for stale in ("Last Updated 명의 = 호출 세션", "domain/ 수정 (크로스 프로젝트 지식)"):
        check(stale not in md, f"폐기 지시 잔존 없음: {stale}")

    print(f"\n결과: {'ALL PASS' if ok else 'FAIL 존재'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
