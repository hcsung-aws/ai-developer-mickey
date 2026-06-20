# Mickey 22 — 세션 마무리: 임시 dump 정리 + M18~M20 sessions/ 아카이빙

# 작업 디렉토리 이동
Set-Location 'C:\Users\hcsung\work\kiro\ai-developer-mickey'

# 1. 임시 dump 파일 정리 (Step 5 검증 용도, 본 세션 종료 후 불필요)
$dumpFiles = @(
    'scripts\_m22_prompt_dump.md',
    'scripts\_m22_prompt_before.md',
    'scripts\_m22_prompt_after.md'
)

foreach ($f in $dumpFiles) {
    if (Test-Path $f) {
        Remove-Item $f
        Write-Host ('Deleted: ' + $f)
    } else {
        Write-Host ('Skip (not found): ' + $f)
    }
}

Write-Host '---'

# 2. M18~M20 SESSION/HANDOFF 6파일을 sessions/ 로 git mv 아카이빙
# (M21 은 본 세션의 직전 단계로 루트 유지, M22 는 본 세션 종료 후 다음 세션 시작 시 처리)
$archiveFiles = @(
    'MICKEY-18-SESSION.md',
    'MICKEY-18-HANDOFF.md',
    'MICKEY-19-SESSION.md',
    'MICKEY-19-HANDOFF.md',
    'MICKEY-20-SESSION.md',
    'MICKEY-20-HANDOFF.md'
)

foreach ($f in $archiveFiles) {
    if (Test-Path $f) {
        git mv $f ('sessions/' + $f)
        Write-Host ('git mv: ' + $f + ' -> sessions/')
    } else {
        Write-Host ('Skip (not found): ' + $f)
    }
}

Write-Host '---'
git status --short
