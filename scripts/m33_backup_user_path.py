# -*- coding: utf-8 -*-
"""
m33_backup_user_path.py
현재 사용자 PATH 값을 파일로 백업한다.
rollback 시 이 파일 내용을 그대로 HKCU\\Environment\\Path 로 되돌리면 됨.
"""
import sys
import time
import winreg
import pathlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = pathlib.Path(__file__).resolve().parents[1]
BACKUP_DIR = REPO / "scripts" / "backup"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# HKCU\Environment\Path 조회 (User 스코프. System 스코프는 건드리지 않음)
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
    value, value_type = winreg.QueryValueEx(key, "Path")

ts = time.strftime("%Y%m%d-%H%M%S")
out = BACKUP_DIR / f"user-path-m33-{ts}.txt"
# 첫 두 줄은 메타(타입/시각), 세 번째 줄이 실제 PATH 값
content = (
    f"# User PATH backup at {ts}\n"
    f"# registry type: {value_type} (2=REG_EXPAND_SZ, 1=REG_SZ)\n"
    f"{value}\n"
)
out.write_text(content, encoding="utf-8")

entries = [e for e in value.split(";") if e]
print(f"[BACKUP] {out}")
print(f"[TYPE]   {value_type}")
print(f"[LEN]    {len(value)} chars, {len(entries)} entries")
