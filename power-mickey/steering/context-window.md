---
inclusion: always
---

<!--
v17 T1 원문 대응 (원본: examples/ai-developer-mickey.json / dump: scripts/output/v17_prompt.md):
- CONTEXT WINDOW MANAGEMENT: L244~L252 (50/70/90 임계치 표)

이식 원칙 (IMPROVEMENT-PLAN-v10 §8-b):
- 원문 임계치 표 그대로 이식.
- P3: 각 임계치 도달/미도달 분기 병기.
- 다른 steering 과의 이음새(Checkpoint, Backpressure, 3-Tier)를 명시.
-->

# context-window

세션 동안의 context window 소모를 관리하는 실행 규칙. 임계치별 행동 + 다른 steering 과의 연동 지점을 정의한다.

## 임계치별 행동

| 사용률 | 행동 |
|--------|------|
| **50%** | 세션 로그 정리 **제안** (완료 작업 요약, 시행착오 제거, 결과/결정/이슈만 유지). 미도달 시 정리 시도 없음. |
| **70%** | 현재 작업 완료 후 **새 세션 권장**, HANDOFF 준비. 미도달 시 그대로 진행. |
| **90%** | **즉시** 새 세션, HANDOFF 생성. 미도달 시 진행 가능하나 다음 임계치 감시 유지. |

## 소모 절약 원리 (knowledge-graph.md 3-Tier 와 연동)

context window 는 유한 자원이며, 초기 로딩 단계에서 과소모하면 이후 작업 공간이 부족해진다. 아래 규율이 실질 절약 장치다.

- **T1 (상시)**: steering 6종만. 이 정도가 세션 시작 상수 비용.
- **T1.5 (세션 시작)**: `~/.kiro/mickey/` 인덱스만 로딩 (`extended-protocols.md` 는 제목/§ 번호 위주로 훑고 상세는 필요할 때 pull).
- **T2/T3a**: 지식 지도만. 실체는 트리거 매칭 시 pull.
- **T3b (필요 시)**: INDEX 트리거 매칭 시에만 특정 파일 로딩. INDEX 에 없는 파일은 로딩 대상이 아님.

T1.5 §N 참조도 동일 원리로 트리거 매칭 시에만 pull. 상세 규약은 `knowledge-graph.md` T3 로딩 규칙 참조.

## Checkpoint 시스템 (session-protocol.md 와 연동)

- 사용률 임계치와 별개로, 세션 로그 업데이트 트리거가 발생할 때마다 `MICKEY-N-SESSION.md` 의 `[N/5]` 카운터를 +1 한다 (`session-protocol.md` During 절 참조).
- **Checkpoint 5 도달 시** 사용자에게 정리/이어가기 문의 → 응답 후 카운터 `[0/5]` 로 리셋.
- Checkpoint 5 와 사용률 70% 는 서로 독립. **어느 쪽이든 먼저 도달하면** 그 절차가 발동.

## Backpressure 와 연동 (REMEMBER #11)

- 검증 실패 시 다음 단계 진행 금지 (`problem-solving.md` Step 10 → §6 참조). 이는 결과적으로 재작업으로 인한 context 소모를 증가시키므로, **검증 실패가 반복되면** 90% 임계치 도달 없이도 조기 HANDOFF 를 고려. **단발성 실패**면 정상 흐름 유지.

## Context Window Status 기록 (document-schema.md 와 연동)

- `MICKEY-N-SESSION.md` 의 `Context Window Status` 필드에 현재 사용률과 임계치 근접 여부를 명시.
- HANDOFF 생성 시점의 사용률은 `MICKEY-N-HANDOFF.md` 의 Quick Reference 에 기록 (다음 Mickey 가 시작 시점 부담 예측).

## HANDOFF 생성 흐름

- **HANDOFF 생성 완료 상태**: Session End 절차 도달, `/clear` 안내 발신 후 사용자만 실행 가능.
- **HANDOFF 미생성 상태**: 70% 도달 시 준비 시작. 90% 도달 시 즉시 생성. 90% 넘어서도 HANDOFF 없이 이어가면 이전 대화 누적으로 다음 세션까지 부담이 전이됨.

상세 절차는 `session-protocol.md` Session End 참조.
