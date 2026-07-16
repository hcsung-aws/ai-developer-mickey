# Mickey 지식 서고 — Seed와 개인 그래프의 분리

이 디렉토리는 **모든 Mickey 사용자에게 초기 배포되는 seed 골격**이며, 실제 지식 그래프는 이것으로부터 각 사용자의 홈 `~/.kiro/mickey/` 에서 개인화되어 축적된다.

## 두 저장소의 성격

| 항목 | 프로젝트 원본 `mickey/` | 사용자 홈 `~/.kiro/mickey/` |
|------|-----------------------|----------------------------|
| 성격 | Seed (골격 · 초기 배포용) | 개인 지식 그래프 (실체) |
| 관리 주체 | 이 프로젝트 컨트리뷰터 (git) | 각 사용자 · Knowledge Curator |
| 수정 흐름 | 사람이 직접 · 세대 갱신 시 | Curator 가 세션마다 자동 |
| 배포 방향 | `install.ps1` / `install.sh` 로 프로젝트 → 사용자 홈 (단방향) | — |
| 사용자 간 동일성 | 동일 (git 관리) | **필연적으로 다름** — 각자 다른 지식 축적 |

**핵심 원칙**: 개인 지식 그래프는 프로젝트에 커밋되지 않는다. 이 원칙은 최근 결정으로 확정되었으며, 이 프로젝트 자체(Mickey 를 개선 대상으로 삼는 프로젝트)도 예외가 아니다.

## Seed 최소 조건 (프로젝트 원본에 반드시 있어야 하는 파일)

새 사용자가 이 리포지토리를 clone 하고 `install.ps1` 실행 시, 사용자 홈에서 Knowledge Curator 가 즉시 동작할 수 있으려면 아래 파일이 프로젝트에 존재해야 한다.

```
mickey/
├── README.md                 # 본 파일 — 서고 계약서
├── extended-protocols.md     # T1.5 상세 프로토콜 (양방향 관리 예외)
├── patterns/
│   └── INDEX.md             # 빈 상태여도 무방, 존재는 필수
└── domain/
    ├── INDEX.md             # 빈 상태여도 무방, 존재는 필수
    ├── GRAPH.md             # 빈 상태여도 무방, 존재는 필수
    ├── PROFILE.md           # 사용자별 채워질 프로필 (템플릿)
    └── CURATOR-PROMPT.md    # Knowledge Curator 프롬프트 원본
```

`entries/` 아래 개별 파일과 `patterns/` 아래 개별 파일은 **seed 필수 조건이 아니다**. 축적된 개인 지식이므로 원칙적으로 프로젝트에 없어야 한다. 다만 교육 · 데모 목적의 seed 예시 몇 건을 남기는 것은 예외 정책으로 허용될 수 있다 (사용자 결정 사안).

## 예외 파일 — `extended-protocols.md`

이 파일만은 프로젝트와 사용자 홈 양쪽에서 관리된다. 이유: v17, v18 등 세대 갱신 시 모든 사용자에게 전파되어야 하는 T1 core protocol 이기 때문. install 스크립트가 `-Force` 로 덮어쓰며, 프로젝트 커밋 시 세대 번호를 명시한다.

## 로딩 규칙 (양쪽 공용)

| 에이전트 | 시점 | 로딩 대상 |
|----------|------|-----------|
| v2 CLI agent (`ai-developer-mickey`) | 세션 시작 (T1.5) | `~/.kiro/mickey/` 존재 시 `extended-protocols.md` + `patterns/INDEX.md` + `domain/INDEX.md` + `domain/GRAPH.md` 우선 |
| v3 Power (`power-mickey`)            | 세션 시작 hook | `~/.kiro/mickey/{patterns,domain}/INDEX.md` 를 지도로 로드 · 상세는 트리거 매칭 시 on-demand |
| Kiro IDE                             | Power 활성화 | v3 와 동일 |

**공통**: INDEX 우선, 상세 entry 는 트리거 매칭 시에만 로딩 (progressive disclosure). INDEX 에 없는 파일은 로딩하지 않음.

## 수정 규칙

### 사용자 홈 (`~/.kiro/mickey/`) — Curator 자동 관리

| 대상 | 수정 주체 | 시점 |
|------|-----------|------|
| `domain/entries/*.md` · `domain/GRAPH.md` · `domain/INDEX.md` | Knowledge Curator 직접 수정 | 세션 종료 시 |
| `patterns/*.md` · `patterns/INDEX.md` · REMEMBER 후보 | Curator 가 `_curator-staging/` 에 초안 · 사용자 승인 후 이동 (Pre-staged Apply) | 세션 종료 시 |

### 프로젝트 원본 (`mickey/`) — 사람이 명시적으로 관리

| 대상 | 시점 | 방법 |
|------|------|------|
| `extended-protocols.md` | 세대 갱신 시 (v17, v18, ...) | 사람이 직접 편집 · 버전 번호 명시 |
| `README.md` (본 파일) | 서고 계약이 바뀔 때 | 사람이 직접 편집 |
| INDEX · GRAPH · PROFILE · CURATOR-PROMPT 템플릿 | 스키마 자체가 바뀔 때 | 사람이 직접 편집 |
| entries/patterns 개별 파일 | **원칙적으로 커밋하지 않음** | 예외 시 사용자 결정 후 선별 커밋 |

## 이 프로젝트만의 특수 사정 (역사적 배경)

Mickey 초창기에는 지식 그래프가 프로젝트별로만 존재했다. 그리고 이 프로젝트(`ai-developer-mickey`) 자체가 "Mickey 를 사용해 Mickey 를 개선하는" 순환 구조라서, 개선 세션의 지식 축적물이 프로젝트 안에 남아 git 에 올라간 이력이 있다. 최근 결정으로 지식 그래프가 글로벌(사용자 홈)로 승격되면서 이 관행은 종료되었으며, 프로젝트에 이미 커밋된 잔재(`domain/entries/*.md` 10건 등)의 정리 방침은 별도로 결정한다.

## 관련 문서

- v17 정본 프롬프트: `../examples/ai-developer-mickey.json`
- v10 마이그레이션 계획: `../IMPROVEMENT-PLAN-v10-power-migration.md`
- 세부 프로토콜: `extended-protocols.md`
- 패턴 지도: `patterns/INDEX.md`
- 도메인 지도: `domain/INDEX.md`
- Curator 프롬프트: `domain/CURATOR-PROMPT.md`

## Last Updated

2026-07-04 (v10 Phase 1 · seed vs 개인 그래프 분리 원칙 명시)
