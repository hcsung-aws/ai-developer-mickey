# Session Continuity

> [한국어 버전](03-session-continuity.md)

## The Problem

AI assistants forget everything when a session ends. Conversations are volatile, but files persist.

```
[Session 1 - Morning]
User: "Add a logging system"
AI: Analyze → Design → Start implementation → Context 70%

[Session 2 - Afternoon]
User: "Continue where we left off"
AI: "What should I continue?"
→ No previous context, need to explain from scratch
```

Mickey solves this with a **file-based session protocol**.

## Session Protocol

### Why

Session continuity isn't just "remembering previous work." It's about **maintaining purpose, accumulating lessons, and enabling the next session to start working immediately**. Without a protocol, every session starts from zero.

### What

Mickey's sessions follow a 4-stage lifecycle:

| Stage | When | Key Actions |
|-------|------|-------------|
| **First Session** | Mickey 1 | Environment scan → Confirm purpose → Generate initial documents |
| **Continuing Session** | Mickey N+1 | Load context → Reconfirm purpose → Create session log |
| **During Session** | Working | Trigger-based log updates + purpose alignment checks |
| **Session End** | Cleanup | Review auto records → Promote lessons → Generate handoff |

### How

#### First Session (Mickey 1)

When starting in a project with no Mickey files:

```
1. Environment scan (OS, directory, git)
2. "When this project is complete, how will it be used?" → Confirm purpose + scenarios
3. Confirm autonomy level (Conservative / Balanced / Autonomous)
4. Project analysis → Generate initial documents
5. Start work after user confirmation
```

Generated documents: PURPOSE-SCENARIO.md, PROJECT-OVERVIEW.md, ENVIRONMENT.md, FILE-STRUCTURE.md, DECISIONS.md, MICKEY-1-SESSION.md

#### Continuing Session (Mickey N+1)

When continuing in a project with existing Mickey files:

```
1. Context loading (by priority):
   PURPOSE-SCENARIO.md ← Top priority
   → Latest HANDOFF.md
   → Latest SESSION.md
   → PROJECT-OVERVIEW.md
   → context_rule/project-context.md
   → adaptive.md
   → INDEX files (knowledge maps)

2. Reconfirm purpose + entropy check
3. Create MICKEY-(N+1)-SESSION.md
4. Summarize previous session + start work
```

#### During Session

Session logs are updated **per work unit**, not all at once at session end:

| Trigger | Action |
|---------|--------|
| TODO item completed | Update session log Progress |
| Error investigation→fix→verification complete | Record in Lessons Learned |
| Decision confirmed with user | Record in Key Decisions |
| 3+ files modified | Update Files Modified |
| context_rule/ or common_knowledge/ changed | Update session log + INDEX |

#### Session End

```
1. Final session log review (minimal work since triggers keep it current)
2. Present auto_notes/ + adaptive.md changes in batch → User review
3. Lesson promotion review → Apply after user confirmation
4. Generate lightweight HANDOFF (internal document for next Mickey)
```

## PURPOSE-SCENARIO: Purpose Management

### Why

AI works hard on given tasks but doesn't judge whether they're **optimal for the original purpose**. The deeper it gets into work, the easier it is to lose the big picture. If "purpose" is just a checklist item, it gets formally checked and skipped.

### What

`PURPOSE-SCENARIO.md` manages the project's **ultimate purpose and usage scenarios** as an independent document:

```markdown
# PURPOSE-SCENARIO

## Ultimate Purpose
A practical guide for naturally learning how to use AI well

## Usage Scenarios
1. Developer applies Mickey to their project → incremental improvement
2. Addressing issues during infra operations with Mickey → cross-session memory
3. Improving Mickey itself → agent system evolution

## Acceptance Criteria
...

## Last Confirmed
2026-03-01 (Mickey 5)
```

### How

- Loaded as **top priority** at session start (T2 highest)
- Alert user when these situations occur during work:
  - Implementation direction conflicts with usage scenarios
  - Feature expansion reveals different direction from original purpose
  - Technical constraints require changing approach to achieve purpose
- Track last confirmation with `Last Confirmed` field

## Session Logs and Handoffs

### Why

Session logs (SESSION.md) are **detailed records of the current session**, while handoffs (HANDOFF.md) are **summary transfers for the next session**. Separating them lets the next Mickey read only the HANDOFF and start immediately, referencing SESSION if needed.

### Session Log (MICKEY-N-SESSION.md)

```markdown
# Mickey N Session Log

## Session Goal
Clear goal for this session

## Previous Context
Completed work from previous session, important decisions

## Current Tasks
- [ ] Task 1 | CC: Specify completion criteria
- [x] Task 2 | CC: Specify completion criteria

## Progress
### Completed
1. Implemented feature A
### In Progress
2. Debugging feature B (80%)

## Key Decisions
- GDScript > C++: 19x efficiency difference

## Files Modified
- replay_logger.gd (new)

## Lessons Learned
- Delta synchronization is the fundamental fix

## Context Window Status
65% — Safe range

## Next Steps
- Implement replay verification system
```

Key: Each task specifies **Completion Criteria (CC)** to clarify what "done" means.

### Handoff (MICKEY-N-HANDOFF.md)

```markdown
# Mickey N Handoff

## Current Status
Replay system implementation complete. Verification system not started.

## Next Steps
Implement state_validator.gd → Build batch test infrastructure

## Important Context
Only things NOT in SESSION.md/auto_notes

## Quick Reference
- Session log: MICKEY-N-SESSION.md
- Context window: 65%
```

Handoffs are **generated automatically without user confirmation** — they're internal documents for the next Mickey.

## Entropy Management

### Why

As sessions accumulate, documents grow, INDEX and actual files diverge, old SESSION files pile up, and auto_notes bloat — **entropy increases**. Left unchecked, 3-Tier loading efficiency degrades.

### What

Entropy checks are performed at Continuing Session start:

| Check Item | Action |
|-----------|--------|
| INDEX consistency | File found not in INDEX → Update INDEX |
| auto_notes freshness | Old/duplicate notes → Clean up or promote |
| SESSION archiving | Old SESSION/HANDOFF → Move to `sessions/` folder |
| File size | T2/T3a files exceeding line limits → Condense/split |

### How

```
Session Start
  ├─ Context loading
  ├─ Entropy check:
  │    ├─ Knowledge files not in INDEX? → Update INDEX
  │    ├─ auto_notes over 50 lines? → Split by category
  │    ├─ MICKEY-1~N-3 SESSION exists? → Archive to sessions/
  │    └─ project-context.md Lessons over 5? → Promote to context_rule/
  └─ Start work
```

## Practical Examples

### Godot Project: Mickey 1 → Mickey 2 Transition

**Mickey 1 ending**:
```
Context 61% → Save session log
Completed: Engine analysis, logging system design
Next: Implement auto test script
```

**Context Overflow occurs** → Compact loses detailed information

**Mickey 2 starting**:
```
Read previous SESSION.md → Restore context
"Starting as Mickey 2. Logging system design was completed in previous session."
→ Information lost to Compact restored from session log
```

**Insight**: "Conversations are volatile, but files persist."

### Mickey Self-Improvement: 9 Consecutive Sessions

The Mickey project itself is a practical example of session continuity:

```
Mickey 1~6: Foundation building (v2→v5)
  → 14 lessons analyzed, 3 promoted to common_knowledge
  → SESSION files archived to sessions/self/

Mickey 7~9: v7.2 implementation
  → Referencing previous lessons for autonomous execution, Backpressure, etc.
  → Preventing purpose drift with PURPOSE-SCENARIO
```

**Insight**: "Knowledge thickens as sessions accumulate. But only with entropy management."

## Best Practices

### DO ✅

1. **Update logs per work unit**: Don't write everything at session end
2. **Decisions with reasons**: "Chose GDScript" → "Chose GDScript (19x more efficient than C++)"
3. **Record failures too**: Attempted approaches and failure reasons save time in next sessions
4. **Regular entropy cleanup**: INDEX consistency, SESSION archiving

### DON'T ❌

1. **Verbose session logs**: Results/decisions/issues only, not essays
2. **Copy SESSION content to HANDOFF**: HANDOFF is 1-2 line summaries only
3. **Leave old SESSIONs**: Don't let SESSION files accumulate in root directory
4. **Skip purpose confirmation**: Don't drift from PURPOSE-SCENARIO while immersed in work

## Next Steps

- [Prompt Engineering](04-prompt-engineering-en.md) - Effective prompt structuring
- [Knowledge Management](05-knowledge-management-en.md) - Auto memory and lesson promotion
- [Prompt Evolution](06-prompt-evolution-en.md) - v2.0 → v7.2 evolution
