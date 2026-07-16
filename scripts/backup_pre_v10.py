"""v10 Power 마이그레이션 이전 자산을 백업한다 (Phase 0).

백업 대상:
1. 프로젝트 내 power-mickey/  (IDE 시절 유물, Phase 2에서 재작성 예정)
2. 사용자 홈 ~/.kiro/powers/installed/power-mickey/  (실제 활성 사본)
3. 사용자 홈 ~/.kiro/agents/ai-developer-mickey.json  (v2 CLI agent)
4. 사용자 홈 ~/.kiro/agents/knowledge-curator.json    (Curator subagent)

원칙:
- 이미 백업이 있으면 건드리지 않는다 (idempotent, 재실행 안전).
- 디렉토리는 zip 아카이브, 단일 파일은 확장자 suffix 사본.
- 삭제 없음. 원본은 그대로 유지.
"""

from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

# 사용자 홈 아래 kiro 설치 루트
HOME_KIRO = Path.home() / ".kiro"

# 프로젝트 루트 (스크립트 위치 기준 상위)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def zip_directory(src: Path, dst_zip: Path) -> bool:
    """디렉토리를 zip 아카이브로 백업.

    반환값: 실제로 아카이브를 생성했으면 True, 스킵했으면 False.
    """
    if dst_zip.exists():
        print(f"[skip] 이미 존재: {dst_zip}")
        return False
    if not src.exists():
        print(f"[skip] 원본 없음: {src}")
        return False

    # zip 내부의 최상위 디렉토리명은 원본 디렉토리명과 동일하게 유지
    with zipfile.ZipFile(dst_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for entry in src.rglob("*"):
            if entry.is_file():
                # zip 안에서의 경로: <src디렉토리명>/<하위 경로>
                arcname = entry.relative_to(src.parent)
                zf.write(entry, arcname)
    print(f"[ok]   dir  : {src} -> {dst_zip}")
    return True


def copy_file_backup(src: Path, dst: Path) -> bool:
    """단일 파일을 그대로 사본 복사.

    반환값: 실제로 복사했으면 True, 스킵했으면 False.
    """
    if dst.exists():
        print(f"[skip] 이미 존재: {dst}")
        return False
    if not src.exists():
        print(f"[skip] 원본 없음: {src}")
        return False
    shutil.copy2(src, dst)
    print(f"[ok]   file : {src} -> {dst}")
    return True


def build_backup_plan():
    """(kind, src, dst) 튜플 리스트로 백업 계획을 반환한다.

    kind 는 'dir' 또는 'file'. 실행 시점의 경로만 계산하고 실제 I/O 는 하지 않는다.
    """
    return [
        # 1. 프로젝트 내 IDE 시절 power-mickey (Phase 2 에서 재작성 대상)
        (
            "dir",
            PROJECT_ROOT / "power-mickey",
            PROJECT_ROOT / "power-mickey.pre-v10-bak.zip",
        ),
        # 2. 사용자 홈의 활성 사본 (kiro_powers 가 실제로 로드하는 것)
        (
            "dir",
            HOME_KIRO / "powers" / "installed" / "power-mickey",
            HOME_KIRO / "powers" / "installed" / "power-mickey.pre-v10-bak.zip",
        ),
        # 3. v2 CLI agent JSON (v3 에서는 prompt 무시되지만 v2 엔진에서는 계속 사용됨)
        (
            "file",
            HOME_KIRO / "agents" / "ai-developer-mickey.json",
            HOME_KIRO / "agents" / "ai-developer-mickey.json.pre-v10-bak",
        ),
        # 4. Curator subagent JSON (Phase 4-A 에서 steering 으로 흡수 예정)
        (
            "file",
            HOME_KIRO / "agents" / "knowledge-curator.json",
            HOME_KIRO / "agents" / "knowledge-curator.json.pre-v10-bak",
        ),
    ]


def run_backup() -> int:
    """백업 계획을 순회하며 실행하고 요약을 출력한다."""
    print("=== v10 마이그레이션 사전 백업 ===")
    created, skipped = 0, 0
    for kind, src, dst in build_backup_plan():
        if kind == "dir":
            ok = zip_directory(src, dst)
        else:
            ok = copy_file_backup(src, dst)
        if ok:
            created += 1
        else:
            skipped += 1
    print(f"=== 완료: 생성 {created}건 / 스킵 {skipped}건 ===")
    return 0


if __name__ == "__main__":
    sys.exit(run_backup())
