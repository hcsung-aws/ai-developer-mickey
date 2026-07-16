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

### CLI 에이전트
- **버전**: v9.1 (Curator 권한 보정 + Pre-staged Apply + T1.5 §17 Knowledge Lifecycle + §18 Activity Metrics)
- **베이스라인**: M21 5주 31세션 측정 (글로벌 domain 참조 2.45/세션, Curator 호출 2.65/세션, auto_notes 참조 5.55/세션)

### Knowledge Curator (M22~M27 진단 사이클)
- 운영 패턴 도입 후 EmptyResponse 발생 → M22~M27 6세션 진단 진행 중
- M22: 첫 발견 / M23: agent 캐시 발견 / M24: 변형 A2 / M25: A1 / M26: G3 (누락 키 3개 보충) / M27: **변형 H (전체 차이 흡수, 검증 M28 인계)**
- 진단 메타 교훈: 측정 도구의 정밀도는 반복 깊이 확장이 필요 (M25 9개 → M26 12개+per-key → M27 deep leaf diff)

### Power Mickey (v10 Power Migration 트랙)
- **트랙**: CLI v2 agent → v3 Power 마이그레이션. 계획서 `IMPROVEMENT-PLAN-v10-power-migration.md`, 세션 로그 `session_history/YYYY-MM-DD-*` (CLI Mickey N 트랙과 병행)
- **진행**: Phase 0~5 완료. **v3 런타임 실측 검증 완료 (2026-07-15)** — 계획서 `VERIFICATION-PLAN-v3-power-runtime.md`, 로그 `session_history/2026-07-14-v3-power-runtime-verification.md`. V1~V8 전 항목 닫힘
- **실측된 v3 소비 모델**: ① steering 자동 주입 없음 — always 도 `readSteering` pull 필수 (POWER.md F1 정정·재배포) ② MCP 는 proxy(`kiro_powers use`) 불가, 직접 마운트(`mcp_<서버>_<도구>`)가 정상 경로 (F2 정정) ③ SessionStart hook 은 터미널 v3(`--agent-engine v3`)에서 발화·stdout 주입 확인, acp-client 는 주입 안 됨 ④ Stop 트리거는 per-response 발화 → stop hook 폐기(F5), 세션 마감은 "세션 정리" 수동 경로로 일원화
- **다음**: IDE 묶음(최후순위) — ③ Kiro IDE steering 인식 실측 + IDE `.kiro.hook` 정식 규격 실측. 부채: registry stale path, 영문 changelog v9.2 백필, `mickey/domain/entries` 잔재(계획서 §8-a)
- **검증 기준값**: `verify_power_structure.py` 7/7, `verify_hooks.py` 6/6 (항목 2 는 stop hook **부재** 가드 포함으로 개정됨), `verify_deploy_power.py` 25/25, `verify_serving_sync.py` IN-SYNC
- 구 실험본(Kiro IDE 0.7+)은 `power-mickey.pre-v10-bak.zip` 로 백업

### 엔트로피 관리
- M27 진입 시 SESSION 6건 누적 (M21~M26) → `sessions/` 로 일괄 아카이빙 완료
- 구조 문서 갱신 (PROJECT-OVERVIEW / FILE-STRUCTURE / project-context) M27 에서 일괄 진행

## Last Updated
2026-07-15 (v3 런타임 실측 검증 V1~V8 완료 + F1·F2 문서 정정·재배포 + F5 stop hook 폐기 반영)
