# M45 조사 ②: 전 프로젝트 _curator-staging의 invoke 리포트 판정 라인 수집
# — Curator 실패(FAILED/TIMEOUT/직접 대행)가 언제 어디서 났는지 시계열로 확인
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

work = Path(r"C:\Users\hcsung\work")
reports = []
# depth 3 이내에서 _curator-staging 탐색 (rglob 전체는 느림)
for depth_glob in ("*/_curator-staging", "*/*/_curator-staging", "*/*/*/_curator-staging"):
    for st in work.glob(depth_glob):
        for f in st.glob("curator-invoke-report-*.txt"):
            head = f.read_text(encoding="utf-8", errors="replace")[:1200]
            # 판정 라인 추출
            result = next((l for l in head.splitlines() if l.startswith("[RESULT]")), "(판정 라인 없음)")
            exitline = next((l for l in head.splitlines() if l.startswith("exit:")), "")
            diffline = next((l for l in head.splitlines() if "staging diff" in l), "")
            reports.append((f.stat().st_mtime, st.parent.name, f.name, exitline.strip(), diffline.strip(), result.strip()))

reports.sort()
print(f"총 리포트 {len(reports)}건 (시간순)")
for _, proj, name, exitline, diffline, result in reports:
    print(f"\n[{proj}] {name}")
    print(f"    {exitline} | {diffline}")
    print(f"    {result[:200]}")
