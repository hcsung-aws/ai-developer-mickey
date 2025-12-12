# 지식 관리 시스템

> [English Version](05-knowledge-management-en.md)

## 왜 필요한가?

복잡한 프로젝트에서는 **재사용 가능한 지식**을 체계적으로 관리해야 합니다.

### 문제 상황

```
Mickey 1: Godot 씬 시스템 분석 → 이해
Mickey 2: (세션 재시작) → 다시 분석 필요
Mickey 3: (세션 재시작) → 또 다시 분석...
```

### 해결

```
Mickey 1: Godot 씬 시스템 분석 → common_knowledge/godot/scene-system.md 저장
Mickey 2: scene-system.md 읽기 → 즉시 이해
Mickey 3: scene-system.md 읽기 → 즉시 이해
```

## 디렉토리 구조

```
project-root/
├── common_knowledge/          # 재사용 가능한 지식
│   ├── INDEX.md              # 지식 인덱스 (필수)
│   ├── godot/
│   │   ├── overview.md       # Godot 개요
│   │   ├── scene-system.md   # 씬 시스템
│   │   └── input-system.md   # 입력 시스템
│   └── testing/
│       ├── overview.md       # 테스팅 개요
│       └── replay-system.md  # 리플레이 시스템
└── context_rule/             # 프로젝트별 규칙
    ├── project-context.md    # 환경 설정
    ├── troubleshooting.md    # 트러블슈팅
    └── mickey-improvements.md # 개선 사항
```

## common_knowledge vs context_rule

### common_knowledge/

**목적**: 재사용 가능한 일반 지식

**특징**:
- 프로젝트 독립적
- 다른 프로젝트에서도 활용 가능
- 기술/개념 설명

**예시**:
```markdown
# common_knowledge/godot/scene-system.md

## Godot Scene System

### Core Concepts
- Scene = Node Tree
- Parent-Child Hierarchy
- Signal-based Communication

### Example
```gdscript
# Create node hierarchy
var root = Node2D.new()
var child = Sprite2D.new()
root.add_child(child)
```
```

### context_rule/

**목적**: 프로젝트별 규칙과 제약사항

**특징**:
- 프로젝트 특화
- 환경 설정 정보
- 알려진 문제와 해결책

**예시**:
```markdown
# context_rule/project-context.md

## Development Environment
- OS: Windows + WSL
- Godot: Windows에서 실행
- 개발: WSL에서 수행
- **중요**: 파일 동기화 필수

## File Locations
- Windows: C:\Users\hcsung\work\q\ai-developer-mickey\pong\
- WSL: /home/hcsung/ai-develop-by-mickey/godot-demo-projects/2d/pong/

## Known Issues
- ❌ C++ 엔진 수정: 19배 작업량
- ✅ GDScript: 간단하고 충분
```

## INDEX.md 패턴

### 목적

- 모든 지식의 진입점
- Context window 최소 사용
- 필요한 문서만 선택적 로드

### 구조

```markdown
# Knowledge Index

## Quick Links
- [Godot Overview](godot/overview.md) - 엔진 구조 개요
- [Testing Overview](testing/overview.md) - 테스팅 전략

## Godot Engine
### Core Systems
- [Scene System](godot/scene-system.md) - 씬-노드 트리
- [Input System](godot/input-system.md) - 입력 처리
- [Collision System](godot/collision-system.md) - 충돌 감지

### Advanced Topics
- [Replay System](godot/replay-system.md) - 리플레이 구현
- [State Validation](godot/state-validation.md) - 상태 검증

## Testing
- [Replay Testing](testing/replay-testing.md) - 리플레이 기반 테스트
- [CI/CD Integration](testing/ci-cd.md) - 자동화 통합
```

### 사용 방법

```
Mickey: "Godot 입력 시스템 정보 필요"
1. INDEX.md 읽기 (작은 context)
2. "Input System" 찾기
3. godot/input-system.md만 로드
→ 효율적인 context 사용
```

## 문서 작성 원칙

### 1. 간결성 (Conciseness)

**나쁜 예**:
```markdown
Godot 엔진은 오픈소스 게임 엔진입니다. 
2014년에 처음 공개되었으며, MIT 라이선스를 사용합니다.
많은 개발자들이 사용하고 있으며...
(500 단어 계속)
```

**좋은 예**:
```markdown
## Godot Engine

### Key Features
- 오픈소스 (MIT License)
- 씬-노드 구조
- GDScript (Python-like)

### Core Concepts
1. Scene = Node Tree
2. Signals for Communication
3. Built-in Physics Engine
```

### 2. 구조화 (Structure)

**계층적 구성**:
```
개요 (Overview)
  ↓
핵심 개념 (Core Concepts)
  ↓
사용 예시 (Examples)
  ↓
상세 참조 (Detailed Reference)
```

### 3. 상호 참조 (Cross-Reference)

```markdown
## Scene System

씬은 노드 트리로 구성됩니다.

**관련 문서**:
- [Node System](node-system.md) - 노드 상세
- [Signal System](signal-system.md) - 통신 방법

**참고**:
입력 처리는 [Input System](input-system.md) 참조
```

## 실전 예시

### Godot 엔진 분석 사례

**문제**: 13,666개 파일의 거대한 코드베이스

**해결 과정**:

#### 1단계: 개요 작성

```markdown
# common_knowledge/godot/overview.md

## Godot Engine Structure

### Main Directories
- `core/`: 엔진 핵심
- `scene/`: 씬/노드 시스템
- `servers/`: 렌더링/물리 서버
- `modules/`: 확장 모듈

### Key Concepts
- Scene-Node Tree
- Signals
- GDScript

**상세 문서**:
- [Scene System](scene-system.md)
- [Input System](input-system.md)
```

#### 2단계: 필요한 부분만 상세화

```markdown
# common_knowledge/godot/input-system.md

## Input System

### Input Class
```gdscript
# Check if key pressed
if Input.is_action_pressed("move_up"):
    position.y -= speed * delta
```

### Custom Actions
Project Settings → Input Map에서 정의

### Replay Mode
```gdscript
# Override input
func get_action_strength(action: String) -> float:
    if replay_mode:
        return replay_data.get_input(action)
    return Input.get_action_strength(action)
```

#### 3단계: 활용

```
Mickey 3: "입력 시스템 정보 필요"
→ INDEX.md 확인
→ input-system.md 로드
→ 즉시 구현 가능
```

## 지식 업데이트 전략

### 언제 업데이트하나?

1. **새로운 개념 학습 시**
   ```
   Mickey: "Godot Signal 시스템 이해"
   → common_knowledge/godot/signal-system.md 생성
   ```

2. **문제 해결 후**
   ```
   Mickey: "Delta 동기화로 에러 해결"
   → common_knowledge/testing/replay-system.md 업데이트
   ```

3. **패턴 발견 시**
   ```
   Mickey: "리셋 프레임 감지 패턴 발견"
   → common_knowledge/testing/state-validation.md 추가
   ```

### 업데이트 방법

```markdown
## 기존 문서에 추가

### State Validation

#### Ball Reset Detection (Added: 2025-12-11)
```gdscript
func _is_ball_reset(expected: Vector2, actual: Vector2) -> bool:
    var diff = (expected - actual).length()
    return diff > 200.0  # Position jump > 200px
```

**Context**: Phase 1-1에서 발견
**Problem**: Ball reset 시 validation 실패
**Solution**: 큰 위치 점프 감지하여 스킵
```

## 측정 가능한 효과

### 지식 관리 없이

```
Mickey 1: Godot 분석 (2시간)
Mickey 2: Godot 재분석 (1.5시간)
Mickey 3: Godot 또 재분석 (1시간)
→ 총 4.5시간 (중복 작업)
```

### 지식 관리 사용

```
Mickey 1: Godot 분석 + 문서화 (2.5시간)
Mickey 2: 문서 읽기 (10분) + 작업
Mickey 3: 문서 읽기 (10분) + 작업
→ 총 2.5시간 + 작업 (효율적)
```

## 모범 사례

### DO ✅

1. **INDEX.md 먼저 작성**
   - 전체 구조 파악
   - 진입점 제공

2. **간결하게 작성**
   - 핵심만 담기
   - 예시 코드 포함

3. **상호 참조 추가**
   - 관련 문서 링크
   - 컨텍스트 제공

4. **정기적 업데이트**
   - 새로운 학습 즉시 반영
   - 오래된 정보 제거

### DON'T ❌

1. **모든 것을 한 파일에**
   - Context window 낭비
   - 검색 어려움

2. **장황한 설명**
   - 불필요한 배경 설명
   - 역사적 맥락 과다

3. **업데이트 미루기**
   - 정보 유실
   - 중복 학습

4. **구조 없이 작성**
   - 읽기 어려움
   - 활용 불가

## 다음 단계

- [실전 사례](case-study/godot-replay-system.md) - Godot 프로젝트 적용 사례
- [예시 파일](../examples/) - 실제 지식 관리 예시
