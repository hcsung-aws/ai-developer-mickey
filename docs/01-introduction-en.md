# Introduction to Mickey

> [한국어 버전](01-introduction.md)

## What is Mickey?

**Mickey** is an AI developer agent that maintains session continuity and continuously improves. Built using Kiro CLI's agent functionality, it solves context window limitations and session consistency issues that arise in complex software development projects.

## Core Concepts

### 1. Session Continuity

Mickey saves work content, decisions, and learnings to files at the end of each session. When the next session starts, it reads the previous session's records and continues the work.

```
Mickey 1 → [Save session log] → Mickey 2 → [Save session log] → Mickey 3 ...
```

### 2. Continuous Improvement

Each Mickey makes better decisions based on the experiences of previous Mickeys:

- Reuse successful approaches
- Avoid failed attempts
- Learn and apply new patterns

### 3. Naming Convention

Mickey increments its number with each session:
- First session: **Mickey 1**
- Second session: **Mickey 2**
- Third session: **Mickey 3**
- ...

This allows clear tracking of each session's work.

## Mickey Agent Configuration

### Basic Configuration

```json
{
  "name": "ai-developer-mickey",
  "description": "An agent that saves success and failure records from each session to files for reference in subsequent sessions, solving problems through continuous improvement",
  "prompt": "You are an AI developer agent 'Mickey'...",
  "tools": ["*"],
  "resources": [
    "file://AGENTS.md",
    "file://README.md"
  ]
}
```

### System Prompt (Core Part)

```
You are an AI developer agent 'Mickey', that maintains session continuity 
by saving records to files and carrying them forward to subsequent sessions. 
Your primary goal is to solve problems through continuous improvement by:

1. Saving session records, progress, and learnings to persistent files
2. Loading and reviewing previous session data at the start of new sessions
3. Building upon previous work and insights
4. Tracking problem-solving approaches and their effectiveness
5. Iteratively improving solutions based on accumulated knowledge
6. Monitoring context window usage and alerting the user when a new session is needed

Always maintain detailed logs of your work, decisions made, and lessons learned. 
Use file operations to ensure continuity across sessions and provide comprehensive 
problem-solving through persistent memory. You should increase postfix 1 by 1 after 
your name from 1. For example, first you is 'Mickey 1', and in the next session, 
you can read your previous postfix and set your name 'Mickey 2'.
```

## Directory Structure

Mickey uses the following directory structure:

```
project-root/
├── MICKEY-1-SESSION.md      # Mickey 1's session log
├── MICKEY-2-SESSION.md      # Mickey 2's session log
├── MICKEY-3-SESSION.md      # Mickey 3's session log
├── common_knowledge/        # Reusable knowledge
│   ├── INDEX.md            # Knowledge index
│   ├── godot/              # Godot-related knowledge
│   └── testing/            # Testing-related knowledge
└── context_rule/           # Context rules
    ├── project-context.md  # Project context
    └── troubleshooting.md  # Troubleshooting guide
```

## Session Log Format

Each Mickey writes session logs in the following format:

```markdown
# Mickey N Session Log
Date: YYYY-MM-DDTHH:MM:SS+09:00

## Session Goal
Goal of this session

## Previous Context (Mickey N-1)
Work completed in previous session

## Current Tasks
List of current tasks in progress

## Progress
- [x] Completed tasks
- [ ] Tasks in progress

## Key Decisions
Important decisions made

## Lessons Learned
Lessons learned

## Next Steps
Tasks for next session
```

## Real-World Usage Example

### Mickey 1 → Mickey 2 Transition

**Situation**: Context window reached 61%, session restart needed

**Mickey 1's final work**:
```
Context Window Usage: 61%
→ Save session log
→ Recommend session restart to user
```

**Mickey 2's start**:
```
1. Read previous session log (MICKEY-1-SESSION.md)
2. Restore work context
3. Declare "Starting as Mickey 2"
4. Continue work
```

## Advantages

### 1. Context Window Efficiency
- Selectively load only necessary information
- Compress and summarize information between sessions

### 2. Work Continuity
- Maintain workflow even when restarting sessions
- Reference previous decisions

### 3. Knowledge Accumulation
- Systematize project-specific knowledge
- Build reusable patterns

### 4. Transparency
- Record all decision processes
- Track problem-solving processes

## Next Steps

- [Context Window Management](02-context-management-en.md) - Methods for efficient context utilization
- [Session Continuity](03-session-continuity-en.md) - Strategies for maintaining consistency across sessions
- [Real-World Case Study](case-study/godot-replay-system-en.md) - Godot project application case
