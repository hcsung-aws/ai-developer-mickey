# AI Developer Mickey

> [한국어 버전](README.md)

> A practical guide for effectively utilizing generative AI assistants

![Mickey](docs/images/mickey-poster.png)

## 📖 Project Overview

**AI Developer Mickey** is an educational project that documents key patterns and strategies discovered while using a generative AI assistant (Kiro) to execute complex software development projects.

Currently, Mickey is also used to **improve the Mickey agent itself**, and the lessons and knowledge accumulated through this process are structured in `context_rule/` and `common_knowledge/`, automatically reflected in subsequent sessions.

### Problems We Aimed to Solve

1. **Context Window Limitations**: Failures due to context window limits during complex issue analysis
2. **Loss of Session Consistency**: Loss of previous context when restarting sessions, leading to failures
3. **Lack of Knowledge Management**: Inability to effectively reuse accumulated knowledge and experience

### Core Idea

Create an AI developer agent called **"Mickey"** that saves success/failure records from each session to files, references them in subsequent sessions, and continuously improves.

### 🔄 Prompt Evolution

The Mickey prompt continues to evolve through real projects:

| Version | Project | Sessions | Key Changes |
|---------|---------|----------|-------------|
| **v2.0** | Godot Replay System | Mickey 1-6 | Session continuity, knowledge management |
| **v5.0** | Packet Capture Agent | Mickey 1-12 | Purpose-first, checklists, automation |
| **v6.1** | Mickey Self-Improvement | Mickey 13 | T3 layering, INDEX map pattern, Power steering evolution |
| **v6.2** | Mickey Self-Improvement | Mickey 14 | PURPOSE-SCENARIO based purpose management system |
| **v6.3** | Mickey Self-Improvement | Mickey 4 | Auto Memory pattern (auto_notes/ + knowledge promotion) |
| **v7** | Mickey Self-Improvement | Mickey 7-8 | Autonomous execution + Subagent + Brownfield onboarding |
| **v7.2** | Mickey Self-Improvement | Mickey 9 | Adaptive Rules (self-improvement) + Autonomy Preference |
| **v7.4** | Mickey Self-Improvement | Mickey 11-12 | REMEMBER retirement management (15→12) + Power Mickey full sync |
| **v8** | Mickey Self-Improvement | Mickey 12 | 🆕 Global Knowledge (patterns/ + domain/) + Session-PURPOSE connection + Postmortem auto-trigger |
| **v8.1** | Mickey Self-Improvement | Mickey 14-15 | 🆕 Knowledge Curator subagent + domain/ activation (PROFILE/GRAPH/entries) + Personal Vault → domain/ transition |
| **v9 (PLAN)** | Mickey Self-Improvement | Mickey 20 | 🆕 3-Tier (R/G/S) + Domain-centric global knowledge + knowledge-organization Skill — POSTMORTEM-based redesign (Phase 1~5, implementation from next session) |
| **v9.1** | Mickey Self-Improvement | Mickey 21-22 | 🆕 v9 PLAN correction+landing: Curator permission fix + Pre-staged Apply + T1.5 §17 Knowledge Lifecycle + §18 Activity Metrics — 5-week 31-session measurement invalidated v9 PLAN's "retire Curator" decision |
| **v10 (Power Migration)** | Mickey Self-Improvement | v10 track | 🆕 CLI v2 agent → Kiro v3 Power migration: 7 steering (6 always + 1 on-demand) + session hooks/scripts + memorygraph removed (file-based knowledge graph) + install-script v3 deploy pipeline |

> 💡 **Key Insight**: AI prompts should not be "write once and done" but **continuously evolved through failure experiences**. See [Prompt Evolution Guide](docs/06-prompt-evolution-en.md) for details.

## 🎯 Learning Objectives

Through this project, you will learn:

- ✅ **Context Window Management**: How to efficiently utilize limited context
- ✅ **Context Abstraction**: Techniques to structure information and load only what's needed
- ✅ **Session Continuity**: Strategies to maintain work across sessions
- ✅ **Prompt Structuring**: Effective prompt design and improvement methods
- ✅ **Knowledge Management System**: Storing and utilizing reusable knowledge
- ✅ **Prompt Evolution**: Continuous prompt improvement through failure experiences 🆕

## 📚 Documentation Structure

### Core Guides (v2.0)

1. [Introduction to Mickey](docs/01-introduction-en.md) - Concept and design of the Mickey agent
   - [한글](docs/01-introduction.md)
2. [Context Window Management](docs/02-context-management-en.md) - Strategies for efficient context utilization
   - [한글](docs/02-context-management.md)
3. [Session Continuity](docs/03-session-continuity-en.md) - Methods to maintain consistency across sessions
   - [한글](docs/03-session-continuity.md)
4. [Prompt Engineering](docs/04-prompt-engineering-en.md) - Effective prompt structuring
   - [한글](docs/04-prompt-engineering.md)
5. [Knowledge Management System](docs/05-knowledge-management-en.md) - Building reusable knowledge
   - [한글](docs/05-knowledge-management.md)

### Prompt Evolution Guide (v5.0) 🆕

6. **[Prompt Evolution: v2.0 → v5.0](docs/06-prompt-evolution-en.md)** - Lessons from the second project ⭐
   - [한글](docs/06-prompt-evolution.md)

### v3 Power Migration (v10) 🆕

- **[v10: From CLI Agent to Kiro v3 Power](docs/09-v3-power-migration-en.md)** - Migration narrative and design decisions
  - [한글](docs/09-v3-power-migration.md)

### AI Perspective

- [Mickey from AI's Perspective](docs/ai-perspective-en.md) - AI's postmortem and practical guide
  - [한글](docs/ai-perspective.md)

### Case Studies

| Project | Version | Status | Documentation |
|---------|---------|--------|---------------|
| Godot Replay System | v2.0 | Complete | [English](docs/case-study/godot-replay-system-en.md) / [한글](docs/case-study/godot-replay-system.md) |
| Packet Capture Agent | v5.0 | In Progress | [English](docs/case-study/packet-capture-agent-en.md) / [한글](docs/case-study/packet-capture-agent.md) 🆕 |

### Session Logs

- [Godot Project Sessions](sessions/) - Mickey 1~6
- [Packet Capture Project Sessions](sessions/packet-capture/) - Mickey 1~12 🆕

## 🚀 Quick Start

### 1. Installation

```bash
# After installing Kiro CLI (https://github.com/aws/kiro-cli)
git clone https://github.com/hcsung-aws/ai-developer-mickey.git
cd ai-developer-mickey
```

**macOS / Linux / WSL:**
```bash
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

What `install.sh` / `install.ps1` does:
- Agent JSON → `~/.kiro/agents/` (CLI v2)
- Global guide → `~/.kiro/mickey/`
- v3 Power → `~/.kiro/powers/installed/power-mickey/` (when kiro-cli is 2.10+; skipped automatically below that)

> The v3 deploy is handled by `scripts/deploy_power.py`, which backs up the existing install before replacing it. Run `python scripts/deploy_power.py --dry-run` to preview without changes.

### 2. Running Mickey in a Project

There are three ways to use Mickey:

| Scenario | How to run | Notes |
|----------|-----------|-------|
| **CLI v2** | `kiro-cli chat --agent ai-developer-mickey` | Uses the v17 prompt (agent JSON) directly. The verified, stable path |
| **CLI v3** | `kiro-cli chat` | power-mickey is auto-detected. Loads 6 always + 1 on-demand steering (kiro-cli 2.10+) |
| **Kiro IDE** | Activate power-mickey in the Powers panel | Same steering, in the IDE |

```bash
cd <project directory>
kiro-cli chat --agent ai-developer-mickey   # CLI v2
```

### What Mickey Automatically Does

- Project analysis and document generation
- Session log creation (MICKEY-N-SESSION.md)
- Lesson recording and next session handoff

### Directory Structure

```
ai-developer-mickey/
├── docs/                    # Core guide documents
├── sessions/               # Mickey session log examples
├── examples/               # Configuration files and examples
│   ├── ai-developer-mickey.json  # Latest prompt
│   ├── knowledge-curator.json    # Knowledge Curator subagent
│   ├── common_knowledge/   # Knowledge management examples
│   └── context_rule/       # Context rule examples
├── context_rule/           # This project's context rules (used by Mickey for self-improvement)
├── common_knowledge/       # This project's common knowledge
├── power-mickey/           # Kiro v3 Power (v10 — CLI v3 + IDE)
└── godot-pong/            # Godot replay system code
```

## ⚡ Kiro v3 Power (v10)

Mickey is also available as a Kiro v3 Power (the v10 migration). Steering files act as entry points and detailed knowledge is pulled only when needed (progressive disclosure), so it **works identically on CLI v3 and Kiro IDE**. See [v3 Power Migration](docs/09-v3-power-migration-en.md) for the full narrative and design decisions.

### Installation

The `install.sh` / `install.ps1` above deploys it automatically when kiro-cli is 2.10+ (`~/.kiro/powers/installed/power-mickey/`).

**Kiro IDE local installation:**
```bash
git clone https://github.com/hcsung-aws/ai-developer-mickey.git
# Kiro IDE → Powers panel → Add power from Local Path → Select power-mickey folder
```

### Power Structure

```
power-mickey/
├── POWER.md              # Onboarding instructions + steering mapping + activation triggers
├── mcp.json              # aws-knowledge-mcp-server (memorygraph removed in v10)
└── steering/             # 6 always + 1 on-demand
    ├── mickey-core.md          # Core Identity + REMEMBER 12
    ├── session-protocol.md     # 4-stage session protocol
    ├── knowledge-graph.md      # Knowledge-graph access contract
    ├── problem-solving.md      # 10-step problem solving
    ├── document-schema.md      # Document schemas
    ├── context-window.md       # Context window management
    └── knowledge-curator.md    # (manual) pulled only at session close
```

### CLI v2 vs v3 Power Comparison

| Item | Kiro CLI v2 (agent JSON) | Kiro v3 Power |
|------|--------------------------|---------------|
| Prompt loading | Full v17 resident | 6 always + 1 on-demand steering + graph-node pull |
| Knowledge graph | File-based (`~/.kiro/mickey/`) | Same (memorygraph MCP removed) |
| Session management | Manual | CLI v3 hooks (`SessionStart`/`Stop`) + scripts |
| Environment | CLI | CLI v3 + Kiro IDE |

## 💡 Key Insights

### 1. GenAI is a 'Combination of Past Experiences'

- **Clear context** is essential for handling completely new requirements
- **One clear instruction** is more effective than a hundred guardrails
- GenAI operates by connecting experience 'modules'

### 2. The Efficiency Trap

- Taking the simple path happens because it's 'most efficient'
- **Properly understanding context and giving instructions** minimizes side effects
- **Step-by-step testing and verification** is essential

### 3. AI as a Feedback Tool

- Use AI as a **'feedback tool'**, not a magic wand
- Resulting learning and judgment are performed by **humans**
- Continuous improvement is possible through **iterative feedback**

## 📊 Project Achievements

### Godot Replay System Development

Using Mickey, we built a complete replay and regression testing system for Godot Engine's Pong game:

- ✅ **Phase 1**: Achieved 100% pass rate (Ball reset detection)
- ✅ **Phase 2**: User guide and CI/CD integration documentation
- ✅ **Phase 3**: Multi-log batch testing infrastructure
- ✅ **Phase 3-1**: AI-based automatic scenario generation system

**Key Features:**
- Game play recording and replay
- Frame-by-frame state validation (Position, Velocity, Direction)
- Automatic bug report generation
- Headless mode batch testing
- 6 automatic scenario generation (by AI difficulty)

## 🔗 Related Links

- [Kiro CLI](https://github.com/aws/kiro-cli) - AWS's generative AI assistant
- [Godot Engine](https://godotengine.org/) - Open-source game engine
- [Packet Capture Agent](https://github.com/hcsung-aws/packet-capture-log-agent) - Second project 🆕
- [Original Notion Document](https://www.notion.so/vaneddie/Demo-AI-Developer-Mickey-Godot-2bcd0b7b36dd807f8487fd8cab537935)

## 📝 License

MIT License

## 🤝 Contributing

Issues and PRs are welcome! Please share your generative AI usage experiences.

---

**Made with ❤️ by Mickey (AI Developer Agent powered by Kiro CLI)**
