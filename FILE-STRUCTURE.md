# File Structure

## Directory Tree

```
ai-developer-mickey/
├── docs/                        # 핵심 가이드 문서
│   ├── images/                  # 이미지 리소스
│   └── case-study/              # 실전 사례 (Godot, Packet Capture)
├── sessions/                    # 외부 프로젝트 세션 로그 예시
│   └── packet-capture/          # 패킷 캡처 프로젝트 세션
├── examples/                    # 설정 파일 및 예시
│   ├── common_knowledge/        # 지식 관리 예시 (Godot, Testing)
│   └── context_rule/            # 컨텍스트 규칙 예시
├── context_rule/                # 이 프로젝트의 컨텍스트 규칙
├── common_knowledge/            # 이 프로젝트의 범용 지식
├── auto_notes/                  # AI 자동 관찰 기록
├── mickey/                      # 글로벌 가이드 (install.sh로 배포)
├── power-mickey/                # [실험적] Kiro IDE Power
│   └── steering/                # Power steering 파일
├── install.sh                   # 설치 스크립트
├── PURPOSE-SCENARIO.md          # 최종 목적 + 사용 시나리오
├── PROJECT-OVERVIEW.md          # 프로젝트 개요
├── ENVIRONMENT.md               # 환경 정보
├── DECISIONS.md                 # 의사결정 로그
├── IMPROVEMENT-PLAN-v6.3.md     # v6.3 개선 계획
├── IMPROVEMENT-PLAN-v7.md       # v7 개선 계획
├── README.md / README-en.md     # 프로젝트 소개
└── MICKEY-N-SESSION/HANDOFF.md  # 세션 로그 (1~9)
```

## Key Files

| 파일 | 역할 |
|------|------|
| examples/ai-developer-mickey.json | 최신 시스템 프롬프트 (v7) |
| mickey/extended-protocols.md | T1.5 글로벌 가이드 |
| install.sh | Agent JSON + 글로벌 가이드 설치 |
| power-mickey/POWER.md | Kiro IDE Power 온보딩 지침 |

## File Statistics
- 총 파일 수: 80
- 주요 구성: Markdown 문서, JSON 설정, Shell 스크립트, 이미지

## Project Structure Pattern
문서 중심 프로젝트 — 에이전트 설정(JSON) + 가이드 문서(Markdown) + 세션 로그

## Last Updated
2026-03-09
