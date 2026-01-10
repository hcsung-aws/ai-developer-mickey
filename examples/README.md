# Mickey System Prompt Versions

이 디렉토리에는 Mickey 시스템 프롬프트의 여러 버전이 포함되어 있습니다.

## 버전 목록

| 파일 | 버전 | 프로젝트 | 설명 |
|------|------|----------|------|
| `ai-developer-mickey.json` | v2.0 | Godot 리플레이 시스템 | 기본 세션 연속성, 지식 관리 |
| `ai-developer-mickey-v5.json` | v5.0 | 패킷 캡처 에이전트 | 목적 우선, 체크리스트, 자동화 |

## 버전별 주요 차이점

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
# v2.0 사용
kiro-cli chat --agent examples/ai-developer-mickey.json

# v5.0 사용 (권장)
kiro-cli chat --agent examples/ai-developer-mickey-v5.json
```
