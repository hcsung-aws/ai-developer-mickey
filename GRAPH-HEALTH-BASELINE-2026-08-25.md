# GRAPH HEALTH BASELINE — 2026-08-25 (Mickey 44)

> 글로벌 도메인 지식 그래프(`~/.kiro/mickey/domain/`) 전면 감사 결과의 **기준점 고정 문서**.
> 이 시점의 그래프 데이터는 의도적으로 **수정하지 않았다** — 개선 방향 A~D(운영 규율/도구 개선)만 반영하고,
> 이후 재측정 시 이 수치와 대조하여 "자연스럽게 개선되는가"를 판정한다.

## 재측정 방법

```
python scripts/graph_audit.py           # 무결성/orphan/중복/클러스터/허브 → scripts/output/graph_audit.txt (글로벌 배포본: ~/.kiro/mickey/scripts/graph_audit.py)
python scripts/m44_growth_analysis.py   # 성장 추이 (promote 백업 스냅샷 기반) → m44_growth_report.txt
python scripts/m44_edge_semantics.py    # 엣지 타입/허브 집중/상투 사유 → m44_edge_semantics.txt
```

## Baseline 수치 (2026-08-25 00시 기준)

> **측정 시점 주의**: 그래프는 타 프로젝트 promote로 계속 성장한다 (M44 세션 중에도 3건 승격되어
> 종료 시점 실측은 노드 131/엣지 376, 저연결 5건 — code-defender-request-repo-cwd 추가).
> 대조 시에는 절대 수치보다 **비율 지표(평균 차수, 허브 점유율, 상투 사유율)와 문제 카운트(orphan/중복/malformed)의 추세**를 본다.
> 평균 차수는 병합(상위+cloud) 그래프 기준 = graph_audit [J] 값.

| 지표 | 값 | 판정 |
|------|-----|------|
| 노드 | 129 (상위 109 + cloud 20) | — |
| 엣지 | 373 (상위 351 + cloud 22) | — |
| dangling 엣지 / Path 결손 | **0 / 0** | 건강 |
| 0-엣지 신규 추가 (7/23~8/24, 27 스냅샷 전수) | **0건** | 건강 — promote 승격 번들의 엣지 강제 효과 |
| orphan (차수 0, anchor 제외) | **1** (external-source-digest-separation) | 문제 — graduated 인계("다음 Curator 반영 예정")가 2개월 방치 |
| 저연결 (차수 1) | **4** (installer-seed-semantics, focus-preclick-input-leakage, mechanism-level-cause-attribution, xray-transaction-search-query-path) | 관찰 — 개선 B 후 자연 보강되는지 확인 |
| 중복 엣지 쌍 | **4** (npm-audit↔packager, cdk-cjs↔packager, supersede↔plan-before-execute, supersede↔phase-based) | 정리 후보 (보류) |
| INDEX 중복 등재 | **3** (powershell-curl-escape ×3, packager ×2, supersede ×2) | 정리 후보 (보류) |
| malformed 표 행 | **1** (installer-auth 노드 Core 셀 미이스케이프 `\|\|`) | 정리 후보 (보류) → **M45 수선 완료 (2026-08-27)**: 해당 행 `\|` 이스케이프 (백업 GRAPH.md.bak-ai-developer-mickey-m45). 동시에 재발 방지 프로세스 교정 — promote 파이프 정규화+셀 수 검증, CURATOR-PROMPT 이스케이프 규율, graph_audit INDEX 파서 이스케이프 존중. 재측정 시 이 항목은 0이 기대값 |
| 표 내부 빈 줄 (상위 GRAPH) | Nodes **9** / Edges **41** | 개선 A-② 후 증가 멈추는지 확인 |
| cloud 드리프트 (상위 등재 + cloud Path) | **5** (appconfig ×2, cloudfront ×2, cdk-context-lookup) | 개선 A-① 후 신규 발생 0 확인 |
| 평균 차수 (병합 그래프, [J]) | **5.78** (종료 시점 5.74 — 상위 GRAPH 단독 기준은 7/23 6.36 → 5.95 완만 하락) | 관찰 — 하락 멈춤/반등이 개선 신호 |
| 신규 노드 평균 엣지 | **~2.4** | 관찰 |
| 상위 5 허브 엣지 점유 | **35%** (deploy-output-distrust 단독 56엣지 = 15%) | 관찰 — 개선 B 후 하락이 개선 신호 |
| 엣지 타입 분포 | similar-to 61% / applies-to 23% / extends 14% / prerequisite 3% | 관찰 |
| 상투 사유 엣지 ("가족/철학/계열") | **21%** (79/373, 전부 similar-to) | 관찰 — 개선 B 후 신규분에서 감소 확인 |

## 연결 보강 후보 (보류분 — 재측정 시 자연 해소 여부 확인)

orphan/저연결 해소용 엣지 9건 후보를 M44에서 도출했으나 **의도적으로 미반영** (Curator 자연 성장 관찰).
상세 목록: `MICKEY-44-SESSION.md` Key Decisions 및 세션 대화 기록 참조. 핵심:
- external-source-digest-separation → external-benchmarking (extends), sot-deduplication-by-reference (similar-to)
- installer-seed-semantics → installer-auth-state-followup-gap, idempotent-infra-setup
- focus-preclick-input-leakage → directed-input-reveals-timing-race-bugs
- mechanism-level-cause-attribution → fail-verdict-cause-preemption, external-regression-hypothesis
- xray-transaction-search-query-path → empty-scan-distrust (cross-category)

## 분류(§20 Step 3) 판정 결과

| 클러스터 | k | 응집률 vs 우연 기대치 | 판정 |
|---------|---|---------------------|------|
| agent-design | 11 | 0.27 vs 0.09 (3.0배) | **도메인 후보** — 카테고리화는 별도 세션에서 §20 파이프라인으로 |
| qa-automation | 7 | 0.11 vs 0.06 (1.8배) | game 대계열(unity+unreal+game-qa 합집합 ~14)로 경계 재설정 시 후보 |
| mcp | 10 | 0.13 vs 0.08 (1.6배) | 경계선 — flat 잔류 (엄선 시 임계 유지 불확실) |
| verification | 23 | 0.24 vs 0.21 (1.1배) | aspect 확증 (M40 판정 유지) |
| testing / distrust | 7 / 7 | 3.0배 / 2.0배 (과반 co-tag=verification) | verification aspect 얽힘 — flat 잔류 |
| cdk | 7 | 1.3배 | aspect 신호 — cloud 드리프트 이관 시 자연 감소 예상 |

## 성장 건전성 진단 (원인 분석)

- **골격 건강**: 무결성 100%, 신규 노드는 항상 엣지와 함께 추가됨 — §17 승격 번들 + promote 스크립트의 구조적 강제가 작동
- **질적 편중 (hub-and-spoke화)**: 신규 엣지가 소수 허브로 집중. 원인 = Curator가 승격 시 GRAPH 스캔에서 눈에 띄는 허브와 연결하는 것이 최저비용 경로이기 때문. 상투 사유 21%가 방증. peer 간(비허브) 연결이 구조적으로 빈약 → 개선 B의 표적
- **드리프트/방치의 공통 원인**: "다음에 반영" 류 인계는 실행 주체가 없으면 방치된다 (orphan 2개월). 감사를 도구화하여 중단점(엔트로피 체크)에 배치 → 개선 C의 표적
- **미러 두절 → 오판 정정 (M44 후반 supersede)**: repo `mickey/domain/` 갱신 두절은 결함이 아니라 **서고 계약(mickey/README.md)의 설계된 분리**였음 — 개인 지식은 공개 repo에 커밋하지 않고, repo는 seed 골격 + [Seed 예시] 10건만 유지. 성장 이력 소스는 `.promote-backups/`가 담당 (본 분석도 이를 사용). 세대 파일(extended-protocols, CURATOR-PROMPT)만 global↔repo 동기화 대상이며 현재 SAME

## 반영된 개선 (M44)

- A: promote_knowledge.py — 카테고리 Path 하위 GRAPH 라우팅 + 표 연속성 보장 + 허브 편중 경고
- B: CURATOR-PROMPT — 엣지 규율 (비허브 peer 1개 이상 + 구체 메커니즘 사유)
- C: extended-protocols §3 — 그래프 감사 도구 등재 + graph_audit.py 글로벌 배포
- D (M44 후반 재정의): ~~promote 미러 동기화 리마인더~~ → **철회** (서고 계약과 충돌 — 개인 지식은 repo 미러 대상이 아님). 대체: 이력 소스는 `.promote-backups/` 공식화 + repo seed 정합성(스키마 현행화, PROFILE 템플릿화)을 M44에서 수술 완료

## Last Updated
2026-08-25 (Mickey 44)
