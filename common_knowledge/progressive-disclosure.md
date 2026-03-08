# Progressive Disclosure 패턴: INDEX = 목차

## 핵심 원칙

AI에게 필요한 것은 모든 정보가 아니라, 어디에 어떤 정보가 있는지 아는 것.
작은 진입점(INDEX)에서 시작하여 필요할 때만 깊이 탐색한다.

## Mickey INDEX와 Harness AGENTS.md의 비교

| | Mickey INDEX | Harness AGENTS.md |
|---|---|---|
| 구조 | 트리거→파일→요약 | 목차 + docs/ 링크 |
| 갱신 | 수동 | doc-gardening 에이전트 자동 정리 + CI 검증 |
| 범위 | 지식 파일만 | 코드 아키텍처 + 설계 문서 + 실행 계획 전부 |

## 적용 방향

1. **INDEX 범위 확장**: 지식 파일뿐 아니라 프로젝트 핵심 파일(소스, 설정, 테스트)도 트리거로 가리킴
2. **INDEX 자동 갱신**: 세션 시작 시 INDEX 파일 존재 여부 + 트리거 유효성 자동 체크
3. **Verify/Update/Suggest 원칙**: INDEX를 "진실"이 아니라 "탐색의 출발점"으로 취급. 현실과 다르면 즉시 수정

## 출처
- OpenAI Harness Engineering (2026-02)
- Anyline Agents Meta-Repo Pattern (2026-03)
- Mickey v6.1 INDEX 지도 패턴 (2026-02)

## Last Updated
2026-03-08
