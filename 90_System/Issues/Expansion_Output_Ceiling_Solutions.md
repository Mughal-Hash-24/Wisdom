# Architectural Upgrade Blueprint: The Two-Pass Expansion System

**Related Issue:** [[Expansion_Output_Ceiling]]
**Filed:** 2026-03-17
**Status:** In Design Phase (Lateral Planning)

---

## 1. The Core Problem Statement

The Kybernetes expansion pipeline suffers from **"Topic Compression" (The Slop Effect)**. 
Because LLM agents are physically constrained to ~800-1000 words per invocation, passing a broad prompt (e.g., "Explain all 23 design patterns") forces the agent to compress the entire scope into that single window. The result is shallow, superficial coverage of profound topics.

Previous theoretical solutions failed because they either:
- Violated separation of concerns (Orchestrator guessing domain structures)
- Relied on non-deterministic LLM auto-splitting
- Reverted to rigid, pre-defined templates (undoing Principle Cards)

## 2. The Solution: Two-Pass Architecture via Explicit Directives

To solve Topic Compression without violating system principles, Kybernetes must shift from a "Single-Shot" to a "Planner-Executor" expansion model. 

The domain expert (the Agent) must define the structure (*The Blueprint*), and the Orchestrator must execute that structure iteratively.

Crucially, **the user must explicitly opt-in** to the mode of expansion via block prefixes. The system will never guess.

### The Four Directives

#### 1. `{{@expand ...}}` : The Standard Mode (Single-Shot)
- **Behavior:** The legacy behavior. One prompt, one pass, ~800 words.
- **Use Case:** Narrow, focused topics (e.g., `{{@expand Explain the Singleton pattern}}`). 
- **Mechanism:** The prompt is passed directly to the domain agent. The agent writes until natural conclusion or token limit.

#### 2. `{{@deep ...}}` : The Unconstrained Two-Pass
- **Behavior:** The agent defines the blueprint; the orchestrator executes it in full.
- **Use Case:** Broad topics where the user trusts the agent to define the scope (e.g., `{{@deep Explain the history of the Roman Empire}}`).
- **Mechanism:**
  - **Pass 1 (Planner):** Orchestrator asks Agent for an unconstrained Table of Contents (Blueprint).
  - **Pass 2 (Executor):** Orchestrator loops over the Blueprint, calling the Agent for each section independently.

#### 3. `{{@blueprint:N ...}}` : The Constrained Two-Pass
- **Behavior:** The agent defines the blueprint, but is forced to fit the topic into exactly `N` sections.
- **Use Case:** Broad topics where the user wants to budget the output length (e.g., `{{@blueprint:3 Explain Quantum Mechanics}}` -> yields exactly 3 agent calls / ~2,400 words).
- **Mechanism:**
  - **Pass 1 (Planner):** Orchestrator asks Agent for a Blueprint containing exactly `N` sections.
  - **Pass 2 (Executor):** Orchestrator loops over the `N` sections.

#### 4. `{{@draft ...}}` : Human-in-the-Loop Planning
- **Behavior:** The system generates the blueprint and stops, injecting it into the note for user review.
- **Use Case:** Massive, multi-faceted topics requiring precise human direction before burning API tokens (e.g., `{{@draft Build a master curriculum for Computer Science}}`).
- **Mechanism:**
  - **Pass 1 (Planner):** Orchestrator asks Agent for an unconstrained Blueprint.
  - **Pause:** `@surgeon` injects the Blueprint as markdown checkboxes and rewrites the prefix to `{{@expand ...}}` (or `@deep`).
  - **Execution Deferred:** Processing halts. The user manually edits the checkboxes. The next time `/os:sort` runs, it processes the edited list.

---

## 3. Systemic Implications & Re-scoping

This is a major architectural upgrade that touches multiple subsystems. Before moving to implementation, the following areas must be deeply analyzed:

### A. The Definition of a "Block"
Currently, `scan_inbox` treats `{{...}}` as atomic units. Under the new architecture, a block is no longer atomic. A `@deep` block represents an array of sub-blocks. 
- *Question:* How does `scan_inbox` pass this relationship to `inbox-sort`?
- *Question:* How does `@surgeon` stitch an array of 5 temp files (`_expand_1_1.md` to `_expand_1_5.md`) back into the single space previously occupied by the original `{{...}}` block?

### B. Latency and Token Economics
A single `{{@deep ...}}` block that yields 6 sections will require 7 agent invocations (1 Planner + 6 Executor). 
- If an inbox file has three `@deep` blocks, `/os:sort` goes from ~1 minute to ~10+ minutes.
- *Implication:* Console logging inside `inbox-sort` must be completely overhauled to show real-time, nested progress (e.g., `[EXPAND] Block 1 (Deep) -> Blueprint Generated -> Executing Section 3/6`).

### C. Principle Card Integrity During Planning
When Pass 1 (Planner) runs, it must still respect the assigned Principle Card. 
- *Implication:* If `@turing` is generating a blueprint for a CS topic using the `Template F (Debugger)` card, the blueprint it generates must reflect a debugging structure (Symptoms -> Hypothesis -> Internals -> Fix). The domain agent instructions must be carefully designed to ensure Pass 1 outputs outlines that *align* with their stylistic directives.

### D. The `@turing` and `@euler` Rigid Templates
Agents `@turing` and `@euler` currently use rigid templates (A-I) loaded via `load_template`. 
- *Conflict:* If a user calls `{{@deep ...}}` on a `@turing` block, does the Two-Pass system override the rigid template A-I system? Or does Pass 1 use the A-I template as the blueprint itself? This intersection needs exact resolution.
