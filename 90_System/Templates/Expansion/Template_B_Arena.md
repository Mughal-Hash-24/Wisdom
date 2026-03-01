# Template B: The Arena

> Use this template for **Direct Comparisons** between two (or more) technologies,
> frameworks, paradigms, languages, or approaches. Examples: "Python vs Java",
> "REST vs GraphQL", "Monolith vs Microservices", "TCP vs UDP".

---

## Header Block (Always include first)

```
> **Seed:** "[Paste the original {{...}} prompt text here verbatim]"
> **Lens:** The Optimizationist / Second-Order Thinking
```

---

## Section Structure

### 1. Executive Summary

One sentence. Name the winner for the most common use case. Be opinionated:
- "Use X when you need Y; use Z when you need W."
- Do NOT hedge with "it depends" without specifying on what.

### 2. Direct Comparison Matrix

Build a markdown table comparing the two items across **at least 5** meaningful dimensions. Choose dimensions relevant to the specific comparison:

| Dimension | [Item A] | [Item B] |
| :--- | :--- | :--- |
| **Core Philosophy** | ... | ... |
| **Performance** | ... | ... |
| **Memory Model** | ... | ... |
| **Learning Curve** | ... | ... |
| **Ecosystem** | ... | ... |
| **Error Handling** | ... | ... |
| **Concurrency** | ... | ... |

Use concrete facts, not opinions. Include benchmark numbers or Big-O where relevant.

### 3. Structural Divergence (The "Why")

Explain **why** these things were designed differently:
- What problem was each one originally built to solve?
- What trade-off did each designer make? (e.g., Safety vs Speed, Simplicity vs Power, Flexibility vs Performance)
- Trace the **design lineage** -- what came before, and what did each one reject or improve?

**Real-world analogy:** Compare the two items to real-world counterparts. Example: "TCP is like certified mail (guaranteed delivery, tracking, signature). UDP is like dropping a postcard in the mailbox (fast, no confirmation, some may get lost)."

### 4. Code Contrast

Show a **side-by-side** code comparison performing the **exact same task**:
- Choose a task that highlights the key difference (e.g., error handling, concurrency, typing).
- Keep each snippet under 10 lines.
- Comment the key divergence points inline.

```[Language A]
// Item A approach
```

```[Language B]
// Item B approach
```

### 5. When to Switch

Provide **specific, concrete scenarios** where someone currently using A should switch to B, and vice versa. Name the tipping points:
- "Switch from A to B when your team grows past 5 developers."
- "Stay with A if your latency budget is <10ms per request."

---

## Output Rules

- **Depth:** Scale with the complexity of the comparison. A simple tool choice may need 250 words; a paradigm-level divergence (OOP vs FP) may need 800+. Cover every section fully.
- **Tone:** Opinionated but evidence-based. Do not equivocate without reason.
- **Formatting:** The comparison matrix is mandatory. Dense, scannable.
