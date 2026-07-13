"""Mickey 지식 그래프 시각화 도구.

이 패키지는 md 기반 지식 그래프(GRAPH.md, INDEX.md)를 파싱하여
브라우저에서 상호작용 가능한 self-contained HTML 로 렌더링한다.

레이어 분리:
- models: 도메인 타입 (외부 의존성 없음)
- parser: md 표 → 도메인 객체 변환
- graph_builder: scope 별 그래프 구성 (글로벌/프로젝트)
- renderer: HTML 템플릿 + vendor JS 인라인 삽입
"""
