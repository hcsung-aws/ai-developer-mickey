"""
M29 사전 진단: 원복 전 디스크 상태 실측
- 글로벌 + repo 양쪽의 현재 hash + size 확인
- .m28-bak (H 백업) 존재 + hash 확인
- 원복 가능성 사전 판정
"""
import hashlib
import json
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')  # adaptive #8 (cp949 가드)


def file_hash_size(p: Path):
    """파일이 존재하면 (hash16, size) 반환, 아니면 (None, None)"""
    if not p.exists():
        return None, None
    data = p.read_bytes()
    h = hashlib.sha256(data).hexdigest()[:16].upper()
    return h, len(data)


def main():
    home = Path.home()
    repo = Path(__file__).resolve().parent.parent

    targets = {
        "global_curator": home / ".kiro" / "agents" / "knowledge-curator.json",
        "global_m28_bak": home / ".kiro" / "agents" / "knowledge-curator.json.m28-bak",
        "repo_curator": repo / "examples" / "knowledge-curator.json",
        "repo_m28_bak": repo / "examples" / "knowledge-curator.json.m28-bak",
    }

    print("=" * 70)
    print("M29 원복 전 디스크 실측")
    print("=" * 70)

    expected_i_hash = "45CAFB42A1152689"  # M28 변형 I
    expected_h_size = 12139               # M27 변형 H (.m28-bak 크기)

    rows = []
    for label, p in targets.items():
        h, sz = file_hash_size(p)
        status = "OK" if h else "MISSING"
        rows.append((label, str(p), h, sz, status))
        print(f"  {label:20s} hash={h or 'MISSING':>16s} size={sz or 0:>6d}  {status}")

    print()
    print("판정:")

    g_cur_h, g_cur_sz = file_hash_size(targets["global_curator"])
    r_cur_h, r_cur_sz = file_hash_size(targets["repo_curator"])
    g_bak_h, g_bak_sz = file_hash_size(targets["global_m28_bak"])
    r_bak_h, r_bak_sz = file_hash_size(targets["repo_m28_bak"])

    checks = [
        ("글로벌 본체 = 변형 I", g_cur_h == expected_i_hash),
        ("repo 본체 = 변형 I", r_cur_h == expected_i_hash),
        ("글로벌 ↔ repo 본체 일치", g_cur_h == r_cur_h),
        ("글로벌 .m28-bak 존재 + size=H", g_bak_sz == expected_h_size),
        ("repo .m28-bak 존재 + size=H", r_bak_sz == expected_h_size),
        ("글로벌 ↔ repo .m28-bak 일치", g_bak_h == r_bak_h),
    ]

    all_ok = True
    for desc, ok in checks:
        mark = "✓" if ok else "✗"
        print(f"  {mark} {desc}")
        if not ok:
            all_ok = False

    print()
    if all_ok:
        print(f"[PASS] 원복 가능. 본체(I, {expected_i_hash}) → .m28-bak(H, {g_bak_h}) 로 복원 진행.")
    else:
        print("[FAIL] 사전 조건 미충족. 원복 중단 + 사용자 확인 필요.")
        sys.exit(1)


if __name__ == "__main__":
    main()
