# -*- coding: utf-8 -*-
"""M43: §17 v24→v25 — Curator 호출 코드화 (invoke_curator.py) + curation 락 규약.

대상 (adaptive #3: global 수정 시 repo 미러 동기화):
1. ~/.kiro/mickey/extended-protocols.md (글로벌)
2. {repo}/mickey/extended-protocols.md (repo 미러)

변경 3건 (safe-batch-replace count-1 guard):
1. 다이어그램: use_subagent → invoke_curator.py run
2. 전송 규약 소절 (M42) → 호출 규약 소절 (M43) 교체
3. Version 24 → 25 + Changes (v25)

백업: 글로벌 .bak-ai-developer-mickey-m43 사전 생성. 판정: 리포트 파일 실측.
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GLOBAL_MD = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO_MD = Path(__file__).resolve().parent.parent / "mickey" / "extended-protocols.md"
OUT = Path(__file__).resolve().parent / "output" / "m43_protocols_v25.txt"

# 교체 대상 소절 (v24 원문) — 파일에서 읽어 count 검증하므로 앵커만 정의
OLD_SECTION_HEAD = "### Curator 호출 전송 규약 (M42)"
OLD_SECTION_TAIL = "### 분기 판단 기준 (Curator 내부)"

NEW_SECTION = """### Curator 호출 규약 (M43 — 코드 진입점)

Curator 호출은 **invoke_curator.py 실행**으로만 수행한다. **delegate 사용 금지.** use_subagent 직접 호출도 락을 우회하므로 금지.

```
python ~/.kiro/mickey/scripts/invoke_curator.py run --project . \\
    --session MICKEY-N-SESSION.md --owner "<프로젝트> Mickey N"
```

- 코드 강제 지점: 스크립트가 curation 락을 잡지 못하면 Curator는 실행되지 않는다 — 동시 큐레이션 회피가 지시가 아닌 코드로 보장됨 (promote와 동일한 LLM 결정론적 하이브리드)
- 전송: `kiro-cli chat --agent knowledge-curator --no-interactive` 자식 프로세스, stdout 파이프 in-band 수신. delegate의 전역 랑데부 저장소(`.subagents/` + `user_notified` 선점 = crosstalk 원흉)를 경유하지 않음 (M43 probe 실측: in-band + .subagents 무변화)
- 완주 판정: 스크립트가 staging 전후 diff를 디스크 실측하여 리포트 출력 (`curator-invoke-report-*.txt`) — 응답 표면 신뢰 금지 규약의 코드화
- 실패/타임아웃 시: 락 유지(state=held) 상태로 종료 — 메인 세션이 **락 아래서** 직접 대행 후 release

#### curation 락 (mickey_lock 공유 모듈 — promote 락과 코드 통합, 파일은 스코프별 분리)

- 위치: `{프로젝트 staging}/.curation.lock/` (프로젝트 로컬 — mkdir 원자성 + owner.json)
- **자동 회수 없음**: 선점 락 발견 시 보유자/경과 시간 보고 후 중단(BUSY). 크래시 잔여물일 수 있으니 사람이 확인한 뒤 `--force` 로만 강제 진입 (human-in-the-loop)
- run 성공 후에도 해제하지 않고 **state=awaiting-merge** 유지 — staging 머지/폐기(Session End 3단계)도 공유 자원 조작이므로. 3단계 완료 후 `invoke_curator.py release` 필수
- 여러 세션의 동시 큐레이션: 타 프로젝트 병렬은 구조적 안전 (쓰기 대상이 각 프로젝트 로컬 + 글로벌은 promote 락). 같은 프로젝트는 curation 락이 코드로 차단

"""


def apply(md_path: Path, report: list) -> bool:
    text = md_path.read_text(encoding="utf-8")

    # 1) 다이어그램 문구
    old_diag = ("Knowledge Curator (use_subagent 동기 호출 — 결과 in-band 반환. "
                "실패/미완주 시 메인 세션이 직접 대행, 격리 구조상 항상 안전)")
    new_diag = ("Knowledge Curator (invoke_curator.py run — curation 락 아래 headless 실행, "
                "완주 판정 디스크 실측. 실패 시 메인 세션이 락 아래서 직접 대행)")

    # 2) 소절 교체: HEAD~TAIL 사이 전체를 NEW_SECTION으로
    head_i = text.count(OLD_SECTION_HEAD)
    tail_i = text.count(OLD_SECTION_TAIL)
    if text.count(old_diag) != 1 or head_i != 1 or tail_i != 1:
        report.append(f"[FAIL] {md_path}: 앵커 count 불일치 "
                      f"(diag={text.count(old_diag)}, head={head_i}, tail={tail_i})")
        return False
    text = text.replace(old_diag, new_diag)
    start = text.index(OLD_SECTION_HEAD)
    end = text.index(OLD_SECTION_TAIL)
    text = text[:start] + NEW_SECTION + text[end:]

    # 3) 버전 푸터
    old_ver = "**Version**: 24\n**Last Updated**: 2026-08-19\n**Changes (v24)**:"
    new_ver = ("**Version**: 25\n**Last Updated**: 2026-08-22\n"
               "**Changes (v25)**: §17 Curator 호출 코드화 (ai-developer-mickey M43): "
               "use_subagent → invoke_curator.py 유일 진입점. curation 락(프로젝트 로컬, mkdir 원자성, "
               "자동 회수 없음 + --force human-in-the-loop, awaiting-merge 상태 유지)을 호출과 같은 "
               "코드 경로에 내장 — 같은 프로젝트 동시 큐레이션을 지시가 아닌 코드로 차단. "
               "전송은 headless 자식 프로세스 stdout in-band (M43 probe: .subagents 무변화). "
               "완주 판정 디스크 실측도 스크립트에 내장. mickey_lock.py로 promote 락과 코드 통합. T1 v20 연동.\n"
               "**Changes (v24)**:")
    if text.count(old_ver) != 1:
        report.append(f"[FAIL] {md_path}: 버전 푸터 count={text.count(old_ver)}")
        return False
    text = text.replace(old_ver, new_ver)

    md_path.write_text(text, encoding="utf-8")
    report.append(f"[OK] {md_path}: 3건 적용")
    return True


def main() -> int:
    report, ok = [], True
    # 백업 (글로벌만 — repo는 git 추적)
    bak = GLOBAL_MD.with_name(GLOBAL_MD.name + ".bak-ai-developer-mickey-m43")
    if not bak.exists():
        shutil.copy2(GLOBAL_MD, bak)
    report.append(f"[BAK] {bak.name}")

    for md in (GLOBAL_MD, REPO_MD):
        ok = apply(md, report) and ok

    # 적용 후 두 파일 동일성 검증
    same = GLOBAL_MD.read_bytes() == REPO_MD.read_bytes()
    report.append(f"[SYNC] global==repo: {same}")
    ok = ok and same

    report.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
