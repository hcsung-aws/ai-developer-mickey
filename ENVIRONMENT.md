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
- Branch: master (v2 CLI agent 트랙 전용) / `mickey-power` (v10 Power 트랙, 별도 clone `c:\Users\hcsung\work\kiro\mickey-power`) — D-38-1

## Code Analysis Tools (§19 감지, M37 실측)
- Tier 1: Serena — `.serena/` 존재 (감지됨)
- Tier 1: Graphify — `graphify-out/` 없음 (미사용)
- Tier 3: Kiro CLI 내장 `code` — `.kiro/settings/lsp.json` 존재 (LSP 활성)

## Autonomy Preference
Level 2 (Balanced) + batch-confirm-autonomous-proceed 패턴 유효

## Key Paths (repo-relative)
- CLI 에이전트: `examples/ai-developer-mickey.json`
- Knowledge Curator: `examples/knowledge-curator.json` (prompt SoT = `~/.kiro/mickey/domain/CURATOR-PROMPT.md`, 동기화는 `scripts/m37_sync_curator_prompt.py`)
- 글로벌 가이드 seed: `mickey/` (install이 seed 시맨틱으로 배포 — 세대 관리 파일만 항상 갱신, D-37-1)
- Power Mickey: `power-mickey/` (작업은 mickey-power 브랜치에서만)
- 문서: `docs/`
- 세션 예시: `sessions/`
- 설치 스크립트: `install.ps1` (Windows) / `install.sh` (bash)

## Dependencies
- Kiro CLI (https://github.com/aws/kiro-cli)

## Notes
- **Line endings**: repo는 LF. Windows native는 Git `core.autocrlf=input` 권장, WSL↔Windows 파일 공유 시 CRLF 변환 필요
- **과거 운영 기록**: docs/07-changelog.md §22 (WSL2 SIMD 제약), sessions/self/ (WSL↔Windows 동기화 패턴)

## Last Updated
2026-07-16 (Mickey 37 — 브랜치 전략(D-38-1), Code Analysis Tools §19 감지 결과, Autonomy Preference, seed 시맨틱 반영)
