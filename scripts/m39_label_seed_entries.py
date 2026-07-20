# M39: §8-a — repo mickey/domain/entries seed 예시 라벨링 스크립트
# 목적: 프로젝트에 잔존한 개인 지식 entry 10건을 "교육·데모용 seed 예시"로 명시 라벨링한다.
#       (IMPROVEMENT-PLAN-v10 §8-a 옵션 (ii), 사용자 확인 2026-07-04)
# 동작: 각 entry의 제목(# ...) 바로 아래에 라벨 블록을 삽입. 멱등(이미 라벨 있으면 skip).
# 검증: --verify 로 전체 파일 라벨 존재 여부만 확인.
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: Windows cp949 대응

ENTRIES_DIR = Path(__file__).resolve().parent.parent / "mickey" / "domain" / "entries"
LABEL_MARK = "[Seed 예시]"
LABEL_BLOCK = (
    "\n> **[Seed 예시]** 이 파일은 교육·데모용 seed 예시이다 (IMPROVEMENT-PLAN-v10 §8-a).\n"
    "> 실제 지식 그래프는 각 사용자 홈 `~/.kiro/mickey/domain/`에서 Knowledge Curator가 축적하며,\n"
    "> 이 예시는 새 사용자가 entry 형식(Core/Decision Context/Tags/Links/Content/Evidence)을 파악하는 참고용이다.\n"
)


def main() -> int:
    verify_only = "--verify" in sys.argv
    files = sorted(ENTRIES_DIR.glob("*.md"))
    print(f"대상: {len(files)}건 / 모드: {'VERIFY' if verify_only else 'APPLY'}")
    ok, changed = 0, 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        if LABEL_MARK in text:
            ok += 1
            print(f"  [labeled] {f.name}")
            continue
        if verify_only:
            print(f"  [MISSING] {f.name}")
            continue
        lines = text.splitlines(keepends=True)
        # 첫 줄은 '# 제목' — 그 바로 아래에 라벨 블록 삽입
        if not lines or not lines[0].startswith("# "):
            print(f"  [SKIP-형식이상] {f.name}")
            continue
        new_text = lines[0] + LABEL_BLOCK + "".join(lines[1:])
        f.write_text(new_text, encoding="utf-8")
        changed += 1
        print(f"  [ADDED] {f.name}")
    total_labeled = ok + changed
    print(f"결과: 라벨 보유 {total_labeled}/{len(files)} (신규 {changed})")
    return 0 if total_labeled == len(files) else 1


if __name__ == "__main__":
    sys.exit(main())
