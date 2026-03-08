# Introduction to Mickey

> [한국어 버전](01-introduction.md)

## What is Mickey?

**Mickey** is an AI developer agent that maintains session continuity and continuously improves itself. Built on Kiro CLI's agent feature, it solves problems that arise in complex software development projects.

### Why Do You Need Mickey?

If you've used an AI coding assistant, you've likely experienced these issues:

| Problem | Cause | Mickey's Solution |
|---------|-------|-------------------|
| Re-explaining yesterday's work today | No memory between sessions | File-based session continuity |
| Drifting from original purpose during work | No purpose tracking mechanism | PURPOSE-SCENARIO based management |
| AI loses the big picture as project grows | Context window limits | 3-Tier Context Loading |
| Repeating the same mistakes | No lesson accumulation system | Knowledge management + auto memory |
| Having to say "record this" every time | No autonomy | Adaptive Rules + Autonomy Preference |

## Core Concepts

### 1. Session Continuity

**Why**: AI forgets everything when a session ends. Conversations are volatile, but files persist.

**What**: Save each session's work, decisions, and lessons to files, and automatically load them in the next session.

**How**:
```
Mickey 1 → [Save SESSION.md + HANDOFF.md] → Mickey 2 → [Load previous records + continue work] → ...
```

### 2. Continuous Improvement

**Why**: Repeating the same mistakes is a waste of time.

**What**: Systematically record failure experiences and automatically reference them in the next session.

**How**:
- `auto_notes/`: AI automatically records observed facts (build commands, error fixes, etc.)
- `context_rule/`: Verified rules (preventing repeated failures, environment settings)
- `context_rule/adaptive.md`: AI self-generated behavioral rules (self-improvement)

### 3. Purpose-First

**Why**: AI works hard on given tasks but doesn't judge whether they're optimal for the purpose.

**What**: Manage the project's ultimate purpose and usage scenarios as an independent document, using it as the basis for all decisions.

**How**: Load `PURPOSE-SCENARIO.md` as the top priority at session start, and continuously check alignment with purpose during work.

### 4. Naming Convention

Mickey increments its number each session: Mickey 1, Mickey 2, Mickey 3, ...
This enables clear tracking of each session's work.

## Mickey's Structure (v7.2)

### System Prompt Composition

Mickey's behavior is organized hierarchically:

| Layer | Location | Role | Loading Time |
|-------|----------|------|-------------|
| **T1** | System prompt | Core identity, universal principles, session protocol | Always |
| **T1.5** | `~/.kiro/mickey/` | Detailed execution guidelines (Brownfield, autonomy, Backpressure, etc.) | Session start |
| **T2** | Project root | PURPOSE-SCENARIO, PROJECT-OVERVIEW, HANDOFF, adaptive.md | Session start |
| **T3a** | INDEX files | Knowledge maps (what knowledge exists) | Session start |
| **T3b** | Individual knowledge files | Detailed knowledge (only when needed) | During work |

**Why this separation?** Context window is finite. Loading everything at once causes important information to be buried. "Give a map, not an encyclopedia" — load only what's needed, when it's needed.

### Core Principles (REMEMBER)

```
1.  Purpose first: PURPOSE-SCENARIO.md is the top priority for all decisions
2.  Simplicity first: Simple alternatives before complex solutions
3.  Session log FIRST, then work
4.  Analysis BEFORE implementation
5.  Check error logs immediately (no guessing)
6.  User confirmation BEFORE changes (auto_notes/adaptive.md are automatic)
7.  Root cause OVER quick fixes
8.  Suggest alternatives when complexity is excessive
9.  Verify prerequisites first
10. Core message first when writing documents
11. Incremental adoption: Start minimal + expand based on feedback only
12. Test after each work unit
13. Test-based completion: Declare complete only after tests pass
14. Autonomous execution conditions: Clear CC + rollback possible + verifiable
15. Backpressure: No proceeding to next step on verification failure
```

### Autonomy Preference

Mickey asks users about their autonomy level in the first session:

| Level | Name | Mickey's Behavior |
|-------|------|-------------------|
| 1 | Conservative | Confirm before all file changes |
| 2 | Balanced (default) | Autonomous for notes/logs, confirm for others |
| 3 | Autonomous | Autonomous execution for tasks with clear completion criteria |

Users can change this anytime with "adjust autonomy."

## Directory Structure

Files Mickey creates in a project:

```
project-root/
├── PURPOSE-SCENARIO.md          # Ultimate purpose + usage scenarios
├── PROJECT-OVERVIEW.md          # Project overview
├── ENVIRONMENT.md               # Environment info + autonomy level
├── FILE-STRUCTURE.md            # File structure
├── DECISIONS.md                 # Decision log
├── MICKEY-N-SESSION.md          # Session log (work records)
├── MICKEY-N-HANDOFF.md          # Handoff (next session transfer)
├── context_rule/                # Project-specific rules
│   ├── INDEX.md                 # Rule map
│   ├── project-context.md       # Environment/goals/constraints/lessons
│   └── adaptive.md              # 🆕 AI self-generated rules
├── common_knowledge/            # Universal reusable patterns
│   └── INDEX.md                 # Knowledge map
└── auto_notes/                  # AI automatic observation records
    └── NOTES.md                 # Notes index
```

## Quick Start

### Installation

```bash
# After installing Kiro CLI (https://github.com/aws/kiro-cli)
git clone https://github.com/hcsung-aws/ai-developer-mickey.git
cd ai-developer-mickey
./install.sh
```

### Running

```bash
cd <project-directory>
kiro-cli chat --agent ai-developer-mickey
```

You can add CLI flags based on autonomy level:
```bash
# Balanced (auto-approve file read/write)
kiro-cli chat --agent ai-developer-mickey --trust-tools=fs_read,fs_write

# Autonomous (auto-approve most tools)
kiro-cli chat --agent ai-developer-mickey --trust-tools=fs_read,fs_write,execute_bash,grep,glob,code
```

### What Mickey Does Automatically

1. Project analysis and initial document generation
2. Autonomy level confirmation
3. Session log writing (MICKEY-N-SESSION.md)
4. Lesson recording and next session handoff
5. Automatic observation recording (auto_notes/)
6. Behavioral rule self-learning (adaptive.md)

## Benefits

### 1. Context Window Efficiency
- 3-Tier loading for selective information loading
- INDEX map pattern to first understand "what's where"

### 2. Work Continuity
- Maintain workflow even when restarting sessions
- Prevent purpose drift with PURPOSE-SCENARIO

### 3. Knowledge Accumulation
- Automatic fact recording with auto_notes/
- Behavioral rule self-learning with adaptive.md
- Lesson promotion path: auto_notes → context_rule → common_knowledge → system prompt

### 4. User Control
- Adjust autonomy level with Autonomy Preference
- Batch review of automatic records at session end
- High-risk decisions always require user confirmation

## Next Steps

- [Context Window Management](02-context-management-en.md) - 3-Tier loading and INDEX pattern
- [Session Continuity](03-session-continuity-en.md) - Session protocol and purpose management
- [Prompt Engineering](04-prompt-engineering-en.md) - Effective prompt structuring
- [Knowledge Management](05-knowledge-management-en.md) - Auto memory and lesson promotion
- [Prompt Evolution](06-prompt-evolution-en.md) - v2.0 → v7.2 evolution
- [Evolution Insights](08-evolution-insight-en.md) - How "using AI well" has evolved
