# Session Continuity

> [한국어 버전](03-session-continuity.md)

## Problem Definition

One of the biggest challenges when using generative AI assistants is **maintaining consistency across sessions**.

### Typical Scenario

```
[Session 1 - Morning]
User: "Add a logging system to Godot engine"
AI: Analysis → Design → Start implementation
→ Context 70% reached, lunch time

[Session 2 - Afternoon]
User: "Continue from where we left off"
AI: "What should I continue?"
→ No previous context, need to explain from scratch
```

## Mickey's Solution

### 1. Session Log

Each Mickey leaves a detailed log at the end of the session.

#### Session Log Structure

```markdown
# Mickey N Session Log
Date: 2025-11-29T01:07:41+09:00

## Session Goal
Clear goal of this session

## Previous Context (Mickey N-1)
- Work completed in previous session
- Important decisions
- Incomplete tasks

## Current Tasks
1. [ ] Task 1
2. [x] Task 2 (completed)
3. [ ] Task 3 (in progress)

## Progress
### Completed Tasks
- ✅ Feature A implemented
- ✅ Test B written

### In Progress
- 🔄 Feature C debugging (80% complete)

### Pending
- ⏳ Documentation

## Key Decisions
### Decision 1: Approach Selection
- Option A: C++ engine modification
- Option B: GDScript plugin
- **Selected**: Option B (Reason: Simple and sufficient)

### Decision 2: Log Format
- **Selected**: JSON Lines
- **Reason**: Easy frame-by-frame parsing

## Problems Encountered
### Problem 1: Delta Mismatch
- **Symptom**: Editor ≠ Headless results
- **Cause**: Delta value difference
- **Solution**: Use delta from log

## Lessons Learned
1. Tolerance adjustment is a temporary fix
2. Finding root cause is important
3. Environment differences suspect Delta

## Files Modified
- `godot-demo-projects/2d/pong/replay_logger.gd` (new)
- `godot-demo-projects/2d/pong/replay_controller.gd` (new)
- `godot-demo-projects/2d/pong/logic/ball.gd` (modified)

## Next Steps
1. Implement replay validation system
2. Build batch testing infrastructure
3. CI/CD integration

## Context Window
- Current: 65% (130,000 / 200,000 tokens)
- Status: Safe to continue
```

### 2. Session Start Protocol

Procedure followed when a new Mickey starts:

#### Step 1: Check Previous Session Log

```
Mickey 2 starts:
1. Scan directory
2. Find MICKEY-1-SESSION.md
3. Read log
4. Restore context
```

#### Step 2: State Declaration

```
"Starting as Mickey 2."
"Previous session (Mickey 1) completed:"
- Godot engine analysis
- Pong game logging system added
- Replay feature designed

"This session will implement the replay validation system."
```

#### Step 3: Continue Work

```
- Reference previous decisions
- Prioritize incomplete tasks
- Start new tasks
```

### 3. Real Transition Case

#### Mickey 1 → Mickey 2

**Mickey 1's final work**:
```
Context Window Usage: 61%

> Completed! Fully verified that AI can follow player actions 
> using engine logs.

[Save session log]
- Engine analysis complete
- Logging system design complete
- Next: Implement automated test scripts
```

**Context Overflow occurs**:
```
The context window has overflowed, summarizing the history...
✔ Conversation history has been compacted successfully!
```

**Mickey 2 starts**:
```
> Will review previous session and start automated test script design.

Reading: /home/hcsung/ai-develop-by-mickey/session_log.txt
Reading: /home/hcsung/ai-develop-by-mickey/godot-analysis/...

> Reviewed previous session. Starting as Mickey 2.

## Automated Test Script Design Summary

Based on what was built in the previous session, will design 
learning data collection + automated test system.
```

**Key**: Restore information lost in Compact from session log!

## Core Principles of Session Continuity

### 1. Clear State Transfer

#### Bad Example
```markdown
## Progress
Did a lot of work today. Modified several files...
```

#### Good Example
```markdown
## Progress
- [x] replay_logger.gd implemented (frame-by-frame state recording)
- [x] replay_controller.gd implemented (playback control)
- [ ] state_validator.gd in progress (50% complete)
```

### 2. Document Decisions

Record all important decisions **with reasons**:

```markdown
## Key Decisions

### GDScript vs C++ Engine Modification
**Selected**: GDScript
**Reasons**: 
- C++: 19x workload, requires engine build
- GDScript: Simple, sufficient functionality
- Easy maintenance

### Log Format: JSON vs Binary
**Selected**: JSON Lines
**Reasons**:
- Human readable
- Easy frame-by-frame parsing
- Convenient debugging
```

### 3. Share Failure Experiences

Failures are also important learning materials:

```markdown
## Problems Encountered

### Attempt 1: Increase Tolerance
- **Approach**: TOLERANCE = 250.0
- **Result**: Failed (root cause unresolved)
- **Lesson**: Temporary fixes only hide problems

### Attempt 2: Delta Synchronization
- **Approach**: Use delta from log
- **Result**: Success (99.88% → 100%)
- **Lesson**: Root cause resolution is important
```

### 4. Specify Next Steps

Clear guide for next Mickey:

```markdown
## Next Steps

### Priority 1: Batch Testing Infrastructure
- [ ] Implement BatchTestRunner.gd
- [ ] Sequential execution of multiple log files
- [ ] Game state reset mechanism

### Priority 2: CI/CD Integration
- [ ] GitHub Actions workflow
- [ ] Headless mode testing
- [ ] Automatic report generation

### Priority 3: Documentation
- [ ] Write user guide
- [ ] Generate API documentation
```

## Session Transition Checklist

### At Session End (Current Mickey)

- [ ] Session log writing complete
- [ ] All decisions documented
- [ ] Modified files list recorded
- [ ] Next steps specified
- [ ] Context window usage recorded
- [ ] Files saved confirmed

### At Session Start (Next Mickey)

- [ ] Read previous session log
- [ ] Confirm and increment Mickey number
- [ ] State declaration ("Starting as Mickey N")
- [ ] Summarize previous work
- [ ] Specify current goal
- [ ] Start work

## Measurable Effects

### Without Session Continuity

```
Session 1: 0% → 60% progress
Session 2: 0% → 40% progress (20% duplicate)
Session 3: 0% → 50% progress (30% duplicate)
→ Total progress: 60% (much duplicate work)
```

### With Mickey

```
Mickey 1: 0% → 60% progress
Mickey 2: 60% → 85% progress (minimal duplication)
Mickey 3: 85% → 100% progress
→ Total progress: 100% (efficient)
```

## Practical Tips

### 1. Write Session Log Immediately

Don't write after work completion, **update during work**:

```
Work start → Create log (specify goal)
↓
Partial completion → Update log (progress)
↓
Problem occurs → Update log (record problem)
↓
Resolution → Update log (solution method)
↓
Session end → Final log review
```

### 2. Utilize Context Rules

Store repeated information in context_rule/:

```markdown
# context_rule/project-context.md

## File Sync Pattern
- Edit in WSL: /home/.../pong/
- Copy to Windows: /mnt/c/.../pong/
- Godot opens: C:\...\pong\

## Common Commands
```bash
# Sync files
cp /home/.../pong/*.gd /mnt/c/.../pong/
```
```

### 3. Build Knowledge Base

Store reusable knowledge in common_knowledge/:

```markdown
# common_knowledge/godot/replay-system.md

## Replay System Design

### Core Concepts
1. Frame-by-frame recording
2. Delta synchronization
3. State validation

### Implementation Pattern
```gdscript
# Record
func _process(delta):
    logger.log_frame(frame, delta, state)

# Replay
func _process(delta):
    delta = log.get_delta(frame)  # Use logged delta
    state = log.get_state(frame)
```
```

## Next Steps

- [Prompt Engineering](04-prompt-engineering-en.md) - Effective prompt structuring
- [Knowledge Management System](05-knowledge-management-en.md) - Building reusable knowledge
- [Real-World Case Study](case-study/godot-replay-system-en.md) - Godot project application case
