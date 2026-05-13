# Project Context

## Environment
- Supported: Windows native 또는 WSL2 (Linux) — 세부 사항은 ENVIRONMENT.md
- Shell: Windows는 PowerShell / Git Bash, Linux는 bash / zsh
- Git repo: hcsung-aws/ai-developer-mickey

## Goal
생성형 AI 어시스턴트(Kiro)를 효과적으로 활용하기 위한 실전 가이드 및 에이전트 시스템 개발/개선

## Constraints
- Line endings: repo는 LF. Windows native는 `core.autocrlf=input` 권장, WSL↔Windows 파일 공유 시 CRLF 변환 필요
- Context window 효율성 중시

## Key Decisions
- 시스템 프롬프트 변경 시 3곳 동기화 필수 (활성 agent JSON, repo JSON, 독립 md)
- Mickey의 차별점은 "점진적 harness 구축" — Greenfield 최적화된 트렌드(Harness Engineering, AI-DLC)와 달리, 세션이 쌓일수록 Brownfield에서도 지식이 두꺼워지는 모델
- 자율 실행 방향: 자율성은 수단, 피드백 루프가 핵심. Completion Criteria 명확 + rollback 가능 + 결과 검증 가능한 작업은 자율 진행 장려

## Lessons Learned
- "목적"을 체크리스트 항목으로만 두면 AI가 작업에 몰입할수록 전체 그림을 놓침 → 독립 문서 + 지속적 참조 메커니즘 필요
- INDEX의 범위를 지식 파일에 한정하지 말 것 — 프로젝트 핵심 파일(소스, 설정, 테스트)도 트리거로 가리키면 "프로젝트 전문가의 머릿속 지도"에 가까워짐
- INDEX는 "진실"이 아니라 "탐색의 출발점" — Verify(현실과 대조), Update(불일치 시 수정), Suggest(개선 제안) 원칙 적용 필요

## Last Updated
2026-05-13 (Mickey 18)
