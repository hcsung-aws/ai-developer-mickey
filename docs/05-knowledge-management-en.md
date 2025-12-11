# Knowledge Management System

> [한국어 버전](05-knowledge-management.md)

## Why Is It Needed?

Complex projects require systematic management of **reusable knowledge**.

### Problem Situation

```
Mickey 1: Analyze Godot scene system → Understand
Mickey 2: (Session restart) → Need to analyze again
Mickey 3: (Session restart) → Analyze again...
```

### Solution

```
Mickey 1: Analyze Godot scene system → Save to common_knowledge/godot/scene-system.md
Mickey 2: Read scene-system.md → Immediate understanding
Mickey 3: Read scene-system.md → Immediate understanding
```

## Directory Structure

```
project-root/
├── common_knowledge/          # Reusable knowledge
│   ├── INDEX.md              # Knowledge index (required)
│   ├── godot/
│   │   ├── overview.md       # Godot overview
│   │   ├── scene-system.md   # Scene system
│   │   └── input-system.md   # Input system
│   └── testing/
│       ├── overview.md       # Testing overview
│       └── replay-system.md  # Replay system
└── context_rule/             # Project-specific rules
    ├── project-context.md    # Environment settings
    ├── troubleshooting.md    # Troubleshooting
    └── mickey-improvements.md # Improvements
```

## common_knowledge vs context_rule

### common_knowledge/

**Purpose**: Reusable general knowledge

**Characteristics**:
- Project-independent
- Usable in other projects
- Technical/conceptual explanations

**Example**:
```markdown
# common_knowledge/godot/scene-system.md

## Godot Scene System

### Core Concepts
- Scene = Node Tree
- Parent-Child Hierarchy
- Signal-based Communication

### Example
```gdscript
# Create node hierarchy
var root = Node2D.new()
var child = Sprite2D.new()
root.add_child(child)
```
```

### context_rule/

**Purpose**: Project-specific rules and constraints

**Characteristics**:
- Project-specific
- Environment configuration information
- Known issues and solutions

**Example**:
```markdown
# context_rule/project-context.md

## Development Environment
- OS: Windows + WSL
- Godot: Runs on Windows
- Development: Performed in WSL
- **Important**: File synchronization required

## File Locations
- Windows: C:\Users\hcsung\work\q\ai-developer-mickey\pong\
- WSL: /home/hcsung/ai-develop-by-mickey/godot-demo-projects/2d/pong/

## Known Issues
- ❌ C++ engine modification: 19x workload
- ✅ GDScript: Simple and sufficient
```

## INDEX.md Pattern

### Purpose

- Entry point for all knowledge
- Minimal context window usage
- Selective loading of needed documents

### Structure

```markdown
# Knowledge Index

## Quick Links
- [Godot Overview](godot/overview.md) - Engine structure overview
- [Testing Overview](testing/overview.md) - Testing strategy

## Godot Engine
### Core Systems
- [Scene System](godot/scene-system.md) - Scene-node tree
- [Input System](godot/input-system.md) - Input handling
- [Collision System](godot/collision-system.md) - Collision detection

### Advanced Topics
- [Replay System](godot/replay-system.md) - Replay implementation
- [State Validation](godot/state-validation.md) - State verification

## Testing
- [Replay Testing](testing/replay-testing.md) - Replay-based testing
- [CI/CD Integration](testing/ci-cd.md) - Automation integration
```

### Usage

```
Mickey: "Need Godot input system information"
1. Read INDEX.md (small context)
2. Find "Input System"
3. Load only godot/input-system.md
→ Efficient context usage
```

## Document Writing Principles

### 1. Conciseness

**Bad Example**:
```markdown
Godot engine is an open-source game engine.
First released in 2014, it uses the MIT license.
Many developers use it...
(continues for 500 words)
```

**Good Example**:
```markdown
## Godot Engine

### Key Features
- Open-source (MIT License)
- Scene-node structure
- GDScript (Python-like)

### Core Concepts
1. Scene = Node Tree
2. Signals for Communication
3. Built-in Physics Engine
```

### 2. Structure

**Hierarchical Organization**:
```
Overview
  ↓
Core Concepts
  ↓
Examples
  ↓
Detailed Reference
```

### 3. Cross-Reference

```markdown
## Scene System

Scenes are composed of node trees.

**Related Documents**:
- [Node System](node-system.md) - Node details
- [Signal System](signal-system.md) - Communication methods

**Reference**:
For input handling, see [Input System](input-system.md)
```

## Real-World Example

### Godot Engine Analysis Case

**Problem**: Massive codebase with 13,666 files

**Solution Process**:

#### Step 1: Write Overview

```markdown
# common_knowledge/godot/overview.md

## Godot Engine Structure

### Main Directories
- `core/`: Engine core
- `scene/`: Scene/node system
- `servers/`: Rendering/physics servers
- `modules/`: Extension modules

### Key Concepts
- Scene-Node Tree
- Signals
- GDScript

**Detailed Documents**:
- [Scene System](scene-system.md)
- [Input System](input-system.md)
```

#### Step 2: Detail Only What's Needed

```markdown
# common_knowledge/godot/input-system.md

## Input System

### Input Class
```gdscript
# Check if key pressed
if Input.is_action_pressed("move_up"):
    position.y -= speed * delta
```

### Custom Actions
Define in Project Settings → Input Map

### Replay Mode
```gdscript
# Override input
func get_action_strength(action: String) -> float:
    if replay_mode:
        return replay_data.get_input(action)
    return Input.get_action_strength(action)
```
```

#### Step 3: Utilize

```
Mickey 3: "Need input system information"
→ Check INDEX.md
→ Load input-system.md
→ Can implement immediately
```

## Knowledge Update Strategy

### When to Update?

1. **When Learning New Concepts**
   ```
   Mickey: "Understanding Godot Signal system"
   → Create common_knowledge/godot/signal-system.md
   ```

2. **After Problem Resolution**
   ```
   Mickey: "Solved error with Delta synchronization"
   → Update common_knowledge/testing/replay-system.md
   ```

3. **When Discovering Patterns**
   ```
   Mickey: "Discovered reset frame detection pattern"
   → Add to common_knowledge/testing/state-validation.md
   ```

### Update Method

```markdown
## Add to Existing Document

### State Validation

#### Ball Reset Detection (Added: 2025-12-11)
```gdscript
func _is_ball_reset(expected: Vector2, actual: Vector2) -> bool:
    var diff = (expected - actual).length()
    return diff > 200.0  # Position jump > 200px
```

**Context**: Discovered in Phase 1-1
**Problem**: Validation fails during Ball reset
**Solution**: Detect large position jumps and skip
```

## Measurable Effects

### Without Knowledge Management

```
Mickey 1: Godot analysis (2 hours)
Mickey 2: Godot re-analysis (1.5 hours)
Mickey 3: Godot re-analysis again (1 hour)
→ Total 4.5 hours (duplicate work)
```

### With Knowledge Management

```
Mickey 1: Godot analysis + documentation (2.5 hours)
Mickey 2: Read docs (10 min) + work
Mickey 3: Read docs (10 min) + work
→ Total 2.5 hours + work (efficient)
```

## Best Practices

### DO ✅

1. **Write INDEX.md First**
   - Understand overall structure
   - Provide entry point

2. **Write Concisely**
   - Include only essentials
   - Include example code

3. **Add Cross-References**
   - Link related documents
   - Provide context

4. **Update Regularly**
   - Reflect new learning immediately
   - Remove outdated information

### DON'T ❌

1. **Put Everything in One File**
   - Wastes context window
   - Difficult to search

2. **Verbose Explanations**
   - Unnecessary background
   - Excessive historical context

3. **Delay Updates**
   - Information loss
   - Duplicate learning

4. **Write Without Structure**
   - Difficult to read
   - Cannot utilize

## Next Steps

- [Real-World Case Study](case-study/godot-replay-system-en.md) - Godot project application case
- [Example Files](../examples/) - Actual knowledge management examples
