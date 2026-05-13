#Requires -Version 5.1
# Mickey 설치 스크립트 (Windows PowerShell 버전)
# bash 사용자: install.sh 참조

$ErrorActionPreference = 'Stop'

$MickeyDir  = Join-Path $env:USERPROFILE '.kiro\mickey'
$AgentsDir  = Join-Path $env:USERPROFILE '.kiro\agents'
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. kiro-cli 확인
if (-not (Get-Command kiro-cli -ErrorAction SilentlyContinue)) {
    Write-Host 'Error: kiro-cli가 설치되어 있지 않습니다.'
    Write-Host 'https://github.com/aws/kiro-cli 에서 설치 후 다시 실행해주세요.'
    exit 1
}

# 2. 글로벌 가이드 설치
$null = New-Item -ItemType Directory -Force -Path `
    $MickeyDir, `
    (Join-Path $MickeyDir 'patterns'), `
    (Join-Path $MickeyDir 'domain'), `
    (Join-Path $MickeyDir 'domain\entries')

Copy-Item (Join-Path $ScriptDir 'mickey\extended-protocols.md') $MickeyDir -Force

# glob 패턴 복사 (대상 파일 없어도 에러 아님)
Get-ChildItem -Path (Join-Path $ScriptDir 'mickey\patterns\*.md') -ErrorAction SilentlyContinue |
    Copy-Item -Destination (Join-Path $MickeyDir 'patterns') -Force

Get-ChildItem -Path (Join-Path $ScriptDir 'mickey\domain\*.md') -ErrorAction SilentlyContinue |
    Copy-Item -Destination (Join-Path $MickeyDir 'domain') -Force

Get-ChildItem -Path (Join-Path $ScriptDir 'mickey\domain\entries\*.md') -ErrorAction SilentlyContinue |
    Copy-Item -Destination (Join-Path $MickeyDir 'domain\entries') -Force

Write-Host "[OK] 글로벌 가이드 설치: $MickeyDir\"

# 3. Agent JSON 설치
$null = New-Item -ItemType Directory -Force -Path $AgentsDir
Copy-Item (Join-Path $ScriptDir 'examples\ai-developer-mickey.json') $AgentsDir -Force
Copy-Item (Join-Path $ScriptDir 'examples\knowledge-curator.json')   $AgentsDir -Force
Write-Host "[OK] Agent 설치: $AgentsDir\ai-developer-mickey.json"
Write-Host "[OK] Agent 설치: $AgentsDir\knowledge-curator.json"

Write-Host ''
Write-Host '설치 완료! 사용법:'
Write-Host '  cd <프로젝트 디렉토리>'
Write-Host '  kiro-cli chat --agent ai-developer-mickey'
