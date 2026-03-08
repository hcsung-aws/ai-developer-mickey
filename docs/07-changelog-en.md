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
