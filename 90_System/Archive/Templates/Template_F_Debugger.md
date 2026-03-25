# Template F: The Debugger

> Use this template for **Error Logs, Stack Traces, and Code Debugging** -- when
> the prompt contains an error message, a broken code snippet, a runtime exception,
> or asks to diagnose unexpected behavior.

---

## Header Block (Always include first)

```
> **Seed:** "[Paste the original {{...}} prompt text here verbatim]"
> **Lens:** The Rubber Duck / The Inversionist
```

---

## Section Structure

### 1. The Symptom

Interpret the error message or unexpected behavior:
- **Error Type:** Classify it (compile-time, runtime, logical, resource exhaustion, concurrency).
- **Error Message:** Quote the exact error text and decode any jargon.
- **Stack Trace Analysis:** If a stack trace is present, identify:
  - The **originating frame** (where the error was thrown).
  - The **root frame** (where the flawed logic started).
  - Any frameworks/libraries in the trace that may be red herrings.

**Real-world analogy:** "Reading a stack trace is like reading a car crash investigation bottom-up -- the last frame is where the collision happened, but the cause may be the driver who ran the red light 3 frames up."

### 2. The Root Cause

Explain **why** the system is throwing this error:
- Name the specific programming concept being violated (null dereference, buffer overflow, type mismatch, race condition, deadlock, resource leak).
- Show the **exact line(s)** where the bug lives (or the pattern that causes it).
- Explain the **sequence of events** that leads to the failure:
  1. State A is created...
  2. Operation B modifies it...
  3. Read C expects X but gets Y because...

Do NOT just point at the error. Trace the causal chain.

### 3. The Fix

Provide the **corrected code** with inline comments explaining each change:

```[language]
// BEFORE (broken):
// broken_line_here

// AFTER (fixed):
// fixed_line_here  // <- Explanation of why this fixes the issue
```

**Requirements:**
- Show both the broken and fixed code (before/after diff style).
- If there are multiple valid fixes, show the **most idiomatic** one first, then mention alternatives.
- If the fix involves a broader pattern change (e.g., switching from `string` to `string_view`), explain the pattern.

### 4. Prevention (The Inversionist)

How to prevent this class of bug in the future:
- **Compiler/Linter flags:** Are there flags that catch this at compile time?
- **Testing strategy:** What test would have caught this? (Unit test, fuzzing, integration test?)
- **Defensive coding:** What guard clause, assertion, or type constraint would prevent recurrence?
- **Design pattern:** Is there a structural change that eliminates the entire category of bug?

Name at least 2 concrete prevention strategies.

### 5. Related Failure Modes

Name 1-2 **similar-looking but different** errors that a reader might confuse with this one:
- "This looks like a NullPointerException, but if you see it in concurrent code, check for a race condition first."
- "Don't confuse this with X, which has a similar message but a completely different cause."

---

## Output Rules

- **Depth:** Scale with the bug's complexity. A simple typo fix needs 150 words; a concurrency bug or memory corruption may need 800+. The root cause chain must be complete regardless.
- **Tone:** Diagnostic. You are a doctor reading a blood test, not a customer support agent.
- **Formatting:** Before/after code diff is mandatory. Show the exact fix.
