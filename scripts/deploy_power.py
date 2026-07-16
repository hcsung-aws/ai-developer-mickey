"""v3 Power(power-mickey) 배포 스크립트.

install.ps1 / install.sh 가 v2 자산(agents JSON, ~/.kiro/mickey 서고)을 배포한 뒤
이 스크립트를 호출하여 v3 power 를 사용자 홈에 배치한다.

배포 책임(단일 책임 함수로 분리):
  1. kiro-cli 버전 파싱 + 게이트 판정 (기본 임계값 2.10)
  2. 기존 installed/power-mickey 타임스탬프 zip 백업 (홈 자산 안전, R6)
  3. clean-replace: full-dir 교체로 구 steering orphan 잔존 방지
  4. installed.json 에 power-mickey 항목 보장

설계 원칙:
  - registry(user-added.json)는 손대지 않는다(B-1). kiro-cli 는 installed/ 물리본을 서빙하므로
    배치만으로 충분하며, registry 는 provenance 메타데이터일 뿐이다.
  - 버전 게이트 미달이면 v3 만 건너뛰고 정상 종료(exit 0)한다. v2 배포는 install 스크립트가
    이미 완료했으므로 CLI/IDE 호환은 유지된다.
  - 모든 부수효과 경로는 --dry-run 으로 무변경 시뮬레이션 가능(테스트 하니스용).
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

POWER_NAME = "power-mickey"
REGISTRY_ID = "user-added"
DEFAULT_MIN_VERSION = (2, 10)


# --- 1. 버전 파싱 + 게이트 -------------------------------------------------

def parse_minor_version(version_output):
    """'kiro-cli-chat 2.12.0' 같은 출력에서 (major, minor) 튜플을 추출한다.

    파싱 실패 시 None 을 반환하여 호출부가 게이트 판정을 보류하도록 한다.
    """
    if not version_output:
        return None
    match = re.search(r"(\d+)\.(\d+)(?:\.\d+)?", version_output)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)))


def version_meets_gate(version_output, min_version=DEFAULT_MIN_VERSION):
    """버전 출력이 최소 임계값 이상인지 판정한다. 파싱 실패 시 False(보수적 스킵)."""
    parsed = parse_minor_version(version_output)
    if parsed is None:
        return False
    return parsed >= min_version


def get_kiro_version():
    """`kiro-cli --version` 을 실행해 원본 출력을 반환한다. 미설치/실패 시 None."""
    try:
        result = subprocess.run(
            ["kiro-cli", "--version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return (result.stdout or result.stderr).strip()


# --- 2. 백업 ---------------------------------------------------------------

def backup_existing_power(installed_dir, dry_run=False):
    """기존 installed/power-mickey 를 타임스탬프 zip 으로 백업한다.

    대상이 없으면 백업을 건너뛴다(신규 설치). 반환값은 수행한 동작 설명 리스트.
    """
    actions = []
    power_dir = installed_dir / POWER_NAME
    if not power_dir.is_dir():
        actions.append(f"[skip] 백업 대상 없음(신규 설치): {power_dir}")
        return actions

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_base = installed_dir / f"{POWER_NAME}.bak-{timestamp}"
    if dry_run:
        actions.append(f"[dry-run] 백업 예정: {power_dir} -> {backup_base}.zip")
        return actions

    # make_archive 는 base_name 에 .zip 을 자동으로 붙인다.
    archive = shutil.make_archive(str(backup_base), "zip", root_dir=str(power_dir))
    actions.append(f"[backup] {power_dir} -> {archive}")
    return actions


# --- 3. clean-replace ------------------------------------------------------

def deploy_power_files(power_src, installed_dir, dry_run=False):
    """power 원본을 installed/power-mickey 로 full-dir 교체 배치한다.

    기존 디렉토리를 통째로 제거한 뒤 복사하므로 구 steering orphan 이 남지 않는다.
    반환값은 수행한 동작 설명 리스트.
    """
    actions = []
    if not power_src.is_dir():
        raise FileNotFoundError(f"power 원본 디렉토리를 찾을 수 없음: {power_src}")

    dst = installed_dir / POWER_NAME
    if dry_run:
        if dst.exists():
            actions.append(f"[dry-run] 기존 제거 예정: {dst}")
        actions.append(f"[dry-run] 복사 예정: {power_src} -> {dst}")
        # 배치될 파일 목록을 미리 보여준다.
        for item in sorted(power_src.rglob("*")):
            if item.is_file():
                rel = item.relative_to(power_src)
                actions.append(f"[dry-run]   + {rel.as_posix()}")
        return actions

    if dst.exists():
        shutil.rmtree(dst)
        actions.append(f"[clean] 기존 제거: {dst}")
    installed_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(power_src, dst)
    actions.append(f"[deploy] 복사: {power_src} -> {dst}")
    return actions


# --- 4. installed.json 항목 보장 -------------------------------------------

def ensure_installed_json_entry(powers_home, dry_run=False):
    """installed.json 에 power-mickey 항목이 존재하도록 보장한다.

    파일이 없으면 기본 골격으로 생성한다. 이미 항목이 있으면 무변경(idempotent).
    반환값은 수행한 동작 설명 리스트.
    """
    actions = []
    installed_json = powers_home / "installed.json"

    if installed_json.exists():
        data = json.loads(installed_json.read_text(encoding="utf-8"))
    else:
        data = {"version": "1.0.0", "installedPowers": [], "dismissedAutoInstalls": []}
        actions.append(f"[create] installed.json 신규 골격 생성 예정: {installed_json}")

    powers = data.setdefault("installedPowers", [])
    already = any(p.get("name") == POWER_NAME for p in powers)
    if already:
        actions.append(f"[skip] installed.json 항목 이미 존재: {POWER_NAME}")
        return actions

    powers.append({"name": POWER_NAME, "registryId": REGISTRY_ID})
    actions.append(f"[register] installed.json 항목 추가: {POWER_NAME} (registryId={REGISTRY_ID})")

    if dry_run:
        actions.append(f"[dry-run] installed.json 기록 보류: {installed_json}")
        return actions

    installed_json.parent.mkdir(parents=True, exist_ok=True)
    installed_json.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return actions


# --- 오케스트레이션 --------------------------------------------------------

def deploy(power_src, powers_home, version_output, min_version, dry_run):
    """v3 power 배포 오케스트레이션. 게이트 미달 시 스킵하고 (skipped, actions) 반환."""
    actions = []
    installed_dir = powers_home / "installed"

    # BRANCH: 버전 게이트 판정
    if not version_meets_gate(version_output, min_version):
        # 게이트 미달/파싱 실패 → v3 스킵(정상 종료). v2 는 install 스크립트가 이미 배포함.
        actions.append(
            f"[gate] kiro-cli 버전 미달 또는 미확인('{version_output}') "
            f"< {min_version[0]}.{min_version[1]} → v3 power 배포 건너뜀. "
            f"CLI v2 는 정상 동작."
        )
        return True, actions

    # 게이트 통과 → 백업 → clean-replace → 대장 갱신
    actions += backup_existing_power(installed_dir, dry_run=dry_run)
    actions += deploy_power_files(power_src, installed_dir, dry_run=dry_run)
    actions += ensure_installed_json_entry(powers_home, dry_run=dry_run)
    return False, actions


def _default_power_src():
    """이 스크립트(scripts/) 기준 프로젝트 루트의 power-mickey 경로."""
    return Path(__file__).resolve().parent.parent / "power-mickey"


def main(argv=None):
    parser = argparse.ArgumentParser(description="v3 power-mickey 배포 스크립트")
    parser.add_argument(
        "--power-src", type=Path, default=_default_power_src(),
        help="power 원본 디렉토리 (기본: 프로젝트 power-mickey/)",
    )
    parser.add_argument(
        "--powers-home", type=Path, default=Path.home() / ".kiro" / "powers",
        help="powers 홈 디렉토리 (기본: ~/.kiro/powers)",
    )
    parser.add_argument(
        "--kiro-version", default=None,
        help="버전 게이트용 버전 문자열 오버라이드 (미지정 시 kiro-cli --version 실행)",
    )
    parser.add_argument(
        "--min-version", default="2.10",
        help="v3 배포 최소 버전 'major.minor' (기본: 2.10)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="실제 변경 없이 수행할 동작만 출력",
    )
    args = parser.parse_args(argv)

    min_parsed = parse_minor_version(args.min_version) or DEFAULT_MIN_VERSION
    version_output = args.kiro_version if args.kiro_version is not None else get_kiro_version()

    try:
        skipped, actions = deploy(
            power_src=args.power_src,
            powers_home=args.powers_home,
            version_output=version_output,
            min_version=min_parsed,
            dry_run=args.dry_run,
        )
    except FileNotFoundError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    prefix = "[dry-run] " if args.dry_run else ""
    for line in actions:
        print(prefix + line if args.dry_run and not line.startswith("[dry-run]") else line)

    if skipped:
        print("v3 power 배포 건너뜀(버전 게이트). v2 CLI 는 정상 사용 가능.")
    elif args.dry_run:
        print("dry-run 완료. 실제 변경 없음.")
    else:
        print(f"v3 power 배포 완료: {args.powers_home / 'installed' / POWER_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
