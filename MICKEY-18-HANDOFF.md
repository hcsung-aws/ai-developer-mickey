# Mickey 18 Handoff

## Current Status
dual-env (Windows native + WSL2) 문서 반영 + install.ps1 포팅 완료, 커밋 `595bdfd` 푸시 완료. adaptive.md #2, #3 추가됨.

## Next Steps (사용자 지정 순서)
1. repo `mickey/` ↔ global `~/.kiro/mickey/` 동기화 (global이 최신)
2. `common_knowledge/agent-design-patterns.md` 보강 (Mickey 17 보류)
3. Phase 4 실전 검증 (2026-06-08)
4. 세션 정리

## Important Context
- **동기화 방향**: global → repo (global이 최신). 불일치 6파일 + repo에 없는 entry 3개 (forced-breakpoint-execution, passive-over-active-retrieval, script-to-library-extraction). 반대 방향(install.ps1 실행)은 최신본 손실 위험 — 동기화 완료 전 `install.sh`/`install.ps1` 실행 금지
- **승격 보류**: Curator가 adaptive #2, #3의 project-context.md 승격 2건 제안 → 2~3세션 관찰 후 재검토
- **로컬 환경**: Windows native (PowerShell 5.1), Git Bash 병용 가능. `machine-env.md`에 Code Defender 주의사항 존재

## Quick Reference
- 세션 로그: `MICKEY-18-SESSION.md`
- adaptive 규칙: `context_rule/adaptive.md`
- 글로벌 지식: `C:\Users\hcsung\.kiro\mickey\` (domain, patterns, extended-protocols)
- Context window: ~40%
