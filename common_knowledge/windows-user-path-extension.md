# Windows 사용자 PATH 확장 표준 조합 (winreg + WM_SETTINGCHANGE)

> Source: ai-developer-mickey Mickey 33 (2026-07-02)

## Core
Windows 사용자 PATH(HKCU\Environment\Path)를 스크립트로 안전하게 확장할 때는 **Python `winreg` + `ctypes.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, ...)` 조합**이 최적. `setx`는 1024자 잘림 위험, PowerShell `[Environment]::SetEnvironmentVariable`은 인용부호 지옥, `SetEnvironmentVariable` API 직접 호출은 프로세스 스코프 한정으로 새 프로세스에 미반영. winreg + broadcast 만이 (a) 원본 타입(REG_EXPAND_SZ) 유지 + (b) 값 길이 안전 + (c) 새로 뜨는 프로세스가 즉시 반영 3조건을 만족.

## Decision Context
Mickey 33 (2026-07-01) — Kiro CLI `/code init` 후 미설치 LSP 서버 3종 자율 설치 과정에서 pip `--user` 로 설치한 pyright 실행 파일(`%APPDATA%\Python\Python313\Scripts\pyright-langserver.exe`)이 PATH에 잡히지 않음. PATH 확장 방법으로 (A) 프로젝트 lsp.json 절대 경로 수정 vs (B) 사용자 PATH 확장 옵션 중 B 선택. 실제 구현 과정에서 `setx` 함정과 PowerShell 인용부호 문제를 회피하기 위해 winreg + broadcast 조합으로 정착.

## Tags
windows, path, environment-variable, winreg, wm-settingchange, broadcast, powershell-escape, setx-truncation, python-stdlib, rollback

## Related
- `~/.kiro/mickey/domain/entries/powershell-curl-escape.md` — Windows PowerShell 인용부호 지옥을 파이썬 스크립트로 회피하는 동일 철학
- `~/.kiro/mickey/domain/entries/cli-help-output-distrust.md` — `setx --help`가 1024자 잘림 경고를 명시하지 않는 문서 drift 사례
- `~/.kiro/mickey/domain/entries/deploy-output-distrust.md` — 도구(setx) 정상 완료 출력을 그대로 믿지 않고 registry 재조회로 교차 검증

## Content

### 안티 패턴 vs 정답

| 방법 | 문제 |
|------|------|
| `setx PATH "..."` | 값이 1024자 넘으면 조용히 잘림. 기존 항목 잃을 위험 |
| PowerShell `[Environment]::SetEnvironmentVariable('Path', $new, 'User')` | 인용부호 이스케이프가 파이썬/셸/PowerShell 중첩 시 매우 취약 |
| Python `os.environ['PATH'] = ...` | 현 프로세스만 반영. 새 프로세스와 registry에 미저장 |
| Windows API `SetEnvironmentVariable` (kernel32) | 프로세스 스코프. registry 미저장 |
| **winreg 직접 쓰기 + WM_SETTINGCHANGE broadcast** | ✅ 3조건 모두 충족 |

### 표준 구현 (Python)

```python
import winreg, ctypes

# 1) 원본 값 조회 (타입까지 보존)
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS) as key:
    current, value_type = winreg.QueryValueEx(key, "Path")
    entries = [e for e in current.split(";") if e]

    # 2) 중복 제거 후 append (대소문자 무시)
    lower_set = {e.lower() for e in entries}
    for new_dir in new_dirs:
        if new_dir.lower() not in lower_set:
            entries.append(new_dir)

    # 3) 원본 타입(보통 REG_EXPAND_SZ=2) 유지하며 저장
    winreg.SetValueEx(key, "Path", 0, value_type, ";".join(entries))

# 4) 새 프로세스가 반영하도록 broadcast
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SMTO_ABORTIFHUNG = 0x0002
result = ctypes.c_long()
ctypes.windll.user32.SendMessageTimeoutW(
    HWND_BROADCAST, WM_SETTINGCHANGE, 0,
    ctypes.c_wchar_p("Environment"), SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
)
```

### 필수 사전 조치: 백업

registry 쓰기 전 원본 PATH를 파일로 백업. rollback 시 이 파일 내용을 그대로 `SetValueEx`로 되돌리면 완전 복구.

```python
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
    value, value_type = winreg.QueryValueEx(key, "Path")
backup_file.write_text(f"# type: {value_type}\n{value}\n", encoding="utf-8")
```

### 검증

현재 프로세스는 부모 환경을 상속하므로 확장 즉시 `os.environ['PATH']` 또는 `shutil.which()` 로는 확인 불가. 검증은:
1. **Registry 재조회** (동일 winreg.QueryValueEx)로 값 반영 확인
2. **실행 파일 절대 경로 실행**으로 바이너리 자체는 동작 확인
3. 새 프로세스(터미널/CLI 재시작) 열어야 자동 감지

### 함정: REG_SZ vs REG_EXPAND_SZ

원본이 REG_EXPAND_SZ(2)인데 SetValueEx에 REG_SZ(1)로 쓰면 `%USERPROFILE%` 같은 환경변수 참조가 리터럴로 굳어짐. QueryValueEx가 반환한 `value_type`을 그대로 SetValueEx의 세 번째 인자로 전달할 것.

### 재사용 스크립트 (본 프로젝트)

Mickey 33에서 3파트로 정형화. 다른 세션/프로젝트에서도 그대로 활용 가능 (파일명 접두어만 세션 번호로 교체):
- `scripts/m33_backup_user_path.py` — 원본 백업
- `scripts/m33_extend_user_path.py` — winreg + broadcast 확장
- `scripts/m33_verify_path_registry.py` — registry 재조회 검증
