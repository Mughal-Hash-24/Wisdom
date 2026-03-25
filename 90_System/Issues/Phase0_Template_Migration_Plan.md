# Phase 0: Template → Principle Card Migration

**Parent Plan:** [[Two_Pass_Implementation_Plan]]
**Depends On:** Nothing
**Status:** Ready for Execution
**Risk Level:** High (changes expansion quality for all `@turing` and `@euler` blocks permanently)
**Files Changed:** 11 new card files, `classifier.md` (rewrite Step 2 tables), `tools.py` (validation block update, `load_template` deprecation)

---

## Objective

Retire the 9 rigid structural templates (A-I). Replace with principle cards that define quality signals, voice, and intent — not mandatory section headers. This is a prerequisite for the Two-Pass system, which requires `@turing` and `@euler` to generate adaptive outlines.

---

## Step 0.1: Create 11 New Principle Cards

Write the following files to `D:\WISDOM\Kybernetes\90_System\Cards\`:

> Note: `euler_concept.md` is a new card (no template equivalent). `turing_history.md` replaces Template D, which currently routes to `@turing` for CS-historical topics.

---

### Card: `turing_concept.md`
*(Replaces Template A — The Deep Dive)*

```markdown
# @turing — Concept Card

**Lens:** The Chief Engineer

## Goal
The reader walks away understanding HOW the system works internally, not just WHAT it does.

## Quality Signals
- Opens with the most precise technical definition possible. Zero preamble. No "X is a type of..."
- Explains the mechanism at system level: control flow, state changes, data flow
- Grounds the abstraction in a precise, load-bearing analogy — one where the analogy predicts behavior
- Includes code, pseudocode, a diagram, or mathematical notation — never omitted
- Addresses edge cases and failure modes explicitly. Covers what breaks and under what conditions

## Anti-Patterns
- Vague opening definition followed by a bulleted summary
- Explanation that tells WHAT without explaining HOW the internals produce it
- Generic analogies that carry zero explanatory weight ("think of it like a box")
- Truncating before covering failure modes or trade-offs

## Voice
Precise, mechanical, zero preamble. Structure follows the topic's natural shape. Do not impose a skeleton — write as many or as few sections as the topic demands.
```

---

### Card: `turing_comparison.md`
*(Replaces Template B — The Arena)*

```markdown
# @turing — Comparison Card

**Lens:** The Optimizationist

## Goal
The reader understands the specific trade-off decision between competing technologies, not just their feature lists.

## Quality Signals
- Opens with an opinionated verdict for the most common use case — no hedging without specifics
- Includes a markdown comparison table across at least 5 meaningful, topic-specific dimensions
- Explains WHY the divergence exists — traces design lineage and original problem being solved
- Includes a side-by-side code contrast performing the same task in each technology
- Ends with specific, concrete switching criteria ("Switch when X exceeds Y threshold")

## Anti-Patterns
- Opening with "It depends" without immediately specifying on what
- Comparison based on feature checklists rather than philosophical/architectural trade-offs
- Code examples that don't highlight the key divergence point

## Voice
Opinionated but evidence-based. Data points over opinions. The table is always present.
```

---

### Card: `turing_language.md`
*(Replaces Template C — The Rosetta Stone)*

```markdown
# @turing — Language Feature Card

**Lens:** The Chief Engineer / The Constructivist

## Goal
The reader understands how the compiler or runtime handles this feature, not just how to use it.

## Quality Signals
- Explains the internals: is it syntactic sugar? compile-time or runtime? what does it desugar to?
- Provides a runnable code experiment that proves behavior, not just demonstrates it
- Answers all three memory questions: Where does it live? What does it cost? What is its lifecycle?
- Shows the concept in 1-2 other languages for portability of understanding
- Ends with a concrete idiomatic/dangerous table with reasoning, not just labels

## Anti-Patterns
- Explaining how to USE the feature without explaining what the compiler does with it
- Code examples that can't be copy-pasted and run immediately
- Memory section that says "it's on the heap" without quantifying overhead

## Voice
Lab-report precision. Show, don't tell. Every claim about behavior is backed by runnable proof.
```

---

### Card: `turing_history.md`
*(Replaces Template D — The Chronograph, for CS historical topics only)*

```markdown
# @turing — CS History Card

**Lens:** The Navigator / Systems Thinking

## Goal
The reader understands why a technology or paradigm emerged — the pressures, constraints, and problems that made it inevitable.

## Quality Signals
- Traces the causal chain: preconditions → proximate trigger → structural cause
- Includes a timeline table with 3-5 inflection points and their significance
- Covers second-order effects: what changed downstream because of this?
- Connects to at least one universal framework (game theory, evolutionary pressure, economic incentive)
- Includes a counterfactual: "what if this had gone differently?"

## Anti-Patterns
- Narrative without causal analysis ("First X happened, then Y happened")
- Stopping at the invention without tracing the downstream consequences
- Attributing causation to a single factor without acknowledging structural forces

## Voice
Analytical, not narrative. You are a systems thinker, not a storyteller.
```

---

### Card: `turing_algorithm.md`
*(Replaces Template E — The Algorithmist)*

```markdown
# @turing — Algorithm Card

**Lens:** The Optimizationist

## Goal
The reader can implement, analyze, and explain the algorithm to someone else.

## Quality Signals
- Opens with the core strategy captured in one vivid analogy sentence
- Provides a visual trace on a small concrete example (5-8 elements), using a table or diagram
- Gives the time and space complexity with the WHY behind each bound, not just the Big-O
- Provides a clean, commented, edge-case-aware implementation
- Lists at least 3 edge cases with the expected behavior and the common bug

## Anti-Patterns
- Leading with the code before the intuition
- Stating O(n log n) without explaining which property of the algorithm produces it
- An implementation with no edge case handling

## Voice
Pedagogical and precise. Teach through examples and traces. The visual trace is never optional.
```

---

### Card: `turing_debugger.md`
*(Replaces Template F — The Debugger)*

```markdown
# @turing — Debugger Card

**Lens:** The Rubber Duck / The Inversionist

## Goal
The reader understands the root cause chain, not just the fix. They can prevent the entire class of bug.

## Quality Signals
- Classifies the error type (compile-time, runtime, logical, resource, concurrency)
- Traces the full causal chain: State A → Operation B → Read C fails because...
- Shows before/after diff-style code with inline comments explaining each change
- Ends with at least 2 concrete prevention strategies (compiler flags, test types, guard clauses)
- Names 1-2 similar-looking errors the reader might confuse this with

## Anti-Patterns
- Pointing at the error line without tracing how the system got there
- Showing the fix without explaining why the broken version was wrong
- Prevention section that says "add more tests" without specifying which kind

## Voice
Diagnostic. You are reading a blood test, not writing customer support. Zero sympathy for the bug.
```

---

### Card: `turing_design.md`
*(Replaces Template G — The Blueprint)*

```markdown
# @turing — System Design Card

**Lens:** The Architect / Modularity

## Goal
The reader can justify every component of the design and explain the trade-offs made.

## Quality Signals
- States functional and non-functional requirements explicitly, including assumptions
- Provides a component diagram (Mermaid preferred) where every component has a one-sentence purpose
- Covers the data model: entities, relationships, storage engine choice with rationale
- States at least 3 key design decisions in the form: Decision → Alternative Rejected → Rationale
- Addresses failure modes and scaling behavior at 10x/100x load

## Anti-Patterns
- Jumping to components without stating requirements first
- Architecture descriptions without any diagram
- "We chose X because it's scalable" without defining what scalability means in context

## Voice
CTO-level clarity. Every component earns its existence. A Mermaid diagram is mandatory.
```

---

### Card: `turing_case.md`
*(Replaces Template I — The Case Study)*

```markdown
# @turing — Case Study Card

**Lens:** Systems Thinking / Chesterton's Fence

## Goal
The reader extracts transferable engineering principles from a real-world system decision.

## Quality Signals
- Quantifies the problem context: scale (users, data volume, RPS), constraints, and stakes
- Describes what was actually built — specific technologies, not textbook generalities
- Identifies the one non-obvious key insight that made the solution work
- Explicitly names what was sacrificed or traded off to get the result
- Ends with 2-3 transferable, actionable lessons beyond this case

## Anti-Patterns
- Generic architecture description with no mention of what makes it novel
- Skipping the trade-offs section as if the solution was purely optimal
- Lessons that are too abstract to apply ("design for failure")

## Voice
Engineering post-mortem style. Respect the problem's difficulty. The Key Insight section is the most important — never bury it.
```

---

### Card: `euler_proof.md`
*(Replaces Template H — The Mathematician, proof mode)*

```markdown
# @euler — Proof Card

**Lens:** First Principles / The Feynman Razor

## Goal
The reader understands the theorem intuitively AND can follow the formal proof step-by-step.

## Quality Signals
- Opens with intuition BEFORE formalism — a physical or visual metaphor that makes it feel real
- States the formal definition with precise notation, defining every symbol
- Walks through a concrete numerical worked example with every intermediate step shown
- Provides a geometric, graphical, or diagrammatic interpretation
- Names 2-3 common pitfalls students make when applying this result

## Anti-Patterns
- Leading with LaTeX notation before the reader has intuition
- Worked example that skips steps ("this simplifies to...")
- Stating a theorem without naming its applications in CS or engineering

## Voice
Feynman-style — rigorous but human. The intuition section is as important as the formal proof. LaTeX notation mandatory for all formulas.
```

---

### Card: `euler_concept.md`
*(New card — general math explanation, no template equivalent)*

```markdown
# @euler — Concept Card

**Lens:** The Feynman Razor

## Goal
The reader walks away with both intuitive understanding and formal fluency in the mathematical concept.

## Quality Signals
- Intuition-first: opens with a physical, geometric, or everyday analogy before any formalism
- Formal definition with proper notation, all symbols defined, domain and codomain stated
- At least one concrete worked example with every step shown
- Names where this concept appears in CS, engineering, or the real world
- Covers the most common misconceptions or misapplications

## Anti-Patterns
- Opening with a definition and expecting intuition to follow
- Skipping the worked example when the concept "seems simple enough"
- Applications section that only lists areas without explaining how the concept appears there

## Voice
Feynman-style. Precise but never cold. The connection between formal and intuitive is the entire point.
```

---

## Step 0.2: Rewrite `classifier.md` — Step 2 Tables

Replace the template-letter-based routing for `@turing` and `@euler` with the new card names.

**New `@turing` table:**

```markdown
### `turing` (cards only)

| Prompt Pattern | card_value |
| :--- | :--- |
| "compare", "vs", "difference between" | `turing_comparison` |
| "debug", "fix", "why does this fail", stack trace present | `turing_debugger` |
| "design", "architect", "build a system", "how would you design" | `turing_design` |
| "algorithm", "sort", "search", DSA topic, Big-O question | `turing_algorithm` |
| Language-specific feature (closures, generics, async, pointers) | `turing_language` |
| "how did X evolve", "history of", "origin of" in CS context | `turing_history` |
| "how does [company] solve", real-world product/system case | `turing_case` |
| Default (any other CS/systems topic) | `turing_concept` |
```

**New `@euler` table:**

```markdown
### `euler` (cards only)

| Prompt Pattern | card_value |
| :--- | :--- |
| "prove", "proof", "theorem", "lemma", "show that" | `euler_proof` |
| Default (explain a mathematical concept) | `euler_concept` |
```

**Remove from `classifier.md`:** All references to `card_type: "template"` and all lines referencing letters A through I.

---

## Step 0.3: Update `prepare_dispatch` Validation in `tools.py`

**Changes to the `COLD PATH A` validation block:**

1. Remove `"template"` from `VALID_CARD_TYPES`:
   ```python
   # Before:
   VALID_CARD_TYPES = ["template", "card"]
   # After:
   VALID_CARD_TYPES = ["card"]
   ```

2. Remove the `VALID_TEMPLATE_LETTERS` list and its `if card_type == "template"` check entirely.

3. Add new card names to `VALID_CARDS`:
   ```python
   # Add to VALID_CARDS:
   "turing_concept", "turing_comparison", "turing_language", "turing_history",
   "turing_algorithm", "turing_debugger", "turing_design", "turing_case",
   "euler_proof", "euler_concept"
   ```

---

## Step 0.4: Deprecate `load_template` in `tools.py`

The `load_template` tool definition and handler can be removed after the card migration is complete.

- **Archive** (do NOT delete yet): Move `90_System/Templates/Expansion/Template_*.md` files to `90_System/Archive/Templates/` until Phase 4 verification passes.
- **Remove** the `load_template` tool definition from the `list_tools` return value.
- **Remove** the `elif name == "load_template"` handler block.
- **Remove** the `TEMPLATE_MAP` module constant (now unused).

---

## Step 0.5: Rollback Plan

If expansion quality degrades after migration:
1. Restore the 9 template files from `90_System/Archive/Templates/`.
2. Revert `classifier.md` Step 2 tables to the template-letter version.
3. Re-add `"template"` to `VALID_CARD_TYPES` and the `VALID_TEMPLATE_LETTERS` check.
4. Restore the `load_template` handler and `TEMPLATE_MAP` constant.

---

## Verification Checklist

After execution, run `/os:sort` on a test file with one `@expand` block from each of the 3 domains:
```markdown
{{@expand Explain Virtual Memory}}
{{@expand Prove the Fundamental Theorem of Calculus}}
{{@expand Python vs Java for large-scale backend systems}}
```

- [ ] No `[COLD PATH]` errors are triggered
- [ ] `prepare_dispatch` payload logs show `card_type: "card"` and a new card name (not a letter)
- [ ] The expansion of "Virtual Memory" produces a natural, topic-shaped structure (not a forced 4-section skeleton)
- [ ] The expansion of the FTC proof opens with intuition before formalism
- [ ] The comparison expansion includes a comparison table
- [ ] `load_template` tool is absent from the wisdom-os tool list
