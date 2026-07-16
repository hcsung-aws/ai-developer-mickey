# 세션 로그: Mickey v10 Power 마이그레이션 (Phase 0~1)

- **날짜**: 2026-07-04 (Sat)
- **엔진**: kiro-cli 2.10.0 · v3 engine
- **목표**: CLI v2 agent `ai-developer-mickey` (v17)을 v3 Power로 마이그레이션하기 위한 Phase 0~1 착수
- **범위**: 사전 준비 · 안전망 · 공용 서고 재정렬 (재작성은 Phase 2에서)

---

## 1. 배경과 사용자 요구

사용자가 v3 부팅 세션에서 기존 v2 Mickey 에이전트를 활용할 방법을 요청했다. 본좌가 강호를 답사한 결과, v3에서는 v2 agent JSON의 `prompt` 필드가 무시되고 `power` 개념으로 프롬프트 확장 방식이 바뀌었음을 확인했다. `kiro-cli` 자체는 `--agent-engine {v1,v2,v3}` 삼중 엔진 옵션이 있어 v2 방식 자체는 그대로 동작하지만, v3에서 동일 심도의 Mickey를 쓰려면 Power를 새로 짜야 한다.

## 2. 조사에서 확정된 사실

| 항목 | 내용 |
|------|------|
| v3 Power 설치 위치 | `~/.kiro/powers/installed/<name>/` (`POWER.md` + `mcp.json` + `steering/`) |
| Power 등록 파일 | `~/.kiro/powers/installed.json` |
| v3 agent JSON 처리 | prompt 필드 무시. 시스템 프롬프트는 v3 base로 강제 |
| v2 자산 | `~/.kiro/agents/*.json` 유지, `kiro-cli agent list` 정상 인식 |
| 공용 서고 | `~/.kiro/mickey/{extended-protocols.md, patterns/, domain/}` — 파일 기반 지식맵 (그래프 DB 아님) |
| `.serena/memories/` | 비어 있음 — 지식 그래프 정본 아님 |
| memorygraph MCP | 사용자 판단으로 배제. 대신 Serena + Graphify에 코드 관계 위임 |

## 3. 사용자가 확정한 마이그레이션 방향

1. **옵션 B** (v3 power에 v2 자산을 적재해 심도 회복) 진행. v3 정식 공개 후 옵션 C로 이어가는 두 단계 전략.
2. 기존 `power-mickey/`는 IDE용 옛 유물이라 **재활용하지 않고 새로 짓는다**.
3. `~/.kiro/mickey/`를 v2·v3 공용 서고로 승격. 단, 공용 도메인 지식과 프로젝트별 지식의 분리는 v2 규약 그대로 유지.
4. memorygraph MCP는 배제. 파일 기반 지식맵 + Serena + Graphify로 대체.
5. Phase 4는 **4-A** (Curator 로직을 steering으로 흡수하는 단순안).
6. **Phase 0~1까지 이번 세션에서 진행**, 이후는 다음 세션.

## 4. 전체 Phase 계획 (요약)

- **Phase 0**: 백업 · 계획서 · 세션 로그 (이번 세션)
- **Phase 1**: `~/.kiro/mickey/` 공용 서고 계약 문서화 및 검증 (이번 세션)
- **Phase 2**: 새 `power-mickey/` 골격 제작 (다음 세션)
- **Phase 3**: 세션 관리 hook·스크립트 (`SessionStart`/`Stop`) 구축
- **Phase 4**: Knowledge Curator 로직을 steering으로 흡수 (4-A)
- **Phase 5**: install.ps1/sh 개편 · README/docs 갱신 · 회귀 검증

상세는 `IMPROVEMENT-PLAN-v10-power-migration.md` 참조.

## 5. 이번 세션 실행 내역

### Phase 0
- [x] `.gitignore`에 `*.pre-v10-bak.zip`, `*.pre-v10-bak/` 패턴 추가
- [x] `session_history/` 디렉토리 개설, 본 파일 개시
- [x] `scripts/backup_pre_v10.py` 신규 작성 (idempotent 백업기)
- [x] `IMPROVEMENT-PLAN-v10-power-migration.md` 프로젝트 루트 생성
- [x] 기존 자산 백업 4건 실행 (`python scripts/backup_pre_v10.py`)
  - `power-mickey/` → `power-mickey.pre-v10-bak.zip`
  - `~/.kiro/powers/installed/power-mickey/` → `~/.kiro/powers/installed/power-mickey.pre-v10-bak.zip`
  - `~/.kiro/agents/ai-developer-mickey.json` → `.pre-v10-bak` 사본
  - `~/.kiro/agents/knowledge-curator.json` → `.pre-v10-bak` 사본

### Phase 1
- [x] `mickey/README.md` 신규 작성 (프로젝트 원본, 공용 서고 계약서)
- [x] `scripts/verify_mickey_home.py` 신규 작성 (Test Harness, `--path` 옵션 지원)
- [x] `scripts/sync_mickey_readme.py` 신규 작성 (Phase 5 install 개편 전 임시 유틸)
- [x] `~/.kiro/mickey/README.md` 배포 (`python scripts/sync_mickey_readme.py`)
- [x] verify 실행
  - `--path ~/.kiro/mickey` → **PASS**
  - `--path mickey` (프로젝트 원본) → **FAIL** (patterns 1개 < 최소 2개)

### 5.1 Phase 1 검증 결과 및 오독 정정

**초기 진단 (오독)**: verify FAIL 결과를 "서고 정본 불일치 이슈"로 규정. 프로젝트 원본과 사용자 홈 격차(patterns 5개, entries 48개)를 결정 필요 항목으로 §8-a 에 기록.

**사용자 지적을 통한 정정 (2026-07-04)**:
- Curator 프롬프트 확인: 사용자 홈만 수정 대상 (`~/.kiro/mickey/domain/**`)
- install.ps1: 프로젝트 → 사용자 홈 단방향 seed 배포
- git 커밋 이력: `Mickey 19: sync global to repo mickey/ (per-file direction)` — 선별 커밋 워크플로

즉 두 저장소의 divergence 는 설계된 정상 동작. 확정된 원칙:

- 프로젝트 `mickey/` = 모든 사용자에게 배포되는 **seed 골격**
- 사용자 홈 `~/.kiro/mickey/` = **각 사용자의 개인 지식 그래프 실체**
- 개인 지식은 프로젝트에 커밋하지 않음 (예외: `extended-protocols.md` T1 core)
- 이 프로젝트 자신도 예외 아님 — 초창기 관행의 잔재(entries 10건)는 정리 대상

**정정 산출물** (Phase 1 재실행):
- [x] `mickey/README.md` 재작성 — seed vs 개인 그래프 원칙 명시
- [x] `scripts/verify_mickey_home.py` 재설계 — `--mode {home,seed,auto}` 분리
- [x] `IMPROVEMENT-PLAN-v10-power-migration.md` §7 R7 · §8-a 정정
- [x] `~/.kiro/mickey/README.md` 재동기화
- [x] verify 재실행: `home` PASS, `seed` PASS (auto 판정도 정확)

**부수 결정 사안** (이번 사이클 밖): 프로젝트에 잔존한 개인 지식 파일들(`domain/entries/*.md` 10건 등) 처리 방침. 상세는 계획서 §8-a 부수 결정 사안 참조.

## 6. 다음 세션 인계 사항

- **Phase 2 진입 준비**:
  - `docs/v2-to-v3-mapping.md` 매트릭스 초안 작성
  - 새 `power-mickey/` steering 7개 초안 작성
  - `mcp.json` 정비 (memorygraph 제거, aws-knowledge 유지)
- **부수 결정 사안**: 프로젝트 잔재 개인 지식 파일 처리 방침 (권고: 교육 · 데모용 seed 예시로 재분류 유지 후 라벨링)
- **참고 원본**: `examples/ai-developer-mickey.json` (v17 prompt), `mickey/extended-protocols.md`
- **백업 위치**:
  - `power-mickey.pre-v10-bak.zip` (프로젝트 루트)
  - `~/.kiro/powers/installed/power-mickey.pre-v10-bak.zip`
  - `~/.kiro/agents/{ai-developer-mickey,knowledge-curator}.json.pre-v10-bak`

---

*본 로그는 세션 진행에 따라 계속 추가 기록됨*
