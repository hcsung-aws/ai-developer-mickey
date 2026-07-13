# -*- coding: utf-8 -*-
"""
m33_extend_user_path.py
사용자 PATH(HKCU\\Environment\\Path) 에 다음 두 폴더를 추가한다.
  1) %APPDATA%\\Python\\Python313\\Scripts   (pyright-langserver 등)
  2) %USERPROFILE%\\.local\\clangd\\clangd_*\\bin  (clangd.exe)

이미 등록된 경로는 skip. 실행 후 WM_SETTINGCHANGE 브로드캐스트로 새 프로세스에 반영.
현재 kiro-cli 세션은 재시작해야 반영됨.
"""
import ctypes
import os
import pathlib
import sys
import winreg

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def find_clangd_bin() -> str | None:
    """.local\\clangd\\clangd_* 폴더 중 clangd.exe 실재 위치의 bin 경로 반환."""
    root = pathlib.Path(os.environ["USERPROFILE"]) / ".local" / "clangd"
    if not root.exists():
        return None
    candidates = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        exe = child / "bin" / "clangd.exe"
        if exe.exists():
            candidates.append(child)
    if not candidates:
        return None
    # 여러 버전 공존 시 가장 최근 수정된 폴더 선택
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    return str(latest / "bin")


def add_to_user_path(paths_to_add: list[str]) -> int:
    """중복 제외 후 사용자 PATH 에 append. 변경 있으면 broadcast."""
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS
    ) as key:
        current, value_type = winreg.QueryValueEx(key, "Path")
        # 빈 항목 제거 + 대소문자 무시 매칭
        entries = [e for e in current.split(";") if e]
        lower_set = {e.lower() for e in entries}
        added: list[str] = []
        for p in paths_to_add:
            if p.lower() in lower_set:
                print(f"[SKIP] already in PATH: {p}")
                continue
            entries.append(p)
            lower_set.add(p.lower())
            added.append(p)
            print(f"[ADD]  {p}")
        if not added:
            print("[INFO] No changes required")
            return 0
        new_value = ";".join(entries)
        # 원본 레지스트리 타입 유지 (보통 REG_EXPAND_SZ=2)
        winreg.SetValueEx(key, "Path", 0, value_type, new_value)
        print(f"[WROTE] {len(new_value)} chars, {len(entries)} entries (type={value_type})")

    # WM_SETTINGCHANGE 브로드캐스트 → 새로 뜨는 프로세스가 갱신된 PATH 상속
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_long()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        ctypes.c_wchar_p("Environment"),
        SMTO_ABORTIFHUNG,
        5000,
        ctypes.byref(result),
    )
    print("[BROADCAST] WM_SETTINGCHANGE dispatched")
    return len(added)


def main() -> int:
    pyright_scripts = str(
        pathlib.Path(os.environ["APPDATA"]) / "Python" / "Python313" / "Scripts"
    )
    targets: list[str] = []
    if pathlib.Path(pyright_scripts).exists():
        targets.append(pyright_scripts)
    else:
        print(f"[WARN] Pyright Scripts dir missing: {pyright_scripts}")

    clangd_bin = find_clangd_bin()
    if clangd_bin:
        targets.append(clangd_bin)
    else:
        print("[WARN] clangd bin not found — run m33_install_clangd.py first")

    if not targets:
        print("[ERROR] Nothing to add")
        return 1

    changed = add_to_user_path(targets)
    print(f"[DONE] {changed} entries added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
