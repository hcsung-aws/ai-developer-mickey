# Mickey 41 Session

## Checkpoint
[4/5]

## Session Meta
- Type: Self-Improvement (멀티 세션 동시 실행 시 세션 종료/큐레이션 충돌 해소)
- Date: 2026-07-22 ~ 2026-07-23
- Track: CLI (master 브랜치. power 작업은 mickey-power 디렉토리 — 이곳에서 power-mickey/ 수정 금지, D-38-1)

## Session Goal
멀티 세션(여러 프로젝트 Mickey 동시 실행) 환경에서 Curator delegate + 글로벌 지식 쓰기가 섞이는 문제의 현재 구현 분석 + 격리 해결책 설계·구현 (옵션 A)

## Purpose Alignment
Infrastructure (자기 개선) — 진화 루프(Curator + 글로벌 domain)의 멀티 세션 안전성 확보. Ultimate Purpose의 "글로벌 승격" 메커니즘 자체를 보수

## Previous Context (M40 HANDOFF 요약)
- M40: §20 aspect 판정 데이터 검증 + §20 지침 실측 기준화 (v20). 세션 종료 큐레이션 delegate lock 충돌로 직접 수행 — 동시 쓰기 혼입 실측
- 인계: ① 포스트모템 07-24 이후 ② .m40-bak 정리 ③ Curator 검증 3회차 ④ cloud/ 감시

## Entropy Check (진입 시 실측)
- git clean, M40 커밋(0d7203a) 확인. 프로젝트 staging 미존재. 포스트모템 미도달(07-24)
- 글로벌 staging dangling 1건: remember-inline-shell-ban.md (unreal-mcp-demo 소유 — skip)
- 글로벌 백업: .m40-bak 3건(본 세션에서 정리 완료) + .m058f5f-bak 4건(타 세션 소관, 보존)

## Current Tasks
옵션 A 구현 (TODO 1784694422476): Curator 로컬 격리 + 결정론적 글로벌 승격 스크립트
- Completion Criteria: WELC 테스트 전체 PASS + 3개 동기화 계층(CURATOR-PROMPT/agent JSON/extended-protocols/T1) 검증 스크립트 ALL PASS + install 배포 반영

## Progress
### Completed
- **충돌 구조 실측 분석**: 공유 가변 자원 4개 식별 — ① delegate lock(프로세스 간 공유, 거부식) ② 글로벌 GRAPH/INDEX 직접 read-modify-write ③ 글로벌 _curator-staging 혼입 ④ 백업/스냅샷 명의 혼재. 근본 결함: 유일한 직렬화 장치(delegate lock)가 "직접 대행" 우회로와 분리 가능 → 동시 쓰기 무방비. 증거: GRAPH Last Updated에 타 프로젝트(epic-lore-benchmark M16) 당일 쓰기, unreal-mcp-demo staging 혼입, .m058f5f-bak 혼재
- **옵션 A/B/C 비교 보고 → 사용자 옵션 A 확정**: 2단계 격리 (Curator=프로젝트 로컬 초안만, 글로벌 반영=락 잡힌 결정론적 스크립트). B(락 규율 프롬프트 의무화)는 adaptive #1 위반, C(agent 복제)는 직렬화 제거 역효과로 기각
- **promote_knowledge.py** (scripts/ SoT + ~/.kiro/mickey/scripts/ 배포): gd-*.md 번들 파싱(Meta/ENTRY-BODY heredoc/Node·Edge·Index·Backlink Row) → .promote.lock(mkdir 원자성+owner.json+stale 600s 자동 회수) → .promote-backups/ 백업 → GRAPH/INDEX 삽입(new=insert, augment=Base-Hash 낙관적 검증) → 병합 무결성 검사(FAIL 시 자동 롤백) → backlink → staging 정리 → 리포트 파일. exit 0=PASS/1=CONFLICT·FAIL/2=BUSY
- **WELC 테스트** (test_promote_knowledge.py): 20 tests — 파싱 4, 표 조작 4, 락 3(획득/BUSY/stale 회수), E2E 4(신규 전체 승격/augment/dry-run/빈 staging), 충돌 3(new 중복/해시 불일치/부분 성공), 롤백 1(dangling→원복), 락 경합 1. **20 PASS + 전체 스위트 123 PASS**
- **CURATOR-PROMPT.md 개정** (SoT): 격리 원칙 신설(글로벌 쓰기 전면 금지), domain 직접 수정→gd- 승격 번들, 글로벌 staging deprecated(모든 후보 프로젝트 staging + Target: global 마커), 출력 형식/응답 처리 개정
- **knowledge-curator.json 2곳** (m41_apply_curator_isolation.py): prompt 동기화 + fs_write allowedPaths에서 `~/.kiro/mickey/domain/**` 제거 (프롬프트+권한 이중 차단) + description 갱신 — 검증 21체크 ALL PASS (m41_verify_isolation.txt)
- **extended-protocols §17 v20→v21** (m41_apply_protocols_v21.py): 라이프사이클 다이어그램/권한 표/Pre-staged 5단계 개정 + "글로벌 승격 락 규약" 신설 + "글로벌 파일 백업 네이밍 규약(.bak-<project>-m<N>)" 신설 + 글로벌 staging deprecated — global/repo 해시 일치 + 구 문구 잔존 0 ALL PASS
- **T1 v17→v18** (m41_apply_t1_v18.py): Session End 2~3단계 격리 구조 반영(delegate BUSY 시 직접 대행 안전 명시, gd- 승격 promote 경유) — 활성 JSON+repo JSON 동기화 ALL PASS (독립 md는 v17부터 부재 실측, m32 선례)
- **install.ps1/sh**: promote_knowledge.py를 세대 관리 파일로 배포 추가 (~/.kiro/mickey/scripts/) + 즉시 수동 배포 완료
- **백업 정리**: 글로벌 .m40-bak 3건 삭제(M40 인계, 안정 확인됨). repo 내 .bak 잔재 정리(git 추적이므로 불필요)

- **Curator 런타임 반영 실측 (probe)**: 파일 접근 금지 probe를 delegate로 실행 → 개정본 프롬프트 확인 ("격리 원칙 M41" YES, 3단계 제목 "직접 수정 실행 (adaptive.md만)"). **delegate subagent는 launch 시점에 agent JSON을 새로 읽음** — M23 캐시 제약은 메인 세션 agent 한정 (auto_notes/tool-constraints.md 기록)
- **세션 종료 큐레이션 (Curator 검증 3회차 — 격리 구조 첫 실전) PASS**: 글로벌 쓰기 0건 (스냅샷 diff의 글로벌 변경은 전부 back-to-basic-modernize의 promote 실행분 — owner 명의로 즉시 식별, 신규 설계 실전 가동 확인). Curator 산출: adaptive #15 직접 수정 + staging 4건 (gd- 2, profile- 1, cr-index 1). 사용자 전체 승인
- **승격 실행**: Base-Hash 스탬프(m41_stamp_base_hash.py) → promote 2/2 PASS (신규 staged-promotion-write-isolation 엣지+3, augment prompt-doc-vs-runtime-loading 엣지+1, 무결성 dangling 0). PROFILE.md "LLM-결정론적 하이브리드" 성향 추가(백업 규약 준수). context_rule/INDEX 카운트 15 갱신. staging 청소 완료

### In Progress
- (없음)

### Blocked
- (없음)

## Key Decisions
- D-41-1: 멀티 세션 격리는 옵션 A (Curator 로컬 격리 + promote 스크립트). 근거: 락 규율을 프롬프트가 아닌 코드로 강제(adaptive #1 + LLM 결정론적 하이브리드 패턴), 사용자 응답 횟수 증가 0 (기존 Pre-staged 일괄 응답에 gd- 합류), delegate BUSY 시 직접 대행이 정식 안전 경로로 승격됨. v9.1 "Curator 직접 수정" 결정은 domain/ 범위에서 철회 (adaptive.md는 프로젝트 로컬이라 유지)
- D-41-2: 글로벌 백업 네이밍 규약 `.bak-<project>-m<N>` (§17 명문화) — 멀티 세션 백업 주체 식별

## Files Modified
- scripts/promote_knowledge.py (신규, SoT) + scripts/tests/test_promote_knowledge.py (신규, 20 tests)
- scripts/m41_apply_curator_isolation.py, m41_verify_isolation.py, m41_apply_protocols_v21.py, m41_apply_t1_v18.py (적용/검증 스크립트)
- ~/.kiro/mickey/domain/CURATOR-PROMPT.md + mickey/domain/CURATOR-PROMPT.md (SoT 개정+동기화)
- ~/.kiro/agents/knowledge-curator.json + examples/knowledge-curator.json (prompt+권한)
- ~/.kiro/mickey/extended-protocols.md + mickey/extended-protocols.md (v21)
- ~/.kiro/agents/ai-developer-mickey.json + examples/ai-developer-mickey.json (T1 v18)
- install.ps1, install.sh (scripts 배포 추가)
- ~/.kiro/mickey/scripts/promote_knowledge.py (글로벌 배포본)
- 글로벌 백업: CURATOR-PROMPT.md/extended-protocols.md에 .bak-ai-developer-mickey-m41 생성, .m40-bak 3건 삭제

## Lessons Learned
- serena create_text_file이 활성 프로젝트 루트(work\kiro 상위)에 오배치 — tool-implicit-root-path-trap 재현 2회차. 세션 시작 시 도구 활성 컨텍스트 확인 필요 (M41)
- PowerShell `;` 체이닝에서 New-Item이 Copy-Item 뒤에 오면 디렉토리 미존재 실패 — 생성을 항상 선행 (사소하나 순서 의존)
- cp949 콘솔 잘림 재확인 (adaptive #14 준수): 적용 스크립트 stdout이 잘려도 리포트 파일 실측으로 판정
- [Protocol] delegate subagent는 launch 시점에 디스크의 agent JSON을 로딩 — M23 "agent JSON 캐시, 새 세션 부팅 필요"는 메인 세션 agent에 한정됨. 설정 변경 후 무해 probe(도구 금지 + 프롬프트 마커 질의)로 ~6초에 버전 검증 가능 (M41)

## Context Window Status
~75% (세션 종료 시점)

## Next Steps
- **power 트랙 인계**: power-mickey/steering/knowledge-curator.md + session-protocol.md가 구 구조(Curator 직접 수정) 기술 — v21 격리 구조로 개정 필요. D-38-1에 따라 mickey-power 디렉토리 세션에서 수행할 것. 참조: 이 SESSION의 Progress + §17 v21
- **다른 활성 프로젝트 전파**: 활성 agent JSON은 즉시 반영됨(다음 세션부터). 각 프로젝트의 잔존 글로벌 staging 항목(remember-inline-shell-ban 등)은 Source 프로젝트가 처분
- Curator 검증 3회차: M41 세션 종료 시 격리 구조로 첫 실전 검증 (gd- 번들 산출 확인)
- 포스트모템 트리거: 2026-07-24 이후 §18 실측
