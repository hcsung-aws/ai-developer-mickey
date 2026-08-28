# -*- coding: utf-8 -*-
"""m46_merge_index_duplicates.py — 글로벌 domain/INDEX.md 중복 등재 3건 병합 수술 (Mickey 46, 사용자 승인)

병합안 (사용자 검토 완료, 2026-08-28):
  ① powershell-curl-escape: 39+45행 병합 (98행 cmd 측면은 유지) — 3행→2행
  ② packager-vs-monorepo-hoisting: 46행 고유 키워드를 40행에 흡수 — 2행→1행
  ③ decision-implementation-supersede-pattern: 트리거 합집합 — 2행→1행

안전장치: 디스크 재독(shared-file-session-drift-reread) + 각 old 행 정확히 1회 존재 가드
(safe-batch-replace) + 동일 디렉토리 백업(.bak-ai-developer-mickey-m46) + 메모리 내 전체 수행 후 일괄 쓰기.
"""
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # adaptive #8

INDEX = Path.home() / ".kiro" / "mickey" / "domain" / "INDEX.md"
BACKUP = INDEX.with_name(INDEX.name + ".bak-ai-developer-mickey-m46")

# (old 행, new 행 또는 None=삭제) — 전부 현재 디스크 원문 리터럴
OPS = [
    # ① 39행 → 병합 행
    (
        "| PowerShell, curl, Windows, JSON body, escape, quoting, body 파일 분리, API 테스트, powershell -Command 인라인, $_ 소실, 조용한 실패 | entries/powershell-curl-escape.md | Windows PowerShell에서 curl.exe에 JSON body 전달 시 따옴표 소실 + cmd 경유 인라인 `$_` 소실 → body 파일 분리 또는 스크립트 분리 |",
        "| PowerShell, curl, Windows, JSON body, escape, quoting, body 파일 분리, API 테스트, powershell -Command 인라인, $_ 소실, 조용한 실패, .ps1, .py | entries/powershell-curl-escape.md | Windows PowerShell에서 curl.exe에 JSON body 전달 시 따옴표 소실 + cmd 경유 인라인 `$_` 소실 → body 파일 분리(`--data-binary @file`) / `.ps1` / `.py` 스크립트 분리 회피 |",
    ),
    # ① 45행 삭제
    (
        "| powershell escape, curl, json body, windows shell, body 파일 분리, .ps1, .py | entries/powershell-curl-escape.md | PowerShell + curl.exe + single-quoted JSON body 의 Windows escape 함정 — body 파일 분리(`--data-binary @file`) / `.ps1` / `.py` 회피 |",
        None,
    ),
    # ② 40행 → 병합 행
    (
        "| monorepo, npm workspaces, hoisting, packager, node_modules 검사, alpha 도구, 워크스페이스 격리, esbuild, npx --no-install, NodejsFunction bundling, target 디렉토리 devDep | entries/packager-vs-monorepo-hoisting.md | 빌드 도구가 srcDir/node_modules 단순 검사 또는 target dir에서 npx --no-install 실행 시 hoisting 환경에서 의존성/바이너리 누락 → 워크스페이스 격리 또는 대상 devDep 추가 |",
        "| monorepo, npm workspaces, hoisting, packager, node_modules 검사, alpha 도구, alpha cdk construct, AgentCore CDK, 워크스페이스 격리, esbuild, npx --no-install, NodejsFunction bundling, target 디렉토리 devDep | entries/packager-vs-monorepo-hoisting.md | 빌드 도구가 srcDir/node_modules 단순 검사 또는 target dir에서 npx --no-install 실행 시 hoisting 환경에서 의존성/바이너리 누락 → 워크스페이스 격리 또는 대상 devDep 추가 |",
    ),
    # ② 46행 삭제
    (
        "| alpha cdk construct, packager, monorepo hoisting, npm workspaces, srcDir node_modules, AgentCore CDK | entries/packager-vs-monorepo-hoisting.md | Alpha CDK construct packager 의 단순 디렉토리 검사 vs npm workspaces 호이스팅 충돌 → 워크스페이스 분리로 해결 |",
        None,
    ),
    # ③ 41행 → 병합 행
    (
        "| 결정 정정, supersede, Reasoning 보존, Implementation 정정, 이력 추적, 의사결정 관리 | entries/decision-implementation-supersede-pattern.md | 결정 Reasoning 보존 + Implementation만 정정 + supersede 표기로 이력 추적성 유지 |",
        "| 결정 정정, supersede, Reasoning 보존, Implementation 정정, reasoning vs implementation, 이력 추적, 의사결정 관리, 의사결정 거버넌스, ADR | entries/decision-implementation-supersede-pattern.md | 결정 Reasoning 보존 + Implementation만 정정 + supersede 표기로 이력 추적성 유지 |",
    ),
    # ③ 47행 삭제
    (
        "| 결정 정정, supersede, reasoning vs implementation, 의사결정 거버넌스, ADR, 추적성 | entries/decision-implementation-supersede-pattern.md | 결정 본문 Reasoning 보존 + Implementation 만 정정 + supersede 표기로 추적성 유지 |",
        None,
    ),
]

# Last Updated 스탬프 (owner 명의) — 2026-08-28 재독 실측값 (drift: workshop M4 promote 반영)
OLD_STAMP = "2026-08-28 (aws-ai-shift-mysql-workshop Mickey 4 promote — 노드 +2, 엣지 +7)"
NEW_STAMP = "2026-08-28 (ai-developer-mickey Mickey 46 — INDEX 중복 등재 3건 병합 수술 7행→4행, 트리거 유실 0. 직전: aws-ai-shift-mysql-workshop Mickey 4 promote)"

text = INDEX.read_text(encoding="utf-8")

# 1) count-1 가드: 모든 old 행이 정확히 1회 존재해야 진행 (drift 감지)
errors = []
for old, _ in OPS:
    n = text.count(old)
    if n != 1:
        errors.append(f"  [GUARD-FAIL] count={n}: {old[:60]}...")
if text.count(OLD_STAMP) != 1:
    errors.append(f"  [GUARD-FAIL] Last Updated 스탬프 count={text.count(OLD_STAMP)}")
if errors:
    print("[ABORT] 가드 실패 — 디스크 상태가 예상과 다름 (drift 가능). 변경 없음")
    print("\n".join(errors))
    sys.exit(1)

# 2) 백업 생성 (수정 전)
shutil.copy2(INDEX, BACKUP)
print(f"[BACKUP] {BACKUP.name}")

# 3) 메모리 내 일괄 치환/삭제 후 한 번에 쓰기
lines = text.split("\n")
out = []
replace_map = {old: new for old, new in OPS}
for line in lines:
    if line in replace_map:
        new = replace_map[line]
        if new is None:
            print(f"  [DELETE] {line[:70]}...")
            continue  # 행 삭제
        print(f"  [MERGE ] {new[:70]}...")
        out.append(new)
    elif OLD_STAMP in line:
        out.append(line.replace(OLD_STAMP, NEW_STAMP))
        print("  [STAMP ] Last Updated 갱신")
    else:
        out.append(line)

INDEX.write_text("\n".join(out), encoding="utf-8")

# 4) 사후 검증: 대상 3개 entry의 등재 횟수 실측
result = INDEX.read_text(encoding="utf-8")
checks = {
    "entries/powershell-curl-escape.md": 2,   # 병합 행 + 98행(cmd 측면)
    "entries/packager-vs-monorepo-hoisting.md": 1,
    "entries/decision-implementation-supersede-pattern.md": 1,
}
ok = True
for key, expect in checks.items():
    n = result.count(key)
    mark = "PASS" if n == expect else "FAIL"
    if n != expect:
        ok = False
    print(f"  [{mark}] {key}: {n}회 (기대 {expect})")

print(f"\n[RESULT] {'ALL PASS' if ok else 'FAIL — 백업에서 복원 필요'}")
sys.exit(0 if ok else 1)
