# Mickey 19 Handoff

## Current Status
repo↔global 동기화(파일별 방향 판정) + agent-design-patterns 보강 + Curator 후속(domain INDEX 정합성 + 제안 P1/P2) 모두 완료. Code Defender(GitDefender) 실체 조사 후 ~/.kiro/mickey/machine-env.md를 절차 상세화로 재작성. master `2e77709` push 완료.

## Next Steps
- Phase 4 실전 검증 (2026-06-08 예정)
- adaptive.md 규칙 #2~5 중 일부는 3+ 세션 유효성 확인 후 context_rule/ 또는 patterns/ 승격 검토 (Curator가 다음 세션에서 재검토 가능)

## Important Context
- **이번 세션이 발견한 패턴**: Mickey 18이 domain entry 파일 3개를 만들었지만 INDEX.md 행은 2개만 누락된 상태로 남았음 → 다음 세션에서 동일 실수 반복 방지 위해 entry 생성 시 INDEX 동시 갱신 확인 필요. adaptive.md #4(파일별 방향 판정 3회차)와 결합되는 패턴.
- **CURATOR-PROMPT 동기화 방향**: repo가 v2(5단계, Mickey 16), global이 v1(3단계)이었음. install 스크립트는 repo→global 방향이라 그대로 두면 v2가 자동 배포됨 → 이번에 수동 복사로 일치시킨 상태. 다음 install 실행은 안전.
- **Code Defender = GitDefender (Amazon 사내)**: machine-env.md에 명령(`request-repo`/`self-attest`)·dry-run 검증·fallback(`--no-verify`)·자율 실행 경계 모두 명시됨. 다음 push 시 묻지 말고 dry-run → 통과면 push, 차단이면 사용자에게 명령 옵션 2개 제시.
- **Curator 호출 방식 검증**: 세션 종료 시 use_subagent로 knowledge-curator 호출 → CURATOR-PROMPT.md 절차로 응답하여 직접 수정 + 제안 분리해서 반환. v2(5단계)가 정상 동작 확인.

## Protocol Feedback
- [Protocol+] 파일별 동기화 방향 판정이 [Protocol] adaptive.md #4로 규칙화됨. 다음 동기화 세션에서 자연스럽게 참조될 것.
- [Protocol+] machine-env.md를 "설치 사실"이 아닌 "구체 실행 절차"로 작성하니 "code defender 승인 어떻게 해?"가 사라짐. Passive>Active 원칙의 자기 적용 — 글로벌 환경 문서에 동일하게 적용 가능.
- [Protocol−] HANDOFF.md가 Mickey 18에서 git에 add 안 된 상태로 남았던 것이 Mickey 19 엔트로피 체크에서 즉시 잡히지 않음. adaptive #5로 규칙화. extended-protocols §3 엔트로피 관리 항목에 명시 추가 검토 가능 (현재는 adaptive에만 존재).

## Quick Reference
- 세션 로그: `MICKEY-19-SESSION.md` (전체 내역, Curator 결과/제안/후속 작업 모두 기록)
- adaptive 규칙: `context_rule/adaptive.md` (규칙 5건)
- 글로벌 지식: `~/.kiro/mickey/` (domain INDEX 갱신, passive-over-active entry 보강, machine-env 절차 상세화)
- 머신 제약: `~/.kiro/mickey/machine-env.md` (Code Defender 절차 전체)
- 마지막 커밋: `2e77709 Mickey 19 post-Curator` (origin/master 동기화 완료)
- Context window: ~55%
