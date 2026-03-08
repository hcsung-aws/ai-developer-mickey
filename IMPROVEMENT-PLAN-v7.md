# Mickey v7 개선 계획

> Harness Engineering / AI-DLC / Ouroboros 트렌드 분석 기반 (Mickey 7 세션)

## 배경

2026년 AI 개발 트렌드(Harness Engineering, AI-DLC, Ouroboros)를 조사하고, Mickey의 현재 동작과 비교 분석하여 도출한 개선 방향성.

핵심 발견: Mickey는 이미 "점진적 harness 구축" 모델의 기반을 가지고 있으며, 이것이 Greenfield 최적화된 트렌드와의 차별점. Brownfield에서도 세션이 쌓일수록 정교해지는 에이전트라는 고유 포지션 확보 가능.

## 핵심 원칙: 프롬프트 최소화 + 점진적 구축

> **v7의 모든 구현은 이 원칙을 준수해야 한다.**

시스템 프롬프트(T1)는 범용 원칙만 포함하고, 상세 프로토콜은 프로젝트별 파일에서 점진적으로 구축한다.
이것은 v6.0 경량화의 핵심이자, "점진적 harness 구축"의 자기 적용이다.

### 구현 규칙

| 넣을 위치 | 기준 | 예시 |
|---|---|---|
| 시스템 프롬프트 (REMEMBER) | 한 줄로 표현 가능한 근본 원칙만 | "Completion Criteria 명확 시 자율 실행 가능" |
| ~/.kiro/mickey/ (T1.5 글로벌 가이드) | 구체적 실행 지침, 판단 기준 | Brownfield 절차, Completion Criteria 작성 가이드, 엔트로피 관리 규칙 |
| context_rule/ (T3b) | 프로젝트 특화 규칙 | 프로젝트별 린트 규칙, 빌드 주의사항 |
| 첫 세션에서 생성 | Mickey가 프로젝트 분석 후 구축 | 프로젝트별 INDEX 확장, auto_notes 초기 기록 |

> **참고**: resources의 `file://AGENTS.md`는 Kiro CLI 표준 (프로젝트별 에이전트 지시). Mickey 글로벌 가이드와는 별개.

### 배포 모델: Installer + T1.5

```
git clone → ./install.sh → kiro-cli chat --agent ai-developer-mickey
```

install.sh가 수행하는 작업:
1. kiro-cli 설치 확인
2. `~/.kiro/mickey/` → extended-protocols.md 설치 (T1.5 글로벌 가이드)
3. `~/.kiro/agents/` → ai-developer-mickey.json 설치

시스템 프롬프트에 T1.5 계층 추가 → 세션 시작 시 `~/.kiro/mickey/` 파일 자동 로딩.

| 형태 | 원칙 전달 방법 | 변경량 |
|---|---|---|
| Kiro CLI | install.sh → ~/.kiro/mickey/ + ~/.kiro/agents/ | 프롬프트 +6줄, extended-protocols.md 신규 |
| Kiro IDE Power | steering/ 디렉토리에 파일 추가 | 파일 1개 추가 |

### 각 개선 항목의 프롬프트 영향

| 항목 | 프롬프트 변경 | T1.5/context_rule 변경 |
|---|---|---|
| Brownfield 온보딩 | First Session에 분기 1줄 | 상세 절차는 T1.5 extended-protocols.md |
| Completion Criteria | SESSION.md 스키마에 1줄 | 작성 가이드는 T1.5 extended-protocols.md |
| 엔트로피 관리 | Continuing Session에 1줄 | 상세 규칙은 T1.5 extended-protocols.md |
| 자율성 모드 | REMEMBER에 1줄 추가 (Phase 2) | 판단 기준은 T1.5에 추가 예정 |
| Subagent Delegation | 없음 (Phase 2) | 위임 가이드라인은 T1.5에 추가 예정 |
| Backpressure | REMEMBER #12 강화 (Phase 2) | 없음 |

**Phase 1 시스템 프롬프트 증가량: +6줄 (252→258)**

## 개선 항목

### Phase 1: 핵심 기반 (구현 완료 ✅)

#### 1-1. Brownfield 온보딩 프로토콜 ✅
- 출처: Anyline meta-repo + Ouroboros knowledge protocol
- 내용: First Session에 Brownfield 분기 추가. 구조화된 탐색 → 의존성 그래프, 파일 역할, 빌드 명령, 알려진 함정을 auto_notes/에 자동 기록
- "before task: read, after task: write" 원칙 적용
- 구현 위치: 시스템 프롬프트 SESSION PROTOCOL

#### 1-2. Completion Criteria 도입 ✅
- 출처: AI-DLC
- 내용: SESSION.md의 각 작업에 검증 가능한 완료 기준 명시
- `자율성 = f(기준 명확도)` — 기준이 명확할수록 자율 실행 범위 확대
- 구현 위치: DOCUMENT SCHEMA (SESSION.md 스키마)

#### 1-3. 엔트로피 관리 자동화 ✅
- 출처: Harness Engineering garbage collection + Ouroboros background consciousness
- 내용: 세션 시작 시 자동 정리 체크 (오래된 auto_notes 정리, INDEX 최신화, 오래된 SESSION 아카이빙)
- 구현 위치: SESSION PROTOCOL (Continuing Session에 정리 단계 추가)

### Phase 2: 자율 실행 체계 (구현 완료 ✅)

#### 2-1. 자율성 모드 도입 (HITL/OHOTL/AHOTL) ✅
- 출처: AI-DLC
- 내용: 작업 유형별 자율성 수준 구분
  - HITL: 아키텍처 결정, 고위험 변경
  - OHOTL: 창의적/주관적 작업, 설계 작업
  - AHOTL: 명확한 Completion Criteria가 있는 기계적 작업
- 구현 위치: 시스템 프롬프트 신규 섹션

#### 2-2. Subagent Delegation 프로토콜 ✅
- 출처: Kiro subagent + Ouroboros supervisor/worker + AWS orchestration 패턴
- 내용: Mickey(orchestrator)가 목적별 subagent에 작업 위임
  - 탐색 에이전트: 코드베이스/트렌드 병렬 조사
  - 구현 에이전트: 독립 모듈 수정 (Completion Criteria 기반 자율 실행)
  - 검증 에이전트: 테스트/린트 실행 및 결과 보고
  - 지식 관리 에이전트: INDEX 갱신, auto_notes 정리, 엔트로피 관리
- 각 subagent에 전달할 것: 역할, 컨텍스트, Completion Criteria, 제약 조건
- 결과 통합: Mickey가 종합 → 교훈 추출 → 지식 베이스 갱신
- Ouroboros 참고 메커니즘:
  - Task decomposition + 결과 추적 (schedule → wait → get_result)
  - Budget/scope 제한 (무한 루프 방지)
  - Fallback chain (subagent 실패 시 Mickey 직접 처리)
  - 결과 기반 피드백 루프 (자율 실행 결과 → 교훈 추출 → 지식 승격)
- 자율 실행 원칙:
  - 가능 조건: Completion Criteria 명확 + rollback 가능 + 결과 검증 가능
  - 실행 후 필수: 결과 기록 + 교훈 추출 + 지식 반영
  - 자율성은 수단, 피드백 루프가 핵심
- 구현 위치: 시스템 프롬프트 신규 섹션 + agent 프로필 템플릿

#### 2-3. Backpressure 경량 도입 ✅
- 출처: AI-DLC
- 내용: 구현 후 검증 실패 시 다음 단계 진행 차단
- 자율 실행의 품질 게이트 역할
- 구현 위치: PROBLEM-SOLVING PROTOCOL에 차단 조건 추가

### Phase 3: 보류 (재검토 조건 포함)

| 항목 | 재검토 조건 |
|------|------------|
| 결정론적 린터/구조 테스트 | 특정 프로젝트에서 반복적 아키텍처 위반 발생 시 |
| Ouroboros식 self-modification | 프롬프트 자동 개선의 안전한 메커니즘 확보 시 |

### 이전 "보류"에서 채택으로 변경된 항목

| 항목 | 이전 판단 | 변경 사유 |
|------|----------|----------|
| Hat 기반 역할 분리 | 보류 | agent 단위 역할 분리로 재해석 → 2-2에 통합 |
| Full autonomous review | 보류 | AHOTL + Completion Criteria 내 자율 리뷰 → 2-1에 통합 |

## 참고 자료

| 출처 | URL | 핵심 개념 |
|------|-----|----------|
| OpenAI Harness Engineering | openai.com/index/harness-engineering/ | repo = system of record, progressive disclosure, garbage collection |
| AI-DLC | ai-dlc.dev | Hat 역할 분리, Completion Criteria, Backpressure, HITL/OHOTL/AHOTL |
| Ouroboros | github.com/razzant/ouroboros | Background consciousness, multi-model review, task decomposition |
| Anyline meta-repo | seylox.github.io/2026/03/05/blog-agents-meta-repo-pattern.html | Brownfield agents meta-repository, active-work tracking |
| Martin Fowler/Böckeler | martinfowler.com/articles/exploring-gen-ai/harness-engineering.html | Pre-AI vs Post-AI 유지보수, harness retrofit 비용 |
| AWS Prescriptive Guidance | docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/ | Orchestration/delegation 패턴 |
| AWS CAO | aws.amazon.com/blogs/opensource/introducing-cli-agent-orchestrator/ | CLI 기반 multi-agent orchestration |

## 작성 정보
- 작성: Mickey 7 세션 (2026-03-08)
- Phase 1 구현: Mickey 8 세션 (2026-03-09)
- Phase 2 구현: Mickey 8 세션 (2026-03-09)
- 상태: Phase 1+2 구현 완료, Phase 3 보류
