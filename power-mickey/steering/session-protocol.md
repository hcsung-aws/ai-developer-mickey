# 세션 관리 프로토콜

## 세션 시작 시 (Mickey Session Initialize 훅)
1. 사용자가 Agent Hooks에서 "Mickey Session Initialize" Start Hook 클릭
2. Agent가 `python .kiro/scripts/session_init.py` 실행 (이전 세션 아카이브 + 새 CURRENT.md + SESSION-BRIEF.md 생성)
3. **PURPOSE-SCENARIO.md 최우선 로딩** — 없으면 첫 세션 절차로 전환
4. `.kiro/sessions/SESSION-BRIEF.md`만 읽기 (HANDOFF 전문을 읽지 않음 — context 절약)
5. Memory Graph에서 기억 제목/태그 목록만 조회 (상세 내용은 on-demand)
6. **목적 재확인**: PURPOSE-SCENARIO.md 내용을 간략히 언급, 변경 필요 시 사용자에게 조정 여부 확인
7. 이전 세션 요약 + 참고 가능한 기억 목록을 사용자에게 보고

### 첫 세션 (PURPOSE-SCENARIO.md 없을 때)
- 사용자에게 질문: "이 프로젝트가 완성되면 어떻게 사용하게 되나요?"
- 답변 기반으로 PURPOSE-SCENARIO.md 생성 (필수 섹션: Ultimate Purpose, Usage Scenarios, Acceptance Criteria, Last Confirmed)

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

### 기타
- 수정한 파일 목록 유지
- **목적 정합성 체크**: 아래 상황 발생 시 사용자에게 알리고 PURPOSE-SCENARIO.md 조정 여부 확인
  - 구현 방향이 PURPOSE-SCENARIO.md의 사용 시나리오와 충돌
  - 기능 확장으로 원래 목적과 다른 방향성 발견
  - 기술적 제약으로 목적 달성 방식 변경 필요

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

## 목표
[세션 목표]

## 진행 상황
- [x] 완료 작업
- [ ] 진행 중

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
