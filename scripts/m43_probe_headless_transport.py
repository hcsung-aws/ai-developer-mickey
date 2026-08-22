# -*- coding: utf-8 -*-
"""M43 probe: kiro-cli chat --no-interactive 전송 경로의 crosstalk 안전성 실측.

검증 항목 (M42 use_subagent probe와 동일 방법론):
  1. in-band 반환: 마커 문자열이 자식 프로세스 stdout으로 왕복하는가
  2. 전역 랑데부 상태 부재: .subagents 디렉토리가 실행 전후 무변화인가
     (delegate crosstalk의 실체였던 저장소 — M42 실측)
  3. 실행 위치 오염 방지: temp 디렉토리에서 실행하여 본 프로젝트의
     conversation resume 상태를 건드리지 않음

판정: 1+2 모두 통과 시 PASS — 직접 subprocess 전송은 delegate와 달리
랑데부 저장소를 경유하지 않음을 증거로 확정.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MARKER = "PROBE-M43-TRANSPORT-OK"
TIMEOUT_SEC = 240  # Kiro #6163(무한 대기) 대비 강제 상한


def snapshot_subagents() -> dict:
    """delegate 전역 상태 디렉토리의 (경로 → mtime) 스냅샷."""
    root = Path(os.environ["LOCALAPPDATA"]) / "kiro-cli" / ".subagents"
    if not root.exists():
        return {}
    return {
        str(p.relative_to(root)): p.stat().st_mtime
        for p in root.rglob("*") if p.is_file()
    }


def main() -> int:
    exe = shutil.which("kiro-cli")
    if not exe:
        print("FAIL: kiro-cli 실행 파일을 찾을 수 없음")
        return 1

    before = snapshot_subagents()

    # temp 디렉토리에서 실행 — 본 프로젝트 디렉토리의 대화 이력 오염 방지
    with tempfile.TemporaryDirectory(prefix="m43probe-") as tmp:
        prompt = f"Reply with exactly this string and nothing else: {MARKER}"
        try:
            proc = subprocess.run(
                [exe, "chat", "--no-interactive", "--trust-tools=", prompt],
                cwd=tmp, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=TIMEOUT_SEC,
            )
        except subprocess.TimeoutExpired:
            print(f"FAIL: {TIMEOUT_SEC}초 타임아웃 — #6163 계열 무한 대기 의심")
            return 1

    after = snapshot_subagents()

    # 항목 1: in-band 반환 확인
    inband = MARKER in (proc.stdout or "")
    # 항목 2: 전역 상태 무변화 확인
    added = set(after) - set(before)
    removed = set(before) - set(after)
    touched = {k for k in set(before) & set(after) if before[k] != after[k]}
    untouched = not (added or removed or touched)

    print(f"exit code        : {proc.returncode}")
    print(f"[1] in-band 마커 : {'PASS' if inband else 'FAIL'}")
    print(f"[2] .subagents   : {'PASS (무변화)' if untouched else 'FAIL'}")
    if not untouched:
        for label, s in (("added", added), ("removed", removed), ("touched", touched)):
            for k in sorted(s):
                print(f"    {label}: {k}")
    if not inband:
        print(f"    stdout tail: {(proc.stdout or '')[-500:]}")
        print(f"    stderr tail: {(proc.stderr or '')[-500:]}")

    ok = inband and untouched
    print(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
