# Template H: The Mathematician

> Use this template for **Mathematics, Logic, and Formal Proofs** -- when the
> prompt asks about a mathematical concept, theorem, proof technique, linear
> algebra, calculus, discrete math, probability, statistics, or any topic where
> formal notation and rigorous reasoning are essential.

---

## Header Block (Always include first)

```
> **Seed:** "[Paste the original {{...}} prompt text here verbatim]"
> **Lens:** First Principles / The Feynman Razor
```

---

## Section Structure

### 1. The Intuition First

Before any formalism, explain **what this concept means** using a physical or visual metaphor:
- "An eigenvector is a direction that a transformation stretches but doesn't rotate -- imagine pulling taffy along a fixed axis."
- "A Markov Chain is like a board game where you roll dice at each square and the rules only depend on which square you're on, never where you came from."

This section should make a reader *feel* the concept before seeing any symbols.

### 2. Formal Definition

Now state the **precise mathematical definition** using proper notation:

$$
\text{Definition: } [Formal Statement]
$$

- Define every symbol used.
- State the domain and codomain explicitly.
- If the definition has preconditions or constraints, list them as numbered items.

### 3. Worked Example

Walk through a **concrete numerical example** step by step:
- Use small, human-readable numbers (2x2 matrices, single-digit values).
- Show every intermediate computation -- do not skip steps.
- Box or highlight the final answer.

### 4. Visual Representation

Provide a **geometric, graphical, or diagrammatic** interpretation:
- For linear algebra: show vector plots or transformation grids.
- For calculus: describe the curve, area, or slope geometrically.
- For probability: use a sample space diagram, tree, or Venn diagram.
- For discrete math: use a graph or grid.

If a Mermaid diagram fits, use one. Otherwise, describe the visual precisely enough that the reader can draw it.

### 5. Connections & Applications

Link this concept to **practical applications**:
- **In CS:** Where does this appear in algorithms, ML, graphics, cryptography?
- **In Engineering:** Where does this appear in signal processing, control systems, optimization?
- **In Daily Life:** Is there a surprising real-world instance?

### 6. Common Pitfalls

Name 2-3 mistakes students commonly make:
- "Confusing eigenvalues with eigenvectors."
- "Forgetting that the determinant must be non-zero for invertibility."
- "Misapplying Bayes' theorem by swapping P(A|B) with P(B|A)."

---

## Output Rules

- **Depth:** Scale with the theorem's depth. A basic definition may need 200 words; a proof with multiple lemmas or a concept with geometric + algebraic interpretations may need 800+. The worked example must be thorough regardless.
- **Tone:** Feynman-style -- rigorous but human. The intuition section is as important as the formal one.
- **Formatting:** LaTeX notation for formulas (use `$$` blocks). Worked example is mandatory.
