---
name: "mickey"
displayName: "Mickey AI Developer Agent"
description: "세션 연속성, 자기 개선, 구조화된 문제 해결을 지원하는 AI 개발자 에이전트"
keywords: [
  "develop", "code", "implement", "fix", "debug", "build", "create",
  "session", "memory", "remember", "continue", "previous",
  "problem", "solution", "error", "bug", "issue",
  "decision", "architecture", "design", "pattern",
  "lesson", "improve", "learn", "refactor", "test"
]
---

# Mickey AI Developer Agent

세션 연속성과 자기 개선을 지원하는 AI 개발자 에이전트입니다.

## 핵심 기능
- 세션 간 맥락 유지 (세션 로그, 핸드오프)
- 구조화된 문제 해결 프로토콜
- 프로젝트별 교훈 축적 및 자기 개선
- Memory Graph를 통한 장기 기억

---

# Onboarding

## Step 1: 프로젝트 구조 생성

Mickey가 사용할 디렉토리를 생성합니다:

```bash
mkdir -p .kiro/sessions/archive
mkdir -p .kiro/scripts
mkdir -p .kiro/steering
mkdir -p .kiro/settings
```

## Step 2: 세션 초기화 스크립트 생성

`.kiro/scripts/session_init.py` 파일을 생성합니다 (크로스 플랫폼 호환):

```python
"""세션 초기화 스크립트.

이전 세션을 아카이브하고 새 세션 로그를 생성한다.
HANDOFF.md에서 핵심만 추출한 SESSION-BRIEF.md를 생성하여
에이전트의 context window 소모를 최소화한다.
"""

import shutil
from datetime import datetime
from pathlib import Path


SESSION_DIR = Path(".kiro/sessions")
CURRENT = SESSION_DIR / "CURRENT.md"
ARCHIVE_DIR = SESSION_DIR / "archive"
BRIEF = SESSION_DIR / "SESSION-BRIEF.md"

TEMPLATE = """# Session Log

## 목표
(세션 시작 시 설정)

## 진행 상황

## 주요 결정

## 수정 파일

## 다음 단계
"""

SECTIONS_TO_EXTRACT = ["현재 상태", "즉시 다음 단계", "중요 컨텍스트"]
MAX_LINES_PER_SECTION = 3


def archive_current_session():
    if not CURRENT.exists():
        return
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    dest = ARCHIVE_DIR / f"session_{timestamp}.md"
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(CURRENT), str(dest))
    print(f"=== 이전 세션 아카이브: {dest.name} ===")


def create_new_session():
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    CURRENT.write_text(TEMPLATE, encoding="utf-8")
    print(f"=== 새 세션 시작: {datetime.now():%Y-%m-%d_%H%M} ===")


def _extract_section(lines, section_name, max_lines):
    """HANDOFF에서 특정 섹션의 첫 N줄만 추출."""
    result = []
    in_section = False
    for line in lines:
        if section_name in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("## "):
                break
            stripped = line.strip()
            if stripped:
                result.append(stripped)
                if len(result) >= max_lines:
                    break
    return result


def create_brief():
    """HANDOFF.md에서 핵심만 추출하여 SESSION-BRIEF.md 생성."""
    handoff = SESSION_DIR / "HANDOFF.md"
    parts = ["# Session Brief\n"]

    if handoff.exists():
        lines = handoff.read_text(encoding="utf-8").splitlines()
        for section in SECTIONS_TO_EXTRACT:
            extracted = _extract_section(lines, section, MAX_LINES_PER_SECTION)
            if extracted:
                parts.append(f"## {section}")
                parts.extend(extracted)
                parts.append("")
    else:
        parts.append("첫 세션입니다. 이전 핸드오프 없음.\n")

    BRIEF.write_text("\n".join(parts), encoding="utf-8")
    print("=== SESSION-BRIEF.md 생성 완료 ===")


def main():
    archive_current_session()
    create_new_session()
    create_brief()


if __name__ == "__main__":
    main()
```

## Step 3: 세션 훅 생성

두 개의 훅을 생성합니다. Spec task 실행 전후에 자동으로 트리거됩니다.

- `preTaskExecution`: spec task가 in_progress로 전환되기 직전에 세션 초기화
- `postTaskExecution`: spec task가 completed로 전환된 직후에 세션 종료

> **⚠️ 알려진 버그 (memorygraph + Windows)**: memorygraph MCP의 `get_recent_activity` 도구를 `project` 파라미터 없이 호출하면, 내부의 `detect_project_context()` 함수가 MCP 서버 프로세스 컨텍스트에서 hang한다. 반드시 `project` 파라미터에 현재 workspace의 절대 경로를 전달해야 한다. 아래 hook 템플릿에는 이 지시가 포함되어 있다.

> **📌 Onboarding 시 주의**: 아래 hook을 생성할 때, 현재 workspace의 절대 경로를 확인하여 hook prompt 내 안내에 반영하라. hook prompt 자체에는 경로를 하드코딩하지 않고, 에이전트가 실행 시점에 workspace 경로를 감지하여 memorygraph 도구 호출에 전달하도록 지시한다.

### 세션 초기화 훅

`.kiro/hooks/mickey-session-init.kiro.hook`:

```json
{
  "name": "Mickey Session Initialize",
  "version": "3.1.0",
  "description": "경량 세션 초기화 — 스크립트가 생성한 brief만 읽고, memorygraph는 제목/태그만 조회 (search_memories 사용, recall_memories project_path 필터 버그 우회)",
  "when": {
    "type": "preTaskExecution"
  },
  "then": {
    "type": "askAgent",
    "prompt": "다음 세션 초기화 절차를 순서대로 수행하라:\n\n1. `python .kiro/scripts/session_init.py` 실행 (이전 세션 아카이브 + 새 CURRENT.md + SESSION-BRIEF.md 생성)\n2. **PURPOSE-SCENARIO.md 최우선 로딩**: 프로젝트 루트의 PURPOSE-SCENARIO.md를 읽어라. 없으면 사용자에게 '이 프로젝트가 완성되면 어떻게 사용하게 되나요?'를 질문하고, 답변 기반으로 PURPOSE-SCENARIO.md를 생성하라 (필수 섹션: Ultimate Purpose, Usage Scenarios, Acceptance Criteria, Last Confirmed).\n3. `.kiro/sessions/SESSION-BRIEF.md`만 읽고 이전 세션 요약을 파악하라. HANDOFF.md를 직접 읽지 마라.\n4. memorygraph의 search_memories로 현재 프로젝트 관련 기억의 제목과 태그만 조회하라 (상세 내용은 조회하지 마라). project_path에 현재 workspace 절대 경로를 전달하라.\\n   ⚠️ recall_memories는 project_path 필터링 버그가 있어 항상 0건을 반환한다. 반드시 search_memories를 사용하라.\n5. **목적 재확인**: PURPOSE-SCENARIO.md 내용을 간략히 언급하고, 변경 필요 시 사용자에게 조정 여부를 확인하라.\n6. 위 결과를 종합하여 '목적 확인', '이전 세션 요약', '참고 가능한 기억 목록'을 사용자에게 간결히 보고하라.\n\n⚠️ context window 절약이 핵심이다. 파일을 추가로 읽거나 memorygraph 상세 내용을 조회하지 마라. 필요 시 작업 중 on-demand로 조회한다.\n⚠️ memorygraph 호출 시 project 파라미터에 현재 workspace 절대 경로를 반드시 전달하라 (Windows hang 버그 방지)."
  }
}
```

### 세션 종료 훅

`.kiro/hooks/mickey-session-close.kiro.hook`:

```json
{
  "name": "Mickey Session Close",
  "version": "1.4.0",
  "description": "세션 종료 시 세션 로그 정리, 교훈 추출, memorygraph 저장, HANDOFF 생성",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "askAgent",
    "prompt": "다음 세션 종료 절차를 순서대로 수행하라:\n\n1. Mickey Power의 self-improvement.md steering을 readSteering으로 읽고 절차를 숙지하라.\n2. `.kiro/sessions/CURRENT.md`를 이번 세션에서 수행한 작업 내용으로 업데이트하라 (목표, 진행 상황, 주요 결정, 수정 파일, 다음 단계).\n3. `.kiro/sessions/HANDOFF.md`를 생성/업데이트하라 (현재 상태, 즉시 다음 단계, 중요 컨텍스트, 유용한 명령어).\n4. 세션 중 발견한 교훈을 분석하라.\n\n⚠️ 교훈 판별 기준 (엄격히 적용):\n- 교훈이란: 다른 프로젝트에서도 참고할 수 있는 새로운 발견, 예상과 다른 결과, 같은 실수의 반복, 또는 효과적인 해결책의 발견이다.\n- 교훈이 아닌 것: '이번 세션에서 한 일'의 기록, 기존에 알려진 패턴(Adapter, Strategy 등)의 단순 적용, 세션 활동 요약.\n- 세션 활동 기록은 CURRENT.md와 HANDOFF.md의 역할이다. memorygraph는 교훈 전용 저장소이다.\n\n교훈이 있는 경우:\n  a. `.kiro/steering/project-lessons.md`에 추가하라. 형식: ## [YYYY-MM-DD] - [주제] / 문제 / 원인 / 해결 / 교훈.\n  b. memorygraph의 store_memory로 저장하라. type은 'solution' 또는 'fix'를 사용하라. 저장 시 반드시 context 파라미터에 {\"project_path\": \"<현재 workspace 절대 경로 (forward slash 사용)>\"} 를 포함하라. 관련 기억 간 create_relationship으로 연결하라.\n\n교훈이 없는 경우:\n  → project-lessons.md 수정 없음, memorygraph 저장 없음. '교훈 없음'으로 보고하라.\n  → 절대로 세션 활동이나 작업 요약을 memorygraph에 저장하지 마라.\n\n5. 범용 원칙(모든 프로젝트에 적용 가능한 것)이 있으면 사용자에게 Global steering 추가를 제안하라.\n6. 최종 결과를 사용자에게 보고하라.\n\n⚠️ memorygraph 호출 시 주의사항:\n- get_recent_activity 호출 시 project 파라미터에 현재 workspace 절대 경로를 반드시 전달하라 (Windows hang 버그 방지).\n- store_memory의 context에는 {\"project_path\": \"...\"} 키를 사용하라 ({\"project\": \"...\"} 는 무시됨).\n\n실행 결과를 간결하게 보고하라."
  }
}
```

## Step 4: 프로젝트 교훈 파일 생성

`.kiro/steering/project-lessons.md` 파일을 생성합니다:

```markdown
---
inclusion: always
---
# 프로젝트 교훈

이 파일은 Mickey가 이 프로젝트에서 학습한 교훈을 기록합니다.
세션 종료 시 Mickey가 직접 이 파일을 업데이트합니다.

## 교훈 목록

(Mickey가 자동으로 추가)
```

## Step 5: Memory Graph 설치

Memory Graph MCP를 설치합니다:

```bash
pip install --user pipx && pipx ensurepath
pipx install memorygraphMCP
```

`.kiro/settings/mcp.json` 파일을 생성합니다:
```json
{
  "mcpServers": {
    "memorygraph": {
      "command": "memorygraph",
      "args": ["--profile", "extended"]
    }
  }
}
```

## Step 6: 온보딩 완료 확인

다음 파일들이 생성되었는지 확인합니다:
- `.kiro/sessions/` 디렉토리
- `.kiro/scripts/session_init.py`
- `.kiro/hooks/mickey-session-init.kiro.hook`
- `.kiro/hooks/mickey-session-close.kiro.hook`
- `.kiro/steering/project-lessons.md`
- `.kiro/settings/mcp.json`

모두 확인되면 Mickey 사용 준비 완료입니다.

> **💡 Context Window 최적화**: 세션 초기화 시 HANDOFF 전문이 아닌 SESSION-BRIEF.md(핵심 요약)만 로딩하고, memorygraph는 제목/태그 목록만 조회합니다. 상세 내용은 작업 중 필요할 때 on-demand로 조회합니다.

---

# 사용법

## 세션 시작
1. 새 채팅 세션을 연다
2. Explorer > Agent Hooks에서 "Mickey Session Initialize" 의 ▶ (Start Hook) 클릭
3. Agent가 세션 초기화 결과를 보고할 때까지 대기
4. 작업 시작

## 세션 종료
1. 작업 완료 후 Explorer > Agent Hooks에서 "Mickey Session Close" 의 ▶ (Start Hook) 클릭
2. Agent가 세션 정리, 교훈 추출, HANDOFF 생성을 수행
3. 결과 보고 확인

---

# When to Load Steering Files

- 코드 작성, 구현, 개발 → `mickey-core.md`
- 새 세션 시작, 세션 관리, 이전 작업 → `session-protocol.md`
- 문제 해결, 디버깅, 에러 수정 → `problem-solving.md`
- 기억, 회상, 이전 결정 → `memory-protocol.md`
- 세션 정리, 교훈 정리, 개선 → `self-improvement.md`
