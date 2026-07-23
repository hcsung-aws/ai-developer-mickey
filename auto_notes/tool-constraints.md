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
