# Mickey v6.3 개선 계획: Auto Memory 패턴 도입

## 배경

Claude Code의 Auto Memory 기능 분석(Mickey 4)을 통해 6가지 개선 항목을 도출.
핵심 방향: **자동 기록 이원화 + 크기 관리 + 작업 비례 트리거 + 승격 경로 명시화 + 세션 전환 경량화**

## 개선 항목 요약

| # | 항목 | 핵심 변경 | 의존성 |
|---|------|----------|--------|
| 1 | 자동 메모리 기록 이원화 | auto_notes/ 디렉토리 도입, 세션 종료 시 일괄 확인 | 없음 |
| 2 | 인덱스 파일 크기 제한 | T2/T3a 파일별 줄 수 + 항목 수 이중 가드 | 없음 |
| 3 | 작업량 비례 업데이트 트리거 | "30분마다" 폐기 → 작업 단위 기반 트리거 | #1 |
| 4 | INDEX 경로 트리거 확장 | INDEX.md 트리거에 경로 패턴 허용 | 없음 |
| 5 | 교훈 승격 명령 | "교훈 승격" 키워드로 세션 중 승격 가능 | #1 |
| 6 | HANDOFF 경량화 | HANDOFF를 "요약 + Important Context + 참조"로 재정의 | #1, #3 |

## 구현 단계

### Phase 1: 시스템 프롬프트 v6.3 작성

**담당**: 다음 Mickey 세션
**산출물**: 시스템 프롬프트 v6.3 (3곳 동기화: 활성 agent JSON, repo JSON, 독립 md)

#### 1-1. KNOWLEDGE MANAGEMENT 섹션 변경

**auto_notes/ 추가 (항목 #1):**
```
### 자동 메모리 (auto_notes/)

"사용자가 작성하는 규칙"과 "AI가 기록하는 관찰 사실"을 분리:

| 저장소 | 성격 | 확인 | 로딩 |
|--------|------|------|------|
| auto_notes/ | 관찰한 사실 (서술적) | 세션 종료 시 일괄 확인 | T3a (NOTES.md) |
| context_rule/ | 검증된 규칙 (규범적) | 즉시 사용자 확인 | T3a→T3b |
| common_knowledge/ | 범용 패턴 (규범적) | 즉시 사용자 확인 | T3a→T3b |

auto_notes/ 구조:
- NOTES.md: 인덱스 (세션 시작 시 로딩)
- 토픽 파일: commands.md, file-roles.md, error-fixes.md 등

자동 기록 대상 (확인 불필요):
- 빌드/테스트/린트 커맨드
- 파일 경로와 역할
- 도구 버전, 환경 상세
- 검증 완료된 에러 해결법
- API 엔드포인트와 용도

크기 관리:
- NOTES.md가 줄 수 제한 초과 시 축약 또는 카테고리별 파일 분리
- 토픽 파일도 비대해지면 세분화
- NOTES.md는 항상 인덱스 역할만 유지
```

**파일 크기 제한 추가 (항목 #2):**
```
### 파일 크기 제한

세션 시작 시 로딩되는 파일은 줄 수 + 항목 수 이중 가드 준수:

| 파일 | 줄 수 제한 | 항목 수 제한 |
|------|-----------|-------------|
| T2 파일 (각각) | 50줄 (project-context만 80줄) | 핵심 섹션 최대 5개 항목 |
| T3a 인덱스 (각각) | 50줄 | — |
| auto_notes/NOTES.md | 50줄 | — |

초과 시 행동:
- 축약, 오래된 항목 승격/제거, 상세 내용 분리
- project-context.md Lessons Learned: 최대 5개, 오래된 것은 context_rule/로 승격
- INDEX.md: 유사 트리거 통합
- 파일 수정 시 줄 수 확인 → 초과 임박하면 즉시 정리
```

**INDEX 경로 트리거 확장 (항목 #4):**
```
T3 로딩 규칙에 추가:
- INDEX 트리거는 키워드 또는 경로 패턴 모두 가능 (예: `power-mickey/*` 파일 수정 시)
- 파일 수정/탐색 시 해당 경로가 INDEX 트리거에 매칭되면 T3b 로딩
```

**교훈 승격 추가 (항목 #5):**
```
### 교훈 승격

사용자가 "교훈 승격" 또는 "패턴 정리"를 요청하면:
1. auto_notes/, 현재 SESSION.md Lessons, 직전 HANDOFF.md 리뷰
2. 반복 패턴 → context_rule/, 범용 패턴 → common_knowledge/, 근본 원칙 → REMEMBER 후보로 분류
3. 항목별 승격 제안 (내용, 근거, 대상) → 사용자 확인
4. 승인 시 반영 + auto_notes/에서 제거 또는 "승격 완료" 표시
```

#### 1-2. SESSION PROTOCOL 섹션 변경

**Continuing Session 컨텍스트 로딩에 추가:**
```
- auto_notes/NOTES.md (T3a)
```

**During Session 변경 (항목 #3):**
```
현재:
- 주요 작업 완료/결정/문제 해결 시 세션 로그 업데이트
- 최소 30분마다 업데이트

변경:
- 세션 로그 업데이트 트리거 (아래 중 하나 발생 시):
  - TODO 항목 완료
  - 에러 조사→수정→검증 사이클 완료
  - 사용자와 의사결정 확정
  - 파일 3개 이상 수정
  - context_rule/ 또는 common_knowledge/ 변경
- auto_notes/: 기록 가능한 사실 발견 시 즉시 기록 (확인 불필요)
```

**Session End 변경 (항목 #1, #5, #6):**
```
현재:
1. 세션 로그 완료
2. HANDOFF 문서 생성
3. 교훈 분류 및 제안
4. 사용자 확인 후 적용

변경:
1. 세션 로그 최종 확인 (작업 단위 트리거로 이미 최신이므로 최소 작업)
2. auto_notes/ 변경 내역 일괄 제시 → 사용자 확인/수정/삭제
3. 교훈 승격 리뷰 (auto_notes/ + SESSION.md → context_rule/common_knowledge/REMEMBER 후보)
4. HANDOFF 경량 생성
5. 사용자 확인 후 적용
```

#### 1-3. DOCUMENT SCHEMA 변경

**HANDOFF 스키마 변경 (항목 #6):**
```
현재: Current Status, Immediate Next Steps, Important Context, Useful Commands, Context Window Usage

변경: Current Status (1~2줄 요약), Next Steps (1~2줄 요약), Important Context (SESSION.md/auto_notes에 없는 것만), Quick Reference (SESSION/auto_notes 경로 + context window 상태)
```

**auto_notes/NOTES.md 스키마 추가:**
```
| auto_notes/NOTES.md | Note Map (카테고리→파일→요약), Last Updated |
```

#### 1-4. REMEMBER 섹션 변경

**#6 수정 (항목 #1):**
```
현재: User confirmation BEFORE changes
변경: User confirmation BEFORE changes — 단, auto_notes/는 저위험 관찰 사실에 한해 자동 기록 (세션 종료 시 일괄 확인)
```

#### 1-5. 3-Tier Context Loading 테이블 변경

```
현재 T3a: common_knowledge/INDEX.md, context_rule/INDEX.md
변경 T3a: common_knowledge/INDEX.md, context_rule/INDEX.md, auto_notes/NOTES.md
```

### Phase 2: 디렉토리 구조 + 문서 초기화

**담당**: Phase 1과 같은 세션 또는 다음 세션
**산출물**: auto_notes/ 디렉토리 + 초기 파일

```bash
mkdir -p auto_notes
```

**auto_notes/NOTES.md 초기 내용:**
```markdown
# Auto Notes INDEX

## Note Map

| 카테고리 | 파일 | 요약 |
|----------|------|------|
| (아직 없음) | — | — |

## Last Updated
(날짜)
```

**기존 파일 크기 점검:**
- project-context.md, INDEX.md 등 현재 줄 수 확인
- 제한 초과 항목이 있으면 즉시 정리

### Phase 3: 실전 테스트 + 반복 개선

**담당**: Phase 2 이후 세션
**목표**: 새 시스템으로 실제 작업 수행하며 검증

**검증 항목:**

| 항목 | 검증 방법 | 성공 기준 |
|------|----------|----------|
| auto_notes/ 자동 기록 | 작업 중 사실 발견 시 기록되는지 | 세션 종료 시 auto_notes/에 기록 존재 |
| 일괄 확인 | 세션 종료 시 변경 내역 제시되는지 | 사용자가 한 번에 확인/수정 가능 |
| 크기 제한 | 파일 수정 시 줄 수 확인하는지 | 제한 초과 파일 없음 |
| 작업 단위 트리거 | TODO 완료 등 시 SESSION.md 업데이트되는지 | 세션 종료 시 SESSION.md가 이미 최신 |
| 경로 트리거 | INDEX에 경로 패턴 사용 가능한지 | 경로 매칭 시 T3b 로딩 |
| 교훈 승격 | "교훈 승격" 키워드 시 프로세스 실행되는지 | 승격 제안 목록 제시 |
| HANDOFF 경량화 | HANDOFF 생성이 빠르고 간결한지 | Important Context + 요약 + 참조만 포함 |

**반복 개선:**
- 테스트 세션에서 발견된 문제 → 프롬프트 조정
- 불필요한 복잡도 발견 시 단순화
- 효과 미미한 항목은 제거 검토

## 버전 정보

- 현재: v6.2 (PURPOSE-SCENARIO 기반 목적 관리)
- 목표: v6.3 (Auto Memory 패턴 도입)
- 분석: Mickey 4 (2026-02-28)
- 구현 시작: Mickey 5 예정

## 참고 자료

- [Anthropic 공식 문서: Manage Claude's memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Claude Code Session Memory 분석](https://claudefa.st/blog/guide/mechanics/session-memory)
- [Claude Code Auto Memory 실험적 기능 분석](https://giuseppegurgone.com/claude-memory)
- [The Decoder: Claude Code auto memory 발표](https://the-decoder.com/claude-code-now-remembers-your-fixes-your-preferences-and-your-project-quirks-on-its-own/)
