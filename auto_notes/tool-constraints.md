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
