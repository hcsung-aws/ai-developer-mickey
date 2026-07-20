# M39: m37 계열 백업 정리 스크립트
# 목적: 안정 검증(m37_phase2_verify 무결성 PASS + SoT 동기화 일치) 후
#       글로벌 ~/.kiro/mickey/ 의 .m37* 백업과 repo untracked 백업을 삭제한다.
# 안전장치: 삭제 대상을 먼저 나열하고, --apply 없이는 dry-run으로만 동작한다.
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: Windows cp949 대응

GLOBAL_ROOT = Path.home() / ".kiro" / "mickey"
REPO_BACKUP = Path(__file__).resolve().parent.parent / "examples" / "knowledge-curator.json.m37-toolfix-bak"


def find_targets() -> list[Path]:
    """글로벌 트리에서 m37 계열 백업(.m37*)과 repo 백업 1건을 수집한다."""
    targets = [p for p in GLOBAL_ROOT.rglob("*") if p.is_file() and ".m37" in p.name]
    if REPO_BACKUP.exists():
        targets.append(REPO_BACKUP)
    return targets


def main() -> int:
    apply = "--apply" in sys.argv
    targets = find_targets()
    print(f"모드: {'APPLY' if apply else 'DRY-RUN'} / 대상 {len(targets)}건")
    for p in targets:
        print(f"  {'DEL' if apply else 'would-del'}: {p}")
        if apply:
            p.unlink()
    # 삭제 후 잔존 검증 (CC: 백업 0건)
    if apply:
        remain = [p for p in GLOBAL_ROOT.rglob("*") if p.is_file() and "bak" in p.name.lower()]
        print(f"잔존 bak 파일: {len(remain)}건")
        for p in remain:
            print(f"  remain: {p}")
        print(f"repo 백업 잔존: {REPO_BACKUP.exists()}")
        return 0 if not remain and not REPO_BACKUP.exists() else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
