# Knowledge Graph + Code Analysis Tool Integration — Expectations vs. Measured Results

> [한국어 버전](10-knowledge-graph-and-tools.md)

Mickey builds a "gets smarter as sessions accumulate" structure on two axes:

1. **Personalized knowledge graph** (`~/.kiro/mickey/domain/`) — domain knowledge reused across projects
2. **Code analysis tool integration** (v9.2, §19) — delegating detailed analysis to Serena / Graphify / Kiro CLI built-in `code`

This document summarizes, for each axis, **what we expected and what actually happened**, with measured data and cases. We did not cherry-pick successes — the failure cases are precisely where the design changed.

---

## 1. Knowledge Graph: Expected Effects

| # | Expectation | Design basis |
|---|-------------|--------------|
| E1 | Never repeat the same judgment/mistake **across projects** | Session lessons → Curator routing → global promotion |
| E2 | Knowledge is **discovered without searching** (Passive) | INDEX triggers + GRAPH backlinks + "when" hints |
| E3 | Minimal session startup cost | Load only the knowledge map (INDEX); bodies on demand |
| E4 | Knowledge **self-reinforces** | Promotion loop + graph integrity verification |

## 2. Knowledge Graph: Measured Results

### Scale and health (2026-09-05, measured by graph_audit.py)

- **175 nodes / 515 edges** (top-level graph 148+488, cloud subgraph 27+27), 173 entry files
- Integrity: **0 dangling edges, 0 missing paths** — maintained by the promotion script's integrity verification / auto-rollback
- Average degree 5.89 — new knowledge is added connected to existing knowledge, not isolated
- Top hub: `deploy-output-distrust` (degree 59) — "distrust a tool's success output; cross-verify with external signals" became the central principle cutting across all domains
- Growth: 131 nodes as of 2026-08-25 → 175 nodes about a month later (one developer, ~10 concurrent projects)
- Usage baseline (measured over 5 weeks / 31 sessions): **2.45 global knowledge references per session**, 2.65 Curator invocations per session

### Positive cases

**Case 1 — The cp949 trilogy: progressive sealing of a recurring failure.**
Encoding failures on Windows cp949 consoles recurred three times in different forms: ① Python UnicodeEncodeError (M22) → ② truncated Korean console output (M39) → ③ PowerShell `>` redirection destroying utf-8 output into mojibake (M48). Each occurrence was captured as a project rule (adaptive #8 → #14 → #19), and on the third occurrence it was promoted to a global entry (`windows-cp949-artifact-ascii-defense`) with a catalog of all four manifestation points. From then on, any project that touches the "redirection" or "mojibake" triggers discovers this knowledge. **The recurrence surface of the same failure family narrows with each manifestation** — a demonstration of E1.

**Case 2 — The Serena latent-incident diagnosis chain: knowledge accelerating diagnosis.**
A `--project` argument hardcoded in an agent JSON silently mis-set every session's active Serena project to an ancestor directory for seven weeks (see §4 below). The diagnosis itself was aided by the graph: the inherited hypothesis ("relative path resolution issue") was rejected by **measuring the live process command line**, pinpointing the real cause (configuration-layer override) — a direct application of `mechanism-level-cause-attribution` ("re-verify remembered failure causes at the mechanism level before citing") and `prompt-doc-vs-runtime-loading` ("confirm effective config by measuring the running process"), both promoted from earlier incidents. The resolution flowed back into the graph as the `tool-implicit-root-path-trap` entry and the §19.3 convention.

**Case 3 — Verified patterns propagating to all projects.**
`batch-confirm-autonomous-proceed` (interpret a short user reply as batch adoption and proceed autonomously) was promoted to patterns/ after 11+ applications with zero failures measured in one project, and now reduces confirmation friction everywhere. `safe-batch-replace` (count-guarded batch replacement) has been verified across 10 generations of reuse.

**Case 4 — Diversity of origin in protocol evolution.**
The last nine versions (v20–v28) of the T1.5 protocol (extended-protocols.md) each originated from a different project: a graph-analysis project (example-list misreading), game QA automation (symbol-context pairing), a modernization project (rerun-as-diagnostic), and Mickey itself (multi-session isolation, the Serena convention). Evidence that **the graph actually functions as a cross-project learning conduit**.

### Negative cases — and how they changed the design

**Case 5 — Knowledge that was only accumulated: 0% usage (M20 postmortem).**
After building the v8.1 knowledge structure and running 76 sessions, grep-based measurement showed **0% usage of global knowledge**. The cause was discovery design, not storage: the "search when needed" (Active) instruction was simply never executed. Redesigning for Passive discovery (INDEX trigger matching + backlinks + "when" hints) recovered the baseline to 2.45 references per session. The failure itself was promoted as `quantitative-usage-measurement` ("0% = design defect") and `passive-over-active-retrieval`. **Accumulating knowledge and having knowledge used are entirely different problems.**

**Case 6 — "Mid-session automatic invocation" failed twice → forced breakpoints.**
Designing knowledge curation to be "invoked by the AI at the right moment" failed twice in a row (the invocation never happened). Delegating timing judgment to an LLM does not work — placement at a natural forced breakpoint, such as session end, is what guarantees execution (`forced-breakpoint-execution`).

**Case 7 — The graph does not stay healthy on its own.**
A full audit (M44) found one orphan node that had been handed off as "to be reflected at the next Curator run" — and left **neglected for two months**. Handoffs without an executing agent get abandoned. That measurement led to making `graph_audit.py` (automated integrity/cleanup-candidate auditing) a standing tool and freezing a baseline. Today's "0 dangling" is a state maintained by tools + breakpoints, not a natural state.

**Case 8 — Multi-session concurrent writes → revoking write access from the LLM.**
Parallel Mickey sessions writing to the global graph concurrently would collide. The fix was structural, not prompt-based: the Curator writes only to project-local staging, and global reflection became the exclusive right of a lock-holding deterministic script (`promote_knowledge.py`) (`staged-promotion-write-isolation`). **"LLM decides, code enforces"** is the core of multi-session safety.

---

## 3. Code Analysis Tool Integration: Expected Effects

v9.2 integrated external code analysis tools in three tiers (Tier 1: Serena/Graphify, Tier 2: user-selected, Tier 3: Kiro CLI built-in `code` = baseline).

| # | Expectation | Design basis |
|---|-------------|--------------|
| T1 | **Remove detailed-analysis burden** from Mickey docs | Shrink FILE-STRUCTURE to a first-step map; delegate detail to tools |
| T2 | Save context window | Query code relations on demand instead of embalming them in docs |
| T3 | Gain precision | LSP (references/definition/diagnostics) + symbol search + architecture graphs |
| T4 | Eliminate the "no tool" case | Built-in `code` always exists as baseline |

## 4. Code Analysis Tool Integration: Measured Results

### Positive cases

**Case 9 — The documentation diet actually lowered maintenance cost.**
After FILE-STRUCTURE.md shrank from a "code-relations encyclopedia" to a depth-2 tree + doc locations + tool detection results, staleness cycles lengthened and update cost dropped sharply. In brownfield onboarding, the structure-analysis document is replaced by 2–3 lines of tool references (`structure-ref.md`). Demonstrates T1/T2.

**Case 10 — The detection rules themselves evolved through measurement.**
In one benchmark project, the absence of a local marker (`.serena/`) was nearly misjudged as "tool absent," falling back to baseline — when in fact Serena was exposed in the MCP tool list and immediately usable. That gap was sealed as §19.2 clause 5 ("no marker ≠ no tool"). Tool-integration conventions grow through measured failures, just like the knowledge graph.

**Case 11 — Operating this repository itself.**
The Mickey repository holds ~30 Python scripts and ~300 documents; symbol navigation and structure discovery are delegated to Serena and built-in `code` (pyright LSP) while Mickey docs keep only the map. The session that produced this document also ran on the Serena `activate_project` → measure → update-docs flow.

### Negative cases — the cost of tool integration

**Case 12 — Serena `--project` hardcoding: a fail-wrong incident latent for seven weeks.**
The biggest incident since tool integration. A `--project` launch argument hardcoded in an agent JSON overrode the global MCP configuration wholesale, so that **for a month and a half, every session's Serena mis-set its active project to an ancestor directory**. File writes landed in the wrong place and another project's session files were lost. Operating wrongly in silence (fail-wrong) is far more dangerous than raising errors (fail-closed) — the resolution was to abolish the launch argument, mandate `activate_project` at session start, and forbid writes before activation is confirmed (§19.3), concluded by multi-session parallel verification (24 processes' command lines, activation logs, misplacement signatures). **Lesson: attaching a tool also attaches a new failure surface made of configuration layers and implicit state.**

**Case 13 — Limits of executing through a tool.**
Serena's `execute_shell_command` has a 240-second timeout and cannot carry the 6+ minute headless Curator run (caller-side truncation was measured). Long-running work is now routed around the tool to a direct execution layer. A tool's strength zone (symbol/structure analysis) and limit zone (long-running execution) must be separated by measurement.

---

## 5. Summary: Results Against Expectations

| Expectation | Verdict | Measured evidence |
|-------------|---------|-------------------|
| E1 Prevent repetition | **Valid** | cp949 trilogy sealed; T1.5 v20–v28 all originated in other projects |
| E2 Passive discovery | **Valid (after redesign)** | M20 0% usage → Passive redesign → 2.45/session |
| E3 Minimal startup cost | Valid | INDEX map loading + on-demand bodies (3-tier loading) |
| E4 Self-reinforcement | **Valid (conditional on tools+breakpoints)** | 0/0 integrity — maintained by graph_audit + locks + forced breakpoints |
| T1/T2 Documentation diet | Valid | FILE-STRUCTURE shrunk; structure-ref in 2–3 lines |
| T3 Precision analysis | Valid | Serena symbols + LSP diagnostics in daily use |
| T4 Baseline guaranteed | Valid | Built-in `code` always on; "no marker" gap sealed |

Three conclusions run through everything.

1. **The biggest value was not "knowledge reuse" but "structural sealing of failures."** The same failure escalates from project rule → global entry → code (locks/scripts/conventions), physically shrinking the recurrence surface itself.
2. **Nothing is automatic.** Knowledge usage, graph health, tool configuration — every spot left to "it will take care of itself" produced a measured failure (0% usage, a two-month orphan, a seven-week latent incident), and recovered only through measurement + forced breakpoints + tooling.
3. **The LLM decides; code enforces.** Promotion integrity is guaranteed by a script, concurrency by locks, invocation procedure by a single entry point. No convention survived on prompt instructions alone.

---

## Related Documents

- [Knowledge Management System](05-knowledge-management-en.md) — 3-tier loading and repository structure
- [Evolution Insight](08-evolution-insight-en.md) — shifts of perspective in protocol evolution
- Graph health check method: `GRAPH-HEALTH-BASELINE-2026-08-25.md` at the repository root
- Usage measurement: T1.5 §18 Activity Metrics (baseline methodology)

## Last Updated
2026-09-06 (Mickey 49 — newly written. Graph measurements as of 2026-09-05)
