# Knowledge Management System

> [한국어 버전](05-knowledge-management.md)

## Why Is It Needed?

```
Mickey 1: Analyze Godot scene system → Understand (2 hours)
Mickey 2: (Session restart) → Re-analyze (1.5 hours)
Mickey 3: (Session restart) → Analyze again (1 hour)
→ 4.5 hours of duplicate work
```

Saving knowledge to files:

```
Mickey 1: Analyze + document (2.5 hours)
Mickey 2: Read document (10 min) → Start working immediately
Mickey 3: Read document (10 min) → Start working immediately
→ No duplication, cumulative learning
```

But as knowledge grows, new problems emerge: **"Which knowledge to load when?"** and **"How to distinguish user-written rules from AI-observed facts?"**

## 4-Store System

### Why

Putting all knowledge in one place mixes trust levels and management approaches. Separating by nature allows different review procedures and loading timing for each.

### What

| Store | Nature | Review Timing | Example |
|-------|--------|--------------|---------|
| **auto_notes/** | AI-observed facts (descriptive) | Batch at session end | Build commands, file roles, error fixes |
| **context_rule/adaptive.md** | AI self-generated rules (adaptive) | Batch at session end | "Update Korean/English simultaneously for README" |
| **context_rule/** | Verified project rules (normative) | Immediate user confirmation | Preventing repeated failures, environment constraints |
| **common_knowledge/** | Universal reusable patterns (normative) | Immediate user confirmation | Architecture patterns, technology comparisons |

### How

```
project-root/
├── auto_notes/                  # AI automatic observation records
│   ├── NOTES.md                # Index (T3a)
│   ├── commands.md             # Build/test/lint commands
│   ├── file-roles.md           # File paths and roles
│   └── error-fixes.md          # Verified error fixes
├── context_rule/                # Project-specific rules
│   ├── INDEX.md                # Rule map (T3a)
│   ├── project-context.md      # Environment/goals/constraints/lessons
│   └── adaptive.md             # AI self-generated rules (T2)
└── common_knowledge/            # Universal reusable patterns
    ├── INDEX.md                # Knowledge map (T3a)
    └── agent-design-patterns.md # Agent design patterns
```

**context_rule/ vs common_knowledge/ distinction**:
- Usable in other projects? → `common_knowledge/`
- Only meaningful in this project? → `context_rule/`

## Auto Memory: auto_notes + adaptive.md

### Why

Having to say "record this" every time is inefficient. If AI automatically records facts discovered during work while **separating them from verified rules**, trust levels can be managed.

### auto_notes/ — Observed Facts

Automatic recording targets (no user confirmation needed):
- Build/test/lint commands
- File paths and roles
- Tool versions, environment details
- Verified error fixes
- API endpoints and purposes

```markdown
# auto_notes/commands.md

## Build
- `npm run build` — Production build
- `npm run dev` — Dev server (port 3000)

## Test
- `npm test` — All tests
- `npm test -- --watch` — Watch mode
```

Size management:
- Split into category files when `NOTES.md` exceeds 50 lines
- Further subdivide topic files when they grow too large
- `NOTES.md` always maintains index role only

### adaptive.md — AI Self-Generated Rules

Behavioral rules Mickey learns on its own during work:

```markdown
# Adaptive Rules

## Rules Learned in This Project
- When modifying README, update Korean/English simultaneously
- When changing install.sh, verify 3-way sync (agent JSON, repo, ~/.kiro/)
- When changing system prompt, also update examples/ folder
```

Difference from auto_notes: auto_notes are **facts** ("build command is npm run build"), adaptive.md are **rules** ("update Korean/English simultaneously when modifying README").

At session end, changes to auto_notes and adaptive.md are **presented in batch** for user review/edit/delete.

## Lesson Promotion Path

### Why

Recurring patterns among auto_notes observations should be elevated to higher tiers. This ensures faster, more reliable reference in the next session.

### What

```
auto_notes (observations) → context_rule (project rules) → common_knowledge (universal patterns) → REMEMBER (core principles)
```

| Promotion Condition | Target |
|--------------------|--------|
| Same mistake repeated 2+ times | → context_rule/ |
| Project-independent reusable pattern discovered | → common_knowledge/ |
| Fundamental principle-level lesson | → REMEMBER (system prompt) |

### How

When user requests "promote lessons" or "organize patterns":

1. Review auto_notes/, SESSION.md Lessons, HANDOFF.md
2. Classify per item: context_rule / common_knowledge / REMEMBER candidate
3. Propose promotion (content, rationale, target) → User confirmation
4. Apply on approval + mark "promoted" in auto_notes

**Practical example**: In Mickey 9, 14 lessons from MICKEY-1~5 were analyzed and 3 were promoted to `common_knowledge/agent-design-patterns.md`.

## Document Writing Principles

### Conciseness

```
❌ "Godot engine is an open-source game engine. First released in 2014..." (500 words)
✅ "## Godot Engine
    - Open source (MIT), scene-node structure, GDScript (Python-like)"
```

### Structure

```
Overview → Core Concepts → Usage Examples → Detailed Reference
```

### Cross-References

```markdown
**Related docs**: [Node System](node-system.md), [Signal System](signal-system.md)
```

## Practical Examples

### Godot Engine Analysis (13,666 files)

1. `common_knowledge/godot/overview.md` — Engine structure overview (Context 5%)
2. Register triggers in INDEX — Selectively load only needed topics
3. Knowledge accumulates across sessions → Analysis time from 2 hours → 10 minutes

**Insight**: "Don't re-analyze what you've already analyzed."

### Mickey Self-Improvement (Lesson Promotion)

```
Mickey 1~5: Accumulate observed facts in auto_notes
Mickey 9: Analyze 14 items → Promote 3 to common_knowledge
  - Script delegation pattern
  - Event-based triggers
  - Plan specificity → execution speed correlation
```

**Insight**: "Observation → Pattern discovery → Rule formation → Principle formation. Knowledge climbs tiers."

## Best Practices

### DO ✅

1. **Write INDEX first**: Provide entry point to knowledge
2. **Keep it concise**: Core only, include example code
3. **Separate by nature**: Facts (auto_notes) / Rules (context_rule) / Patterns (common_knowledge)
4. **Regular promotion**: Recurring patterns to higher tiers

### DON'T ❌

1. **Everything in one file**: Wastes context window, hard to search
2. **Add files without INDEX**: Creates orphan files that never get loaded
3. **Delay promotion**: auto_notes bloats and patterns get buried
4. **Mix facts and rules**: Makes trust management impossible

## Next Steps

- [Prompt Evolution](06-prompt-evolution-en.md) - v2.0 → v7.2 evolution
- [Evolution Insights](08-evolution-insight-en.md) - How "using AI well" has evolved
- [Case Study](case-study/godot-replay-system.md) - Godot project case study
