# 2026-07-16 — mickey-power 브랜치 Kickoff (트랙 분리 인계)

> **이 문서는 이 디렉토리에서 새 세션을 시작하는 Mickey가 가장 먼저 읽는 진입 문서다.**
> 작성: 2026-07-16 v10 트랙 분리 세션 (master `78f87ab` 시점. 당초 M38로 오귀속 → 날짜 기반으로 정정. CLI 트랙 M37은 원본 디렉토리에서 병행 진행 중이었음)

## 1. 이 디렉토리의 정체 (1분 진입 가이드)

- **브랜치**: `mickey-power` — power-mickey(v10) 작업 **전용**
- **원본 디렉토리** `c:\Users\hcsung\work\kiro\ai-developer-mickey` (master) = **v2 CLI agent mickey 트랙 전용**. 그쪽 작업(MICKEY-N 세션, 지식 그래프 Phase 2, Curator 보정)은 여기서 하지 않는다
- **통합 계획**: Kiro CLI v3 정식 출시 시 v3(power)로 완전 통합, 이 분리는 그때까지의 과도기 구조 (D-38-1)
- **지식 그래프는 공유**: 양 트랙 모두 `~/.kiro/mickey/` (글로벌 SoT)를 참조한다. 브랜치 분리로 지식이 갈라지지 않는 것이 정상

## 2. 세션 규약 (이 디렉토리 한정) — 날짜+UID 규약 (D-0717-1)

> 2026-07-17 사용자 확정 (세션 b3d7e1). 구 규약(`YYYY-MM-DD-<주제>.md`)을 대체한다.
> 배경: 같은 프로젝트에서 세션이 여러 개 동시에 열리는 IDE 상황 + CLI 연속성 공백(boot hook이 매번 "Mickey 1" 오판) 해소.

- **로그 파일명**: `session_history/YYYY-MM-DD-<UID>-log.md`
- **HANDOFF 파일명**: `session_history/YYYY-MM-DD-<UID>-handoff.md`
- **UID**: 6자리 hex 권장 (예: `b3d7e1`). session_history/ 내 유일성 확보. 생성: `python .kiro/scripts/gen_session_uid.py` (충돌 회피 내장. one-liner 금지 규칙 준수)
- **기록 후 의무**: 채팅 응답에 UID를 명시적으로 남긴다 (IDE는 지난 채팅을 열람 가능하므로 이것이 세션 선택의 열쇠)
- **이어가기 절차 (양쪽 분기)**:
  - **IDE**: 사용자가 새 세션에서 UID를 알려주면 → 해당 UID의 log/handoff 로드. UID 미지정 시 → CLI 경로와 동일하게 최신본 제시 후 확인.
  - **CLI**: 가장 최근 저장된 log + handoff를 탐지 → **사용자 확인 받은 뒤** 진행 (자동 진행 금지).
- **`sessions/MICKEY-N-*` 는 master(CLI 트랙) 소유 — 이 디렉토리에서 생성/갱신 금지.** steering 의 MICKEY-N-SESSION 생성 절차는 이 디렉토리에서는 위 날짜+UID 로그로 대체한다 (번호 충돌 방지, v3 통합 시 병합 안전)
- 그 외 프로토콜(REMEMBER, 10단계, Curator, context-window)은 steering 그대로 적용
- power steering(session-protocol.md)으로의 일반화("MICKEY-N 사용 불가 환경" 분기)는 **v3 통합 시점 판단으로 보류** — 사용자 재확인 전 steering 수정 금지 (D-0717-1 부속 결정)

## 3. 현재 상태 (2026-07-16 실측)

- v10 Power Migration: **Phase 0~5 완료 + v3 런타임 검증 V1~V8 전 항목 닫힘**
- 검증 기준값 (전부 일치 확인, 이 clone 에서 실측):
  - `python scripts/verify_power_structure.py` → **7/7**
  - `python scripts/verify_hooks.py` → **6/6**
  - `python scripts/verify_deploy_power.py` → 25/25 (기준값)
  - `python scripts/verify_serving_sync.py` → **IN-SYNC** (홈 서빙본 `~/.kiro/powers/installed/power-mickey/` 9파일 sha256 일치)
- 실사용 테스트: acp-client 세션(M38)에서 activate → steering pull → 세션 프로토콜 → MCP 직접 호출 전부 정상 동작 확인
- `.kiro/hooks` + `.kiro/scripts` 는 `.gitignore`(`.kiro/` 전체 제외) 탓에 clone 에 누락 → 수동 이식됨 (`m38_copy_kiro_workspace.py`). **git 미추적 상태이므로 유실 주의**

## 4. 잔여 과제 (우선순위 제안)

1. **`.kiro/` gitignore 부분 해제 검토** — `hooks/`, `scripts/` 만 추적 대상으로 전환할지 결정. 미해결 시 clone 마다 수동 복사 반복 (즉시 우회 → 정식 해결 인계 건)
2. **IDE 묶음 실측** (v10 최후순위 인계) — Kiro IDE steering 인식 + IDE `.kiro.hook` 정식 규격 실측
3. **registry stale path** (v10 부채)
4. **영문 changelog v9.2 백필** (v10 부채)
5. **`mickey/domain/entries` 잔재 정리** (계획서 §8-a)
6. (관찰) `~/.kiro/powers/installed/` 백업 zip 4개 누적 — pre-v10 백업은 롤백 안전장치이므로 최후 정리

## 5. 작업 흐름 (배포 파이프라인)

1. `power-mickey/` 정본 수정
2. `python scripts/deploy_power.py` — 홈 배포 (버전 게이트 2.10 + 자동 백업 + clean-replace)
3. `python scripts/verify_serving_sync.py` — IN-SYNC 확인
4. 검증 3종 회귀 (기준값 7/7, 6/6, 25/25 유지 확인)
5. 커밋은 `mickey-power` 브랜치에만. **master 로 직접 커밋 금지**

## 6. 참고 문서 위치

- 계획서: `IMPROVEMENT-PLAN-v10-power-migration.md`, `VERIFICATION-PLAN-v3-power-runtime.md`
- 직전 로그: `session_history/2026-07-14-v3-power-runtime-verification.md` (V1~V8 결과표 + F1~F5 처리)
- 이식 매트릭스: `docs/v2-to-v3-mapping.md`
- 환경 갱신 (2026-07-17/19 실측): SessionStart hook 이 **acp-client 에서도 발화 확인됨** (V6 당시 "미발화" 기록은 구버전 클라이언트 기준 — 버전업으로 해소 추정). 단, hook stdout 한글 mojibake 이슈는 별도 (hook 개정에서 처리)

## Last Updated
2026-07-19 (세션 551c3f — §2 날짜+UID 규약 성문화, §6 acp-client hook 발화 사실 갱신)
