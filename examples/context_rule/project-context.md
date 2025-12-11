# Project Context for Mickey Agents

## Environment Setup

### /1 Development Environment
- **Host OS**: Windows
- **Development Environment**: WSL (Windows Subsystem for Linux)
- **Godot Editor**: Running on Windows
- **File Access**: WSL can access Windows files via `/mnt/c/`
- **Log Location**: `C:\Users\hcsung\AppData\Roaming\Godot\app_userdata\Pong with GDScript\`
- **WSL Log Path**: `/mnt/c/Users/hcsung/AppData/Roaming/Godot/app_userdata/Pong with GDScript/`
- **Project Location (Windows)**: `C:\Users\hcsung\work\q\ai-developer-mickey\pong\`
- **WSL Project Path**: `/mnt/c/Users/hcsung/work/q/ai-developer-mickey/pong/`
- **WSL Development Path**: `/home/hcsung/ai-develop-by-mickey/godot-demo-projects/2d/pong/`

**File Sync Pattern**: 
- Edit files in WSL: `/home/hcsung/ai-develop-by-mickey/godot-demo-projects/2d/pong/`
- Copy to Windows: `/mnt/c/Users/hcsung/work/q/ai-developer-mickey/pong/`
- Godot Editor opens: `C:\Users\hcsung\work\q\ai-developer-mickey\pong\`

**Important**: Always sync files from WSL to Windows after editing.

---

## Project Goal

### /2 Regression Testing System for Pong Game

**Primary Objective**: Develop a regression testing system that:
1. Records game play logs (Golden Logs)
2. Replays recorded logs
3. Validates actual behavior against expected behavior
4. Reports any differences/bugs automatically

**Implementation Priority**:
1. **GDScript** (Preferred) - If possible
2. **Godot Plugin** - If GDScript alone is insufficient
3. **Standalone Program** - Only if above options don't work

**Key Components**:
- Log Recorder (✅ Completed - `replay_logger.gd`)
- Log Replayer (✅ Completed - `replay_controller.gd`, `replay_input.gd`)
- State Validator (✅ Completed - `state_validator.gd`)
- Bug Reporter (✅ Completed - `bug_reporter.gd`)

**Current Status**:
- Pass Rate: 99.88% (841 frames, 1 error - Ball reset)
- CI/CD: Headless mode working
- Environment: Editor = Headless (identical results)
- Production Ready: ✅

---

## Decision Making Process

### /3 AI-Assisted Automation with Validation

**Principle**: Use AI for automation, but validate approach before implementation

**Process**:
1. **Analyze Current Situation**
   - Consider implementation difficulty
   - Evaluate reproducibility/reliability
   - Assess maintenance cost

2. **Propose Multiple Options**
   - List all possible approaches
   - Compare pros/cons for each
   - Estimate time/complexity

3. **Get User Confirmation**
   - Present options clearly
   - Recommend optimal approach
   - Wait for user decision before proceeding

4. **Implement Chosen Approach**
   - Follow minimal code principle
   - Test incrementally
   - Document decisions

**Example Decision Points**:
- GDScript vs C++ implementation → GDScript chosen (simpler, sufficient)
- AI Learning vs Replay Testing → Replay Testing chosen (matches actual goal)
- Input replay vs State replay → TBD (needs user decision)

---

## Key Decisions Made

### Mickey 1
- ✅ Built Godot Engine 4.6.dev
- ✅ Analyzed Pong game
- ✅ Implemented LLM AI player (AWS Bedrock Claude Haiku)
- ✅ Designed engine-level logging system

### Mickey 2
- ✅ Designed test automation system
- ✅ Analyzed C++ library feasibility
- ❌ Rejected C++ approach (19x more work, minimal benefit)
- ✅ Chose GDScript + Plugin approach

### Mickey 3
- ✅ Analyzed game logs (894 frames)
- ✅ Validated log quality for testing
- ✅ Clarified project goal: Regression Testing (not AI Learning)
- ✅ Designed replay-based testing system
- ⏳ Next: Implement log replayer

### Mickey 4 (완료)
- ✅ Replay Engine (Phase 1)
- ✅ State Validator (Phase 2)
- ✅ Bug Reporter (Phase 3)
- ✅ CI/CD 통합
- ✅ Delta 로그 사용 (핵심 해결)
- ✅ 99.88% pass rate 달성
- ✅ Production Ready

### Mickey 5 (다음)
- 선택: 리셋 프레임 스킵 (100% 달성)
- 선택: 충돌 로그 개선 (Phase 4)
- 선택: 다양한 시나리오 테스트

---

## Technical Constraints

### Deterministic Replay Challenges
1. **Physics Engine**: May not be fully deterministic
   - Solution: Fixed timestep, seed control, tolerance thresholds

2. **Input vs State Replay**
   - Input Replay: Record keyboard inputs → replay inputs
   - State Replay: Record states → force states
   - Decision needed: Which approach to use?

3. **Tolerance Thresholds**
   - Position: ±1 pixel acceptable
   - Velocity: ±0.1 acceptable
   - Needs tuning based on testing

---

## File Locations

### Project Root
`/home/hcsung/ai-develop-by-mickey/`

### Key Files
- Session logs: `MICKEY-{N}-SESSION.md`
- Analysis docs: `godot-analysis/*.md`
- Test scripts: `scripts/`
- Pong game: `godot-demo-projects/2d/pong/`

### Windows Godot Logs
- Path: `C:\Users\hcsung\AppData\Roaming\Godot\app_userdata\Pong with GDScript\`
- WSL: `/mnt/c/Users/hcsung/AppData/Roaming/Godot/app_userdata/Pong with GDScript/`
- Format: `simple_log.jsonl`

---

## Communication Guidelines

### When Starting a Session
1. Read previous Mickey session logs
2. Identify your number (Mickey N+1)
3. **IMMEDIATELY create MICKEY-(N+1)-SESSION.md** ⭐ CRITICAL
4. Summarize current status
5. Begin work

### Session Log Requirements ⭐ NEW
- **Create session log BEFORE first response to user**
- Update log after each major task
- Include: goals, progress, problems, solutions, next steps
- See `context_rule/mickey-agent-improvements.md` for details

### When Making Decisions
1. Present multiple options
2. Explain trade-offs clearly
3. Recommend optimal approach
4. Wait for user confirmation

### When Completing Tasks
1. Update session log
2. Document decisions made
3. Note lessons learned
4. Prepare handoff for next Mickey

---

## 🔴 중요한 교훈 (Mickey 4)

### Critical 1: 로그 구조 이해 필수
**Frame N의 로그 = _process() 실행 후 상태**
- Ball._process() 실행 → Ball 이동
- ReplayLogger._process() 실행 → 이동 후 상태 기록
- 검증은 Ball 이동 후 수행해야 함

**타이밍 다이어그램 필수**:
```
녹화: Ball._process() → Logger._process() → Frame N 기록
재생: Ball._process() → Validator → Frame N 검증
```

### Critical 2: Delta는 모든 곳에서 사용
**Ball + Paddle 모두 로그 delta 사용 필수**
```gdscript
if ReplayInput.replay_mode and frame_data.has("delta"):
    delta = frame_data.delta
```

**확인 방법**:
```bash
grep -r "delta" logic/ --include="*.gd"
```

### Critical 3: 근본 원인 우선, 임시방편 금지
- Tolerance 조정 금지 (임시방편)
- 에러 패턴 분석 (누적? 특정 프레임?)
- 근본 원인 찾기 (Delta? Seed? Direction?)

### Critical 4: 환경별 차이 = Delta 문제
- 에디터 ≠ Headless → Delta 차이 의심
- 로그의 delta 사용으로 해결
- VSync 설정 무관

### Critical 5: Collision = Direction 로그 사용
- Collision 프레임 에러 → Direction 의심
- 로그의 direction 강제 적용
- Paddle collision 무시

---

## 참고 문서 (필독!)

- **트러블슈팅**: `context_rule/replay-troubleshooting.md` ⭐
- **세션 로그**: `MICKEY-4-SESSION.md`
- **개선 사항**: `context_rule/mickey-agent-improvements.md`

---

## Current Phase: Implementation

### Immediate Next Steps
1. Improve log structure (add input information)
2. Implement log replayer (`log_replayer.gd`)
3. Implement state validator (`state_validator.gd`)
4. Implement bug reporter (`bug_reporter.gd`)
5. Integration testing

### Estimated Timeline
- Total: 5 hours
- Phase 1 (Replayer): 2 hours
- Phase 2 (Validator): 1 hour
- Phase 3 (Reporter): 1 hour
- Phase 4 (Testing): 1 hour

---

## Success Criteria

### Minimum Viable Product
- [ ] Can replay recorded logs
- [ ] Can detect Ball position differences
- [ ] Can output errors to console

### Full Success
- [ ] Validates all game objects
- [ ] Generates detailed reports
- [ ] CI/CD integration ready
- [ ] 10+ test cases passing

---

## References

- Main plan: `REGRESSION-TEST-PLAN.md`
- Log analysis: `LOG-ANALYSIS.md`
- Previous decisions: `DECISION-SUMMARY.md`
- Mickey 2 session: `MICKEY-2-SESSION.md`
- Mickey 3 session: `MICKEY-3-SESSION.md`
