# Template A: The Deep Dive

> Use this template for **General Computer Science Theory** -- concepts like
> Virtual Memory, TCP/IP, Compiler Phases, Cache Coherence, Concurrency Models,
> or any fundamental CS topic that isn't language-specific, algorithmic, or a
> direct comparison.

---

## Header Block (Always include first)

```
> **Seed:** "[Paste the original {{...}} prompt text here verbatim]"
> **Lens:** First Principles / The Chief Engineer
```

---

## Section Structure

### 1. Ontological Definition

Provide the **formal, academic definition** of the concept. Be surgical:
- Define *what* it is in one precise sentence.
- State *which domain* it belongs to (OS, Networking, Databases, etc.).
- If the term is overloaded (e.g., "process" vs "thread"), disambiguate immediately.

Do NOT start with "X is a..." followed by a vague paraphrase. Start with the most precise technical sentence possible.

### 2. The Internal Mechanics (Under the Hood)

This is the core section. Explain **how it actually works** at the system level:
- **Control Flow:** What sequence of operations occurs? What triggers what?
- **State Changes:** What data structures change, and how?
- **Data Flow:** Where does data move -- between registers, caches, memory, disk, network?

**Mandatory inclusions:**
- At least one **diagram, pseudo-code block, or mathematical formula** illustrating the mechanism.
- Name the key **data structures** involved (hash tables, page tables, B-trees, etc.).
- If there is a **state machine**, draw it or describe the transitions explicitly.

### 3. Systems Context & Anchoring

Ground the abstract concept using a **real-world analogy**:
- Pick an analogy from everyday life (a library, a restaurant kitchen, a postal system, a highway, a factory assembly line).
- Map each component of the analogy to a component of the system.
- Make the analogy precise enough that a reader could *predict* system behavior from it.

**Example:** "Virtual Memory is like a library's card catalog. The catalog (page table) maps book titles (virtual addresses) to shelf locations (physical frames). When a book isn't on the shelf (page fault), the librarian retrieves it from the warehouse (disk)."

Do NOT use generic analogies like "think of it like a box." The analogy must carry explanatory weight.

### 4. Edge Cases & Constraints

Identify **when this concept breaks, fails, or behaves unexpectedly**:
- What are the boundary conditions?
- What assumptions does it rely on?
- What happens under extreme load, scale, or adversarial input?
- Are there known failure modes or trade-offs?

Name at least 2 concrete edge cases with brief explanations.

---

## Output Rules

- **Depth:** Scale with the topic's complexity. Simple concepts may need 200 words; deep systems topics may need 800+. Cover every section fully -- do not truncate to hit a number. When in doubt, include more detail rather than less.
- **Tone:** Zero preamble. Start directly with the definition. No "Let's explore..." or "In this note..."
- **Formatting:** Use headers, bullet points, and code blocks. Dense, scannable, professional.
