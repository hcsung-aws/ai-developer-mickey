# 세션 관리 프로토콜

## 세션 시작 시 (Mickey Session Initialize 훅)
1. 사용자가 Agent Hooks에서 "Mickey Session Initialize" Start Hook 클릭
2. Agent가 `python .kiro/scripts/session_init.py` 실행 (이전 세션 아카이브 + 새 CURRENT.md + SESSION-BRIEF.md 생성)
3. `.kiro/sessions/SESSION-BRIEF.md`만 읽기 (HANDOFF 전문을 읽지 않음 — context 절약)
4. Memory Graph에서 기억 제목/태그 목록만 조회 (상세 내용은 on-demand)
5. 이전 세션 요약 + 참고 가능한 기억 목록을 사용자에게 보고

> **⚠️ Context Window 최적화**: 세션 시작 시 최소한의 정보만 로딩한다.
> 상세 HANDOFF 내용이나 memorygraph 상세는 작업 중 필요할 때 조회한다.

## 작업 중 on-demand 조회
- HANDOFF.md 상세 내용이 필요하면 그때 읽기
- memorygraph에서 관련 기억의 상세 내용이 필요하면 recall_memories로 조회
- 이전 결정/교훈 참고가 필요하면 해당 기억 ID로 상세 조회

## 세션 중
- 주요 작업 완료 시 CURRENT.md 업데이트
- 중요 결정 시 기록
- 수정한 파일 목록 유지

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
[완료된 것, 진행 중인 것]

## 즉시 다음 단계
1. [Step 1]
2. [Step 2]

## 중요 컨텍스트
- [알아야 할 것들]

## 유용한 명령어
```bash
[자주 사용한 명령어]
```
```
