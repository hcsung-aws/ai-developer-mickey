"""Mickey 22 git 커밋 4건 분할 (T7)

본 세션 변경분이 크므로 논리 단위로 4개 커밋으로 분할:
1. Step 3+4: PURPOSE-SCENARIO + T1.5 §17/§18/§8 stub (v15→v16)
2. Step 5: T1 시스템 프롬프트 5건 변경 (v15→v16)
3. Step 6: README/changelog (한글/영어) + evolution-insight
4. T7: M18~M20 sessions/ 아카이빙 + SESSION/HANDOFF

각 커밋마다 git reset → git add 명시적 추가 → git commit -F (임시 파일 메시지).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

# Windows cp949 stdout 우회
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'C:\Users\hcsung\work\kiro\ai-developer-mickey')


COMMITS = [
    {
        'name': 'Step 3+4',
        'add': [
            'PURPOSE-SCENARIO.md',
            'mickey/extended-protocols.md',
            'scripts/m22_verify_protocols_sync.ps1',
            'scripts/m22_verify_protocols_sync.py',
        ],
        'message': """Mickey 22 Step 3+4: PURPOSE-SCENARIO + T1.5 §17/§18/§8 stub (v15→v16)

- PURPOSE-SCENARIO.md: 3-Tier 진화 루프 (R/G/S) + Knowledge Curator + Pre-staged Apply 명문화
- mickey/extended-protocols.md (Version 15 → 16):
  * §17 Knowledge Lifecycle 신설 (라이프사이클 다이어그램 + Curator 권한 + Pre-staged 5단계 + 5회 검증 기간)
  * §18 Activity Metrics 신설 (baseline 5주 31세션 실측 + 임계값 + 표본 가드)
  * §8 Adaptive Rules 흡수 stub (§9~§16 번호 유지)
- 글로벌(~/.kiro/mickey/extended-protocols.md) + repo 양쪽 동시 갱신, Python hash 일치 검증 (cea8d881...)
- m22_verify_protocols_sync.{ps1,py}: 글로벌/repo 동기화 검증 스크립트
""",
    },
    {
        'name': 'Step 5',
        'add': [
            'examples/ai-developer-mickey.json',
            'scripts/m22_verify_agent_sync.py',
            'scripts/m22_dump_prompt.py',
            'scripts/m22_apply_t1_changes.py',
        ],
        'message': """Mickey 22 Step 5: T1 시스템 프롬프트 5건 변경 (v15 → v16)

변경 5건 (활성 + repo 동시):
A. Continuing Session 1b 엔트로피 체크에 _curator-staging/ dangling 항목 추가
B. Session End 단계 2: Curator delegate (보정된 권한) + 첫 5회 git diff 자동 보고
B. Session End 단계 3: Pre-staged 항목 일괄 제시 + 사용자 단일 응답 (전체/번호/없음/보류)
C. KNOWLEDGE MANAGEMENT 자동 메모리 표 adaptive.md 행 갱신 (Curator 직접 수정 + 5회 git diff 검증)
D. 교훈 승격 절차 Curator 자동 분류로 단순화 (T1.5 §17 참조)
E. 푸터 v15 → v16

활성 + repo Python hash 일치 (86e6a50f...). 277줄 → 273줄, 10008자 → 10307자.
m22_apply_t1_changes.py: 각 패턴 1건 매칭 검증 (count != 1 → RuntimeError) 가드 포함.
""",
    },
    {
        'name': 'Step 6',
        'add': [
            'README.md',
            'README-en.md',
            'docs/07-changelog.md',
            'docs/07-changelog-en.md',
            'docs/08-evolution-insight.md',
        ],
        'message': """Mickey 22 Step 6: README + changelog (한글/영어) + evolution-insight 갱신

- README.md / README-en.md: 진화 표 v9.1 행 추가, footer 에 ADDENDUM 우선 명시 강화
- docs/07-changelog.md / 07-changelog-en.md:
  * 버전 요약 표에 v9.1 행 추가
  * v9.1 (2026-06-19~20) 신규 섹션 ~60줄: Curator 권한 보정 + Pre-staged Apply + T1.5 §17/§18 신설 + T1 변경 + M20→M21 진단 비교 표 + 메타 교훈 + Supersedes
- docs/08-evolution-insight.md: Phase 6 에 4번 '자가 진단의 표본 가드' 추가 (M20→M21 사례 + 3개월 잠복 기간 원칙)
""",
    },
    {
        'name': 'T7',
        'add': [
            'MICKEY-22-SESSION.md',
            'MICKEY-22-HANDOFF.md',
            'scripts/m22_session_cleanup.ps1',
            'MICKEY-18-SESSION.md',
            'MICKEY-18-HANDOFF.md',
            'MICKEY-19-SESSION.md',
            'MICKEY-19-HANDOFF.md',
            'MICKEY-20-SESSION.md',
            'MICKEY-20-HANDOFF.md',
            'sessions/MICKEY-18-SESSION.md',
            'sessions/MICKEY-18-HANDOFF.md',
            'sessions/MICKEY-19-SESSION.md',
            'sessions/MICKEY-19-HANDOFF.md',
            'sessions/MICKEY-20-SESSION.md',
            'sessions/MICKEY-20-HANDOFF.md',
        ],
        'message': """Mickey 22 T7: 엔트로피 정리 + SESSION/HANDOFF (M18~M20 sessions/ 아카이빙)

- M18~M20 SESSION/HANDOFF 6파일 git mv → sessions/ (M21은 본 세션 직전 단계로 루트 유지)
- 임시 dump 3파일 삭제: scripts/_m22_prompt_*.md (Step 5 검증 산출물, 본 세션 종료 후 불필요)
- MICKEY-22-SESSION.md: 18 Completed / 10 Decisions / 7 Lessons
- MICKEY-22-HANDOFF.md: Mickey 23 인계 (Phase 3 5/5 카운터 자동 호출 통합 → Phase 4 마이그레이션)
- m22_session_cleanup.ps1: 본 세션 정리 자동화 스크립트 (패턴 참조 보존)
""",
    },
]


def run(cmd, allow_fail: bool = False) -> subprocess.CompletedProcess:
    """git 명령 실행. UTF-8 출력 캡처. 실패 시 stderr 출력 후 예외 (allow_fail 제외)."""
    print('$ ' + ' '.join(str(c) for c in cmd))
    result = subprocess.run(
        cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print('[stderr]', result.stderr.rstrip())
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(f'Command failed (exit {result.returncode}): {cmd}')
    return result


def main():
    # 사전 상태 출력
    print('=== Initial git status ===')
    run(['git', 'status', '--short'])

    for i, c in enumerate(COMMITS, 1):
        print(f'\n=== Commit {i}/4: {c["name"]} ===')

        # Reset staging area (이전 staged 변경분 모두 unstage)
        run(['git', 'reset', 'HEAD', '--'])

        # Add target files (존재하지 않는 경로는 git이 무시 또는 경고. allow_fail로 진행)
        # 단, T7의 경우 원본(MICKEY-18-SESSION.md 등)은 working tree에서 사라진 deletion이고
        # sessions/ 경로는 untracked. 둘 다 add해야 git이 rename으로 묶음.
        run(['git', 'add', '--'] + c['add'], allow_fail=True)

        # Show staged
        run(['git', 'diff', '--cached', '--stat'])

        # Commit via -F (메시지 임시 파일)
        with tempfile.NamedTemporaryFile(
            'w', encoding='utf-8', suffix='.txt', delete=False, dir=str(ROOT)
        ) as fp:
            fp.write(c['message'])
            msgfile = fp.name

        try:
            run(['git', 'commit', '-F', msgfile])
        finally:
            Path(msgfile).unlink(missing_ok=True)

    print('\n=== Final git log (last 6) ===')
    run(['git', 'log', '--oneline', '-6'])

    print('\n=== Final git status ===')
    run(['git', 'status', '--short'])


if __name__ == '__main__':
    main()
