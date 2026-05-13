# Environment

## Supported Environments

Mickey 프로젝트는 다음 두 환경에서 개발/운영한다.

### Windows (native)
- OS: Windows 10/11
- Shell: PowerShell 또는 Git Bash
- HOME: `%USERPROFILE%` (예: `C:\Users\<user>`)
- Tools: Git for Windows, Python 3, Kiro CLI (`kiro-cli.exe`)

### Linux / WSL2
- OS: Linux (WSL2에서 검증됨)
- Shell: bash / zsh
- HOME: `$HOME` (예: `/home/<user>`)
- Tools: Git, Python 3, Kiro CLI

> 이 머신에만 해당되는 환경 제약은 `~/.kiro/mickey/machine-env.md`에 기록한다 (repo 미포함).

## Project Type
Documentation + Agent Configuration (Markdown, JSON, Python)

## Version Control
- Remote: https://github.com/hcsung-aws/ai-developer-mickey.git
- Branch: master

## Key Paths (repo-relative)
- CLI 에이전트: `examples/ai-developer-mickey.json`
- Knowledge Curator: `examples/knowledge-curator.json`
- 글로벌 가이드 원본: `mickey/extended-protocols.md` (install.sh → `~/.kiro/mickey/`)
- Power Mickey: `power-mickey/`
- 문서: `docs/`
- 세션 예시: `sessions/`
- 설치 스크립트: `install.sh` (bash — Windows는 Git Bash로 실행)

## Dependencies
- Kiro CLI (https://github.com/aws/kiro-cli)

## Notes
- **Line endings**: repo는 LF. Windows native는 Git `core.autocrlf=input` 권장, WSL↔Windows 파일 공유 시 CRLF 변환 필요
- **과거 운영 기록**: docs/07-changelog.md §22 (WSL2 SIMD 제약), sessions/self/ (WSL↔Windows 동기화 패턴)

## Last Updated
2026-05-13 (Mickey 18)
