# Persona System Diagnostic: Non-CS Content is Bland

**Filed:** 2026-03-04
**Severity:** Design Flaw (not a bug -- a structural bias)
**Affects:** All non-CS expansions (history, literature, art, psychology, economics)

---

## Symptom

Expansions for CS topics are detailed, opinionated, and rich with personality (analogies, diagrams, code proofs, edge cases). Expansions for non-CS topics read like encyclopedia entries -- technically correct but bland, clinical, and lifeless.

**Example contrast:**
- CS prompt about Java Streams → gets memory analysis, runnable code, real-world analogy, anti-patterns. *Feels alive.*
- History prompt about Rasputin → gets dates, causes, effects. *Reads like Wikipedia.*

---

## Root Cause Analysis

### 1. Template Coverage is 78% CS, 11% General, 11% Nothing

| Template | Domain | Personality Level |
| :--- | :--- | :--- |
| A - Deep Dive | CS Theory (OS, Networks) | High -- internals, state machines, analogies |
| B - Arena | CS Comparisons (Python vs Java) | High -- opinionated, side-by-side code |
| C - Rosetta Stone | Programming Languages | High -- bytecode, memory, cross-language |
| E - Algorithmist | DSA | High -- visual traces, complexity proofs |
| F - Debugger | CS Debugging | High -- root cause, fix verification |
| G - Blueprint | System Design | High -- architecture diagrams, trade-offs |
| H - Mathematician | Math/Proofs | Medium -- formal but structured |
| I - Case Study | Tech Companies | High -- MapReduce, Discord, etc. |
| **D - Chronograph** | **Everything else** | **Low -- analytical but soulless** |

**7 of 9 templates are CS-specific.** Non-CS gets ONE template (Chronograph) that must cover history, literature, psychology, economics, art, philosophy, and culture. It can't do all of those well.

### 2. The Chronograph Template is Analytical, Not Narrative

Template D's structure:
1. Causal Chain → Root causes (good for wars, bad for novels)
2. Timeline → Key dates (good for history, useless for literary analysis)
3. Systemic Impact → Second-order effects (good for economics, bad for art)
4. Conceptual Anchors → Game theory, psychology frameworks
5. Counterfactual → "What if?" (good for history, irrelevant for culture)

**Problem:** This is a *systems analysis* template wearing a humanities costume. It forces every non-CS topic through the same analytical lens: "find the root cause, trace the ripple effects, apply a framework." This works for "Why did Rome fall?" but produces dead output for "Analyze the women in The Godfather."

Literary analysis, art criticism, and cultural commentary require:
- **Voice and perspective** (not just facts)
- **Close reading** (textual evidence from the source)
- **Thematic synthesis** (connecting patterns across the work)
- **Emotional and aesthetic engagement** (what does it *feel* like?)

None of these exist in Template D.

### 3. Non-CS Personas Have Thin Mandates

Compare the Chief Engineer to the Historian:

**Chief Engineer (4 mandates + 4 enrichment axes):**
- Explain internals with intuitive analogies
- Use real-world anchors
- Scale depth dynamically
- No fluff, start with definition
- *Axes: internals, memory/complexity, code proof, edge cases*

**Historian (4 mandates + 4 enrichment axes):**
- Trace root causes
- Timeline and impact
- Primary sources
- Systemic parallels
- *Axes: root causes, timeline, systemic impact, parallels*

The Chief Engineer's mandates produce a *distinctive voice* -- you can tell a CE response from a generic one. The Historian's mandates are just "do historical analysis" -- they don't create personality, tone, or surprise.

### 4. Missing Personas Entirely

There is no persona for:
- **Literary Critic** (close reading, thematic analysis, character arcs)
- **Cultural Analyst** (art, music, film, aesthetics)
- **Philosopher** (ethics, epistemology, existentialism)
- **Storyteller/Writer** (narrative craft, prose style, creative technique)

These topics fall through to the **Generalist**, which is the blandest persona -- "first principles, systemic context, evidence, practical output." That's engineer-speak applied to art.

### 5. The Freeform Enrichment Axes are Anemic for Non-CS

When the expander goes Freeform, it auto-enriches using the persona's axes. Compare:

| Persona | Enrichment Axes | Personality Potential |
| :--- | :--- | :--- |
| Chief Engineer | internals, memory/complexity, code proof, edge cases | Highly specific, produces unique output |
| Historian | root causes, timeline, systemic impact, parallels | Generic analytical framework |
| Economist | incentives, market dynamics, second-order effects, data | Decent but clinical |
| Psychologist | evolutionary basis, cognitive mechanism, evidence, practical advice | OK but academic |
| Generalist | first principles, systemic context, evidence, actionable takeaway | **Systems engineering applied to everything** |

The Generalist's axes -- "first principles, systemic context" -- are the axes of an **engineer analyzing a non-engineering topic**. This is why literary analysis reads like a technical report.

---

## Impact

- History notes are factually solid but read like textbook summaries
- Literary analysis lacks close reading, textual evidence, and critical voice
- Art/culture/philosophy prompts get the Generalist treatment: sterile, detached, "first principles"
- The system's personality is fundamentally that of a CS student analyzing the world through CS frameworks
- Notes on non-CS topics are less useful for retention because they lack the engagement that makes CS notes memorable

---

## Proposed Fixes (by effort)

### Quick Win: Enrich existing persona mandates with voice directives
Add **tone and personality** instructions to each non-CS persona. The Chief Engineer has implicit personality ("No fluff. Start with the definition."). The Historian needs equivalent directives:
- "Write like you're telling the story over dinner, not presenting a thesis"
- "Name the people. Quote them. Make the reader see the room."
- "Be opinionated. State which interpretation you find most compelling and why."

### Medium: Create 2-3 new templates for non-CS domains
- **Template J: The Critic** → Literary/film/art analysis (close reading, thematic synthesis, textual evidence, aesthetic engagement)
- **Template K: The Storyteller** → Narrative-driven historical or biographical content (characters, turning points, dramatic irony, pacing)
- **Template L: The Philosopher** → Ethical and philosophical analysis (thought experiments, counterarguments, lived implications)

### Structural: Split the Generalist fallthrough
Replace the single Generalist with domain-specific fallthroughs:
- **Humanist** (literature, philosophy, art, culture) → voice-driven, aesthetically engaged
- **Scientist** (biology, physics, chemistry) → evidence-driven, experimental
- **Generalist** (truly misc) → keeps current behavior
