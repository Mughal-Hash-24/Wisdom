# Template C: The Rosetta Stone

> Use this template for **Programming Language Features & Syntax** -- when the
> prompt asks about a specific language feature like closures, generics, async/await,
> decorators, pattern matching, smart pointers, or any construct tied to a
> particular language's type system, runtime, or compiler.

---

## Header Block (Always include first)

```
> **Seed:** "[Paste the original {{...}} prompt text here verbatim]"
> **Lens:** The Chief Engineer / The Constructivist
```

---

## Section Structure

### 1. Surgical Definition (Internals)

Don't just say what the feature does. Explain how the **compiler or runtime** sees it:
- Is it syntactic sugar for something simpler? If yes, show what it desugars to.
- Is it a compile-time construct (erased at runtime) or a runtime object (allocated in memory)?
- What IR (Intermediate Representation) or bytecode does it produce?
- Does the language spec define it, or is it implementation-specific?

**Real-world analogy:** Ground the concept using an everyday parallel. Example: "A closure is like a tourist carrying a phrasebook from their home country. The phrasebook (captured variables) travels with them (the function) even after they leave their home scope."

### 2. The Laboratory (Proof of Concept)

Provide a **runnable code experiment** that **proves** the behavior, not just demonstrates it:
- Print memory addresses to show allocation
- Trigger a deliberate failure to show error boundaries
- Inspect bytecode/IL output if relevant
- Time a tight loop to show performance characteristics

```[Language]
// Experiment: [What this proves]
// Expected output: [What the reader should see]
```

The experiment should be **copy-pasteable** -- a reader should be able to run it immediately and learn from the output.

### 3. Memory & System Context

Answer these three questions with specifics:

- **Where does it live?**
  Stack, heap, static segment, register, or a combination? Is it boxed? Is there indirection?

- **What does it cost?**
  Overhead per call/allocation? V-table lookups? Boxing/unboxing? Hidden allocations?
  Quantify where possible (e.g., "8 bytes per closure for the captured reference").

- **What is its lifecycle?**
  When is it created? When is it destroyed? Who owns it? Is it reference-counted, garbage-collected, or RAII-managed?

### 4. Cross-Language Parallels

Show how the **same concept** exists (or doesn't) in 1-2 other languages:
- If it exists: how does the implementation differ?
- If it doesn't exist: what workaround does the other language use?

This builds transferable understanding. Keep each parallel to 2-3 sentences + a short snippet.

### 5. Best Practices & Anti-Patterns

Split into two columns:

| Idiomatic | Dangerous |
| :--- | :--- |
| Do this because... | Don't do this because... |

Name at least 2 of each. Explain **why** each is good/bad, not just that it is.

---

## Output Rules

- **Depth:** Scale with the feature's internal complexity. A simple syntactic shortcut may need 200 words; a feature with deep runtime mechanics (e.g., async/await, generics) may need 800+. Cover every section fully.
- **Tone:** Lab-report precision. Show, don't tell.
- **Formatting:** Code blocks are mandatory. The experiment must be runnable.
