# .kiro/hooks/ — Mickey 세션 hook

**성격**: v1 JSON hook — Kiro CLI v3 와 Kiro IDE 1.0 **공용 규격** (kiro.dev/docs/hooks.md, 2026-07-17 실측 확정). Mickey 프로토콜 부팅을 자동화한다. hook 없이도 스크립트 단독 호출로 동일 동작 가능.

**세션 기록 규약**: D-0717-1 (날짜+UID) — `DECISIONS.md` / kickoff 문서 §2 참조.

## 파일 목록

| 파일 | 대상 | 트리거 | 실행 스크립트 |
|------|------|--------|--------------|
| `mickey-session-start.json` | CLI v3 + IDE 1.0 공용 | `SessionStart` | `.kiro/scripts/mickey_session_boot.py` |

boot 스크립트는 stdout 리포트로 P3 분기 4종(PURPOSE-SCENARIO / HANDOFF / BROWNFIELD / MCP-TOOLS)을 알린다. HANDOFF 분기는 최신 `*-handoff.md`(mtime) + UID 를 제시하며, **자동 진행하지 않고 사용자 확인을 요구**한다 (D-0717-1 이어가기 절차).

## 폐기 이력

### 2026-07-19 — legacy `.kiro.hook` 2종 삭제 (D-0717-2, 세션 551c3f)

`mickey-pre-task.kiro.hook` (preTaskExecution) / `mickey-post-task.kiro.hook` (postTaskExecution) 삭제.
- **근거**: IDE 1.0 은 legacy when/then `.kiro.hook` 규격을 **로딩하지 않는다** (패널에 upgrade badge 만 표시, 마이그레이션 전 미실행 — kiro.dev/docs/whats-new-1-0.md). 구/신 양쪽 규격에서 무효.
- **대체 경로**: 신규격(v1 JSON)은 CLI/IDE 공용이므로 `mickey-session-start.json` 하나로 양쪽 커버. 세션 마감은 close 스크립트 수동 호출 (아래 참조).
- **재도입 가드**: `scripts/verify_hooks.py` 항목 3 이 `.kiro/hooks/*.kiro.hook` 부재를 검증한다.

### 2026-07-15 — `mickey-session-stop.json` 폐기 (F5)

`Stop` → `mickey_session_close.py` hook 폐기.
- **근거**: 프로브 실측 결과 `Stop` 트리거는 세션 종료가 아니라 **응답 종료마다(per-response)** 발화. 세션 마감(close) 의도와 불일치하며, Stop 의 stdout 은 컨텍스트로 전달되지 않아 실질 효과도 없음.
- **대체 경로**: 세션 마감은 사용자의 "세션 정리" 요청 시 close 스크립트 수동 호출로 일원화.
- **재도입 가드**: `scripts/verify_hooks.py` 항목 2 가 이 파일의 부재를 검증한다.

재도입하려면 검증기와 이 README 를 함께 개정할 것.

## 활성화 조건 (양쪽 분기)

- **hook 을 활성하려는 경우**: `.kiro/hooks/*.json` 을 그대로 두면 CLI v3 / IDE 1.0 이 세션 시작 시 자동 로드.
- **hook 을 활성하지 않으려는 경우**: 해당 JSON 파일을 삭제하거나 이동. 스크립트는 사용자가 직접 호출 가능하므로 프로토콜 준수에 지장 없음.

## 스크립트 단독 호출

hook 자동 로드를 원하지 않을 때 아래 명령으로 동일 결과 확보:

```powershell
python .kiro\scripts\mickey_session_boot.py --project-root .
python .kiro\scripts\mickey_session_close.py --project-root .
python .kiro\scripts\gen_session_uid.py   # 새 세션 UID 발급 (D-0717-1)
```

옵션 상세는 각 스크립트의 `--help` 참조.

## 인코딩 주의 (2026-07-19 실측)

hook 소비자(CLI 런타임)는 stdout 을 UTF-8 로 디코딩한다. boot/close 스크립트는 `sys.stdout.reconfigure(encoding="utf-8")` 로 이를 보장한다 (Windows 기본 cp949 로 인한 mojibake 방지). 새 hook 스크립트를 추가할 때도 동일 처리 필수 — `verify_hooks.py` 항목 7 이 이 계약을 검증한다.

## 검증

`python scripts\verify_hooks.py` — 기준값 **7/7** (2026-07-19 확립. 이전 기준 6/6 은 legacy skeleton 검증 포함 시절의 것).

## Last Updated

2026-07-19 (세션 551c3f — D-0717-2 집행: legacy 삭제 + 전면 개정)
