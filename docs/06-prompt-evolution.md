# 프롬프트 진화: v2.0 → v5.0

> [English Version](06-prompt-evolution-en.md)

> 두 번째 프로젝트에서 배운 것: AI 프롬프트는 "작성"하는 것이 아니라 "진화"시키는 것이다

## 개요

이 문서는 Mickey 프롬프트가 첫 번째 프로젝트(Godot 리플레이 시스템, v2.0)에서 두 번째 프로젝트(패킷 캡처 에이전트, v5.0)를 거치며 어떻게 진화했는지, 그리고 **왜 그렇게 진화해야 했는지**를 설명합니다.

**핵심 메시지**: 프롬프트 진화의 동력은 **실패 경험**입니다.

## 진화 요약

| 영역 | v2.0 | v5.0 | 변화 이유 |
|------|------|------|----------|
| REMEMBER 원칙 | 6개 | 18개 | 새로운 실패 패턴 발견 |
| 체크리스트 | 없음 | 7개 | 일반 지침으로는 구체적 실수 방지 불가 |
| 자동화 | 없음 | 세션 종료 프로토콜 | 반복 지시 비효율 |
| 목적 확인 | 없음 | 필수 | 수단에 매몰되어 목적 상실 |

---

## 1. "기록하라" → "목적을 먼저 확인하라"

### v2.0의 접근

```
세션 로그 작성에 집중
→ 무엇을 했는지 기록
→ 다음 세션에서 이어가기
```

### v5.0에서 추가된 것

```markdown
## 세션 시작 시 질문

"오늘 작업의 **최종 목적**은 무엇인가요?"

→ 목적을 명확히 한 후, 그 목적에 가장 **단순하고 직접적인** 방법을 먼저 제안
```

### 왜 바뀌어야 했는가?

**Mickey 7의 실패:**
- 목적: 패킷 캡처 테스트
- 시도: Forgotten Server(오픈소스 게임 서버) 설정
- 결과: 3일 소요 (vcpkg 버그, 프로토콜 버전, 포트 문제...)
- 전환: 자체 시뮬레이터 개발 → 1.5일 완성

**교훈:**
> AI는 주어진 작업을 열심히 하지만, 그것이 목적에 최적인지 판단하지 않는다.

### AI 활용자가 배울 점

**나쁜 예:**
```
"Forgotten Server를 설정해줘"
```

**좋은 예:**
```
"패킷 캡처 테스트를 하고 싶어. 
Forgotten Server가 최선인지, 더 단순한 방법이 있는지 먼저 분석해줘"
```

---

## 2. "분석하라" → "체크리스트를 따르라"

### v2.0의 접근

```markdown
### Before ANY Implementation:

1. Analyze Data Structures (5-10 minutes)
2. Analyze Side Effects (5-10 minutes)
3. Search for Similar Issues
4. Present Options to User
5. Get User Confirmation
```

### v5.0에서 추가된 것

```markdown
### 비동기/콜백 패턴 구현 시 체크리스트

1. **버퍼 소유권**
   - 버퍼를 누가 할당하고 해제하는가?
   - 버퍼 크기/오프셋을 누가 관리하는가?
   - 비동기 완료 시 버퍼가 유효한가?

2. **락 재진입**
   - 콜백/핸들러 안에서 락을 다시 잡는가?
   - std::mutex vs std::recursive_mutex 선택

3. **생명주기**
   - 콜백 실행 시 객체가 살아있는가?
   - shared_from_this() 사용 여부
```

### 왜 바뀌어야 했는가?

**Mickey 8의 실패들:**

1. **버퍼 소유권 문제**
   - 증상: 캐릭터 좌표 워프, 입력 불가
   - 원인: 외부 ParsePacket에서 버퍼 수정 → Session의 recvSize_ 불일치
   - 해결: Session 내부에서 버퍼 관리

2. **중첩 락 데드락**
   - 증상: abort() 발생
   - 원인: ForEach(lock) → Handler → Broadcast(lock)
   - 해결: std::recursive_mutex 사용

3. **브로드캐스트 누락**
   - 증상: 플레이어 퇴장 시 다른 클라이언트에 반영 안 됨
   - 원인: SC_CHAR_LEAVE 패킷 전송 누락
   - 해결: 상태 변경 시 브로드캐스트 체크리스트 추가

**교훈:**
> AI는 일반적 지침("분석하라")보다 구체적 체크리스트에 더 잘 따른다.

### AI 활용자가 배울 점

**나쁜 예:**
```
"비동기 코드 작성 시 주의해"
```

**좋은 예:**
```
"비동기 코드 작성 전 확인:
1. 버퍼 소유권은 누가 관리하는가?
2. 콜백 내에서 락을 다시 잡는가?
3. 콜백 실행 시 객체가 살아있는가?"
```

---

## 3. "문제 해결" → "근본 원인 우선"

### v2.0의 접근

```markdown
### When Encountering Issues

"I found [issue]. Let me analyze:
- Root cause: [analysis]
- Proposed fix: [solution]"
```

### v5.0에서 추가된 것

```markdown
### 에러 발생 시 즉시 수행

1. **에러 로그 전문 확인** (추측하지 말 것)
2. **근본 원인 질문**: "왜 이 에러가 발생하는가?"
3. **영향 범위 파악**: "이 문제가 다른 곳에도 영향을 주는가?"
4. **해결책 제시 전 원인 설명**: 사용자에게 원인 먼저 설명
```

### 왜 바뀌어야 했는가?

**Mickey 7의 실패:**
- 문제: vcpkg tar 추출 오류
- 첫 시도: 캐시 삭제 → 실패
- 두 번째 시도: vcpkg 업데이트 → 실패
- 세 번째 시도: 에러 로그 분석 → CMake가 gzip을 bzip2로 풀려고 함 (버그)
- 해결: WSL tar 사용하도록 스크립트 수정

**교훈:**
> AI는 빠른 해결을 선호하지만, 근본 원인을 놓치기 쉽다.

### AI 활용자가 배울 점

```
AI: "캐시를 삭제하면 해결됩니다"
당신: "왜 캐시 문제라고 생각해? 에러 로그를 다시 분석해줘"
```

---

## 4. "지식 관리" → "실패 경험 체계화"

### v2.0의 접근

```
common_knowledge/: 재사용 가능한 지식 저장
context_rule/: 프로젝트 컨텍스트 저장
```

### v5.0에서 추가된 것

```markdown
# context_rule/mickey-agent-improvements-m8.md

### Lesson 12: 비동기 버퍼 소유권
- **문제**: 외부에서 버퍼 수정 시 동기화 실패
- **원인**: ParsePacket이 length를 참조로 받아 수정
- **해결**: Session 내부에서 버퍼 관리
- **교훈**: 버퍼 관리는 한 곳에서만

### Lesson 13: 콜백 내 락 주의
- **문제**: ForEach(lock) → Handler → Broadcast(lock) = 데드락
- **해결**: std::recursive_mutex 사용
- **교훈**: 콜백 패턴에서 중첩 락 가능성 항상 고려
```

### 왜 바뀌어야 했는가?

- v2.0: "무엇을 했는지" 기록
- v5.0: "무엇을 하지 말아야 하는지" 기록

**교훈:**
> 실패 경험을 체계화하면 같은 실수를 반복하지 않는다.

### AI 활용자가 배울 점

세션 종료 시 실패 경험을 다음 형식으로 기록:

```markdown
### Lesson N: [주제]
- **문제**: [무엇이 잘못되었는가]
- **원인**: [왜 잘못되었는가]
- **해결**: [어떻게 해결했는가]
- **교훈**: [다음에 무엇을 피해야 하는가]
```

---

## 5. "세션 연속성" → "자동화된 프로토콜"

### v2.0의 접근

```
세션 종료 시:
1. 세션 로그 작성
2. 핸드오프 문서 생성
3. context_rule 업데이트
```

### v5.0에서 추가된 것

```markdown
## SESSION END PROTOCOL

### When user says "세션 정리" or similar:

Automatically perform these steps:
1. Update MICKEY-N-SESSION.md with all completed work
2. Create MICKEY-N-HANDOFF.md for next Mickey
3. Update context_rule/ if new lessons learned
4. Update system prompt if new patterns discovered

No need for user to explain - just do it.
```

### 왜 바뀌어야 했는가?

- v2.0: 매번 "세션 로그 작성해", "핸드오프 만들어" 지시
- v5.0: "세션 정리"라고 하면 자동으로 모든 작업 수행

**교훈:**
> 반복되는 패턴은 프롬프트에 자동화로 넣어야 한다.

### AI 활용자가 배울 점

자주 반복하는 지시가 있다면 프롬프트에 추가:

```markdown
### When user says "[트리거 문구]":

Automatically perform:
1. [작업 1]
2. [작업 2]
3. [작업 3]
```

---

## REMEMBER 섹션 비교

### v2.0 (6개 원칙)

```
1. Session log FIRST, then work
2. Analysis BEFORE implementation
3. User confirmation BEFORE changes
4. Root cause OVER quick fixes
5. Documentation ALWAYS
6. Context window MONITOR constantly
```

### v5.0 (18개 원칙)

```
1. 목적 우선: 작업 전 최종 목적 명확화
2. 단순함 우선: 복잡한 솔루션보다 단순한 대안 먼저
3. Session log FIRST, then work
4. Analysis BEFORE implementation
5. 에러 로그 즉시 확인 (추측하지 말 것)
6. 빌드 시스템 확인 후 수정
7. User confirmation BEFORE changes
8. Root cause OVER quick fixes
9. 복잡도 과도 시 대안 제안
10. Documentation ALWAYS
11. Context window MONITOR constantly
12. 비동기 버퍼 소유권: 버퍼 관리는 한 곳에서만
13. 콜백 내 락 주의: recursive_mutex 필요 여부 확인
14. 멀티플레이어 브로드캐스트: 상태 변경 시 다른 클라이언트 고려
15. Windows 빌드 전 프로세스 확인: 실행 중인 exe는 덮어쓰기 불가
16. MSVC 한글 주석 금지: UTF-8 한글이 C4819 오류 유발
17. JSON 스키마 타입 일치: 파서가 기대하는 타입과 JSON 값 타입 확인
18. 구조체 vs 실제 전송: 정의된 구조체와 실제 전송 데이터가 다를 수 있음
```

---

## 메타 인사이트: 프롬프트 진화의 법칙

### 1. 프롬프트는 "한 번 작성하고 끝"이 아니다

```
v2.0: 6개 원칙
  ↓ (Mickey 7-9 실패)
v5.0: 18개 원칙 + 7개 체크리스트
```

### 2. 실패 경험이 프롬프트 개선의 원동력

| Mickey | 실패 | 추가된 원칙/체크리스트 |
|--------|------|----------------------|
| 7 | 목적 상실, 복잡도 과다 | 목적 우선, 단순함 우선, 도구 선택 체크리스트 |
| 8 | 버퍼 소유권, 데드락, 브로드캐스트 | 비동기 체크리스트, 멀티플레이어 체크리스트 |
| 9 | MSVC 한글, JSON 타입 | MSVC 주의사항, JSON 스키마 확인 |

### 3. 추상화 수준의 진화

```
일반적 지침  →  구체적 체크리스트  →  자동화된 프로토콜
"분석하라"  →  "버퍼 소유권 확인"  →  "세션 정리 시 자동 수행"
```

---

## 다음 단계

- [패킷 캡처 에이전트 케이스 스터디](case-study/packet-capture-agent.md) - 실제 프로젝트 적용 사례
- [시스템 프롬프트 v5.0](../examples/ai-developer-mickey.json) - 전체 프롬프트 확인
- [Mickey 7-12 세션 로그](../sessions/packet-capture/) - 실제 작업 기록

---

**핵심 메시지:**
> AI 프롬프트는 "작성"하는 것이 아니라 "진화"시키는 것이다.
> 실패 경험이 프롬프트 개선의 원동력이다.
