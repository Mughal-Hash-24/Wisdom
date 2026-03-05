# Blueprint: Multi-Domain Expansion Architecture v3

**Filed:** 2026-03-04
**Status:** Explorable Ideas -- not a final implementation plan
**Prerequisite Reading:** `Persona_NonCS_Diagnostic.md`, `Template_Rigidity_Diagnostic.md`

---

## The Problem in One Sentence

The expansion system was designed by a CS student, for CS content, and it shows: every non-CS expansion gets squeezed through engineering frameworks that strip away voice, narrative, and aesthetic engagement.

---

## Idea 1: The Three-Layer Architecture

Replace the current binary system (template OR freeform) with three composable layers that the expander assembles per-prompt:

```
Layer 1: DOMAIN LENS    → What world are we in? (Technical, Humanistic, Scientific, Creative)
Layer 2: ANALYSIS MODE   → What are we doing? (Explaining, Comparing, Narrating, Critiquing, Proving)
Layer 3: VOICE PROFILE   → How should it sound? (Clinical, Narrative, Polemical, Pedagogical, Lyrical)
```

The expander picks one from each layer and combines them. This creates a matrix of possibilities:

| Prompt | Domain | Mode | Voice |
| :--- | :--- | :--- | :--- |
| "Explain Virtual Memory" | Technical | Explaining | Clinical |
| "Compare Rasputin to Richelieu" | Humanistic | Comparing | Narrative |
| "Critique women in The Godfather" | Creative | Critiquing | Polemical |
| "Prove the Fundamental Theorem of Calculus" | Scientific | Proving | Pedagogical |
| "How did Spotify build Discover Weekly?" | Technical | Narrating | Clinical |

**Why this works:** Current system has 9 rigid templates. This system produces `4 × 5 × 5 = 100` combinations from just 14 small definition files. And any combination can emerge naturally -- you don't need a "Template J for literary criticism."

**Exploration needed:** Define the actual lenses, modes, and voice profiles. Test whether the LLM can reliably combine three instructions without confusion.

---

## Idea 2: Principle Cards (Replace Section-Rigid Templates)

Research confirms that "Dynamic Hierarchical Outlining" -- where the structure adapts during generation rather than being fixed upfront -- produces significantly better long-form content. The current templates violate this by locking structure before the LLM even reads the prompt.

**Principle Card format:**

```markdown
# [Analysis Mode Name]

## Goal
What this analysis type is supposed to accomplish. One sentence.

## Quality Signals (what good looks like)
- Bullet list of 4-5 observable qualities in excellent output
- The LLM targets these, not fixed sections

## Anti-Patterns (what to avoid)
- Bullet list of 3-4 things that make output bad
- Specific to this analysis type

## Voice Guidance
- 2-3 sentences on tone, perspective, and engagement style
- Specific examples of good phrasing vs generic phrasing
```

**Example: "Critiquing" Principle Card:**

```markdown
# Critiquing

## Goal
Evaluate a work (text, system, art, argument) by examining its choices, strengths, blind spots, and implications.

## Quality Signals
- Uses specific evidence FROM THE WORK (quotes, scenes, code, data) -- not just assertions
- Takes a clear interpretive position and defends it
- Acknowledges the strongest counter-arguments before dismissing them
- Connects the specific work to broader themes or traditions
- The reader finishes with a sharper understanding than they started with

## Anti-Patterns
- DO NOT just summarize the work and call it analysis
- DO NOT apply frameworks that don't fit (game theory on poetry, timeline tables on character arcs)
- DO NOT hedge every claim with "it depends" -- commit to an interpretation
- DO NOT write like a textbook -- this is criticism, not a report

## Voice Guidance
Write like a sharp, well-read reviewer who respects the work but isn't afraid to challenge it. 
Use "I" sparingly but don't hide behind passive voice. Name the specific choices the creator made 
and interrogate WHY. If something is brilliant, say it's brilliant and explain why. If something 
fails, say it fails and explain the structural reason.
```

**Why this works:** The LLM reads the card and generates whatever structure serves the topic. For The Godfather's women, it might produce "Constraint as Character Design → The Kay-Connie Spectrum → Apollonia: Fantasy vs Reality → What Puzo Gets Right → What He Doesn't." For Rasputin, entirely different headings. Same quality principles, different structures.

**Keep rigid templates for narrow domains:** Templates C (Rosetta Stone), E (Algorithmist), F (Debugger), G (Blueprint), H (Mathematician) stay as-is. Their domains are narrow enough that rigid sections add value (code blocks, complexity tables, visual traces).

---

## Idea 3: Voice Profiles with "Burstiness" Directives

Research shows AI struggles with humanities because it produces uniform sentence lengths and predictable word choices (low "burstiness" and "perplexity"). Human writing varies wildly -- short punchy sentences next to long flowing ones. AI defaults to medium-everything.

**Fix: Add explicit burstiness directives to voice profiles:**

```markdown
# Narrative Voice Profile

## Sentence Rhythm
Vary sentence length deliberately. Follow a long analytical sentence with a short declarative one. 
Use fragments for emphasis. Like this. Then expand again into a full complex sentence that builds 
the argument across multiple clauses before landing on the point.

## Word Choice
Avoid the AI default register (utilize, facilitate, leverage, implement, comprehensive, robust). 
Use concrete, specific, vivid language. Not "he gained significant influence" but "he had the 
Empress's ear, and through her, the Tsar's signature."

## Engagement Hooks
Start paragraphs with something unexpected -- a question, a contradiction, a vivid detail. 
NOT "In this section, we will examine..." but "The ambulance broke down on the road from the 
airport. The most powerful man in Pakistan lay in the back, dying."
```

**Why this works:** These directives are domain-agnostic. They make ANY content more engaging. But they particularly fix the humanities problem where the content is inherently narrative but the AI writes it like a technical report.

---

## Idea 4: Exemplar-Driven Persona Calibration

Instead of abstract mandates ("trace root causes"), give each persona a **gold-standard example** of what their output should sound like. The LLM pattern-matches against examples far more reliably than it follows abstract instructions.

**For the Historian:**

```markdown
## Gold Standard (what your output should sound like)

"Rasputin arrived in St. Petersburg in 1903 with nothing but a reputation and a stare 
that unsettled everyone who met him. The city's spiritual salon circuit -- desperate for 
authentic mystics in an age of manufactured spirituality -- received him like a gift. But 
Rasputin's real genius wasn't spiritual. It was political. He understood, perhaps better 
than any aristocrat, that power flows through the person closest to the decision-maker's 
pain. And the Tsarina's pain had a name: Alexei."
```

**For the Generalist (literary analysis):**

```markdown
## Gold Standard

"Puzo gives Kay Adams exactly one moment of genuine agency in the entire novel -- and 
then he closes the door on it. Literally. The final image of Kay kneeling in church while 
Michael's office door shuts is not subtle, but it doesn't need to be. What's interesting 
is that Puzo seems aware of what he's doing. He doesn't frame Kay's exclusion as natural 
or comfortable. He frames it as the price. The question is whether Puzo is critiquing 
patriarchy or simply documenting it, and the novel never fully commits to either."
```

**Why this works:** A 100-word example communicates more about voice, tone, and personality than 500 words of mandates. The LLM reads it and thinks "oh, THAT's what we're going for."

---

## Idea 5: Domain-Aware Enrichment Axes

Replace the current flat enrichment axes with domain-sensitive ones that activate based on the detected topic:

**Current (flat):**
```
Historian axes: root causes, timeline, systemic impact, parallels
→ Same axes for "Fall of Rome" and "Women in The Godfather"
```

**Proposed (domain-sensitive):**
```yaml
Historian:
  political_history: [power dynamics, institutional decay, key actors, competing narratives]
  cultural_history: [social norms, art/literature as evidence, lived experience, identity]
  military_history: [strategy, logistics, terrain, technology, morale]
  intellectual_history: [ideas in context, transmission, reception, legacy]

Generalist:
  literary_analysis: [close reading, character motivation, thematic patterns, authorial choices, textual evidence]
  philosophical: [thought experiment, counterargument, lived implications, historical precedent]
  cultural_criticism: [aesthetic engagement, medium-specific analysis, context, influence, reception]
```

The expander detects which sub-domain applies and selects the relevant axes. "Fall of Rome" gets `political_history` axes. "Women in The Godfather" gets `literary_analysis` axes.

**Why this works:** The enrichment step is where freeform prompts get expanded before generation. If the axes are domain-relevant, the expanded prompt naturally produces better content. Current axes force historical analysis on everything.

---

## Idea 6: The Persona Personality Matrix

Currently each persona has mandates (what to do) but no personality (how to be). Add a personality matrix:

| Trait | Chief Engineer | Historian | Economist | Psychologist | Critic |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Opens with** | Definition | A scene or moment | A number or contradiction | A puzzle about behavior | A provocative claim |
| **Persuades via** | Diagrams + code proof | Narrative + primary sources | Data + incentive analysis | Studies + evolutionary logic | Textual evidence + interpretation |
| **Tone** | Precise, surgical | Vivid, storytelling | Opinionated, data-driven | Curious, explains the irrational | Sharp, intellectually combative |
| **Signature move** | "Under the hood, what actually happens is..." | "But what nobody saw coming was..." | "The second-order effect was..." | "The evolutionary reason for this is..." | "What's really going on here is..." |
| **Avoids** | Vague hand-waving | Dry chronology | Qualitative mush | Moralizing | Fence-sitting |

Each persona's "signature move" and "opens with" create a fingerprint. You can identify which persona wrote a piece without being told.

---

## Implementation Priority

| Idea | Impact | Effort | Verdict |
| :--- | :--- | :--- | :--- |
| 4. Exemplar calibration | Highest | Lowest (just write examples) | **Do first** |
| 6. Personality matrix | High | Low (add to GEMINI.md) | **Do second** |
| 3. Burstiness directives | High | Low (add to voice profiles) | **Do third** |
| 2. Principle cards | High | Medium (rewrite broad templates) | **Do fourth** |
| 5. Domain-aware axes | Medium | Medium (restructure enrichment) | **Do fifth** |
| 1. Three-layer architecture | Highest (long-term) | High (full rearchitect) | **Explore last** |

---

## What NOT to Do

- **Don't add more rigid templates.** The problem isn't "not enough templates" -- it's that templates constrain structure. Adding Template J, K, L just creates more boxes to force content into.
- **Don't over-specify.** Every line of instruction is a line the LLM might misinterpret. The exemplar approach (Idea 4) communicates more with less.
- **Don't separate "CS brain" from "humanities brain."** The system should be one coherent personality that *shifts register* depending on the domain, not two separate brains.
