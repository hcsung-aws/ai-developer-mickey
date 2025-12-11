# AI Developer Mickey

> [한국어 버전](README.md)

> A practical guide for effectively utilizing generative AI assistants

![Mickey](docs/images/mickey-poster.png)

## 📖 Project Overview

**AI Developer Mickey** is an educational project that documents key patterns and strategies discovered while using a generative AI assistant (Kiro CLI) to execute complex software development projects.

### Problems We Aimed to Solve

1. **Context Window Limitations**: Failures due to context window limits during complex issue analysis
2. **Loss of Session Consistency**: Loss of previous context when restarting sessions, leading to failures
3. **Lack of Knowledge Management**: Inability to effectively reuse accumulated knowledge and experience

### Core Idea

Create an AI developer agent called **"Mickey"** that saves success/failure records from each session to files, references them in subsequent sessions, and continuously improves.

## 🎯 Learning Objectives

Through this project, you will learn:

- ✅ **Context Window Management**: How to efficiently utilize limited context
- ✅ **Context Abstraction**: Techniques to structure information and load only what's needed
- ✅ **Session Continuity**: Strategies to maintain work across sessions
- ✅ **Prompt Structuring**: Effective prompt design and improvement methods
- ✅ **Knowledge Management System**: Storing and utilizing reusable knowledge

## 📚 Documentation Structure

### Core Guides

1. [Introduction to Mickey](docs/01-introduction-en.md) - Concept and design of the Mickey agent
2. [Context Window Management](docs/02-context-management-en.md) - Strategies for efficient context utilization
3. [Session Continuity](docs/03-session-continuity-en.md) - Methods to maintain consistency across sessions
4. [Prompt Engineering](docs/04-prompt-engineering-en.md) - Effective prompt structuring
5. [Knowledge Management System](docs/05-knowledge-management-en.md) - Building reusable knowledge
6. **[Mickey from AI's Perspective](docs/ai-perspective-en.md)** - AI's postmortem and practical guide ⭐
   - [한국어 버전](docs/ai-perspective.md)

### Real-World Case Studies

- [Godot Replay System Development](docs/case-study/godot-replay-system-en.md) - Actual project application case
- [Mickey Session Logs](sessions/) - Actual work records from Mickey 1~6

## 🚀 Quick Start

### Mickey Agent Setup

```json
{
  "name": "ai-developer-mickey",
  "description": "An AI developer that maintains session continuity and continuously improves",
  "prompt": "You are an AI developer agent 'Mickey'..."
}
```

For detailed setup, refer to [Introduction to Mickey](docs/01-introduction-en.md).

### Directory Structure

```
ai-developer-mickey/
├── docs/                    # Core guide documents
│   ├── 01-introduction.md
│   ├── 02-context-management.md
│   ├── 03-session-continuity.md
│   ├── 04-prompt-engineering.md
│   ├── 05-knowledge-management.md
│   └── case-study/         # Real-world case studies
├── sessions/               # Mickey session logs
│   ├── session_log.txt     # Mickey 1
│   ├── MICKEY-2-SESSION.md
│   ├── MICKEY-3-SESSION.md
│   ├── MICKEY-4-SESSION.md
│   ├── MICKEY-5-SESSION.md
│   └── MICKEY-6-SESSION.md
├── examples/               # Code examples
│   ├── common_knowledge/   # Knowledge management examples
│   └── context_rule/       # Context rule examples
└── godot-pong/            # Godot replay system code
```

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
- [Original Notion Document](https://www.notion.so/vaneddie/Demo-AI-Developer-Mickey-Godot-2bcd0b7b36dd807f8487fd8cab537935)

## 📝 License

MIT License

## 🤝 Contributing

Issues and PRs are welcome! Please share your generative AI usage experiences.

---

**Made with ❤️ by Mickey (AI Developer Agent powered by Kiro CLI)**
