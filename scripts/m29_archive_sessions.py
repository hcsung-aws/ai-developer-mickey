"""
M29 SESSION 아카이빙: M27/M28/M29 의 SESSION + HANDOFF 6개 파일을 sessions/ 로 이동.

PowerShell Get-ChildItem 와일드카드가 본 환경에서 빈 결과 반환하는 이슈 회피.
Python pathlib + shutil 으로 안전한 이동.

절차:
1. precondition: 6개 파일 존재 + sessions/ 디렉토리 존재 확인
2. 충돌 검사: sessions/ 에 동일 이름 파일이 이미 있는지 확인
3. apply: 6개 파일 일괄 이동
4. post-check: 루트에 더 이상 없음 + sessions/ 에 있음 확인
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')


def main():
    repo = Path(__file__).resolve().parent.parent
    sessions = repo / "sessions"

    targets = [
        "MICKEY-27-SESSION.md",
        "MICKEY-27-HANDOFF.md",
        "MICKEY-28-SESSION.md",
        "MICKEY-28-HANDOFF.md",
        "MICKEY-29-SESSION.md",
        "MICKEY-29-HANDOFF.md",
    ]

    print("=" * 70)
    print("M29 SESSION 아카이빙: 루트 → sessions/")
    print("=" * 70)

    # Step 1: precondition
    print("\n[Step 1] Precondition 검증")
    if not sessions.is_dir():
        sys.exit(f"[ABORT] sessions/ 디렉토리 없음: {sessions}")
    print(f"  sessions/ 존재: {sessions}")

    missing = []
    for name in targets:
        src = repo / name
        if not src.is_file():
            missing.append(name)
        else:
            print(f"  ✓ {name}: {src.stat().st_size} bytes")
    if missing:
        sys.exit(f"[ABORT] 루트에 없는 파일: {missing}")

    # Step 2: 충돌 검사
    print("\n[Step 2] 충돌 검사")
    conflicts = []
    for name in targets:
        dst = sessions / name
        if dst.exists():
            conflicts.append(name)
    if conflicts:
        sys.exit(f"[ABORT] sessions/ 에 이미 존재: {conflicts}")
    print("  충돌 없음")

    # Step 3: apply (개별 이동)
    print("\n[Step 3] Apply (개별 이동)")
    moved = []
    for name in targets:
        src = repo / name
        dst = sessions / name
        shutil.move(str(src), str(dst))
        moved.append((name, dst.stat().st_size))
        print(f"  → {name}: {dst.stat().st_size} bytes")

    # Step 4: post-check
    print("\n[Step 4] Post-check")
    all_ok = True
    for name in targets:
        src = repo / name
        dst = sessions / name
        if src.exists():
            print(f"  ✗ {name}: 루트에 잔존")
            all_ok = False
        if not dst.is_file():
            print(f"  ✗ {name}: sessions/ 에 없음")
            all_ok = False
    if all_ok:
        print(f"  ✓ 6개 파일 모두 sessions/ 로 이동 완료")
    else:
        sys.exit("[ABORT] Post-check 실패")

    print("\n" + "=" * 70)
    print(f"결과: M27/M28/M29 의 SESSION + HANDOFF {len(moved)}개 아카이빙 완료")
    print(f"위치: {sessions}")
    print("=" * 70)


if __name__ == "__main__":
    main()
