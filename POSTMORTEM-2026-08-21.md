# POSTMORTEM 2026-08-21 (경량, Mickey 42)

> §9 자동 트리거 (M41 인계: 2026-07-24 이후 도달) + §18 Activity Metrics 실측.
> 측정: `scripts/m42_measure_usage.py` (m21 패턴 동일 — 비교 가능성 유지). 원자료: `scripts/output/m42_metrics.txt`, `m42_protocol_lines.txt`

## 1. Activity Metrics — 전 지표 임계값 이상 (위반 0)

윈도우: 2026-06-20 ~ 08-21 (M21 baseline 이후 9주). 표본: 활성 11개 프로젝트 104세션 (mickey-power 제외 — sessions/ 33건이 m38 워크스페이스 복사 산물로 이중 카운트 오염, 측정 중 발견·제거).

| 메트릭 | 전체 (104세션) | 타 프로젝트만 (83세션) | baseline (M21) | 임계 | 판정 |
|--------|--------------|---------------------|---------------|------|------|
| 글로벌 domain 참조 | 2.76 | 2.05 | 2.45 | 0.5 | OK |
| Curator 호출 흔적 | 9.75 | 4.80 | 2.65 | 0.5 | OK |
| auto_notes 참조 | 3.47 | 3.77 | 5.55 | 1.0 | OK (하락 추세 — 감시) |
| [Protocol] 태그 | 3.24 | 2.07 | 2.03 | 0.3 | OK |

- 표본 가드 (M21 교훈) 적용: 타 프로젝트만 분리 판정 — 전 지표 OK. 자기 자신(ai-developer-mickey)은 메타 편향으로 curator 29.05 등 과대
- auto_notes 3.77 vs baseline 5.55: 임계(1.0) 대비 여유 있으나 하락 추세. 1회 관찰로 조치 없음, 다음 측정 시 재확인

## 2. [Protocol] 태그 정성 분석 (332건 중 타 프로젝트 170건 표본 정독)

### 긍정 (프로토콜이 실전에서 작동)
- **batch-confirm-autonomous-proceed**: anjin/epic-lore/bvt 3개 프로젝트에서 10회 이상 실증, 이의 0회 — patterns/ 유지 확고
- **M41 격리 구조**: anjin M10 "delegate Curator 크래시에도 격리(staging) 덕에 안전" — 쓰기 격리가 크래시 상황에서 실전 검증됨. promote 실전 다수 (epic-lore M17이 결함 2건 발견·정정까지)
- **M42 전환 조기 실증**: anjin M11 "use_subagent Curator 전환 첫 실전 성공 — 완주 판정을 staging 디스크 실측으로 수행한 절차 유효" — **D-42-1의 1회차 완주 검증 관문이 타 프로젝트에서 이미 통과**
- **Curator 검증 기간 git diff**: back-to-basic M5에서 누락 1건 조기 감지 — 안전망 실증
- **실측 계열 원칙군** (deploy-output-distrust / empty-scan-distrust / ide-file-write-flush-distrust / R-014): 전 프로젝트에서 최다 적중 — Mickey 지식 체계의 주력 자산
- **§10 동작 시나리오** (anjin M4: 데이터 호환성 항목이 재작업 0회), **§14 이상 감지** (epic-lore M14: 유휴 과금 발견), **§21 기호-맥락** (anjin M9), **경량 포스트모템 자가 실행** (epic-lore M17, anjin M11 — 프로토콜이 타 프로젝트에서 자율 작동)

### 부정/마찰 (반복 신호)
1. **PowerShell execute 계층 함정 — 최다 반복**: python -c 위반 재발 (epic-lore M15 2회 + anjin M9), `$_`/`$env:`/`&&` 소실, Format-Table/Select-String 출력 유실 (anjin M7 + 본 세션 재현), 한/영 미전환 "ㅛ" (back-to-basic M15 4회). epic-lore M15 진단이 정곡: "규칙 존재만으로 부족" — 규칙은 있으나 위반이 구조적으로 재발
2. **Curator subagent 글로벌 읽기 차단** (anjin M4): 비대화 모드에서 `~/.kiro/mickey/**` 읽기가 "no user to approve"로 차단 → 회피 지시(domain 후보는 staging에만)가 3회 연속 성공 (M5~M7). 회피가 사실상 표준 경로가 됐으나 CURATOR-PROMPT에 미명문화
3. **세션 정리 누락 비용** (back-to-basic M2→M3): 다음 세션이 승계 정리 비용 지불 — 5/5 정리 문의가 규정임을 실증

## 3. 변경 이력 대조 (§9 step 4 — baseline 이후 변경 유효성)

| 변경 | 판정 | 근거 |
|------|------|------|
| M41 격리 (T1 v18 + §17 v21 + promote) | **유효** | 크래시 상황 안전 (anjin M10), promote 실전 다수, 글로벌 쓰기 혼입 재발 0 |
| M42 전송 전환 (T1 v19 + §17 v24) | **유효 (조기)** | anjin M11 첫 실전 성공. 본 프로젝트 1회차는 이번 세션 종료 시 |
| §20 실측 기준화 (M40) | 판단 보류 | 재트리거 사례 미발생 (잠복 기간) |
| §22 MCP 경유 감지 / §23 기호-맥락 (타 프로젝트발) | 유효 | 각 원 프로젝트 실증 (epic-lore M7 / anjin M9) |
| Curator 검증 기간 (첫 5회 git diff) | 유효 | 누락 조기 감지 1건 (back-to-basic M5) |

## 4. 개선 후보 (사용자 결정 대상)

1. **PowerShell 함정 구조 대책** (반복 최다): 규칙 추가는 M14 원칙(기존 체계 검토 우선) 위반 — 대신 기존 규칙의 **강제 장치** 검토. 후보: 세션 내 1회 위반 즉시 해당 세션 잔여를 .py 스크립트 전용으로 전환하는 원스트라이크 규약 (adaptive 후보)
2. **Curator 회피 지시 명문화**: anjin의 "domain 후보는 staging에만 + 글로벌 읽기 실패 시 컨텍스트로 대체" 회피를 CURATOR-PROMPT 정식 반영 (3회 실증)
3. auto_notes 하락 추세: 조치 없음, 다음 측정 시 재확인 (기록만)

## 결론

진화 루프 건강: **양호**. 4개 지표 전부 임계값 상회 + M41/M42 구조 변경이 타 프로젝트 실전에서 검증됨. M20(0% 위기) → M21(baseline) → 현재까지 활용도가 유지·상승 추세. 반복 마찰은 도구 계층(PowerShell execute)에 집중 — 지식이 아니라 강제 구조의 문제.
