# VERIFICATION-PLAN — v3 Power 런타임 실측 검증

- **작성일**: 2026-07-14
- **선행 상태**: v10 Power Migration Phase 5 사실상 완료. 홈 `~/.kiro/powers/installed/power-mickey/` 가 v10 서빙 중. 정적 검증기 3종 전부 기준값 일치 (7/7, 6/6, 25/25).
- **관련 문서**: `IMPROVEMENT-PLAN-v10-power-migration.md`, `session_history/2026-07-13-mickey-v10-migration-phase-5-install.md`

---

## 1. 배경

지금까지의 검증은 전부 **정적 검증**(파일 구조 · front matter · 배포 스크립트 harness)이었다. 회귀 시나리오 ①(CLI v2) ②(CLI v3)도 "부팅이 되고 에이전트가 응답한다" 수준이었고, **v3 런타임이 Power 를 실제로 어떻게 소비하는지**(kiro_powers 도구 경유 activate · steering 로딩 · MCP proxy · hook 발화)는 실측된 바 없다.

이번 세션은 v3 런타임 위에서 돌고 있고 power-mickey 가 설치된 상태이므로, **살아있는 세션 안에서 직접 실측**할 수 있다.

## 2. 목표

v3 런타임에서 power-mickey 의 소비 경로 전체가 실제로 동작하는지 실측하고, 동작/미동작/관측불가를 항목별로 판정하여 기록한다. 이 결과는 후보 A(IDE 묶음) 진행 여부와 부채 우선순위 판단의 근거가 된다.

## 3. 검증 항목 매트릭스

| # | 항목 | 방법 | 기대 결과 | 판정 기준 |
|---|------|------|-----------|-----------|
| V1 | Power 등록 인식 | `kiro_powers list` 호출 | power-mickey 가 이름·설명·키워드·MCP 서버(aws-knowledge-mcp-server)와 함께 나열 | 4개 필드 전부 존재하며 v10 내용과 일치 |
| V2 | activate 동작 | `kiro_powers activate power-mickey` 호출 | POWER.md 전문 + steeringFiles 7종 목록 + toolsByServer(aws-knowledge 도구들) 반환 | steering 7종 이름 전부 확인, MCP 도구 1개 이상 노출 |
| V3 | readSteering 동작 | steering 7종 각각 `readSteering` 호출 | 각 파일 전문 반환 | 7/7 로드 성공, 각 파일의 핵심 마커(REMEMBER 12 등) 존재 |
| V4 | 서빙본-정본 일치 | 홈 `installed/power-mickey/**` 와 프로젝트 `power-mickey/**` 를 .py 스크립트로 해시 비교 | 전 파일 일치 | 불일치 0건 |
| V5 | MCP proxy 동작 | `kiro_powers use` 로 read-only 도구(list_regions) 1회 호출 | 정상 응답 (리전 목록) | 에러 없이 데이터 반환 |
| V6 | SessionStart hook 발화 | boot 스크립트 산출물(로그·파일 mtime)을 .py 스크립트로 실측 | 이번 세션 부팅 시각 근처의 산출물 존재 | 산출물 mtime 이 세션 시작 시각과 정합 |
| V7 | steering inclusion 모드 | always 6종 자동 주입 / manual 1종(knowledge-curator) 미주입 여부 관측 | always 는 주입, manual 은 activate 전 미주입 | §5 관측 한계 참조 — 판정 불가 시 '관측불가'로 기록 |
| V8 | Stop hook 발화 | 세션 종료 시점 산출물 확인 | close 스크립트 산출물 생성 | **이번 세션 내 실측 불가** — 다음 세션 시작 시 V8 후속 확인으로 이월 |

## 4. 실행 순서 및 분기

각 단계는 **성공 경로와 실패 경로를 모두** 따른다.

1. **V1 (list)** — 성공하면 V2 로 진행 / 실패하면(power-mickey 미노출) 즉시 중단하고 registry(`user-added.json`) 상태를 보고. 이 경우 부채 B-1(stale path)이 원인일 수 있으므로 후속 항목을 실행하지 않는다.
2. **V2 (activate)** — 성공하면 V3 로 진행 / 실패하면 POWER.md front matter 와 홈 물리본 상태를 보고하고 V3~V5 를 건너뛴다. V4·V6 은 kiro_powers 와 무관하므로 계속 진행한다.
3. **V3 (readSteering ×7)** — 7/7 성공하면 진행 / 일부 실패하면 실패 파일명과 에러를 기록하고 나머지 항목은 계속 진행한다.
4. **V4 (해시 비교)** — .py 스크립트(`scripts/verify_serving_sync.py` 신규 작성)로 실행. 일치하면 진행 / 불일치가 있으면 불일치 목록을 보고하고, **재배포(`deploy_power.py`)는 사용자 확인 전에 실행하지 않는다**.
5. **V5 (MCP use)** — read-only 도구만 사용한다. 성공/실패 모두 기록 후 진행. 쓰기성 도구는 어떤 경우에도 호출하지 않는다.
6. **V6 (SessionStart hook)** — 산출물이 있으면 발화로 판정 / 없으면 "미발화 또는 산출물 없음"으로 기록하되, boot 스크립트가 산출물을 남기는 구조인지 먼저 코드를 읽어 확인한 뒤 판정한다 (산출물을 안 남기는 스크립트면 '관측불가'로 판정).
7. **V7 (inclusion 모드)** — §5 관측 한계에 따라 판정 가능한 범위만 기록.
8. **V8 (Stop hook)** — 이번 세션에서는 실행하지 않고, 다음 세션 인계에 후속 확인 항목으로 명시한다.

## 5. 관측 한계 (미리 인정하고 들어가는 것)

- **V7**: 에이전트가 자기 컨텍스트에 steering 이 주입됐는지 스스로 관측하는 것은 자기참조적이라 신뢰도가 낮다. 간접 증거(activate 전에 steering 고유 규약을 알고 있는가)로만 판정하고, 애매하면 '관측불가'로 기록한다. IDE 실측(후보 A)에서 더 정확히 판정할 수 있다.
- **V8**: Stop hook 은 세션이 끝나야 발화하므로 구조적으로 이번 세션 내 실측 불가.
- **키워드 자동 트리거**: v3 가 사용자 프롬프트 키워드로 power 를 자동 제안하는지는 런타임 내부 동작이라 관측 수단이 없다. 이번 계획에서 제외한다.

## 6. 산출물

- 검증 결과표 (항목별 PASS / FAIL / 관측불가) → 세션 로그 `session_history/2026-07-14-v3-power-runtime-verification.md`
- 신규 스크립트: `scripts/verify_serving_sync.py` (V4용, 재사용 가능한 정적 검증기로 유지)
- FAIL 항목 발견 시: 원인 분석과 수정 후보를 기록하되, **수정 실행은 사용자 확인 후**로 한다.
- 검증 완료 후 PROJECT-OVERVIEW.md 의 Power Mickey 소절에 런타임 실측 결과 한 줄 반영 (사용자 확인 후).

## 7. 이 계획이 끝나면

- 전 항목 PASS → 후보 A/B/C 선택으로 복귀 (런타임 신뢰 확보 상태).
- FAIL 존재 → FAIL 항목 수리를 최우선 작업으로 승격하고 사용자와 협의.

## Last Updated

2026-07-14 (초안 작성, 실행 전)
