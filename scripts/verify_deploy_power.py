"""deploy_power.py 테스트 하니스.

실제 사용자 홈(~/.kiro/powers)을 건드리지 않도록 임시 디렉토리를 powers-home 으로 삼아
버전 게이트 · 백업 · clean-replace(orphan 제거) · installed.json idempotent 를 검증한다.

Working Effectively with Legacy Code 의 test harness 원칙: 배포 로직 변경 시 side effect 를
즉시 감지할 수 있는 회귀 방어선을 둔다. deploy_power.py 의 함수를 직접 import 하여 검사한다.
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

# 같은 scripts/ 디렉토리의 deploy_power 를 import
sys.path.insert(0, str(Path(__file__).resolve().parent))
import deploy_power as dp  # noqa: E402

PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    mark = "OK" if condition else "FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" : {detail}" if detail else ""
    print(f"  [ {mark} ] {name}{suffix}")


def _make_fake_power_src(root):
    """v10 형태의 가짜 power 원본을 생성한다 (steering 3개 + POWER.md + mcp.json)."""
    src = root / "power-mickey"
    steering = src / "steering"
    steering.mkdir(parents=True)
    (src / "POWER.md").write_text("# fake power\n", encoding="utf-8")
    (src / "mcp.json").write_text('{"mcpServers": {}}\n', encoding="utf-8")
    for fname in ("mickey-core.md", "session-protocol.md", "knowledge-curator.md"):
        (steering / fname).write_text(f"# {fname}\n", encoding="utf-8")
    return src


def _seed_stale_install(powers_home):
    """구 pre-v10 형태의 설치본을 심는다 (orphan 검증용 steering 포함)."""
    dst = powers_home / "installed" / dp.POWER_NAME / "steering"
    dst.mkdir(parents=True)
    # v10 에 존재하지 않는 orphan 파일들
    (dst / "self-improvement.md").write_text("# stale\n", encoding="utf-8")
    (dst / "memory-protocol.md").write_text("# stale\n", encoding="utf-8")


def test_version_parsing():
    print("--- 1. 버전 파싱 ---")
    check("'kiro-cli-chat 2.12.0' -> (2,12)", dp.parse_minor_version("kiro-cli-chat 2.12.0") == (2, 12))
    check("'2.10' -> (2,10)", dp.parse_minor_version("2.10") == (2, 10))
    check("빈 문자열 -> None", dp.parse_minor_version("") is None)
    check("숫자 없음 -> None", dp.parse_minor_version("kiro-cli") is None)


def test_version_gate():
    print("--- 2. 버전 게이트 (임계값 2.10) ---")
    gate = (2, 10)
    check("2.12.0 통과", dp.version_meets_gate("kiro-cli-chat 2.12.0", gate) is True)
    check("2.10.0 통과(경계)", dp.version_meets_gate("2.10.0", gate) is True)
    check("2.9.9 미달", dp.version_meets_gate("2.9.9", gate) is False)
    check("1.99 미달(major 우선)", dp.version_meets_gate("1.99", gate) is False)
    check("None 미달(보수적 스킵)", dp.version_meets_gate(None, gate) is False)


def test_dry_run_no_change():
    print("--- 3. dry-run 무변경 ---")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = _make_fake_power_src(tmp / "proj")
        home = tmp / "powers"
        skipped, _ = dp.deploy(src, home, "2.12.0", (2, 10), dry_run=True)
        check("게이트 통과(skipped=False)", skipped is False)
        check("installed/ 미생성", not (home / "installed").exists())
        check("installed.json 미생성", not (home / "installed.json").exists())


def test_real_deploy_removes_orphan():
    print("--- 4. 실제 배포 + orphan 제거 ---")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = _make_fake_power_src(tmp / "proj")
        home = tmp / "powers"
        _seed_stale_install(home)
        # 배포 전: orphan 존재
        steering_dir = home / "installed" / dp.POWER_NAME / "steering"
        check("배포 전 orphan(self-improvement.md) 존재", (steering_dir / "self-improvement.md").exists())

        dp.deploy(src, home, "2.12.0", (2, 10), dry_run=False)

        check("배포 후 orphan(self-improvement.md) 제거", not (steering_dir / "self-improvement.md").exists())
        check("배포 후 orphan(memory-protocol.md) 제거", not (steering_dir / "memory-protocol.md").exists())
        check("v10 steering(knowledge-curator.md) 배치", (steering_dir / "knowledge-curator.md").exists())
        check("POWER.md 배치", (home / "installed" / dp.POWER_NAME / "POWER.md").exists())
        check("mcp.json 배치", (home / "installed" / dp.POWER_NAME / "mcp.json").exists())
        # 백업 zip 생성 확인
        backups = list((home / "installed").glob(f"{dp.POWER_NAME}.bak-*.zip"))
        check("기존 설치본 백업 zip 생성", len(backups) == 1, detail=str(backups[0].name) if backups else "없음")


def test_installed_json_idempotent():
    print("--- 5. installed.json 항목 보장 + idempotent ---")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = _make_fake_power_src(tmp / "proj")
        home = tmp / "powers"

        dp.deploy(src, home, "2.12.0", (2, 10), dry_run=False)
        data1 = json.loads((home / "installed.json").read_text(encoding="utf-8"))
        names1 = [p["name"] for p in data1["installedPowers"]]
        check("installed.json 항목 추가됨", names1.count(dp.POWER_NAME) == 1)

        # 재실행 (idempotent)
        dp.deploy(src, home, "2.12.0", (2, 10), dry_run=False)
        data2 = json.loads((home / "installed.json").read_text(encoding="utf-8"))
        names2 = [p["name"] for p in data2["installedPowers"]]
        check("재실행 후 중복 없음", names2.count(dp.POWER_NAME) == 1)


def test_gate_miss_skips():
    print("--- 6. 게이트 미달 시 v3 스킵 ---")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = _make_fake_power_src(tmp / "proj")
        home = tmp / "powers"
        skipped, actions = dp.deploy(src, home, "2.9.0", (2, 10), dry_run=False)
        check("skipped=True", skipped is True)
        check("installed/ 미생성(배포 안 함)", not (home / "installed").exists())
        check("installed.json 미생성", not (home / "installed.json").exists())
        check("게이트 안내 메시지 포함", any("[gate]" in a for a in actions))


def main():
    for test in (
        test_version_parsing,
        test_version_gate,
        test_dry_run_no_change,
        test_real_deploy_removes_orphan,
        test_installed_json_idempotent,
        test_gate_miss_skips,
    ):
        test()
        print()

    total = PASS + FAIL
    print(f"Summary: PASS {PASS} / FAIL {FAIL} / total {total}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
