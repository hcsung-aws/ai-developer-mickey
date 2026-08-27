# M45 조사 ③: FAILED 리포트 4건의 실패 원인 추출
# — 리포트 말미(stderr/에러 메시지)와 stdout 마지막 부분을 확인
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

targets = [
    r"C:\Users\hcsung\work\kiro\epic-lore-benchmark\_curator-staging\curator-invoke-report-20260826-183035.txt",
    r"C:\Users\hcsung\work\kiro\anjin-llm-scenario-poc\_curator-staging\curator-invoke-report-20260827-002113.txt",
    r"C:\Users\hcsung\work\kiro\workshop\_curator-staging\curator-invoke-report-20260827-013700.txt",
    r"C:\Users\hcsung\work\kiro\anjin-llm-scenario-poc\_curator-staging\curator-invoke-report-20260827-103030.txt",
]
# workshop 경로는 추정이므로 실존 확인 후 glob 보정
resolved = []
for t in targets:
    p = Path(t)
    if p.exists():
        resolved.append(p)
    else:
        # work 하위에서 파일명으로 탐색
        hits = list(Path(r"C:\Users\hcsung\work").glob(f"*/*/_curator-staging/{p.name}")) + \
               list(Path(r"C:\Users\hcsung\work").glob(f"*/_curator-staging/{p.name}"))
        resolved.extend(hits)

for p in resolved:
    txt = p.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()
    print("=" * 80)
    print(f"### {p.parent.parent.name} / {p.name} (총 {len(lines)}줄, {len(txt)} chars)")
    # 헤더 8줄
    for l in lines[:8]:
        print("  " + l)
    print("  ...")
    # stderr 섹션 존재 시 출력
    if "## curator stderr" in txt:
        idx = txt.index("## curator stderr")
        print("  [stderr 섹션]")
        for l in txt[idx:idx+1500].splitlines():
            print("  " + l)
    # 마지막 25줄
    print("  [마지막 25줄]")
    for l in lines[-25:]:
        print("  " + l[:180])
    print()
