# -*- coding: utf-8 -*-
"""M43: §22 PowerShell 원스트라이크 신설 (v25→v26) — 별도 커밋 대상.

배경 (POSTMORTEM 2026-08-21 개선 후보 ①): PowerShell execute 계층 함정이 반복
마찰 1위. 개별 규칙은 이미 존재하나 위반이 구조적으로 재발 — 새 규칙 추가가 아닌
기존 규칙의 강제 장치(1회 위반 → 세션 잔여 .py 전용 전환)를 명문화.

대상: 글로벌 + repo 미러 (adaptive #3). 판정: 리포트 파일 실측.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GLOBAL_MD = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO_MD = Path(__file__).resolve().parent.parent / "mickey" / "extended-protocols.md"
OUT = Path(__file__).resolve().parent / "output" / "m43_ps_one_strike.txt"

SECTION = """## 22. PowerShell 원스트라이크 (Shell Execution Enforcement)

> 개별 규칙(인라인 python -c 금지, `&&` 미지원 등)은 이미 존재하나 위반이 구조적으로 재발 (POSTMORTEM 2026-08-21: 반복 마찰 1위). 본 조항은 새 규칙이 아니라 **기존 규칙의 강제 장치**다.

### 규약

- 세션 중 PowerShell 인라인 명령이 구문/이스케이프/출력 계층 함정으로 **1회라도** 실패하거나 위반을 자각하면 — 그 즉시 해당 세션의 잔여 셸 작업을 **.py 스크립트 파일 전용으로 전환**한다
  - 함정 예: `&&` 파서 오류, 따옴표 중첩, python -c one-liner, Format-Table/Select-String 출력 유실, `$_`/`$env:` 소실, `[`로 시작하는 출력 라인 소실
- **인라인 변형 재시도 금지** — 같은 명령을 따옴표/구분자만 바꿔 재시도하는 것이 반복 마찰의 실체
- 예외: 단일 명령 + 단순 인자(git status, python script.py 등 이스케이프 불요 명령)는 전환 후에도 인라인 허용
- 위반/전환 사실을 SESSION.md Lessons Learned에 `[Protocol]` 태그로 기록 (§18 측정 대상)

### 근거

- POSTMORTEM 2026-08-21: python -c 재발 (epic-lore M15 2회 + anjin M9), `&&` 소실 (M43 재현), Format-Table/Select-String 출력 유실 (anjin M7 + M42 + M43 `[` 라인 소실), 한/영 미전환 4회 (back-to-basic M15)
- epic-lore M15 진단: "규칙 존재만으로 부족" — 위반 감지 시점에 실행 계층 자체를 바꾸는 구조적 차단이 필요

---

"""

OLD_VER = "**Version**: 25\n**Last Updated**: 2026-08-22\n**Changes (v25)**:"
NEW_VER = ("**Version**: 26\n**Last Updated**: 2026-08-22\n"
           "**Changes (v26)**: §22 PowerShell 원스트라이크 신설 (ai-developer-mickey M43, "
           "POSTMORTEM 2026-08-21 개선 후보 ①): 인라인 셸 함정 1회 위반 시 세션 잔여를 "
           ".py 스크립트 전용 전환 — 기존 셸 규칙의 강제 장치. 인라인 변형 재시도 금지. "
           "근거: PowerShell execute 계층 함정이 8개 프로젝트 [Protocol] 태그 반복 마찰 1위.\n"
           "**Changes (v25)**:")

# §22를 푸터 구분선 직전에 삽입 — §21 근거 뒤의 "---\n\n**Version**" 앵커 사용
ANCHOR = "---\n\n**Version**: 25"


def apply(md_path: Path, report: list) -> bool:
    text = md_path.read_text(encoding="utf-8")
    if text.count(ANCHOR) != 1 or text.count(OLD_VER) != 1 or text.count(SECTION) != 0:
        report.append(f"[FAIL] {md_path}: 앵커 count 불일치 "
                      f"(anchor={text.count(ANCHOR)}, ver={text.count(OLD_VER)})")
        return False
    text = text.replace(ANCHOR, "---\n\n" + SECTION + "**Version**: 25")
    text = text.replace(OLD_VER, NEW_VER)
    md_path.write_text(text, encoding="utf-8")
    report.append(f"[OK] {md_path}: §22 삽입 + v26")
    return True


def main() -> int:
    report, ok = [], True
    for md in (GLOBAL_MD, REPO_MD):
        ok = apply(md, report) and ok
    same = GLOBAL_MD.read_bytes() == REPO_MD.read_bytes()
    report.append(f"[SYNC] global==repo: {same}")
    ok = ok and same
    report.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(report), encoding="utf-8")
    print(f"written: {OUT} ({'ALL PASS' if ok else 'FAIL'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
