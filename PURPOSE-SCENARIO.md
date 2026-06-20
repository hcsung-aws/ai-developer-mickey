# PURPOSE-SCENARIO

## Ultimate Purpose

Mickey와 함께 탐색·분석·해결·개선하는 과정에서 누적되는 사용자의 결정/판단/도메인 경험을, **3-Tier(R/G/S) 진화 루프**로 점진적으로 구조화하여 다음 세션·다음 프로젝트에서 자동 적용되도록 한다. 이 과정 자체가 "AI를 잘 사용하는 법"의 실전 가이드가 된다.

핵심: Kiro CLI/IDE 생태계 안에서, **세션 연속성 + 점진적 개선 + 도메인 지식 자기 강화**의 세 축으로 AI 개발을 효율화한다. 사용자가 같은 판단을 반복하지 않도록, 최종 활용 단계(REMEMBER, Skill, 글로벌 domain)에서는 자동으로 적용된다.

### 3-Tier 진화 루프
- **R (Rule)** — 판단/추론 방식. T1 REMEMBER + T1.5 핵심
- **G (Knowledge)** — 작업 중 알게 된 사실/구조/패턴. `auto_notes/` (입구) → 글로벌 `~/.kiro/mickey/domain/` (본체) + `GRAPH.md` backlink
- **S (Skill)** — R+G를 활용한 동작 절차. `~/.kiro/skills/` 또는 프로젝트 `.kiro/skills/`

### 진화 메커니즘 (Knowledge Curator + Pre-staged Apply)
세션 종료 시 또는 5/5 체크포인트 도달 시 Knowledge Curator subagent가 자동 호출되어:
1. 직접 수정 영역 (글로벌 `domain/`, `adaptive.md`) 은 Curator가 즉시 적용 (보정된 권한)
2. 제안 영역 (common_knowledge/, context_rule/, REMEMBER 후보) 은 staging 디렉토리에 초안 작성 → 사용자 단일 응답("전체"/번호/"없음"/"보류")으로 일괄 결정

## Usage Scenarios

1. **소프트웨어 개발 / 인프라 운영 / 일반 작업**: 세션 진행 중 결정·학습이 `auto_notes/`에 누적 → Curator가 R/G/S로 분기 판단 → 일반화 가능 지식은 글로벌 `domain/`으로 승격 → 다른 프로젝트에서 backlink로 자연 발견 + 직접 확장
2. **Mickey 자체 개선**: AI 기술 발전 + 외부 트렌드 + 다른 프로젝트의 활용 패턴 → 본 진화 루프 자체에 반영 (포스트모템 + ADDENDUM 형태 의사결정 이력 추적)

## Acceptance Criteria

"충분"은 없음. 진화 루프의 **건강 지표**를 정량 측정한다.
- 측정 대상: 글로벌 domain 참조 / Curator 호출 / auto_notes 참조 / [Protocol] 태그 (세션당 평균)
- baseline + 임계값 + 측정 방법: T1.5 §18 (Activity Metrics) 참조
- 임계값 위반 시: 포스트모템 트리거 + 진단 보정 (M20→M21 패턴 참조)

## Last Confirmed
2026-06-20 (Mickey 22)

## Last Updated
2026-06-20
