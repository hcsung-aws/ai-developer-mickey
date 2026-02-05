# 세션 관리 프로토콜

## 세션 시작 시
1. Hook이 자동으로 이전 세션 아카이브 및 새 세션 로그 생성
2. `.kiro/sessions/CURRENT.md` 확인
3. `.kiro/sessions/HANDOFF.md` 확인 (있으면)
4. 이전 컨텍스트 요약 후 사용자에게 보고
5. Memory Graph 있으면 `recall_memories`로 프로젝트 기억 조회

## 세션 중
- 주요 작업 완료 시 CURRENT.md 업데이트
- 중요 결정 시 기록
- 수정한 파일 목록 유지

## /compact 후 새 세션 시작 시
1. agentSpawn hook이 자동으로 세션 전환 처리
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
