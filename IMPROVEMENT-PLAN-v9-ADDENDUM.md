# IMPROVEMENT-PLAN-v9 ADDENDUM (Mickey 21)

> **작성**: Mickey 21 (2026-06-19~20)
> **목적**: IMPROVEMENT-PLAN-v9 (Mickey 20, 2026-05-14)의 **진단 입력은 보존**하되, 5주간 누적 데이터로 검증한 결과에 따라 일부 결정과 작업 범위를 **보정**한다. 원본 PLAN을 직접 수정하지 않고 ADDENDUM 형태로 추가하여 의사결정 이력 추적성을 유지한다.
> **Status**: 사용자 승인 대기 → 승인 시 Phase 1 진입

---

## 1. Mickey 21 진단 요약

### 측정 데이터 (5주간 신규 31세션)
- 글로벌 domain 참조: **76회 (avg 2.45/세션)** — M20: 0%
- Curator 호출/언급: **82회 (avg 2.65/세션)** — M20: 0회
- 신규 글로벌 entry: **14+건** (vision-math-helper / gamejob_crawler / code-analyze-helper 3개 프로젝트 출처)
- gamejob_crawler M27이 vision-math-helper M10이 만든 entry 직접 확장 — **이상적 활용 패턴 자연 발생**

### M20 진단의 본질적 결함
1. **표본 편향**: 76세션 중 19세션이 ai-developer-mickey 자기 자신 (메타 작업 위주라 도메인 entry 트리거 부족)
2. **시간 부족**: v8.1 도입 1.5개월 시점, 다른 프로젝트 정착 전
3. **메타 함정**: M20 본인이 진단한 "M14 함정 (추가 전 폐지/검토 먼저)"의 자기 적용 실패

### 결론
v8.1 글로벌 도메인 체계는 **작동하고 있다**. 마찰은 있으나 폐기 대상이 아님. v9 PLAN의 기본 방향(3-Tier R/G/S, 글로벌 도메인 중심, stub 라이프사이클)은 유효. **Curator 폐지 결정만 명확히 잘못됨** — Curator는 "진화 + 마찰 해소" 방향으로 보정.

---

## 2. 결정 보정 요약표

| 결정 | 원본 PLAN | Mickey 21 보정 | 영향 |
|------|----------|---------------|------|
| **D-3** Curator 검증 종료 | 본 진단으로 종료 | **폐기** — Curator가 정상 작동 중임을 5주 데이터로 확인 | 마이그레이션 우선순위 #2 변경 |
| **D-7** Curator → Skill 대체 | knowledge-organization Skill이 Curator subagent 대체 | **수정** — 대체가 아닌 **권한 보정 + Pre-staged Apply 패턴 도입** (D-7-FIX 참조). Skill은 후속 트랙에서 재검토 | Phase 2 범위 변경 |
| **D-6** 글로벌 도메인 중심 | 약한 근거 | **강화** — 5주 데이터 + M27 자연 확장 사례를 입증으로 추가 | 본 ADDENDUM §1을 입증 데이터로 PLAN에 흡수 |
| **D-9** 즉시 Phase 1 진입 | 다음 세션에서 시작 | **수정** — 본 ADDENDUM 적용 후 Phase 1 시작. 작업 범위 자체는 거의 그대로 | 1세션 지연 |
| **D-21-A** (신규) 프로젝트 구조 위치 정책 | 미정의 | **옵션 B 채택** — 프로젝트 루트 또는 `.kiro/mickey/` 둘 다 허용. 측정/탐색 도구가 양쪽 자동 감지 | T1.5 §3 엔트로피 체크 + 측정 스크립트 보강 |

### 그대로 유지되는 결정
- **D-1, D-2, D-4** (분석 표본 정의): 본 진단의 표본 편향 진단 입력으로 보존. 향후 자기 진단 시 표본 다양성 가드로 활용.
- **D-5** 3-Tier R/G/S 단순화: 분류 자체는 옳음. 측정 결과도 R/G/S 자연 분리 확인.
- **D-8** stub 라이프사이클: 유효. Pre-staged Apply 패턴과 자연스럽게 결합.

---

## 3. D-7-FIX: Curator 권한 보정 + Pre-staged Apply 패턴

### 문제 정의 (5주 후 확인된 마찰)
Curator 자체는 작동하나 **마찰 1 (제안 영역 매번 승인 부담)** 이 가장 핵심. Curator가 P1, P2, P3 형태로 항목별 사용자 승인을 요청하여 응답 왕복이 누적됨. 마찰 2 (작은 보강도 승인) + 마찰 3 (Skip 조건 부재) 는 사용자가 "중요치 않음" 으로 판정.

### 해결 방향: 두 변경의 조합

#### 변경 A — knowledge-curator.json 권한 보정

**진짜 원인**: 현재 `"tools": ["*"], "allowedTools": []` 라 모든 도구를 사용 가능하나 사용 시마다 사용자 승인 요구. 마찰의 본질은 권한 누락이지 설계 결함 아님.

**보정안 (knowledge-curator.json 변경분)**:
```json
{
  "name": "knowledge-curator",
  "tools": ["fs_read", "fs_write", "grep", "glob"],
  "allowedTools": ["fs_read", "grep", "glob", "fs_write"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": [
        "~/.kiro/mickey/domain/**",
        "**/context_rule/adaptive.md",
        "**/_curator-staging/**"
      ],
      "deniedPaths": [
        "**/.git/**",
        "**/node_modules/**",
        "**/.venv/**",
        "**/credentials*",
        "**/.env*",
        "**/*.key",
        "**/*.pem"
      ]
    }
  }
}
```

**보안 보장 한계 (정직한 명시)**:
- 확실: `tools` 외 도구는 호출 불가. fs_write 자체에 파일 삭제 동작 없음.
- 조심: `allowedPaths` 외 경로 시도는 차단이 아닌 **사용자 확인 요청** 모드. 100% 차단 아님.
- 결론: 자동화 위험은 매우 낮으나 0%는 아님. 100% 안전을 원하면 fs_write 자동 승인 자체를 빼야 하나 마찰 복원됨.

**완화책 — N회 검증 기간**:
- 첫 5회 Curator 호출 동안 Mickey가 Curator 동작 후 `git diff` 결과를 사용자에게 자동 보고
- 5회 동안 의도와 다른 변경이 0건이면 정상 동작 신뢰 → git diff 자동 보고는 옵션화
- 어느 시점이든 의도 외 변경 발견 시 즉시 fs_write 자동 승인 회수 (allowedTools에서 fs_write 제거)

#### 변경 B — Pre-staged Apply 패턴

**원리**: Curator가 "제안만" 영역(common_knowledge/, context_rule/, REMEMBER 등)에 대해서도 staging 디렉토리에 **초안을 미리 작성**한다. 사용자에게는 staging 위치 + 1줄 요약을 일괄 보고하고 **단일 응답**으로 결정 받는다.

**Curator 출력 형식 변경 (요약)**:
```
## Curator 결과

### 직접 수정 (이미 적용 완료)
- domain/: ...
- adaptive.md: ...

### Pre-staged 제안 (사용자 결정 필요 — 초안 작성 완료)
| # | 대상 | staging 파일 | 1줄 요약 |
|---|------|-------------|---------|
| 1 | common_knowledge/ | _curator-staging/ck-cross-reference-injection.md | 교차 참조 삽입 기법 신설 |
| 2 | context_rule/INDEX.md | _curator-staging/cr-index-trigger-add.diff | adaptive.md 트리거 행 추가 |
| 3 | REMEMBER | _curator-staging/remember-12-batch-confirm.md | AR-5 일괄 채택 패턴 승격 후보 |

→ 응답 형식: "전체" / "1,3" / "없음" / "보류" 중 하나
```

**Mickey의 응답 처리**:
- "전체" → staging 파일 모두를 정식 위치로 이동 + staging 청소
- "1,3" → 해당 번호만 이동 + 나머지 폐기
- "없음" → 모든 staging 폐기
- "보류" → staging 유지 (다음 세션에서 재제시)

**staging 위치**:
- 프로젝트 내: `.kiro/_curator-staging/` (Mickey 표준 위치 또는 비표준 `.kiro/mickey/` 환경 모두 매칭)
- 글로벌 후보: `~/.kiro/mickey/_curator-staging/` (REMEMBER, T1.5 후보)
- gitignore 또는 tracked 모두 가능 — 본좌 권장은 **tracked** (사용자가 git diff로 검토 용이)

**dangling staging 처리**:
- 다음 세션 시작 시 엔트로피 체크에 staging 잔존 항목 1회 보고
- 3세션 이상 보류 시 자동 폐기 후 사용자 알림

---

## 4. Phase 1 작업 범위 보정

원본 PLAN §6 Phase 1 의 5개 작업 중 **3개는 그대로**, **2개는 보정**.

### 그대로 (보정 없음)
- [ ] 새 PURPOSE-SCENARIO.md 갱신 (3-Tier + 진화 루프 반영)
- [ ] Tier R/G/S 정의를 README/docs/07-changelog.md 에 반영
- [ ] agent JSON 신버전 install + 3곳 동기화

### 보정 1 — T1.5 §17 Knowledge Lifecycle 작성

**원본 가정**: knowledge-organization Skill 이 라이프사이클 분기 판단을 수행
**보정**: Curator 가 동일 분기 판단을 수행 (CURATOR-PROMPT.md 의 2단계 라우팅 그대로). §17 본문에서:
- "knowledge-organization Skill" 표기를 모두 **"Knowledge Curator"** 로 교체
- Pre-staged Apply 패턴을 라이프사이클 다이어그램에 반영 (제안 영역 → staging → 사용자 일괄 결정)
- 5회 검증 기간 명시 (Curator fs_write 자동 승인 신뢰 정착 절차)

### 보정 2 — T1.5 §18 Activity Metrics 작성

**원본 가정**: baseline 미정 (Skill 호출 빈도로 측정)
**보정**: 본 ADDENDUM §1 측정 데이터를 baseline 으로 명시.

§18 본문에 포함할 baseline 표:
| 메트릭 | 기준값 (Mickey 21, 5주 31세션) | 임계값 |
|--------|--------------------------------|--------|
| 글로벌 domain 참조 / 세션 | 2.45 | < 0.5 → 활용 저하 경보 |
| Curator 호출 / 세션 | 2.65 | < 0.5 → 호출 저하 경보 |
| auto_notes 참조 / 세션 | 5.55 | < 1.0 → 입구 저하 경보 |
| [Protocol] 태그 / 세션 | 2.03 | < 0.3 → 메타 인지 저하 경보 |

측정 방법: `scripts/m21_measure_usage.py` 를 매 5세션마다 자동 실행 (Mickey 가 5/5 카운터 도달 시 메트릭 출력 후 임계값 위반 보고).

### 보정 3 — T1 시스템 프롬프트 변경 (Session End 단계)

**원본 v8.1**: "Knowledge Curator 호출"
**원본 PLAN**: "knowledge-organization Skill 호출"
**보정**: **"Knowledge Curator delegate (보정된 권한으로 마찰 최소화)"** + "사용자 응답: 전체/번호/없음/보류 중 하나" 명시

또한 T1 Continuing Session 로딩 단계에 다음 추가:
- 엔트로피 체크 시 `_curator-staging/` dangling 항목 확인 → 보류 항목 사용자에게 1회 재제시

---

## 5. Phase 2~5 영향

| Phase | 원본 | 보정 |
|-------|------|------|
| **Phase 2** knowledge-organization Skill 구현 | 1~2세션 | **폐기**. Curator 권한 보정으로 동일 효과 달성. Skill 트랙은 후속 검토 대상으로 보관 (만약 향후 Curator 한계 발견 시 재진입). |
| **Phase 3** 활용도 메트릭 자동 측정 | 1세션 | **간소화**. 본 진단 스크립트(`m21_measure_usage.py`) + `m21_sample_lines.py` 가 이미 작동. Phase 3 작업은 "5/5 카운터 도달 시 자동 호출 통합" 1건만. |
| **Phase 4** 마이그레이션 | 점진 (여러 세션) | **#2 변경** (아래 §6 참조), 그 외 우선순위 유지 |
| **Phase 5** 다른 프로젝트 실전 검증 | 다음 5세션 | **이미 자연 발생 중**. vision-math/gamejob/code-analyze 3개 프로젝트에서 v8.1 패턴 정착 확인. Phase 5 는 본 ADDENDUM 의 권한 보정 + Pre-staged 가 같은 프로젝트들에서 마찰 감소를 일으키는지만 확인. |

---

## 6. 마이그레이션 우선순위 수정

| 순위 | 자산 | 원본 작업 | 보정 작업 |
|------|------|----------|----------|
| 1 | `~/.kiro/mickey/patterns/INDEX.md` | domain 흡수 + 폐지 | **유지** (그대로) |
| **2** | `~/.kiro/mickey/domain/CURATOR-PROMPT.md` | Skill 본체로 변환 | **`examples/knowledge-curator.json` 권한 보정 + CURATOR-PROMPT.md 에 Pre-staged Apply 5단계 추가** (변환 X) |
| 3 | `common_knowledge/agent-design-patterns.md` | domain/entries 이전 + stub | **유지** |
| 4 | `common_knowledge/progressive-disclosure.md` | domain/entries 이전 + stub | **유지** |
| 5 | `context_rule/adaptive.md` | R/G/S 분기 + stub 또는 폐기 | **유지** |
| 6 | `~/.kiro/mickey/domain/PROFILE.md` | Skill 분기 판단 입력 명시 | **Curator 분기 판단 입력 명시** (역할 동일, 명칭만 변경) |

---

## 7. M14 함정 자기 적용 결과 (메타 노트)

원본 PLAN 자체가 "M14 함정(추가 전 폐지/검토 먼저)" 의 자기 적용을 시도했으나 **본 적용 시도가 또 한 번 함정에 빠짐** — Curator 폐지 → 새 Skill 추가가 "추가 전 폐지/검토" 의 형태 변형이지 본질 적용은 아니었음. **본 ADDENDUM 이 진짜 자기 적용**:
- 폐지 검토 → Curator 는 폐지 대상이 아님 (작동 중)
- 그대로 유지 + 마찰만 보정 (권한 + Pre-staged) → 새 메커니즘 추가 0건
- 신규 §17/§18 도 새 추상화가 아닌 기존 동작의 명문화

**교훈 (REMEMBER 후보)**: "추가 전 폐지/검토" 원칙 적용 시, 폐지 후보가 자체 부적격 케이스가 가장 가치 있는 발견. 무엇이 작동 중인지를 정량으로 먼저 측정해야 함.

---

## 8. 사용자 승인 + 다음 단계

### 본 ADDENDUM 승인 사항 (사용자 결정 필요)
- [O] §3 D-7-FIX (권한 보정 + Pre-staged Apply + N=5회 검증)
- [O] §2 결정 보정 (D-3 폐기, D-6 강화, D-7 수정, D-9 수정, D-21-A 옵션 B)
- [O] §4~6 작업 범위 + 마이그레이션 우선순위 보정

### 승인 후 즉시 진행 (Phase 1 진입)
1. `examples/knowledge-curator.json` 보정 (§3 변경 A)
2. CURATOR-PROMPT.md 에 Pre-staged Apply 5단계 추가 (§3 변경 B)
3. 새 PURPOSE-SCENARIO.md 갱신
4. T1.5 §17 (Knowledge Lifecycle) + §18 (Activity Metrics) 작성
5. T1 시스템 프롬프트 변경 (Session End 단계)
6. README/docs/07-changelog.md 에 Tier R/G/S 정의 반영
7. agent JSON 신버전 install + 3곳 동기화 (active agent + repo JSON + 독립 md)

### 본 ADDENDUM 의 위치
- 원본 `IMPROVEMENT-PLAN-v9.md` 와 **동등한 권위** (보정 결정의 SoT)
- 원본 PLAN 의 결정과 본 ADDENDUM 의 보정이 충돌 시 **ADDENDUM 우선**
- 원본 PLAN 은 진단 입력 + 미보정 결정의 보존 용도로 유지 (삭제 X)

---

**작성**: Mickey 21 (2026-06-19~20)
**Supersedes (부분)**: IMPROVEMENT-PLAN-v9.md §6 Phase 1, §7 마이그레이션 우선순위 #2, §9 결정 D-3/D-7/D-9
**Reference**: `MICKEY-21-SESSION.md`, `scripts/m21_measure_usage.py`, `scripts/m21_sample_lines.py`
