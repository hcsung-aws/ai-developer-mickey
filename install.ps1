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

# 2. 글로벌 가이드 설치 (seed 시맨틱 — IMPROVEMENT-PLAN-v10 §8-a)
#    - 세대 관리 파일(extended-protocols.md, domain\CURATOR-PROMPT.md):
#      프로토콜 배포물이므로 항상 최신으로 갱신
#    - 그 외 seed 파일(patterns/domain/entries): ~/.kiro/mickey/ 는 사용자 개인
#      지식 그래프의 실체이므로 "대상 미존재 시에만" 복사 — 기존 축적 지식을 덮어쓰지 않음
$null = New-Item -ItemType Directory -Force -Path `
    $MickeyDir, `
    (Join-Path $MickeyDir 'patterns'), `
    (Join-Path $MickeyDir 'domain'), `
    (Join-Path $MickeyDir 'domain\entries')

# seed 복사 도우미: 대상에 같은 이름 파일이 없을 때만 복사 (개인 지식 보호)
function Copy-SeedFiles {
    param([string]$SourceGlob, [string]$DestDir, [string[]]$ExcludeNames = @())
    Get-ChildItem -Path $SourceGlob -ErrorAction SilentlyContinue |
        Where-Object { $ExcludeNames -notcontains $_.Name } |
        ForEach-Object {
            $dest = Join-Path $DestDir $_.Name
            if (-not (Test-Path $dest)) { Copy-Item $_.FullName $dest }
        }
}

# 세대 관리 파일: 항상 덮어쓰기
Copy-Item (Join-Path $ScriptDir 'mickey\extended-protocols.md') $MickeyDir -Force
Copy-Item (Join-Path $ScriptDir 'mickey\domain\CURATOR-PROMPT.md') (Join-Path $MickeyDir 'domain') -Force

# 글로벌 승격 스크립트: 세대 관리 (결정론적 도구 — 항상 최신 배포, §17 락 규약)
$null = New-Item -ItemType Directory -Force -Path (Join-Path $MickeyDir 'scripts')
Copy-Item (Join-Path $ScriptDir 'scripts\promote_knowledge.py') (Join-Path $MickeyDir 'scripts') -Force

# seed 파일: 미존재 시에만 복사 (CURATOR-PROMPT.md 는 위 세대 관리에서 처리됨)
Copy-SeedFiles (Join-Path $ScriptDir 'mickey\patterns\*.md') (Join-Path $MickeyDir 'patterns')
Copy-SeedFiles (Join-Path $ScriptDir 'mickey\domain\*.md') (Join-Path $MickeyDir 'domain') -ExcludeNames @('CURATOR-PROMPT.md')
Copy-SeedFiles (Join-Path $ScriptDir 'mickey\domain\entries\*.md') (Join-Path $MickeyDir 'domain\entries')

Write-Host "[OK] 글로벌 가이드 설치: $MickeyDir\ (seed 는 미존재 시에만, 세대 관리 파일은 갱신)"

# 3. Agent JSON 설치
$null = New-Item -ItemType Directory -Force -Path $AgentsDir
Copy-Item (Join-Path $ScriptDir 'examples\ai-developer-mickey.json') $AgentsDir -Force
Copy-Item (Join-Path $ScriptDir 'examples\knowledge-curator.json')   $AgentsDir -Force
Write-Host "[OK] Agent 설치: $AgentsDir\ai-developer-mickey.json"
Write-Host "[OK] Agent 설치: $AgentsDir\knowledge-curator.json"

# 4. v3 Power 배포 (버전 게이트는 deploy_power.py 가 판정)
#    핵심 배포 로직(백업/clean-replace/installed.json)은 셸 중복을 피해 파이썬 단일 구현에 위임.
#    kiro-cli 2.10 미만이면 스크립트가 v3 를 건너뛰고 정상 종료(v2 는 위에서 이미 배포됨).
$DeployPower = Join-Path $ScriptDir 'scripts\deploy_power.py'
if (Test-Path $DeployPower) {
    python $DeployPower
} else {
    Write-Host "[WARN] v3 배포 스크립트 없음: $DeployPower (v2 만 설치됨)"
}

Write-Host ''
Write-Host '설치 완료! 사용법:'
Write-Host '  [CLI v2] kiro-cli chat --agent ai-developer-mickey'
Write-Host '  [CLI v3] kiro-cli chat  (이후 power-mickey 자동 인식)'
