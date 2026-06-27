# Mickey 21 Handoff

## Current Status
M20 진단(글로벌 0% / Curator 0회) 무효화 확정. 5주간 신규 31세션 실측에서 글로벌 76회 / Curator 82회. M20의 표본 편향(자기 자신 + v8.1 도입 1.5개월)이 결함의 본질. **IMPROVEMENT-PLAN-v9-ADDENDUM** 작성 + 사용자 [O] 3건 승인. **D-7-FIX (권한 보정 + Pre-staged Apply 패턴)** 적용 완료 — knowledge-curator.json v2 + CURATOR-PROMPT.md v3 글로벌+repo 동기화. 엔트로피 체크: M10~M17 SESSION/HANDOFF 16파일 `sessions/` 아카이빙 + auto_notes/NOTES.md Last Updated 갱신. Phase 1 §8 단계 1+2 완료, **단계 3~7은 Mickey 22 인계**.

## Next Steps (Mickey 22 = Phase 1 단계 3~7)

순서 권장 (의존성 + 영향 범위 고려):

### Step 3 — 새 PURPOSE-SCENARIO.md 갱신
- 위치: `PURPOSE-SCENARIO.md`
- 변경: 3-Tier (R/G/S) + Knowledge Curator 진화 루프 + Pre-staged Apply 패턴 반영
- 입력: IMPROVEMENT-PLAN-v9.md §1 + ADDENDUM §1 (측정 baseline)
- 검증: Last Updated/Last Confirmed 갱신, R/G/S 정의 명확

### Step 4 — T1.5 §17 (Knowledge Lifecycle) + §18 (Activity Metrics) 작성
- 위치: `~/.kiro/mickey/extended-protocols.md` + `mickey/extended-protocols.md` (동기화)
- §17 본문 핵심:
  - 라이프사이클 다이어그램 (auto_notes → R/G/S 분기 → Curator + Pre-staged Apply)
  - 분기 판단 기준 (CURATOR-PROMPT.md 2단계 라우팅과 일치)
  - 5회 검증 기간 명시 (Curator fs_write 자동 승인 신뢰 정착)
- §18 본문 핵심:
  - 활용도 메트릭 baseline 표 (ADDENDUM §4 보정 2의 표 그대로)
  - 측정 방법: `scripts/m21_measure_usage.py` 매 5세션마다 자동 실행
  - 임계값 위반 시 행동 (예: < 0.5 도메인 참조 → 활용 저하 경보)
- 주의: ADDENDUM §4에 따라 "knowledge-organization Skill" 표기는 모두 "Knowledge Curator" 로

### Step 5 — T1 시스템 프롬프트 변경 (Session End 단계)
- 위치: `examples/ai-developer-mickey.json` (repo) + `~/.kiro/agents/ai-developer-mickey.json` (활성)
- 변경 핵심:
  - Session End 단계 2: "Knowledge Curator delegate (보정된 권한으로 마찰 최소화)" 명시
  - Session End 단계 3: "Pre-staged 제안 + 단일 응답 (전체/번호/없음/보류)" 흐름 추가
  - Continuing Session 엔트로피 체크: `_curator-staging/` dangling 항목 확인 추가
  - 첫 5회 호출 시 git diff 자동 보고 (검증 기간) 명시

### Step 6 — README/docs/07-changelog.md 에 Tier R/G/S 정의 반영
- 위치: `README.md`, `README-en.md`, `docs/07-changelog.md`, `docs/07-changelog-en.md`
- 변경: v9 항목 추가 (3-Tier + Curator 권한 보정 + Pre-staged Apply)
- 진화 인사이트 (`docs/08-evolution-insight.md`) 도 검토 (M21 진단 입력 추가 가치)

### Step 7 — agent JSON v16 install + 3곳 동기화
- install.ps1/install.sh 실행 또는 수동 동기화
- 동기화 대상 (3곳):
  1. 활성 agent: `~/.kiro/agents/ai-developer-mickey.json`
  2. repo: `examples/ai-developer-mickey.json`
  3. 독립 md: `examples/MICKEY-PROMPT-V*.md` 신규 v9 본문 또는 v8.1 명세 갱신
- 검증: M19 패턴 (파일별 방향 판정) 따라 일괄 install 금지, 파일별 개별 복사

## Important Context

### v9 PLAN의 두 문서 (ADDENDUM 우선)
- 원본 `IMPROVEMENT-PLAN-v9.md` (Mickey 20): 진단 입력 + 미보정 결정 보존
- 보정 `IMPROVEMENT-PLAN-v9-ADDENDUM.md` (Mickey 21): D-3 폐기 / D-7 수정 / D-9 수정 / D-21-A 신규 / D-6 강화
- **충돌 시 ADDENDUM 우선**

### Curator 마찰 해결 핵심 (M22 가 알아야 할 것)
- 마찰의 진짜 원인: `allowedTools: []` 빈 배열 (사용자 매번 승인 요구)
- 해결: `tools` 4개 제한 + `allowedTools` 자동 승인 + `fs_write.allowedPaths/deniedPaths` 안전 가드
- Pre-staged Apply: 제안 영역(common_knowledge/context_rule/patterns/REMEMBER) 은 staging 디렉토리에 초안 작성 후 사용자 단일 응답으로 결정
- N=5회 검증 기간: 첫 5회 Curator 호출 동안 Mickey가 git diff 자동 보고

### vision-math-helper `.kiro/mickey/` 위치 (D-21-A 옵션 B 채택)
- Mickey 자체 변형, 사용자 의도 X
- 옵션 B: 다양성 허용 + 자동 감지 (CURATOR-PROMPT.md §4단계 staging 위치 자동 감지 규칙 이미 반영)
- T1 First Session 도 이 유연성을 명시할지 Step 5에서 검토

### Phase 2~5 영향 (ADDENDUM §5 참조)
- Phase 2 (knowledge-organization Skill 구현): **폐기**. Curator 보정으로 동일 효과
- Phase 3 (활용도 메트릭 자동 측정): **간소화**. m21_measure_usage.py 가 baseline. "5/5 카운터 자동 호출 통합" 1건만
- Phase 4 (마이그레이션): #2 변경 (CURATOR-PROMPT.md → Skill 변환 X), 그 외 우선순위 유지
- Phase 5 (실전 검증): **이미 자연 발생**. Pre-staged Apply 가 같은 프로젝트들에서 마찰 감소 일으키는지만 확인

## Protocol Feedback

- [Protocol+] **subagent 권한 4단 체계의 발견** — Kiro CLI 의 `tools / allowedTools / toolsSettings.fs_write.allowedPaths / deniedPaths` 4단으로 자동 승인 + 안전 가드 동시 적용 가능. 새 메커니즘 추가 전에 항상 기존 권한 체계 사양 확인이 우선.
- [Protocol+] **포스트모템 결론은 충분한 잠복 기간 후 재검증** — M20이 v8.1 도입 1.5개월 후 0% 결론 → 5주 후 정반대 실측. T1.5 §9 포스트모템 자동 트리거 조건에 "도입 후 최소 3개월 경과" 명시 검토 가치.
- [Protocol+] **M14 함정 자기 적용의 진짜 형태** — "추가 전 폐지/검토" 의 진짜 가치는 폐지 후보가 자체 부적격일 때 발견. Mickey 21 ADDENDUM 이 사례.
- [Protocol] **자기 진단 표본 편향 가드** — 자기 자신 위주의 표본은 메타 작업 비중이 높아 도메인 entry 트리거가 적음. 진단 시 다른 프로젝트 표본을 항상 우선 비교.
- [Protocol] **Pre-staged Apply 패턴은 Kiro CLI 기능 범위에서 추가 도구 없이 구현 가능** — 검증 완료. 참고 구현 예시는 CURATOR-PROMPT.md v3.

## Quick Reference
- **본 세션 메인**: `MICKEY-21-SESSION.md` (13 Completed, 6 Decisions, 7 Lessons)
- **새 ADDENDUM**: `IMPROVEMENT-PLAN-v9-ADDENDUM.md` (8 sections, 사용자 [O] 3건 승인)
- **측정 스크립트**: `scripts/m21_measure_usage.py`, `scripts/m21_sample_lines.py`, `scripts/m21_apply_curator_config.py`
- **갱신된 자산**:
  - `~/.kiro/mickey/domain/CURATOR-PROMPT.md` (v3, 10520 bytes)
  - `mickey/domain/CURATOR-PROMPT.md` (repo 동기화, hash 일치)
  - `~/.kiro/agents/knowledge-curator.json` (v2, 7900 bytes)
  - `examples/knowledge-curator.json` (repo 동기화)
- **아카이빙 완료**: `sessions/MICKEY-{10..17}-{SESSION,HANDOFF}.md` (16파일 git mv)
- **Mickey 22 시작점**: 본 HANDOFF Next Steps Step 3부터
- **Context window 인계 시점**: ~80%
