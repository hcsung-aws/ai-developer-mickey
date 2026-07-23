# -*- coding: utf-8 -*-
"""M41: extended-protocols §17 v20→v21 개정 — Curator 격리 + promote 락 규약.

safe-batch-replace 패턴: LF 정규화 → 각 패턴 count==1 검증 → 메모리 내 일괄 적용
→ CRLF 복원 → global/repo 동시 기록 → 해시 일치 검증 (adaptive #3).
백업: .bak-ai-developer-mickey-m41 (global은 사전 생성됨, repo는 git 추적이라 생략).
"""
import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GLOBAL = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO = Path(__file__).resolve().parent.parent / "mickey" / "extended-protocols.md"
OUT = Path(__file__).resolve().parent / "output" / "m41_protocols_v21.txt"

# ── 교체 목록 (old, new) — 모두 LF 정규화 기준 ─────────────────────
EDITS = []

# 1) §17 도입부 한 줄
EDITS.append((
    "> 세션 중 발견되는 결정·교훈·패턴을 R/G/S 3-Tier로 분기하여 글로벌/프로젝트 지식 저장소로 진화시키는 루프. Knowledge Curator subagent가 분기 판단 + 직접 수정 + Pre-staged Apply를 수행한다.",
    "> 세션 중 발견되는 결정·교훈·패턴을 R/G/S 3-Tier로 분기하여 글로벌/프로젝트 지식 저장소로 진화시키는 루프. Curator는 분기 판단 + 프로젝트 로컬 초안 작성만 수행하고(격리 원칙), 글로벌 반영은 사용자 승인 후 promote_knowledge.py(락 직렬화)가 수행한다 (M41 — 멀티 세션 충돌 해소).",
))

# 2) 라이프사이클 다이어그램
EDITS.append((
    """Knowledge Curator (subagent, delegate 호출)
  ├── 직접 수정 영역 (fs_write 자동 승인)
  │   ├── ~/.kiro/mickey/domain/ — 크로스 프로젝트 지식
  │   ├── {project}/context_rule/adaptive.md — 프로젝트 반복 패턴
  │   └── {project}/common_knowledge/INDEX.md (Domain Links 섹션)
  │
  └── Pre-staged Apply 영역 (사용자 결정 필요)
      ├── {project}/_curator-staging/ — common_knowledge/, context_rule/ 후보
      └── ~/.kiro/mickey/_curator-staging/ — patterns/, REMEMBER, PROFILE 후보
        ↓
        사용자 단일 응답 ("전체" / 번호 / "없음" / "보류")
        ↓
        Mickey가 staging → 정식 위치 이동 또는 폐기""",
    """Knowledge Curator (subagent delegate — 락 사용 중이면 메인 세션이 직접 대행, 격리 구조상 항상 안전)
  ├── 직접 수정 영역 (프로젝트 로컬만)
  │   └── {project}/context_rule/adaptive.md — 프로젝트 반복 패턴
  │
  └── staging 영역 (프로젝트 로컬 — 글로벌 쓰기 없음, 멀티 세션 격리)
      └── {project}/_curator-staging/
          ├── gd-*.md — 글로벌 domain/ 승격 번들 (entry 본문 + GRAPH/INDEX 행 명세)
          ├── ck-* / cr-* — common_knowledge/, context_rule/ 후보
          └── pat-* / remember-* / profile-* — 글로벌 patterns/REMEMBER/PROFILE 후보 (Target: global)
        ↓
        사용자 단일 응답 ("전체" / 번호 / "없음" / "보류")
        ↓
        ├── gd-* 승인분 → Mickey가 promote_knowledge.py 실행
        │     (글로벌 락 직렬화 + 백업 + GRAPH/INDEX 삽입 + 무결성 검증/자동 롤백 + backlink)
        └── 그 외 승인분 → Mickey가 staging → 정식 위치 이동 또는 폐기""",
))

# 3) 권한 표
EDITS.append((
    """### Curator 권한 (보정 후)

| 도구 | 자동 승인 | 비고 |
|------|----------|------|
| fs_read, grep, glob | 전체 자동 | 읽기/탐색은 무제한 |
| fs_write | 자동 경로만 | 그 외는 사용자 확인 |
| 자동 승인 경로 | `~/.kiro/mickey/domain/**`, `**/context_rule/adaptive.md`, `**/_curator-staging/**` | |
| 거부 경로 | `**/.git/**`, `**/node_modules/**`, `**/.venv/**`, `**/credentials*`, `**/.env*`, `**/*.key`, `**/*.pem` | 항상 차단 |""",
    """### Curator 권한 (격리 후, M41)

| 도구 | 자동 승인 | 비고 |
|------|----------|------|
| fs_read, grep, glob | 전체 자동 | 읽기/탐색은 무제한 (글로벌 포함) |
| fs_write | 자동 경로만 | 그 외는 사용자 확인 |
| 자동 승인 경로 | `**/context_rule/adaptive.md`, `**/_curator-staging/**` (프로젝트 로컬) | 글로벌 `~/.kiro/mickey/**` 쓰기는 회수됨 — 글로벌 반영은 promote 스크립트만의 권한 |
| 거부 경로 | `**/.git/**`, `**/node_modules/**`, `**/.venv/**`, `**/credentials*`, `**/.env*`, `**/*.key`, `**/*.pem` | 항상 차단 |""",
))

# 4) Pre-staged Apply 5단계
EDITS.append((
    """1. Curator가 제안 영역의 변경 후보를 staging 디렉토리에 **정식 형식으로 초안 작성** (머지 시 단순 이동)
2. Curator 출력에 staging 파일 목록 + 1줄 요약 + 머지 절차 포함
3. Mickey가 사용자에게 단일 응답 요청: "전체" / 번호 / "없음" / "보류"
4. 응답에 따라 staging → 정식 위치 이동 또는 폐기
5. dangling 항목은 다음 세션 시작 엔트로피 체크에서 재제시. 3세션 이상 보류 시 자동 폐기 후보""",
    """1. Curator가 모든 승격 후보를 **프로젝트 staging**에 초안 작성 — gd-*(글로벌 domain 번들)는 promote가 기계 파싱하는 번들 형식(CURATOR-PROMPT.md 4단계 참조), 그 외는 정식 위치와 동일 형식 (머지 시 단순 이동)
2. Curator 출력에 staging 파일 목록 + 1줄 요약 + 머지 절차 포함
3. Mickey가 사용자에게 단일 응답 요청: "전체" / 번호 / "없음" / "보류"
4. 응답에 따라 처리: gd-* 승인분은 promote_knowledge.py 실행(아래 "글로벌 승격" 참조), 그 외 승인분은 staging → 정식 위치 이동, 미승인분 폐기
5. dangling 항목은 다음 세션 시작 엔트로피 체크에서 재제시. 3세션 이상 보류 시 자동 폐기 후보

### 글로벌 승격 (promote_knowledge.py) — 락 규약

글로벌 `~/.kiro/mickey/domain/` 쓰기는 본 스크립트만의 권한이다 — 락 규율을 LLM 프롬프트가 아닌 코드로 강제 (LLM 결정론적 하이브리드 패턴).

- 위치: `~/.kiro/mickey/scripts/promote_knowledge.py` (SoT: ai-developer-mickey repo `scripts/`, install이 배포)
- 실행: `python ~/.kiro/mickey/scripts/promote_knowledge.py --project {프로젝트 루트} --owner "{project} Mickey N"` — `--files`로 특정 번들만, `--dry-run`으로 계획 확인
- 락: `~/.kiro/mickey/.promote.lock/` — mkdir 원자성 + owner.json(명의/PID/시각). 사용 중이면 exit 2(BUSY), 보유자 명의를 출력하므로 잠시 후 재시도. 10분 경과 stale 락은 자동 회수
- 트랜잭션: 수정 전 파일을 `~/.kiro/mickey/.promote-backups/<ts>-<owner>/`에 백업 → entry 생성/보강 → GRAPH/INDEX 행 삽입 → 병합 무결성 검사(dangling 0, missing path 0) → 위반 시 자동 롤백. Last Updated는 owner 명의로 스탬프
- 충돌 (낙관적 동시성 제어): Mode=new인데 노드/entry 기존재, Mode=augment인데 Base-Hash 불일치(타 세션 변경 감지) → 해당 번들만 CONFLICT 스킵(staging 보존), Mickey가 사용자 보고 후 재큐레이션/폐기 결정
- exit code: 0=전체 성공 / 1=CONFLICT 잔여 또는 무결성 FAIL(롤백 완료) / 2=락 BUSY

### 글로벌 파일 백업 네이밍 규약 (M41)

git 미추적 글로벌 파일(`~/.kiro/mickey/**`)을 수동 편집하기 전 백업은 `<원본 파일명>.bak-<project>-m<N>` 형식으로 생성한다 (예: `GRAPH.md.bak-ai-developer-mickey-m41`) — 멀티 세션 환경에서 백업 생성 주체 식별용. promote 스크립트의 자동 백업은 `.promote-backups/`로 분리되므로 규약 대상 아님. 안정 확인 후 생성 세션(또는 인계받은 후속 세션)이 삭제한다""",
))

# 5) staging 위치 — 글로벌 staging deprecated
EDITS.append((
    """- 프로젝트 루트에 `MICKEY-*-SESSION.md` 직접 존재 → `{프로젝트}/_curator-staging/`
- `.kiro/mickey/MICKEY-*-SESSION.md` 존재 (비표준 구조) → `{프로젝트}/.kiro/_curator-staging/`
- 글로벌 (REMEMBER/patterns/PROFILE) → `~/.kiro/mickey/_curator-staging/`""",
    """- 프로젝트 루트에 `MICKEY-*-SESSION.md` 직접 존재 → `{프로젝트}/_curator-staging/`
- `.kiro/mickey/MICKEY-*-SESSION.md` 존재 (비표준 구조) → `{프로젝트}/.kiro/_curator-staging/`
- 글로벌 `~/.kiro/mickey/_curator-staging/`은 **deprecated (M41)** — 신규 쓰기 금지. 글로벌 대상 후보(patterns/REMEMBER/PROFILE)도 프로젝트 staging에 `Target: global` 마커로 작성. 잔존 항목은 ownership 규칙에 따라 Source 프로젝트만 처분 가능""",
))

# 6) 버전 푸터
EDITS.append((
    """**Version**: 20
**Last Updated**: 2026-07-21""",
    """**Version**: 21
**Last Updated**: 2026-07-22
**Changes (v21)**: §17 멀티 세션 격리 (M41, 옵션 A): Curator 글로벌 직접 수정 폐지 → 프로젝트 로컬 staging(gd- 승격 번들) + promote_knowledge.py(락 직렬화 + Base-Hash 낙관적 검증 + 무결성 롤백)로 이원화. 글로벌 _curator-staging deprecated. 글로벌 백업 네이밍 규약(.bak-<project>-m<N>) 신설. 근거: delegate lock 프로세스 간 공유(M40) + 직접 대행 우회 시 동시 쓰기 무방비 + 글로벌 staging 혼입 실측""",
))


def main() -> int:
    raw = GLOBAL.read_text(encoding="utf-8")
    crlf = "\r\n" in raw
    text = raw.replace("\r\n", "\n")

    lines, ok = [], True
    for i, (old, new) in enumerate(EDITS, 1):
        n = text.count(old)
        if n != 1:
            lines.append(f"[FAIL] edit {i}: count={n} (기대 1)")
            ok = False
        else:
            text = text.replace(old, new)
            lines.append(f"[OK] edit {i} 적용")

    if not ok:
        OUT.write_text("\n".join(lines), encoding="utf-8")
        print("\n".join(lines))
        return 1

    out_text = text.replace("\n", "\r\n") if crlf else text
    GLOBAL.write_text(out_text, encoding="utf-8", newline="")
    REPO.write_text(out_text, encoding="utf-8", newline="")

    h1 = hashlib.sha256(GLOBAL.read_bytes()).hexdigest()
    h2 = hashlib.sha256(REPO.read_bytes()).hexdigest()
    lines.append(f"[{'PASS' if h1 == h2 else 'FAIL'}] global/repo 해시 일치: {h1[:16]}")
    ok &= h1 == h2

    # 구 문구 잔존 0건 검증
    check_text = GLOBAL.read_text(encoding="utf-8")
    for stale in ("~/.kiro/mickey/_curator-staging/ — patterns/",
                  "`~/.kiro/mickey/domain/**`, `**/context_rule/adaptive.md`",
                  "**Version**: 20"):
        cnt = check_text.count(stale)
        lines.append(f"[{'PASS' if cnt == 0 else 'FAIL'}] 구 문구 잔존 0: {stale[:40]}... ({cnt})")
        ok &= cnt == 0

    lines.append(f"RESULT: {'ALL PASS' if ok else 'FAIL'}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"written: {OUT} ({'ALL PASS' if ok else 'FAIL'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
