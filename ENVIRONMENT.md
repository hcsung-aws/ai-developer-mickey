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

## Code Analysis Tools (§19 감지, M37 실측 / M49 갱신)
- Tier 1: Serena — `.serena/` 존재 (감지됨)
  - **§19.3 fail-closed 규약 (M47~48 검증 완료)**: MCP 서버는 `--project` 기동 인자 **없이** 운용 (agent JSON / 글로벌 mcp.json 공통). 세션 시작 시 `activate_project <프로젝트 루트 절대 경로>` 명시 실행 + 활성 프로젝트 일치 확인 전까지 Serena 쓰기 도구 사용 금지. 활성화 전 도구 에러는 정상(fail-closed)
  - 머신 전역 등록 목록 `~/.serena/serena_config.yml` — 세션 실행 중 수동 편집 금지 (M48 정리, 등록 17건)
- Tier 1: Graphify — `graphify-out/` 없음 (미사용)
- Tier 3: Kiro CLI 내장 `code` — `.kiro/settings/lsp.json` 존재 (LSP 활성)

## Autonomy Preference
Level 2 (Balanced) + batch-confirm-autonomous-proceed 패턴 유효

## Key Paths (repo-relative)
- CLI 에이전트: `examples/ai-developer-mickey.json` (T1 v20)
- Knowledge Curator: `examples/knowledge-curator.json` (prompt SoT = `~/.kiro/mickey/domain/CURATOR-PROMPT.md`, 동기화는 `scripts/m37_sync_curator_prompt.py`)
- 세션 인프라 스크립트: `scripts/invoke_curator.py`(Curator 유일 진입점 + curation 락 + Base-Hash 자동 기입), `scripts/promote_knowledge.py`(글로벌 승격 전담 + promote 락), `scripts/mickey_lock.py`(공유 락 모듈), `scripts/graph_audit.py`(그래프 무결성 감사) — 글로벌 배포는 `scripts/m43_deploy_global_scripts.py` (수정 시 재배포 세트, adaptive #16)
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
2026-09-05 (Mickey 49 — §19.3 serena fail-closed 규약(M47~48 검증), 세션 인프라 스크립트 경로, T1 v20 반영)
