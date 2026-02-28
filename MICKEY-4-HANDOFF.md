# Mickey 4 Handoff

## Current Status
- **완료**: Claude Code Auto Memory 기능 조사 및 Mickey와 비교 분석
- **완료**: 6개 개선 항목 상세 분석 (항목별 실현 가능성/방법/대안 검토, 사용자 확인)
- **완료**: v6.3 개선 계획 문서 작성 (IMPROVEMENT-PLAN-v6.3.md)
- **완료**: README 업데이트 + git push (before 스냅샷 확보)

## Immediate Next Steps
1. **Phase 1**: 시스템 프롬프트 v6.3 작성 (IMPROVEMENT-PLAN-v6.3.md의 1-1~1-5 항목 기반)
2. **Phase 2**: auto_notes/ 디렉토리 + 초기 파일 생성, 기존 파일 크기 점검
3. **Phase 3**: 실전 테스트 + 반복 개선
4. 이 프로젝트 자체에 PURPOSE-SCENARIO.md 생성 (Mickey 3부터 이월)

## Important Context
- v6.3 개선 6개 항목 모두 사용자 승인 완료. 각 항목의 최종 결정:
  - #1 auto_notes/: 자동 기록 + **세션 종료 시 일괄 확인** + 크기 초과 시 축약/세분화
  - #2 크기 제한: **줄 수 + 항목 수 이중 가드** (T2 각 50줄, project-context 80줄, T3a 각 50줄)
  - #3 트리거: "30분마다" 폐기 → **작업 단위 기반만** (턴 폴백은 문제 발생 시 추후)
  - #4 경로 트리거: **INDEX 포맷 확장만** (별도 시스템 없음)
  - #5 교훈 승격: **"교훈 승격" 키워드** 세션 중 트리거 + 기존 세션 종료 프로토콜 유지
  - #6 HANDOFF: **1~2줄 요약 + Important Context + 참조** (완전 제거 아님)
- 시스템 프롬프트 변경 시 3곳 동기화 필수 (활성 agent JSON, repo JSON, 독립 md)
- before 스냅샷: commit c76dbcd

## Quick Reference
- 개선 계획: IMPROVEMENT-PLAN-v6.3.md
- 세션 로그: MICKEY-4-SESSION.md
- Context window: 양호
