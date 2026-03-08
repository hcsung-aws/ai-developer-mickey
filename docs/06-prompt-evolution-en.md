# Prompt Evolution: v2.0 → v7.2

> [한국어 버전](06-prompt-evolution.md)

> AI prompts aren't "written" — they're "evolved"

## Overview

This document explains how Mickey's prompt evolved through real projects, and **why it had to evolve that way**.

**Core message**: The driving force of prompt evolution is **failure experience**.

## Evolution Flow

```
v2.0 (Foundation) → v5.0 (Specificity) → v6.0 (Lightweight) → v7.2 (Autonomy)
  File-based          Checklists           3-Tier separation    Self-improvement
  memory              Protocols            INDEX pattern         Autonomous execution
```

---

## Phase 1: v2.0 → v5.0 (Foundation → Specificity)

### Evolution Summary

| Area | v2.0 | v5.0 | Reason for Change |
|------|------|------|-------------------|
| REMEMBER principles | 6 | 18 | New failure patterns discovered |
| Checklists | None | 7 | General guidelines can't prevent specific mistakes |
| Automation | None | Session end protocol | Repeated instructions inefficient |
| Purpose check | None | Required | Lost purpose while focused on means |

### 1. "Record" → "Confirm Purpose First"

**Mickey 7's failure:**
- Purpose: Packet capture testing
- Attempt: Set up Forgotten Server (open-source game server) → 3 days spent
- Pivot: Build custom simulator → 1.5 days to completion

**Lesson**: AI works hard on given tasks but doesn't judge whether they're optimal for the purpose.

```
❌ "Set up Forgotten Server"
✅ "I want to test packet capture. Analyze the simplest approach first"
```

### 2. "Analyze" → "Follow Checklists"

**Mickey 8's failures:**
- Buffer ownership issue → Character coordinate warping
- Nested lock deadlock → abort() triggered
- Broadcast omission → Player departure not reflected

**Lesson**: AI follows specific checklists better than general guidelines ("analyze").

### 3. "Problem Solving" → "Root Cause First"

**Mickey 7's failure:**
- vcpkg tar extraction error → Cache delete (fail) → Update (fail) → Error log analysis → CMake bug found

**Lesson**: AI prefers quick fixes but easily misses root causes.

### 4. "Knowledge Management" → "Systematized Failure Experience"

v2.0 recorded "what was done", v5.0 recorded "what NOT to do."

```markdown
### Lesson N: [Topic]
- **Problem**: [What went wrong]
- **Cause**: [Why it went wrong]
- **Fix**: [How it was resolved]
- **Lesson**: [What to avoid next time]
```

### 5. "Session Continuity" → "Automated Protocol"

v2.0: Instruct "write session log" every time → v5.0: Say "session cleanup" and everything runs automatically.

**Lesson**: Repeated patterns should be automated in the prompt.

---

## Phase 2: v5.0 → v6.3 (Specificity → Lightweight)

### Why It Had to Change

v5.0's problem: Prompt **bloated with domain-specific content**.
- Godot checklists, C++ async checklists, MSVC warnings...
- Unnecessary content occupying context in new projects

### v6.0: Lightweight/Optimization

| Change | Reason |
|--------|--------|
| Remove domain-specific content | Transition to universal agent |
| REMEMBER 18 → 8 | Move domain-specific principles to context_rule/ |
| Introduce 3-Tier Context Loading | Prompt has principles only, details in files |
| Introduce Document Schema | Ensure document format consistency |

**Insight**: Shifted from "putting everything in the prompt" to "prompt has principles only, details in files."

### v6.1: INDEX Map Pattern

**Problem**: As knowledge files grow, figuring out "what's in which file" itself consumes context.

**Solution**: Introduce **trigger → file → summary** mapping in INDEX. Read only INDEX at session start, load specific files only when triggers match during work.

### v6.2: PURPOSE-SCENARIO Independent Document

**Problem**: "Purpose first" exists in REMEMBER, but gets formally checked and skipped when immersed in work.

**Solution**: Separate purpose into independent document, load as T2 top priority. Alert user when purpose drift detected.

### v6.3: Auto Memory Pattern

**Problem**: Inefficient to instruct "record this" every time. User-written rules and AI-observed facts mixed together.

**Solution**: Dual auto memory:
- `auto_notes/`: AI-observed facts (descriptive, batch review at session end)
- `context_rule/adaptive.md`: AI self-generated rules (adaptive, batch review at session end)

---

## Phase 3: v7.0 → v7.2 (Lightweight → Autonomy)

### Why It Had to Change

Up to v6.3, the model was "user instructs → AI executes." But requiring confirmation even for repetitive, clear tasks is inefficient.

### v7.0: Autonomous Execution + Subagent + Brownfield

| Change | Reason |
|--------|--------|
| Autonomous execution conditions | Autonomous when CC clear + rollback possible + verifiable |
| Backpressure | No proceeding on verification failure |
| Brownfield onboarding | Auto-analysis when existing codebase detected |
| T1.5 layer introduced | Separate detailed guidelines to `~/.kiro/mickey/` |

**Insight**: Autonomy is a means, **feedback loops are the key**. Execute autonomously but always verify.

### v7.1: Adaptive Rules

**Problem**: Users had to manually teach project-specific behavioral rules.

**Solution**: Design `context_rule/adaptive.md` as a self-modifiable sub-prompt. When patterns are discovered during work, rules are added automatically.

### v7.2: Autonomy Preference

**Problem**: Different users want different autonomy levels. Some want to confirm every change, others just want results.

**Solution**: 3-level autonomy (Conservative / Balanced / Autonomous) + CLI `--trust-tools` integration.

---

## REMEMBER Section Evolution

```
v2.0: 6 (universal principles)
  ↓ Failure experience accumulation
v5.0: 18 (including domain-specific)
  ↓ Lightweight
v6.0: 8 (domain-specific → moved to context_rule/)
  ↓ New lessons accumulated
v7.2: 15 (autonomy/verification/testing principles added)
```

Key: REMEMBER retains only **fundamental principles validated through projects**. Domain-specific lessons go to context_rule/, universal patterns to common_knowledge/.

---

## Meta-Insights: Laws of Prompt Evolution

### 1. Failure Drives Evolution

| Session | Failure | What Was Added |
|---------|---------|---------------|
| Mickey 7 | Lost purpose, excessive complexity | Purpose first, simplicity first |
| Mickey 8 | Buffer ownership, deadlock | Async checklists |
| Mickey 9 | Domain-specific bloat | 3-Tier, lightweight |
| Mickey 10 | Insufficient autonomy | Autonomous execution, Backpressure |

### 2. Abstraction Level Evolution

```
General guidelines → Specific checklists → Automated protocols → Self-improvement
"Analyze" → "Check buffer ownership" → "Auto-execute on session cleanup" → "adaptive.md self-modification"
```

### 3. Prompts Oscillate Between Expansion and Contraction

```
v2.0 (concise) → v5.0 (expansion) → v6.0 (contraction/lightweight) → v7.2 (structural expansion)
```

Expansion: Rules added as failure experiences accumulate
Contraction: Separate domain-specific, keep only principles
Structural expansion: Maintain principles but add execution mechanisms (autonomy, self-improvement)

---

**Core message:**
> AI prompts aren't "written" — they're "evolved."
> Failure experience drives prompt improvement, maturing through cycles of expansion and contraction.

## Next Steps

- [Changelog](07-changelog-en.md) - Detailed version-by-version changes
- [Evolution Insights](08-evolution-insight-en.md) - How "using AI well" has evolved
- [Packet Capture Agent Case Study](case-study/packet-capture-agent.md) - v5.0 practical application
