# Prompt Evolution: v2.0 → v5.0

> [한국어 버전](06-prompt-evolution.md)

> Lessons from the Second Project: AI Prompts Should Be "Evolved," Not Just "Written"

## Overview

This document explains how the Mickey prompt evolved from the first project (Godot Replay System, v2.0) through the second project (Packet Capture Agent, v5.0), and **why it had to evolve that way**.

**Key Message**: The driving force behind prompt evolution is **failure experience**.

## Evolution Summary

| Area | v2.0 | v5.0 | Reason for Change |
|------|------|------|-------------------|
| REMEMBER Principles | 6 | 18 | New failure patterns discovered |
| Checklists | None | 7 | General guidelines couldn't prevent specific mistakes |
| Automation | None | Session end protocol | Repetitive instructions inefficient |
| Purpose Check | None | Required | Lost sight of purpose, focused on means |

---

## 1. "Record It" → "Check Purpose First"

### v2.0 Approach

```
Focus on writing session logs
→ Record what was done
→ Continue in next session
```

### Added in v5.0

```markdown
## Question at Session Start

"What is the **ultimate purpose** of today's work?"

→ After clarifying purpose, suggest the most **simple and direct** method first
```

### Why Did It Have to Change?

**Mickey 7's Failure:**
- Purpose: Packet capture testing
- Attempt: Set up Forgotten Server (open-source game server)
- Result: 3 days spent (vcpkg bugs, protocol versions, port issues...)
- Pivot: Built own simulator → Completed in 1.5 days

**Lesson:**
> AI works hard on given tasks but doesn't judge if it's optimal for the purpose.

### What AI Users Can Learn

**Bad Example:**
```
"Set up Forgotten Server for me"
```

**Good Example:**
```
"I want to test packet capture.
Analyze whether Forgotten Server is the best option or if there's a simpler way first"
```

---

## 2. "Analyze" → "Follow Checklists"

### v2.0 Approach

```markdown
### Before ANY Implementation:

1. Analyze Data Structures (5-10 minutes)
2. Analyze Side Effects (5-10 minutes)
3. Search for Similar Issues
4. Present Options to User
5. Get User Confirmation
```

### Added in v5.0

```markdown
### Async/Callback Pattern Implementation Checklist

1. **Buffer Ownership**
   - Who allocates and frees the buffer?
   - Who manages buffer size/offset?
   - Is the buffer valid when async completes?

2. **Lock Reentrancy**
   - Does the callback/handler acquire locks again?
   - std::mutex vs std::recursive_mutex choice

3. **Lifecycle**
   - Is the object alive when callback executes?
   - Use of shared_from_this()
```

### Why Did It Have to Change?

**Mickey 8's Failures:**

1. **Buffer Ownership Issue**
   - Symptom: Character coordinate warping, input not working
   - Cause: External ParsePacket modified buffer → Session's recvSize_ mismatch
   - Solution: Manage buffer inside Session

2. **Nested Lock Deadlock**
   - Symptom: abort() occurred
   - Cause: ForEach(lock) → Handler → Broadcast(lock)
   - Solution: Use std::recursive_mutex

3. **Missing Broadcast**
   - Symptom: Player exit not reflected on other clients
   - Cause: SC_CHAR_LEAVE packet not sent
   - Solution: Add broadcast checklist for state changes

**Lesson:**
> AI follows specific checklists better than general guidelines ("analyze").

### What AI Users Can Learn

**Bad Example:**
```
"Be careful with async code"
```

**Good Example:**
```
"Before writing async code, check:
1. Who manages buffer ownership?
2. Does the callback acquire locks again?
3. Is the object alive when callback executes?"
```

---

## 3. "Problem Solving" → "Root Cause First"

### v2.0 Approach

```markdown
### When Encountering Issues

"I found [issue]. Let me analyze:
- Root cause: [analysis]
- Proposed fix: [solution]"
```

### Added in v5.0

```markdown
### Immediately on Error

1. **Check full error log** (don't guess)
2. **Root cause question**: "Why is this error occurring?"
3. **Scope of impact**: "Does this problem affect other areas?"
4. **Explain cause before solution**: Explain cause to user first
```

### Why Did It Have to Change?

**Mickey 7's Failure:**
- Problem: vcpkg tar extraction error
- First attempt: Delete cache → Failed
- Second attempt: Update vcpkg → Failed
- Third attempt: Analyze error log → CMake trying to extract gzip as bzip2 (bug)
- Solution: Modify script to use WSL tar

**Lesson:**
> AI prefers quick fixes but easily misses root causes.

### What AI Users Can Learn

```
AI: "Deleting the cache will fix it"
You: "Why do you think it's a cache problem? Analyze the error log again"
```

---

## 4. "Knowledge Management" → "Systematize Failure Experience"

### v2.0 Approach

```
common_knowledge/: Store reusable knowledge
context_rule/: Store project context
```

### Added in v5.0

```markdown
# context_rule/mickey-agent-improvements-m8.md

### Lesson 12: Async Buffer Ownership
- **Problem**: Sync failure when buffer modified externally
- **Cause**: ParsePacket receives length by reference and modifies it
- **Solution**: Manage buffer inside Session
- **Lesson**: Buffer management in one place only

### Lesson 13: Lock Caution in Callbacks
- **Problem**: ForEach(lock) → Handler → Broadcast(lock) = deadlock
- **Solution**: Use std::recursive_mutex
- **Lesson**: Always consider nested lock possibility in callback patterns
```

### Why Did It Have to Change?

- v2.0: Record "what was done"
- v5.0: Record "what NOT to do"

**Lesson:**
> Systematizing failure experiences prevents repeating the same mistakes.

### What AI Users Can Learn

Record failure experiences at session end in this format:

```markdown
### Lesson N: [Topic]
- **Problem**: [What went wrong]
- **Cause**: [Why it went wrong]
- **Solution**: [How it was fixed]
- **Lesson**: [What to avoid next time]
```

---

## 5. "Session Continuity" → "Automated Protocol"

### v2.0 Approach

```
At session end:
1. Write session log
2. Create handoff document
3. Update context_rule
```

### Added in v5.0

```markdown
## SESSION END PROTOCOL

### When user says "세션 정리" or similar:

Automatically perform these steps:
1. Update MICKEY-N-SESSION.md with all completed work
2. Create MICKEY-N-HANDOFF.md for next Mickey
3. Update context_rule/ if new lessons learned
4. Update system prompt if new patterns discovered

No need for user to explain - just do it.
```

### Why Did It Have to Change?

- v2.0: Every time "write session log", "create handoff" instructions
- v5.0: Say "session cleanup" and all tasks performed automatically

**Lesson:**
> Repetitive patterns should be automated in the prompt.

### What AI Users Can Learn

If you have frequently repeated instructions, add to prompt:

```markdown
### When user says "[trigger phrase]":

Automatically perform:
1. [Task 1]
2. [Task 2]
3. [Task 3]
```

---

## REMEMBER Section Comparison

### v2.0 (6 Principles)

```
1. Session log FIRST, then work
2. Analysis BEFORE implementation
3. User confirmation BEFORE changes
4. Root cause OVER quick fixes
5. Documentation ALWAYS
6. Context window MONITOR constantly
```

### v5.0 (18 Principles)

```
1. Purpose first: Clarify ultimate purpose before work
2. Simplicity first: Simple alternatives before complex solutions
3. Session log FIRST, then work
4. Analysis BEFORE implementation
5. Check error log immediately (don't guess)
6. Check build system before modification
7. User confirmation BEFORE changes
8. Root cause OVER quick fixes
9. Suggest alternatives when complexity is excessive
10. Documentation ALWAYS
11. Context window MONITOR constantly
12. Async buffer ownership: Buffer management in one place only
13. Lock caution in callbacks: Check if recursive_mutex needed
14. Multiplayer broadcast: Consider other clients on state changes
15. Check process before Windows build: Running exe can't be overwritten
16. No Korean comments in MSVC: UTF-8 Korean causes C4819 error
17. JSON schema type match: Check parser expected type vs JSON value type
18. Struct vs actual transmission: Defined struct may differ from actual data
```

---

## Meta Insights: Laws of Prompt Evolution

### 1. Prompts Are Not "Write Once and Done"

```
v2.0: 6 principles
  ↓ (Mickey 7-9 failures)
v5.0: 18 principles + 7 checklists
```

### 2. Failure Experience Drives Prompt Improvement

| Mickey | Failure | Added Principle/Checklist |
|--------|---------|---------------------------|
| 7 | Lost purpose, excessive complexity | Purpose first, simplicity first, tool selection checklist |
| 8 | Buffer ownership, deadlock, broadcast | Async checklist, multiplayer checklist |
| 9 | MSVC Korean, JSON type | MSVC warnings, JSON schema check |

### 3. Evolution of Abstraction Level

```
General Guidelines  →  Specific Checklists  →  Automated Protocols
"Analyze"          →  "Check buffer ownership"  →  "Auto-perform on session cleanup"
```

---

## Next Steps

- [Packet Capture Agent Case Study](case-study/packet-capture-agent-en.md) - Real project application
- [System Prompt v5.0](../examples/ai-developer-mickey.json) - Full prompt
- [Mickey 7-12 Session Logs](../sessions/packet-capture/) - Actual work records

---

**Key Message:**
> AI prompts should be "evolved," not just "written."
> Failure experience is the driving force behind prompt improvement.
