# Mickey 22 — extended-protocols.md 글로벌/repo hash 일치 + 줄 수 검증
$global = Get-FileHash 'C:\Users\hcsung\.kiro\mickey\extended-protocols.md' -Algorithm SHA256
$repo   = Get-FileHash 'C:\Users\hcsung\work\kiro\ai-developer-mickey\mickey\extended-protocols.md' -Algorithm SHA256

Write-Host ('Global: ' + $global.Hash)
Write-Host ('Repo:   ' + $repo.Hash)

if ($global.Hash -eq $repo.Hash) {
    Write-Host 'OK: hash match'
} else {
    Write-Host 'FAIL: hash mismatch'
}

Write-Host '---'

$globalLines = (Get-Content 'C:\Users\hcsung\.kiro\mickey\extended-protocols.md' | Measure-Object -Line).Lines
$repoLines   = (Get-Content 'C:\Users\hcsung\work\kiro\ai-developer-mickey\mickey\extended-protocols.md' | Measure-Object -Line).Lines

Write-Host ('Global lines: ' + $globalLines)
Write-Host ('Repo lines:   ' + $repoLines)
