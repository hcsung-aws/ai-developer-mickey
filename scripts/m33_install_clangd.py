# -*- coding: utf-8 -*-
"""
m33_install_clangd.py
GitHub Releases 에서 clangd 최신 stable Windows zip 을 받아
%USERPROFILE%\\.local\\clangd\\ 아래 압축 해제한다.
PATH 등록은 별도 스크립트(m33_extend_user_path.py)가 담당.
"""
import json
import os
import pathlib
import shutil
import sys
import urllib.request
import zipfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

API_URL = "https://api.github.com/repos/clangd/clangd/releases/latest"
TARGET_ROOT = pathlib.Path(os.environ["USERPROFILE"]) / ".local" / "clangd"


def http_get_json(url: str) -> dict:
    """GitHub API 응답을 JSON 으로 파싱한다. User-Agent 없으면 403 반환됨."""
    req = urllib.request.Request(url, headers={"User-Agent": "mickey-33"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def http_download(url: str, dest: pathlib.Path) -> None:
    """스트리밍 다운로드. 대용량(수십 MB) 대비 청크 복사."""
    req = urllib.request.Request(url, headers={"User-Agent": "mickey-33"})
    with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f, length=1024 * 1024)


def find_windows_zip(assets: list) -> dict | None:
    """clangd-windows-<version>.zip 패턴 asset 선택."""
    for a in assets:
        name = a["name"].lower()
        if name.startswith("clangd-windows-") and name.endswith(".zip"):
            return a
    return None


def main() -> int:
    print(f"[INFO] Querying {API_URL}")
    rel = http_get_json(API_URL)
    tag = rel.get("tag_name", "?")
    print(f"[INFO] Latest tag: {tag}")

    asset = find_windows_zip(rel.get("assets", []))
    if asset is None:
        print("[ERROR] Windows zip asset not found in latest release")
        return 1

    print(f"[INFO] Asset: {asset['name']} ({asset['size']:,} bytes)")

    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    zip_path = TARGET_ROOT / asset["name"]
    if zip_path.exists():
        # 재실행 대비, 기존 zip 재사용
        print(f"[SKIP] zip already downloaded: {zip_path}")
    else:
        print(f"[DL]   -> {zip_path}")
        http_download(asset["browser_download_url"], zip_path)

    # zip 최상위 디렉토리명 (예: clangd_18.1.3)
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        if not names:
            print("[ERROR] empty zip")
            return 2
        top = names[0].split("/")[0]
        target = TARGET_ROOT / top
        if target.exists():
            print(f"[SKIP] already extracted: {target}")
        else:
            print(f"[EXTRACT] {zip_path} -> {TARGET_ROOT}")
            z.extractall(TARGET_ROOT)

    bin_dir = TARGET_ROOT / top / "bin"
    clangd_exe = bin_dir / "clangd.exe"
    print(f"[CHECK] clangd.exe exists = {clangd_exe.exists()}")
    print(f"[BIN]   {bin_dir}")
    if not clangd_exe.exists():
        print("[ERROR] clangd.exe missing after extract")
        return 3

    # zip 파일은 정상 완료 후 정리 (재실행 없이 사용 가능하도록)
    try:
        zip_path.unlink()
        print(f"[CLEAN] removed {zip_path}")
    except OSError as e:
        print(f"[WARN] cleanup skipped: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
