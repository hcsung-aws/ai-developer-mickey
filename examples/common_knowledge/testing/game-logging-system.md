# 게임 로깅 시스템

## 구현 방법

### GDScript (권장)
- **파일**: `game_logger.gd`
- **개발 시간**: 1.5일
- **성능**: 0.3% 오버헤드 (무시 가능)
- **유지보수**: 쉬움

### C++ GDExtension (비권장)
- **개발 시간**: 4주
- **성능**: 0.03% 오버헤드
- **ROI**: 10+ 프로젝트 필요

## 로그 형식

JSON Lines (.jsonl):
```json
{"version":1,"start_time":"...","game":"pong"}
{"frame":0,"time":0.0,"delta":0.016,"events":[...]}
```

## 통합 방법

1. `game_logger.gd` 복사
2. 메인 씬에 추가
3. 게임 오브젝트 참조 설정

**소요 시간**: 5분

## 관련 문서
- 구현: `game_logger.gd`
- 사용 가이드: `TEST-AUTOMATION-README.md`
- 설계: `godot-analysis/test-automation-system.md`
- 타당성: `DECISION-SUMMARY.md`
