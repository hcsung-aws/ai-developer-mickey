"""Mickey 31~35 CLI 트랙 분리 commit 스크립트.

M30(51e1b40) 이후 4세션(+M35) 미반영 변경분이 누적. adaptive rule #5 위반.
CLI 트랙 산출물만 세션별로 분리 커밋하여 논리 단위 유지 + 병렬 v10 트랙과 격리.

세션 매핑:
- M31: 경량 포스트모템 + safe-batch-replace 9세대 보강
- M32: v17 프로토콜 (T1.5 §19 + T1 SESSION PROTOCOL 4a) + 도구 3-Tier 통합
- M33: Kiro CLI Tier 3 LSP baseline 활성화 + Windows PATH 확장 표준
- M34: 지식 그래프 시각화 도구 (Phase 1+1.5+2, WELC harness)
- M35: 지식 그래프 시각화 Phase 3 UI (필터+이웃 강조) + 문서 정합성 복원

사용법:
    python scripts/m35_split_commits.py           # dry-run (기본)
    python scripts/m35_split_commits.py --execute # 실제 커밋

각 커밋 전 파일 목록 표시. missing 파일은 경고 후 스킵. 실행 실패 시 즉시 중단.

주의:
- 병렬 v10 트랙 파일은 명시적으로 제외 (examples/, power-mickey/, session_history/, IMPROVEMENT-PLAN v10/progressive, docs/v2-to-v3-mapping.md, mickey/README.md, backup zip 등)
- M34/M35 겹침 파일(templates/graph.html.tmpl, tests/test_renderer.py, ROADMAP.md)은 M35 커밋에 최종 상태로 포함
- MICKEY-35-HANDOFF.md 는 세션 종료 시 생성 후 M35 커밋에 포함 (본 스크립트 실행 전 존재 확인)
- master 직접 push 는 회피 원칙 (본 스크립트는 push 하지 않음, 사용자 결정)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

# adaptive #8: Windows cp949 환경에서 한글 출력 안전
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 세션별 커밋 스코프 정의 (파일 경로는 ROOT 기준 상대)
# ---------------------------------------------------------------------------

COMMITS = [
    {
        "session": "M31",
        "name": "Mickey 31",
        "message": """Mickey 31: 경량 포스트모템 + safe-batch-replace 9세대 보강

- M21 baseline 이후 10세션 임계 자동 트리거로 경량 포스트모템 수행
- 5개 프로젝트 162개 [Protocol] 태그 수집 + v9.1 6개 변경 판정
- 메타 신호 식별 (§9 자동 트리거가 §18 잠복 가드 우회) → 같은 세션에서 §9 보강 (extended-protocols.md 갱신은 M32 재갱신에 흡수)
- safe-batch-replace 9세대 보강: post-check 를 `written.count(new) == 1` + `old not in written` 결합으로 변경 (M30 발견 False FAIL 함정 회피)
""",
        "files": [
            "sessions/MICKEY-31-SESSION.md",
            "sessions/MICKEY-31-HANDOFF.md",
            "scripts/m31_apply.py",
            "common_knowledge/safe-batch-replace.md",
        ],
    },
    {
        "session": "M32",
        "name": "Mickey 32",
        "message": """Mickey 32: v17 프로토콜 (T1.5 §19 + T1 SESSION PROTOCOL 4a) + 도구 3-Tier 통합

- T1.5 §19 External Code Analysis Integration 신설 (Tier 1 Serena/Graphify + Tier 2 사용자 확인 + Tier 3 Kiro CLI 내장 `code` baseline)
- §1 Brownfield Phase 2 축소 (도구 위임)
- T1 (agent JSON) SESSION PROTOCOL 4a + DOCUMENT SCHEMA FILE-STRUCTURE 스키마 필수/선택 분리
- 글로벌+repo mickey/extended-protocols.md v17 최종 상태 (hash 9B3CEB...)
- docs/07-changelog.md v9.2 상세 (M31 자기 정정 + M32 §19 신설 누적)
- safe-batch-replace 10세대 안정 (Phase A 3건 + Phase B 4건 JSON escape 회피)
- Phase A~D 일괄 자율 진행 성공 (batch-confirm-autonomous-proceed 12+회)
- Note: examples/ai-developer-mickey.json v17 반영분은 별도 커밋 스코프 (본 커밋 제외)
""",
        "files": [
            "sessions/MICKEY-32-SESSION.md",
            "sessions/MICKEY-32-HANDOFF.md",
            "scripts/m32_precheck.py",
            "scripts/m32_apply_protocols.py",
            "scripts/m32_apply_agent_json.py",
            "mickey/extended-protocols.md",
            "docs/07-changelog.md",
        ],
    },
    {
        "session": "M33",
        "name": "Mickey 33",
        "message": """Mickey 33: Kiro CLI Tier 3 LSP baseline 활성화 + Windows PATH 확장 표준

- TypeScript LSP 5.3.0 + Pyright 1.1.411 + clangd 22.1.6 설치 (Rust 사용자 결정으로 건너뜀)
- Windows 사용자 PATH 확장 (Pyright + clangd bin) — winreg.SetValueEx + WM_SETTINGCHANGE broadcast 표준 조합
- setx 1024자 잘림 / PowerShell 인용부호 지옥 회피 (REG_EXPAND_SZ 유지)
- 12 entries total, 2 신규 (백업: scripts/backup/user-path-m33-20260702-001352.txt)
- Curator 승인 지식 2건 추가:
  * common_knowledge/windows-user-path-extension.md
  * common_knowledge/kiro-cli-lsp-init-settings-location.md (§19.2 감지 마커 불일치 근거)
- Note: 글로벌 machine-env.md LSP Servers 섹션 append 는 사용자 홈이라 repo 미포함
- §19 첫 실전 적용 성공 + batch-confirm-autonomous-proceed 13+회 누적
""",
        "files": [
            "sessions/MICKEY-33-SESSION.md",
            "sessions/MICKEY-33-HANDOFF.md",
            "scripts/m33_probe_lsp_deps.py",
            "scripts/m33_install_clangd.py",
            "scripts/m33_backup_user_path.py",
            "scripts/m33_extend_user_path.py",
            "scripts/m33_verify_path_registry.py",
            "scripts/m33_cleanup_staging.py",
            "scripts/backup/user-path-m33-20260702-001352.txt",
            "common_knowledge/windows-user-path-extension.md",
            "common_knowledge/kiro-cli-lsp-init-settings-location.md",
        ],
    },
    {
        "session": "M34",
        "name": "Mickey 34",
        "message": """Mickey 34: 지식 그래프 시각화 도구 (Phase 1+1.5+2, WELC harness)

- 완전 오프라인 self-contained HTML (vis-network 9.1.9 인라인)
- Phase 1: 글로벌 스코프 (~/.kiro/mickey/domain/GRAPH.md + patterns/INDEX.md) 렌더
- Phase 1.5: Graduated 흡수 EXTENDS 엣지 자동 생성 + 물리 옵션 튜닝 + zoom-to-fit + 연결 중심성 기반 노드 크기/border/라벨 규칙
- Phase 2: 프로젝트 스코프 (project_knowledge 노드 + Domain Links CROSS_SCOPE 엣지 + 뷰 스위치 Project/Global/Combined)
- WELC harness: models/parser/builder 계층별 유닛 테스트 + fixture 기반 스냅샷 (M34 시점 89 tests, M35에서 확장)
- CLI: `python scripts/mickey_graph_viz.py --scope global/project`
- Note: templates/graph.html.tmpl, tests/test_renderer.py, ROADMAP.md 는 M35 Phase 3 UI 반영분과 함께 M35 커밋에 최종 상태 포함
- 파생 산출물:
  * common_knowledge/knowledge-file-relation-annotation.md (INDEX Domain Links out-of-sync 발견)
  * IMPROVEMENT-PLAN-project-knowledge-index-sync.md (개선안, 후속 세션 처리)
- .gitignore 신규: vendor/output/__pycache__/pytest_cache/pre-v10-bak.zip + .kiro/.serena/ (본 커밋에 포함)
- SESSION.md 냉동 원인: 마지막 대화 시점 최종 갱신 누락 (M35 진입 시 실측으로 실 진척 파악)
""",
        "files": [
            "sessions/MICKEY-34-SESSION.md",
            "scripts/mickey_graph/__init__.py",
            "scripts/mickey_graph/models.py",
            "scripts/mickey_graph/parser.py",
            "scripts/mickey_graph/graph_builder.py",
            "scripts/mickey_graph/renderer.py",
            "scripts/mickey_graph_viz.py",
            "scripts/setup_vendor.py",
            "scripts/verify_offline.py",
            "scripts/tests/__init__.py",
            "scripts/tests/conftest.py",
            "scripts/tests/test_parser.py",
            "scripts/tests/test_graph_builder.py",
            "scripts/tests/fixtures/sample-graph.md",
            "scripts/tests/fixtures/sample-patterns-index.md",
            "scripts/tests/fixtures/sample-project-auto-notes.md",
            "scripts/tests/fixtures/sample-project-common-knowledge.md",
            "scripts/tests/fixtures/sample-project-context-rule.md",
            ".gitignore",
            "common_knowledge/knowledge-file-relation-annotation.md",
            "IMPROVEMENT-PLAN-project-knowledge-index-sync.md",
        ],
    },
    {
        "session": "M35",
        "name": "Mickey 35",
        "message": """Mickey 35: 지식 그래프 시각화 Phase 3 UI (필터+이웃 강조) + 문서 정합성 복원 + Curator 정식 호출

- **Phase 3 UI** (template + JS 확장, renderer.py 무변경):
  * 태그 chip 필터 (빈도순 정렬, count 표시, All/None 버튼) — B 개선: count>=2 임계값 + Show all/Hide singletons 토글 + max-height 110px 스크롤 (다태그 380+ 데이터셋 대응)
  * 노드 kind 5종 + 엣지 type 6종 체크박스 (색상 swatch 병기)
  * 이웃 1-hop 강조 (opacity 조작, 노드 0.15/엣지 0.05 dim, 배경 클릭 시 원상복구 + 상세 초기화)
  * 노드 그룹핑(Phase 3 T2d) 재평가 결과: 생략 (태그 chip UX 중복 + kind legend 색상 충돌 위험)
- **WELC 회귀**: pytest 89 → 97 (Phase 3 회귀 8건) → 101 (B 개선 4건)
- **6개 UX 시나리오 브라우저 검증 통과**: 태그 chip 토글 / Show all 토글 / Kind 필터 / Edge type 필터 / 노드 클릭 이웃 강조+상세 / 배경 클릭 복원
- **T3 문서 정합성 복원**:
  * scripts/mickey_graph/ROADMAP.md — Phase 2/3 완료 표시 + 상세 구현 요약
  * common_knowledge/mickey-graph-visualization.md 신규 (사용법/UI 매핑/Phase 4 계획/재사용 원칙)
  * common_knowledge/INDEX.md — mickey-graph-visualization 등재 + data-view-preseeding-immutability Domain Backlink
  * FILE-STRUCTURE.md — scripts/mickey_graph 트리 반영, .serena 감지 갱신, Steering Trigger 재분석 도달 표기, Key Files 4건 추가
- **Curator 정식 호출** (4세션 우회 후 첫 정상 응답):
  * 글로벌 domain/entries/data-view-preseeding-immutability.md 신규 생성 (Data-View pre-seeding으로 Renderer 불변)
  * adaptive.md 규칙 #9 추가 (SESSION 냉동 vs 디스크 실측 분리 취급)
  * context_rule/INDEX.md 트리거 확장
  * Pre-staged 후보 없음 (승격 대상 없음)
- MICKEY-34 실측 발견: SESSION 냉동 vs Phase 2 완료 상태 불일치 → must-follow-rules "새 세션 진입 시 디스크 재확인" 원칙 정확 발현
- **CLI 트랙 세션 분리 커밋 완결**: M31~M35 5개 커밋, 병렬 v10 트랙과 파일 격리 (adaptive #4/#5 준수)
""",
        "files": [
            "sessions/MICKEY-35-SESSION.md",
            "sessions/MICKEY-35-HANDOFF.md",
            "scripts/mickey_graph/templates/graph.html.tmpl",
            "scripts/mickey_graph/ROADMAP.md",
            "scripts/tests/test_renderer.py",
            "common_knowledge/mickey-graph-visualization.md",
            "common_knowledge/INDEX.md",
            "context_rule/adaptive.md",
            "context_rule/INDEX.md",
            "FILE-STRUCTURE.md",
            "scripts/m35_split_commits.py",
        ],
    },
]


# ---------------------------------------------------------------------------
# 실행 헬퍼
# ---------------------------------------------------------------------------

def run(cmd: list[str], *, execute: bool, cwd: Path = ROOT) -> None:
    """git 명령 실행 (또는 dry-run 표시). 실패 시 CalledProcessError."""
    display = " ".join(cmd)
    if execute:
        print(f"  RUN: {display}")
        subprocess.run(cmd, cwd=cwd, check=True)
    else:
        print(f"  [DRY-RUN] {display}")


def check_git_status(execute: bool) -> None:
    """현재 git 상태가 clean 하지 않으면 (staged 항목이 있으면) 초기화."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=ROOT, check=True, capture_output=True, text=True
    )
    if result.stdout.strip():
        print("  Warning: staging area not empty, resetting first")
        run(["git", "reset"], execute=execute)


def commit_session(commit: dict, execute: bool) -> None:
    """세션별 파일 추가 + 커밋. 파일 존재 검증 후 실행."""
    print(f"\n=== {commit['session']}: {commit['name']} ===")

    existing: list[str] = []
    missing: list[str] = []
    for rel in commit["files"]:
        if (ROOT / rel).exists():
            existing.append(rel)
        else:
            missing.append(rel)

    if missing:
        print(f"  MISSING ({len(missing)}) — skipped:")
        for m in missing:
            print(f"    ! {m}")

    print(f"  ADD ({len(existing)}):")
    for f in existing:
        print(f"    + {f}")

    if not existing:
        print("  SKIP: no files to commit")
        return

    # git add (경로 리스트 방식 — glob 없음)
    run(["git", "add", "--"] + existing, execute=execute)

    # git commit -F <임시 파일> (multi-line 메시지 안전 처리)
    if execute:
        # 임시 파일에 커밋 메시지 기록 후 -F 옵션으로 전달
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".txt", delete=False
        ) as tmp:
            tmp.write(commit["message"].strip() + "\n")
            tmp_path = tmp.name
        try:
            run(["git", "commit", "-F", tmp_path], execute=execute)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    else:
        # dry-run 은 메시지 첫 줄만 표시
        first_line = commit["message"].strip().splitlines()[0]
        print(f"  [DRY-RUN] git commit -F <tmp> ({first_line!r})")


def show_final_log(execute: bool) -> None:
    """최종 git log 표시 (검증용)."""
    if not execute:
        print("\n[DRY-RUN] Final log check skipped")
        return
    print("\n=== Final git log (last 10) ===")
    subprocess.run(["git", "log", "--oneline", "-10"], cwd=ROOT, check=False)


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Mickey 31~35 CLI 트랙 분리 commit",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help="실제 git 명령 실행 (기본은 dry-run)"
    )
    parser.add_argument(
        "--only", type=str, default=None,
        help="특정 세션만 실행 (콤마 분리 가능, 예: M31,M32,M33,M34). 기본은 전 세션 순차"
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    print(f"Mode: {'EXECUTE' if args.execute else 'DRY-RUN'}")
    print(f"Repo: {ROOT}")

    check_git_status(execute=args.execute)

    targets = COMMITS
    if args.only:
        only_set = {s.strip().upper() for s in args.only.split(",") if s.strip()}
        targets = [c for c in COMMITS if c["session"] in only_set]
        if not targets:
            print(f"ERROR: no commit spec matches '{args.only}'",
                  file=sys.stderr)
            return 2
        print(f"Filter: {sorted(c['session'] for c in targets)}")

    for commit in targets:
        try:
            commit_session(commit, execute=args.execute)
        except subprocess.CalledProcessError as e:
            print(f"\nERROR: {commit['session']} failed with rc={e.returncode}",
                  file=sys.stderr)
            print("Aborting — resolve issue and re-run remaining sessions with --only",
                  file=sys.stderr)
            return 1

    show_final_log(execute=args.execute)
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
