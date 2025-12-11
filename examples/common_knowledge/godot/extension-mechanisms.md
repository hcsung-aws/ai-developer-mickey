# Godot 확장 메커니즘

## 세 가지 방법

### 1. GDExtension (외부 라이브러리)
- **파일**: DLL/SO 동적 라이브러리
- **장점**: 엔진 재빌드 불필요, 배포 용이
- **단점**: 성능 오버헤드, API 제한
- **적합**: 범용 라이브러리, 플러그인

### 2. Engine Module (내부 모듈)
- **위치**: `godot/modules/`
- **장점**: 최고 성능, 전체 API 접근
- **단점**: 엔진 재빌드 필수, 배포 어려움
- **적합**: 엔진 핵심 기능

### 3. GDScript (스크립트)
- **파일**: .gd 스크립트
- **장점**: 빠른 개발, 쉬운 수정
- **단점**: 상대적으로 느림 (실제로는 충분)
- **적합**: 대부분의 게임 로직

## 코드 컨벤션

- 클래스: `PascalCase`
- 메서드: `snake_case`
- 파라미터: `p_` 접두사
- 멤버: `snake_case`

## 관련 문서
- 구현 예시: `godot-analysis/cpp-implementation-guide.md`
- 타당성 분석: `godot-analysis/cpp-library-feasibility-analysis.md`
