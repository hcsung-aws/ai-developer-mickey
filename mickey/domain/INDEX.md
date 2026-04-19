# Global Domain Knowledge INDEX

> 프로젝트에서 승격된 도메인 지식. "다른 프로젝트에서 같은 기술/도구를 쓸 때 참고할 가치가 있는가?"가 승격 기준.
> 관계 맵: GRAPH.md 참조. 상세: entries/ 참조.

## Domain Map

| 트리거 | 파일 | 요약 |
|--------|------|------|
| phase 분해, 점진적, 로드맵, 단계별 | entries/phase-based-decomposition.md | Phase→Step 분해 + E2E 검증 후 진행 |
| WELC, test harness, characterization test, 리팩토링 안전 | entries/welc-test-harness.md | 수정 전 기존 동작을 테스트로 캡처 |
| 계획 문서, IMPROVEMENT-PLAN, 판단 비용, 실행 속도 | entries/plan-before-execute.md | 상세 계획 선행 → 구현 시 판단 제거 |
| 벤치마킹, 외부 기술, 선별 채택, gap 분석 | entries/external-benchmarking.md | 외부 기술을 자기 맥락에서 재해석 |
| 검증 도구, 동시 발전, coevolution, 테스트 대상 | entries/tool-and-target-coevolution.md | 대상과 도구를 함께 개선하여 검증 범위 확장 |

## 접근 경로
1. 주 경로: GRAPH.md Tags/Title 스캔 → Core로 즉시 판단 → entries/ 상세 (1홉)
2. 관계 탐색: entry의 Links → 연결 entry (2홉)
3. 트리거 매칭: 이 INDEX의 트리거 → 해당 entry 직접 로딩

## Last Updated
2026-04-19 (Mickey 15)
