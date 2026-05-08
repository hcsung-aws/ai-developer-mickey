# Mickey 16 Session Log

## Checkpoint [0/5]

## Session Meta
- Type: Self-Improvement
- Mickey: 16
- Date: 2026-05-08

## Session Goal
Knowledge Curator를 전체 지식 관리자로 확장 재설계 + T1 프로토콜 수정 + E2E 검증

## Purpose Alignment
- 기여 시나리오: Mickey 자체 개선 (PURPOSE-SCENARIO "Mickey 자체 개선" 시나리오)
- 이번 세션 범위: Phase 3 검증 실패 분석 → Curator 역할 확장 → 프로토콜 수정 → E2E 테스트

## Previous Context
- Mickey 15: Knowledge Curator + domain/ 구조 구축 완료 (Phase 1~3). 비정상 종료.
- 문제 발견: 6개 프로젝트에서 Curator 호출 0회, adaptive.md 생성 0건, domain/ 갱신 0회
- 근본 원인: "세션 중 자동 호출"은 판단 병목 + 실행 마찰로 동작 불가

## Current Tasks
- [ ] MICKEY-16-SESSION.md 생성 | CC: 파일 존재
- [ ] Knowledge Curator 프롬프트 확장 | CC: domain + adaptive + common_knowledge + context_rule + patterns/REMEMBER 제안 포함
- [ ] knowledge-curator.json 업데이트 | CC: 확장 프롬프트 반영, JSON 유효
- [ ] T1 프로토콜 수정 | CC: During Session Curator 호출 제거, Session End에 통합
- [ ] E2E 시뮬레이션 테스트 | CC: skr M36~37 맥락으로 Curator 호출, 의미 있는 출력 생성
- [ ] examples/ai-developer-mickey.json 동기화 | CC: 활성 JSON과 일치

## Progress

### Completed
1. **문제 분석**: 6개 프로젝트 세션 로그 조사 → Curator 호출 0회, adaptive.md 생성 0건, domain/ 미갱신 확인
2. **근본 원인 식별**: 판단 병목 (auto_notes만 동작하는 이유: 판단 불필요), 세션 중 호출 실패 증명
3. **해결 방향 합의**: Curator를 전체 지식 관리자로 확장, 세션 종료 배치로 전환
4. **Curator 프롬프트 확장**: domain/ + adaptive.md 직접 수정, common_knowledge/context_rule/patterns/REMEMBER 제안 구조
5. **T1 프로토콜 수정 (v14→v15)**: During Session Curator 호출 제거, Session End 6단계로 통합
6. **E2E 시뮬레이션 성공**: skr M36-37 맥락으로 Curator 호출 → entry 1건 신규 + 1건 보강, GRAPH 갱신, adaptive 규칙 2건 추가
7. **3곳 동기화**: 활성 agent JSON + repo examples JSON + CURATOR-PROMPT.md
8. **Domain Backlink 메커니즘 추가**: Curator가 domain 저장 시 프로젝트 INDEX에 역방향 링크 삽입
9. **GRAPH.md Core 강화**: "언제 쓰는가" 힌트 포함 (6개 노드 모두)
10. **T1 domain/ 참조 방식 변경**: active 검색 → passive 발견 (GRAPH Core + 프로젝트 Domain Links)
11. **DECISIONS.md 기록**: 검증 시점 2026-06-08 명시

## Key Decisions
- D: "세션 중 Curator 자동 호출" 제거 → 세션 종료 1회 배치로 전환 (6개 프로젝트에서 실패 증명)
- D: Curator 범위 확장 (domain/ only → adaptive + common_knowledge + context_rule + domain + 승격 제안)
- D: 권한 모델 — domain/+adaptive.md는 직접 수정, 나머지는 제안만 (사용자 확인 필요)
- D: Domain Backlink — domain entry 저장 시 프로젝트 INDEX에 역방향 링크 삽입 (passive 활용 경로)
- D: adaptive.md 역할 재정의 — "모든 행동 참조" → "승격 스테이징 영역"
- D: GRAPH.md Core 강화 — "언제 쓰는가" 힌트 포함하여 passive 리마인더 효과 극대화
- **검증 시점**: 2026-06-08 (1개월 후) — 3개+ 프로젝트에서 Curator 호출 + Backlink 참조 사례 확인

## Files Modified
- mickey/domain/CURATOR-PROMPT.md (전면 재작성)
- examples/knowledge-curator.json (프롬프트 확장 반영)
- examples/ai-developer-mickey.json (v15 동기화)
- ~/.kiro/agents/ai-developer-mickey.json (v14→v15)
- ~/.kiro/agents/knowledge-curator.json (확장 프롬프트)
- ~/.kiro/mickey/domain/GRAPH.md (E2E 테스트로 노드/엣지 추가)
- ~/.kiro/mickey/domain/INDEX.md (트리거 추가)
- ~/.kiro/mickey/domain/entries/script-to-library-extraction.md (신규)
- ~/.kiro/mickey/domain/entries/welc-test-harness.md (Evidence 보강)
- skr-reverse-poc/context_rule/adaptive.md (규칙 2건 추가)

## Lessons Learned
- [Protocol] "세션 중 자동 호출" 패턴은 구조적으로 실패한다. 판단 + 다단계 실행이 필요한 작업은 자연스러운 중단점(세션 종료)에 배치해야 동작함
- [Protocol] TMI-agent와 Knowledge Curator가 동일한 실패 패턴 — "프롬프트에 적혀 있지만 실행되지 않는" 문제의 해결책은 실행 시점을 강제 중단점으로 이동하는 것

## Context Window Status
~35%

## Next Steps
- 다음 실제 프로젝트 세션에서 세션 종료 시 Curator 호출 검증 (Phase 4)
- install.sh 갱신 (확장된 CURATOR-PROMPT.md 배포 경로 확인)
