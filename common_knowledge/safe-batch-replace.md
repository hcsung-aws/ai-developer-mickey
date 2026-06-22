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
