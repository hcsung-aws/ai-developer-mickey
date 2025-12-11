# Context Window 관리

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
[이전 세션]
- 상세한 분석 결과
- 설계 결정 사항
- 시도한 접근 방식
- 실패한 이유

[Compact 후]
- "Godot 엔진 분석 중"
- "로깅 시스템 구현 필요"
→ 구체적인 컨텍스트 대부분 유실
```

## Mickey의 해결 방법

### 1. 지식 추상화 (Knowledge Abstraction)

**원칙**: 모든 정보를 context에 넣지 말고, 필요한 것만 선택적으로 로드

#### 계층적 문서 구조

```
common_knowledge/
├── INDEX.md                    # 최상위 인덱스 (항상 로드)
├── godot/
│   ├── overview.md            # 개요 (필요시 로드)
│   ├── scene-system.md        # 상세 (필요시 로드)
│   └── collision-system.md    # 상세 (필요시 로드)
└── testing/
    ├── overview.md
    └── replay-system.md
```

#### INDEX.md 예시

```markdown
# Knowledge Index

## Godot Engine
- [Overview](godot/overview.md) - 엔진 구조 개요
- [Scene System](godot/scene-system.md) - 씬-노드 트리 구조
- [Collision System](godot/collision-system.md) - 충돌 감지 시스템

## Testing
- [Overview](testing/overview.md) - 테스팅 전략
- [Replay System](testing/replay-system.md) - 리플레이 시스템 설계
```

**사용 방법**:
1. INDEX.md만 먼저 로드 (작은 context 사용)
2. 필요한 주제 파악
3. 해당 문서만 선택적으로 로드

### 2. Context Rules (컨텍스트 규칙)

**원칙**: 반복되는 실패나 불가능한 작업을 문서화하여 시간 낭비 방지

#### context_rule/project-context.md

```markdown
# Project Context

## Environment
- OS: Windows + WSL
- Godot: Running on Windows
- Development: WSL
- File Sync: WSL → Windows 필수

## Known Issues
- ❌ C++ 엔진 수정: 19배 작업량, 최소 이득
- ✅ GDScript 접근: 간단하고 충분함

## File Locations
- Windows Project: C:\Users\...\pong\
- WSL Project: /home/.../godot-demo-projects/2d/pong/
- Logs: C:\Users\...\AppData\Roaming\Godot\...
```

**효과**:
- 이미 시도한 접근 방식 반복 방지
- 환경 설정 정보 빠른 참조
- 알려진 제약사항 명확히 인지

### 3. 세션 로그 압축

**원칙**: 세션 로그는 핵심 정보만 간결하게 기록

#### 나쁜 예 (장황함)

```markdown
## Progress
오늘 작업을 시작하면서 먼저 Godot 엔진의 구조를 분석했습니다. 
엔진은 매우 복잡했고 여러 파일을 읽어야 했습니다. 
처음에는 C++로 접근하려 했으나 너무 복잡해서...
(500 단어 계속)
```

#### 좋은 예 (간결함)

```markdown
## Progress
- [x] Godot 엔진 구조 분석 완료
- [x] C++ 접근 검토 → GDScript 선택 (19배 효율)
- [x] Pong 게임 로깅 시스템 추가
- [ ] 리플레이 시스템 구현 중

## Key Decisions
- GDScript > C++: 간단하고 충분함
- 로그 형식: JSON Lines (프레임별 상태)
```

### 4. Context Window 모니터링

Mickey는 항상 context window 사용량을 추적합니다:

```
Context Window Usage: 52% (104,000 / 200,000 tokens)
→ 안전 범위

Context Window Usage: 70% (140,000 / 200,000 tokens)
→ 정리 권장

Context Window Usage: 85% (170,000 / 200,000 tokens)
→ 세션 재시작 필수
```

**임계값**:
- **< 70%**: 정상 작업
- **70-85%**: 정리 시작 (불필요한 정보 제거)
- **> 85%**: 세션 로그 저장 후 재시작

## 실전 적용 사례

### Godot 엔진 분석

**문제**: Godot 엔진은 13,666개 파일로 구성된 거대한 코드베이스

**해결**:

1. **1단계: 개요 파악**
   ```
   - README.md 읽기
   - 디렉토리 구조 파악
   - 핵심 모듈 식별
   → Context 사용: 5%
   ```

2. **2단계: 지식 구조화**
   ```
   - common_knowledge/godot/overview.md 작성
   - 핵심 개념만 추출 (씬, 노드, 시그널)
   - 상세 내용은 별도 문서로 분리
   → Context 사용: 추가 3%
   ```

3. **3단계: 필요시 상세 로드**
   ```
   - 충돌 시스템 필요 → collision-system.md 로드
   - 입력 시스템 필요 → input-system.md 로드
   → Context 사용: 각 2-3%
   ```

**결과**: 전체 엔진을 context에 넣지 않고도 필요한 작업 완료

### 리플레이 시스템 개발

**문제**: 복잡한 설계 결정과 여러 시도가 필요한 작업

**해결**:

1. **설계 결정 기록**
   ```markdown
   ## Key Decisions (Mickey 3)
   - Input Replay vs State Replay
     → State Replay 선택 (100% 정확도)
   - Delta 동기화 필수
     → 로그의 delta 사용
   ```

2. **실패 경험 공유**
   ```markdown
   ## Lessons Learned (Mickey 4)
   - ❌ Tolerance 조정: 임시방편, 근본 해결 아님
   - ✅ Delta 동기화: 근본 원인 해결
   - ✅ Direction 로그 사용: Collision 에러 해결
   ```

3. **다음 Mickey 활용**
   ```
   Mickey 5 시작 시:
   - 이전 결정 사항 참고
   - 실패한 접근 회피
   - 검증된 방법 적용
   ```

## 모범 사례

### DO ✅

1. **계층적 문서 구조 사용**
   - 개요 → 상세 순서
   - 필요한 것만 로드

2. **간결한 세션 로그**
   - 핵심 정보만 기록
   - 불릿 포인트 활용

3. **Context Rules 활용**
   - 반복 실패 문서화
   - 환경 정보 명시

4. **정기적 모니터링**
   - Context 사용량 추적
   - 70% 도달 시 정리

### DON'T ❌

1. **모든 파일을 한 번에 로드**
   - Context 낭비
   - 불필요한 정보 과다

2. **장황한 설명**
   - 세션 로그에 에세이 작성
   - 중복 정보 반복

3. **Context 무시**
   - 90% 넘어서까지 작업
   - Compact 후 재시작 (정보 유실)

4. **구조화 없이 저장**
   - 모든 정보를 한 파일에
   - 검색 불가능한 형태

## 측정 가능한 효과

### Mickey 없이

```
세션 1: Context 100% → Compact → 정보 유실
세션 2: 처음부터 다시 시작
세션 3: 또 다시 Compact...
→ 진행 속도: 느림, 반복 작업 많음
```

### Mickey 사용

```
Mickey 1: Context 70% → 세션 로그 저장
Mickey 2: 이전 작업 이어가기 → Context 50%
Mickey 3: 추가 작업 → Context 65%
→ 진행 속도: 빠름, 누적 학습
```

## 다음 단계

- [세션 연속성](03-session-continuity.md) - 세션 간 일관성 유지 방법
- [지식 관리 시스템](05-knowledge-management.md) - 재사용 가능한 지식 구축
- [실전 사례](case-study/godot-replay-system.md) - 실제 적용 사례
