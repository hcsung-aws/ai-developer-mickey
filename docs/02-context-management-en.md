# Context Window Management

> [한국어 버전](02-context-management.md)

## What is a Context Window?

A context window is the amount of text an AI model can process at once. Kiro CLI provides a 200,000 token context window, but even this can be insufficient for complex projects.

## The Problem

### Typical Failure Scenario

```
1. Start analyzing complex codebase
2. Read multiple files → Context 50% used
3. Additional analysis and coding → Context 70% used
4. Need more information → Context 90% used
5. Context overflow → Session summary (Compact)
6. Important context lost → Work fails
```

### Restarting Without Mickey

```
[Previous Session]                    [After Compact]
- Detailed analysis results           - "Analyzing Godot engine"
- Design decisions                    - "Need to implement logging"
- Attempted approaches                → Most specific context lost
- Reasons for failure
```

Core problem: **"Loading everything into context causes you to miss what actually matters."**

## Mickey's Solution: 3-Tier Context Loading

### Why

Context window is finite. Loading everything at once buries important information and leaves no room for later in the session. **"Give a map, not an encyclopedia"** — load only what's needed, when it's needed.

### What

Information is classified hierarchically by importance and loading timing:

| Tier | Loading Time | Content | Example |
|------|-------------|---------|---------|
| **T1** | Always | Core identity, universal principles | System prompt |
| **T1.5** | Session start | Detailed execution guidelines | `~/.kiro/mickey/extended-protocols.md` |
| **T2** | Session start | Project core documents | PURPOSE-SCENARIO, HANDOFF, adaptive.md |
| **T3a** | Session start | Knowledge maps (INDEX) | `common_knowledge/INDEX.md` |
| **T3b** | Only when needed | Detailed knowledge | Files matched by INDEX triggers |

### How

```
Session Start
  ├─ T1: System prompt (always loaded)
  ├─ T1.5: ~/.kiro/mickey/ (loaded if exists)
  ├─ T2: PURPOSE-SCENARIO → HANDOFF → PROJECT-OVERVIEW → adaptive.md
  ├─ T3a: Load INDEX files (knowledge maps only)
  │
  └─ During work...
       └─ "error fix" keyword occurs → INDEX trigger match
            └─ T3b: Load auto_notes/error-fixes.md (that file only)
```

**Key**: T3a (INDEX) is a map that only tells you "what knowledge exists." Actual detailed content (T3b) is loaded only when needed during work.

## INDEX Pattern: Trigger-Based Knowledge Maps

### Why

As knowledge files grow, figuring out "what's in which file" itself consumes context. INDEX solves this as a table of contents.

### What

INDEX is a mapping table in **trigger → file → summary** format:

```markdown
# Common Knowledge INDEX

## Knowledge Map

| Trigger | File | Summary |
|---------|------|---------|
| INDEX design, knowledge map | progressive-disclosure.md | INDEX=TOC pattern principles |
| agent design, context window | agent-design-patterns.md | Script delegation, event-based triggers |
```

### How

1. Load only INDEX at session start (dozens of lines)
2. When keywords/paths match triggers during work, load only that file
3. Files not in INDEX are not loaded (update INDEX first)

Triggers can be **path patterns** as well as keywords:
- When modifying `power-mickey/*` files → load `kiro-powers.md`
- Keywords `error`, `에러` → load `error-fixes.md`

Mickey manages 3 INDEXes:

| INDEX | Location | Purpose |
|-------|----------|---------|
| `context_rule/INDEX.md` | Project rules | Preventing repeated failures, environment settings, known issues |
| `common_knowledge/INDEX.md` | Universal patterns | Project-independent reusable patterns |
| `auto_notes/NOTES.md` | Observation records | Facts automatically recorded by AI |

## Auto Memory: auto_notes + adaptive.md

### Why

"Rules written by users" and "facts observed by AI" have different natures. Separating them allows different trust levels and management approaches for each.

### What

| Store | Nature | Review Timing | Example |
|-------|--------|--------------|---------|
| `auto_notes/` | Observed facts (descriptive) | Batch at session end | Build commands, file roles, error fixes |
| `context_rule/adaptive.md` | AI self-generated rules (adaptive) | Batch at session end | "In this project, run lint before tests" |
| `context_rule/` | Verified rules (normative) | Immediate user confirmation | Preventing repeated failures, environment constraints |
| `common_knowledge/` | Universal patterns (normative) | Immediate user confirmation | Architecture patterns, technology comparisons |

### How

**auto_notes/** — Record facts discovered during work immediately (no user confirmation needed):
```
auto_notes/
├── NOTES.md          # Index (loaded at session start as T3a)
├── commands.md       # Build/test/lint commands
├── file-roles.md     # File paths and roles
└── error-fixes.md    # Verified error fixes
```

**adaptive.md** — Behavioral rules Mickey learns on its own:
```markdown
# Adaptive Rules
- When modifying README in this project, update both Korean/English simultaneously
- When changing install.sh, verify 3-way sync (agent JSON, repo, ~/.kiro/)
```

At session end, changes to auto_notes and adaptive.md are presented in batch for user review/edit/delete.

**Lesson promotion path**: Recurring patterns are promoted to higher tiers:
```
auto_notes → context_rule → common_knowledge → system prompt (REMEMBER)
```

## File Size Limits

### Why

If files loaded at session start become bloated, 3-Tier loses its meaning. Size guards on each file maintain context efficiency.

### Limits

| File | Line Limit | Item Limit |
|------|-----------|------------|
| T2 files (each) | 50 lines | Max 5 items per key section |
| project-context.md | 80 lines | Lessons Learned max 5 |
| T3a indexes (each) | 50 lines | — |
| auto_notes/NOTES.md | 50 lines | — |

### When Exceeded

- Condense, promote/remove old items, split detailed content
- Lessons Learned over 5 → promote old ones to `context_rule/`
- Similar INDEX triggers → merge
- Check line count on file modification → clean up immediately when approaching limit

## Context Window Monitoring

Mickey adjusts behavior based on context window usage:

| Usage | Action |
|-------|--------|
| **50%** | Suggest session log cleanup (summarize completed work, remove trial-and-error) |
| **70%** | Recommend new session after current task, prepare handoff |
| **90%** | Immediate new session, generate handoff |

### Without Mickey vs With Mickey

```
[Without Mickey]                      [With Mickey]
Session 1: 100% → Compact → Info lost  Mickey 1: 70% → Save session log
Session 2: Start from scratch           Mickey 2: Continue previous work → 50%
Session 3: Compact again...              Mickey 3: Additional work → 65%
→ Repeated work, slow progress           → Cumulative learning, fast progress
```

## Practical Examples

### Godot Engine Analysis (13,666 files)

**Problem**: Can't fit a massive codebase into context

**Solution** (3-Tier applied):
1. Grasp overview → write `common_knowledge/godot/overview.md` (Context 5%)
2. Register triggers in INDEX → selectively load only needed topics (2-3% each)
3. Complete work without loading the entire engine into context

**Insight**: "You don't need to know everything. You just need to know where everything is."

### Mickey Self-Improvement (v2 → v7.2)

**Problem**: As prompts grew complex, loading volume at session start increased

**Solution**:
- v6.0: Remove domain-specific content, introduce 3-Tier → lightweight system prompt
- v6.1: INDEX map pattern → selective T3b loading
- v6.3: Separate auto_notes → separate observed facts from rules
- v7.2: adaptive.md → separate AI self-learning rules

**Insight**: "Classifying information matters more than adding information."

## Best Practices

### DO ✅

1. **Hierarchical loading**: INDEX first, details only when needed
2. **Concise records**: Key information only, use bullet points
3. **Respect size guards**: Check line count when modifying files
4. **Regular cleanup**: Clean session logs when reaching 50%

### DON'T ❌

1. **Load all files at once**: Wastes context, buries important info
2. **Verbose session logs**: Results/decisions/issues only, not essays
3. **Work past 90%**: Risk of information loss after Compact
4. **Add knowledge files without INDEX**: Creates orphan files that never get loaded

## Next Steps

- [Session Continuity](03-session-continuity-en.md) - Session protocol and purpose management
- [Knowledge Management](05-knowledge-management-en.md) - Auto memory and lesson promotion
- [Case Study](case-study/godot-replay-system.md) - Godot replay system case study
