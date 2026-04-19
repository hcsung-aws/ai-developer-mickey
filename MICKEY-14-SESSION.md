# Mickey 14 Session Log

## Checkpoint [5/5]

## Session Meta
- Type: Self-Improvement
- Date: 2026-04-18

## Session Goal
v10 실전 검증 → 프로토콜 개선 + Personal Knowledge Graph 설계

## Purpose Alignment
- 기여 시나리오: Mickey 자체 개선 (PURPOSE-SCENARIO "Mickey 자체 개선" 시나리오)
- 이번 세션 범위: v10 기능 검증 + Checkpoint 카운터 도입 + 프로젝트 간 지식 단절 해소 설계

## Previous Context
- Mickey 13: v10 구현 완료 (중간 체크포인트 + Soft Restart). 실전 검증 미완료.

## Current Tasks
- [x] v10 실전 검증: skr-reverse-poc + packet-capture-log-agent 세션 로그 분석 | CC: 체크포인트/soft restart 발동 여부 + 전후 비교 데이터 확보
- [x] 분석 결과 기반 프로토콜 개선: Checkpoint 카운터 도입 + Soft Restart 제거 | CC: T1 v12 + T1.5 v13 + 3곳 동기화
- [x] Personal Knowledge Graph 방향성 논의 + IMPROVEMENT-PLAN 작성 | CC: 저장소 비교(최소/최대) + Phase 1~3 계획 + 열린 질문 정리
- [x] Phase 1 실행: T1 v13 (vault 검색 규칙 + MCP 설정) + vault 초기 구조 생성 | CC: T1 v13 + 3곳 동기화 + vault 디렉토리 + INDEX.md
- [x] Phase 2 실행: MCP 설치 + vault 초기 데이터 10개 노트 생성 | CC: pip install 완료 + vault 경로 설정 + 10개 노트(3 tech, 3 pattern, 2 lesson, 1 decision, 1 INDEX)
- [x] 방향 전환: Obsidian 한계 발견 → 기존 지식 구조화 확장 전략으로 전환 | CC: 현재 구조 분석 + Gap 5개 식별 + 3단계 진행 계획 수립

## Progress

### Completed
1. **v10 실전 검증**:
   - 분석 범위: skr-reverse-poc M29~M36 (8세션), packet-capture-log-agent M24~M28 (5세션)
   - 결과: 중간 체크포인트 발동 0건, soft restart 언급 0건 (세션 로그 기준)
   - 사용자 피드백: soft restart는 실제 사용했으나 /clear 후 흔적 소실. 50% 종료는 사용자의 의식적 판단.
   - 근본 원인: 프로토콜이 자기 실행되지 않음 — 구현 몰입 시 메타 프로토콜에 주의가 가지 않음
   - M31(skr)은 15개 작업 완료에도 체크포인트 미발동 — 가장 명확한 증거

2. **프로토콜 개선 (Checkpoint 카운터)**:
   - 핵심: "이미 하는 행동(세션 로그 쓰기)에 최소 부하만 얹기"
   - T1 v11→v12: SESSION 스키마에 `Checkpoint [0/5]` 추가, 세션 로그 트리거에 카운터 +1 결합
   - T1.5 v12→v13: §14 Soft Restart 전체 제거 (카운터에 흡수), 번호 재조정
   - 3곳 동기화 완료 (해시 일치 확인)

3. **Personal Knowledge Graph 설계**:
   - 논의 과정: Karpathy LLM Wiki 분석 → 사용자 요구와의 차이 식별 → 방향성 수렴
   - 핵심 요구: 프로젝트 간 도메인 지식 단절 해소, 연관관계 기반 검색, 클라우드 범용성, 개인화
   - 기존 INDEX 구조와 병렬로 동작하는 별도 채널 (확장이 아님)
   - 저장소 비교: Obsidian+MCP(무료, 경량) vs Neptune Analytics(월$70+, 진정한 그래프 쿼리)
   - 결정: Obsidian으로 시작, 한계 발견 시 Neptune 전환
   - Obsidian MCP 조사: bbdaniels/obsidian-mcp-server (Python, search/read/write, Obsidian 앱 불필요)
   - IMPROVEMENT-PLAN-v8.1.md 작성 완료

## Key Decisions
- Checkpoint 카운터: 세션 로그 트리거에 편승 (A+C 방안). Soft Restart 독립 프로토콜 제거.
- Personal Knowledge Graph: Obsidian+MCP로 시작했으나, Obsidian의 그래프가 자동 연관관계 발견이 아닌 수동 [[wikilinks]] 시각화에 불과함을 확인 → 기존 지식 구조화 확장 전략으로 전환. Obsidian MCP 비활성화.
- 검색 규칙: T1 v13에 추가했으나, Obsidian MCP 비활성화로 현재 미동작. 지식 확장 전략 확정 후 재설계 예정.

## Files Modified
- examples/ai-developer-mickey.json (v11→v12)
- mickey/extended-protocols.md (v12→v13)
- ~/.kiro/agents/ai-developer-mickey.json (동기화)
- ~/.kiro/mickey/extended-protocols.md (동기화)
- IMPROVEMENT-PLAN-v8.1.md (신규)
- ~/.kiro/mickey/vault/INDEX.md (신규)
- ~/.kiro/mickey/vault/ 디렉토리 구조 (technologies/, patterns/, lessons/, decisions/)

## Lessons Learned
- [Protocol] "자기 실행 안 되는 프로토콜"을 고치려고 프로토콜을 더 추가하면 같은 문제 반복. 이미 실행되는 행동에 편승하는 것이 유일한 해법.
- [Protocol] /clear 기반 soft restart는 세션 로그에 흔적이 남지 않아 사후 검증 불가 — "부재 증거"와 "미실행"을 구분해야 함.
- Graph가 RAG보다 적합한 용도: "이 개념과 연결된 다른 개념/교훈/결정을 찾아라"는 관계 탐색이 본질. 텍스트 유사도(RAG)로는 구조적 관계를 잡기 어려움.

## Context Window Status
~45%

## Context Window Status
~50%

## Next Steps
- 지식 구조화 확장 2단계: 강한 연관관계 설정 방법 설계 (Obsidian [[wikilinks]] 개념을 기존 INDEX 체계에 적용)
- 지식 구조화 확장 3단계: 확장 전략 결정 + 실행 (domain/ 활성화, 프로젝트 간 지식 공유, 개인 도메인 지식 포함)
- Checkpoint 카운터 실전 검증 (다른 프로젝트에서)
- PROJECT-OVERVIEW.md 갱신
