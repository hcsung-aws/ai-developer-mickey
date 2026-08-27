# Project Context

## Environment
- Supported: Windows native 또는 WSL2 (Linux) — 세부 사항은 ENVIRONMENT.md
- Shell: Windows는 PowerShell / Git Bash, Linux는 bash / zsh
- Git repo: hcsung-aws/ai-developer-mickey

## Goal
생성형 AI 어시스턴트(Kiro)를 효과적으로 활용하기 위한 실전 가이드 및 에이전트 시스템 개발/개선

## Constraints
- Line endings: repo는 LF. Windows native는 `core.autocrlf=input` 권장, WSL↔Windows 파일 공유 시 CRLF 변환 필요
- Kiro CLI agent 캐시: agent JSON 변경 후 ping 검증은 새 세션 부팅 필요 (M23 발견) — 본 세션 내 검증 불가
- Context window 효율성 중시 (3-Tier 로딩)
- **repo `mickey/` = 설치 seed 골격 (미러 아님, M44 정정)**: 서고 계약(mickey/README.md, 2026-07-04 확정) — 개인 도메인 지식·patterns·PROFILE 실데이터는 공개 repo에 커밋 금지. 예외는 [Seed 예시] 라벨 10건 + 세대 파일(extended-protocols, CURATOR-PROMPT — adaptive #3의 실제 적용 범위, global↔repo hash 동기화 유지). m37_mickey_mirror_diff.py의 대량 GLOBAL_ONLY는 정상 상태이니 세대 파일 diff만 판정 대상
- **headless Curator는 서비스 스로틀로 간헐 절단 (M45 실측)**: ModelThrottleError "unexpectedly high load"로 자식 kiro-cli가 작업 도중 exit 1 — invoke_curator가 1회 재시도 + attempt별 stderr/stdout 전문 로그 내장. 실패 시 리포트 파일에서 원인 즉시 확인 가능

## Key Decisions
- 시스템 프롬프트 변경 시 3곳 동기화 필수 (활성 agent JSON, repo JSON, 독립 md)
- Mickey의 차별점은 "점진적 harness 구축" — Greenfield 최적화된 트렌드(Harness Engineering, AI-DLC)와 달리, 세션이 쌓일수록 Brownfield에서도 지식이 두꺼워지는 모델
- 자율 실행 방향: 자율성은 수단, 피드백 루프가 핵심. Completion Criteria 명확 + rollback 가능 + 결과 검증 가능한 작업은 자율 진행 장려
- v9.1 Curator 진화 루프 (M22): 직접 수정 영역(domain/+adaptive.md) + Pre-staged Apply 영역(staging→사용자 일괄 결정)으로 마찰 최소화
- T1.5 §17 Knowledge Lifecycle + §18 Activity Metrics (M22, baseline: 5주 31세션 측정)

## Lessons Learned
- "목적"을 체크리스트 항목으로만 두면 AI가 작업에 몰입할수록 전체 그림을 놓침 → 독립 문서 + 지속적 참조 메커니즘 필요
- INDEX의 범위를 지식 파일에 한정하지 말 것 — 프로젝트 핵심 파일(소스, 설정, 테스트)도 트리거로 가리키면 "프로젝트 전문가의 머릿속 지도"에 가까워짐
- INDEX는 "진실"이 아니라 "탐색의 출발점" — Verify(현실과 대조), Update(불일치 시 수정), Suggest(개선 제안) 원칙 적용 필요
- **자가 개선 진단 시 측정 도구의 정밀도는 단일 정밀화로 끝나지 않음** — 각 변형 적용 후에도 측정 도구의 한계를 의심해야 함. M25(9개 항목) → M26(12개+per-key) → M27(deep leaf diff) 의 반복 깊이 확장이 가설 공간을 정정. 글로벌 entry: `~/.kiro/mickey/domain/entries/iterative-measurement-deepening.md` (Mickey 27)
- **인계 사항도 새 세션 진입 시 디스크 상태 재확인** — M26 이 dangling staging 5세션 보류로 인계했으나 M27 진입 실측 결과 다른 프로젝트가 이미 정식 위치로 머지 완료. 인계는 "원본"이 아닌 "그 시점 관찰" — 새 세션은 디스크 재스캔으로 정합성 확인 필요 (Mickey 27)

## Last Updated
2026-08-27 (Mickey 45 — headless Curator 스로틀 간헐 절단 제약 추가)
