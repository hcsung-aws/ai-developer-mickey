# Mickey 15 Session Log

## Checkpoint [0/5]

## Session Meta
- Type: Self-Improvement
- Date: 2026-04-19

## Session Goal
도메인 지식 저장소 설계 확정 + PROFILE.md 초안 작성 + 구현 계획 수립

## Purpose Alignment
- 기여 시나리오: Mickey 자체 개선 (PURPOSE-SCENARIO "Mickey 자체 개선" 시나리오)
- 이번 세션 범위: domain/ 확장 전략의 "어떻게"와 "언제"를 구체화하여 실행 가능한 설계로 확정

## Previous Context
- Mickey 14: 지식 구조화 확장 1단계 완료 (Gap 5개 식별), Obsidian→기존 체계 확장으로 전환
- 남은 작업: 2단계(강한 연관관계 설정) → 3단계(확장 전략 결정+실행)

## Current Tasks
- [x] 결정 이력 수집 (이 프로젝트 + 다른 Mickey 프로젝트) | CC: DECISIONS.md + 세션 분석 파일에서 결정 패턴 추출
- [x] PROFILE.md 초안 작성 | CC: 사용자 성향/결정 기준/관계 선호 반영, 사용자 확인
- [x] 최종 설계 문서 작성 (IMPROVEMENT-PLAN-v8.1.md 재작성) | CC: 사용자 피드백 전부 반영한 확정 설계
- [x] Phase 1 실행: 초기 구조 생성 + 기존 패턴 마이그레이션 | CC: domain/ 구조 + entries/ 5개 + GRAPH.md 5노드5엣지 + INDEX.md 갱신

## Progress

### Completed
1. **설계 논의 + 방향 확정**: "어떻게"(subagent Knowledge Curator + 결정 중심 큐레이션 + PROFILE.md 개인화) + "언제"(세션 로그 트리거에 편승, 항상 per-trigger) 합의
2. **PROFILE.md 초안 작성**: 6개 프로젝트 결정 이력에서 사용자 성향 추출 (점진적 확장, 검증 기반, 계획-실행 균형, 외부 선별 채택, 피드백 루프, 엔트로피 관리)
3. **IMPROVEMENT-PLAN-v8.1.md 전면 재작성**: Obsidian 기반 → 파일 기반 + Subagent + 결정 중심 큐레이션으로 전환

4. **Phase 2: Subagent 프롬프트 + 단독 검증**:
   - CURATOR-PROMPT.md 작성 (3단계: 저장 판단 → 큐레이션 → PROFILE 제안)
   - 테스트 3건 실행: 결정(저장✅), 교훈(저장✅), 커맨드(비저장✅)
   - PROFILE 참조 확인: Decision Style/Relationship Preferences가 출력에 반영됨
5. **Knowledge Curator agent 생성 + 설치**:
   - examples/knowledge-curator.json 생성 (전용 agent — 자체적으로 GRAPH.md/PROFILE.md 읽기)
   - install.sh 갱신 (knowledge-curator.json 배포 + domain/entries/ 디렉토리 포함)
   - 로컬 설치 완료: ~/.kiro/agents/knowledge-curator.json + ~/.kiro/mickey/domain/ 전체 동기화
   - 제약: 현재 세션에서는 agent 미인식 (세션 시작 시 로딩). 다음 세션에서 delegate 호출 검증 필요

## Key Decisions
- domain/ 크기 제한 없음. O(1) 접근을 위한 구조화(GRAPH.md 100줄 기준 + 1~2홉 링크)로 해결
- subagent 호출: 동기(use_subagent)로 시작, 안정화 후 delegate(비동기)로 전환
- subagent 호출은 안정화 후에도 트리거마다 유지. 사람 확인만 점진적 감소
- 지식 저장 기준: 사용자의 '결정'과 '성향' 중심. 단순 사실이 아닌 결정 맥락 + 성향 정합성
- patterns/(핵심 원칙, 상한 7개)와 domain/(실전 지식, 제한 없음) 병행. 추상도의 차이
- 인터페이스 독립: domain/ 정규 형식이 source of truth. 외부 도구는 입출력 어댑터. 출력은 당장 Mermaid
- Mickey 역할 한정: 맥락 전달 + 결과 안내만. 저장 판단/큐레이션/관계 설정은 모두 subagent

## Files Modified
- MICKEY-15-SESSION.md (신규)
- mickey/domain/PROFILE.md (신규)
- mickey/domain/GRAPH.md (신규)
- mickey/domain/INDEX.md (갱신)
- mickey/domain/CURATOR-PROMPT.md (신규)
- mickey/domain/entries/ (5개 entry 신규)
- examples/knowledge-curator.json (신규)
- install.sh (갱신)
- IMPROVEMENT-PLAN-v8.1.md (전면 재작성)
- ~/.kiro/agents/knowledge-curator.json (설치)
- ~/.kiro/mickey/domain/ (동기화)

## Lessons Learned
- [Protocol] knowledge-curator.json에 `customInstructions` 필드 사용 불가 — kiro-cli가 인식하지 못하는 필드. 유효 필드 목록: $schema, name, description, prompt, mcpServers, tools, toolAliases, allowedTools, resources, hooks, toolsSettings, includeMcpJson, useLegacyMcpJson, model, keyboardShortcut, welcomeMessage
- [Protocol] PowerShell에서 Get-Content + IndexOf + Substring 패턴 반복 사용 시 CrowdStrike가 의심스러운 동작으로 탐지하여 프로세스 종료 가능. JSON 파일 수정은 파일 편집 도구 사용 권장

## Context Window Status
~25% (비정상 종료)

## Next Steps
- Phase 3 마무리: T1 v14 동기화 완료 확인 (다음 세션에서 검증)
- Phase 4: 다른 프로젝트에서 E2E 동작 확인 (Knowledge Curator delegate 호출 → 저장 → 알림)
