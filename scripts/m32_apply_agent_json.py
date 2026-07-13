# -*- coding: utf-8 -*-
"""
M32 Phase B: ai-developer-mickey.json T1 프롬프트 수정 (repo + global 동시).

변경 내용 (4건 일괄, prompt 필드 내부 문자열):
1. SESSION PROTOCOL First Session에 Step 4a 삽입 (Step 4/5 사이)
2. Continuing Session 엔트로피 체크 문장에 "code analysis tool 감지" 추가
3. DOCUMENT SCHEMA FILE-STRUCTURE.md 행 대체 (필수/선택 분리)
4. Version 16 → 17, Last Updated + Changes 갱신

safe-batch-replace 4-step 10세대. JSON escape 함정 회피 위해 json.load/dump 사용.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
GLOBAL_PATH = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"
REPO_PATH = ROOT / "examples" / "ai-developer-mickey.json"

EXPECTED_PRECOND_HASH = "86E6A50F7B96E9B69AAD486873993366CFB688DF52983311B2FD51D1BB76D7F5"

# ─────────────────────────────────────────────────────────────────
# 변경 1: SESSION PROTOCOL First Session — Step 4/5 사이에 4a 삽입
# ─────────────────────────────────────────────────────────────────
OLD_1 = """4. **답변 기반 분석**: 프로젝트 유형에 맞는 파일/구조 탐색
5. **초기 문서 생성** (Document Schema 참조):"""

NEW_1 = """4. **답변 기반 분석**: 프로젝트 유형에 맞는 파일/구조 탐색
4a. **코드 분석 도구 감지 + 안내** (T1.5 §19 참조):
   - `.serena/`, `graphify-out/` 스캔 → Tier 1 감지 시 `common_knowledge/INDEX.md` Tool Links 및 `ENVIRONMENT.md` 에 등록
   - Tier 1 미감지 → 사용자에게 3가지 선택지 제시: ① Serena/Graphify 설치 안내 ② 다른 도구(Tier 2) 지정 ③ Kiro CLI 내장 `code` 도구(Tier 3, baseline)로 진행
   - Tier 3 사용 시 `.kiro/lsp.json` 미존재하면 사용자에게 `/code init` 실행 권장 (LSP 활성 시 정밀 분석 확보)
   - 감지 결과를 `ENVIRONMENT.md` "Code Analysis Tools" 항목에 기록
5. **초기 문서 생성** (Document Schema 참조):"""

# ─────────────────────────────────────────────────────────────────
# 변경 2: Continuing Session 엔트로피 체크 문장 확장
# ─────────────────────────────────────────────────────────────────
OLD_2 = """1b. **엔트로피 체크**: INDEX 정합성, auto_notes 최신성, 오래된 SESSION 아카이빙 필요 여부, `_curator-staging/` dangling 항목, **포스트모템 트리거 조건** 확인 (T1.5 §3 + §17 + §9 참조)"""

NEW_2 = """1b. **엔트로피 체크**: INDEX 정합성, auto_notes 최신성, 오래된 SESSION 아카이빙 필요 여부, `_curator-staging/` dangling 항목, **코드 분석 도구 감지 상태**(`.serena/`, `graphify-out/`, `.kiro/lsp.json` 및 INDEX Tool Links 정합성 — T1.5 §19), **포스트모템 트리거 조건** 확인 (T1.5 §3 + §17 + §9 + §19 참조)"""

# ─────────────────────────────────────────────────────────────────
# 변경 3: DOCUMENT SCHEMA FILE-STRUCTURE.md 행
# ─────────────────────────────────────────────────────────────────
OLD_3 = """| **FILE-STRUCTURE.md** | Directory Tree, Key Files (Config/Source/Docs), File Statistics, Project Structure Pattern, Last Updated |"""

NEW_3 = """| **FILE-STRUCTURE.md** | [필수] Directory Tree (depth 2), Mickey Docs Locations, Code Analysis Tools (§19 감지 결과), Steering Trigger, Last Updated. [선택] Key Files, File Statistics, Project Structure Pattern (Tier 1/2 도구 결과가 대체하면 생략 가능, Tier 3 만 사용 시 유지 권장) |"""

# ─────────────────────────────────────────────────────────────────
# 변경 4: Version 16 → 17 및 Changes 갱신
# ─────────────────────────────────────────────────────────────────
OLD_4 = """**Version**: 16
**Last Updated**: 2026-06-20
**Changes**: Curator delegate 시 Pre-staged Apply 흐름 + 단일 응답 명시 (Session End 2~3), Continuing Session 엔트로피 체크에 staging dangling 추가, 교훈 승격 Curator 자동 분류로 단순화 (T1.5 §17 + §18 신설과 연동)"""

NEW_4 = """**Version**: 17
**Last Updated**: 2026-07-01
**Changes**: SESSION PROTOCOL 4a (코드 분석 도구 감지) 신설, Continuing Session 엔트로피 체크에 §19 항목 추가, FILE-STRUCTURE.md 스키마 필수/선택 분리 (Tier 감지에 따라 상세 도구 위임 vs Mickey 지도 유지). T1.5 §19 External Code Analysis Integration 신설과 연동 (Tier 1 Serena/Graphify default + Tier 2 사용자 확인 + Tier 3 내장 code baseline)"""


def sha256(path: Path) -> str:
    """파일 SHA-256 해시 측정."""
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def step1_precondition() -> None:
    """양쪽 hash + baseline + 각 old_str count=1."""
    print("[Step 1] Precondition")
    g_hash = sha256(GLOBAL_PATH)
    r_hash = sha256(REPO_PATH)
    print(f"  Global: {g_hash}")
    print(f"  Repo  : {r_hash}")
    if g_hash != r_hash:
        raise RuntimeError("hash mismatch between global and repo")
    if g_hash != EXPECTED_PRECOND_HASH:
        raise RuntimeError(f"baseline hash mismatch. expected {EXPECTED_PRECOND_HASH}")

    for path in [GLOBAL_PATH, REPO_PATH]:
        data = json.loads(path.read_text(encoding="utf-8"))
        prompt = data["prompt"]
        for label, old in [("OLD_1", OLD_1), ("OLD_2", OLD_2),
                           ("OLD_3", OLD_3), ("OLD_4", OLD_4)]:
            cnt = prompt.count(old)
            if cnt != 1:
                raise RuntimeError(f"{path.name} {label}: expected 1, got {cnt}")
        print(f"  {path.name}: all 4 old_str present exactly once")
    print("  PASS")


def step2_backup() -> None:
    """양쪽 .m32-bak."""
    print("[Step 2] Backup")
    for src in (GLOBAL_PATH, REPO_PATH):
        bak = src.with_suffix(src.suffix + ".m32-bak")
        shutil.copy2(src, bak)
        print(f"  {bak}")
    print("  PASS")


def apply_change(path: Path) -> None:
    """단일 JSON 파일 4건 순차 변경 + post-check."""
    data = json.loads(path.read_text(encoding="utf-8"))
    prompt = data["prompt"]
    for old, new in [(OLD_1, NEW_1), (OLD_2, NEW_2), (OLD_3, NEW_3), (OLD_4, NEW_4)]:
        if prompt.count(old) != 1:
            raise RuntimeError(f"{path}: old count != 1 during apply")
        prompt = prompt.replace(old, new, 1)
    data["prompt"] = prompt
    # json.dump 시 원본 형식 유지 위해 indent=2 + ensure_ascii=False
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # 디스크 재확인
    disk_data = json.loads(path.read_text(encoding="utf-8"))
    disk_prompt = disk_data["prompt"]
    for label, new in [("NEW_1", NEW_1), ("NEW_2", NEW_2), ("NEW_3", NEW_3), ("NEW_4", NEW_4)]:
        if disk_prompt.count(new) != 1:
            raise RuntimeError(f"{path}: {label} count != 1 after write")
    for label, old in [("OLD_1", OLD_1), ("OLD_2", OLD_2), ("OLD_3", OLD_3), ("OLD_4", OLD_4)]:
        if old in disk_prompt:
            raise RuntimeError(f"{path}: {label} still present after write")


def step3_apply() -> None:
    """양쪽 동일 변경."""
    print("[Step 3] Apply")
    apply_change(GLOBAL_PATH)
    apply_change(REPO_PATH)
    print("  PASS")


def step4_postcheck() -> None:
    """양쪽 hash 재일치 + baseline 과 다름 + JSON 파싱 성공."""
    print("[Step 4] Post-check")
    g_hash = sha256(GLOBAL_PATH)
    r_hash = sha256(REPO_PATH)
    print(f"  Global: {g_hash}")
    print(f"  Repo  : {r_hash}")
    if g_hash != r_hash:
        raise RuntimeError("hash mismatch after apply")
    if g_hash == EXPECTED_PRECOND_HASH:
        raise RuntimeError("hash unchanged — apply did not take effect")

    # JSON 재파싱 검증
    for path in [GLOBAL_PATH, REPO_PATH]:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "prompt" in data and "**Version**: 17" in data["prompt"]
    print(f"  baseline {EXPECTED_PRECOND_HASH[:16]}... -> {g_hash[:16]}...")
    print("  JSON parse + Version 17 check: PASS")
    print("  PASS")


def main() -> int:
    """4-step 순차 실행."""
    print("=" * 60)
    print("M32 Phase B: agent JSON T1 프롬프트 수정 (safe-batch-replace 10세대)")
    print("=" * 60)
    step1_precondition()
    step2_backup()
    step3_apply()
    step4_postcheck()
    print("=" * 60)
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
