# Project Context

## Environment
- WSL2 (Linux) + Windows Kiro IDE
- Git repo: hcsung-aws/ai-developer-mickey

## Goal
Power Mickey의 안정적 동작 및 지속적 개선

## Constraints
- Kiro IDE userTriggered hook은 askAgent만 지원
- memorygraph get_recent_activity: Windows에서 project 파라미터 필수 (hang 버그)
- CRLF: Windows 쪽 파일은 CRLF, repo는 LF

## Key Decisions
- Hook: userTriggered + askAgent 방식
- Context loading: 하이브리드 (SESSION-BRIEF + memorygraph 제목/태그만)
- 세션 스크립트: Python (크로스 플랫폼)

## Known Issues
- memorygraph Windows hang 버그 (project 파라미터 누락 시)

## Lessons Learned
- agentSpawn + runCommand는 Kiro IDE에서 동작하지 않음
- context window 절약을 위해 스크립트에서 요약 생성, 에이전트는 결과만 읽기

## Common Commands
```bash
# Windows 디렉토리에 반영
cp power-mickey/POWER.md /mnt/c/Users/hcsung/work/q/power-mickey/
cp power-mickey/steering/*.md /mnt/c/Users/hcsung/work/q/power-mickey/steering/
sed -i 's/$/\r/' /mnt/c/Users/hcsung/work/q/power-mickey/POWER.md /mnt/c/Users/hcsung/work/q/power-mickey/steering/*.md
```

## Last Updated
2026-02-19
