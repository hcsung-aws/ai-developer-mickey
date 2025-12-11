# Context Window Management

> [한국어 버전](02-context-management.md)

## What is a Context Window?

A context window is the amount of text an AI model can process at once. While Kiro CLI provides a 200,000 token context window, even this can be insufficient for complex projects.

## Problem Scenarios

### Typical Failure Scenario

```
1. Start analyzing complex codebase
2. Read multiple files → 50% context used
3. Additional analysis and code writing → 70% context used
4. Need more information → 90% context used
5. Context overflow → Session summary (Compact)
6. Loss of important context → Task failure
```

### Session Restart Without Mickey

```
[Previous Session]
- Detailed analysis results
- Design decisions
- Attempted approaches
- Reasons for failures

[After Compact]
- "Analyzing Godot engine"
- "Need to implement logging system"
→ Most specific context lost
```

## Mickey's Solution

### 1. Knowledge Abstraction

**Principle**: Don't put all information in context; selectively load only what's needed

#### Hierarchical Document Structure

```
common_knowledge/
├── INDEX.md                    # Top-level index (always load)
├── godot/
│   ├── overview.md            # Overview (load as needed)
│   ├── scene-system.md        # Details (load as needed)
│   └── collision-system.md    # Details (load as needed)
└── testing/
    ├── overview.md
    └── replay-system.md
```

#### INDEX.md Example

```markdown
# Knowledge Index

## Godot Engine
- [Overview](godot/overview.md) - Engine structure overview
- [Scene System](godot/scene-system.md) - Scene-node tree structure
- [Collision System](godot/collision-system.md) - Collision detection system

## Testing
- [Overview](testing/overview.md) - Testing strategy
- [Replay System](testing/replay-system.md) - Replay system design
```

**Usage**:
1. Load only INDEX.md first (small context usage)
2. Identify needed topics
3. Selectively load only relevant documents

### 2. Context Rules

**Principle**: Document repeated failures or impossible tasks to prevent wasting time

#### context_rule/project-context.md

```markdown
# Project Context

## Environment
- OS: Windows + WSL
- Godot: Running on Windows
- Development: WSL
- File Sync: WSL → Windows required

## Known Issues
- ❌ C++ engine modification: 19x workload, minimal benefit
- ✅ GDScript approach: Simple and sufficient

## File Locations
- Windows Project: C:\Users\...\pong\
- WSL Project: /home/.../godot-demo-projects/2d/pong/
- Logs: C:\Users\...\AppData\Roaming\Godot\...
```

**Benefits**:
- Prevent repeating already-tried approaches
- Quick reference for environment settings
- Clear awareness of known constraints

### 3. Session Log Compression

**Principle**: Record only essential information concisely in session logs

#### Bad Example (Verbose)

```markdown
## Progress
Starting today's work, I first analyzed the Godot engine structure.
The engine was very complex and required reading many files.
Initially tried C++ approach but it was too complex...
(continues for 500 words)
```

#### Good Example (Concise)

```markdown
## Progress
- [x] Godot engine structure analysis complete
- [x] C++ approach reviewed → GDScript selected (19x efficiency)
- [x] Pong game logging system added
- [ ] Replay system implementation in progress

## Key Decisions
- GDScript > C++: Simple and sufficient
- Log format: JSON Lines (frame-by-frame state)
```

### 4. Context Window Monitoring

Mickey always tracks context window usage:

```
Context Window Usage: 52% (104,000 / 200,000 tokens)
→ Safe range

Context Window Usage: 70% (140,000 / 200,000 tokens)
→ Cleanup recommended

Context Window Usage: 85% (170,000 / 200,000 tokens)
→ Session restart required
```

**Thresholds**:
- **< 70%**: Normal operation
- **70-85%**: Start cleanup (remove unnecessary information)
- **> 85%**: Save session log and restart

## Real-World Application

### Godot Engine Analysis

**Problem**: Godot engine is a massive codebase with 13,666 files

**Solution**:

1. **Step 1: Understand Overview**
   ```
   - Read README.md
   - Understand directory structure
   - Identify core modules
   → Context usage: 5%
   ```

2. **Step 2: Structure Knowledge**
   ```
   - Write common_knowledge/godot/overview.md
   - Extract only core concepts (scene, node, signal)
   - Separate detailed content into separate documents
   → Context usage: additional 3%
   ```

3. **Step 3: Load Details as Needed**
   ```
   - Need collision system → load collision-system.md
   - Need input system → load input-system.md
   → Context usage: 2-3% each
   ```

**Result**: Completed necessary work without putting entire engine in context

### Replay System Development

**Problem**: Complex design decisions and multiple attempts required

**Solution**:

1. **Record Design Decisions**
   ```markdown
   ## Key Decisions (Mickey 3)
   - Input Replay vs State Replay
     → State Replay selected (100% accuracy)
   - Delta synchronization required
     → Use delta from log
   ```

2. **Share Failure Experiences**
   ```markdown
   ## Lessons Learned (Mickey 4)
   - ❌ Tolerance adjustment: Temporary fix, not root solution
   - ✅ Delta synchronization: Root cause resolution
   - ✅ Direction log usage: Collision error resolution
   ```

3. **Next Mickey Utilization**
   ```
   When Mickey 5 starts:
   - Reference previous decisions
   - Avoid failed approaches
   - Apply verified methods
   ```

## Best Practices

### DO ✅

1. **Use Hierarchical Document Structure**
   - Overview → Details order
   - Load only what's needed

2. **Concise Session Logs**
   - Record only essential information
   - Use bullet points

3. **Utilize Context Rules**
   - Document repeated failures
   - Specify environment information

4. **Regular Monitoring**
   - Track context usage
   - Cleanup when reaching 70%

### DON'T ❌

1. **Load All Files at Once**
   - Wastes context
   - Excessive unnecessary information

2. **Verbose Explanations**
   - Write essays in session logs
   - Repeat duplicate information

3. **Ignore Context**
   - Work beyond 90%
   - Restart after Compact (information loss)

4. **Save Without Structure**
   - Put all information in one file
   - Unsearchable format

## Measurable Effects

### Without Mickey

```
Session 1: Context 100% → Compact → Information loss
Session 2: Start from scratch
Session 3: Compact again...
→ Progress speed: Slow, many repeated tasks
```

### With Mickey

```
Mickey 1: Context 70% → Save session log
Mickey 2: Continue previous work → Context 50%
Mickey 3: Additional work → Context 65%
→ Progress speed: Fast, cumulative learning
```

## Next Steps

- [Session Continuity](03-session-continuity-en.md) - Methods to maintain consistency across sessions
- [Knowledge Management System](05-knowledge-management-en.md) - Building reusable knowledge
- [Real-World Case Study](case-study/godot-replay-system-en.md) - Actual application case
