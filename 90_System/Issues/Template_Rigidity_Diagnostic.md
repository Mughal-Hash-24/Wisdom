# Template Rigidity Diagnostic: Forced Structure Kills Content

**Filed:** 2026-03-04
**Severity:** Design Flaw
**Related:** `Persona_NonCS_Diagnostic.md`

---

## Symptom

Even when the expander selects the "correct" template, the output feels forced. Sections that don't apply to the topic get stuffed with filler. Sections that the topic *needs* don't exist in the template. The expansion fits the template's shape instead of the topic's shape.

---

## Evidence: Template vs. Topic Mismatch

### Case 1: Template D (Chronograph) applied to "Critique the women in The Godfather"

| Template Section | Relevance to Prompt |
| :--- | :--- |
| 1. Causal Chain | Irrelevant -- literary characters don't have "root causes" in the historical sense |
| 2. Timeline & Key Inflection Points | Barely relevant -- character arcs aren't chronological events |
| 3. Systemic Impact | Forced -- "how did Connie Corleone impact the economy?" is nonsensical |
| 4. Conceptual Anchors | Partially useful -- psychology applies, game theory doesn't |
| 5. Counterfactual | Marginally useful -- "what if Kay left Michael?" is interesting but not the crux |

**What the prompt actually needs:**
- Close reading of specific scenes and dialogue
- Character comparison (Kay vs Connie vs Apollonia -- different modes of female constraint)
- Authorial intent vs reader interpretation (is Puzo aware of the misogyny?)
- Thematic synthesis (what does femininity *mean* in this world?)

None of these exist as template sections.

### Case 2: Template B (Arena) applied to "Compare Rasputin's influence to Richelieu and Sejanus"

| Template Section | Relevance to Prompt |
| :--- | :--- |
| 1. Executive Summary | OK -- "Rasputin is closest to Sejanus" |
| 2. Direct Comparison Matrix | Forced -- "Memory Model" and "Concurrency" columns make no sense for historical figures |
| 3. Structural Divergence | Good -- why each advisor arose |
| 4. **Code Contrast** | **Completely irrelevant** -- there is no code |
| 5. When to Switch | Nonsensical for historical comparison |

The Arena template's mandatory `Code Contrast` section forces the expander to either skip the section (violating template rules) or generate filler (reducing quality).

### Case 3: Template A (Deep Dive) applied to "Explain Stoic philosophy"

| Template Section | Relevance to Prompt |
| :--- | :--- |
| 1. Ontological Definition | OK -- define Stoicism |
| 2. Internal Mechanics (Under the Hood) | Forced -- philosophy doesn't have "control flow" or "data structures" |
| 3. Systems Context & Anchoring | Reasonable -- analogies work |
| 4. Edge Cases & Constraints | Awkward -- "when does Stoicism break?" is a valid question but "edge cases" is the wrong framing |

---

## Root Cause: Templates Are Section-Rigid, Not Principle-Flexible

Each template mandates **specific sections with specific names**. The expander either follows all sections (producing irrelevant filler) or skips sections (producing an incomplete template application). There is no middle ground.

### The Rigidity Spectrum

| Level | Description | Current State |
| :--- | :--- | :--- |
| **1. Rigid** | Fixed sections, fixed order, all mandatory | Templates A, B, C, E, F, G ← **we're here** |
| **2. Semi-flexible** | Fixed principles, suggested sections, optional depth | Template D partially |
| **3. Principle-driven** | Define the *goals* of each section, let LLM decide structure | **Not implemented** |
| **4. Freeform** | No template, persona axes only | Current freeform mode |

The jump from Level 1 (rigid) to Level 4 (no structure) is too large. There's no Level 2-3 option that says: "Here are the *principles* this expansion should follow -- organize the output however best serves the topic."

---

## The Adapted Mode Isn't Solving This

The expander has an "Adapted" mode that says "use the template as a skeleton, customize or skip sections." In theory this handles rigidity. In practice:

1. The LLM sees a template with 5 sections and defaults to following all 5
2. "Skip irrelevant sections" is a vague instruction -- the LLM doesn't know which are irrelevant
3. Even when it skips, it doesn't *replace* with topic-appropriate sections -- it just produces a shorter output
4. The template's *tone* still leaks through ("edge cases", "data structures", "code contrast")

Adapted mode trims the template. It doesn't reshape it.

---

## Proposed Fix: Principle-Based Templates

Instead of section-rigid templates, create **principle cards** -- short documents that define:
1. **What to accomplish** (not what sections to write)
2. **What makes this type of analysis good** (quality criteria)
3. **What to avoid** (anti-patterns)

### Example: Principle Card for "Comparison Analysis"

```markdown
# Comparison Principle

**Goal:** Help the reader understand WHY two things differ, not just HOW.

**Quality Criteria:**
- Must include a structured comparison (table, side-by-side, or matrix)
- Must explain the design philosophy or historical context behind each approach
- Must take a position -- state which is better in specific contexts
- Must include at least one concrete example that illustrates the key difference

**Anti-patterns:**
- Don't produce a comparison matrix with dimensions that don't apply to the subject
- Don't include "Code Contrast" for non-code topics
- Don't equivocate without specifying what the decision depends on

**Tone:** Opinionated analyst. Take sides, justify with evidence.
```

The LLM reads this card and structures the output however the topic demands:
- For Python vs Java → includes code, benchmarks, ecosystem comparison
- For Rasputin vs Richelieu → includes historical context, power dynamics, structural parallels
- Same principles, different structures

### Template Migration Path

| Current Template | Becomes | Covers |
| :--- | :--- | :--- |
| A (Deep Dive) | "Explanation" principle | Anything that needs explained (CS, science, philosophy) |
| B (Arena) | "Comparison" principle | Any comparison (tech, historical, literary) |
| C (Rosetta Stone) | Keep as-is | Language features only (narrow enough to stay rigid) |
| D (Chronograph) | "Narrative Analysis" principle | History, biography, events |
| E (Algorithmist) | Keep as-is | DSA only (narrow enough to stay rigid) |
| F (Debugger) | Keep as-is | Debugging only |
| G (Blueprint) | Keep as-is | System design only |
| H (Mathematician) | Keep as-is | Proofs only |
| I (Case Study) | "Case Analysis" principle | Any case study (tech, business, historical) |
| **NEW** | "Critical Reading" principle | Literary/art/film analysis |
| **NEW** | "Philosophical Inquiry" principle | Ethics, epistemology, thought experiments |

**Key insight:** CS-specific templates (C, E, F, G, H) are narrow enough that rigidity works. Broad templates (A, B, D, I) cover too many domains and need to become principle-based.

---

## Summary

The templates were designed for CS topics where structure is king -- every algorithm has complexity, every system has components, every language has syntax. But when these structures are applied to humanities, literature, or culture, they produce content that feels like a systems engineer analyzing art. The fix isn't more templates -- it's replacing broad templates with flexible principle cards that define *goals* instead of *sections*.
