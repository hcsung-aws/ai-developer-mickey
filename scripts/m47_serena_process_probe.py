# M47: Serena 활성 프로젝트 오지정 원인 규명용 프로세스 실측 프로브
# 목적: 동시 실행 중인 serena MCP 서버 프로세스들의 cwd/cmdline/부모 체인을 실측하여
#       "--project ." 상대 경로가 어느 디렉토리 기준으로 해석되는지 증거 확보
import sys
import io

# Windows cp949 콘솔에서 UnicodeEncodeError 방지 (adaptive #8)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import psutil
except ImportError:
    print("psutil 미설치 — 설치 필요: pip install psutil")
    sys.exit(1)


def describe(p):
    """프로세스 핵심 정보를 안전하게 추출 (권한 오류는 표시만)"""
    try:
        cwd = p.cwd()
    except Exception as e:
        cwd = f"<접근 불가: {type(e).__name__}>"
    try:
        cmdline = " ".join(p.cmdline())
    except Exception:
        cmdline = "<접근 불가>"
    return cwd, cmdline


def main():
    # serena 관련 프로세스와 kiro-cli 프로세스를 모두 수집
    targets = []
    for p in psutil.process_iter(["pid", "ppid", "name"]):
        name = (p.info["name"] or "").lower()
        if "serena" in name or "kiro" in name:
            targets.append(p)
        else:
            # python이 serena를 실행하는 형태도 잡는다
            try:
                cl = " ".join(p.cmdline()).lower()
                if "serena" in cl or "kiro-cli" in cl:
                    targets.append(p)
            except Exception:
                pass

    print(f"=== 대상 프로세스 {len(targets)}개 ===\n")
    for p in targets:
        cwd, cmdline = describe(p)
        # 부모 체인 (2단계) — 어느 kiro-cli 세션이 띄운 serena인지 식별
        chain = []
        try:
            parent = p.parent()
            for _ in range(2):
                if parent is None:
                    break
                pc_cwd, _ = describe(parent)
                chain.append(f"{parent.name()}(pid={parent.pid}, cwd={pc_cwd})")
                parent = parent.parent()
        except Exception:
            pass
        print(f"[{p.info['name']}] pid={p.pid}")
        print(f"  cwd     : {cwd}")
        print(f"  cmdline : {cmdline[:200]}")
        print(f"  부모 체인: {' <- '.join(chain) if chain else '<없음>'}")
        print()


if __name__ == "__main__":
    main()
