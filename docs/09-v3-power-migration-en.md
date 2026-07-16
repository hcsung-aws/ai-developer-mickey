# v10: From CLI Agent to Kiro v3 Power

> [한국어 버전](09-v3-power-migration.md)

> The narrative and design decisions behind migrating Mickey from a CLI v2 agent (JSON prompt) to the Kiro v3 Power format.

## Why migrate

Mickey originally ran as a single Kiro CLI agent JSON (`examples/ai-developer-mickey.json`) holding a prompt evolved through v17. Simple, but with two limits:

- **Always-on load**: The full ~278-line prompt sits in context every session. A large chunk of the context window is consumed the moment a session starts.
- **No IDE integration**: Kiro IDE users cannot use a CLI agent. They need the Power format (steering + POWER.md).

The v3 Power solves both. By treating steering as an **entry point** and pulling detailed knowledge **only when needed** (progressive disclosure), we cut the initial consumption while running on both CLI and IDE.

## Core design principle: separating entry points from graph nodes

The most important decision was **"what goes into steering, and what stays in the original files."**

| Layer | Ported? | Rationale |
|-------|---------|-----------|
| **T1** (v17 prompt skeleton, 278 lines) | Split into 6 steering files | The always-needed backbone for every session |
| **T1.5** (`extended-protocols.md` §1~§19) | Not ported, kept original | Situational deep protocols. Steering only names triggers; pull the specific §N when needed |
| **Knowledge-graph nodes** (`domain/entries/*`, `patterns/*`) | Not ported, kept original | INDEX/GRAPH/PROFILE access contract already exists. Steering only names the access path |
| **Curator canonical** (`CURATOR-PROMPT.md`) | Not ported, kept original | `knowledge-curator.md` only summarizes the invocation contract |

This keeps each steering file a thin ≤200-line entry point, and lets T1.5 and graph knowledge evolve per session without redeploying steering. **The evolution loop and the deployment lifecycle are decoupled.**

## v2 vs v3 structure

| Item | CLI v2 (agent JSON) | Kiro v3 Power |
|------|--------------------|---------------|
| Prompt format | Single JSON `prompt` field | `POWER.md` + `steering/*.md` |
| Loading | Fully resident | 6 always steering + 1 on-demand + graph-node pull |
| Knowledge graph | memorygraph MCP (early) / file-based | File-based (`~/.kiro/mickey/`) |
| Session management | Manual / hook | CLI v3 hooks (`SessionStart`/`Stop`) + scripts |
| MCP | Per-agent | `mcp.json` (aws-knowledge only; Serena/Graphify reused globally) |
| Usage | `kiro-cli chat --agent ai-developer-mickey` | `kiro-cli chat` (power-mickey auto-detected) / Kiro IDE |

Both paths are **kept in parallel**. v2-engine users keep the agent JSON; v3 users use the Power.

## Steering layout (6 always + 1 on-demand)

**Always loaded (`inclusion: always`)**

| Steering | Role |
|----------|------|
| `mickey-core.md` | Core Identity + REMEMBER 12 + Anti-Patterns |
| `session-protocol.md` | First/Continuing/During/End Session + graph triggers |
| `knowledge-graph.md` | Knowledge-graph access contract + 3-Tier loading |
| `problem-solving.md` | 10-step skeleton + deep-protocol triggers |
| `document-schema.md` | Required schemas for 10 document types |
| `context-window.md` | 50/70/90 management rules |

**On-demand (`inclusion: manual`)**

| Steering | When pulled |
|----------|-------------|
| `knowledge-curator.md` | Pulled via `readSteering` only at session close. Not pulled otherwise |

The reason Curator rules are not always loaded is clear: keeping a session-close-only contract resident every session violates progressive disclosure.

## Phase-by-phase progress

- **Phase 0~2**: Retire the old experimental power (Kiro IDE 0.7 era), rebuild the skeleton. Split v17 into 6 steering files. 100% traceability via the port matrix (`docs/v2-to-v3-mapping.md`).
- **Phase 3**: Session hooks/scripts. The 2 CLI v3 hooks stay thin; logic is isolated into `mickey_session_boot.py`/`mickey_session_close.py`. IDE `.kiro.hook` deferred as skeleton until spec is measured.
- **Phase 4-A**: Absorb Knowledge Curator logic into `knowledge-curator.md` (manual). The canonical procedure stays original and is pulled. Removed triple-duplication of the invocation contract.
- **Phase 5**: install-script overhaul + documentation update.

## Deployment pipeline (Phase 5)

To place the v3 Power in the user's home, we first had to learn what kiro-cli actually reads. Measurement showed kiro-cli serves the **physical copy in `~/.kiro/powers/installed/power-mickey/`**. The registry source path is merely provenance metadata.

That fact drove the deployment design. `scripts/deploy_power.py` owns the core logic as single responsibilities:

1. **Version gate** — parse `kiro-cli --version`; deploy v3 only at 2.10+. If below/unparseable, skip v3 and exit cleanly (v2 preserved).
2. **Backup** — archive the existing install as `power-mickey.bak-<timestamp>.zip`.
3. **clean-replace** — replace the whole directory (rmtree + copytree). This was essential: measurement found stale pre-v10 steering (memory-protocol, self-improvement) in the home, and a plain overwrite would leave those orphans, causing kiro to load the wrong steering.
4. **installed.json guarantee** — add the entry if missing, no-op if present (idempotent).

`install.ps1`/`install.sh` keep the existing v2 deploy (agents JSON + `~/.kiro/mickey` library) and merely add the `deploy_power.py` call. **v2 always, v3 conditionally.**

## Why memorygraph was removed

The early experimental power managed long-term memory via the memorygraph MCP. v10 removes it and unifies on a file-based knowledge graph (INDEX/GRAPH/PROFILE/entries under `~/.kiro/mickey/`).

- No MCP dependency, so install and portability get simpler.
- Knowledge stays as markdown, enabling git version control and review.
- Frees us from runtime constraints like memorygraph's Windows hang bug (project parameter required).

## Verification

A test harness stands as the regression line.

- `verify_power_structure.py` **7/7** — steering presence · front matter · POWER mapping · T1 traceability · triggers · P3 both-branch · inclusion modes
- `verify_hooks.py` **6/6** — session hooks/scripts
- `verify_deploy_power.py` **25/25** — version parsing · gate · dry-run no-change · orphan removal · idempotent · gate-miss skip (uses a temp home, leaving the real home untouched)

## Lessons

- **Verify instead of assume**: We confirmed the registry-vs-installed consumption model by actually activating the power, which revealed the need for clean-replace.
- **Separating entry point from source** is the heart of progressive disclosure. Resisting the urge to stuff everything into steering was the essence of v10.
- **Test harness first**: Logic that mutates home assets was defended with a temp-directory harness before running against the real home (Working Effectively with Legacy Code).

## References

- Plan: [`IMPROVEMENT-PLAN-v10-power-migration.md`](../IMPROVEMENT-PLAN-v10-power-migration.md)
- Port matrix: [`docs/v2-to-v3-mapping.md`](v2-to-v3-mapping.md)
- Changelog: [Changelog](07-changelog-en.md)
- Session logs: `session_history/2026-07-04~13-mickey-v10-migration-*.md`
