# -*- coding: utf-8 -*-
"""
m33_probe_lsp_deps.py
LSP 관련 언어 런타임/서버 실행 파일 존재 여부를 PATH 에서 조사한다.
Kiro CLI /code init 이후 설치 필요 대상을 산출하기 위함.
"""
import sys
import shutil

# Windows cp949 방어 (must-follow-rules)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 조사 대상: 런타임 + LSP 서버 실행 파일
targets = {
    "runtime": [
        "node", "npm", "npx",
        "python", "py", "pip", "pipx",
        "cargo", "rustup",
        "go",
    ],
    "lsp_server": [
        "typescript-language-server",   # ts/js
        "pyright-langserver",           # python (실제 실행 파일)
        "pyright",                       # python (프론트엔드)
        "rust-analyzer",                # rust
        "clangd",                        # c/cpp
        "gopls",                         # go
        "solargraph",                    # ruby
        "jdtls",                         # java
    ],
    "compiler": [
        "clang", "gcc", "cl",
    ],
}

def probe(name: str) -> str:
    path = shutil.which(name)
    return path or ""

print("=== Runtime ===")
for name in targets["runtime"]:
    p = probe(name)
    tag = "OK" if p else "MISS"
    print(f"[{tag:4}] {name:32} {p}")

print()
print("=== LSP Server ===")
for name in targets["lsp_server"]:
    p = probe(name)
    tag = "OK" if p else "MISS"
    print(f"[{tag:4}] {name:32} {p}")

print()
print("=== Compiler (참고) ===")
for name in targets["compiler"]:
    p = probe(name)
    tag = "OK" if p else "MISS"
    print(f"[{tag:4}] {name:32} {p}")
