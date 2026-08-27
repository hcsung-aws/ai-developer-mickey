# Mickey 45 Session

## Checkpoint
[1/5]

## Session Meta
- Type: Maintenance (진화 루프 인프라 진단)
- Date: 2026-08-27 ~
- Track: CLI (master 브랜치)

## Session Goal
① 말폼 드리프트(installer-auth GRAPH 행) 설명 + 기원 조사 ② Curator 반복 실패 원인 규명

## Purpose Alignment
Infrastructure — 진화 메커니즘(Curator→promote 루프)의 신뢰성이 시나리오 1·2 전체의 기반

## Previous Context (M44 HANDOFF 요약)
- M44 완료: README 한/영 최신화 + 글로벌 그래프 전면 감사 → baseline 동결(GRAPH-HEALTH-BASELINE-2026-08-25.md, D-44-1 데이터 불변) + 개선 A(promote 라우팅) B(Curator 엣지 규율) C(§3 v27 + graph_audit 상비화) 반영. D(미러 리마인더)는 서고 계약 충돌로 철회(D-44-4)
- 인계: 재측정 사이클(수 주 후), 분류 후보(agent-design + game-qa), changelog 백필, Curator 검증 3/5회차, 글로벌 .bak 정리, 자율성 수준 미기록(ENVIRONMENT.md)

## Entropy Check (진입 시 실측, 2026-08-27)
- _curator-staging/: 리포트 4건만 (dangling 0, curation 락 없음 — 정상)
- 루트 SESSION 누적: M39~M43 5세션분 잔존 → 아카이빙 후보
- graph_audit 실행 (baseline+2일): dangling 0 / Path 결손 0 (불변 조건 유지)
  - **신규 드리프트 1건**: installer-auth-state-followup-gap (back-to-basic M20, 08-27 promote) — GRAPH Nodes 행 malformed(셀 수 이상, 미이스케이프 파이프 추정) + INDEX 경로 대조 불일치 + 차수 1. 개선 A 이후 promote인데 표 결함 발생 → 재측정 시 핵심 반례 후보
  - orphan 2 (baseline 1): external-source-digest-separation(기존) + cloud anchor 노드 신규 검출
  - 중복 엣지 5쌍 (baseline 4): heuristic-verifier <-> unit-test-vs-live-latent-gap 신규
  - [M] cloud 드리프트 5건 (baseline 5, 증가 없음 — A-① 유효 신호)
- [Protocol] §22 원스트라이크 발동: 감사 실행 시 `&` 체이닝 사용 (M43/M44와 동일 함정) — 이후 인라인은 단순 단일 명령만

## Current Tasks
- [x] 말폼 드리프트 기원 조사 | CC: 최초 유입 시점 + 원인 특정 → 2026-07-24 epic-lore M17, 코드 스팬 파이프 미이스케이프
- [x] Curator 실패 원인 규명 | CC: 실패 리포트 + kiro.log 실측 → ModelThrottleError (서비스 과부하)
- [x] 개선 A: invoke_curator 재시도+상세 로깅 | CC: 테스트 통과 → 161/161, 글로벌 배포 ALL PASS
- [x] 개선 B: promote 파이프 위생 + CURATOR-PROMPT 규율 | CC: 테스트 통과 + m37 sync ALL PASS
- [x] 개선 C: GRAPH 86행 수선 + graph_audit 파서 수정 | CC: 재감사 [L] 0 + [G] 불일치 0

## Progress
### Completed
- 컨텍스트 로딩 (T2 + T3a + T1.5 v27 + 글로벌 INDEX 2종. GRAPH.md는 on-demand 보류)
- 엔트로피 체크 + graph_audit 실측
- **말폼 드리프트 기원 규명** (m45_drift_curator_probe.py): installer-auth-state-followup-gap GRAPH 86행 "언제" 셀에 미이스케이프 `|| true`. 최초 등장 = 2026-07-24 epic-lore M17 promote 백업 — **한 달 전 기존 결함, baseline 32행에 "정리 후보(보류)"로 이미 등재**. 세션 시작 시 "신규 드리프트" 보고는 오판 (baseline 미대조). 엣지 3행 + INDEX 행은 `\|\|`로 올바름 → gd- 번들의 노드 행만 이스케이프 누락. graph_audit [G] INDEX 불일치는 이 malformed 행의 파싱 어긋남 파생 증상
- **가드 부재 확인**: promote_knowledge.py, CURATOR-PROMPT.md 양쪽 모두 파이프 이스케이프 규율/검증 없음
- **Curator 실패 실체 규명** (m45_curator_report_scan.py + m45_failed_report_read.py + m45_kiro_log_errors.py): 최근 이틀 8회 중 4회 실패 (epic-lore 08-26 18:30, anjin 08-27 00:21 + 10:30, workshop 01:37). 전 건 자식 kiro-cli가 작업 도중 exit 1 (adaptive 수정까지 정상 진행 후 절단된 사례 포함). kiro.log 실측: **ModelThrottleError "unexpectedly high load" + HTTP 500 stream 실패 반복 후 abort** — 서비스 측 스로틀링. 성공/실패 교차 발생은 부하 간헐성과 정합. kiro-cli.EXE 08-26 00:55 갱신 직후부터라는 시간 상관도 존재 (확정 불가)
- **진단 공백 발견**: invoke_curator.py가 proc.stderr를 캡처만 하고 리포트 미기록 — 실패 원인이 매번 유실
- **개선 3종 구현 완료 (사용자 승인: A+B+C 전부 + 로그 최대 상세화)**:
  - A (invoke_curator.py): exit≠0 시 1회 재시도(기본 60초 대기, --retries/--retry-delay 인자화) + 시도별 exit/elapsed/stdout·stderr 크기/staging diff + stderr·stdout 전문 보존 + kiro-cli 버전·command 환경 증거 + 타임아웃 부분 출력 보존. 타임아웃은 재시도 없이 중단 (스로틀 절단과 양상 상이)
  - B (promote_knowledge.py): escape_pipes_in_code_spans(코드 스팬 내 `\|` 자동 정규화) + split_cells(이스케이프 존중) + validate_cell_count(스키마 5/4/3/3, 쓰기 전 fail-fast) — parse_bundle에 배선. CURATOR-PROMPT.md에 이스케이프 규율 추가 (백업 .bak-ai-developer-mickey-m45, m37 sync ALL PASS — agent JSON 2곳 + repo seed)
  - C (데이터 수선): GRAPH.md 86행 `\|\|` 이스케이프 (백업 .bak-ai-developer-mickey-m45) + graph_audit.py INDEX 파서 이스케이프 존중 수정 + m43_deploy_global_scripts.py FILES에 graph_audit.py 등재 (M44 누락 보완) + baseline 문서 수선 각주
  - 검증: pytest 161/161 (baseline 149 + 신규 12), 글로벌 배포 4파일 ALL PASS, 재감사 [A][B] 0 유지 + [L] 0 + [G] 불일치 0

### In Progress
- (없음)

### Blocked
- (없음)

## Key Decisions
- **D-45-1 (사용자)**: 말폼 드리프트 + Curator 실패 대응 3종 전부 적용 — A(invoke 재시도+상세 로깅) B(promote 파이프 위생+CURATOR-PROMPT 규율) C(GRAPH 86행 수선+audit 파서 수정). 로그는 최대 상세화 (시도별 전문 보존). C는 D-44-1(데이터 불변)의 예외 — audit 파싱을 방해하는 결함이라 수선하되 baseline에 각주로 기록하여 재측정 오염 방지
- **D-45-2**: 타임아웃(1800초 hang)은 재시도하지 않음 — 스로틀 절단(45~429초 exit 1)과 실패 양상이 달라 무인 30분 추가 대기는 부적절. 재시도는 exit≠0에만

## Files Modified
- scripts/invoke_curator.py (+글로벌 배포) — 재시도 + 상세 로깅
- scripts/promote_knowledge.py (+글로벌 배포) — 표 행 위생 3함수 + parse_bundle 배선
- scripts/graph_audit.py (+글로벌 배포) — INDEX 파서 이스케이프 존중
- scripts/m43_deploy_global_scripts.py — FILES에 graph_audit.py 등재
- scripts/tests/test_invoke_curator.py — 재시도/stderr/타임아웃 테스트 4종 (1종 대체)
- scripts/tests/test_promote_knowledge.py — TestRowHygiene 9종
- 글로벌 CURATOR-PROMPT.md (SoT) + agent JSON 2곳 + repo seed — 이스케이프 규율 (m37 sync)
- 글로벌 GRAPH.md 86행 수선 (백업 2종: GRAPH/CURATOR-PROMPT .bak-ai-developer-mickey-m45)
- GRAPH-HEALTH-BASELINE-2026-08-25.md — 수선 각주
- scripts/m45_*.py 조사 스크립트 6종
- MICKEY-45-SESSION.md

## Lessons Learned
- [Protocol] §22 위반 1회 (`&` 체이닝) — 원스트라이크 발동, 잔여 셸 작업 단순 명령/스크립트 전용
- [Protocol] **baseline 미대조 신규 판정 오판**: 세션 시작 엔트로피 체크에서 malformed 행을 "신규 드리프트"로 보고했으나 baseline 문서 32행에 이미 등재된 기존 결함이었음 — 감사 결과를 baseline과 대조하기 전에 신규/기존 판정 금지 (process-fix-over-data-fix-remeasure의 대조 원칙)
- **진단 도구 자신도 이스케이프 계약의 소비자**: graph_audit이 GRAPH 파서에는 이스케이프 존중 split을 쓰면서 INDEX 파서에는 naive split을 써서 오탐 생성 — 같은 파일 내 파서 간 계약 불일치. 수선(C)이 오탐을 드러내 도구 버그까지 연쇄 발견 (verification-tool-as-health-scanner의 역방향 사례)
- **배포 목록 등재 누락 재발**: M44가 graph_audit을 "글로벌 배포"했다고 기록했으나 m43_deploy_global_scripts.py FILES에는 미등재 — install 경유만 배포됨. adaptive #16의 사각지대 (deploy 스크립트 자체의 목록 최신성)

## Context Window Status
~15% (세션 시작)

## Next Steps
- (사용자 작업 확정 후)
