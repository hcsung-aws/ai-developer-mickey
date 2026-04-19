# IMPROVEMENT-PLAN: Domain Knowledge System (v8.1 revised)

## 배경

Mickey는 프로젝트별로 지식을 축적하지만, 프로젝트 간 지식이 단절되어 있다. 현재 글로벌 지식(~/.kiro/mickey/patterns/)은 추상 패턴 5개에 한정되고, domain/은 비어 있다. 구체적인 도메인 지식(기술 선택, 에러 해결, 아키텍처 결정)은 프로젝트 안에 갇혀 있다.

### 핵심 목표

1. **결정 중심 지식 큐레이션**: 단순 사실이 아닌, 사용자의 '결정'과 그 맥락(성향, 근거, 결과)을 중심으로 저장
2. **O(1) 접근**: GRAPH.md → entry(1홉) → 연결 entry(2홉)로 즉시 도달. 크기 제한 없이 구조화로 해결
3. **개인화 진화**: PROFILE.md가 사용자의 성향/결정 방식을 반영하고, 작업마다 진화

### 설계 원칙

1. **결정 중심**: 단순 사실이 아닌, 사용자의 '결정'과 그 맥락(성향, 근거, 결과)을 중심으로 저장
2. **O(1) 접근**: GRAPH.md → entry(1홉) → 연결 entry(2홉). 크기 제한 없이 구조화로 해결
3. **개인화 진화**: PROFILE.md가 사용자의 성향/결정 방식을 반영하고, 작업마다 진화
4. **인터페이스 독립**: domain/의 내부 표현(entries/ + GRAPH.md)이 정규 형식. 외부 도구(Obsidian, Loop, Notion, GraphDB 등)는 입출력 인터페이스에 불과. 어떤 형식의 지식이 들어와도 동일하게 처리하고, 필요 시 어떤 형식으로든 내보낼 수 있는 구조

### patterns/ vs domain/ 관계

| | patterns/ | domain/ |
|--|-----------|---------|
| 성격 | 핵심 원칙 (헌법) | 실전 지식 (판례집) |
| 크기 | 의도적으로 작게 (상한 7개) | 제한 없음, 구조화로 관리 |
| 관계 | 없음 (독립적 원칙) | GRAPH.md로 명시적 관계 |
| 승격 기준 | "완전히 다른 도메인에서도 유효한가?" | "다른 프로젝트에서 참고할 가치가 있는가?" |

동일 주제가 양쪽에 존재할 수 있음 (예: WELC). 이는 중복이 아니라 추상도의 차이 — patterns/는 1줄 원칙, domain/은 맥락+관계 포함 상세.

---

## 설계

### 저장소 구조

```
~/.kiro/mickey/domain/
├── INDEX.md          # T3a 로딩용 트리거→파일 매핑 (기존)
├── PROFILE.md        # 사용자 도메인 프로필 (subagent 참조)
├── GRAPH.md          # 관계 맵 (노드 목록 + 엣지 목록, 상한 200줄)
└── entries/          # 개별 지식 항목
    └── *.md
```

GRAPH.md 분리 기준: **100줄**. 초과 시 카테고리별 서브그래프 분리 (GRAPH-[category].md). 마스터 GRAPH.md는 카테고리→서브그래프 매핑만 유지.

### 아키텍처: 정규 형식 + 인터페이스 어댑터

```
[입력 소스]                    [정규 형식]              [출력 뷰]
                                                      
Obsidian 메모  ─┐              entries/*.md            ┌─ Obsidian 그래프 뷰
Loop 문서      ─┤              GRAPH.md               ├─ Loop 호환 문서
세션 교훈      ─┼─→ Curator ─→ INDEX.md               ├─ Notion 페이지
plain text     ─┤              PROFILE.md             ├─ GraphDB (Neptune 등)
사용자 결정    ─┘                                      └─ Mermaid 다이어그램
```

- **정규 형식**: entries/ + GRAPH.md가 유일한 진실의 원천 (source of truth)
- **입력**: 어떤 형식이든 Knowledge Curator가 정규 형식으로 변환하여 저장
- **출력**: 정규 형식에서 필요한 뷰를 생성 (export adapter). 당장은 구현하지 않되, 정규 형식이 특정 도구에 종속되지 않도록 설계

### Entry 형식

```markdown
# [제목]

## Core
[1~2문장 핵심]

## Decision Context
[이 지식이 생긴 결정의 맥락 — 무엇을 선택했고, 왜, 어떤 성향이 반영되었는지]

## Tags
[도메인 태그]

## Links
- [대상 파일] | [관계 유형] | [연결 근거 1줄]

## Content
[실제 지식 내용]

## Source
[프로젝트명, 세션, 날짜]
```

### 관계 유형 (5개, 필요 시 확장)

| 유형 | 의미 |
|------|------|
| extends | 확장/심화 |
| contradicts | 충돌/대안 |
| applies-to | 적용 대상 |
| prerequisite | 전제 조건 |
| similar-to | 유사하지만 다른 맥락 |

### GRAPH.md 구조

```markdown
# Knowledge Graph

## Nodes
| ID | Title | Tags | Core |
|----|-------|------|------|
| welc-test-harness | WELC Test Harness | testing, safety | 수정 전 기존 동작을 테스트로 캡처 |

## Edges
| From | To | Type | Reason |
|------|----|------|--------|
| welc-test-harness | phase-decomposition | applies-to | Phase별 수정 시 각 단계에서 WELC 적용 |
```

Core 컬럼이 있으므로 GRAPH.md만 읽어도 각 노드의 핵심을 파악 가능. 상세가 필요할 때만 entry 파일로 이동(1홉).

### 접근 경로 (O(1) 목표)

```
작업 중 키워드 발생
  → GRAPH.md의 Tags/Title 스캔 (0홉, T3a에서 이미 로딩)
  → 매칭 노드의 Core로 즉시 판단
  → 상세 필요 시 entries/[id].md 읽기 (1홉)
  → 연관 지식 필요 시 Links 따라 1~2개 추가 읽기 (2홉)
```

### 확장성

- GRAPH.md가 200줄 초과 시: 카테고리별 서브그래프 분리
- 마스터 GRAPH.md는 카테고리→서브그래프 매핑만 유지
- 당장은 단일 GRAPH.md로 시작

### 입력 형식 독립

Knowledge Curator는 입력 소스의 형식에 의존하지 않음:
- Obsidian 메모 ([[wikilinks]] 포함) → wikilinks를 관계 힌트로 활용하되, 정규 형식으로 변환
- Loop/Notion 문서 → 구조화된 텍스트에서 핵심 추출
- 세션 교훈/결정 → 그대로 처리 (가장 일반적인 경로)
- plain text → 맥락 부족 시 Mickey에게 추가 정보 요청

출력 뷰(Obsidian 그래프, Loop 문서 등)는 정규 형식에서 생성하는 별도 어댑터로, 필요 시 구현.

---

## Subagent: Knowledge Curator

### 역할
작업 맥락을 받아 저장 여부를 판단하고, 저장할 경우 사용자 성향에 맞게 구조화하여 기존 지식과의 관계를 설정.

### 입력 (Mickey가 전달)
1. **작업 맥락 원문**: 이번 작업 단위의 세션 로그/결정/교훈/에러 해결 등 — 원래 맥락을 최대한 살려서 전달 (Mickey는 가공하지 않음)
2. **GRAPH.md**: 기존 관계 맵 전체
3. **PROFILE.md**: 사용자 프로필

### 출력 (Subagent가 반환)
1. **저장 판단**: 저장할 지식이 있는지 여부 + 근거
2. **새 entry 파일** (저장 시, entries/에 저장)
3. **GRAPH.md 업데이트** (새 노드 + 엣지 추가)
4. **INDEX.md 업데이트** (트리거 추가)
5. **1줄 요약** (Mickey가 사용자에게 알림용)
6. **PROFILE.md 업데이트 제안** (해당 시, 선택적)

### 프롬프트 핵심

```
너는 Knowledge Curator다.

## 저장 판단 (1단계)
입력된 작업 맥락에서 domain/에 저장할 가치가 있는 지식이 있는지 판단한다.

저장 대상:
- 사용자가 명시적으로 결정한 내용 (옵션 비교 후 선택) + 그 결정의 맥락과 성향
- 실패→원인 분석→해결의 교훈 (특히 PROFILE.md의 성향을 따르지 않아 실패한 경우)
- 새로 발견한 패턴/안티패턴 (사용자 성향에 부합하거나 위반한 사례)
- 다른 프로젝트에서도 참고할 가치가 있는 판단/패턴/교훈

저장 비대상:
- 프로젝트 특화 사실 (파일 경로, 환경 변수, 커맨드) → auto_notes/ 영역
- 이미 GRAPH.md에 있는 내용의 단순 반복
- 일회성 디버깅 과정
- 사용자 결정이 포함되지 않은 단순 작업 기록

저장할 것이 없으면 "저장 대상 없음"만 반환.

## 큐레이션 (2단계, 저장 대상이 있을 때)
1. PROFILE.md의 Decision Style과 Relationship Preferences를 기준으로 판단
2. 단순 사실("A는 B다")보다 결정 맥락("A 상황에서 B를 선택한 이유는 C, 이는 사용자의 D 성향 반영")을 중시
3. 관계 유형: extends, contradicts, applies-to, prerequisite, similar-to
4. 연결 근거를 반드시 1줄로 명시. 확실하지 않은 관계는 만들지 않음 (precision > recall)
5. 기존 entry와 중복이면 기존 entry를 보강 (새로 만들지 않음)

## PROFILE 업데이트 제안 (3단계, 선택적)
이번 지식에서 사용자의 새로운 성향/선호가 드러나면 PROFILE.md 업데이트를 제안.
제안 형식: "[섹션] [현재 내용 요약] → [제안 변경] | [근거]"
```

### 호출 흐름

```
세션 로그 업데이트 트리거 발동
  → Mickey: 이번 작업 단위의 맥락을 원문 그대로 subagent에 전달
           (GRAPH.md + PROFILE.md 함께 전달)
  → Subagent: 저장 판단 + 큐레이션 + PROFILE 제안
  → Mickey: 결과를 사용자에게 안내
           - 저장됨: "📝 [X] 저장, [Y]·[Z]와 연결"
           - 저장 없음: (알림 생략)
           - PROFILE 제안: "💡 PROFILE 업데이트 제안: ..."
  → 사용자: 작업 계속 (교정은 나중에)
```

Mickey의 역할은 **맥락 전달 + 결과 안내**에 한정. 저장 판단, 큐레이션, 관계 설정은 모두 subagent가 수행.

---

## 피드백 루프

### 작업 단위 (자동)
- subagent가 PROFILE.md 업데이트 제안 → 사용자 수락/거절 → 반영

### 세션 종료 (배치)
- 이번 세션 domain/ 추가분 일괄 제시
- 사용자: 수정/삭제/관계 교정
- 교정 내용 → PROFILE.md Corrections Log에 기록

### 정기 포스트모템 (주기적)
- domain/ 전체 현황 분석: 노드 수, 엣지 밀도, 고립 노드, 오래된 항목
- PROFILE.md 정합성 검토: Corrections Log 패턴 → Relationship Preferences 갱신
- GRAPH.md 구조 최적화: 중복 엣지 정리, 카테고리 재분류

---

## 실행 계획

### Phase 1: 초기 구조 + 마이그레이션 (이번 세션)
1. domain/ 디렉토리 구조 생성 (PROFILE.md, GRAPH.md, entries/)
2. 기존 patterns/INDEX.md의 5개 패턴을 entries/로 마이그레이션
3. GRAPH.md 초기 작성 (5개 노드 + 관계)
4. INDEX.md 갱신

**완료 기준**: GRAPH.md에서 5개 노드의 관계를 따라가며 entries/ 파일에 도달 가능

### Phase 2: Subagent 프롬프트 작성 + 단독 검증
1. Knowledge Curator subagent 프롬프트 작성
2. 테스트 지식 3개 입력 → 출력 품질 확인
3. PROFILE.md 참조가 출력에 반영되는지 확인

**완료 기준**: subagent가 PROFILE.md 기반으로 관계를 판단하고, 형식에 맞는 entry + GRAPH.md 업데이트를 생성

### Phase 3: 통합 + 프로토콜 반영
1. T1 프로토콜에 domain/ 접근 규칙 추가 (During Session)
2. 세션 로그 트리거에 subagent 호출 로직 추가
3. 실제 세션에서 E2E 동작 확인

**완료 기준**: 작업 단위 트리거 → subagent 호출 → 저장 → 알림 E2E 동작

### Phase 4: 실전 검증 + 개선 (다른 프로젝트에서)
1. 다른 프로젝트 세션에서 domain/ 지식이 실제로 참조되는지 확인
2. subagent 큐레이션 품질 평가
3. PROFILE.md 진화 확인

**완료 기준**: 다른 프로젝트에서 domain/ 지식을 참조하여 작업에 활용한 사례 1건 이상

---

## 열린 질문

1. ~~subagent 호출 방식~~ → 동기(use_subagent)로 시작, 안정화 후 delegate(비동기)로 전환
2. ~~GRAPH.md 분리 기준~~ → 100줄 기준으로 확정
3. ~~patterns/ vs domain/~~ → 병행 확정. patterns/=핵심 원칙(상한 7개), domain/=실전 지식(제한 없음)
4. ~~출력 어댑터~~ → 당장은 Mermaid. 인터페이스 독립 원칙은 유지하되 다른 어댑터는 필요 시 구현

---

**Status**: Phase 1 준비 완료
**Created**: 2026-04-18 (Mickey 14)
**Revised**: 2026-04-19 (Mickey 15) — Obsidian 기반 → 파일 기반 + Subagent로 전면 재설계
