# Mickey 공통 지식 베이스

## 디렉토리 구조

```
common_knowledge/
├── INDEX.md (현재 파일)
├── godot/
│   └── extension-mechanisms.md
└── testing/
    └── game-logging-system.md

context_rule/
└── cpp-development-decision.md
```

## 빠른 참조

### Godot 엔진
- **확장 메커니즘**: `godot/extension-mechanisms.md`
  - GDExtension, Module, GDScript 비교
  - 코드 컨벤션

### 테스트 시스템
- **게임 로깅**: `testing/game-logging-system.md`
  - GDScript vs C++ 비교
  - 통합 방법

### 의사결정 규칙
- **C++ 개발**: `../context_rule/cpp-development-decision.md`
  - 체크리스트
  - ROI 분석

## 상세 문서 위치

### 프로젝트 루트
- `MICKEY-2-SESSION.md` - 세션 로그
- `DECISION-SUMMARY.md` - 의사결정 요약
- `TEST-AUTOMATION-README.md` - 사용 가이드

### godot-analysis/
- `test-automation-system.md` - 시스템 설계
- `cpp-library-feasibility-analysis.md` - C++ 타당성 분석
- `cpp-implementation-guide.md` - C++ 구현 예시

### 구현 파일
- `game_logger.gd` - 게임 로거
- `build_training_data.py` - 학습 데이터 생성
- `test_runner.py` - 자동 테스트

## 사용 방법

1. **새 세션 시작시**: `INDEX.md` 읽기
2. **특정 주제**: 해당 디렉토리 문서 참조
3. **상세 정보**: 관련 문서 링크 따라가기
