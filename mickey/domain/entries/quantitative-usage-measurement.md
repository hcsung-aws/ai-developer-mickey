# 정량 활용도 측정 기반 진단

## Core
프로토콜/도구의 실제 효과를 추측이 아닌 정량 측정(grep, 카운터)으로 판단한다. 0% 활용은 설계 결함의 명확한 신호.

## Decision Context
v8.1 도입 후 "잘 되고 있을 것"이라는 추측을 76세션 grep 측정으로 반증. domain/Curator 자기 개선 외 활용 0%, adaptive.md gamejob 0% 등 정량 데이터가 v9 전면 재설계의 결정적 입력이 됨. 사용자의 "검증 기반 진행" 성향이 포스트모템 수준에서도 적용된 사례.

## Tags
measurement, postmortem, quantitative, verification, protocol-design

## Links
- plan-before-execute | prerequisite | 정량 측정 결과가 다음 계획의 입력이 됨
- tool-and-target-coevolution | similar-to | 측정 도구(grep)와 측정 대상(프로토콜)이 함께 정교화

## Content
- 측정 방법: 세션 로그/파일에서 grep으로 특정 저장소/규칙의 참조 횟수 카운트
- 표본: 프로젝트별 세션 수 × 저장소별 참조 비율 = 활용도 매트릭스
- 판단 기준: 0% = 설계 결함(트리거 미작동 또는 불필요), 5~10% = 개선 여지, 80%+ = 정상
- 적용 시점: 포스트모템, 버전 전환 전 진단, 5/5 카운터 도달 시
- 핵심 교훈: "사용되지 않는 프로토콜은 존재하지 않는 것과 같다" — 추측 대신 실측

## Source
ai-developer-mickey (M20, 2026-05-14)
