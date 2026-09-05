# Context Rule INDEX

## Rule Map

| 트리거 | 파일 | 요약 |
|--------|------|------|
| 프롬프트 수정, 문서 구조, 시스템 프롬프트 | project-context.md | 프로젝트 환경/목표/제약/교훈 |
| Power 수정, Kiro IDE Power, POWER.md, steering 수정, hook, memorygraph | kiro-powers.md | Powers 동작 방식/설계 결정/알려진 이슈/Windows 반영 |
| 동기화, 방향 판정, install, HANDOFF, commit 확인, 저장소 정합성, cp949, Python 인코딩, 콘솔 잘림, 파일 리다이렉트, 셸 리다이렉트 mojibake, 리포트 직접 기록, SESSION 냉동, 디스크 실측, 취소 보고, 글로벌 편집 백업, 런타임 로딩, 인계 위험 실측, 도구 활성 컨텍스트, 암묵 기준 경로, 글로벌 재배포, scripts 배포 세트, FILES 목록 등재, agent JSON drift, 3자 대조, 프로세스 cmdline 실측 | adaptive.md | 반복 패턴 규칙 19건 (자동 호출, 덮어쓰기 방향, global↔repo, 파일별 판정, HANDOFF commit, 기존 체계 검토 우선, 환경 스캔, cp949 3종, SESSION-디스크 불일치, 글로벌 백업, 런타임 로딩 실측, 인계 서술 재정의, 취소 보고 디스크 실측, 경로 상태 도구 컨텍스트 확인, repo scripts→글로벌 재배포 세트, deploy FILES 목록 실측, agent JSON 3자 대조+cmdline 실측, 셸 리다이렉트 금지—Python 직접 utf-8 기록) |

## Last Updated
2026-09-05 (Mickey 48 — adaptive.md 규칙 #19 추가(PowerShell 리다이렉트 인코딩 파괴 → Python 직접 기록), 카운트 18→19건)
