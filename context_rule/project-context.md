# Project Context

## Environment
- WSL2 (Linux) + Windows Kiro IDE
- Git repo: hcsung-aws/ai-developer-mickey

## Goal
생성형 AI 어시스턴트(Kiro)를 효과적으로 활용하기 위한 실전 가이드 및 에이전트 시스템 개발/개선

## Constraints
- CRLF: Windows 쪽 파일은 CRLF, repo는 LF
- Context window 효율성 중시

## Key Decisions
- 시스템 프롬프트 변경 시 3곳 동기화 필수 (활성 agent JSON, repo JSON, 독립 md)

## Lessons Learned
- "목적"을 체크리스트 항목으로만 두면 AI가 작업에 몰입할수록 전체 그림을 놓침 → 독립 문서 + 지속적 참조 메커니즘 필요

## Last Updated
2026-02-22
