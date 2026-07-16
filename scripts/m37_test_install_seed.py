# -*- coding: utf-8 -*-
"""M37: install 스크립트 seed 시맨틱 테스트 harness (WELC).

검증 대상: install.ps1 / install.sh 의 '글로벌 가이드 설치' 섹션
- 세대 관리 파일(extended-protocols.md, domain/CURATOR-PROMPT.md)은 항상 갱신되는가
- seed 파일(domain/GRAPH.md 등)은 기존 사용자 파일을 덮어쓰지 않는가
- 사용자가 추가한 개인 entry 는 생존하는가
- 신규 설치(빈 홈)에서는 seed 전체가 배포되는가

방식: USERPROFILE(HOME)을 임시 디렉토리로 리다이렉트하여 실제 스크립트를 E2E 실행.
install.ps1 은 $env:USERPROFILE, deploy_power.py 는 Path.home()(=USERPROFILE) 기준이므로
실제 홈은 건드리지 않는다.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

REPO = Path(r"C:\Users\hcsung\work\kiro\ai-developer-mickey")
SEED = REPO / "mickey"

PASS, FAIL = 0, 0

def check(name: str, cond: bool, detail: str = ""):
    global PASS, FAIL
    mark = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{mark}] {name}" + (f" — {detail}" if detail and not cond else ""))

def run_install_ps1(fake_home: Path):
    """임시 홈으로 install.ps1 실행 (실제 홈 미접촉)."""
    env = os.environ.copy()
    env["USERPROFILE"] = str(fake_home)
    r = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", str(REPO / "install.ps1")],
        capture_output=True, text=True, env=env, cwd=str(REPO), timeout=300,
        encoding="utf-8", errors="replace",  # PS 출력에 non-cp949 바이트 존재 가능
    )
    return r

def seed_entry_names():
    return sorted(p.name for p in (SEED / "domain" / "entries").glob("*.md"))

def main():
    tmp = Path(tempfile.mkdtemp(prefix="m37_install_test_"))
    try:
        fake_home = tmp / "home"
        fake_home.mkdir()
        mickey = fake_home / ".kiro" / "mickey"

        # ── 시나리오 1: 신규 설치 (빈 홈) — seed 전체 배포 ──
        print("=== 시나리오 1: 신규 설치 (빈 홈) ===")
        r = run_install_ps1(fake_home)
        check("install.ps1 정상 종료", r.returncode == 0, f"rc={r.returncode}\n{r.stdout[-500:]}\n{r.stderr[-500:]}")
        check("extended-protocols.md 배포", (mickey / "extended-protocols.md").exists())
        check("domain/CURATOR-PROMPT.md 배포", (mickey / "domain" / "CURATOR-PROMPT.md").exists())
        check("domain/GRAPH.md seed 배포", (mickey / "domain" / "GRAPH.md").exists())
        check("patterns/INDEX.md seed 배포", (mickey / "patterns" / "INDEX.md").exists())
        installed_entries = sorted(p.name for p in (mickey / "domain" / "entries").glob("*.md"))
        check(f"entries seed 전체 배포 ({len(seed_entry_names())}건)", installed_entries == seed_entry_names())

        # ── 시나리오 2: 기존 사용자 홈 — 개인 지식 보호 + 세대 관리 갱신 ──
        print("=== 시나리오 2: 재설치 (기존 사용자 홈) ===")
        # 사용자 개인 지식 시뮬레이션: seed 파일 변조 + 개인 entry 추가
        (mickey / "domain" / "GRAPH.md").write_text("USER-DATA-M37-GRAPH", encoding="utf-8")
        (mickey / "domain" / "INDEX.md").write_text("USER-DATA-M37-INDEX", encoding="utf-8")
        (mickey / "domain" / "entries" / "user-own-entry.md").write_text("USER-OWN", encoding="utf-8")
        (mickey / "patterns" / "INDEX.md").write_text("USER-PATTERNS", encoding="utf-8")
        # 세대 관리 파일은 구버전 시뮬레이션 (stale)
        (mickey / "extended-protocols.md").write_text("STALE-PROTOCOL", encoding="utf-8")
        (mickey / "domain" / "CURATOR-PROMPT.md").write_text("STALE-CURATOR", encoding="utf-8")

        r = run_install_ps1(fake_home)
        check("재실행 정상 종료", r.returncode == 0, f"rc={r.returncode}")
        check("GRAPH.md 미덮어쓰기 (개인 지식 보호)",
              (mickey / "domain" / "GRAPH.md").read_text(encoding="utf-8") == "USER-DATA-M37-GRAPH")
        check("INDEX.md 미덮어쓰기 (개인 지식 보호)",
              (mickey / "domain" / "INDEX.md").read_text(encoding="utf-8") == "USER-DATA-M37-INDEX")
        check("patterns/INDEX.md 미덮어쓰기",
              (mickey / "patterns" / "INDEX.md").read_text(encoding="utf-8") == "USER-PATTERNS")
        check("개인 entry 생존", (mickey / "domain" / "entries" / "user-own-entry.md").exists())
        check("extended-protocols.md 갱신 (세대 관리)",
              (mickey / "extended-protocols.md").read_bytes() == (SEED / "extended-protocols.md").read_bytes())
        check("CURATOR-PROMPT.md 갱신 (세대 관리)",
              (mickey / "domain" / "CURATOR-PROMPT.md").read_bytes() == (SEED / "domain" / "CURATOR-PROMPT.md").read_bytes())

        # ── 시나리오 3: install.sh (Git bash 가용 시) ──
        # WSL bash(System32)는 Windows 경로 해석 불가 → Git bash 만 사용
        bash = next((p for p in [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
        ] if Path(p).exists()), None)
        if bash:
            print("=== 시나리오 3: install.sh (Git bash) ===")
            home2 = tmp / "home2"
            home2.mkdir()
            env = os.environ.copy()
            env["HOME"] = str(home2)
            env["USERPROFILE"] = str(home2)  # deploy_power.py(Path.home())도 리다이렉트
            sh_path = str(REPO / "install.sh").replace("\\", "/")  # Git bash 경로 표기
            r = subprocess.run([bash, sh_path],
                               capture_output=True, text=True, env=env, cwd=str(REPO),
                               timeout=300, encoding="utf-8", errors="replace")
            m2 = home2 / ".kiro" / "mickey"
            # rc 대신 seed 섹션 완료 메시지로 판정: Git bash 환경에서는 §4 deploy_power 의
            # `python` 이 WindowsApps 스텁으로 잡혀 실패할 수 있음 (seed 로직과 무관, 실제 Linux 는 python3 사용)
            check("sh: 글로벌 가이드 설치 섹션 완료", "글로벌 가이드 설치" in r.stdout, f"rc={r.returncode}\n{r.stdout[-300:]}")
            check("sh: GRAPH.md seed 배포", (m2 / "domain" / "GRAPH.md").exists())
            # 개인 지식 보호 재현
            (m2 / "domain" / "GRAPH.md").write_text("USER-SH", encoding="utf-8")
            (m2 / "extended-protocols.md").write_text("STALE-SH", encoding="utf-8")
            r = subprocess.run([bash, sh_path],
                               capture_output=True, text=True, env=env, cwd=str(REPO),
                               timeout=300, encoding="utf-8", errors="replace")
            check("sh: 재실행 seed 섹션 완료", "글로벌 가이드 설치" in r.stdout, f"rc={r.returncode}")
            check("sh: GRAPH.md 미덮어쓰기",
                  (m2 / "domain" / "GRAPH.md").read_text(encoding="utf-8") == "USER-SH")
            check("sh: extended-protocols.md 갱신",
                  (m2 / "extended-protocols.md").read_bytes() == (SEED / "extended-protocols.md").read_bytes())
        else:
            print("=== 시나리오 3: bash 미발견 — install.sh 테스트 skip ===")

        print(f"\n결과: {PASS} passed / {FAIL} failed")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
