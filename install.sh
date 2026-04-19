#!/bin/bash
set -e

MICKEY_DIR="$HOME/.kiro/mickey"
AGENTS_DIR="$HOME/.kiro/agents"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. kiro-cli 확인
if ! command -v kiro-cli &> /dev/null; then
  echo "Error: kiro-cli가 설치되어 있지 않습니다."
  echo "https://github.com/aws/kiro-cli 에서 설치 후 다시 실행해주세요."
  exit 1
fi

# 2. 글로벌 가이드 설치
mkdir -p "$MICKEY_DIR" "$MICKEY_DIR/patterns" "$MICKEY_DIR/domain" "$MICKEY_DIR/domain/entries"
cp "$SCRIPT_DIR/mickey/extended-protocols.md" "$MICKEY_DIR/"
cp "$SCRIPT_DIR/mickey/patterns/"*.md "$MICKEY_DIR/patterns/" 2>/dev/null || true
cp "$SCRIPT_DIR/mickey/domain/"*.md "$MICKEY_DIR/domain/" 2>/dev/null || true
cp "$SCRIPT_DIR/mickey/domain/entries/"*.md "$MICKEY_DIR/domain/entries/" 2>/dev/null || true
echo "✅ 글로벌 가이드 설치: $MICKEY_DIR/"

# 3. Agent JSON 설치
mkdir -p "$AGENTS_DIR"
cp "$SCRIPT_DIR/examples/ai-developer-mickey.json" "$AGENTS_DIR/"
cp "$SCRIPT_DIR/examples/knowledge-curator.json" "$AGENTS_DIR/"
echo "✅ Agent 설치: $AGENTS_DIR/ai-developer-mickey.json"
echo "✅ Agent 설치: $AGENTS_DIR/knowledge-curator.json"

echo ""
echo "설치 완료! 사용법:"
echo "  cd <프로젝트 디렉토리>"
echo "  kiro-cli chat --agent ai-developer-mickey"
