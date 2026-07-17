# 도구 제약 사항

## Kiro subagent
- `use_subagent`로 최대 4개 병렬 delegation
- subagent 간 통신 불가 — 의존성 있는 작업은 순차 spawn 필요
- 각 subagent에 충분한 context 전달 설계 필요

## Kiro CLI resources
- `file://` 경로는 프로젝트 CWD 기준 상대 경로 → 글로벌 파일 배포에 부적합
- `file://AGENTS.md`는 Kiro CLI 기본 템플릿 필드 (프로젝트별 에이전트 지시용, 제거 금지)

## README 동기화
- README.md(한글) 변경 시 README-en.md(영문)도 확인 필요
- v6.3 상태 불일치 발견 (Mickey 7에서 수정)

## Last Updated
2026-03-08


## execute_pwsh(cmd 계열) 에서 git commit -m 따옴표 소실 (2026-07-16 트랙 분리 세션, 2회 재현)

- 증상: `git commit -m "여러 단어 메시지"` 실행 시 따옴표가 벗겨져 각 단어가 pathspec 으로 해석됨 (`error: pathspec '...' did not match`)
- 우회: 메시지를 파일로 작성 후 `git commit -F <파일>` 사용. 커밋 후 파일 삭제
- 동일 계열: PowerShell 인라인 명령 미실행(에코만 됨) 사례도 M38 에서 관찰 — 2줄 이상 로직은 .py 스크립트로 분리하는 기존 규칙 준수가 안전
