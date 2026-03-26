# 세션 관리 프로토콜

## 세션 시작 시 (Mickey Session Initialize 훅)
1. 사용자가 Agent Hooks에서 "Mickey Session Initialize" Start Hook 클릭
2. Agent가 `python .kiro/scripts/session_init.py` 실행 (이전 세션 아카이브 + 새 CURRENT.md + SESSION-BRIEF.md 생성)
3. **PURPOSE-SCENARIO.md 최우선 로딩** — 없으면 첫 세션 절차로 전환
4. `.kiro/sessions/SESSION-BRIEF.md`만 읽기 (HANDOFF 전문을 읽지 않음 — context 절약)
5. **글로벌 지식 로딩**: `~/.kiro/mickey/patterns/INDEX.md` + `~/.kiro/mickey/domain/INDEX.md` 존재 시 로딩
6. Memory Graph에서 기억 제목/태그 목록만 조회 (상세 내용은 on-demand)
7. **목적 재확인**: PURPOSE-SCENARIO.md 내용을 간략히 언급, 변경 필요 시 사용자에게 조정 여부 확인
8. 이전 세션 요약 + 참고 가능한 기억 목록을 사용자에게 보고

### 첫 세션 (PURPOSE-SCENARIO.md 없을 때)
- 사용자에게 질문: "이 프로젝트가 완성되면 어떻게 사용하게 되나요?"
- 답변 기반으로 PURPOSE-SCENARIO.md 생성 (필수 섹션: Ultimate Purpose, Usage Scenarios, Acceptance Criteria, Last Confirmed)

### Brownfield 감지 (기존 코드/문서가 있는 프로젝트)
첫 세션에서 기존 자산 발견 시 PURPOSE-SCENARIO 생성 전에 수행:
1. **자산 식별**: 디렉토리 구조 탐색, 핵심 파일 식별 (설정, 진입점, README)
2. **관계 분석**: 파일/컴포넌트 간 관계, 데이터 흐름 파악. 주요 파일은 실제 내용을 읽어서 분석
3. **상태 평가**: 기능별 완성도, 목표 대비 Gap, 품질 관찰
4. 분석 결과를 사용자에게 보고 후 PURPOSE-SCENARIO 생성으로 진행

> **⚠️ Context Window 최적화**: 세션 시작 시 최소한의 정보만 로딩한다.
> 상세 HANDOFF 내용이나 memorygraph 상세는 작업 중 필요할 때 조회한다.

## 작업 중 on-demand 조회
- HANDOFF.md 상세 내용이 필요하면 그때 읽기
- memorygraph에서 관련 기억의 상세 내용이 필요하면 recall_memories로 조회
- 이전 결정/교훈 참고가 필요하면 해당 기억 ID로 상세 조회

## 세션 중

### CURRENT.md 업데이트 트리거 (아래 중 하나 발생 시)
- TODO 항목 완료
- 에러 조사→수정→검증 사이클 완료
- 사용자와 의사결정 확정
- 파일 3개 이상 수정
- steering 또는 project-lessons.md 변경

### 목적 정합성 체크
아래 상황 발생 시 사용자에게 알리고 PURPOSE-SCENARIO.md 조정 여부 확인:
- 구현 방향이 PURPOSE-SCENARIO.md의 사용 시나리오와 충돌
- 기능 확장으로 원래 목적과 다른 방향성 발견
- 기술적 제약으로 목적 달성 방식 변경 필요

### 동작 시나리오 체크
새 기능/수정 구현 시 아래를 사용자에게 기술하고 확인:
- 완성 후 어떻게 동작하는지 (흐름)
- 기존 코드와 어디서 연결되는지 (연결점)
- 사용자가 어떻게 사용하는지 (사용법)

### Completion Criteria
작업 목표 설정 시 검증 가능한 완료 기준을 명시한다:
- **관찰 가능**: 실행 결과로 확인 가능 (빌드 성공, 테스트 통과)
- **명확**: 주관적 판단 불필요 ("깔끔한 코드" ❌ → "lint 에러 0" ✅)
- **최소**: 해당 작업의 핵심만

### 엔트로피 체크 (계속 세션에서)
컨텍스트 로딩 후 빠르게 확인:
1. **project-lessons.md 최신성**: 오래된 항목이 여전히 유효한지
2. **steering 정합성**: project-lessons.md 항목 수 상한(10개) 준수 여부
3. **아카이브 필요성**: `.kiro/sessions/archive/`에 오래된 세션이 과도하게 쌓여 있지 않은지

## 세션 종료 시 (Mickey Session Close 훅)
1. 사용자가 Agent Hooks에서 "Mickey Session Close" Start Hook 클릭
2. Agent가 `self-improvement.md` steering을 readSteering으로 읽고 절차 숙지
3. CURRENT.md 업데이트 (목표, 진행 상황, 주요 결정, 수정 파일, 다음 단계)
4. HANDOFF.md 생성/업데이트
5. 교훈 분석 → project-lessons.md 추가
6. 중요 교훈 → memorygraph store_memory 저장
7. 범용 원칙 → 사용자에게 Global steering 추가 제안
8. 최종 결과 보고

## /compact 후 새 세션 시작 시
1. Mickey Session Initialize 훅을 다시 실행
2. /compact된 context에서 이전 작업 내용 확인
3. HANDOFF.md 참고
4. 새 세션 로그에 목표 설정 후 작업 계속

## 세션 로그 형식 (CURRENT.md)

```markdown
# Session Log

## Session Meta
- Type: [Implementation/Self-Improvement/Maintenance/Planning]

## 목표
[세션 목표]

## Purpose Alignment
- 기여 시나리오: [PURPOSE-SCENARIO의 어느 시나리오/단계]
- 이번 세션 범위: [구체적 범위]

## 진행 상황
- [x] 완료 작업 | CC: [완료 기준]
- [ ] 진행 중 | CC: [완료 기준]

## 주요 결정
- [결정 내용과 이유]

## 수정 파일
- [파일 목록]

## 다음 단계
- [다음 작업]
```

## 핸드오프 형식 (HANDOFF.md)

```markdown
# Handoff

## 현재 상태
[1~2줄 요약]

## 다음 단계
[1~2줄 요약]

## 중요 컨텍스트
[CURRENT.md에 없는 것만]

## Quick Reference
- 세션 로그: .kiro/sessions/CURRENT.md
- Context window: [상태]
```
