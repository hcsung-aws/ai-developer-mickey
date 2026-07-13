"""vis-network 라이브러리 벤더 다운로드 스크립트 (최초 1회 실행).

목적:
    scripts/mickey_graph/vendor/ 아래에 vis-network standalone min bundle 을
    로컬 저장하여, 이후 runtime 은 완전 오프라인 동작 가능하게 한다.

정책:
    - 이 스크립트만 인터넷 접근 필요. 실행 후에는 오프라인 완전 자립.
    - 결과 파일은 .gitignore 대상. 다른 머신에서는 이 스크립트를 재실행.
    - 다운로드 후 최소 크기 검증 (100KB 이상). 정확한 SHA 검증은 선택 사항.

사용법:
    python scripts/setup_vendor.py
"""

from __future__ import annotations

import hashlib
import shutil
import sys
import urllib.request
from pathlib import Path

# --- 상수 ---

# vis-network 9.1.9 UMD 최소 번들 (2024-04 릴리스 기준 안정판)
VIS_NETWORK_VERSION = "9.1.9"
VIS_NETWORK_URL = (
    f"https://unpkg.com/vis-network@{VIS_NETWORK_VERSION}"
    "/standalone/umd/vis-network.min.js"
)
# 크기 sanity check: 300KB 근처. 100KB 미만이면 다운로드 실패로 판단
MIN_EXPECTED_SIZE_BYTES = 100 * 1024

# 대상 경로
VENDOR_DIR = Path(__file__).parent / "mickey_graph" / "vendor"
VENDOR_FILE = VENDOR_DIR / "vis-network.min.js"
VENDOR_META_FILE = VENDOR_DIR / "VERSION.txt"


def _ensure_stdout_utf8() -> None:
    """Windows cp949 환경에서 non-ASCII 출력 안전. adaptive #8 규칙."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def download_vis_network(url: str, dest: Path) -> Path:
    """URL 에서 파일 다운로드하여 dest 로 저장. 임시 파일 경유로 원자성 확보."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")

    print(f"[setup_vendor] downloading: {url}")
    with urllib.request.urlopen(url, timeout=60) as response:
        with tmp.open("wb") as f:
            shutil.copyfileobj(response, f)

    shutil.move(str(tmp), str(dest))
    return dest


def verify_size(path: Path, min_bytes: int) -> int:
    """파일 크기 검증. 미달 시 예외."""
    size = path.stat().st_size
    if size < min_bytes:
        raise RuntimeError(
            f"downloaded file too small: {size} bytes (expected >= {min_bytes})"
        )
    return size


def write_meta(path: Path, version: str, source_url: str, size: int, sha256: str) -> None:
    """다운로드 메타데이터 기록 (재현 가능성 + 감사)."""
    path.write_text(
        f"vis-network version: {version}\n"
        f"source: {source_url}\n"
        f"size: {size} bytes\n"
        f"sha256: {sha256}\n",
        encoding="utf-8",
    )


def compute_sha256(path: Path) -> str:
    """다운로드 파일 sha256 (감사 로그용)."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    _ensure_stdout_utf8()

    try:
        download_vis_network(VIS_NETWORK_URL, VENDOR_FILE)
        size = verify_size(VENDOR_FILE, MIN_EXPECTED_SIZE_BYTES)
        sha = compute_sha256(VENDOR_FILE)
        write_meta(VENDOR_META_FILE, VIS_NETWORK_VERSION, VIS_NETWORK_URL, size, sha)
    except Exception as e:  # noqa: BLE001
        print(f"[setup_vendor] ERROR: {e}", file=sys.stderr)
        return 1

    print(f"[setup_vendor] OK: {VENDOR_FILE} ({size:,} bytes)")
    print(f"[setup_vendor] sha256: {sha}")
    print(f"[setup_vendor] meta: {VENDOR_META_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
