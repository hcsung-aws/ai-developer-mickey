# 지식 관리 시스템

> [English Version](05-knowledge-management-en.md)

## 왜 필요한가?

```
Mickey 1: Godot 씬 시스템 분석 → 이해 (2시간)
Mickey 2: (세션 재시작) → 다시 분석 (1.5시간)
Mickey 3: (세션 재시작) → 또 다시 분석 (1시간)
→ 4.5시간 중복 작업
```

지식을 파일로 저장하면:

```
Mickey 1: 분석 + 문서화 (2.5시간)
Mickey 2: 문서 읽기 (10분) → 즉시 작업
Mickey 3: 문서 읽기 (10분) → 즉시 작업
→ 중복 제거, 누적 학습
```

하지만 지식이 늘어나면 새로운 문제가 생깁니다: **"어떤 지식을 언제 로딩할 것인가?"**, **"사용자가 작성한 규칙과 AI가 관찰한 사실을 어떻게 구분할 것인가?"**

## 4개 저장소 체계

### 왜 (WHY)

모든 지식을 한 곳에 넣으면 신뢰도와 관리 방식이 뒤섞입니다. 성격에 따라 분리하면 각각의 확인 절차와 로딩 시점을 다르게 할 수 있습니다.

### 무엇을 (WHAT)

| 저장소 | 성격 | 확인 시점 | 예시 |
|--------|------|----------|------|
| **auto_notes/** | AI가 관찰한 사실 (서술적) | 세션 종료 시 일괄 | 빌드 명령, 파일 역할, 에러 해결법 |
| **context_rule/adaptive.md** | AI 자가 생성 규칙 (적응형) | 세션 종료 시 일괄 | "README 수정 시 한글/영문 동시" |
| **context_rule/** | 검증된 프로젝트 규칙 (규범적) | 즉시 사용자 확인 | 반복 실패 방지, 환경 제약, 알려진 이슈 |
| **common_knowledge/** | 범용 재사용 패턴 (규범적) | 즉시 사용자 확인 | 아키텍처 패턴, 기술 비교, 구현 패턴 |

### 어떻게 (HOW)

```
project-root/
├── auto_notes/                  # AI 자동 관찰 기록
│   ├── NOTES.md                # 인덱스 (T3a)
│   ├── commands.md             # 빌드/테스트/린트 커맨드
│   ├── file-roles.md           # 파일 경로와 역할
│   └── error-fixes.md          # 검증 완료된 에러 해결법
├── context_rule/                # 프로젝트 특화 규칙
│   ├── INDEX.md                # 규칙 지도 (T3a)
│   ├── project-context.md      # 환경/목표/제약/교훈
│   └── adaptive.md             # AI 자가 생성 규칙 (T2)
└── common_knowledge/            # 범용 재사용 패턴
    ├── INDEX.md                # 지식 지도 (T3a)
    └── agent-design-patterns.md # 에이전트 설계 패턴
```

**context_rule/ vs common_knowledge/ 구분 기준**:
- 다른 프로젝트에서도 쓸 수 있는가? → `common_knowledge/`
- 이 프로젝트에서만 의미 있는가? → `context_rule/`

## 자동 메모리: auto_notes + adaptive.md

### 왜 (WHY)

매번 "이것 기록해"라고 지시하는 것은 비효율적입니다. AI가 작업 중 발견한 사실을 자동으로 기록하되, **검증된 규칙과 분리**하면 신뢰도를 관리할 수 있습니다.

### auto_notes/ — 관찰한 사실

자동 기록 대상 (사용자 확인 불필요):
- 빌드/테스트/린트 커맨드
- 파일 경로와 역할
- 도구 버전, 환경 상세
- 검증 완료된 에러 해결법
- API 엔드포인트와 용도

```markdown
# auto_notes/commands.md

## Build
- `npm run build` — 프로덕션 빌드
- `npm run dev` — 개발 서버 (port 3000)

## Test
- `npm test` — 전체 테스트
- `npm test -- --watch` — 변경 감지 모드
```

크기 관리:
- `NOTES.md`가 50줄 초과 시 카테고리별 파일 분리
- 토픽 파일도 비대해지면 세분화
- `NOTES.md`는 항상 인덱스 역할만 유지

### adaptive.md — AI 자가 생성 규칙

Mickey가 작업 중 스스로 학습한 행동 규칙:

```markdown
# Adaptive Rules

## 이 프로젝트에서 학습한 규칙
- README 수정 시 한글/영문 동시 수정 필요
- install.sh 변경 시 3곳 동기화 확인 (agent JSON, repo, ~/.kiro/)
- 시스템 프롬프트 변경 시 examples/ 폴더도 업데이트
```

auto_notes와의 차이: auto_notes는 **사실** ("빌드 명령은 npm run build"), adaptive.md는 **규칙** ("README 수정 시 한글/영문 동시 수정").

세션 종료 시 auto_notes와 adaptive.md 변경 내역을 **일괄 제시**하여 사용자가 확인/수정/삭제합니다.

## 교훈 승격 경로

### 왜 (WHY)

auto_notes의 관찰 사실 중 반복되는 패턴은 더 높은 계층으로 올려야 합니다. 그래야 다음 세션에서 더 빠르게, 더 확실하게 참조됩니다.

### 무엇을 (WHAT)

```
auto_notes (관찰) → context_rule (프로젝트 규칙) → common_knowledge (범용 패턴) → REMEMBER (핵심 원칙)
```

| 승격 조건 | 대상 |
|----------|------|
| 같은 실수 2번 이상 반복 | → context_rule/ |
| 프로젝트 무관 재사용 패턴 발견 | → common_knowledge/ |
| 근본 원칙 수준의 교훈 | → REMEMBER (시스템 프롬프트) |

### 어떻게 (HOW)

사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면:

1. auto_notes/, SESSION.md Lessons, HANDOFF.md 리뷰
2. 항목별 분류: context_rule / common_knowledge / REMEMBER 후보
3. 승격 제안 (내용, 근거, 대상) → 사용자 확인
4. 승인 시 반영 + auto_notes에서 "승격 완료" 표시

**실전 사례**: Mickey 9에서 MICKEY-1~5의 교훈 14건을 분석하여 3건을 `common_knowledge/agent-design-patterns.md`로 승격했습니다.

## 문서 작성 원칙

### 간결성

```
❌ "Godot 엔진은 오픈소스 게임 엔진입니다. 2014년에 처음 공개되었으며..." (500단어)
✅ "## Godot Engine
    - 오픈소스 (MIT), 씬-노드 구조, GDScript (Python-like)"
```

### 구조화

```
개요 → 핵심 개념 → 사용 예시 → 상세 참조
```

### 상호 참조

```markdown
**관련 문서**: [Node System](node-system.md), [Signal System](signal-system.md)
```

## 실전 적용 사례

### Godot 엔진 분석 (13,666개 파일)

1. `common_knowledge/godot/overview.md` — 엔진 구조 개요 (Context 5%)
2. INDEX에 트리거 등록 — 필요한 주제만 선택적 로딩
3. 세션 거듭할수록 지식 축적 → 분석 시간 2시간 → 10분

**인사이트**: "한 번 분석한 것을 다시 분석하지 않는다."

### Mickey 자체 개선 (교훈 승격)

```
Mickey 1~5: auto_notes에 관찰 사실 축적
Mickey 9: 14건 분석 → 3건 common_knowledge 승격
  - 스크립트 위임 패턴
  - 이벤트 기반 트리거
  - 계획 구체성→실행 속도 상관관계
```

**인사이트**: "관찰 → 패턴 발견 → 규칙화 → 원칙화. 지식은 계층을 올라간다."

## 모범 사례

### DO ✅

1. **INDEX 먼저 작성**: 지식의 진입점 제공
2. **간결하게**: 핵심만, 예시 코드 포함
3. **성격별 분리**: 사실(auto_notes) / 규칙(context_rule) / 패턴(common_knowledge)
4. **정기적 승격**: 반복 패턴은 상위 계층으로

### DON'T ❌

1. **모든 것을 한 파일에**: Context window 낭비, 검색 어려움
2. **INDEX 없이 파일 추가**: 로딩되지 않는 고아 파일 발생
3. **승격 미루기**: auto_notes가 비대해지고 패턴이 묻힘
4. **사실과 규칙 혼재**: 신뢰도 관리 불가

## 다음 단계

- [프롬프트 진화](06-prompt-evolution.md) - v2.0 → v7.2 진화 과정
- [진화 인사이트](08-evolution-insight.md) - "AI를 잘 쓰는 법"이 어떻게 진화해 왔는가
- [실전 사례](case-study/godot-replay-system.md) - Godot 프로젝트 적용 사례
