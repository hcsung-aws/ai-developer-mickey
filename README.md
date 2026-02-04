# AI Developer Mickey

> [English Version](README-en.md)

> 생성형 AI 어시스턴트를 효과적으로 활용하기 위한 실전 가이드

![Mickey](docs/images/mickey-poster.png)

## 📖 프로젝트 소개

**AI Developer Mickey**는 생성형 AI 어시스턴트(Kiro CLI)를 활용하여 복잡한 소프트웨어 개발 프로젝트를 수행하는 과정에서 발견한 핵심 패턴과 전략을 정리한 교육용 프로젝트입니다.

### 해결하고자 한 문제

1. **Context Window 부족**: 복잡한 이슈 분석 중 컨텍스트 윈도우 한계로 실패
2. **세션 간 일관성 상실**: 세션 재시작 시 이전 컨텍스트 유실로 정상 동작 실패
3. **지식 관리 부재**: 축적된 지식과 경험을 효과적으로 재사용하지 못함

### 핵심 아이디어

**"Mickey"**라는 AI 개발자 에이전트를 만들어, 각 세션의 성공/실패 기록을 파일로 저장하고 다음 세션에서 참고하여 지속적으로 개선하는 방식으로 문제를 해결합니다.

### 🔄 프롬프트의 진화

Mickey 프롬프트는 실제 프로젝트를 거치며 계속 진화하고 있습니다:

| 버전 | 프로젝트 | 세션 수 | 핵심 변화 |
|------|----------|---------|----------|
| **v2.0** | Godot 리플레이 시스템 | Mickey 1-6 | 세션 연속성, 지식 관리 체계 확립 |
| **v5.0** | 패킷 캡처 에이전트 | Mickey 1-12 | 목적 우선, 체크리스트, 자동화 |
| **v5.1** | AI Agent 자동화 플랫폼 | Mickey 1-7 | 전제조건 검증, Agent Builder 연동 |
| **v5.2** | AI Agent 자동화 플랫폼 | Mickey 8 | 문서화 패턴, 점진적 도입 원칙 |
| **v5.3** | AI Agent 자동화 플랫폼 | Mickey 9 | 세션 종료 프로토콜 강화, 자동 개선 제안 |

> 💡 **핵심 통찰**: AI 프롬프트는 "한 번 작성하고 끝"이 아니라 **실패 경험을 통해 지속적으로 진화**시켜야 합니다. 자세한 내용은 [프롬프트 진화 가이드](docs/06-prompt-evolution.md)를 참고하세요.

## 🎯 학습 목표

이 프로젝트를 통해 다음을 배울 수 있습니다:

- ✅ **Context Window 관리**: 제한된 컨텍스트를 효율적으로 활용하는 방법
- ✅ **Context 추상화**: 정보를 구조화하여 필요한 내용만 로드하는 기법
- ✅ **세션 간 일관성 유지**: 세션을 넘어 작업을 이어가는 전략
- ✅ **Prompt 구조화**: 효과적인 프롬프트 설계 및 개선 방법
- ✅ **지식 관리 시스템**: 재사용 가능한 지식 저장 및 활용
- ✅ **프롬프트 진화**: 실패 경험을 통한 지속적인 프롬프트 개선 🆕

## 📚 문서 구조

### 핵심 가이드 (v2.0)

1. [Mickey 소개](docs/01-introduction.md) - Mickey 에이전트의 개념과 설계
   - [English](docs/01-introduction-en.md)
2. [Context Window 관리](docs/02-context-management.md) - 컨텍스트 효율적 활용 전략
   - [English](docs/02-context-management-en.md)
3. [세션 연속성](docs/03-session-continuity.md) - 세션 간 일관성 유지 방법
   - [English](docs/03-session-continuity-en.md)
4. [Prompt 엔지니어링](docs/04-prompt-engineering.md) - 효과적인 프롬프트 구조화
   - [English](docs/04-prompt-engineering-en.md)
5. [지식 관리 시스템](docs/05-knowledge-management.md) - 재사용 가능한 지식 구축
   - [English](docs/05-knowledge-management-en.md)

### 프롬프트 진화 가이드 (v5.0) 🆕

6. **[프롬프트 진화: v2.0 → v5.0](docs/06-prompt-evolution.md)** - 두 번째 프로젝트에서 배운 것 ⭐
   - [English](docs/06-prompt-evolution-en.md)

### AI 관점

- [AI 관점에서 본 Mickey](docs/ai-perspective.md) - AI의 포스트모템 및 실무 가이드
  - [English](docs/ai-perspective-en.md)

### 실전 사례

| 프로젝트 | 버전 | 상태 | 문서 |
|----------|------|------|------|
| Godot 리플레이 시스템 | v2.0 | 완료 | [한글](docs/case-study/godot-replay-system.md) / [English](docs/case-study/godot-replay-system-en.md) |
| 패킷 캡처 에이전트 | v5.0 | 진행 중 | [한글](docs/case-study/packet-capture-agent.md) / [English](docs/case-study/packet-capture-agent-en.md) 🆕 |

### 세션 로그

- [Godot 프로젝트 세션](sessions/) - Mickey 1~6
- [패킷 캡처 프로젝트 세션](sessions/packet-capture/) - Mickey 1~12 🆕

## 🚀 빠른 시작

### Mickey 에이전트 설정

```json
{
  "name": "ai-developer-mickey",
  "description": "세션 연속성을 유지하며 지속적으로 개선하는 AI 개발자",
  "prompt": "You are an AI developer agent 'Mickey'..."
}
```

자세한 설정은 [Mickey 소개](docs/01-introduction.md)를 참고하세요.

### 디렉토리 구조

```
ai-developer-mickey/
├── docs/                    # 핵심 가이드 문서
│   ├── 01-introduction.md
│   ├── 02-context-management.md
│   ├── 03-session-continuity.md
│   ├── 04-prompt-engineering.md
│   ├── 05-knowledge-management.md
│   └── case-study/         # 실전 사례 연구
├── sessions/               # Mickey 세션 로그
│   ├── session_log.txt     # Mickey 1
│   ├── MICKEY-2-SESSION.md
│   ├── MICKEY-3-SESSION.md
│   ├── MICKEY-4-SESSION.md
│   ├── MICKEY-5-SESSION.md
│   └── MICKEY-6-SESSION.md
├── examples/               # 코드 예시
│   ├── common_knowledge/   # 지식 관리 예시
│   └── context_rule/       # 컨텍스트 규칙 예시
└── godot-pong/            # Godot 리플레이 시스템 코드
```

## 💡 핵심 인사이트

### 1. GenAI는 '과거 경험의 조합'

- 완전히 새로운 요구사항을 처리하려면 **명확한 맥락**이 필수
- 백 가지 가드레일보다 **한 가지 명확한 지시**가 효과적
- GenAI는 경험 '모듈'을 연결하는 방식으로 동작

### 2. 효율성의 함정

- 단순한 길로 빠지는 것은 그것이 '가장 효율적'이기 때문
- **맥락을 제대로 이해하고 지시**하면 부작용 최소화
- **단계별 테스트와 확인**은 필수

### 3. AI는 피드백 도구

- AI를 '도깨비방망이'가 아닌 **'피드백 도구'**로 활용
- 결과적인 학습과 판단은 **사람**이 수행
- 지속적인 개선은 **반복적인 피드백**을 통해 가능

## 📊 프로젝트 성과

### Godot 리플레이 시스템 개발

Mickey를 활용하여 Godot 엔진의 Pong 게임에 완전한 리플레이 및 회귀 테스트 시스템을 구축했습니다:

- ✅ **Phase 1**: 100% pass rate 달성 (Ball reset 감지)
- ✅ **Phase 2**: 사용자 가이드 및 CI/CD 통합 문서 작성
- ✅ **Phase 3**: Multi-log 배치 테스트 인프라 구축
- ✅ **Phase 3-1**: AI 기반 자동 시나리오 생성 시스템

**주요 기능:**
- 게임 플레이 녹화 및 재생
- 프레임별 상태 검증 (Position, Velocity, Direction)
- 자동 버그 리포트 생성
- Headless 모드 배치 테스트
- 6가지 시나리오 자동 생성 (AI 난이도별)

## 🔗 관련 링크

- [Kiro CLI](https://github.com/aws/kiro-cli) - AWS의 생성형 AI 어시스턴트
- [Godot Engine](https://godotengine.org/) - 오픈소스 게임 엔진
- [패킷 캡처 에이전트](https://github.com/hcsung-aws/packet-capture-log-agent) - 두 번째 프로젝트 🆕
- [원본 Notion 문서](https://www.notion.so/vaneddie/Demo-AI-Developer-Mickey-Godot-2bcd0b7b36dd807f8487fd8cab537935)

## 🚀 진행 중인 프로젝트

### AI Agent 기반 업무 자동화 플랫폼

Mickey를 활용하여 **어떤 조직/업무에도 적용 가능한 Multi-Agent 시스템 템플릿**을 개발했습니다.

**주요 기능**:
- Multi-Agent 협업 (Supervisor + 전문가 Agent)
- 실행 기록 기반 점진적 개선
- 👍/👎 피드백 수집 및 분석
- **Agent Builder**: 자연어로 새 Agent 생성 및 Supervisor 연결

**v5.2 주요 개선사항**:
- **문서화 패턴**: 핵심 메시지 정의, 사용자 여정 기반 구조화, 실패 사례 포함
- **점진적 도입 원칙**: 최소 기능으로 시작, 피드백 체계 먼저, 피드백 기반 확장만

**v5.3 주요 개선사항** (NEW):
- **세션 종료 프로토콜 강화**: 교훈 분석 → 범용/프로젝트 분류 → 사용자 확인 → 자동 적용
- **자동 개선 제안**: 세션 중 발견한 패턴을 시스템 프롬프트 또는 프로젝트 지침에 자동 반영

**v5.1 주요 개선사항**:
- 전제조건 검증: 구현 시작 전 목적 달성에 필요한 핵심 자원/조건 확보 여부 확인
- Agent Builder 연동: Mickey가 Agent Builder를 subagent로 호출하여 새 Agent 생성 가능

**Agent Builder 사용법**:
```bash
# Kiro CLI에서 Agent Builder 실행
kiro chat --agent agent-builder

# 예시 명령
> "HR Agent 만들어줘. 휴가 신청, 직원 조회 기능으로"
```

Agent Builder는 Mickey와 연동하여 프로젝트 맥락을 참고하면서 새 Agent를 생성합니다.

**Agent Builder v5.2 개선사항**:
- **단계별 확장 원칙**: 처음 1-2개 기능으로 시작, 테스트 후 확장 권장
- **테스트 데이터 패턴**: 하드코딩 테스트 → 실제 API 연동 순서
- **app.py 연결 안내**: 수동 연결 필요 명시
- **피드백 루프 안내**: 생성 후 피드백 수집/분석 안내

**Agent Builder v5.3 개선사항** (NEW):
- **app.py 자동 연결**: 9개 항목 체크리스트로 UI 연결까지 자동화
- **테스트 데이터 명시 필수**: 응답에 `⚠️ [테스트 데이터]` 표시 강제
- **코드 품질 원칙**: TDD, Clean Architecture, Tidy First 원칙 준수

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR을 환영합니다! 생성형 AI 활용 경험을 공유해주세요.

---

**Made with ❤️ by Mickey (AI Developer Agent powered by Kiro CLI)**
