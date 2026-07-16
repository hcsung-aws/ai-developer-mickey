# -*- coding: utf-8 -*-
"""이전 세션 수정 파일들의 디스크 반영 여부 확인 스크립트.

목적: IDE 에이전트의 파일 쓰기 도구가 에디터 버퍼에만 반영되고
디스크에 flush되지 않는 경우를 탐지한다. 디스크에서 직접 읽어
존재 여부, 크기, 수정 시각, 핵심 마커 문자열 포함 여부를 검사한다.
"""
import os
import sys
import datetime

# 검사 대상: (경로, 반드시 포함되어야 할 마커 문자열 또는 None)
TARGETS = [
    ("session_history/2026-07-13-mickey-v10-migration-phase-5-install.md", "다음 세션 인계"),
    ("PROJECT-OVERVIEW.md", "Power Mickey"),
    ("docs/09-v3-power-migration.md", "Phase 5"),
    ("README.md", None),
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    all_ok = True
    for rel_path, marker in TARGETS:
        full = os.path.join(ROOT, rel_path)
        if not os.path.isfile(full):
            print(f"[MISSING] {rel_path}")
            all_ok = False
            continue
        size = os.path.getsize(full)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full))
        # 디스크에서 직접 읽어 마커 확인 (utf-8 우선, 실패 시 cp949 fallback)
        marker_ok = True
        if marker:
            try:
                with open(full, encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(full, encoding="cp949") as f:
                    content = f.read()
            marker_ok = marker in content
        status = "OK" if marker_ok else "MARKER-FAIL"
        if not marker_ok:
            all_ok = False
        print(f"[{status}] {rel_path} | size={size} | mtime={mtime:%Y-%m-%d %H:%M:%S}"
              + (f" | marker='{marker}' found={marker_ok}" if marker else ""))
    print()
    print("RESULT:", "ALL-SYNCED" if all_ok else "SYNC-PROBLEM")
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
