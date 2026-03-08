# Context Window 관리

> [English Version](02-context-management-en.md)

## Context Window란?

Context Window는 AI 모델이 한 번에 처리할 수 있는 텍스트의 양입니다. Kiro CLI의 경우 200,000 토큰의 context window를 제공하지만, 복잡한 프로젝트에서는 이마저도 부족할 수 있습니다.

## 문제 상황

### 전형적인 실패 시나리오

```
1. 복잡한 코드베이스 분석 시작
2. 여러 파일 읽기 → Context 50% 사용
3. 추가 분석 및 코드 작성 → Context 70% 사용
4. 더 많은 정보 필요 → Context 90% 사용
5. Context overflow → 세션 요약 (Compact)
6. 중요한 컨텍스트 유실 → 작업 실패
```

### Mickey 없이 세션 재시작 시

```
[이전 세션]                          [Compact 후]
- 상세한 분석 결과                    - "Godot 엔진 분석 중"
- 설계 결정 사항                      - "로깅 시스템 구현 필요"
- 시도한 접근 방식                    → 구체적인 컨텍스트 대부분 유실
- 실패한 이유
```

핵심 문제: **"모든 정보를 context에 넣으면 정작 필요한 정보를 놓친다."**

## Mickey의 해결: 3-Tier Context Loading

### 왜 (WHY)

Context window는 유한합니다. 모든 정보를 한 번에 넣으면 중요한 정보가 묻히고, 세션 후반에 공간이 부족해집니다. **"지도를 주되, 백과사전을 주지 마라"** — 필요한 것만 필요한 때에 로딩해야 합니다.

### 무엇을 (WHAT)

정보를 중요도와 로딩 시점에 따라 계층적으로 분류합니다:

| Tier | 로딩 시점 | 내용 | 예시 |
|------|----------|------|------|
| **T1** | 항상 | 핵심 정체성, 범용 원칙 | 시스템 프롬프트 |
| **T1.5** | 세션 시작 | 상세 실행 지침 | `~/.kiro/mickey/extended-protocols.md` |
| **T2** | 세션 시작 | 프로젝트 핵심 문서 | PURPOSE-SCENARIO, HANDOFF, adaptive.md |
| **T3a** | 세션 시작 | 지식 지도 (INDEX) | `common_knowledge/INDEX.md` |
| **T3b** | 필요할 때만 | 상세 지식 | INDEX에서 트리거 매칭된 파일 |

### 어떻게 (HOW)

```
세션 시작
  ├─ T1: 시스템 프롬프트 (항상 로딩)
  ├─ T1.5: ~/.kiro/mickey/ (존재 시 로딩)
  ├─ T2: PURPOSE-SCENARIO → HANDOFF → PROJECT-OVERVIEW → adaptive.md
  ├─ T3a: INDEX 파일들 로딩 (지식 지도만)
  │
  └─ 작업 중...
       └─ "에러 해결" 키워드 발생 → INDEX 트리거 매칭
            └─ T3b: auto_notes/error-fixes.md 로딩 (해당 파일만)
```

**핵심**: T3a(INDEX)는 "어떤 지식이 있는지"만 알려주는 지도입니다. 실제 상세 내용(T3b)은 작업 중 필요할 때만 로딩합니다.

## INDEX 패턴: 트리거 기반 지식 지도

### 왜 (WHY)

지식 파일이 늘어나면 "어떤 파일에 뭐가 있는지" 파악하는 것 자체가 context를 소모합니다. INDEX는 이 문제를 해결하는 목차입니다.

### 무엇을 (WHAT)

INDEX는 **트리거 → 파일 → 요약** 형태의 매핑 테이블입니다:

```markdown
# Common Knowledge INDEX

## Knowledge Map

| 트리거 | 파일 | 요약 |
|--------|------|------|
| INDEX 설계, 지식 지도 | progressive-disclosure.md | INDEX=목차 패턴 원칙 |
| 에이전트 설계, context window | agent-design-patterns.md | 스크립트 위임, 이벤트 기반 트리거 |
```

### 어떻게 (HOW)

1. 세션 시작 시 INDEX만 로딩 (수십 줄)
2. 작업 중 키워드/경로가 트리거에 매칭되면 해당 파일만 로딩
3. INDEX에 없는 파일은 로딩하지 않음 (INDEX 업데이트 우선)

트리거는 키워드뿐 아니라 **경로 패턴**도 가능합니다:
- `power-mickey/*` 파일 수정 시 → `kiro-powers.md` 로딩
- `에러`, `error` 키워드 → `error-fixes.md` 로딩

Mickey는 3개의 INDEX를 관리합니다:

| INDEX | 위치 | 용도 |
|-------|------|------|
| `context_rule/INDEX.md` | 프로젝트 규칙 | 반복 실패 방지, 환경 설정, 알려진 이슈 |
| `common_knowledge/INDEX.md` | 범용 패턴 | 프로젝트 무관 재사용 패턴 |
| `auto_notes/NOTES.md` | 관찰 기록 | AI가 자동 기록한 사실 |

## 자동 메모리: auto_notes + adaptive.md

### 왜 (WHY)

"사용자가 작성하는 규칙"과 "AI가 관찰한 사실"은 성격이 다릅니다. 이를 분리하면 각각의 신뢰도와 관리 방식을 다르게 할 수 있습니다.

### 무엇을 (WHAT)

| 저장소 | 성격 | 확인 시점 | 예시 |
|--------|------|----------|------|
| `auto_notes/` | 관찰한 사실 (서술적) | 세션 종료 시 일괄 | 빌드 명령, 파일 역할, 에러 해결법 |
| `context_rule/adaptive.md` | AI 자가 생성 규칙 (적응형) | 세션 종료 시 일괄 | "이 프로젝트에서는 테스트 전 lint 먼저" |
| `context_rule/` | 검증된 규칙 (규범적) | 즉시 사용자 확인 | 반복 실패 방지, 환경 제약 |
| `common_knowledge/` | 범용 패턴 (규범적) | 즉시 사용자 확인 | 아키텍처 패턴, 기술 비교 |

### 어떻게 (HOW)

**auto_notes/** — 작업 중 발견한 사실을 즉시 기록 (사용자 확인 불필요):
```
auto_notes/
├── NOTES.md          # 인덱스 (T3a로 세션 시작 시 로딩)
├── commands.md       # 빌드/테스트/린트 커맨드
├── file-roles.md     # 파일 경로와 역할
└── error-fixes.md    # 검증 완료된 에러 해결법
```

**adaptive.md** — Mickey가 스스로 학습한 행동 규칙:
```markdown
# Adaptive Rules
- 이 프로젝트에서 README 수정 시 한글/영문 동시 수정 필요
- install.sh 변경 시 3곳 동기화 확인 (agent JSON, repo, ~/.kiro/)
```

세션 종료 시 auto_notes와 adaptive.md 변경 내역을 일괄 제시하여 사용자가 확인/수정/삭제할 수 있습니다.

**교훈 승격 경로**: 반복되는 패턴은 더 높은 계층으로 승격됩니다:
```
auto_notes → context_rule → common_knowledge → 시스템 프롬프트 (REMEMBER)
```

## 파일 크기 제한

### 왜 (WHY)

세션 시작 시 로딩되는 파일이 비대해지면 3-Tier의 의미가 없어집니다. 각 파일에 크기 가드를 두어 context 효율을 유지합니다.

### 제한 기준

| 파일 | 줄 수 제한 | 항목 수 제한 |
|------|-----------|-------------|
| T2 파일 (각각) | 50줄 | 핵심 섹션 최대 5개 항목 |
| project-context.md | 80줄 | Lessons Learned 최대 5개 |
| T3a 인덱스 (각각) | 50줄 | — |
| auto_notes/NOTES.md | 50줄 | — |

### 초과 시 행동

- 축약, 오래된 항목 승격/제거, 상세 내용 분리
- Lessons Learned 5개 초과 → 오래된 것은 `context_rule/`로 승격
- INDEX 트리거 유사 항목 → 통합
- 파일 수정 시 줄 수 확인 → 초과 임박하면 즉시 정리

## Context Window 모니터링

Mickey는 context window 사용량에 따라 행동을 조절합니다:

| 사용률 | 행동 |
|--------|------|
| **50%** | 세션 로그 정리 제안 (완료 작업 요약, 시행착오 제거) |
| **70%** | 현재 작업 완료 후 새 세션 권장, 핸드오프 준비 |
| **90%** | 즉시 새 세션, 핸드오프 생성 |

### Mickey 없이 vs Mickey 사용

```
[Mickey 없이]                        [Mickey 사용]
세션 1: 100% → Compact → 정보 유실    Mickey 1: 70% → 세션 로그 저장
세션 2: 처음부터 다시 시작              Mickey 2: 이전 작업 이어가기 → 50%
세션 3: 또 다시 Compact...             Mickey 3: 추가 작업 → 65%
→ 반복 작업, 느린 진행                  → 누적 학습, 빠른 진행
```

## 실전 적용 사례

### Godot 엔진 분석 (13,666개 파일)

**문제**: 거대한 코드베이스를 context에 넣을 수 없음

**해결** (3-Tier 적용):
1. 개요 파악 → `common_knowledge/godot/overview.md` 작성 (Context 5%)
2. INDEX에 트리거 등록 → 필요한 주제만 선택적 로딩 (각 2-3%)
3. 전체 엔진을 context에 넣지 않고도 작업 완료

**인사이트**: "모든 것을 알 필요 없다. 어디에 뭐가 있는지만 알면 된다."

### Mickey 자체 개선 (v2 → v7.2)

**문제**: 프롬프트가 복잡해질수록 세션 시작 시 로딩량 증가

**해결**:
- v6.0: 도메인 특화 내용 제거, 3-Tier 도입 → 시스템 프롬프트 경량화
- v6.1: INDEX 지도 패턴 → T3b 선택적 로딩
- v6.3: auto_notes 분리 → 관찰 사실과 규칙 분리
- v7.2: adaptive.md → AI 자가 학습 규칙 분리

**인사이트**: "정보를 추가하는 것보다 분류하는 것이 더 중요하다."

## 모범 사례

### DO ✅

1. **계층적 로딩**: INDEX 먼저, 상세는 필요할 때만
2. **간결한 기록**: 핵심 정보만, 불릿 포인트 활용
3. **크기 가드 준수**: 파일 수정 시 줄 수 확인
4. **정기적 정리**: 50% 도달 시 세션 로그 정리

### DON'T ❌

1. **모든 파일을 한 번에 로드**: Context 낭비, 중요 정보 매몰
2. **장황한 세션 로그**: 에세이 대신 결과/결정/이슈만
3. **90% 넘어서까지 작업**: Compact 후 정보 유실 위험
4. **INDEX 없이 지식 파일 추가**: 로딩되지 않는 고아 파일 발생

## 다음 단계

- [세션 연속성](03-session-continuity.md) - 세션 프로토콜과 목적 관리
- [지식 관리 시스템](05-knowledge-management.md) - 자동 메모리와 교훈 승격
- [실전 사례](case-study/godot-replay-system.md) - Godot 리플레이 시스템 적용 사례
