# Mickey Prompt Changelog

> [한국어 버전](07-changelog.md)

> Version-by-version changes to the Mickey system prompt.

## Version Summary

| Version | Date | Project | Key Change |
|---------|------|---------|------------|
| v2.0 | 2024-12 | Godot Replay System | Session continuity, knowledge management established |
| v5.0 | 2025-01 | Packet Capture Agent | Purpose-first, checklists, automation |
| v5.1 | 2026-01 | AI Agent Automation Platform | Prerequisite verification |
| v5.2 | 2026-02 | AI Agent Automation Platform | Documentation patterns, incremental adoption |
| v5.3 | 2026-02 | AI Agent Automation Platform | Session end protocol, auto improvement suggestions |
| v5.4 | 2026-02 | AI Agent Automation Platform | Mandatory testing protocol |
| v6.0 | 2026-02 | Prompt Lightweight | Domain-specific removal, schema transition, 3-Tier loading |
| v6.1 | 2026-02 | Mickey Self-Improvement | T3 layering - INDEX map pattern |
| v6.2 | 2026-02 | Mickey Self-Improvement | PURPOSE-SCENARIO based purpose management |
| v6.3 | 2026-03 | Mickey Self-Improvement | Auto Memory pattern (dual auto memory) |
| v7 | 2026-03 | Mickey Self-Improvement | Autonomous execution + Subagent + Brownfield onboarding |
| v7.1 | 2026-03 | Mickey Self-Improvement | Adaptive Rules (self-improving sub-prompt) |
| v7.2 | 2026-03 | Mickey Self-Improvement | Autonomy Preference (per-user autonomy level) |
| v7.3 | 2026-03 | Mickey Self-Improvement | REMEMBER consolidation (#12+#13 → WELC) + size management protocol |
| v7.4 | 2026-03 | Mickey Self-Improvement | REMEMBER retirement management (15→12) + Power Mickey full sync |
| v8 | 2026-03 | Mickey Self-Improvement | Global Knowledge (patterns/ + domain/) + Session-PURPOSE connection + Postmortem auto-trigger |
| v8.1 | 2026-04 | Mickey Self-Improvement | Knowledge Curator subagent + domain/ activation + Personal Vault → domain/ transition |
| v9 (PLAN) | 2026-05 | Mickey Self-Improvement | 3-Tier (R/G/S) + Domain-centric global knowledge + knowledge-organization Skill — POSTMORTEM-based redesign |
| v9.1 | 2026-06 | Mickey Self-Improvement | v9 PLAN correction+landing: Curator permission fix + Pre-staged Apply + T1.5 §17/§18 + ADDENDUM-first |

---

## v9.1 (2026-06-19~20)

**Project**: Mickey Self-Improvement (Mickey 21-22)
**Status**: v9 PLAN correction + Phase 1 landing complete

### Key Change: Curator Permission Fix + Pre-staged Apply Pattern

v9 PLAN (Mickey 20) diagnosed "v8.1 usage 0%", but 5-week measurement of 31 new sessions showed global domain 76 references / Curator 82 invocations. Correcting M20's sample bias (self-focused + 1.5-month timing), we invalidated PLAN's "retire Curator" decision and landed Curator in evolution + friction-resolution direction.

### Major Changes

1. **knowledge-curator.json permission fix** (D-7-FIX)
   - `tools` limited to 4: fs_read, fs_write, grep, glob
   - `allowedTools` auto-approve (previously: `[]` empty array required user approval each time)
   - `fs_write.allowedPaths` limited to 3: `~/.kiro/mickey/domain/**`, `**/context_rule/adaptive.md`, `**/_curator-staging/**`
   - `fs_write.deniedPaths` 7 items: `.git`, `node_modules`, `.venv`, `credentials*`, `.env*`, `*.key`, `*.pem`

2. **Pre-staged Apply pattern introduced**
   - Curator drafts proposal-area (common_knowledge/, context_rule/, patterns/, REMEMBER) changes in staging directory in final format
   - User decides in single response: "all" / numbers ("1,3") / "none" / "hold"
   - Resolves friction 1 (per-item approval in proposal area). Implemented within Kiro CLI feature range without additional tools/plugins

3. **T1.5 §17 Knowledge Lifecycle introduced**
   - Lifecycle diagram: auto_notes → Curator → direct-modify area + Pre-staged Apply area
   - Curator permissions + Pre-staged 5 steps + staging location auto-detection + 5-call validation period

4. **T1.5 §18 Activity Metrics introduced**
   - Baseline (5-week 31-session measurement): domain 2.45/session, Curator 2.65, auto_notes 5.55, [Protocol] 2.03
   - On threshold violation: 1st → re-measure, 2nd consecutive → postmortem trigger
   - Measurement script: `scripts/m21_measure_usage.py`
   - Auto-invocation mechanism deferred to Phase 3

5. **T1.5 §8 Adaptive Rules absorbed (stub only)**
   - Body absorbed into §17 + CURATOR-PROMPT.md. Stub remains

6. **T1 system prompt change (v15 → v16)**
   - Continuing Session 1b: entropy check adds `_curator-staging/` dangling items
   - Session End step 2: Curator delegate (corrected permissions) + first 5 calls auto git diff report
   - Session End step 3: Pre-staged items batch presentation + user single response
   - Lesson promotion procedure simplified to Curator auto-classification

7. **PURPOSE-SCENARIO updated**
   - 3-Tier evolution loop (R/G/S) + Curator + Pre-staged Apply made explicit
   - Acceptance Criteria → activity metrics measurement (refer T1.5 §18)

### M20 → M21 Diagnosis Comparison

| M20 conclusion (76 sessions) | M21 measurement (5-week 31 sessions) | Verdict |
|------------------------------|--------------------------------------|---------|
| Global domain 0% | 76 references / avg 2.45/session | M20 invalidated |
| Curator invocations 0 | 82 / avg 2.65/session | M20 invalidated |
| common_knowledge 5~10% | 58 / 1.87/session | consistent |
| auto_notes 80~100% | 172 / 5.55/session | consistent |

### Meta Lessons (REMEMBER candidates)

- Postmortem conclusions require sufficient incubation (3+ months) before re-validation
- Self-focused samples have high meta-work ratio → low domain entry triggers; self-diagnosis must prioritize comparison with other projects
- "Retire/review before adding" principle's true value emerges when retire candidate is self-disqualifying (M14 trap self-application)

### Supersedes (partial)

- IMPROVEMENT-PLAN-v9.md §6 Phase 1 (Curator → Skill transition), §7 migration priority #2, §9 decisions D-3/D-7/D-9
- ADDENDUM is SoT (`IMPROVEMENT-PLAN-v9-ADDENDUM.md`)

---

## v9 (PLAN, 2026-05-14)

**Project**: Mickey Self-Improvement (Mickey 20)
**Status**: PLAN written, implementation not started (Phase 1 from next session)

### Key Change: 3-Tier (R/G/S) + Domain-centric + Kiro Skill Integration

POSTMORTEM-2026-05-14 confirmed v8.1 failure (0% usage outside self-improvement) via 76-session quantitative measurement. After analysis of external trends (Claude Skills, AGENTS.md, Auto Memory), redesigned to be **Kiro-only + Domain-centric global knowledge**.

### Major Changes (Planned)

1. **3-Tier Simplification**: F (auto_notes) absorbed as G's entry. R (way of judging) / G (facts/structure) / S (procedures)
2. **Domain Global as Body**: `~/.kiro/mickey/domain/` is the body. Project-internal kept to truly project-specific facts only
3. **knowledge-organization Skill**: Replaces Curator subagent. Auto-invoked at 5/5 checkpoint
4. **Progressive stub lifecycle**: On promotion, body moves to new location, original becomes a stub with trigger info
5. **External standards integration excluded**: Mickey is Kiro CLI/IDE only. No CLAUDE.md/AGENTS.md integration
6. **Migration priority**: patterns/ retire → CURATOR-PROMPT conversion → common_knowledge stub → adaptive R/G/S split

### Diagnostic Data (POSTMORTEM)

- 76-session sample: ai-mickey 19s + skr-poc 40s + gamejob 18s
- Usage: auto_notes 80~100% / domain·Curator 0% (outside self-improvement) / adaptive.md gamejob 0%
- External trends: Claude Skills (2025-10), AGENTS.md cross-platform, Auto Memory, GraphRAG·MAGMA, Agent Stability Index

### Supersedes

- IMPROVEMENT-PLAN-v8.md, IMPROVEMENT-PLAN-v8.1.md (intent absorbed as diagnostic input)
- M16's 2026-06-08 Curator validation (terminated due to trigger structure flaw)

---

## v8 (2026-03-26)

**Project**: Mickey Self-Improvement (Mickey 12)

### Key Change: Global Knowledge Structure + Protocol Maturation

Resolved 3 structural gaps found from comprehensive analysis of 7 projects, 65+ sessions.

### Major Changes

1. **Global Knowledge Structure (`~/.kiro/mickey/patterns/` + `domain/`)**
   - patterns/: Domain-agnostic approach patterns (7-item cap, loaded at session start)
   - domain/: Domain knowledge (INDEX trigger-based on-demand, /knowledge as optional)
   - Promotion criteria: patterns/ = "Valid in completely different domain?", domain/ = "Reference value for same tech?"
   - Portability: markdown + INDEX is primary path, /knowledge is optional optimization

2. **Session-PURPOSE Connection**
   - Purpose Alignment section added to SESSION.md (contributing scenario + session scope)
   - Maintenance sessions classified as "Infrastructure"

3. **Session Metadata**
   - Session Meta added to SESSION.md (Type: Implementation/Self-Improvement/Maintenance/Planning)
   - Foundation for self-improvement cost visibility

4. **Postmortem Auto-trigger**
   - Lightweight postmortem suggested at 10+ sessions or after REMEMBER change used in 3+ projects
   - Lightweight = [Protocol] tag collection + positive/negative classification + 1-page summary

5. **install.sh Extended**: patterns/ + domain/ directory deployment

---

## v7.4 (2026-03-26)

**Project**: Mickey Self-Improvement (Mickey 11-12)

### Key Change: REMEMBER Retirement Management + Power Mickey Full Sync

Resolved REMEMBER exceeding the 12-item cap + synced Power Mickey steering to CLI v7.4 level.

### Major Changes

1. **REMEMBER Retirement (15→12)**
   - #3 "Session log FIRST" → Internalized in SESSION PROTOCOL
   - #8 "Suggest alternatives when complexity is excessive" → Overlaps with #2 "Simplicity first"
   - #10 "Core message first in documentation" → Overlaps with #1 "Purpose first"
   - Retired items moved to T1.5 Graduated REMEMBER (not deleted)

2. **Power Mickey Steering Full Sync**
   - mickey-core.md: Working principles 5→12 (based on CLI REMEMBER)
   - problem-solving.md: Added behavioral scenario/minimal code/bug propagation/Backpressure
   - session-protocol.md: Added Brownfield/entropy/behavioral scenario/Completion Criteria
   - self-improvement.md: Adaptive Rules/promotion enhancement/Graduated/Architectural Guard/postmortem
   - memory-protocol.md: Size management clarification

3. **Hook Version Updates**
   - init: 3.1.0 → 3.2.0 (PURPOSE-SCENARIO loading added)
   - close: 1.4.0 → 1.5.0 (project-lessons cap + lesson promotion guidance)

---

## v7.3 (2026-03-25)

**Project**: Mickey Self-Improvement (Mickey 11)

### Key Change: REMEMBER Consolidation + Size Management Protocol

Resolved overlap between REMEMBER items + introduced cap management system.

### Major Changes

1. **REMEMBER #12+#13 Consolidation**
   - Former #12 "Test-based completion" + #13 "Verification-based completion" → Merged into one
   - Added Test Harness (WELC) approach: wrap existing behavior in tests before modifying

2. **REMEMBER Size Management Protocol**
   - Cap: 12 items
   - When exceeded, oldest items with lowest violation frequency become retirement candidates
   - Retirement: Move to T1.5 "Graduated REMEMBER" section (not deleted)

3. **T1.5 §11 Graduated REMEMBER Section Added**

---

## v7.2 (2026-03-09)

**Project**: Mickey Self-Improvement (Mickey 9)

### Key Change: Autonomy Preference

Solves the problem of different users wanting different autonomy levels. Confirms autonomy level in first session and records in ENVIRONMENT.md.

### Major Changes

1. **3-level autonomy**: Conservative / Balanced (default) / Autonomous
2. **CLI integration**: `--trust-tools` flag for auto-approving tools per autonomy level
3. **T1.5 Section 4 expanded**: Detailed guide per autonomy level

---

## v7.1 (2026-03-09)

**Project**: Mickey Self-Improvement (Mickey 9)

### Key Change: Adaptive Rules

Solves the problem of users having to manually teach project-specific behavioral rules.

### Major Changes

1. **context_rule/adaptive.md**: Self-modifiable sub-prompt by AI
2. **Safeguards**: Existing context_rule/ files cannot be modified, only adaptive.md
3. **Promotion path**: adaptive.md → context_rule/ → common_knowledge/ → REMEMBER

---

## v7 (2026-03-08)

**Project**: Mickey Self-Improvement (Mickey 8-9)

### Key Change: Autonomous Execution + Brownfield Onboarding

### Major Changes

1. **Autonomous execution conditions**: CC clear + rollback possible + verifiable → autonomous
2. **Backpressure**: No proceeding on verification failure
3. **Brownfield onboarding**: Auto-analysis when existing codebase detected
4. **T1.5 layer**: Separate detailed guidelines to `~/.kiro/mickey/extended-protocols.md`
5. **install.sh**: Automated deployment

---

## v6.3 (2026-03-01)

**Project**: Mickey Self-Improvement (Mickey 5)

### Key Change: Auto Memory Pattern

### Major Changes

1. **auto_notes/**: AI auto-records observed facts (no user confirmation needed)
2. **File size limits**: T2 files 50 lines, T3a indexes 50 lines
3. **Work unit triggers**: Session log updated per work unit, not at session end
4. **Lesson promotion path**: auto_notes → context_rule → common_knowledge → REMEMBER

---

## v6.2 (2026-02-21)

**Project**: Mickey Self-Improvement (Mickey 14)

### Key Change: PURPOSE-SCENARIO Based Purpose Management

### Major Changes

1. **PURPOSE-SCENARIO.md**: Independent document with Ultimate Purpose, Usage Scenarios, Acceptance Criteria
2. **Session protocol**: "When this project is complete, how will it be used?" question in first session
3. **Purpose alignment check**: Alert user when implementation conflicts with scenarios

---

## v6.1 (2026-02-19)

**Project**: Mickey Self-Improvement (Mickey 13)

### Key Change: T3 Layering and INDEX Map Pattern

### Major Changes

1. **T3a/T3b split**: INDEX (knowledge map) loaded at session start, detailed files loaded only on trigger match
2. **INDEX format**: Trigger → File → Summary mapping table
3. **Power Mickey**: Hybrid context loading with SESSION-BRIEF + memorygraph

---

## v6.0 (2026-02-08)

**Project**: System Prompt Lightweight (Mickey 12)

### Key Change: Lightweight and Self-Contained Design

### Major Changes

1. **Template → Document Schema**: 8 full templates (~200 lines) → 1 schema table (~10 lines)
2. **Domain-specific removal**: C++ async, game server, MSVC checklists removed
3. **3-Tier Context Loading**: T1 (always) / T2 (session start) / T3 (on demand)
4. **REMEMBER cleanup**: 24 → 13 (universal principles only)

---

## v5.4 (2026-02-05)

### Key Change: Mandatory Testing Protocol
- All implementations require test verification before completion

## v5.3 (2026-02-04)

### Key Change: Session End Protocol + Auto Improvement
- Lesson classification system (universal → prompt, project → context_rule/)
- Auto improvement suggestions with user approval

## v5.2 (2026-02-02)

### Key Change: Documentation Pattern + Incremental Adoption
- Core message first, user journey-based structure
- Start minimal, expand based on feedback only

## v5.1 (2026-01-31)

### Key Change: Prerequisite Verification
- Verify key resources/conditions before starting implementation

## v5.0 (2025-01)

### Key Change: Purpose-First + Checklists
- 5 core principles (purpose, simplicity, root cause, analysis, confirmation)
- Checklist-based approach (tool selection, build system, error handling)
- REMEMBER section for quick reference

## v2.0 (2024-12)

### Key Change: Session Continuity + Knowledge Management
- SESSION.md / HANDOFF.md session logs
- common_knowledge/ / context_rule/ knowledge stores
- Context window monitoring (50%/70%/90%)

---

## Prompt File

The latest prompt is available at [examples/ai-developer-mickey.json](../examples/ai-developer-mickey.json).
