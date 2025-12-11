# Prompt Engineering

> [한국어 버전](04-prompt-engineering.md)

## Mickey Prompt Evolution

Mickey's system prompt has continuously improved through iterations.

### Initial Version (Mickey 1)

```
An agent that saves success and failure records from each session to files 
for reference in subsequent sessions, solving problems through continuous improvement
```

**Characteristics**: Simple and contains only the core

### Improved Version (After Mickey 3)

Added **knowledge management** section after experiencing context window limitations during Godot engine analysis:

```
KNOWLEDGE MANAGEMENT:
- Store reusable knowledge for future Mickey sessions in ./common_knowledge/ directory
- Structure information in semantic units that minimize context window usage when loaded
- Add cross-references between documents
```

**Reason for addition**: Need for efficient information structuring when analyzing massive codebases

### Final Version (Current)

```
You are an AI developer agent 'Mickey', that maintains session continuity 
by saving records to files and carrying them forward to subsequent sessions.

Your primary goal is to solve problems through continuous improvement by:
1. Saving session records, progress, and learnings to persistent files
2. Loading and reviewing previous session data at the start of new sessions
3. Building upon previous work and insights
4. Tracking problem-solving approaches and their effectiveness
5. Iteratively improving solutions based on accumulated knowledge
6. Monitoring context window usage and alerting when a new session is needed

KNOWLEDGE MANAGEMENT:
- Store reusable knowledge in ./common_knowledge/ directory
- Structure information in semantic units
- Add cross-references between documents

CONTEXT RULES:
- Document repeated failures in ./context_rule/ directory
- Store as actionable guidelines
- Organize by semantic meaning

IMPORTANT: If context window lacks sufficient space, inform the user 
to restart the session. Save all progress before recommending restart.
```

## Core Prompt Principles

### 1. Clear Role Definition

```
You are an AI developer agent 'Mickey'
```

**Why important**: AI needs to clearly understand its role for consistent behavior

### 2. Specific Action Guidelines

```
1. Saving session records...
2. Loading and reviewing...
3. Building upon...
```

**Why important**: Specific actions are more executable than abstract goals

### 3. Explicit Constraints

```
IMPORTANT: If context window lacks sufficient space, inform the user...
```

**Why important**: Need behavior rules for problem situations

## Effective User Prompts

### DO ✅

#### 1. Provide Context

**Bad Example**:
```
"Fix the error"
```

**Good Example**:
```
"In the Godot Pong game's replay system, Ball position validation 
shows velocity diff=209.45 error at Frame 139. 
Previous Mickey 4 solved position errors with Delta synchronization, 
and velocity errors might have similar causes. Please analyze."
```

#### 2. Request Step-by-Step Confirmation

**Bad Example**:
```
"Implement everything"
```

**Good Example**:
```
"First analyze the current implementation, identify problems, 
then propose solutions. I'll confirm at each step."
```

#### 3. Reference Previous Work

**Good Example**:
```
"Check what previous Mickey told you and the guidelines"
"Analyze the existing implementation thoroughly and let me know if there are any issues"
```

### DON'T ❌

#### 1. Vague Instructions

```
"Do it well"
"Figure it out"
"Make it good"
```

#### 2. Requests Without Context

```
"There's an error"
"It doesn't work"
"It's weird"
```

#### 3. Too Many Requests at Once

```
"Do A and B and C and D and E"
→ Break into steps
```

## Practical Prompt Patterns

### Pattern 1: Analyze → Propose → Confirm

```
User: "Analyze the current implementation thoroughly to check 
      if there are any issues with things that were working well before"

Mickey: [Performs analysis]
        "Found the following issues:
         1. SimpleAI interferes in replay mode
         2. Solution: Add replay_mode check
         Should I proceed with the fix?"

User: "Yes, please fix it"
```

### Pattern 2: Provide Context → Request Task

```
User: "We're currently in Phase 3-1. 
      Both Left and Right paddles need to be controlled by AI,
      and we need to create various scenarios (good tracking, missing goals).
      Please synthesize the current implementation with my requirements 
      and make a proposal"

Mickey: [Analyzes and proposes]
```

### Pattern 3: Problem Situation → Reference Previous Solutions

```
User: "Could 'Total frames played: 0' be caused by the value 
      being reset to 0 during initialization? 
      Analyze the existing implementation and let me know"

Mickey: [Analyzes code]
        "ReplayInput.disable_replay() resets _current_frame = 0. 
         This is normal behavior."
```

## Prompt Improvement Cases

### Case 1: Finding File Paths

**Initial Attempt** (Failed):
```
User: "Find the Windows path"
Mickey: [Attempts full directory search] → Cancelled
```

**Improved Attempt** (Success):
```
User: "Refer to previous Mickey's records or guidelines to find 
      where pong.tscn is in the Windows environment and continue"
Mickey: [Checks context_rule/project-context.md]
        "Found C:\Users\hcsung\work\q\ai-developer-mickey\pong\"
```

**Lesson**: Encourage use of existing knowledge

### Case 2: Configuration Check

**Initial Attempt** (Insufficient):
```
User: "Test it"
Mickey: [Runs test] → Fails
```

**Improved Attempt** (Success):
```
User: "It seems the configuration for running BatchTestRunner isn't complete.
      Check what previous Mickey told you and let me know what needs fixing"
Mickey: [Checks previous records]
        "ReplayLogger: enable_logging = false needed
         BatchTestRunner: auto_start = true needed"
```

**Lesson**: Explain specific problem situation

## Next Steps

- [Knowledge Management System](05-knowledge-management-en.md) - Building reusable knowledge
- [Real-World Case Study](case-study/godot-replay-system-en.md) - Godot project application case
