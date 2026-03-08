# Prompt Engineering

> [한국어 버전](04-prompt-engineering.md)

## Why Prompts Matter

A system prompt is the **behavioral rulebook** for an AI agent. A well-structured prompt makes AI behave consistently; a poor one produces different results every session.

Mickey's prompt isn't "write once and done" — it has **continuously evolved through failure experiences**.

## System Prompt Evolution

### Early (v1~v2): Core Idea Only

```
An agent that saves success and failure records from each session to files,
carries them forward to subsequent sessions, and solves problems through continuous improvement
```

Simple, but the core was there: **file-based memory + continuous improvement**.

### Growth (v3~v5): Specific Action Guidelines Added

Gaps became apparent through the Godot project:

| Problem | Added Guideline |
|---------|----------------|
| Knowledge scattered in context | KNOWLEDGE MANAGEMENT section |
| Repeating same mistakes | CONTEXT RULES section |
| Working without purpose | REMEMBER: Purpose first |
| Starting implementation without analysis | PROBLEM-SOLVING PROTOCOL |
| No context overflow response | Context Window monitoring |

v5.0 established **checklist-based protocols**.

### Transition (v6.0~v6.3): Lightweight and Automated

Prompts up to v5 had domain-specific content (Godot, packet capture, etc.) mixed in. v6.0 brought fundamental structural change:

| Change | Reason |
|--------|--------|
| Remove domain-specific content | Transition to universal agent |
| Introduce 3-Tier Context Loading | Context window efficiency |
| INDEX map pattern (v6.1) | Selective knowledge loading |
| PURPOSE-SCENARIO independent document (v6.2) | Strengthen purpose tracking |
| auto_notes auto memory (v6.3) | Separate observed facts from rules |

**Insight**: Shifted from "putting everything in the prompt" to "prompt has principles only, details in files."

### Current (v7~v7.2): Autonomy and Self-Improvement

| Change | Reason |
|--------|--------|
| Autonomous execution conditions (v7) | Autonomous when CC clear + rollback possible |
| Backpressure (v7) | No proceeding on verification failure |
| Adaptive Rules (v7.1) | AI self-learns behavioral rules |
| Autonomy Preference (v7.2) | Per-user autonomy level selection |

## Prompt Structuring Principles

### Why

As prompts get longer, AI misses important parts. Hierarchical structuring separates "always follow" from "reference when needed."

### What

Mickey v7.2's prompt consists of two layers:

| Layer | Location | Content | Size |
|-------|----------|---------|------|
| **T1** | System prompt | Identity, session protocol, REMEMBER | Core only |
| **T1.5** | `~/.kiro/mickey/` | Detailed execution guidelines (Brownfield, autonomy, Backpressure, etc.) | Extensible |

### How

**What goes in T1 (system prompt)**:
- Core identity ("You are Mickey")
- Session protocol (First/Continuing/During/End)
- Problem-solving protocol
- 3-Tier loading rules
- REMEMBER (15 core principles)

**What goes in T1.5 (extended guidelines)**:
- Brownfield onboarding procedure
- Autonomy Preference detailed guide
- Backpressure rules
- Architectural Guard
- Adaptive Rules safeguards

**Key**: T1 is "what to do", T1.5 is "how to do it."

### REMEMBER Section

A **core principles list** at the end of the prompt. The top-priority rules AI references during work:

```
1. Purpose first: PURPOSE-SCENARIO.md is the top priority for all decisions
2. Simplicity first: Simple alternatives before complex solutions
3. Session log FIRST, then work
4. Analysis BEFORE implementation
5. Check error logs immediately (no guessing)
...
```

Each item notes **which session it was learned from** (e.g., "Mickey 10"). This enables tracing the origin of principles.

### Document Schema

Defines **required sections** for documents Mickey generates:

```
| Document | Required Sections |
| SESSION.md | Goal, Tasks(+CC), Progress, Decisions, Files, Lessons, Next |
| HANDOFF.md | Status(1-2 lines), Next(1-2 lines), Important Context, Quick Reference |
| PURPOSE-SCENARIO.md | Purpose, Scenarios, Acceptance Criteria, Last Confirmed |
```

Defining schemas prevents AI from creating documents in different formats each time.

## Effective User Prompts

**User instructions** matter as much as system prompts.

### DO ✅

**1. Provide context**
```
❌ "Fix the error"
✅ "In the replay system, velocity diff=209.45 error at Frame 139.
    Previous Mickey fixed position errors with Delta sync,
    velocity might have similar cause. Analyze please."
```

**2. Request step-by-step confirmation**
```
❌ "Implement everything"
✅ "First analyze current implementation, identify issues,
    then suggest solutions. I'll confirm at each step."
```

**3. Guide to reference previous work**
```
✅ "Check previous Mickey records and guidelines"
✅ "Check context_rule for any known issues"
```

### DON'T ❌

```
❌ "Do it well" / "Figure it out"          → Vague instructions
❌ "Got an error" / "Doesn't work"         → No context
❌ "Do A and B and C and D and E"          → Too many requests at once
```

## Practical Prompt Patterns

### Pattern 1: Analyze → Suggest → Confirm

```
User: "Analyze current implementation for any issues"
Mickey: [Analyze] → "Found 2 issues. Shall I fix them?"
User: "Yes, fix them"
```

### Pattern 2: Context + Constraints → Work Request

```
User: "Working on Phase 3-1. Both paddles AI-controlled,
       need various scenarios. Suggest based on current implementation and requirements"
```

### Pattern 3: Problem + Reference Previous Solutions

```
User: "Could Total frames played: 0 be an initialization issue?
       Analyze existing implementation"
```

## Prompt Improvement Cases

### Case 1: Leveraging Existing Knowledge

```
❌ "Find the Windows path" → Full directory search attempt → Failed
✅ "Check previous Mickey records to find the Windows path"
   → Found immediately in context_rule/project-context.md
```

**Lesson**: Giving AI hints about "where to look" is efficient.

### Case 2: Verifying Prerequisites

```
❌ "Run the test" → Failed due to incomplete setup
✅ "Check previous records to verify all settings are in place before running tests"
   → Found 2 missing settings, fixed them
```

**Lesson**: "Verify then execute" is faster than "execute immediately."

## Next Steps

- [Knowledge Management](05-knowledge-management-en.md) - Auto memory and lesson promotion
- [Prompt Evolution](06-prompt-evolution-en.md) - v2.0 → v7.2 detailed evolution
- [Evolution Insights](08-evolution-insight-en.md) - How "using AI well" has evolved
