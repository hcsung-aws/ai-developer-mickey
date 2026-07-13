# 안전한 일괄 Search/Replace 자동화 패턴

> Source: Mickey 22 (2026-06-20)

## 문제
복수 패턴을 한 파일에 일괄 적용할 때, 부분 적용(일부만 성공)이 발생하면 파일이 불일치 상태에 빠진다.

## 해결: Count-1 Guard 패턴

```python
for pattern_name, (old, new) in changes.items():
    count = content.count(old)
    if count != 1:
        raise RuntimeError(f"{pattern_name}: expected 1 match, got {count}")
    content = content.replace(old, new, 1)
```

## 핵심 원칙
1. **각 패턴은 정확히 1건 매칭** — 0건(패턴 오류) 또는 2+건(모호한 패턴)이면 즉시 중단
2. **전체 변경을 메모리에서 수행 후 한 번에 기록** — 중간 상태가 디스크에 남지 않음
3. **적용 순서 무관** — 각 패턴이 서로 겹치지 않도록 설계 (겹치면 순서 의존성 발생)
4. **적용 후 hash 검증** — 복수 파일 동기화 시 hash 일치로 정합성 확인

## 적용 범위
- 프로토콜/프롬프트 일괄 수정 (Mickey agent JSON, extended-protocols 등)
- IaC 설정 파일 일괄 변경
- 마이그레이션 스크립트에서 복수 파일 동시 패치

## 주의
- 정규식이 아닌 문자열 매칭이므로 패턴에 정규식 메타문자 있으면 그대로 리터럴 매칭됨
- 2건 이상 매칭이 정상인 경우(replaceAll 의도)는 별도 변수로 expected count를 명시

## 참고 구현
- `scripts/m22_apply_t1_changes.py` (ai-developer-mickey, Mickey 22) — T1 시스템 프롬프트 5건 일괄 변경에 사용. 활성+repo agent JSON 동시 갱신 + hash 일치 검증 포함.

---

## 4-Step 절차 (M25 이후 안정 패턴, 9세대 누적)

복수 파일 동기화 + 보안 가드를 결합한 표준 형태:

1. **Precondition**: 양쪽 hash 일치 + 예상 baseline hash + `count(old)==1`
2. **Backup**: `.{tag}-bak` 생성 (rollback 가능)
3. **Apply**: 메모리 변경 후 디스크 쓰기
4. **Post-check**: 디스크 재읽기 + `count(new)==1` + `old not in disk` + 양쪽 hash 재일치

## Post-check 로직 함정 (M30 발견 → M31 9세대 보강)

❌ 잘못된 패턴 (M30 발견):

```python
written = path.read_text(encoding="utf-8")
if OLD_STR in written:
    raise RuntimeError("old still present")  # new 가 old 를 부분 포함 시 False FAIL
```

✅ 권장 패턴 (M31 9세대 검증):

```python
written = path.read_text(encoding="utf-8")
if written.count(NEW_STR) != 1:
    raise RuntimeError("new_str count != 1")   # 의도된 결과 적용 확인 (1차)
if OLD_STR in written:
    raise RuntimeError("old still present")     # 보조 검증 (new 가 old 와 독립일 때만 유의미)
```

> new 가 old 의 모든 줄을 포함하는 변경(예: 라인 추가, 라인 강조 표시)에서 `old in written` 단독은 False FAIL 발생.
> **의도된 new 의 정확한 출현 횟수 검증이 1차, 잔존 old 검증은 보조**.

## 참고 구현 (9세대 누적 이력)

| 세대 | 스크립트 | Mickey | 특기 |
|------|---------|--------|------|
| 1 | `scripts/m22_apply_t1_changes.py` | 22 | Count-1 Guard 패턴 첫 도입 |
| 2 | `scripts/m25_apply_a1.py` | 25 | 4-step 패턴 정립 (precondition + backup + apply + post-check) |
| 3~7 | `scripts/m26_*.py` ~ `scripts/m29_*.py` | 26~29 | 진단 사이클 변형 적용 (G3, H, I, 원복) |
| 8 | `scripts/m30_apply_ownership.py` | 30 | post-check 함정 (`old not in written` 단독 사용 시 False FAIL) 발견 |
| **9** | **`scripts/m31_apply.py`** | **31** | **post-check 로직 보강 적용** (`count(new)==1` + `old not in written` 결합) |

## Last Updated
2026-06-30 (Mickey 31, 9세대 보강 — post-check 로직 함정 + 참고 구현 이력)
