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
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


SESSION_DIR = Path(".kiro/sessions")
CURRENT = SESSION_DIR / "CURRENT.md"
ARCHIVE_DIR = SESSION_DIR / "archive"

TEMPLATE = """# Session Log

## 목표
(세션 시작 시 설정)

## 진행 상황

## 주요 결정

## 수정 파일

## 다음 단계
"""


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
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    print(f"=== 새 세션 시작: {timestamp} ===")


def show_handoff():
    handoff = SESSION_DIR / "HANDOFF.md"
    if handoff.exists():
        print("\n=== 이전 핸드오프 ===")
        print(handoff.read_text(encoding="utf-8"))


def main():
    archive_current_session()
    create_new_session()
    show_handoff()


if __name__ == "__main__":
    main()
```

## Step 3: 세션 훅 생성

두 개의 훅을 생성합니다. 둘 다 `userTriggered` + `askAgent` 조합입니다.

> **참고**: Kiro에서 `userTriggered` 이벤트는 `askAgent`만 지원합니다.
> `runCommand`는 `promptSubmit`, `agentStop`, `preToolUse`, `postToolUse`에서만 유효합니다.

> **⚠️ 알려진 버그 (memorygraph + Windows)**: memorygraph MCP의 `get_recent_activity` 도구를 `project` 파라미터 없이 호출하면, 내부의 `detect_project_context()` 함수가 MCP 서버 프로세스 컨텍스트에서 hang한다. 반드시 `project` 파라미터에 현재 workspace의 절대 경로를 전달해야 한다. 아래 hook 템플릿에는 이 지시가 포함되어 있다.

> **📌 Onboarding 시 주의**: 아래 hook을 생성할 때, 현재 workspace의 절대 경로를 확인하여 hook prompt 내 안내에 반영하라. hook prompt 자체에는 경로를 하드코딩하지 않고, 에이전트가 실행 시점에 workspace 경로를 감지하여 memorygraph 도구 호출에 전달하도록 지시한다.

### 세션 초기화 훅

`.kiro/hooks/mickey-session-init.kiro.hook`:

```json
{
  "name": "Mickey Session Initialize",
  "version": "2.1.0",
  "description": "새 세션 시작 시 이전 세션 아카이브 및 새 세션 로그 생성, HANDOFF 확인, memorygraph recall",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "다음 세션 초기화 절차를 순서대로 수행하라:\n\n1. `python .kiro/scripts/session_init.py` 스크립트를 실행하여 이전 세션을 아카이브하고 새 CURRENT.md를 생성하라.\n2. `.kiro/sessions/HANDOFF.md` 파일이 존재하면 읽고 내용을 요약하여 보고하라.\n3. Mickey Power의 session-protocol.md steering을 readSteering으로 읽고 세션 프로토콜을 숙지하라.\n4. memorygraph의 recall_memories 도구로 현재 프로젝트 관련 최근 기억을 조회하라. 이때 project_path 파라미터에 반드시 현재 workspace의 절대 경로를 전달하라.\n5. memorygraph의 get_recent_activity 도구를 호출할 때는 반드시 project 파라미터에 현재 workspace의 절대 경로를 전달하라. project를 생략하면 자동감지 로직이 Windows에서 hang하는 알려진 버그가 있다.\n6. 위 결과를 종합하여 '이전 세션 요약'과 '이번 세션에서 이어갈 작업'을 사용자에게 보고하라.\n\n⚠️ 중요: memorygraph의 get_recent_activity 호출 시 project 파라미터를 절대 생략하지 마라.\n\n실행 결과를 간결하게 보고하라."
  }
}
```

### 세션 종료 훅

`.kiro/hooks/mickey-session-close.kiro.hook`:

```json
{
  "name": "Mickey Session Close",
  "version": "1.1.0",
  "description": "세션 종료 시 세션 로그 정리, 교훈 추출, memorygraph 저장, HANDOFF 생성",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "다음 세션 종료 절차를 순서대로 수행하라:\n\n1. Mickey Power의 self-improvement.md steering을 readSteering으로 읽고 절차를 숙지하라.\n2. `.kiro/sessions/CURRENT.md`를 이번 세션에서 수행한 작업 내용으로 업데이트하라 (목표, 진행 상황, 주요 결정, 수정 파일, 다음 단계).\n3. `.kiro/sessions/HANDOFF.md`를 생성/업데이트하라 (현재 상태, 즉시 다음 단계, 중요 컨텍스트, 유용한 명령어).\n4. 세션 중 발견한 교훈을 분석하여 프로젝트 교훈은 `.kiro/steering/project-lessons.md`에 추가하라. 형식: ## [YYYY-MM-DD] - [주제] / 문제 / 원인 / 해결 / 교훈.\n5. 중요한 교훈이나 해결책은 memorygraph의 store_memory 도구로 저장하라. 저장 시 반드시 context 파라미터에 {\"project_path\": \"<현재 workspace 절대 경로 (forward slash 사용)>\"} 를 포함하라. project_path가 없으면 project 기반 필터링이 동작하지 않는다. 관련 기억 간 create_relationship으로 연결하라.\n6. memorygraph의 get_recent_activity 도구를 호출할 때는 반드시 project 파라미터에 현재 workspace의 절대 경로를 전달하라. project를 생략하면 자동감지 로직이 Windows에서 hang하는 알려진 버그가 있다.\n7. 범용 원칙(모든 프로젝트에 적용 가능한 것)이 있으면 사용자에게 Global steering 추가를 제안하라.\n8. 최종 결과를 사용자에게 보고하라.\n\n⚠️ 중요: memorygraph의 get_recent_activity 호출 시 project 파라미터를 절대 생략하지 마라.\n\n실행 결과를 간결하게 보고하라."
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
