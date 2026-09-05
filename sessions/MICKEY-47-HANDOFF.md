# Mickey 47 Handoff

## Current Status

Serena 활성 프로젝트 오지정 **근본 원인 규명 + Option A 적용 완주**. 원인은 M46 인계 가설(상대 경로 "." cwd 해석)이 아니라 **활성 agent JSON의 `--project C:\...\work\kiro` 하드코딩**(글로벌 mcp.json을 통째 override, 7주+ 잠복 — 프로세스 cmdline 실측으로 입증). 조치: ① agent JSON + 글로벌 mcp.json에서 `--project` 제거 (fail-closed, 백업 `.bak-m47-serena`) ② T1.5 v28 §19.3 "Serena 세션 활성화 규약" 신설 + repo 세대 파일 hash 동기화 ③ 본 세션 activate_project 실증. Curator 검증 5/5 PASS → **git diff 자동 보고 옵션화 확정**. 승격 2/2 (tool-implicit-root-path-trap / prompt-doc-vs-runtime-loading augment) + adaptive #18.

## Next Steps (M48 — 사용자 합의 플랜, 2026-09-05)

M48은 "기존 활성 세션 전부 정리 후" 시작되는 세션이다. 시작 직후 순서:
1. **Option A 첫 실측 검증**: 새 세션 serena가 프로젝트 미지정으로 기동하는지 확인 → `activate_project <절대 경로>` → 활성 확인 (T1.5 v28 §19.3 — 활성화 확인 전 Serena 쓰기 도구 금지)
2. **기존 세션 종료 실측**: `python scripts/m47_serena_process_probe.py` → kiro-cli/serena 프로세스가 자기 자신 것만 남았는지 확인 (눈대중 금지)
3. **보류 정리 (D-47-2)** — 자기 serena도 serena_config.yml 공유자이므로 다른 등록 이벤트 전 세션 초반 수행 + 편집 후 파일 재독:
   - serena_config.yml 쓰레기 등록 제거 (후보: `work`, `work\kiro`, `AppData\Local\Programs\Kiro`, `.kiro\crew\workspace` — 실 사용 여부 사용자 확인 후)
   - `work\kiro\.serena\` 처분 (memories 내용 확인 후)
   - 미아 세션 파일 2건 처분: `work\kiro\MICKEY-7-SESSION.md`(bvt-anjin-comparison), `MICKEY-24-SESSION.md`(epic-lore-benchmark)
4. **invoke_curator.py 개선**: run 완료 후 augment 번들의 `Base-Hash: pending`을 실제 sha256으로 자동 기입하는 단계 코드화 (이번 세션 CONFLICT 오탐의 근본 해결 — Curator는 해시 계산 불가, 결정론 작업은 코드로). 수정 시 adaptive #16 (repo scripts → m43_deploy_global_scripts.py 재배포 세트) 준수

## Important Context (SESSION/auto_notes에 없는 것만)

- 실행 중이던 구세션들은 구설정(work\kiro 고정)으로 떠 있었음 — M48 시점엔 전부 종료됐을 것이나 2번 실측으로 확정할 것
- kirocrew.json의 serena는 여전히 `--project .` (fail-wrong 내재) — 해당 agent 사용 시점에 동일 수정 권장
- FILE-STRUCTURE.md(M35)/ENVIRONMENT.md(M37) 노후 — ENVIRONMENT는 Code Analysis Tools에 fail-closed 규약 반영 겸 갱신 후보
- 글로벌 staging 잔존물 1건 (remember-inline-shell-ban.md, Source: unreal-mcp-demo M1) — 외부 소속 skip 유지

## Protocol Feedback

- [Protocol] invoke_curator→promote 파이프라인의 Base-Hash 계약 결함 발견 (위 Next Steps 4번) — 검증 기간 5회차에 형식 결함이 처음 표면화된 것은 이번이 첫 augment+pending 조합이었기 때문
- [Protocol] §22 원스트라이크 1회 발동 (`&` 체이닝, 5회째 재발) — 발동 후 잔여 세션 위반 0

## Quick Reference

- 세션 메인: `MICKEY-47-SESSION.md` (증거 사슬 8항 + D-47-1/2)
- 신규 스크립트: `scripts/m47_serena_process_probe.py` (프로세스 실측), `scripts/m47_verify_serena_config.py`, `scripts/m47_fix_bundle_basehash.py`
- 백업: `~/.kiro/agents/ai-developer-mickey.json.bak-m47-serena`, `~/.kiro/settings/mcp.json.bak-m47-serena`, `~/.kiro/mickey/extended-protocols.md.bak-ai-developer-mickey-m47` (안정 확인 후 삭제 대상)
- Context window: 종료 시점 ~70%. M48은 fresh context 필수
