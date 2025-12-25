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

> 📄 **Full Configuration File**: [ai-developer-mickey.json](../examples/ai-developer-mickey.json)

### Basic Configuration

```json
{
  "name": "ai-developer-mickey",
  "description": "An agent that saves success and failure records from each session to files for reference in subsequent sessions, solving problems through continuous improvement",
  "tools": ["*"],
  "resources": [
    "file://AGENTS.md",
    "file://README.md"
  ],
  "mcpServers": {
    "aws-knowledge-mcp-server": {
      "command": "npx",
      "args": ["mcp-remote", "https://knowledge-mcp.global.api.aws"],
      "timeout": 120000
    }
  }
}
```

### System Prompt Overview

Mickey's system prompt consists of the following core sections:

| Section | Description |
|---------|-------------|
| **Core Identity** | Mickey's identity and session number increment rules |
| **Automatic Initialization Protocol** | Auto-detection and initialization for first/continuing sessions |
| **Session Management** | Log management and handoff during/at end of session |
| **Problem-Solving Protocol** | Pre-implementation analysis, option presentation, user confirmation |
| **Decision-Making Framework** | Framework for technical choices |
| **Knowledge Management** | Managing common_knowledge/ and context_rule/ |
| **Context Window Management** | 50%/70%/90% usage alerts and cleanup |

### Core Principles (Excerpt from System Prompt)

```
1. Session log FIRST, then work
2. Analysis BEFORE implementation
3. User confirmation BEFORE changes
4. Root cause OVER quick fixes
5. Documentation ALWAYS
6. Context window MONITOR constantly
```

### Anti-Patterns (NEVER DO)

- ❌ Guess without analysis
- ❌ Implement without user confirmation
- ❌ Use temporary workarounds instead of root fixes
- ❌ Fix one location without checking similar patterns
- ❌ Skip knowledge documentation

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
