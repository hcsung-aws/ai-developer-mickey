# 분석 중간 요약: 기타 프로젝트들

## ai-agent-automation-platform (31세션)

### 프로젝트 개요
AI Agent 기반 운영 자동화(AIOps) 스타터 킷. 로컬→AWS 프로덕션 전체 여정 지원.
Python + AWS (AgentCore, Bedrock, CDK, Fargate).

### 세션 흐름 패턴
- M1~3: PoC 구현 (AgentCore 기반 DevOps Agent)
- M4~9: 기능 확장 (피드백, Agent Builder, KB, 테스트 모드)
- M10~13: Knowledge Base 구현 + 문서화
- M14~17: 리팩토링 + Kiro CLI Agent 체계화 (delegate 워크플로)
- M18~23: 뉴스 Agent + 템플릿 개선 + KB 자동 생성 (CDK)
- M24~29: PURPOSE-SCENARIO 도입 + Hybrid Architecture + E2E 배포
- M30~32: 멀티모달 프로토타이핑 + 병합

### 사용자 접근법 패턴
1. **PoC → 기능 확장 → 리팩토링 → 배포 사이클**: 빠르게 동작하는 것 먼저 → 기능 추가 → 구조 정리 → 프로덕션
2. **Agent Builder로 Agent 생성 → 리뷰 → 피드백 루프**: AI가 AI를 만들고 개선하는 메타 패턴
3. **템플릿 기반 재사용**: 로컬/AWS 템플릿으로 반복 가능한 배포
4. **E2E 테스트 중심 검증**: 각 단계마다 E2E 테스트로 확인
5. **프로토타이핑 → 병합**: 실험적 기능을 별도 프로토타입으로 검증 후 메인에 병합

### 핵심 교훈
- Agent Builder가 프롬프트 세부 요구사항을 자기 해석으로 변경하는 경향 → 명시적 지시 필요
- KB 도구가 tools에 있어도 프롬프트에 사용 지침이 없으면 Agent가 호출하지 않음
- use_subagent delegate → 리뷰 → 피드백 루프 패턴이 효과적

## game-ui-qa-genai-automation (254 아카이브, Power 기반)

### 프로젝트 개요
AWS Bedrock Claude Vision 기반 게임 UI 분석 + BVT 자동 검증 프레임워크.
Python + AWS Bedrock + Playwright.

### 특징
- Power Mickey 최초 실전 적용 프로젝트
- memorygraph MCP 실전 사용 → 버그 발견 및 우회법 축적
- project-lessons.md에 상세한 교훈 기록 (MCP 디버깅, Strategy 패턴 등)
- 254개 아카이브 = 가장 많은 세션 수 (Power의 spec task 단위)

### 사용자 접근법 패턴
- Power Mickey의 실전 검증장 역할
- 발견된 문제가 Mickey 프로토콜 개선으로 직접 연결 (memorygraph 버그 → kiro-powers.md)

## gamejob_crawler (2세션)

### 프로젝트 개요
게임 채용공고 크롤링 → LLM 분석 → Slack 봇 인텔리전스 시스템.
Python + AWS (Lambda, S3, Bedrock, Slack).

### 특징
- 2세션만에 전체 시스템 구현 + 배포 + E2E 테스트
- 명확한 PURPOSE-SCENARIO (4개 시나리오)
- 빠른 실행 패턴 (계획보다 구현 우선)

## loop-translator (4세션)

### 프로젝트 개요
SharePoint Loop 한국어 문서 → 영문 번역 자동화.
Python + Playwright + Bedrock.

### 특징
- 실용적 도구 (업무 자동화)
- 4세션에 걸쳐 점진적 버그 수정 + 포맷팅 보존
- 작은 프로젝트에서도 Mickey 프로토콜 적용

## skr-reverse-poc (2세션, 11~12번)

### 프로젝트 개요
세븐나이츠 Re:BIRTH 역기획 → 텍스트 RPG + AWS 인프라 데모.
Python + DynamoDB + QUIC.

### 특징
- AI 활용 게임 개발 프로세스 실험
- 역기획 → 온톨로지 → 설계 → 구현 파이프라인
- DynamoDB 스키마 설계에 MCP 활용
- 세션 11~12만 존재 (이전 세션은 다른 환경에서 진행된 것으로 추정)

## 프로젝트 간 공통 패턴

1. **다양한 도메인에서 일관된 Mickey 활용**: 게임 QA, AIOps, 패킷 캡처, 크롤링, 번역, 게임 개발
2. **실전 프로젝트 → Mickey 개선 피드백 루프**: 모든 프로젝트의 실패/교훈이 Mickey 프로토콜로 환류
3. **Phase/Step 기반 점진적 접근**: 큰 프로젝트는 Phase로 나누고, 각 Phase도 Step으로 세분화
4. **E2E 검증 중심**: 기능 구현 후 반드시 E2E 테스트
5. **PURPOSE-SCENARIO 활용**: 대부분의 프로젝트에 명확한 목적+시나리오 문서 존재
