# -*- coding: utf-8 -*-
"""M44: extended-protocols v27 반영 + graph_audit.py 글로벌 배포.

수행 내용 (safe-batch-replace: count-1 guard + 메모리 내 수행 + hash 검증):
1. 글로벌 ~/.kiro/mickey/extended-protocols.md 백업 (.bak-ai-developer-mickey-m44)
2. §3 세션 시작 체크에 8항(그래프 무결성 감사 도구) 신설 — 개선 C
3. Version 26 → 27 + Changes(v27) 항목 추가
4. repo 미러 mickey/extended-protocols.md 동기화 + sha256 일치 검증
5. scripts/graph_audit.py → ~/.kiro/mickey/scripts/ 배포 + sha256 일치 검증
"""
import hashlib
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

GLOBAL = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO = Path(__file__).resolve().parents[1]
MIRROR = REPO / "mickey" / "extended-protocols.md"
AUDIT_SRC = REPO / "scripts" / "graph_audit.py"
AUDIT_DST = Path.home() / ".kiro" / "mickey" / "scripts" / "graph_audit.py"

# (needle, replacement) — 각 needle은 정확히 1회만 존재해야 함 (count-1 guard)
EDITS = [
    # §3 8항 신설 (7항 뒤)
    (
        "7. **domain 카테고리 클러스터 스캔** (§20 연동): `domain/GRAPH.md` Nodes 표의 태그 클러스터가 임계값(7개 노드) 이상 → Step 3 카테고리화 후보로 제시. 즉시 재편 강제 아님 (사용자 확인 시 응집 도메인 vs 횡단 관점 판단)",
        "7. **domain 카테고리 클러스터 스캔** (§20 연동): `domain/GRAPH.md` Nodes 표의 태그 클러스터가 임계값(7개 노드) 이상 → Step 3 카테고리화 후보로 제시. 즉시 재편 강제 아님 (사용자 확인 시 응집 도메인 vs 횡단 관점 판단)\n"
        "8. **domain 그래프 무결성 감사** (M44 도구화): `python ~/.kiro/mickey/scripts/graph_audit.py` 실행 — 불변 조건(dangling 엣지/Path 결손)과 정리 후보(orphan/중복 엣지/INDEX 중복 등재/malformed 표 행/카테고리 드리프트/태그 클러스터)를 실측. 불변 조건 위반은 즉시 수술 제안, 정리 후보는 notify. 6·7항의 스캔은 이 도구 출력이 겸한다. 기준점 대조: ai-developer-mickey `GRAPH-HEALTH-BASELINE-*.md` (M44 baseline — \"다음에 반영\" 류 인계는 실행 주체가 없으면 방치된다는 실측이 도구화 근거)",
    ),
    # 버전 푸터
    (
        "**Version**: 26\n**Last Updated**: 2026-08-22\n**Changes (v26)**:",
        "**Version**: 27\n**Last Updated**: 2026-08-25\n"
        "**Changes (v27)**: §3 세션 시작 체크 8항 신설 (ai-developer-mickey M44, 그래프 전면 감사): graph_audit.py 상비 도구화 — dangling/Path(불변)와 orphan/중복/malformed/드리프트(정리 후보) 실측을 엔트로피 체크 중단점에 배치. 근거: orphan 1건이 \"다음 Curator 반영 예정\" 인계로 2개월 방치 (forced-breakpoint 원칙 위반 실측). 연동: promote_knowledge.py 카테고리 라우팅 + 표 연속성 + 허브 편중 경고 (개선 A), CURATOR-PROMPT 엣지 편중 방지 규율 (개선 B), promote 미러 동기화 리마인더 (개선 D). baseline: GRAPH-HEALTH-BASELINE-2026-08-25.md\n"
        "**Changes (v26)**:",
    ),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    text = GLOBAL.read_text(encoding="utf-8")
    # count-1 guard: 모든 needle이 정확히 1회 존재해야 부분 적용 없이 진행
    for needle, _ in EDITS:
        n = text.count(needle)
        if n != 1:
            print(f"[FAIL] needle 출현 {n}회 (1회 필요): {needle[:60]}...")
            return 1
    # 백업 → 메모리 내 일괄 적용 → 쓰기
    bak = GLOBAL.with_name(GLOBAL.name + ".bak-ai-developer-mickey-m44")
    shutil.copy2(GLOBAL, bak)
    print(f"[OK] 백업: {bak}")
    for needle, repl in EDITS:
        text = text.replace(needle, repl)
    GLOBAL.write_text(text, encoding="utf-8")
    print(f"[OK] 글로벌 v27 반영: {GLOBAL}")

    # repo 미러 동기화 (global → repo, adaptive #3)
    shutil.copy2(GLOBAL, MIRROR)
    ok_mirror = sha(GLOBAL) == sha(MIRROR)
    print(f"[{'PASS' if ok_mirror else 'FAIL'}] repo 미러 hash match: {MIRROR}")

    # graph_audit.py 글로벌 배포
    AUDIT_DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AUDIT_SRC, AUDIT_DST)
    ok_audit = sha(AUDIT_SRC) == sha(AUDIT_DST)
    print(f"[{'PASS' if ok_audit else 'FAIL'}] graph_audit 글로벌 배포 hash match: {AUDIT_DST}")

    # 사후 검증: v27 마커 + 8항 존재
    final = GLOBAL.read_text(encoding="utf-8")
    checks = [
        ("Version 27", "**Version**: 27" in final),
        ("Changes v27", "**Changes (v27)**" in final),
        ("§3 8항", "domain 그래프 무결성 감사" in final),
    ]
    all_ok = ok_mirror and ok_audit
    for name, ok in checks:
        all_ok &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("[RESULT]", "ALL PASS" if all_ok else "FAIL 존재")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
