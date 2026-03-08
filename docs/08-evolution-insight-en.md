# Evolution of Using AI Well: What Mickey Discovered

> [한국어 버전](08-evolution-insight.md)

> A record of how "using AI effectively" has evolved through building and improving the Mickey agent, and where it's heading.

## Why Read This

If you've used an AI coding assistant, you've likely experienced:

- Having to re-explain yesterday's work today
- Drifting from the original purpose while immersed in work
- AI losing the big picture as the project grows
- AI being particularly weak with existing codebases

Mickey is an AI development agent that has solved these problems one by one through direct experience. This document organizes the patterns discovered in that process, showing that "using AI well" isn't just a prompting technique — it's a **system design problem**.

---

## Phase 1: The Memory Problem (v2.0, 2024-12)

### Cause: AI Can't Remember

The first problem discovered while developing the Godot replay system was simple. AI assistants forget everything when a session ends. Yesterday's design decisions, discovered bugs, agreed directions — all gone.

### Result: Session Continuity System

File-based memory was introduced:
- **SESSION.md**: Work records for each session
- **HANDOFF.md**: Key information to pass to the next session
- **context_rule/**: Project-specific rules (preventing repeated failures)
- **common_knowledge/**: Project-independent reusable patterns

### Discovered Principle

> **"AI's memory is files."** Conversations are volatile, but files persist. Session continuity can only be guaranteed through structured files.

This was later rediscovered in Harness Engineering as "repository knowledge as the system of record."

---

## Phase 2: The Direction Problem (v5.0, 2025-01)

### Cause: AI Loses Direction

The second problem discovered while developing the packet capture agent was more subtle. AI performs given tasks well but forgets **why it's doing them**. When immersed in implementation, it drifts from the original purpose, chooses complex solutions, and treats symptoms instead of root causes.

### Result: Purpose-First Principles + Checklists

Five core principles were introduced:
1. Purpose first — basis for all decisions
2. Simplicity first — simple alternatives before complex solutions
3. Root cause first — fix causes, not symptoms
4. Analysis before implementation — no guessing
5. User confirmation before changes — no unilateral action

v5.1~v5.4 continued adding lessons through real projects (AI Agent Automation Platform):
- v5.1: Prerequisite verification
- v5.2: Incremental adoption
- v5.3: Session end protocol
- v5.4: Mandatory testing protocol

### Discovered Principle

> **"Principles are born from failure."** Behind each REMEMBER item is a real failure experience. The 24 principles in v5.0 were extracted from 24 failures.

---

## Phase 3: The Efficiency Problem (v6.0-6.2, 2026-02)

### Cause: More Information Isn't Better

Prompts accumulated through v5.x became bloated with domain-specific content (C++ patterns, game server checklists, MSVC build rules). In new projects, useless information occupied the context window, and AI's attention was diverted to irrelevant rules.

### Result: 3-Stage Lightweight

**v6.0 — Structural Innovation**: Removed all domain-specific content and introduced 3-Tier Context Loading.
- T1 (always): Universal principles only (system prompt)
- T2 (session start): Project core information only
- T3 (on demand): Specific knowledge files only

**v6.1 — INDEX Map Pattern**: Further refined T3. Used INDEX.md as a "table of contents for knowledge," grasping "what knowledge exists" at session start and loading only needed files during actual work.

**v6.2 — PURPOSE-SCENARIO**: Separated "purpose" from a checklist item into an independent document. Elevated to the top priority for all decisions, with continuous alignment checks during work.

### Discovered Principle

> **"Give a map, not an encyclopedia."** What AI needs isn't all information, but knowing where what information is. Progressive disclosure — start from a small entry point and explore deeply when needed.

This exactly matches the Harness Engineering pattern of "using AGENTS.md as a table of contents, distributing details in docs/." Mickey independently discovered this pattern.

---

## Phase 4: The Recording Problem (v6.3, 2026-03)

### Cause: Users Must Direct Everything

A problem discovered while analyzing Claude Code's Auto Memory feature. Mickey organizes lessons well, but **only records when the user says "record this."** Observed facts like build commands, file roles, and error fixes could be recorded automatically by AI, but requiring user confirmation each time is inefficient.

### Result: Dual Auto Memory

Separated "rules written by users" from "facts observed by AI":
- **auto_notes/**: Facts automatically recorded by AI (batch review at session end)
- **context_rule/**: Rules verified by users (immediate confirmation)
- **common_knowledge/**: Universal patterns (immediate confirmation)

File size limits, work unit triggers, and lesson promotion paths were also introduced.

### Discovered Principle

> **"Low-risk observations automatically, high-risk decisions together with users."** Requiring user confirmation for everything is safe but slow. Distinguishing autonomy levels by risk secures both speed and safety.

---

## Phase 5: Autonomy and Self-Improvement (v7~v7.2, 2026-03)

### Cause: Single Agent Limits + User Dependency

Problems discovered while researching 2026 AI development trends (Harness Engineering, AI-DLC, Ouroboros). Mickey performs analysis/implementation/verification as a single agent, and all behavioral rules must be taught by users.

### What Was Learned from Trends

**Harness Engineering** (OpenAI): Repo is the system of record for knowledge, deterministic linters and structural tests enforce architecture, and garbage collection agents manage entropy.

**AI-DLC**: Core formula is `autonomy = f(criteria clarity)` — the clearer the completion criteria, the more autonomously AI can execute. Backpressure (constraint-based quality gates) says "satisfy this condition" instead of "do it this way."

**Ouroboros**: Self-modifying AI agent with supervisor/worker model for task decomposition and parallel execution.

### Result: v7~v7.2 Implementation Complete

**v7 — Autonomous Execution + Backpressure**:
- Autonomous when CC clear + rollback possible + verifiable
- No proceeding on verification failure (Backpressure)
- Brownfield onboarding: Auto-analysis when existing codebase detected
- T1.5 layer: Separate detailed guidelines to `~/.kiro/mickey/` + `install.sh` deployment

**v7.1 — Adaptive Rules**:
- Design `context_rule/adaptive.md` as a self-modifiable sub-prompt
- Auto-add rules when patterns discovered during work, batch user review at session end

**v7.2 — Autonomy Preference**:
- 3-level autonomy (Conservative / Balanced / Autonomous)
- CLI `--trust-tools` flag integration
- Confirm user preference in first session → Record in ENVIRONMENT.md

### Discovered Principle

> **"The value of autonomous execution is lessons, not speed."** Execute fast, learn from results, structure what's learned to do better next time. And different users want different autonomy levels — that's also something to adapt to.

---

## Core Discovery: Incremental Harness Building in Brownfield

One discovery runs through the entire evolution process.

Harness Engineering, AI-DLC, and Ouroboros are all **optimized for Greenfield (new development)**. They design harnesses from scratch in clean environments, generate code from nothing, or decompose intents cleanly.

But most real-world projects are **Brownfield (improving existing code)**. There's existing code, implicit rules, and technical debt. Birgitta Böckeler on Martin Fowler's site points out: *"Retrofitting a harness to an existing codebase is like running static analysis for the first time on code that's never been analyzed."*

Mickey's evolution naturally provides the answer to this problem:

```
Harness Engineering:  Design complete harness from scratch (Greenfield optimal)
Mickey:               Harness thickens as sessions accumulate (Brownfield suitable)

Session 1: Environment scan + basic structure understanding
Session 2: Key file roles + build commands accumulated
Session 3: Dependency patterns + repeated failure rules accumulated
...
Session N: Project expert-level knowledge base complete
```

In v7, a Brownfield onboarding protocol was implemented to automatically perform structured exploration when existing codebases are detected.

This is Mickey's unique position. When session continuity (Phase 1) + purpose-first (Phase 2) + efficient structuring (Phase 3) + auto recording (Phase 4) + autonomous execution (Phase 5) combine, you get **an AI development agent that becomes increasingly sophisticated in Brownfield as sessions accumulate**.

---

## The Full Picture of Evolution

| Phase | Version | Problem Discovered | Solution | Core Principle |
|-------|---------|-------------------|----------|---------------|
| 1 | v2.0 | AI can't remember | File-based session continuity | AI's memory is files |
| 2 | v5.0-5.4 | AI loses direction | Purpose-first + failure-based principles | Principles are born from failure |
| 3 | v6.0-6.2 | Information overload is harmful | 3-Tier loading + INDEX maps | Give a map, not an encyclopedia |
| 4 | v6.3 | Confirming everything is slow | Dual auto memory | Low-risk auto, high-risk together |
| 5 | v7~v7.2 | Single agent limits + user dependency | Autonomous execution + Adaptive Rules + Autonomy Preference | Value of autonomous execution is lessons |

Each Phase builds on the previous. Without memory, you can't set direction; without direction, structuring is meaningless; without structure, auto recording creates chaos; without auto recording, lessons from autonomous execution are lost.

---

## Phase 6: Future Directions

With Phase 5 complete, Mickey has "session continuity + purpose management + efficient structuring + auto memory + autonomous execution + self-improvement." Areas to explore next:

1. **Deeper multi-agent collaboration**: Current subagent delegation is at guide level. Actual orchestrator-worker pattern for parallel processing + result integration
2. **Cross-project knowledge transfer**: common_knowledge/ is shared across projects but still manual. Mechanism for automatically recommending Project A's lessons to Project B
3. **Proactive behavior**: Currently Mickey is reactive (user requests → execute). Evolve to proactive: suggest "autonomously executable items from previous incomplete work" at session start

These directions are still in planning and will be refined through real projects.

---

## References

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — Repo-based knowledge management, progressive disclosure, garbage collection
- [AI-DLC](https://ai-dlc.dev/) — Hat role separation, Completion Criteria, Backpressure, autonomy modes
- [Ouroboros](https://github.com/razzant/ouroboros) — Self-modifying AI, supervisor/worker, background consciousness
- [Anyline: Agents Meta-Repo Pattern](https://seylox.github.io/2026/03/05/blog-agents-meta-repo-pattern.html) — Brownfield multi-repo agent context management
- [Martin Fowler/Böckeler: Harness Engineering Analysis](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — Pre-AI vs Post-AI maintenance
- [AWS: Agentic AI Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html) — Orchestration/delegation patterns

---

*Written: Mickey 7 session (2026-03-08), Updated: Mickey 10 session (2026-03-09)*
*This document itself is a product of Mickey's evolution. It will be updated when new discoveries are made in future sessions.*
