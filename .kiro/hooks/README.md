# .kiro/hooks/ — Mickey v10 Phase 3 hook 예시

**성격**: 예시 파일. Mickey 프로토콜 부팅·마감을 자동화하고 싶을 때 활성. 활성화하지 않아도 스크립트 단독 호출로 동일 동작 가능.

**규약**: 계획서 `IMPROVEMENT-PLAN-v10-power-migration.md` §6 Phase 3.

## 파일 목록

| 파일 | 대상 | 트리거 | 실행 스크립트 |
|------|------|--------|--------------|
| `mickey-session-start.json` | Kiro CLI v3 | `SessionStart` | `.kiro/scripts/mickey_session_boot.py` |
| `mickey-pre-task.kiro.hook` | Kiro IDE    | `preTaskExecution`  | `.kiro/scripts/mickey_session_boot.py` |
| `mickey-post-task.kiro.hook`| Kiro IDE    | `postTaskExecution` | `.kiro/scripts/mickey_session_close.py` |

## 폐기된 hook (F5, 2026-07-15 실측)

`mickey-session-stop.json` (`Stop` → `mickey_session_close.py`) 은 폐기됨.
- **근거**: 프로브 실측 결과 `Stop` 트리거는 세션 종료가 아니라 **응답 종료마다(per-response)** 발화. 세션 마감(close) 의도와 불일치하며, Stop 의 stdout 은 컨텍스트로 전달되지 않아 실질 효과도 없음.
- **대체 경로**: 세션 마감은 사용자의 "세션 정리" 요청 시 close 스크립트 수동 호출로 일원화 (아래 "스크립트 단독 호출" 참조).
- **재도입 가드**: `scripts/verify_hooks.py` 항목 2 가 이 파일의 부재를 검증한다. 재도입하려면 검증기와 이 README 를 함께 개정할 것.

## 활성화 조건 (양쪽 분기)

- **CLI v3 hook 을 활성하려는 경우**: `.kiro/hooks/*.json` 을 그대로 두면 kiro-cli v3 가 세션 시작 시 자동 로드.
- **CLI v3 hook 을 활성하지 않으려는 경우**: 해당 JSON 파일을 삭제하거나 이동. 스크립트는 사용자가 직접 호출 가능하므로 프로토콜 준수에 지장 없음.

- **IDE hook 을 활성하려는 경우**: Kiro IDE 가 `.kiro.hook` 형식을 최종 확정한 뒤 skeleton 을 정식 규격으로 조정 (Phase 5 회귀 검증 항목).
- **IDE hook 을 활성하지 않으려는 경우**: `.kiro.hook` 파일은 skeleton 상태이므로 삭제해도 무방.

## 스크립트 단독 호출

hook 자동 로드를 원하지 않을 때 (또는 hook 규격 확정 전) 아래 명령으로 동일 결과 확보:

```powershell
python .kiro\scripts\mickey_session_boot.py --project-root .
python .kiro\scripts\mickey_session_close.py --project-root .
```

옵션 상세는 각 스크립트의 `--help` 참조.

## 검증

`scripts\verify_hooks.py` 로 파일 존재 · 형식 · 스크립트 단독 실행 · BRANCH 마커를 자동 확인.
