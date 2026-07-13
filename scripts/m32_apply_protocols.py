# -*- coding: utf-8 -*-
"""
M32 Phase A: extended-protocols.md 수정 (repo + global 동시).

변경 내용 (3건 일괄):
1. §1 Phase 2 문단 대체 — 도구 3-Tier 방식 선택으로 축소
2. §1 품질 게이트 문장 대체 — structure.md 또는 structure-ref.md 하나
3. §18 뒤에 §19 신규 섹션 추가 — External Code Analysis Integration
4. Version 16 → 17, Last Updated, Changes 갱신

safe-batch-replace 4-step 10세대 (M31 post-check 로직 보강 유지):
1. precondition: 양쪽 hash 일치 + baseline 일치 + old_str 3개 각각 count=1
2. backup: .m32-bak 양쪽 생성
3. apply: 순차 3건 replace
4. post-check: 양쪽 hash 재일치 + 각 new_str count=1 + 각 old_str absent
"""
import hashlib
import shutil
import sys
from pathlib import Path

# Windows cp949 우회 (adaptive #8)
sys.stdout.reconfigure(encoding='utf-8')

GLOBAL_PATH = Path.home() / ".kiro" / "mickey" / "extended-protocols.md"
REPO_PATH = Path(__file__).resolve().parent.parent / "mickey" / "extended-protocols.md"

# M31 이후 baseline hash
EXPECTED_PRECOND_HASH = "CB6221C6E3E17F47F6A163642479E0408CF94656501BB9D371119B243E317F86"

# ─────────────────────────────────────────────────────────────────
# 변경 1: §1 Phase 2 문단 대체 (관계/구조 분석 → 도구 위임)
# ─────────────────────────────────────────────────────────────────
OLD_1 = """#### Phase 2: 관계/구조 분석 → auto_notes/structure.md
- 파일/컴포넌트 간 관계 파악
- 정보/데이터 흐름 추적
- 핵심 구조 정리 (의존 관계, 주제 맵, 계층 등)
- 주요 파일은 실제 내용을 읽어서 분석 (목록/심볼만으로 판단 금지)
"""

NEW_1 = """#### Phase 2: 관계/구조 분석 → 도구 위임 (§19 참조)
목표: 파일/컴포넌트 간 관계 파악, 정보/데이터 흐름, 핵심 구조.

방식 선택 (우선순위, §19 3-Tier 체계):
1. **Tier 1 감지** (`.serena/memories/`, `graphify-out/GRAPH_REPORT.md`) → 도구 결과 참조. `auto_notes/structure.md` 대신 `structure-ref.md` (2~3줄 지도 + 도구 결과 링크)만 작성
2. **Tier 2** (사용자 확인 후 도입한 다른 도구) → Tier 1과 동일 처리, 도구 이름 명시
3. **Tier 3 (Kiro CLI 내장 `code`, baseline)** → `search_codebase_map` + `generate_codebase_overview` + `search_symbols` 로 관계 파악. 결과 요약을 `auto_notes/structure.md` 에 기록. `/code init` 미실행 상태면 사용자에게 실행 안내 (§19.3 참조)

Phase 1/Phase 3 는 도구 유무와 무관하게 유지. 주요 파일 내용은 도구가 미커버하는 부분에 한해 직접 읽는다.
"""

# ─────────────────────────────────────────────────────────────────
# 변경 2: §1 품질 게이트 필수 파일 목록 변경
# ─────────────────────────────────────────────────────────────────
OLD_2 = """### 지식 베이스 품질 게이트
초기 문서 생성(T1 Step 5) 전에 아래 필수 파일이 auto_notes/에 존재해야 한다:
- [필수] inventory.md, structure.md, status.md
- [해당 시] commands.md, pitfalls.md
"""

NEW_2 = """### 지식 베이스 품질 게이트
초기 문서 생성(T1 Step 5) 전에 아래 필수 파일이 auto_notes/에 존재해야 한다:
- [필수] inventory.md, status.md, 그리고 (structure.md 또는 structure-ref.md 중 하나 — §19 Tier에 따라 결정)
- [해당 시] commands.md, pitfalls.md
"""

# ─────────────────────────────────────────────────────────────────
# 변경 3: §18 마지막 + Version 부분에 §19 삽입 및 Version 갱신
# ─────────────────────────────────────────────────────────────────
OLD_3 = """### Last Baseline Updated
2026-06-19 (Mickey 21, 5주 31세션 신규 측정. M20의 76세션 0% 결론은 표본 편향으로 무효화)

---

**Version**: 16
**Last Updated**: 2026-06-20
**Changes**: §17 Knowledge Lifecycle + §18 Activity Metrics 추가, §8 Adaptive Rules 흡수 stub로 변경 (Curator 진화 루프 + Pre-staged Apply + 활용도 baseline 명문화)
"""

NEW_3 = """### Last Baseline Updated
2026-06-19 (Mickey 21, 5주 31세션 신규 측정. M20의 76세션 0% 결론은 표본 편향으로 무효화)

---

## 19. External Code Analysis Integration

프로젝트 코드 상세 분석을 외부 도구에 위임하여 Mickey는 first-step 지도 + 작업 상황 파악에 집중한다.

### 19.1 도구 3-Tier 체계

| Tier | 도구 | 감지 마커 | Mickey 동작 |
|------|------|----------|------------|
| **Tier 1 (Default 권장)** | Serena (`oraios/serena`) | `<project>/.serena/project.yml` 또는 상위 경로 `.serena/` | 감지 시 자동 참조. INDEX Tool Links 등록 |
| **Tier 1 (Default 권장)** | Graphify (`safishamsi/graphify`) | `<project>/graphify-out/GRAPH_REPORT.md` | 감지 시 자동 참조. `AGENTS.md` 존재 시 default resource 로 자연 로딩 |
| **Tier 2 (User-Selected)** | 사용자 지정 도구 (sourcegraph, ctags, code2prompt 등) | 사용자 지정 마커 | 도입 전 사용자 확인 필수 (§19.3 참조) |
| **Tier 3 (Baseline)** | Kiro CLI 내장 `code` (tree-sitter + optional LSP) | 항상 사용 가능 | **기본 흐름**: 세션 시작 시 `/code init` 유도. LSP 활성 후 tree-sitter + LSP 조합 자율 사용 |

**핵심 원칙**: Tier 3 는 항상 baseline 으로 활성화. Tier 1/2 는 감지되면 조합. "No-Tool" 케이스는 인정하지 않는다 (내장 `code` 도구가 존재하므로).

### 19.2 감지 규칙 (세션 시작 시 자동)

First Session Step 4a / Continuing Session 엔트로피 체크에서 다음을 수행:

1. 프로젝트 루트 및 상위 1레벨에서 `.serena/` 존재 확인
2. 프로젝트 루트에서 `graphify-out/GRAPH_REPORT.md` 존재 확인
3. 프로젝트 루트에서 `.kiro/lsp.json` 또는 `lsp.json` 존재 확인 (LSP 활성 여부)
4. 감지 결과를 다음 위치에 기록:
   - `ENVIRONMENT.md` "Code Analysis Tools" 항목 (한 번만 기록)
   - `common_knowledge/INDEX.md` "Tool Links" 섹션 (트리거 매핑)

Continuing Session 에서 감지 결과가 이전 세션과 다르면 변경 사유 확인.

### 19.3 Tier 별 Mickey 역할

**Tier 1 감지 시**:
- `FILE-STRUCTURE.md` 는 **first-step 지도**만 유지 (Directory Tree depth 2 + Mickey 문서 위치 + Steering Trigger)
- 상세 코드 관계 질문 → 감지된 도구 결과 참조 안내
- Brownfield Phase 2 → `structure-ref.md` (도구 참조 + 2~3줄 지도)

**Tier 2 (사용자 확인 후 도입)**:
새 도구 도입 전 사용자에게 다음 3가지 명시적으로 제시:
- **이유**: Serena/Graphify/내장 `code` 외에 왜 필요한가 (커버 영역 차이)
- **설치 명령**: 예상 설치 절차 + 산출물 위치
- **조합 방식**: 다른 Tier 와 어떻게 함께 쓸 것인가 (중복 회피 우선순위)

사용자 승인 후 감지 마커를 §19.1 표에 추가 (T1.5 수정 → 사용자 확인). 도입 이유는 `context_rule/project-context.md` Key Decisions 에 기록.

**Tier 3 (내장 `code`) — 기본 흐름**:
- 세션 시작 시 `.kiro/lsp.json` 존재 확인 → 미존재 시 사용자에게 안내:
  > "`/code init` 실행하여 LSP 활성화를 권장합니다. tree-sitter 는 이미 사용 가능하며, LSP 활성 시 find_references / goto_definition / rename_symbol / get_diagnostics 등 추가 정밀 기능 확보. language server 미설치 시 대상 언어에 맞춰 설치 안내 (Kiro CLI docs 참조)."
- `/code init` 은 사용자만 실행 가능 (Mickey 대행 불가). 사용자 응답 대기.
- Tree-sitter 기본 operations 은 사용자 승인 없이 자율 사용 가능:
  - `search_symbols`, `get_document_symbols`, `lookup_symbols`
  - `pattern_search`, `pattern_rewrite`
  - `generate_codebase_overview`, `search_codebase_map`
- LSP operations 은 활성 확인 후 사용:
  - `find_references`, `goto_definition`, `get_hover`, `get_diagnostics`, `get_completions`, `rename_symbol`

### 19.4 조합 원칙

- **중복 회피**: 동일 정보를 여러 도구가 제공하면 우선순위 하나만 참조 (Serena > Graphify > 내장 `code`). 사용자가 특정 도구 강제 지정 시 그 도구 우선
- **상호 보완**: 도구별 강점이 다르면 병용 가능
  - Serena: 심볼 검색 + memory 지도
  - Graphify: 아키텍처 그래프 + community 분석
  - 내장 `code`: LSP 정밀 (find_references, goto_definition, rename_symbol)
  - 예: 심볼 검색은 Serena, 아키텍처 질문은 Graphify, refactoring 은 내장 `code` LSP
- **Mickey 지도 항상 유지**: `FILE-STRUCTURE.md` Directory Tree (depth 2) 는 어떤 도구를 쓰든 유지 (사용자 first-step 이해용)

### 19.5 활성화 지원 명령

**Serena** (`oraios/serena`):
- 설치: 프로젝트별 `.serena/project.yml` 생성, MCP 서버로 통합
- 상세: https://oraios.github.io/serena/

**Graphify** (`safishamsi/graphify`, PyPI: `graphifyy`):
- 설치: `uv tool install graphifyy` (또는 `pipx install graphifyy`)
- 등록: `graphify install` → AI 어시스턴트 skill 등록
- 실행: `/graphify .` → `graphify-out/{GRAPH_REPORT.md, graph.html, graph.json}` 생성
- 갱신: `graphify update .` (AST-only, no API cost)

**Kiro CLI 내장 `code`**:
- 활성화: `kiro-cli settings chat.enableCodeIntelligence true` (초기 1회)
- LSP 초기화: 프로젝트 루트에서 `/code init` (사용자만 실행 가능)
- 재시작: `/code init -f`
- 상태 확인: `/code status`
- 로그: `/code logs -l ERROR -n 50`
- 개관: `/code overview [path]`

### 19.6 세션 로그 기록

Tier 3 (`code` 도구) 사용 흔적은 `SESSION.md` Progress 에 기록하여 도구 활용 이력 추적:
- 어떤 operation 을 언제 사용했는지 요약 (예: "Phase 2 관계 분석에 `search_codebase_map` + `search_symbols` 활용")
- LSP 활성/비활성 상태 (`.kiro/lsp.json` 존재 여부)
- Tier 1/2 와의 조합 여부

---

**Version**: 17
**Last Updated**: 2026-07-01
**Changes**: §19 External Code Analysis Integration 신설 (Tier 1: Serena/Graphify default, Tier 2: user-selected, Tier 3: Kiro CLI 내장 code baseline + /code init 유도). §1 Phase 2 도구 위임으로 축소 + 품질 게이트 structure.md/structure-ref.md 택일. FILE-STRUCTURE.md 스키마 변경은 T1 (agent JSON) 동시 갱신.
"""


def sha256(path: Path) -> str:
    """파일 SHA-256 해시 측정."""
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def step1_precondition() -> None:
    """양쪽 hash 일치 + baseline 일치 + 각 old_str count=1 검증."""
    print("[Step 1] Precondition")
    g_hash = sha256(GLOBAL_PATH)
    r_hash = sha256(REPO_PATH)
    print(f"  Global: {g_hash}")
    print(f"  Repo  : {r_hash}")
    if g_hash != r_hash:
        raise RuntimeError("hash mismatch between global and repo")
    if g_hash != EXPECTED_PRECOND_HASH:
        raise RuntimeError(f"baseline hash mismatch. expected {EXPECTED_PRECOND_HASH}")

    g_text = GLOBAL_PATH.read_text(encoding="utf-8")
    r_text = REPO_PATH.read_text(encoding="utf-8")
    for label, old in [("OLD_1", OLD_1), ("OLD_2", OLD_2), ("OLD_3", OLD_3)]:
        g_count = g_text.count(old)
        r_count = r_text.count(old)
        print(f"  {label}: global={g_count} repo={r_count}")
        if g_count != 1 or r_count != 1:
            raise RuntimeError(f"{label} count mismatch (expected 1 on both)")
    print("  PASS")


def step2_backup() -> None:
    """양쪽 .m32-bak 생성."""
    print("[Step 2] Backup")
    for src in (GLOBAL_PATH, REPO_PATH):
        bak = src.with_suffix(src.suffix + ".m32-bak")
        shutil.copy2(src, bak)
        print(f"  {bak}")
    print("  PASS")


def apply_change(path: Path) -> None:
    """단일 파일 3건 순차 변경 + post-check (10세대 유지)."""
    text = path.read_text(encoding="utf-8")
    for old, new in [(OLD_1, NEW_1), (OLD_2, NEW_2), (OLD_3, NEW_3)]:
        if text.count(old) != 1:
            raise RuntimeError(f"{path}: old count != 1 during apply")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")

    # 디스크 재확인 (must-follow-rules: fs_write 후 디스크 검증)
    disk = path.read_text(encoding="utf-8")
    for label, new in [("NEW_1", NEW_1), ("NEW_2", NEW_2), ("NEW_3", NEW_3)]:
        if disk.count(new) != 1:
            raise RuntimeError(f"{path}: {label} count != 1 after write")
    for label, old in [("OLD_1", OLD_1), ("OLD_2", OLD_2), ("OLD_3", OLD_3)]:
        if old in disk:
            raise RuntimeError(f"{path}: {label} still present after write")


def step3_apply() -> None:
    """양쪽 동일 변경."""
    print("[Step 3] Apply")
    apply_change(GLOBAL_PATH)
    apply_change(REPO_PATH)
    print("  PASS")


def step4_postcheck() -> None:
    """양쪽 hash 재일치 + baseline 과 다름 확인."""
    print("[Step 4] Post-check")
    g_hash = sha256(GLOBAL_PATH)
    r_hash = sha256(REPO_PATH)
    print(f"  Global: {g_hash}")
    print(f"  Repo  : {r_hash}")
    if g_hash != r_hash:
        raise RuntimeError("hash mismatch after apply")
    if g_hash == EXPECTED_PRECOND_HASH:
        raise RuntimeError("hash unchanged — apply did not take effect")
    print(f"  baseline {EXPECTED_PRECOND_HASH[:16]}... -> {g_hash[:16]}...")
    print("  PASS")


def main() -> int:
    """4-step 순차 실행."""
    print("=" * 60)
    print("M32 Phase A: extended-protocols.md §19 신설 (safe-batch-replace 10세대)")
    print("=" * 60)
    step1_precondition()
    step2_backup()
    step3_apply()
    step4_postcheck()
    print("=" * 60)
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
