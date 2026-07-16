# 2026-07-09 · Mickey v10 마이그레이션 · Phase 2c

**세션 목표**: v10 power migration Phase 2c 정식 Test Harness (`scripts/verify_power_structure.py`) 작성 및 실행. 계획서 §6 Phase 2 CC 6개 항목을 자동 검증.

## 착수 배경

- Phase 2b(2026-07-07) 산출물: steering 6개 초안 (총 573줄) + 사전 검증기(`m34_check_steering_size.py`) PASS 6/6.
- 이번 세션 인계 지점: 계획서 §9 "Phase 2c 진입"에 명시된 검증기 작성 + 6개 CC 자동 재확인.
- 참고 자산: `scripts/output/v17_prompt.md`(T1 원문 dump), `docs/v2-to-v3-mapping.md`(이식 매트릭스 §3~§4).

## 진행 원칙

- 검증기는 단일 파일(`scripts/verify_power_structure.py`)에 각 검증 항목을 단일 책임 함수로 분리 (Clean Architecture, 느슨한 결합).
- 정답지는 상수 블록(SPEC)에 명시 · 매트릭스 §3~§4 근거 주석 첨부.
- 표준 출력은 ASCII only (Windows cp949 콘솔 대응). 파일 내용은 utf-8.
- 사이드 이펙트 없음. 파일 수정·네트워크 접근 없음.
- 종료 코드: PASS 0 / FAIL 1 (CI 통합 가능).

## 산출물

### 신규 (1건)

- `scripts/verify_power_structure.py` — Phase 2c 정식 Test Harness.
  - 검증 함수 6개 (각 단일 책임): `check_files_exist`, `check_front_matter`, `check_power_covers_steering`, `check_t1_traceability`, `check_t15_triggers`, `check_p3_symmetric`.
  - 유틸: `read_utf8`, `extract_front_matter` (얕은 YAML top-level 파서 — `name/description/keywords/inclusion` 존재 여부만 확인이면 충분).
  - 자료 구조: `CheckResult` dataclass (name / passed / details 리스트).
  - CLI: `--root` 옵션 지원. 기본값 = 프로젝트루트/power-mickey.

### 변경 (1건)

- `scripts/verify_power_structure.py` P3 대칭 쌍 사전 확장 (1차 실행 후):
  - 추가: `("있었을 때만", "없으면")` — document-schema.md HANDOFF Protocol Feedback 분기
  - 추가: `("감지 시", "만 사용 시")` — document-schema.md FILE-STRUCTURE Tier 감지 분기
  - 근거: 결정 이력 D-2c-1 참조

### 미변경 (검증 대상 자산 무손실)

- `power-mickey/POWER.md`, `mcp.json`, `steering/*.md` 6개 — 원본 유지.

## 검증 항목별 결과

### 최종 실행 결과

```
Summary: PASS 6 / FAIL 0 / total 6
Exit Code: 0
```

| # | 검증 항목 | 결과 | 세부 |
|---|---------|------|------|
| 1 | 파일 존재 | PASS | POWER.md + mcp.json + steering/*.md 6개 모두 존재 |
| 2 | Front matter 유효성 | PASS | POWER.md의 name/description/keywords · steering 6개 각각의 inclusion 키 확인 |
| 3 | POWER.md → steering 매핑 완결성 | PASS | POWER.md 본문에 steering 6개 파일명 모두 언급 |
| 4 | T1 100% 추적성 | PASS | REMEMBER 12 · Session 4단계 · Document 11종 · PS 10단계 마커 모두 확인 |
| 5 | T1.5 §N 트리거 존재 | PASS | 매트릭스 §4 표의 트리거 지정 위치 모두 확인 (§8→§17 흡수 언급 포함) |
| 6 | P3 양쪽 분기 병기 | PASS | steering 6개 모두 최소 1쌍 이상의 대칭 표현 확인 |

### 1차 실행에서 발견된 FAIL 과 정정

1차 실행 시 항목 6에서 `document-schema.md` 하나만 대칭 쌍 미검출로 FAIL. 원인은 검증기 사전이 "긍정/부정 쌍"에 좁게 국한된 것. `document-schema.md` 원문은 P3 원칙을 실질 준수(Tier 감지 결과별 분기 · [Protocol] 태그 조건 · HANDOFF Protocol Feedback 있음/없음)했으나 표현 형태가 "선택 갈래 대칭"이라 미매치.

사용자 확인 후 옵션 A(검증기 사전 확장) 선택 → 2차 실행 PASS.

## 결정 이력

- **D-2c-1**: P3 검증 사전 확장 (2026-07-09). 근거: P3 원칙 원문("양쪽 분기 병기")은 "긍정/부정 쌍"뿐 아니라 "선택 갈래 대칭"도 포함. 실제 원문 문구 훼손 없이 검증기 사전에 자연스러운 갈래 표현 2개 추가. Alternative: `document-schema.md` 수정 (부작용: 자연스러운 문장 흐름 훼손, 규약 왜곡 위험).

- **D-2c-2**: 얕은 YAML 파서 사용 (2026-07-09). front matter 검사는 top-level 키 4~5개 존재 여부만 확인하면 되므로 정규식 기반 얕은 파서로 충분. Alternative: PyYAML 의존성 추가 (거부 이유: 의존성 증가 대비 이익 미미, 검증기의 단일 파일 재사용성 훼손).

- **D-2c-3**: 콘솔 mojibake 는 다음 사이클 개선 사항으로 유보 (2026-07-09). 파일 내용은 utf-8, 콘솔 출력은 ASCII only 지만 상세 details 안에 한글 파일명·매칭 문구가 섞여 있어 cp949 콘솔에서는 mojibake 발생. 다음 개선안 후보: `--report <파일경로>` 옵션 추가하여 utf-8 리포트 파일 저장. 이번 세션에서는 종료 코드와 항목별 PASS/FAIL 로 결과 판정 가능하므로 유보.

## 반성 사항

- Phase 2b 세션의 두 반성(`python -c` one-liner · em-dash 출력) 을 이번 세션 내내 준수함. 스크립트 파일 우선 · print 문 ASCII only · 파일 내용은 utf-8. 실전 준수 첫 세션.

## Phase 3 인계 (다음 세션)

### 다음 세션 목표

Phase 3 — 세션 관리 hook + 파이썬 스크립트 제작.

### 계획서 §6 Phase 3 요약

**계층 3분**:
- CLI v3용: `.kiro/hooks/<id>.json` (`SessionStart`/`Stop`/`UserPromptSubmit`)
- IDE용: `.kiro/hooks/<name>.kiro.hook` (`preTaskExecution`/`postTaskExecution`)
- 공용 로직: `.kiro/scripts/mickey_session_boot.py`, `mickey_session_close.py` — hook 은 얇게, 로직은 파이썬에

**양쪽 분기 명시 필수 사례** (P3):
- PURPOSE-SCENARIO.md 존재 여부 → 로드 or 신규 질문
- Serena/Graphify 감지 여부 → INDEX Tool Links 등록 or Tier 3 baseline
- 이전 HANDOFF 존재 여부 → 로드 or Mickey 1 세션 취급
- Brownfield 감지 여부 → 온보딩 수행 or 스킵

**CC**: 스크립트 각각 hook 없이 단독 실행 가능 · v3/IDE 예시 파일 각각 존재.

### 검증 방식 후보

- `scripts/verify_power_structure.py` 를 확장하여 hook·스크립트 검증도 통합할지, 별도 검증기(`verify_hooks.py`)를 만들지 결정 필요.
- 본좌 권고: 별도 파일. 관심사 분리 (SRP). `verify_power_structure.py` 는 steering 구조 검증에 집중, hook 검증은 별건.

### 참고 자산

- Kiro CLI v3 hook 규격은 이 세션 시점 미확정 (계획서 R1). Phase 3 착수 시 실측 확인 필요.
- Kiro IDE hook 형식(`*.kiro.hook`)은 기존 문서 참조 가능.
- `createHook` 도구는 v3 CLI 에서 사용 가능 (권한 있으면).

### 후속 Phase 예고

- Phase 4-A: Knowledge Curator 로직을 `knowledge-curator.md` steering 으로 흡수.
- Phase 5: install 스크립트 개편 + 문서 갱신 + 회귀 검증 (v2/v3/IDE 3 시나리오).

## 이번 세션 컨텍스트 소모 상태

- 세션 진입 시 인수인계 파악 · Phase 2a/2b 매트릭스·steering·POWER.md 실측 · 검증기 작성 · 2회 실행.
- 소모율: 중간 정도. 다음 세션(Phase 3)은 hook 규격 실측 + 신규 파일 4~6개 예상 → 컨텍스트 여유 필요 → HANDOFF 후 `/clear` 권장.

## Last Updated

2026-07-09 (Mickey Phase 2c 완료)
