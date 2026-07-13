# 지식 파일 본문 관계 명시 표준화 (`## Related` + INDEX 동기화)

> Source: ai-developer-mickey Mickey 34 (2026-07-02)

## Core
프로젝트 지식 파일(common_knowledge/, context_rule/, auto_notes/) 안에서 다른 지식(특히 글로벌 domain entry)과의 관계를 표현할 때는 **파일 본문 `## Related` 섹션에 명시** + **INDEX.md Domain Links 표에도 동시 등록** 원칙을 준수한다. 두 위치가 어긋나면 도구/에이전트가 관계를 놓친다.

## Decision Context
Mickey 34 (2026-07-02) — 프로젝트 지식 그래프 시각화 도구 구축 중 발견. `common_knowledge/*.md` 본문에는 `## Related` 섹션이나 "교차 참조" 문구로 글로벌 domain entry 참조가 있지만(9건), `common_knowledge/INDEX.md` Domain Links 표에는 6건만 등록되어 있어 3파일의 7건이 out-of-sync. INDEX 만 파싱하는 도구는 실제 관계의 절반을 놓친다.

## Tags
knowledge-management, related-section, index-sync, domain-links, project-knowledge, out-of-sync, cross-scope, backlink, passive-discovery

## Related
- `~/.kiro/mickey/domain/entries/passive-over-active-retrieval.md` — 파일 본문에 backlink 를 삽입하여 자연 발견 유도. `## Related` 는 그 실행 형식
- `~/.kiro/mickey/domain/entries/sot-deduplication-by-reference.md` — 관계 정보의 SoT 는 파일 본문에 두되 INDEX 는 참조. 두 위치를 SoT 로 두면 동기화 실패

## Content

### 표준 형식

```markdown
# 문서 제목

## Core
한 줄 요약 (INDEX Domain Links 힌트로도 사용)

## Tags
kebab-case-tag, another-tag, ...

## Related
- `~/.kiro/mickey/domain/entries/foo.md` — 이 문서와의 관련성 짧은 설명
- `~/.kiro/mickey/domain/entries/bar.md` — 다른 관련성

## Content
본문 상세 ...
```

### 관계 명시 위치 (2곳 동시 갱신)

1. **파일 본문 `## Related` 섹션** (SoT)
   - 관련 글로벌 domain entry 를 리스트 항목으로 명시
   - 각 항목에 관련성 짧은 설명 (호버/독자 판단용)
   - "교차 참조" 문구는 legacy 표기. 신규 파일은 `## Related` 섹션 사용
2. **`common_knowledge/INDEX.md` Domain Links 표** (탐색 진입점)
   - 트리거 키워드 → 글로벌 entry 경로 → 힌트 3컬럼
   - 힌트는 본문 `## Related` 의 관련성 설명과 일치 또는 요약
   - 지식 지도 로딩 시 T3a 에서 이 표만 로딩하여 관계 조회 가능

### 갱신 트리거

프로젝트 지식 파일 추가/수정 시 아래 상황에서 두 위치 동시 갱신:
- 새 지식 파일 생성 (Curator staging → 정식 위치 이동 시)
- 기존 지식 파일에 신규 domain entry 참조 추가
- 글로벌 domain entry 가 renamed/graduated 되어 참조 갱신 필요

### 자동 검증

시각화 도구(`scripts/mickey_graph_viz.py --scope project`) 가 `## Related` 를 본문에서 파싱하고 INDEX Domain Links 와 비교하여 out-of-sync 항목을 WARNING 로그로 출력. 세션 시작 엔트로피 체크 시 이 명령 실행 후보.

### Anti-pattern

- 관계를 INDEX 표에만 두고 본문에 명시 안 함 → 파일을 여는 사용자/에이전트가 관계를 모름
- 관계를 본문에만 두고 INDEX 미갱신 → 지식 지도 로딩 시 노출 안 됨 (Passive 발견 실패)
- "교차 참조: <경로>" 자유 문구만 사용 → 도구가 파싱하기 어려움. `## Related` 섹션으로 통일

## Last Updated
2026-07-02 (Mickey 34)
