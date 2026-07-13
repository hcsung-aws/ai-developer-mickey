# -*- coding: utf-8 -*-
"""
m33_verify_path_registry.py
현재 kiro-cli 프로세스는 부모 환경을 상속하므로 PATH 변경이 즉시 안 잡힌다.
registry(HKCU\\Environment\\Path) 를 직접 재조회하여 두 신규 항목이 실제 기록되었는지 확인.
"""
import sys
import winreg

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
    value, value_type = winreg.QueryValueEx(key, "Path")

entries = [e for e in value.split(";") if e]
print(f"[TYPE]    {value_type} (2=REG_EXPAND_SZ)")
print(f"[LEN]     {len(value)} chars, {len(entries)} entries")

wanted = [
    r"C:\Users\hcsung\AppData\Roaming\Python\Python313\Scripts",
    r"C:\Users\hcsung\.local\clangd\clangd_22.1.6\bin",
]
lower_entries = {e.lower() for e in entries}
for w in wanted:
    ok = w.lower() in lower_entries
    tag = "OK" if ok else "MISS"
    print(f"[{tag:4}]    {w}")
