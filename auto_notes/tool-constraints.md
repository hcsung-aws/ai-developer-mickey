# 도구 제약 사항

## Kiro subagent
- `use_subagent`로 최대 4개 병렬 delegation
- subagent 간 통신 불가 — 의존성 있는 작업은 순차 spawn 필요
- 각 subagent에 충분한 context 전달 설계 필요

## Kiro CLI resources
- `file://` 경로는 프로젝트 CWD 기준 상대 경로 → 글로벌 파일 배포에 부적합
- `file://AGENTS.md`는 Kiro CLI 기본 템플릿 필드 (프로젝트별 에이전트 지시용, 제거 금지)

## README 동기화
- README.md(한글) 변경 시 README-en.md(영문)도 확인 필요
- v6.3 상태 불일치 발견 (Mickey 7에서 수정)

## Last Updated
2026-03-08


## execute_pwsh(cmd 계열) 에서 git commit -m 따옴표 소실 (2026-07-16 트랙 분리 세션, 2회 재현)

- 증상: `git commit -m "여러 단어 메시지"` 실행 시 따옴표가 벗겨져 각 단어가 pathspec 으로 해석됨 (`error: pathspec '...' did not match`)
- 우회: 메시지를 파일로 작성 후 `git commit -F <파일>` 사용. 커밋 후 파일 삭제
- 동일 계열: PowerShell 인라인 명령 미실행(에코만 됨) 사례도 M38 에서 관찰 — 2줄 이상 로직은 .py 스크립트로 분리하는 기존 규칙 준수가 안전

## delegate subagent 상태의 프로세스 간 공유 (2026-07-21, Mickey 40)

- 증상: 이 세션에서 knowledge-curator를 한 번도 launch하지 않았는데 첫 launch 시도가 "Agent 'knowledge-curator' is already running"으로 거부됨. 약 2분+ 대기 후에도 동일
- 추정: delegate의 agent별 단일 실행 lock이 kiro-cli 프로세스 간 공유됨 — 타 세션(동시 오픈)의 Curator 실행 또는 비정상 종료 잔여 lock과 충돌
- 관찰: 작업 파일 위치로 문서화된 `.kiro/.subagents/`는 프로젝트/홈 어디에도 미존재 (lock 실체 미확인)
- 영향: 세션 종료 프로토콜의 Curator 호출이 타 세션과 직렬화됨. 동시 실행 시 글로벌 domain/ 동시 수정 위험은 오히려 차단되는 효과도 있음
- 대응(M40): Curator 역할을 메인 세션이 직접 수행(직접 수정 + Pre-staged 절차 동일 적용). 검증 3회차 카운트에는 불포함

## delegate subagent는 launch 시점에 agent JSON을 새로 읽음 (2026-07-23, Mickey 41)

- 실측: 세션 부팅 후 knowledge-curator.json을 수정(M41 격리 개정)하고 같은 세션에서 delegate launch → probe 응답이 개정본 프롬프트 확인 ("격리 원칙 M41" 존재, 3단계 제목 개정판)
- 의미: M23의 "agent JSON 캐시 — 새 세션 부팅 필요" 제약은 **메인 세션 agent에 한정**. delegate subagent는 launch 시점 디스크의 JSON을 사용하므로 본 세션 내 즉시 반영됨
- 활용: Curator 설정 변경 후 무해한 probe(파일 접근 금지 + 프롬프트 내 마커 문구 질의)로 버전 확인 가능 (비용 ~6초)

## delegate 결과 crosstalk의 실체 — 머신 전역 상태 + user_notified 선점 (2026-08-19, Mickey 42)

- 실측: delegate 상태 저장소는 `C:\Users\hcsung\AppData\Local\kiro-cli\.subagents\` — 머신 전역 단일 디렉토리 (M40 "lock 실체 미확인" 종결). 상태 파일 키는 **agent 이름** (`knowledge-curator.json`), 필드: agent/task/status/pid/output/`user_notified`/cwd — **세션 식별자 없음**
- 메커니즘: 결과 수신은 status 폴링뿐 + `user_notified` 선점 플래그 → 먼저 조회한 세션이 타 세션의 결과를 가로챔 (crosstalk). 같은 agent launch 시 기존 작업 replace (문서 명시)
- use_subagent 대비 실측 (probe): 결과 in-band 반환 (summary 도구, 마커 왕복 확인) + 전역 .subagents 무변화 + 실행 아티팩트는 UUID 키 (`cli-checkouts/<UUID>`, `run-receipts/<UUID>`) — crosstalk 구조적 불가
- 잔여 위험: Kiro #6765 (use_subagent 응답 채널 60~95초 절단) — Curator 실전 1회차에서 완주 검증 필요, 완주 판정은 staging 디스크 실측
- 조치 (M42): T1 v19 + T1.5 §17 v24 — Curator 호출 delegate 금지, use_subagent(동기) 전환

## Format-Table 파이프 출력 소실 — 항목 있는데 빈 표 (2026-08-19, Mickey 42)

- 증상: `Get-ChildItem | Select-Object ... | Format-Table | Out-String` 이 항목 2건 존재하는데 빈 출력 반환 (execute 계층에서 렌더 소실 추정)
- 우회: `ForEach-Object { Write-Output (...) }` 로 문자열 직접 조립 — 동일 데이터 정상 출력
- empty-scan-distrust 재현 사례: 첫 스캔 "비어 있음"을 Measure-Object 카운트(2)로 반증 후 재조회
