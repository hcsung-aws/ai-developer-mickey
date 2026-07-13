# Kiro CLI `/code init` 산출물 실제 위치 (.kiro/settings/lsp.json)

> Source: ai-developer-mickey Mickey 33 (2026-07-02)

## Core
Kiro CLI `/code init` 이 생성하는 LSP 설정 파일의 실제 위치는 **`<project>/.kiro/settings/lsp.json`** (2026-07-01 실측). 공식 문서(kiro.dev/docs/cli/code-intelligence/) 표기는 `.kiro/lsp.json` 또는 `lsp.json` 이나, 실제 산출물은 `.kiro/settings/` 하위. 감지 로직/스캐너 설계 시 두 위치 모두 확인해야 안전.

## Decision Context
Mickey 33 (2026-07-01) — 사용자가 `/code init` 실행 후 상태 확인 과정에서 발견. Mickey 프로토콜 T1.5 §19.2 감지 로직은 `.kiro/lsp.json`만 확인하고 있어 새 세션에서 LSP 활성 상태를 오판할 위험. 문서와 실행 결과 간 drift 확인 후 지식으로 등재.

## Tags
kiro-cli, code-intelligence, lsp, lsp-json, settings-location, doc-drift, detection-marker, file-resolution

## Related
- `~/.kiro/mickey/domain/entries/cli-help-output-distrust.md` — 도구 문서와 실 동작 drift 가족 패턴 (`--help` 표기 ≠ 실제 동작)
- `~/.kiro/mickey/domain/entries/empty-scan-distrust.md` — 문서 표기 경로가 미감지되면 다른 후보 위치까지 재확인
- `~/.kiro/mickey/domain/entries/llm-path-normalization.md` — 도구 산출물 경로에 대해 다중 후보 전략 유지

## Content

### 실측 결과 (2026-07-01, Windows)

```
kiro-cli: /code init 실행
프로젝트: C:\Users\hcsung\work\kiro\ai-developer-mickey\

산출물: C:\Users\hcsung\work\kiro\ai-developer-mickey\.kiro\settings\lsp.json  (실재)
문서 표기: .kiro/lsp.json 또는 lsp.json                                      (미실재)
```

### 문서와 실 동작의 관계

Kiro CLI 공식 문서 원문 발췌:
> "This creates `lsp.json` configuration and starts language servers."
> "Delete `lsp.json` from your project root to disable."
> "Automatically initializes on startup if lsp.json exists."

문서에는 `.kiro/lsp.json` (일부 페이지) 또는 `lsp.json` (project root) 로 표기되지만, 실측은 `.kiro/settings/lsp.json`. 문서 drift 가능성 높음. 향후 CLI 버전에서 위치가 변경될 수 있으므로 **감지 로직은 3개 후보 모두 확인**하는 것이 안전:

1. `<project>/.kiro/settings/lsp.json` (2026-07-01 실측 위치)
2. `<project>/.kiro/lsp.json` (일부 문서 표기)
3. `<project>/lsp.json` (다른 문서 표기)

### 활용

- Mickey T1.5 §19.2 감지 마커 목록 확장 후보
- 다른 Kiro CLI 통합 도구 개발 시 lsp.json 경로 하드코딩 회피
- CI/IDE 세팅 스크립트에서 존재 확인할 때 3개 위치 모두 스캔

### 파일 스키마 (실측)

`.kiro/settings/lsp.json` 은 `{"languages": {...}}` 최상위 키 하나. 각 언어별 `name`, `command`, `args`, `file_extensions`, `project_patterns`, `exclude_patterns`, `multi_workspace`, `initialization_options`, `request_timeout_secs` 필드. 자세한 스키마는 Kiro CLI `code-intelligence` 문서 "Custom Language Servers" 섹션 참조.

### 관련 슬래시 커맨드

| 명령 | 효과 |
|------|------|
| `/code init` | lsp.json 신규 생성 + LSP 서버 시작 |
| `/code init -f` | 기존 lsp.json 유지, LSP 서버 강제 재시작 |
| `/code status` | 현재 LSP 서버 상태 조회 |
| `/code logs -l ERROR` | LSP 서버 에러 로그 |

lsp.json 파일 삭제 → 코드 인텔리전스 비활성.
