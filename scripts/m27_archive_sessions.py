# -*- coding: utf-8 -*-
"""
M27 — SESSION 아카이빙 (M21~M26 의 SESSION/HANDOFF 12파일 → sessions/)

T1.5 §3 엔트로피 관리: 루트의 SESSION 파일 3개 이상 → 아카이빙.
M27 진입 시 6건 누적 (M21~M26), 임계 3 초과 5세션째 미처리.

git mv 사용 → git 이력 보존, revert 가능.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")
SESSIONS_DIR = PROJECT_ROOT / "sessions"

# 아카이빙 대상 (M21~M26 의 SESSION + HANDOFF 12파일)
TARGETS = [
    f"MICKEY-{i}-{kind}.md"
    for i in range(21, 27)
    for kind in ("SESSION", "HANDOFF")
]


def run_git(args: list[str]) -> tuple[int, str, str]:
    """git 명령 실행. returncode, stdout, stderr 반환."""
    p = subprocess.run(
        ["git"] + args,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return p.returncode, p.stdout, p.stderr


def main() -> int:
    if not SESSIONS_DIR.exists():
        print(f"[ERR] sessions/ 디렉토리 없음: {SESSIONS_DIR}", file=sys.stderr)
        return 1

    print(f"# M27 SESSION 아카이빙 (M21~M26 → sessions/)")
    print(f"# 대상: {len(TARGETS)}개 파일")
    print()

    moved = []
    skipped = []
    errors = []

    for name in TARGETS:
        src = PROJECT_ROOT / name
        dst = SESSIONS_DIR / name

        if not src.exists():
            skipped.append((name, "원본 없음 (이미 이동됐거나 미존재)"))
            print(f"  [SKIP] {name} — 원본 없음")
            continue

        if dst.exists():
            skipped.append((name, "대상 이미 존재"))
            print(f"  [SKIP] {name} — 대상 이미 존재")
            continue

        # git mv 로 이동 (이력 보존)
        rel_src = name
        rel_dst = f"sessions/{name}"
        rc, out, err = run_git(["mv", rel_src, rel_dst])
        if rc != 0:
            errors.append((name, err.strip()))
            print(f"  [ERR]  {name} — {err.strip()}")
            continue

        moved.append(name)
        print(f"  [OK]   {name} → sessions/{name}")

    print()
    print("=" * 60)
    print(f"[SUMMARY] moved={len(moved)} skipped={len(skipped)} errors={len(errors)}")
    print("=" * 60)
    if errors:
        return 1

    # 결과 검증: 루트에 M21~M26 SESSION/HANDOFF 가 모두 사라졌는지
    remaining = [n for n in TARGETS if (PROJECT_ROOT / n).exists()]
    if remaining:
        print(f"[WARN] 루트에 잔류: {remaining}")
        return 1
    print("[OK] 루트에 M21~M26 SESSION/HANDOFF 잔류 없음")

    # git status 요약
    rc, out, err = run_git(["status", "--short"])
    if rc == 0:
        renamed = [line for line in out.splitlines() if line.startswith("R ") or line.startswith("R")]
        print(f"[git status] renamed={len(renamed)}")
        for line in renamed[:5]:
            print(f"  {line}")
        if len(renamed) > 5:
            print(f"  ... ({len(renamed) - 5}건 더)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
