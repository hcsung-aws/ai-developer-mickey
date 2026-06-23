"""Mickey 24~26 진단 사이클 분리 commit (3건).

미반영 변경분이 누적되어 있음 (M22 의 adaptive.md Rule #5 위반).
세션별로 분리하여 진단 사이클 흐름을 commit 추적성으로 보존:

1. M24: Curator 변형 A2 적용 (tools=["*"] + allowedTools=4건)
2. M25: A2 검증 FAIL → 정밀 비교 → A1 적용 (allowedTools=[])
3. M26: A1 검증 FAIL → 측정 확장 → 누락 키 3개 발견 → G3 적용

각 commit 마다 git reset → git add 명시적 추가 → git commit -F 임시 파일.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

COMMITS = [
    {
        "name": "Mickey 24",
        "add": [
            "MICKEY-24-SESSION.md",
            "MICKEY-24-HANDOFF.md",
            "scripts/m24_verify_curator_variant_a2.py",
            "examples/knowledge-curator.json.m24-bak",
        ],
        "message": """Mickey 24: Curator 변형 A2 적용 (tools=["*"] + allowedTools=4건)

- M22~M23 의 Curator EmptyResponse 진단 사이클 연속
- 변형 가설: ai-developer-mickey 패턴 모방 (tools 필드만)
- 글로벌+repo knowledge-curator.json 적용 + .m24-bak 으로 원본 (11797 bytes) 양쪽 보존
- 검증은 Kiro CLI agent 캐시 (M23 발견) 로 인해 새 세션 부팅 강제 → M25 인계
- m24_verify_curator_variant_a2.py: A2 적용 후 검증 절차 (실제 검증은 M25)
""",
    },
    {
        "name": "Mickey 25",
        "add": [
            "MICKEY-25-SESSION.md",
            "MICKEY-25-HANDOFF.md",
            "scripts/m25_apply_curator_variant_a1.py",
            "scripts/m25_compare_agent_json.py",
            "examples/knowledge-curator.json.m25-bak",
        ],
        "message": """Mickey 25: A2 검증 FAIL → 정밀 비교 (변형 B 기각) → A1 적용 (allowedTools=[])

- A2 검증 FAIL: AgentLoopError(EmptyResponse) 재현
- m25_compare_agent_json.py: Curator vs ai-developer-mickey 정밀 비교 (9개 항목)
  * 변형 B (prompt 본문 길이) 기각: 정상이 50% 더 김 (10307 vs 6754)
  * 변형 A1 (allowedTools=[]) 가설 부각: 정상은 두 필드 동시 일치 패턴
- m25_apply_curator_variant_a1.py: 4-step safe-batch-replace 패턴
  * precondition (hash 검증) → backup (.m25-bak, 11748 bytes) → apply → post-check
- 글로벌+repo hash 일치 PASS (545891F304E37943, size 11688)
- 자동 승인 4건 의도 손실 (Pre-staged Apply 흐름 정합성은 보완 논의 보류)
- 실제 검증은 M26 인계 (캐시 강제)
""",
    },
    {
        "name": "Mickey 26",
        "add": [
            "MICKEY-26-SESSION.md",
            "MICKEY-26-HANDOFF.md",
            "scripts/m26_compare_agent_json_extended.py",
            "scripts/m26_extract_missing_keys.py",
            "scripts/m26_apply_curator_variant_g3.py",
            "examples/knowledge-curator.json.m26-bak",
            "examples/knowledge-curator.json",
        ],
        "message": """Mickey 26: A1 검증 FAIL → 측정 확장으로 누락 JSON 키 3개 발견 → G3 적용

- A1 검증 FAIL: AgentLoopError(EmptyResponse) 재현
- M25 측정 도구 한계 발견: obj.get("model") 이 missing key 와 explicit null 미분리
  → 변형 가설 공간이 통째로 가려져 A1/A2/B 가 헛된 시도로 끝남 (3세션 비용)
- m26_compare_agent_json_extended.py: 측정 범위 확장 (9 → 12 항목 + per-key + raw bytes + prompt 패턴)
  * Top-level 키 비교에서 누락 5건 발견 (mcpServers, useLegacyMcpJson, model, resources, toolsSettings)
  * 가장 의심: mcpServers 키 부재 (agent loop 초기화 시 MCP 컨텍스트 참조 가능성)
- m26_extract_missing_keys.py: 정상 에이전트의 누락 키 실제 값 추출
- 변형 G3 — 최소 모방 (정상 키 패턴 12개 일치, 의도는 미변경):
  * mcpServers={} (curator 는 MCP 사용 안 함, 빈 dict 로 키만 추가)
  * useLegacyMcpJson=false
  * model=null
- m26_apply_curator_variant_g3.py: 4-step safe-batch-replace 패턴 재사용
  * precondition (A1 hash + 9 키 + 누락 3 키 확인) → backup (.m26-bak, 11688 bytes) → apply → post-check
- 글로벌+repo hash 일치 PASS (5DF8F946DF56833F, size 11757)
- 검증은 M27 인계 (캐시 강제)

[Protocol] 측정 도구의 false negative 가 가설 공간 전체를 가릴 수 있음 — 측정 도구는 missing/present/value 3상태 분리 보고 필수
[Protocol] 측정 확장의 비용 대비 효용 — 5분의 측정 정밀화로 새 세션 부팅 1~2회 비용 회피
""",
    },
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """git 명령 실행 — UTF-8 인코딩 강제."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if check and result.returncode != 0:
        print(f"    [stderr] {result.stderr.strip()}")
        raise RuntimeError(f"git command failed: {cmd}")
    return result


def commit_one(name: str, files: list[str], message: str) -> None:
    print(f"\n=== {name} ===")
    # reset stage (이전 add 잔여 제거)
    run(["git", "reset"], check=False)

    # 명시적 add
    for f in files:
        path = ROOT / f
        if not path.exists():
            print(f"  ✗ MISSING: {f} — 건너뜀")
            continue
        run(["git", "add", "--", f])

    # 임시 파일에 메시지 기록 (Windows cp949 + 한글 escape 회피)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", delete=False, suffix=".txt"
    ) as tmp:
        tmp.write(message)
        tmp_path = tmp.name

    try:
        run(["git", "commit", "-F", tmp_path])
    finally:
        os.unlink(tmp_path)


def main() -> int:
    for c in COMMITS:
        commit_one(c["name"], c["add"], c["message"])

    print("\n=== 최종 git log ===")
    run(["git", "log", "--oneline", "-6"])
    print("\n=== 잔여 git status ===")
    run(["git", "status", "--short"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
