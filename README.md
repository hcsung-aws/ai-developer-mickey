# AI Developer Mickey

> [English Version](README-en.md)

> 생성형 AI 어시스턴트를 효과적으로 활용하기 위한 실전 가이드

![Mickey](docs/images/mickey-poster.png)

## 📖 프로젝트 소개

**AI Developer Mickey**는 생성형 AI 어시스턴트(Kiro CLI)를 활용하여 복잡한 소프트웨어 개발 프로젝트를 수행하는 과정에서 발견한 핵심 패턴과 전략을 정리한 교육용 프로젝트입니다.

### 해결하고자 한 문제

| 문제 | 해결 방법 |
|------|----------|
| **Context Window 부족** | 구조화된 문서로 필요한 정보만 로드 |
| **세션 간 일관성 상실** | 세션 로그와 핸드오프 문서로 연속성 유지 |
| **지식 관리 부재** | common_knowledge/와 context_rule/로 체계화 |

### 핵심 아이디어

**"Mickey"**라는 AI 개발자 에이전트를 만들어, 각 세션의 성공/실패 기록을 파일로 저장하고 다음 세션에서 참고하여 **지속적으로 개선**하는 방식으로 문제를 해결합니다.

```
세션 시작 → 이전 기록 참조 → 작업 수행 → 교훈 기록 → 다음 세션에 반영
```

## 🎯 학습 목표

- ✅ **Context Window 관리**: 제한된 컨텍스트를 효율적으로 활용
- ✅ **세션 간 일관성 유지**: 세션을 넘어 작업을 이어가는 전략
- ✅ **지식 관리 시스템**: 재사용 가능한 지식 저장 및 활용
- ✅ **프롬프트 진화**: 실패 경험을 통한 지속적인 개선

## 📚 문서 구조

### 핵심 가이드

| 문서 | 설명 |
|------|------|
| [Mickey 소개](docs/01-introduction.md) | Mickey 에이전트의 개념과 설계 |
| [Context Window 관리](docs/02-context-management.md) | 컨텍스트 효율적 활용 전략 |
| [세션 연속성](docs/03-session-continuity.md) | 세션 간 일관성 유지 방법 |
| [Prompt 엔지니어링](docs/04-prompt-engineering.md) | 효과적인 프롬프트 구조화 |
| [지식 관리 시스템](docs/05-knowledge-management.md) | 재사용 가능한 지식 구축 |
| [프롬프트 진화](docs/06-prompt-evolution.md) | v2.0 → v5.0 진화 과정 |
| [변경 이력](docs/07-changelog.md) | 버전별 변경사항 |

### 실전 사례

| 프로젝트 | 버전 | 문서 |
|----------|------|------|
| Godot 리플레이 시스템 | v2.0 | [한글](docs/case-study/godot-replay-system.md) |
| 패킷 캡처 에이전트 | v5.0 | [한글](docs/case-study/packet-capture-agent.md) |

## 🔄 프롬프트 진화

Mickey 프롬프트는 실제 프로젝트를 거치며 계속 진화합니다:

| 버전 | 핵심 변화 |
|------|----------|
| **v2.0** | 세션 연속성, 지식 관리 체계 확립 |
| **v5.0** | 목적 우선, 체크리스트, REMEMBER 섹션 |
| **v5.3** | 세션 종료 프로토콜, 자동 개선 제안 |
| **v5.4** | 필수 테스트 프로토콜 |

> 💡 자세한 변경 이력은 [변경 이력 문서](docs/07-changelog.md)를 참고하세요.

## 🚀 빠른 시작

### 1. Mickey 에이전트 설정

```bash
# Kiro CLI 설치 후
cp examples/ai-developer-mickey.json ~/.kiro/agents/
```

### 2. 프로젝트에서 Mickey 실행

```bash
kiro chat --agent ai-developer-mickey
```

### 3. Mickey가 자동으로 수행하는 것

- 프로젝트 분석 및 문서 생성
- 세션 로그 작성 (MICKEY-N-SESSION.md)
- 교훈 기록 및 다음 세션 인수인계

## 💡 핵심 인사이트

### AI는 피드백 도구

- AI를 '도깨비방망이'가 아닌 **'피드백 도구'**로 활용
- 결과적인 학습과 판단은 **사람**이 수행
- 지속적인 개선은 **반복적인 피드백**을 통해 가능

### 프롬프트는 진화한다

- "한 번 작성하고 끝"이 아님
- **실패 경험을 통해 지속적으로 개선**
- 각 세션의 교훈을 프롬프트에 반영

## 📁 디렉토리 구조

```
ai-developer-mickey/
├── docs/                    # 핵심 가이드 문서
├── sessions/               # Mickey 세션 로그 예시
├── examples/               # 설정 파일 및 예시
│   ├── ai-developer-mickey.json  # 최신 프롬프트
│   ├── common_knowledge/   # 지식 관리 예시
│   └── context_rule/       # 컨텍스트 규칙 예시
└── godot-pong/            # Godot 리플레이 시스템 코드
```

## 🔗 관련 링크

- [Kiro CLI](https://github.com/aws/kiro-cli) - AWS의 생성형 AI 어시스턴트
- [AI Agent 자동화 플랫폼](https://github.com/hcsung-aws/ai-agent-automation-platform) - Mickey 활용 프로젝트

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR을 환영합니다! 생성형 AI 활용 경험을 공유해주세요.

---

**Made with ❤️ by Mickey (AI Developer Agent powered by Kiro CLI)**
