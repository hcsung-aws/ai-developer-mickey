# Replay System Troubleshooting Guide

## 빠른 진단

### 증상 → 원인 → 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| Position 오차 누적 (15→16→17px) | Delta 차이 | 로그 delta 사용 |
| Collision 프레임 velocity 200+ | Direction 불일치 | 로그 direction 사용 |
| Headless ≠ 에디터 | Delta/VSync 차이 | 로그 delta 사용 |
| Ball 이상 동작 (리셋) | Collision 로직 오류 | 조건 체크 |
| 출력 누락 | quit() 타이밍 | await process_frame |

---

## 상세 진단

### 1. Position 오차 누적

**증상**:
```
Frame 10: diff=15.46
Frame 11: diff=16.35
Frame 12: diff=17.47
Frame 13: diff=18.37
```

**진단**:
- 오차가 선형 증가
- Delta 차이로 인한 누적 오차

**해결**:
```gdscript
// Ball.gd, Paddle.gd
func _process(delta: float) -> void:
    if ReplayInput.replay_mode and frame_data.has("delta"):
        delta = frame_data.delta
```

**확인**:
```bash
# 로그의 delta 확인
jq '.delta' replay_log.jsonl | head -10
```

---

### 2. Collision 프레임 에러

**증상**:
```
Frame 139: velocity diff=209.45
Frame 407: velocity diff=222.97
```

**진단**:
- 특정 프레임에서만 큰 차이
- Paddle 충돌 프레임
- Direction 변경 시점

**해결**:
```gdscript
// Ball.gd
func _process(delta: float) -> void:
    if ReplayInput.replay_mode:
        direction = Vector2(frame_data.state.ball.dir[0], frame_data.state.ball.dir[1])
```

**확인**:
```bash
# 충돌 프레임 확인
sed -n '139,141p' replay_log.jsonl | jq '.state.ball.dir'
```

---

### 3. Headless vs 에디터 차이

**증상**:
```
에디터: 99.88% pass rate
Headless: 1.19% pass rate
```

**진단**:
- 같은 로그, 다른 환경
- VSync 차이
- Delta 불안정

**해결**:
- Ball + Paddle 모두 로그 delta 사용
- 모든 _process(delta) 확인

**확인**:
```bash
# Delta 사용처 검색
grep -r "delta" logic/ --include="*.gd"
```

---

### 4. Ball 이상 동작

**증상**:
```
Frame 2: pos=104
Frame 3: pos=318  // 리셋!
```

**진단**:
- 충돌이 없는데 direction 변경
- Collision 로직 오류

**해결**:
```gdscript
// Paddle.gd
func _on_area_entered(area: Area2D) -> void:
    if not ReplayInput.replay_mode:
        area.direction = Vector2(_ball_dir, randf() * 2 - 1).normalized()
```

**확인**:
- 로그에서 direction 변화 확인
- 충돌 없으면 direction 유지

---

### 5. 출력 누락

**증상**:
```
=== Replay Started ===
...
--- Debugging process stopped ---
// "Replay Finished" 없음!
```

**진단**:
- quit() 즉시 실행
- Print 버퍼 flush 안 됨

**해결**:
```gdscript
stop_replay()
await get_tree().process_frame  // 1 프레임 대기
get_tree().quit(exit_code)
```

---

## 디버깅 체크리스트

### Pass Rate가 낮다면?

- [ ] 로그 구조 분석 (Frame N = 언제 기록?)
- [ ] Delta 사용처 검색 (grep "delta")
- [ ] Ball delta 사용 확인
- [ ] Paddle delta 사용 확인
- [ ] Direction 로그 사용 확인
- [ ] Seed 동기화 확인

### 환경별 차이가 있다면?

- [ ] 같은 로그 사용 확인
- [ ] Delta 차이 의심
- [ ] VSync 설정 확인
- [ ] 모든 _process(delta) 확인

### Collision 에러가 있다면?

- [ ] Direction 로그 사용 확인
- [ ] Seed 동기화 확인
- [ ] Collision 로직 확인
- [ ] 로그에서 direction 변화 확인

---

## 올바른 디버깅 순서

1. **로그 분석**:
   ```bash
   head -5 replay_log.jsonl
   jq '.state.ball' replay_log.jsonl | head -5
   ```

2. **타이밍 다이어그램 작성**:
   ```
   녹화: Ball._process() → Logger._process()
   재생: Ball._process() → Validator
   ```

3. **증상 패턴 확인**:
   - 누적 오차? → Delta
   - 특정 프레임? → Collision
   - 환경별 차이? → Delta/VSync

4. **체크리스트 검증**:
   - Delta 사용?
   - Direction 사용?
   - Seed 동기화?

5. **근본 원인 해결**:
   - Tolerance 조정 금지
   - 임시방편 금지

---

## 안티패턴

### ❌ 하지 말 것

1. **추측으로 타이밍 수정**
   - _process → _physics_process 무작위 변경
   - await 무작위 추가

2. **Tolerance로 문제 숨기기**
   - TOLERANCE = 250.0
   - 근본 원인 무시

3. **부분 수정**
   - Ball만 수정, Paddle 누락
   - grep 검색 생략

4. **로그 구조 무시**
   - 타이밍 다이어그램 생략
   - 추측으로 구현

---

## 참고 문서

- 세션 로그: `MICKEY-4-SESSION.md`
- 개선 사항: `mickey-agent-improvements.md`
- 프로젝트 컨텍스트: `project-context.md`
