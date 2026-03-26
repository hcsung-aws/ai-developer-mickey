# IMPROVEMENT-PLAN-v8: 글로벌 지식 구조 + 프로토콜 성숙화

> 분석 근거: auto_notes/analysis-*.md (7개 프로젝트, 65+ 세션 종합 분석)

## 배경

Mickey v7.4까지의 진화에서 발견된 3가지 구조적 Gap:
1. **프로젝트 간 지식 이전이 수동적** → 글로벌 지식 구조 도입
2. **프로토콜 유효성 검증이 정성적** → 포스트모템 자동 트리거
3. **자기 개선 비용 대비 효과 불투명** → 세션 메타데이터 + PURPOSE 연결

## 변경 요약

| 항목 | 변경 | 영향 범위 |
|------|------|----------|
| 글로벌 patterns/ | 접근법 패턴 라이브러리 신설 | T1.5, install.sh |
| 글로벌 domain/ | 도메인 지식 저장소 신설 | T1.5, install.sh |
| 세션-PURPOSE 연결 | SESSION.md에 Purpose Alignment 섹션 | T1 DOCUMENT SCHEMA |
| 포스트모템 자동 트리거 | 엔트로피 체크에 트리거 조건 추가 | T1.5 §9 |
| 세션 메타데이터 | SESSION.md에 Session Meta 섹션 | T1 DOCUMENT SCHEMA |
| install.sh 확장 | patterns/ + domain/ 배포 | install.sh |

---

## Phase 1: 글로벌 지식 구조 (patterns/ + domain/)

### 1-1. 디렉토리 생성 + 초기 파일

```
~/.kiro/mickey/
├── extended-protocols.md      # 기존 (T1.5)
├── patterns/                  # 신규: 접근법 패턴
│   └── INDEX.md               # 패턴 목록
└── domain/                    # 신규: 도메인 지식
    └── INDEX.md               # 트리거 → 파일 매핑
```

**patterns/INDEX.md 초기 내용** (기존 프로젝트 분석에서 추출):

| 패턴 | 요약 | 출처 |
|------|------|------|
| Phase 기반 점진적 분해 | 큰 목표를 Phase→Step으로 분해, 각 단계 E2E 검증 후 진행 | packet-capture, ai-agent |
| WELC (Test Harness) | 수정 전 기존 동작을 테스트로 캡처 → 수정 → 사이드이펙트 감지 | packet-capture M9 |
| 계획 문서 선행 | IMPROVEMENT-PLAN 수준의 구체적 계획 → 구현 세션에서 판단 비용 제거 | ai-developer-mickey M4→M5 |
| 외부 벤치마킹 → 선별 채택 | 외부 기술을 조사하되 자기 맥락에서 재해석하여 적용 | ai-developer-mickey M4, M7 |
| 검증 대상과 도구 동시 발전 | 테스트 대상과 도구를 함께 개선하여 검증 범위 확장 | packet-capture |

**domain/INDEX.md 초기 내용**: (빈 상태로 시작, 프로젝트에서 승격 시 추가)

| 트리거 | 파일 | 요약 |
|--------|------|------|
| (승격 시 추가) | — | — |

**CC**: 디렉토리 + INDEX 파일 존재, patterns/ 5개 패턴 기재

### 1-2. T1.5에 글로벌 지식 프로토콜 추가

extended-protocols.md에 §12 추가:

```markdown
## 12. Global Knowledge

### 구조
- patterns/: 도메인 무관 접근법 패턴 (상한 7개)
- domain/: 도메인 지식 (INDEX 트리거 기반 on-demand)

### 로딩
- 세션 시작 시: patterns/INDEX.md + domain/INDEX.md 로딩 (T1.5와 함께)
- 작업 중: INDEX 트리거 매칭 시 해당 파일 로딩
- 보조 검색 (선택적): /knowledge, grep, IDE 내장 검색 등 환경별 도구

### 승격 기준
- patterns/ 후보: "완전히 다른 도메인의 프로젝트에서도 이 접근법이 유효한가?"
- domain/ 후보: "다른 프로젝트에서 같은 기술/도구를 쓸 때 참고할 가치가 있는가?"
- 프로젝트 한정 지식은 프로젝트 common_knowledge/에 유지

### 크기 관리
- patterns/: 7개 상한. 초과 시 은퇴 (Graduated Patterns로 이동)
- domain/: 상한 없음. 6개월 미참조 시 아카이브 제안
```

**CC**: T1.5 §12 존재, 로딩/승격/크기 규칙 명시

### 1-3. T1 세션 프로토콜에 글로벌 지식 로딩 추가

Continuing Session 컨텍스트 로딩 목록에 추가:
```
1a. T1.5 로딩: ~/.kiro/mickey/ 존재 시 파일 로딩
    → patterns/INDEX.md, domain/INDEX.md도 함께 로딩
```

**CC**: T1 Continuing Session에 patterns/domain INDEX 로딩 명시

### 1-4. install.sh 확장

```bash
# 기존
cp "$SCRIPT_DIR/mickey/extended-protocols.md" "$MICKEY_DIR/"

# 추가
mkdir -p "$MICKEY_DIR/patterns" "$MICKEY_DIR/domain"
cp "$SCRIPT_DIR/mickey/patterns/"*.md "$MICKEY_DIR/patterns/" 2>/dev/null
cp "$SCRIPT_DIR/mickey/domain/"*.md "$MICKEY_DIR/domain/" 2>/dev/null
```

**CC**: install.sh 실행 시 patterns/ + domain/ 배포 확인

### 1-5. 리포지토리 구조 반영

```
mickey/
├── extended-protocols.md
├── patterns/
│   └── INDEX.md
└── domain/
    └── INDEX.md
```

**CC**: git push 완료

---

## Phase 2: 프로토콜 업데이트

### 2-1. 세션-PURPOSE 연결 (T1 DOCUMENT SCHEMA)

SESSION.md 스키마에 Purpose Alignment 섹션 추가:

```markdown
| **MICKEY-N-SESSION.md** | ...(기존)..., Purpose Alignment (기여 시나리오, 이번 세션 범위, 유지보수 세션은 "Infrastructure"로 분류) |
```

**CC**: DOCUMENT SCHEMA 테이블에 Purpose Alignment 포함

### 2-2. 세션 메타데이터 (T1 DOCUMENT SCHEMA)

SESSION.md 스키마에 Session Meta 섹션 추가:

```markdown
| **MICKEY-N-SESSION.md** | ...(기존)..., Session Meta (Type: Implementation/Self-Improvement/Maintenance/Planning) |
```

**CC**: DOCUMENT SCHEMA 테이블에 Session Meta 포함

### 2-3. 포스트모템 자동 트리거 (T1.5 §9)

기존 §9 포스트모템 프로토콜에 자동 트리거 조건 추가:

```markdown
### 자동 트리거 (엔트로피 체크 시 확인)
아래 조건 중 하나 충족 시 경량 포스트모템 제안:
- 프로젝트에서 10세션 이상 경과
- REMEMBER 또는 T1.5 변경 후 3개 프로젝트에서 사용

경량 포스트모템 = [Protocol] 태그 수집 + 긍정/부정 분류 + 1페이지 요약.
전체 포스트모템은 사용자 요청 시에만.
```

**CC**: T1.5 §9에 자동 트리거 조건 + 경량 포스트모템 정의 존재

### 2-4. 교훈 승격 경로 업데이트

기존 승격 경로에 글로벌 단계 추가:

```
프로젝트 auto_notes/ → context_rule/ → common_knowledge/ (프로젝트 내)
                                              ↓ (접근법)
                                        ~/.kiro/mickey/patterns/
                                              ↓ (도메인 지식)
                                        ~/.kiro/mickey/domain/
                                              ↓ (근본 원칙)
                                        REMEMBER 후보
```

**CC**: T1.5 교훈 승격 섹션에 글로벌 경로 명시

---

## Phase 3: 에이전트 동기화 + 설치

### 3-1. CLI 에이전트 JSON 업데이트 (v8)

T1 변경사항 반영:
- DOCUMENT SCHEMA: Purpose Alignment, Session Meta 추가
- Continuing Session: 글로벌 INDEX 로딩 추가
- 버전: v7.4 → v8

**CC**: agent JSON v8, install.sh 설치 완료

### 3-2. Power Mickey steering 동기화

해당 steering 파일에 변경사항 반영:
- session-protocol.md: 글로벌 INDEX 로딩, Purpose Alignment
- self-improvement.md: 글로벌 승격 경로, 포스트모템 자동 트리거

**CC**: Power steering 업데이트 + Windows 동기화

### 3-3. 문서 최신화

- README.md / README-en.md: 버전 테이블 v8 추가
- docs/07-changelog.md / 07-changelog-en.md: v8 항목 추가
- docs/06-prompt-evolution.md / 06-prompt-evolution-en.md: v8 반영

**CC**: git push 완료

---

## Phase 4: 실전 적용 + 검증

### 4-1. 기존 프로젝트에서 글로벌 승격 리뷰

대상: packet-capture, ai-agent-automation-platform의 common_knowledge/
- 접근법 패턴 → patterns/ 승격 후보 식별
- 도메인 지식 → domain/ 승격 후보 식별
- 사용자 확인 후 승격

**CC**: 최소 1건 이상 승격 완료

### 4-2. 새 프로젝트에서 글로벌 지식 활용 테스트

다음 새 프로젝트 시작 시:
- patterns/INDEX.md가 세션 시작 시 로딩되는지 확인
- 접근법 패턴이 실제 작업에 참조되는지 확인
- Purpose Alignment, Session Meta가 자연스럽게 기록되는지 확인

**CC**: 새 프로젝트 1개에서 글로벌 지식 참조 확인

---

## 실행 순서

| Phase | 예상 작업량 | 의존성 |
|-------|-----------|--------|
| Phase 1 | 1세션 | 없음 |
| Phase 2 | Phase 1과 동일 세션 가능 | Phase 1 완료 |
| Phase 3 | 1세션 | Phase 2 완료 |
| Phase 4 | 다음 실전 프로젝트에서 | Phase 3 완료 |

Phase 1+2는 한 세션에서 구현 가능. Phase 3도 같은 세션에서 가능하면 함께 진행.
Phase 4는 다음 실전 프로젝트에서 자연스럽게 검증.

---

**Version**: v8 계획
**Created**: 2026-03-26 (Mickey 12)
**Status**: 사용자 승인 대기
