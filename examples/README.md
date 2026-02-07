# Mickey System Prompt Versions

이 디렉토리에는 Mickey 시스템 프롬프트의 여러 버전이 포함되어 있습니다.

## 버전 목록

| 파일 | 버전 | 설명 |
|------|------|------|
| `ai-developer-mickey.json` | v6.0 | 최신 경량화 프롬프트 (스키마 기반) |
| `MICKEY-PROMPT-V6.md` | v6.0 | 경량화/최적화 - 도메인 특화 제거, 스키마 전환 |
| `MICKEY-PROMPT-V5.md` | v5.1 | 전제조건 검증, 체크리스트 기반 |
| `ai-developer-mickey-v5.json` | v5.0 | 목적 우선, 체크리스트, 자동화 |

## 버전별 주요 차이점

### v5.x → v6.0 변경 사항

1. **경량화**: 프롬프트 크기 대폭 축소 (템플릿 전문 → Document Schema 테이블)
2. **도메인 특화 제거**: Async/Multiplayer/Windows/MSVC 등 특정 기술 내용 제거
3. **3-Tier Context Loading**: 정보를 계층적으로 로딩하여 context window 효율화
4. **자립형 설계**: 프롬프트 하나만으로 어떤 프로젝트에서든 동작
5. **REMEMBER 정리**: 24개 → 13개 (범용 원칙만 유지)

### v2.0 → v5.0 변경 사항

1. **REMEMBER 원칙**: 6개 → 18개
2. **체크리스트 추가**: 7개 (비동기, 멀티플레이어, 빌드 등)
3. **목적 우선 원칙**: 작업 전 목적 확인 필수화
4. **에러 핸들링 프로토콜**: 에러 로그 즉시 확인
5. **세션 종료 프로토콜**: "세션 정리" 시 자동 수행

자세한 내용은 [프롬프트 진화 가이드](../docs/06-prompt-evolution.md)를 참고하세요.

## 사용 방법

Kiro CLI에서 사용하려면:

```bash
# 최신 v6.0 사용 (권장)
cp examples/ai-developer-mickey.json ~/.kiro/agents/
kiro chat --agent ai-developer-mickey
```
