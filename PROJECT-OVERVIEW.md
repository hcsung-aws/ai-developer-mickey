# Project Overview

## Project Name
AI Developer Mickey

## Goal
생성형 AI 어시스턴트(Kiro)를 효과적으로 활용하기 위한 실전 가이드 및 에이전트 시스템 개발/개선

## Scope
- Mickey 에이전트 프롬프트 (CLI용 JSON, IDE용 Power)
- 교육용 문서 (가이드, 케이스 스터디)
- 세션 관리 시스템 (로그, 핸드오프, 지식 관리)

## Constraints
- Kiro IDE Power의 hook 제약: userTriggered는 askAgent만 지원
- Windows memorygraph hang 버그: project 파라미터 필수
- Context window 효율성 중시

## Success Criteria
- Power Mickey가 Kiro IDE에서 안정적으로 동작
- 세션 시작 시 context window 소모 최소화
- 점진적 개선 루프 (교훈 축적 → 다음 세션 반영) 유지

## Current Status
- CLI 에이전트: v6.1 안정
- Power Mickey: 실전 테스트 기반 수정 완료 + 하이브리드 context loading 도입

## Last Updated
2026-02-19
