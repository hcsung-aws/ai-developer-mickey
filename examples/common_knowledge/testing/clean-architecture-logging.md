# 클린 아키텍처 - 게임 로깅 시스템

## 레이어 구조

### Layer 4: UI/Configuration
- **파일**: `scripts/config/game_logger.gd`
- **역할**: 프로젝트 통합, 설정
- **의존**: Layer 3, 2

### Layer 3: Application Logic
- **파일**: `scripts/application/game_state_collector.gd`
- **역할**: 게임 상태 수집, 이벤트 필터링
- **의존**: Layer 2

### Layer 2: Core Logic
- **파일**: `scripts/core/game_logger_core.gd`
- **역할**: 파일 I/O, JSON 직렬화, 버퍼링
- **의존**: Layer 1 (Godot Core)

## 5분 통합

```gdscript
var logger := GameLogger.new()
var collector := MyGameCollector.new()

func _ready():
    add_child(logger)
    add_child(collector)
    collector.state_collected.connect(logger.log_frame)
    logger.start_recording()
```

## 장점

- **관심사 분리**: 각 레이어 독립적
- **재사용성**: Core/Application 레이어 범용
- **테스트 용이**: 레이어별 단위 테스트
- **유지보수**: 변경 영향 최소화

## 관련 문서
- 구현: `scripts/ARCHITECTURE.md`
- 예시: `scripts/config/pong_logger_integration.gd`
