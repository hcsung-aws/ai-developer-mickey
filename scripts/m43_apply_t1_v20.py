# -*- coding: utf-8 -*-
"""M43: T1 시스템 프롬프트 v19→v20 — Session End 2단계 Curator 호출 코드화.

배경 (D-43): "같은 프로젝트 동시 큐레이션 회피"가 지시 기반이라 감지 수단이 없었음.
invoke_curator.py가 curation 락 검사를 호출과 같은 코드 경로에 내장 — 락을 잡지
못하면 Curator가 실행되지 않는다. 3단계 완료 후 release 의무 추가.

대상: 1) ~/.kiro/agents/ai-developer-mickey.json (활성 런타임)
      2) {repo}/examples/ai-developer-mickey.json (install 배포원)

변경 4건 (prompt 필드 내부 문자열, safe-batch-replace count-1 guard):
1. Session End 2단계: use_subagent → invoke_curator.py run
2. Session End 3단계: 처리 완료 후 release 의무 추가
3. Version 19 → 20
4. Changes 갱신

백업: .bak-ai-developer-mickey-m43. 판정: 리포트 파일 실측 (adaptive #14).
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HOME_JSON = Path.home() / ".kiro" / "agents" / "ai-developer-mickey.json"
REPO_JSON = Path(__file__).resolve().parent.parent / "examples" / "ai-developer-mickey.json"
OUT = Path(__file__).resolve().parent / "output" / "m43_t1_v20.txt"

EDITS = []

# 1) Session End 2단계 — 호출 코드화
EDITS.append((
    """2. **Knowledge Curator 호출**: SESSION.md + 프로젝트 경로를 knowledge-curator agent에 use_subagent(동기)로 호출 — delegate 금지 (전역 상태가 멀티 세션 crosstalk 유발, T1.5 §17 전송 규약). Curator는 글로벌을 쓰지 않는다(격리 원칙) — ① adaptive.md만 직접 수정, ② 모든 승격 후보(글로벌 domain은 gd- 번들, 그 외 ck-/cr-/pat-/remember-)를 프로젝트 _curator-staging/에 초안 작성. 완주 판정은 응답 표면이 아닌 staging 파일 디스크 실측으로. 실패/미완주 시 메인 세션이 직접 대행 — 격리 구조상 안전. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)""",
    """2. **Knowledge Curator 호출**: `python ~/.kiro/mickey/scripts/invoke_curator.py run --project . --session MICKEY-N-SESSION.md --owner "<프로젝트> Mickey N"` 실행 — 유일한 코드 진입점. use_subagent/delegate 직접 호출 금지 (curation 락 우회, T1.5 §17 호출 규약). 스크립트가 락 획득 → headless Curator 실행 → staging diff 디스크 실측 → 리포트를 일괄 수행. BUSY(락 선점) 시 보유자/경과 시간을 사용자에게 보고하고 사용자 승인 하에만 --force 강제 진입. 실패/타임아웃 시 락 유지 상태 — 메인 세션이 락 아래서 직접 대행 (격리 구조상 안전). Curator는 글로벌을 쓰지 않는다(격리 원칙) — ① adaptive.md만 직접 수정, ② 모든 승격 후보(글로벌 domain은 gd- 번들, 그 외 ck-/cr-/pat-/remember-)를 프로젝트 _curator-staging/에 초안 작성. 첫 5회 호출 동안 동작 후 git diff 자동 보고 (검증 기간, T1.5 §17 참조)""",
))

# 2) Session End 3단계 — release 의무
EDITS.append((
    """승인된 gd- 번들은 promote_knowledge.py로 글로벌 승격 (락 직렬화 + 무결성 검증 + 리포트 — T1.5 §17 락 규약), 그 외 승인분은 staging → 정식 위치 이동, 미승인분 폐기""",
    """승인된 gd- 번들은 promote_knowledge.py로 글로벌 승격 (락 직렬화 + 무결성 검증 + 리포트 — T1.5 §17 락 규약), 그 외 승인분은 staging → 정식 위치 이동, 미승인분 폐기. 처리 완료 후 `invoke_curator.py release`로 curation 락 해제 (필수 — 잊으면 다음 세션이 BUSY로 차단됨)""",
))

# 3) 버전 푸터
EDITS.append((
    """**Version**: 19
**Last Updated**: 2026-08-19""",
    """**Version**: 20
**Last Updated**: 2026-08-22""",
))

# 4) Changes 갱신
EDITS.append((
    """**Changes**: Session End 2단계 Curator 전송 전환 (M42): delegate → use_subagent(동기). 근거: delegate 전역 상태(.subagents, agent 이름 키 + user_notified 선점 + status 폴링)가 session-agnostic이라 멀티 세션 crosstalk/replace 실측. 완주 판정은 staging 디스크 실측 (Kiro #6765 채널 절단 대비), 실패 시 직접 대행. T1.5 §17 v24 전송 규약과 연동""",
    """**Changes**: Session End 2단계 Curator 호출 코드화 (M43): use_subagent → invoke_curator.py 유일 진입점. curation 락(프로젝트 로컬, 자동 회수 없음 + --force human-in-the-loop)을 호출 코드 경로에 내장 — 같은 프로젝트 동시 큐레이션을 코드로 차단. 3단계 후 release 의무. 완주 판정 디스크 실측은 스크립트에 내장. T1.5 §17 v25 호출 규약과 연동""",
))


def apply(json_path: Path, report: list) -> bool:
    bak = json_path.with_suffix(json_path.suffix + ".bak-ai-developer-mickey-m43")
    if not bak.exists():
        shutil.copy2(json_path, bak)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    prompt = data["prompt"]
    for i, (old, new) in enumerate(EDITS, 1):
        n = prompt.count(old)
        if n != 1:
            report.append(f"[FAIL] {json_path.name} edit {i}: count={n} (기대 1)")
            return False
        prompt = prompt.replace(old, new)
    data["prompt"] = prompt
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    report.append(f"[OK] {json_path.name}: 4건 적용 (백업 {bak.name})")
    return True


def main() -> int:
    report, ok = [], True
    for target in (HOME_JSON, REPO_JSON):
        ok &= apply(target, report)
    if ok:
        p1 = json.loads(HOME_JSON.read_text(encoding="utf-8"))["prompt"]
        p2 = json.loads(REPO_JSON.read_text(encoding="utf-8"))["prompt"]
        checks = [
            (p1 == p2, "HOME == REPO prompt"),
            ("invoke_curator.py run" in p1, "신규 키워드: invoke_curator.py run"),
            ("invoke_curator.py release" in p1, "신규 키워드: release 의무"),
            ("**Version**: 20" in p1, "Version 20"),
            ("use_subagent(동기)로 호출" not in p1, "구 문구 잔존 0 (use_subagent 호출)"),
            ("**Version**: 19" not in p1, "구 버전 잔존 0"),
        ]
        for cond, label in checks:
            report.append(f"[{'PASS' if cond else 'FAIL'}] {label}")
            ok &= cond
    report.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(report), encoding="utf-8")
    print(f"written: {OUT} ({'ALL PASS' if ok else 'FAIL'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
