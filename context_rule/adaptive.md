# Adaptive Rules

> Mickey가 작업 중 발견한 반복 패턴을 규칙화한 것. 세션 종료 시 사용자 확인.

## Rules

1. **'세션 중 자동 호출' 설계는 실패한다 — 판단+다단계 실행 작업은 강제 중단점에 배치** — Mickey 16, TMI-agent + Curator 동일 실패 (2회)
2. **덮어쓰기 방향 실행 전 소스/대상 diff 필수 — 최신본이 어디인지 확인 없이 install/deploy 금지** — Mickey 18, global→repo 방향 오판 시 최신 domain entry 손실 위험
3. **global `~/.kiro/mickey/` 수정 시 repo `mickey/` 동기화 확인 — 누락 시 install이 오래된 내용 배포** — Mickey 18, domain entry 3개 + 6파일 불일치 발견
