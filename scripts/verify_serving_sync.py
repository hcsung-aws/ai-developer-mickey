# -*- coding: utf-8 -*-
"""V4: 홈 서빙본(~/.kiro/powers/installed/power-mickey) vs 프로젝트 정본(power-mickey/) 해시 비교.

목적: v3 런타임이 실제로 소비하는 물리본이 프로젝트 정본과 일치하는지 검증한다.
- 양쪽 파일 목록을 재귀 수집하여 상대 경로 기준으로 대조
- 한쪽에만 있는 파일(orphan/missing)과 내용 불일치(sha256)를 각각 보고
- 백업 zip 등 배포 산출물은 서빙본 쪽에서 제외
"""
import hashlib
import os
import sys

# 비교 대상 루트
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(PROJECT_ROOT, "power-mickey")                          # 프로젝트 정본
SERVING = os.path.join(os.path.expanduser("~"), ".kiro", "powers", "installed", "power-mickey")  # 홈 서빙본

# 서빙본 쪽에서 비교 제외할 파일 패턴 (배포 백업 zip 등)
EXCLUDE_SUFFIXES = (".zip",)


def collect(root):
    """루트 아래 전 파일의 {상대경로: sha256} 맵 생성. 제외 패턴은 건너뜀."""
    result = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(EXCLUDE_SUFFIXES):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            with open(full, "rb") as f:
                result[rel] = hashlib.sha256(f.read()).hexdigest()
    return result


def main():
    for label, path in (("정본", CANON), ("서빙본", SERVING)):
        if not os.path.isdir(path):
            print(f"[FAIL] {label} 디렉토리 없음: {path}")
            sys.exit(1)

    canon = collect(CANON)
    serving = collect(SERVING)

    only_canon = sorted(set(canon) - set(serving))      # 정본에만 있음 (서빙 누락)
    only_serving = sorted(set(serving) - set(canon))    # 서빙본에만 있음 (orphan)
    mismatch = sorted(r for r in set(canon) & set(serving) if canon[r] != serving[r])

    print(f"정본: {CANON} ({len(canon)} files)")
    print(f"서빙본: {SERVING} ({len(serving)} files)")
    print()

    ok = True
    if only_canon:
        ok = False
        print("--- 정본에만 존재 (서빙 누락) ---")
        for r in only_canon:
            print(f"  [MISSING-IN-SERVING] {r}")
    if only_serving:
        ok = False
        print("--- 서빙본에만 존재 (orphan) ---")
        for r in only_serving:
            print(f"  [ORPHAN-IN-SERVING] {r}")
    if mismatch:
        ok = False
        print("--- 내용 불일치 (sha256) ---")
        for r in mismatch:
            print(f"  [HASH-MISMATCH] {r}")

    if ok:
        print(f"일치 파일: {len(canon)}건, 불일치 0건")
    print()
    print("RESULT:", "IN-SYNC" if ok else "OUT-OF-SYNC")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
