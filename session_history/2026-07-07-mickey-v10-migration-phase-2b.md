# 2026-07-07 · Mickey v10 마이그레이션 · Phase 2b

**세션 목표**: v17 T1 프롬프트(278줄)를 v3 power steering 6종으로 이식.

## 착수 배경

- Phase 2a(2026-07-07 이전 세션) 산출물 7건 디스크 반영 검증 완료.
- 참고 자산: `scripts/output/v17_prompt.md`(T1 원문 dump) + `docs/v2-to-v3-mapping.md`(이식 매트릭스).
- 계획서 §6 Phase 2b · §8-b 재조정 원칙(steering=진입점, T1.5·그래프 노드는 원본 유지)에 따라 진행.

## 이번 세션 초입에서 정정된 오해

- 본좌 초기 계획: `power-mickey/steering/` 잔존 5개 파일을 "폐기/대체" 관점으로 표에 포함.
- 사용자 정정: 잔존 5개는 IDE 시절 별도 축소본으로 계보가 다름. 이식 논리에 관여시키지 말고 Phase 2b 마지막에 삭제만 하면 된다.
- 반영: 이식 원본은 오직 `examples/ai-developer-mickey.json` T1(v17, 278줄).

## 확정된 진행 원칙

- 각 steering 200줄 이내(Clean Code).
- T1.5 §N은 트리거 문장만. 상세 이식 금지.
- 지식 그래프 노드(entries/patterns)는 접근 경로만.
- P3: 조건부 지시는 양쪽 분기 병기.
- 각 파일 상단에 v17 원문 대응 주석(줄 번호) 명시하여 Phase 2c 검증기가 활용 가능하게.
- 파일별 순차 검토 방식.

## 산출물 계획

| # | 파일 | v17 원문 범위 | 상태 |
|---|------|-------------|------|
| 1 | `power-mickey/steering/mickey-core.md` | L3~17, L254~271 | 착수 |
| 2 | `power-mickey/steering/session-protocol.md` | L21~87 | 대기 |
| 3 | `power-mickey/steering/knowledge-graph.md` | L158~242 | 대기 |
| 4 | `power-mickey/steering/problem-solving.md` | L111~154 | 대기 |
| 5 | `power-mickey/steering/document-schema.md` | L89~107 | 대기 |
| 6 | `power-mickey/steering/context-window.md` | L244~252 | 대기 |

## 잔존 5개 파일 처리

- 옵션 A 채택: Phase 2b 마지막에 삭제.
- 백업은 `power-mickey.pre-v10-bak.zip`에 이미 존재.
- 대상: `mickey-core.md`, `session-protocol.md`, `problem-solving.md`, `memory-protocol.md`, `self-improvement.md` — 앞 3개는 신규 6종과 이름이 겹치므로 신규 생성 시 자동으로 덮어써짐. 뒤 2개는 종료 시 명시적 삭제 필요.

## 진행 로그

- 2026-07-07 착수: 세션 로그 개시.
- 2026-07-07: `mickey-core.md` 초안 작성 시작.


## Phase 2b 완료 (2026-07-07)

### 산출물 (6개 steering)

| # | 파일 | 줄 수 | v17 원문 범위 |
|---|------|-------|--------------|
| 1 | `power-mickey/steering/mickey-core.md` | 67 | L3~17, L254~271 |
| 2 | `power-mickey/steering/session-protocol.md` | 115 | L21~87 |
| 3 | `power-mickey/steering/knowledge-graph.md` | 158 | L158~242 + Curator 규약 |
| 4 | `power-mickey/steering/problem-solving.md` | 88 | L111~154 |
| 5 | `power-mickey/steering/document-schema.md` | 87 | L89~107 (11종) |
| 6 | `power-mickey/steering/context-window.md` | 58 | L244~252 |

총 573줄. 각 파일 200줄 이내(계획서 §6 Phase 2 CC 통과).

### 부수 산출물 (스크립트 2건)

- `scripts/m34_check_steering_size.py` — 파일별 크기·필수 요소 사전 검증기 (Phase 2c 정식 검증기의 사전 단계)
- `scripts/m34_verify_backup_zip.py` — 잔존 파일 삭제 전 백업 안전망 확인

### 삭제된 파일 (계보가 다른 IDE 시절 유물)

- `power-mickey/steering/memory-protocol.md` (백업: `power-mickey.pre-v10-bak.zip`)
- `power-mickey/steering/self-improvement.md` (백업: 동일 zip)

나머지 3개(`mickey-core.md`, `session-protocol.md`, `problem-solving.md`)는 신규 생성으로 자동 덮어써짐.

### 최종 검증 결과 (m34_check_steering_size.py 전체 실행)

- PASS 6 / FAIL 0 / 총 6
- 모든 파일에 front matter · v17 원문 대응 주석 · H1 헤더 확인.

### 파일별 검토 이력 (사용자 승인 시점)

1. `mickey-core.md` — 초안 75줄 → 사용자 지시에 따라 "다른 steering과의 관계" 섹션 제거 (fileMatch/manual 세분화 전이라 불필요) → 67줄로 확정.
2. `session-protocol.md` — 115줄 초안 그대로 확정.
3. `knowledge-graph.md` — 158줄 초안 그대로 확정.
4. `problem-solving.md` — 88줄 초안 그대로 확정.
5. `document-schema.md` — 87줄 초안 그대로 확정.
6. `context-window.md` — 58줄 초안 그대로 확정.

### 이번 세션 반성 사항

- 본좌가 인계 문서에서 "python -c one-liner 두 번 위반" 반성을 했음에도 이번 세션에서 한 번 더 위반. Windows cmd 셸에서 `python -c "import pathlib..."` 시도 → SyntaxError. 즉시 `.py` 스크립트로 전환하여 복구했으나 규율 미숙 반복. 다음 세션에서는 이 함정을 사전에 인지하고 `.py` 우선 접근을 유지해야 함.
- cp949 콘솔이 em-dash(—) 출력을 못하는 문제도 반복. 스크립트 print 문에서 ASCII 문자만 쓰는 규율을 지켜야 한다.

## Phase 2c 인계 (다음 세션)

### 다음 세션 목표

`scripts/verify_power_structure.py` (정식 Test Harness) 작성 및 실행.

### 검증 항목 6개 (계획서 §6 Phase 2c)

1. **파일 존재**: POWER.md + mcp.json + steering/*.md 6개
2. **front matter 유효성**: POWER.md front matter(name/description/keywords) + 각 steering `inclusion` 필드
3. **readSteering 매핑 완결성**: POWER.md 안내가 steering 6개 모두 커버
4. **T1 100% 추적성**: v17 prompt 원문 dump(`scripts/output/v17_prompt.md`)의 핵심 키워드가 steering 어딘가에 존재
   - REMEMBER 12개 (핵심 키워드)
   - Session Protocol 4단계 헤딩
   - Document Schema 11종 파일명 (매핑 문서 §3.4의 "10종" 표기는 오기, 실제 11개)
   - Problem-Solving 10단계 번호
5. **T1.5 트리거 존재**: 매핑 §4 표의 트리거 예시 문구가 지정 steering에 존재
   - session-protocol.md: §1, §3, §4, §9, §10, §13, §14, §16, §17, §19
   - knowledge-graph.md: §8→§17, §9, §12, §17, §18
   - problem-solving.md: §2, §4, §5, §6, §7, §10, §14, §15
   - mickey-core.md: §4, §6, §9, §10, §11, §14, §15
6. **P3 양쪽 분기 병기**: 조건부 지시 문구 검색 시 부정 조건도 함께 존재 (예: "존재 시" 와 "미존재 시" 쌍)

### 참고 자산 (Phase 2c 필독)

- `docs/v2-to-v3-mapping.md` §3~§4 — 이식 매트릭스 (검증 기준의 원본)
- `scripts/output/v17_prompt.md` — T1 원문 dump (추적성 검증의 정답지)
- `scripts/m34_check_steering_size.py` — 사전 검증기 (Phase 2c 정식 검증기의 뼈대로 확장 가능)

### 후속 Phase 예고

- Phase 3: 세션 관리 hook + 스크립트 (CLI v3용 `.kiro/hooks/*.json` + IDE용 `.kiro.hook` + 공용 파이썬 스크립트)
- Phase 4-A: Knowledge Curator 로직을 `knowledge-curator.md` steering 으로 흡수
- Phase 5: install 스크립트 개편 + 문서 갱신 + 회귀 검증

Phase 2c 는 verify 스크립트 작성 + 실행으로 짧게 끝날 것으로 예상. 산출물은 그 스크립트 1건 + 실행 로그.
