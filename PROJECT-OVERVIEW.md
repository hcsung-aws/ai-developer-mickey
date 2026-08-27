# Project Overview

## Project Name
AI Developer Mickey

## Goal
생성형 AI 어시스턴트(Kiro)를 효과적으로 활용하기 위한 실전 가이드 및 에이전트 시스템 개발/개선

## Scope
- Mickey 에이전트 프롬프트 (CLI용 JSON, IDE용 Power)
- Knowledge Curator subagent (지식 자동 분기 + Pre-staged Apply)
- 교육용 문서 (가이드, 케이스 스터디, 프롬프트 진화 기록)
- 세션 관리 시스템 (로그, 핸드오프, 엔트로피 처리)
- 글로벌 지식 구조 (`~/.kiro/mickey/` patterns + domain)

## Constraints
- Kiro IDE Power의 hook 제약: userTriggered는 askAgent만 지원
- Windows memorygraph hang 버그: project 파라미터 필수
- Kiro CLI agent 캐시: agent JSON 변경 후 검증은 새 세션 부팅 필요 (M23 발견)
- Context window 효율성 중시 (3-Tier 로딩)

## Success Criteria
- Power Mickey가 Kiro IDE에서 안정적으로 동작
- 세션 시작 시 context window 소모 최소화 (T2 + T3a 인덱스 우선 로딩)
- 점진적 개선 루프 (교훈 축적 → 다음 세션 반영) 유지
- 진화 루프 건강 지표 baseline 유지 (T1.5 §18 Activity Metrics)

## Current Status

### CLI 에이전트 (주 트랙)
- **버전**: T1 v20 (M43) + T1.5 extended-protocols v27 (M44)
- **Curator 운영 강화 3연작 완료 (M41~43)**: 글로벌 쓰기 격리(promote_knowledge.py 전담 + 락) → use_subagent 전송 → 호출 코드화(`invoke_curator.py` 유일 진입점 + curation 락 내장)
- **M45 스로틀 대응**: 간헐 실패 원인 = ModelThrottleError 실측 → invoke 1회 재시도 + attempt별 전문 로그. 신규 경로 검증 3/5회차
- **그래프 건전성**: GRAPH-HEALTH-BASELINE-2026-08-25 동결 + graph_audit.py 상비화(§3-8). 재측정 사이클 대기 — M46 감사에서 불변 조건 유지 + malformed 0 확인

### Power Mickey (v10 트랙)
- v3 런타임 실측 검증 완료 (2026-07-15, V1~V8 전 항목 닫힘). 상세: `IMPROVEMENT-PLAN-v10-power-migration.md` + `docs/09-v3-power-migration.md`
- 잔여: IDE 묶음(최후순위) + M41 격리 구조 steering 개정 (mickey-power 세션 소관), registry stale path

### 엔트로피 관리
- M46: 루트 SESSION M39~45 아카이빙(sessions/) + changelog 백필(v10 이후 CLI 트랙 + 영문 v9.2) + 본 문서 갱신

## Last Updated
2026-08-28 (Mickey 46 — Current Status 압축 갱신: M41~45 Curator 3연작/baseline/스로틀 대응 반영, M22~27 진단 사이클 등 노후 항목 제거)
