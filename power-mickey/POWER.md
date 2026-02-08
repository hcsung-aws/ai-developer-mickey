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

`.kiro/scripts/session-init.sh` 파일을 생성합니다:

```bash
#!/bin/bash
SESSION_DIR=".kiro/sessions"
CURRENT="$SESSION_DIR/CURRENT.md"
DATE=$(date +%Y-%m-%d_%H%M)

mkdir -p "$SESSION_DIR/archive"

if [ -f "$CURRENT" ]; then
    mv "$CURRENT" "$SESSION_DIR/archive/session_$DATE.md"
    echo "=== 이전 세션 아카이브: session_$DATE.md ==="
fi

cat > "$CURRENT" << 'EOF'
# Session Log

## 목표
(세션 시작 시 설정)

## 진행 상황

## 주요 결정

## 수정 파일

## 다음 단계
EOF

echo "=== 새 세션 시작: $DATE ==="

if [ -f "$SESSION_DIR/HANDOFF.md" ]; then
    echo ""
    echo "=== 이전 핸드오프 ==="
    cat "$SESSION_DIR/HANDOFF.md"
fi
```

스크립트에 실행 권한을 부여합니다:
```bash
chmod +x .kiro/scripts/session-init.sh
```

## Step 3: 세션 초기화 Hook 생성

`.kiro/hooks/mickey-session-init.kiro.hook` 파일을 생성합니다:

```json
{
  "enabled": true,
  "name": "Mickey Session Initialize",
  "description": "새 세션 시작 시 이전 세션 아카이브 및 새 세션 로그 생성",
  "version": "1",
  "when": {
    "type": "agentSpawn"
  },
  "then": {
    "type": "runCommand",
    "command": "bash .kiro/scripts/session-init.sh"
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
- `.kiro/scripts/session-init.sh`
- `.kiro/hooks/mickey-session-init.kiro.hook`
- `.kiro/steering/project-lessons.md`
- `.kiro/settings/mcp.json`

모두 확인되면 Mickey 사용 준비 완료입니다.

---

# When to Load Steering Files

- 코드 작성, 구현, 개발 → `mickey-core.md` (always 로딩)
- 새 세션 시작, 세션 관리, /compact, context window → `session-protocol.md`
- 문제 해결, 디버깅, 에러 수정, 도구/솔루션 선택 → `problem-solving.md`
- 기억, 회상, 이전 결정, 지식 관리 → `memory-protocol.md`
- 세션 정리, 교훈 정리, 개선, 테스트 완료 확인 → `self-improvement.md`
