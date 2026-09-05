# -*- coding: utf-8 -*-
"""M48: serena_config.yml 쓰레기 등록 제거 (A1~A3) + work\kiro\.serena 삭제 (B).

D-47-2 사용자 승인분 (2026-09-05):
- A1: C:\\Users\\hcsung\\work            (조상 디렉토리)
- A2: C:\\Users\\hcsung\\work\\kiro       (M47 사고 낙착지, 조상 디렉토리)
- A3: C:\\Users\\hcsung\\AppData\\Local\\Programs\\Kiro (IDE 설치 폴더)
- A4: .kiro\\crew\\workspace 는 유지 (kirocrew 계속 사용 — 사용자 확정)
- B : work\\kiro\\.serena 삭제 (memories 0건 + 7월 캐시뿐 — 실측 확인됨)

안전장치:
- adaptive #10: 편집 전 동일 디렉토리에 백업 생성 (.bak-m48)
- 편집 후 파일 재독으로 결과 검증 (§19.3 공유 파일 주의)
- projects 목록 라인만 수술 — 다른 설정 블록은 바이트 단위로 보존
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8: cp949 환경 필수

CONFIG = Path.home() / ".serena" / "serena_config.yml"
BACKUP = CONFIG.with_name("serena_config.yml.bak-m48")

# 제거 대상 (사용자 승인 A1~A3) — 정확 일치만 제거 (destructive-target-strict-matching)
REMOVE = {
    r"C:\Users\hcsung\work",
    r"C:\Users\hcsung\work\kiro",
    r"C:\Users\hcsung\AppData\Local\Programs\Kiro",
}

# B: 삭제할 고아 .serena 디렉토리
ORPHAN_SERENA = Path(r"C:\Users\hcsung\work\kiro\.serena")


def main() -> int:
    # --- A: config 수술 ---
    text = CONFIG.read_text(encoding="utf-8")
    shutil.copy2(CONFIG, BACKUP)
    print(f"[백업] {BACKUP}")

    lines = text.splitlines(keepends=True)
    removed, kept = [], []
    for line in lines:
        # projects 목록 항목은 "- <경로>" 형태 — 경로를 정확 일치로 비교
        stripped = line.strip()
        if stripped.startswith("- ") and stripped[2:].strip() in REMOVE:
            removed.append(stripped[2:].strip())
            continue
        kept.append(line)

    if len(removed) != len(REMOVE):
        print(f"[중단] 제거 예정 {len(REMOVE)}건 중 {len(removed)}건만 발견: {removed}")
        return 1

    CONFIG.write_text("".join(kept), encoding="utf-8")

    # 재독 검증: 제거 대상이 더 이상 없고, 유지 대상(A4 등)은 남아 있는지
    reread = CONFIG.read_text(encoding="utf-8")
    fail = False
    for path in REMOVE:
        if f"- {path}\n" in reread:
            print(f"[검증 실패] 여전히 존재: {path}")
            fail = True
    must_keep = [
        r"C:\Users\hcsung\.kiro\crew\workspace",  # A4 유지 확정
        r"C:\Users\hcsung\work\kiro\ai-developer-mickey",
    ]
    for path in must_keep:
        if path not in reread:
            print(f"[검증 실패] 유지 대상 소실: {path}")
            fail = True
    if fail:
        print("[복원 안내] 백업에서 복원 필요: " + str(BACKUP))
        return 1

    remaining = [l.strip()[2:] for l in reread.splitlines() if l.strip().startswith("- C:")]
    print(f"[A 완료] 제거 {len(removed)}건: {removed}")
    print(f"[A 완료] 잔여 등록 {len(remaining)}건")

    # --- B: 고아 .serena 삭제 ---
    if ORPHAN_SERENA.exists():
        # 최종 안전 확인: memories가 비어 있는지 (실측 재확인 — 눈대중 금지)
        memories = ORPHAN_SERENA / "memories"
        mem_files = list(memories.glob("*")) if memories.exists() else []
        if mem_files:
            print(f"[중단] memories 비어있지 않음 ({len(mem_files)}건) — 삭제 보류")
            return 1
        shutil.rmtree(ORPHAN_SERENA)
        print(f"[B 완료] 삭제: {ORPHAN_SERENA} (존재 확인: {ORPHAN_SERENA.exists()})")
    else:
        print(f"[B 스킵] 이미 없음: {ORPHAN_SERENA}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
