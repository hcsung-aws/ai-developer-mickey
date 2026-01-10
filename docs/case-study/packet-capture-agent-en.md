# Packet Capture Agent Case Study

> [한국어 버전](packet-capture-agent.md)

> Second Project: Mickey 1-12, Prompt v2.0 → v5.0 Evolution

## Project Overview

| Item | Content |
|------|---------|
| **Goal** | Online game TCP packet capture → Source code-based parsing → Reproducible log generation |
| **Period** | 2025-12-13 ~ In Progress |
| **Sessions** | Mickey 1-12 |
| **Prompt Version** | v2.0 → v5.0 |
| **GitHub** | [packet-capture-log-agent](https://github.com/hcsung-aws/packet-capture-log-agent) |

## Project Journey

### Phase 1: Foundation Building (Mickey 1-4)

| Mickey | Main Work | Result |
|--------|-----------|--------|
| 1 | Requirements analysis, tech stack decision | C# .NET 9 selected, proposal written |
| 2 | Raw Socket capture, dynamic protocol parsing | EchoClient test successful |
| 3 | Packet replay feature, real game research | Most games use encryption confirmed |
| 4 | XTEA/RSA decryption pipeline | Transform pipeline designed |

**Lessons from this phase:**
- Be careful with MemoryStream Position management
- Most real games use encryption → Test environment needed

### Phase 2: Test Environment Setup Attempt (Mickey 5-7)

| Mickey | Main Work | Result |
|--------|-----------|--------|
| 5 | (Short session) | - |
| 6 | Forgotten Server build environment | vcpkg path/version issues |
| 7 | vcpkg bug resolution, **Direction change** | Own simulator decision ⭐ |

**Mickey 7's Key Decision:**

```
Purpose: Packet capture testing
Attempt: Forgotten Server setup (3 days spent)
Problems: vcpkg bugs, protocol versions, port issues...
Decision: Pivot to own simulator development
Result: Completed in 1.5 days
```

**Principles added from this phase:**
- Purpose first: Clarify ultimate purpose before work
- Simplicity first: Simple alternatives before complex solutions
- Early pivot: Suggest alternatives when complexity is excessive

### Phase 3: Simulator Development (Mickey 8-12)

| Mickey | Main Work | Result |
|--------|-----------|--------|
| 8 | MMORPG simulator implementation | Boost.Asio server, multiplayer |
| 9 | DB integration, protocol auto-generation | MySQL ODBC, GitHub upload |
| 10 | Packet replay test, character system | Struct packing issue resolved |
| 11 | Build environment cleanup, protocol sync | vcpkg disabled |
| 12 | (Current) | - |

**Mickey 8's Key Failures and Lessons:**

1. **Buffer Ownership Issue**
   ```
   Symptom: Character coordinate warping, input not working
   Cause: External ParsePacket modifying buffer
   Solution: Manage buffer inside Session
   ```

2. **Nested Lock Deadlock**
   ```
   Symptom: abort() occurred
   Cause: ForEach(lock) → Handler → Broadcast(lock)
   Solution: Use std::recursive_mutex
   ```

3. **Missing Broadcast**
   ```
   Symptom: Player exit not reflected on other clients
   Cause: SC_CHAR_LEAVE packet not sent
   Solution: Add broadcast checklist for state changes
   ```

**Checklists added from this phase:**
- Async/callback pattern checklist
- Multiplayer state sync checklist
- Windows build checklist

## Prompt Evolution Timeline

```
Mickey 1-6: Using v2.0 prompt
  │
  ├─ Mickey 7 failure: Lost purpose, excessive complexity
  │   └─ Added: Purpose first, simplicity first, tool selection checklist
  │
  ├─ Mickey 8 failure: Buffer ownership, deadlock, broadcast
  │   └─ Added: Async checklist, multiplayer checklist
  │
  ├─ Mickey 9 failure: MSVC Korean, JSON type
  │   └─ Added: MSVC warnings, JSON schema check, session end protocol
  │
Mickey 10-12: Using v5.0 prompt
```

## Comparison with Godot Project

| Item | Godot Replay (v2.0) | Packet Capture (v5.0) |
|------|---------------------|----------------------|
| Environment | Single (Godot) | Cross-platform (WSL + Windows) |
| Complexity | Medium | High |
| Sessions | 6 | 12 |
| Main Challenges | Frame sync, test automation | Network, DB, build system |
| Prompt Changes | Basic patterns established | Checklists, automation added |

## Key Lessons

### 1. Don't Lose Sight of Purpose

```
Bad: "Set up Forgotten Server for me"
Good: "Packet capture testing is the goal. Analyze the simplest approach first"
```

### 2. Specific Checklists Over General Guidelines

```
Bad: "Be careful with async code"
Good: "Check buffer ownership, lock reentrancy, object lifecycle"
```

### 3. Systematize Failures

```markdown
### Lesson N: [Topic]
- Problem: [What went wrong]
- Cause: [Why it went wrong]
- Solution: [How it was fixed]
- Lesson: [What to avoid next time]
```

## Related Documents

- [Prompt Evolution Guide](../06-prompt-evolution-en.md) - Detailed v2.0 → v5.0 analysis
- [Mickey 7-12 Session Logs](../../sessions/packet-capture/) - Actual work records
- [System Prompt v5.0](../../examples/ai-developer-mickey.json) - Full prompt

---

*This document is for an in-progress project and will be updated upon completion.*
