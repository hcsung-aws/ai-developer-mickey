"""
M29 원복: 변형 I → H (.m28-bak)
safe-batch-replace 4-step 패턴 7세대 적용 (원복도 역방향 변형의 일종)

절차:
1. precondition: 본체 = I, .m28-bak = H 재확인
2. backup: 현재 I 본체를 .m29-bak 으로 보존 (추적성)
3. apply: .m28-bak (H) → 본체 (글로벌 + repo 양쪽)
4. post-check: 본체 hash = H, 글로벌 ↔ repo 일치 확인
"""
import hashlib
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 상수
HASH_I = "45CAFB42A1152689"            # 변형 I (M28 적용 결과)
HASH_H = "F65CAF62C5DBDD0F"            # 변형 H (M27 적용 결과, .m28-bak 내용)
SIZE_I = 12137
SIZE_H = 12139


def file_hash_size(p: Path):
    if not p.exists():
        return None, None
    data = p.read_bytes()
    h = hashlib.sha256(data).hexdigest()[:16].upper()
    return h, len(data)


def step1_precondition(targets):
    """현재 디스크가 원복 시작점인지 재확인"""
    print("[Step 1] Precondition 검증")
    for label, p in targets.items():
        h, sz = file_hash_size(p)
        print(f"  {label:20s} hash={h} size={sz}")

    g_cur_h, _ = file_hash_size(targets["global_curator"])
    r_cur_h, _ = file_hash_size(targets["repo_curator"])
    g_bak_h, g_bak_sz = file_hash_size(targets["global_m28_bak"])
    r_bak_h, r_bak_sz = file_hash_size(targets["repo_m28_bak"])

    checks = [
        ("글로벌 본체 = I", g_cur_h == HASH_I),
        ("repo 본체 = I", r_cur_h == HASH_I),
        ("글로벌 .m28-bak = H", g_bak_h == HASH_H and g_bak_sz == SIZE_H),
        ("repo .m28-bak = H", r_bak_h == HASH_H and r_bak_sz == SIZE_H),
    ]
    for desc, ok in checks:
        print(f"  {'✓' if ok else '✗'} {desc}")
        if not ok:
            sys.exit(f"[ABORT] Step 1 FAIL: {desc}")
    print("  PASS")


def step2_backup(targets):
    """현재 I 본체를 .m29-bak 으로 보존 (역방향 변형 추적성)"""
    print("\n[Step 2] Backup (.m29-bak 생성)")
    for src_key, bak_key in [
        ("global_curator", "global_m29_bak"),
        ("repo_curator", "repo_m29_bak"),
    ]:
        src = targets[src_key]
        bak = targets[bak_key]
        shutil.copy2(src, bak)
        h, sz = file_hash_size(bak)
        print(f"  {bak.name}: hash={h} size={sz}")
        if h != HASH_I or sz != SIZE_I:
            sys.exit(f"[ABORT] Step 2 FAIL: backup hash mismatch for {bak}")
    print("  PASS")


def step3_apply(targets):
    """.m28-bak (H) → 본체 (양쪽)"""
    print("\n[Step 3] Apply (.m28-bak → 본체)")
    for bak_key, dst_key in [
        ("global_m28_bak", "global_curator"),
        ("repo_m28_bak", "repo_curator"),
    ]:
        bak = targets[bak_key]
        dst = targets[dst_key]
        shutil.copy2(bak, dst)
        print(f"  {dst.name}: ← {bak.name}")
    print("  복사 완료")


def step4_postcheck(targets):
    """본체 hash = H 양쪽 일치 검증"""
    print("\n[Step 4] Post-check")
    g_cur_h, g_cur_sz = file_hash_size(targets["global_curator"])
    r_cur_h, r_cur_sz = file_hash_size(targets["repo_curator"])
    print(f"  global_curator: hash={g_cur_h} size={g_cur_sz}")
    print(f"  repo_curator:   hash={r_cur_h} size={r_cur_sz}")

    checks = [
        ("글로벌 본체 = H", g_cur_h == HASH_H and g_cur_sz == SIZE_H),
        ("repo 본체 = H", r_cur_h == HASH_H and r_cur_sz == SIZE_H),
        ("글로벌 ↔ repo 일치", g_cur_h == r_cur_h),
    ]
    all_ok = True
    for desc, ok in checks:
        print(f"  {'✓' if ok else '✗'} {desc}")
        if not ok:
            all_ok = False
    if not all_ok:
        sys.exit("[ABORT] Step 4 FAIL")
    print("  PASS — 원복 완료")


def main():
    home = Path.home()
    repo = Path(__file__).resolve().parent.parent

    targets = {
        "global_curator": home / ".kiro" / "agents" / "knowledge-curator.json",
        "global_m28_bak": home / ".kiro" / "agents" / "knowledge-curator.json.m28-bak",
        "global_m29_bak": home / ".kiro" / "agents" / "knowledge-curator.json.m29-bak",
        "repo_curator": repo / "examples" / "knowledge-curator.json",
        "repo_m28_bak": repo / "examples" / "knowledge-curator.json.m28-bak",
        "repo_m29_bak": repo / "examples" / "knowledge-curator.json.m29-bak",
    }

    print("=" * 70)
    print("M29 원복: 변형 I → H (.m28-bak)")
    print("=" * 70)

    step1_precondition(targets)
    step2_backup(targets)
    step3_apply(targets)
    step4_postcheck(targets)

    print("\n" + "=" * 70)
    print("결과: 변형 I → H 원복 성공")
    print(f"  본체 (양쪽): hash={HASH_H}, size={SIZE_H}")
    print(f"  백업 누적: .m24-bak (원본) ~ .m29-bak (I, 12137 bytes) — 6단계 모두 보존")
    print("=" * 70)


if __name__ == "__main__":
    main()
