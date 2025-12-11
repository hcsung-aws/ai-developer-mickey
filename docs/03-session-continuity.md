# 세션 연속성 (Session Continuity)

> [English Version](03-session-continuity-en.md)

## 문제 정의

생성형 AI 어시스턴트를 사용할 때 가장 큰 도전 과제 중 하나는 **세션 간 일관성 유지**입니다.

### 전형적인 시나리오

```
[세션 1 - 오전]
사용자: "Godot 엔진에 로깅 시스템을 추가해줘"
AI: 분석 → 설계 → 구현 시작
→ Context 70% 도달, 점심 시간

[세션 2 - 오후]
사용자: "이어서 진행해줘"
AI: "무엇을 이어서 진행할까요?" 
→ 이전 컨텍스트 없음, 처음부터 설명 필요
```

## Mickey의 해결 방법

### 1. 세션 로그 (Session Log)

각 Mickey는 세션 종료 시 상세한 로그를 남깁니다.

#### 세션 로그 구조

```markdown
# Mickey N Session Log
Date: 2025-11-29T01:07:41+09:00

## Session Goal
이번 세션의 명확한 목표

## Previous Context (Mickey N-1)
- 이전 세션에서 완료한 작업
- 중요한 결정 사항
- 미완료 작업

## Current Tasks
1. [ ] 작업 1
2. [x] 작업 2 (완료)
3. [ ] 작업 3 (진행 중)

## Progress
### 완료된 작업
- ✅ 기능 A 구현
- ✅ 테스트 B 작성

### 진행 중인 작업
- 🔄 기능 C 디버깅 (80% 완료)

### 대기 중인 작업
- ⏳ 문서 작성

## Key Decisions
### 결정 1: 접근 방식 선택
- 옵션 A: C++ 엔진 수정
- 옵션 B: GDScript 플러그인
- **선택**: 옵션 B (이유: 간단하고 충분함)

### 결정 2: 로그 형식
- **선택**: JSON Lines
- **이유**: 프레임별 파싱 용이

## Problems Encountered
### 문제 1: Delta 불일치
- **증상**: 에디터 ≠ Headless 결과
- **원인**: Delta 값 차이
- **해결**: 로그의 delta 사용

## Lessons Learned
1. Tolerance 조정은 임시방편
2. 근본 원인 찾기가 중요
3. 환경별 차이는 Delta 의심

## Files Modified
- `godot-demo-projects/2d/pong/replay_logger.gd` (신규)
- `godot-demo-projects/2d/pong/replay_controller.gd` (신규)
- `godot-demo-projects/2d/pong/logic/ball.gd` (수정)

## Next Steps
1. 리플레이 검증 시스템 구현
2. 배치 테스트 인프라 구축
3. CI/CD 통합

## Context Window
- Current: 65% (130,000 / 200,000 tokens)
- Status: Safe to continue
```

### 2. 세션 시작 프로토콜

새로운 Mickey가 시작할 때 따르는 절차:

#### Step 1: 이전 세션 로그 확인

```
Mickey 2 시작:
1. 디렉토리 스캔
2. MICKEY-1-SESSION.md 발견
3. 로그 읽기
4. 컨텍스트 복원
```

#### Step 2: 상태 선언

```
"Mickey 2로 시작하겠습니다."
"이전 세션(Mickey 1)에서 다음을 완료했습니다:"
- Godot 엔진 분석
- Pong 게임 로깅 시스템 추가
- 리플레이 기능 설계

"이번 세션에서는 리플레이 검증 시스템을 구현하겠습니다."
```

#### Step 3: 작업 이어가기

```
- 이전 결정 사항 참고
- 미완료 작업 우선 처리
- 새로운 작업 시작
```

### 3. 실제 전환 사례

#### Mickey 1 → Mickey 2

**Mickey 1의 마지막 작업**:
```
Context Window Usage: 61%

> 완료했습니다! 엔진 로그로 AI가 플레이어 조작을 따라할 수 있는지 
> 완전히 검증했습니다.

[세션 로그 저장]
- 엔진 분석 완료
- 로깅 시스템 설계 완료
- 다음: 자동 테스트 스크립트 구현
```

**Context Overflow 발생**:
```
The context window has overflowed, summarizing the history...
✔ Conversation history has been compacted successfully!
```

**Mickey 2 시작**:
```
> 이전 세션 내용을 검토하고 자동 테스트 스크립트 설계를 시작하겠습니다.

Reading: /home/hcsung/ai-develop-by-mickey/session_log.txt
Reading: /home/hcsung/ai-develop-by-mickey/godot-analysis/...

> 이전 세션 내용을 확인했습니다. Mickey 2로 시작하겠습니다.

## 자동 테스트 스크립트 설계 종합

이전 세션에서 구축한 내용을 바탕으로, 학습용 데이터 수집 + 
자동 테스트 시스템을 설계하겠습니다.
```

**핵심**: Compact로 유실된 정보를 세션 로그에서 복원!

## 세션 연속성의 핵심 원칙

### 1. 명확한 상태 전달

#### 나쁜 예
```markdown
## Progress
오늘 많은 작업을 했습니다. 여러 파일을 수정했고...
```

#### 좋은 예
```markdown
## Progress
- [x] replay_logger.gd 구현 (프레임별 상태 기록)
- [x] replay_controller.gd 구현 (재생 제어)
- [ ] state_validator.gd 구현 중 (50% 완료)
```

### 2. 결정 사항 문서화

모든 중요한 결정은 **이유와 함께** 기록:

```markdown
## Key Decisions

### GDScript vs C++ 엔진 수정
**선택**: GDScript
**이유**: 
- C++: 19배 작업량, 엔진 빌드 필요
- GDScript: 간단, 충분한 기능
- 유지보수 용이

### 로그 형식: JSON vs Binary
**선택**: JSON Lines
**이유**:
- 사람이 읽을 수 있음
- 프레임별 파싱 용이
- 디버깅 편리
```

### 3. 실패 경험 공유

실패도 중요한 학습 자료:

```markdown
## Problems Encountered

### 시도 1: Tolerance 증가
- **접근**: TOLERANCE = 250.0
- **결과**: 실패 (근본 원인 미해결)
- **교훈**: 임시방편은 문제를 숨길 뿐

### 시도 2: Delta 동기화
- **접근**: 로그의 delta 사용
- **결과**: 성공 (99.88% → 100%)
- **교훈**: 근본 원인 해결이 중요
```

### 4. 다음 단계 명시

다음 Mickey를 위한 명확한 가이드:

```markdown
## Next Steps

### 우선순위 1: 배치 테스트 인프라
- [ ] BatchTestRunner.gd 구현
- [ ] 여러 로그 파일 순차 실행
- [ ] 게임 상태 리셋 메커니즘

### 우선순위 2: CI/CD 통합
- [ ] GitHub Actions 워크플로우
- [ ] Headless 모드 테스트
- [ ] 자동 리포트 생성

### 우선순위 3: 문서화
- [ ] 사용자 가이드 작성
- [ ] API 문서 생성
```

## 세션 전환 체크리스트

### 세션 종료 시 (Current Mickey)

- [ ] 세션 로그 작성 완료
- [ ] 모든 결정 사항 문서화
- [ ] 수정된 파일 목록 기록
- [ ] 다음 단계 명시
- [ ] Context window 사용량 기록
- [ ] 파일 저장 확인

### 세션 시작 시 (Next Mickey)

- [ ] 이전 세션 로그 읽기
- [ ] Mickey 번호 확인 및 증가
- [ ] 상태 선언 ("Mickey N으로 시작")
- [ ] 이전 작업 요약
- [ ] 현재 목표 명시
- [ ] 작업 시작

## 측정 가능한 효과

### 세션 연속성 없이

```
세션 1: 0% → 60% 진행
세션 2: 0% → 40% 진행 (20% 중복)
세션 3: 0% → 50% 진행 (30% 중복)
→ 총 진행: 60% (많은 중복 작업)
```

### Mickey 사용

```
Mickey 1: 0% → 60% 진행
Mickey 2: 60% → 85% 진행 (중복 최소)
Mickey 3: 85% → 100% 진행
→ 총 진행: 100% (효율적)
```

## 실전 팁

### 1. 세션 로그는 즉시 작성

작업 완료 후 바로 작성하지 말고, **작업 중간중간** 업데이트:

```
작업 시작 → 로그 생성 (목표 명시)
↓
중간 완료 → 로그 업데이트 (진행 상황)
↓
문제 발생 → 로그 업데이트 (문제 기록)
↓
해결 → 로그 업데이트 (해결 방법)
↓
세션 종료 → 로그 최종 검토
```

### 2. 컨텍스트 규칙 활용

반복되는 정보는 context_rule/에 저장:

```markdown
# context_rule/project-context.md

## File Sync Pattern
- Edit in WSL: /home/.../pong/
- Copy to Windows: /mnt/c/.../pong/
- Godot opens: C:\...\pong\

## Common Commands
```bash
# Sync files
cp /home/.../pong/*.gd /mnt/c/.../pong/
```
```

### 3. 지식 베이스 구축

재사용 가능한 지식은 common_knowledge/에:

```markdown
# common_knowledge/godot/replay-system.md

## Replay System Design

### Core Concepts
1. Frame-by-frame recording
2. Delta synchronization
3. State validation

### Implementation Pattern
```gdscript
# Record
func _process(delta):
    logger.log_frame(frame, delta, state)

# Replay
func _process(delta):
    delta = log.get_delta(frame)  # Use logged delta
    state = log.get_state(frame)
```
```

## 다음 단계

- [Prompt 엔지니어링](04-prompt-engineering.md) - 효과적인 프롬프트 구조화
- [지식 관리 시스템](05-knowledge-management.md) - 재사용 가능한 지식 구축
- [실전 사례](case-study/godot-replay-system.md) - Godot 프로젝트 적용 사례
