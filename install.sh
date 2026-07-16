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

# 2. 글로벌 가이드 설치 (seed 시맨틱 — IMPROVEMENT-PLAN-v10 §8-a)
#    - 세대 관리 파일(extended-protocols.md, domain/CURATOR-PROMPT.md):
#      프로토콜 배포물이므로 항상 최신으로 갱신
#    - 그 외 seed 파일(patterns/domain/entries): ~/.kiro/mickey/ 는 사용자 개인
#      지식 그래프의 실체이므로 "대상 미존재 시에만" 복사 — 기존 축적 지식을 덮어쓰지 않음
mkdir -p "$MICKEY_DIR" "$MICKEY_DIR/patterns" "$MICKEY_DIR/domain" "$MICKEY_DIR/domain/entries"

# 세대 관리 파일: 항상 덮어쓰기
cp "$SCRIPT_DIR/mickey/extended-protocols.md" "$MICKEY_DIR/"
cp "$SCRIPT_DIR/mickey/domain/CURATOR-PROMPT.md" "$MICKEY_DIR/domain/"

# seed 복사: 대상에 같은 이름 파일이 없을 때만 (개인 지식 덮어쓰기 금지)
copy_seed_glob() { # $1=소스 디렉토리, $2=대상 디렉토리, $3=제외 파일명(옵션)
  local src dest
  for src in "$1"/*.md; do
    [ -e "$src" ] || continue                       # glob 미매칭 시 skip
    [ "$(basename "$src")" = "${3:-}" ] && continue # 세대 관리 파일은 위에서 처리됨
    dest="$2/$(basename "$src")"
    [ -e "$dest" ] || cp "$src" "$dest"
  done
}
copy_seed_glob "$SCRIPT_DIR/mickey/patterns" "$MICKEY_DIR/patterns"
copy_seed_glob "$SCRIPT_DIR/mickey/domain" "$MICKEY_DIR/domain" "CURATOR-PROMPT.md"
copy_seed_glob "$SCRIPT_DIR/mickey/domain/entries" "$MICKEY_DIR/domain/entries"
echo "✅ 글로벌 가이드 설치: $MICKEY_DIR/ (seed 는 미존재 시에만, 세대 관리 파일은 갱신)"

# 3. Agent JSON 설치
mkdir -p "$AGENTS_DIR"
cp "$SCRIPT_DIR/examples/ai-developer-mickey.json" "$AGENTS_DIR/"
cp "$SCRIPT_DIR/examples/knowledge-curator.json" "$AGENTS_DIR/"
echo "✅ Agent 설치: $AGENTS_DIR/ai-developer-mickey.json"
echo "✅ Agent 설치: $AGENTS_DIR/knowledge-curator.json"

# 4. v3 Power 배포 (버전 게이트는 deploy_power.py 가 판정)
#    핵심 배포 로직(백업/clean-replace/installed.json)은 셸 중복을 피해 파이썬 단일 구현에 위임.
#    kiro-cli 2.10 미만이면 스크립트가 v3 를 건너뛰고 정상 종료(v2 는 위에서 이미 배포됨).
DEPLOY_POWER="$SCRIPT_DIR/scripts/deploy_power.py"
if [ -f "$DEPLOY_POWER" ]; then
  # python3 우선, 없으면 python 으로 폴백 (플랫폼별 인터프리터 명 차이 흡수)
  if command -v python3 &> /dev/null; then
    PY=python3
  else
    PY=python
  fi
  "$PY" "$DEPLOY_POWER"
else
  echo "[WARN] v3 배포 스크립트 없음: $DEPLOY_POWER (v2 만 설치됨)"
fi

echo ""
echo "설치 완료! 사용법:"
echo "  [CLI v2] kiro-cli chat --agent ai-developer-mickey"
echo "  [CLI v3] kiro-cli chat  (이후 power-mickey 자동 인식)"
