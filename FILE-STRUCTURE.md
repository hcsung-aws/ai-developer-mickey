# File Structure

## Directory Tree

```
ai-developer-mickey/
├── docs/                          # 핵심 가이드 문서 (한/영 페어)
│   ├── images/                    # 이미지 리소스 (mickey-poster.png 등)
│   └── case-study/                # 실전 사례 (Godot, Packet Capture)
├── sessions/                      # 세션 로그 아카이브
│   ├── MICKEY-2~20-SESSION.md     # M2~M20 (이전 정리분)
│   ├── MICKEY-21~26-SESSION.md    # M21~M26 (M27 에서 일괄 아카이빙)
│   ├── MICKEY-21~26-HANDOFF.md    # 동
│   ├── packet-capture/            # 패킷 캡처 프로젝트 세션
│   └── self/                      # 자기 개선 세션
├── examples/                      # 설정 파일 + 예시
│   ├── ai-developer-mickey.json   # 최신 시스템 프롬프트 (v9.1)
│   ├── ai-developer-mickey-v5.json # v5 보존 (이력)
│   ├── knowledge-curator.json     # Knowledge Curator subagent (M27 변형 H 적용)
│   ├── knowledge-curator.json.{m24,m25,m26,m27}-bak  # 변형 단계별 백업
│   ├── common_knowledge/          # 지식 관리 예시
│   ├── context_rule/              # 컨텍스트 규칙 예시
│   ├── MICKEY-PROMPT-V5.md        # v5 프롬프트 보존
│   └── MICKEY-PROMPT-V6.md        # v6 프롬프트 보존
├── context_rule/                  # 프로젝트 특화 규칙 (T3a→T3b)
│   ├── INDEX.md                   # 트리거 → 파일 매핑
│   ├── project-context.md         # 환경/목표/제약/교훈
│   ├── kiro-powers.md             # Power Mickey 동작 방식
│   └── adaptive.md                # 반복 패턴 자동 규칙 (Curator 직접 수정)
├── common_knowledge/              # 범용 패턴 지식 (T3a→T3b)
│   ├── INDEX.md                   # + Domain Links 섹션
│   ├── agent-design-patterns.md
│   ├── progressive-disclosure.md
│   └── safe-batch-replace.md      # M22 추가, M25~M27 4세대 재사용 검증
├── auto_notes/                    # AI 자동 관찰 기록 (T3a)
│   ├── NOTES.md                   # 인덱스
│   ├── tool-constraints.md
│   ├── analysis-self-improvement.md
│   ├── analysis-packet-capture.md
│   └── analysis-other-projects.md
├── mickey/                        # 글로벌 가이드 원본 (install.sh → ~/.kiro/mickey/)
│   ├── extended-protocols.md      # T1.5 본문 (§1~§18, v16)
│   ├── domain/                    # 글로벌 도메인 entry 미러
│   └── patterns/                  # 글로벌 patterns 미러
├── power-mickey/                  # [실험적] Kiro IDE Power
│   ├── POWER.md                   # 온보딩 지침
│   ├── mcp.json                   # Memory Graph MCP 설정
│   └── steering/                  # Power steering (mickey-core/session-protocol/...)
├── scripts/                       # 유지보수/진단 스크립트 (Mickey N 별)
│   ├── m21_*.py                   # 사용도 측정 (5주 31세션 baseline)
│   ├── m22_*.{py,ps1}             # T1 동기화 + SESSION 아카이빙 + 커밋 분리
│   ├── m24/m25/m26_*.py           # Curator 변형 진단 (A2/A1/G3 적용 + 비교)
│   └── m27_*.py                   # M27 deep diff + 변형 H + SESSION 아카이빙
├── install.sh / install.ps1       # 설치 스크립트 (bash + PowerShell)
├── PURPOSE-SCENARIO.md            # 최종 목적 + 사용 시나리오 (T2)
├── PROJECT-OVERVIEW.md            # 프로젝트 개요 (T2)
├── ENVIRONMENT.md                 # 환경 정보 (T2)
├── FILE-STRUCTURE.md              # 본 파일
├── DECISIONS.md                   # 의사결정 로그
├── IMPROVEMENT-PLAN-v6.3.md       # v6.3 개선 계획
├── IMPROVEMENT-PLAN-v7.md         # v7 개선 계획
├── IMPROVEMENT-PLAN-v8.md         # v8 개선 계획
├── IMPROVEMENT-PLAN-v8.1.md       # v8.1 개선 계획
├── IMPROVEMENT-PLAN-v9.md         # v9 PLAN (M20)
├── IMPROVEMENT-PLAN-v9-ADDENDUM.md # v9.1 보정 (M21)
├── POSTMORTEM-2026-05-14.md       # M20 v8.1 활용도 진단
├── README.md / README-en.md       # 프로젝트 소개 (한/영)
└── MICKEY-N-SESSION/HANDOFF.md    # 현재 진행 세션 (M27)
```

## Key Files

| 파일 | 역할 |
|------|------|
| examples/ai-developer-mickey.json | 최신 시스템 프롬프트 (v9.1) |
| examples/knowledge-curator.json | Knowledge Curator subagent (M27 변형 H 적용 후) |
| mickey/extended-protocols.md | T1.5 글로벌 가이드 (§1~§18, v16) |
| install.sh / install.ps1 | Agent JSON + 글로벌 가이드 설치 (3 파일 동기화) |
| power-mickey/POWER.md | Kiro IDE Power 온보딩 지침 |
| context_rule/adaptive.md | Curator 직접 수정 영역 (반복 패턴 8건) |
| common_knowledge/safe-batch-replace.md | 4세대 재사용 검증 (M22→M27) |

## File Statistics
- 총 파일 수: ~140 (M27 시점, 디렉토리 별도)
- 주요 구성: Markdown 문서 (가이드/세션 로그), JSON 설정 (에이전트), Python 스크립트 (진단/적용)
- 백업 파일: examples/knowledge-curator.json.{m24,m25,m26,m27}-bak (4단계)

## Project Structure Pattern
**문서 중심 + 자기 개선 루프** — 에이전트 설정(JSON) + 가이드 문서(Markdown) + 세션 로그 + 진단 스크립트가 함께 진화. SESSION/HANDOFF 임계 3 초과 시 `sessions/` 로 아카이빙하여 루트 가시성 유지.

## Last Updated
2026-06-23 (Mickey 27 — SESSION 아카이빙 + 구조 문서 갱신, 파일 카운트 ~140)
