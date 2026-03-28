# Fiqh Multi-Madhab Agent Architecture — Design Analysis

**Date:** 2026-03-27
**Status:** Proposal / Pre-Implementation
**Origin:** Design discussion synthesized from Claude Sonnet (Extended Thinking) + Kybernetes architectural review

---

## 1. The Proposal

A five-agent pipeline for answering questions in Islamic jurisprudence (fiqh):

1. **Four madhab advocacy agents** — each one inhabits a single school of legal thought: Hanafi, Maliki, Shafi'i, Hanbali. Each agent argues its school's position with proper classical references.
2. **One synthesizer agent** — unbiased fifth agent that reads all four arguments and produces a structured synthesis, including consensus points, divergence reasons, and a probabilistic conclusion.
3. **Persistent output** — all four arguments are kept alongside the synthesis so a human can draw independent conclusions.

This is a domain-specific multi-perspective pipeline, structurally distinct from every agent in the current system.

---

## 2. Why the Architecture is Correct

### 2.1 Fiqh is structurally multi-perspective

The four madhabs are not competing errors. They are legitimate methodological traditions that have recognized each other's validity for 1,200 years. A single-agent fiqh answer makes an invisible school selection. This architecture makes that selection explicit at every level. That is epistemically superior to any alternative.

### 2.2 Advocacy and synthesis require different cognitive postures

Conflating them — making the fourth agent also do synthesis — produces biased synthesis disguised as neutral. A separate synthesizer agent with a distinct principle card and explicit instruction to hold no school allegiance is the correct structural choice.

### 2.3 Preserving the four arguments is correct PKM design

The synthesis answers the question. The four arguments explain *why the question is hard*. In fiqh, the divergence map is often more valuable than the answer. A user who reads only the synthesis has lost structural knowledge about the tradition. Keeping all four outputs is consistent with the vault's philosophy of depth-over-convenience.

### 2.4 It maps onto an existing Kybernetes pattern

The current `@classifier → @domain_agent → stitch` pipeline already handles single-domain expansion. The madhab pipeline is a structured variant: `madhab_classifier → [4 × madhab_agent] → @fiqh_synthesizer → stitch`. The infrastructure (prepare_dispatch, write_expansion, stitch_files) works with any number of agents writing to block_id temp files. No new tooling primitives are required.

---

## 3. Critical Concerns Not Raised in the Claude Discussion

### 3.1 The Hallucination Risk is Categorically Different Here

This is the most serious concern in the entire architecture. In every other domain agent (Turing, Newton, Euler), a hallucinated claim is wrong but recoverable — a user can verify it. In fiqh, a hallucinated classical citation is structurally deceptive. If `@hanafi` writes:

> *"Ibn Abidin states in Radd al-Muhtar (vol. 3, p. 412) that..."*

...and that citation is fabricated, the output reads as authoritative scholarly discourse. A user without training cannot tell. The text has the grammar of expertise while being empty of it.

**This is not a minor bug. It is an architectural integrity failure.**

The Claude discussion identifies this but proposes only a "verification layer that flags uncertain citations." That is necessary but insufficient. The agents need stronger constraints at the prompt level:

- Agents MUST distinguish between: (a) definitive classical positions they are certain of, and (b) positions described at the school-level without a specific source.
- The agent instruction must include: *"If you cannot provide a verified citation, describe the school's methodological disposition and general ruling without fabricating a source. It is better to be honest about the limits of your knowledge than to hallucinate a reference."*
- The synthesis card must explicitly note: *"Citations marked [UNCERTAIN] in any of the four arguments must be flagged in the synthesis. Do not incorporate uncertain citations as evidence."*

This doesn't eliminate the risk — it creates a structural norm that makes the failure mode visible rather than invisible.

### 3.2 Fiqh Has an Internal Dimension Separate from Legal Rulings

All four madhabs and their synthesis are about *zahir* — the outward legal ruling. But fiqh in Wisdom sits adjacent to Al-Ghazali, who explicitly criticizes jurists who know the external ruling but have lost the *batin* — the inner wisdom behind it. The current proposal produces a legal analysis tool but not an integrative wisdom tool unless a sixth component is added.

**Recommendation:** The synthesizer principle card should include a Maqasid layer AND a Ghazalian reflection layer — not just "what is the ruling" but "what is the ruling protecting, and how does the disagreement illuminate the spirit of the law?" This is what makes it *Kybernetes* material rather than a generic fiqh chatbot.

### 3.3 Temporal and Classical/Contemporary Ambiguity

Many user queries will not be purely classical. Questions about:
- Digital finance (cryptocurrency, DeFi, digital contracts)
- Bioethics (organ donation, in vitro fertilization, gene editing)
- Social structures (women in workforce, modern family law)
- Technology (AI-generated art ownership, algorithmic trading)

...have no direct classical ruling. The madhab agents will be performing new analogical reasoning (*qiyas*), not citing settled law. This is epistemically different and must be labelled clearly.

**A mandatory distinction must be encoded in each agent's output:**

```
[CLASSICAL POSITION] — Direct ruling from the school's established literature.
[DERIVED POSITION] — New qiyas from classical principles applied to a modern case.
```

Conflating these destroys the intellectual honesty of the architecture.

### 3.4 The Classifier Problem

The existing `@classifier` routes prompts to a single domain agent. The fiqh pipeline requires a different entry condition: a prompt must be recognized as *requiring the madhab pipeline* rather than a single `@turing`-style expansion.

This raises a design question: does fiqh get its own top-level classifier branch, or is it a sub-domain of a new general `@iqbal` extension?

**Analysis:** Fiqh is not philosophy in the `@iqbal` sense — it is positive law. It requires its own entry pathway. The current classifier's domain table must be extended:

| Keywords | Domain | Pipeline |
| :--- | :--- | :--- |
| fiqh, madhab, halal, haram, zakat, salah, nikah, Islamic law, shariah ruling | `fiqh` | **Madhab Multi-Agent Pipeline** (not standard expansion) |

This requires a structural change to the `@classifier` agent definition — it must be able to return `"pipeline": "madhab"` as a routing signal, not just a single domain agent name.

### 3.5 Internal Disagreement Within Each School

Each madhab contains internal disagreements (*ikhtilaf*). The "Hanafi position" on a given question may have three valid internal opinions held by different generations of Hanafi jurists. Presenting one as *the* Hanafi position is already a simplification.

**Options:**

**Option A (Simple):** Each agent presents the dominant (*mu'tamad*) opinion of its school and explicitly labels it as such: *"The preponderant Hanafi ruling (*al-fatwa alayhi*) is..."*

**Option B (Rich):** Each agent presents the dominant position AND flags the most significant internal minority opinion if one exists. This doubles output depth but captures the true structure of the tradition.

**Recommendation:** Start with Option A. Add Option B as a `@deep` directive variant: `{{@deep What is the ruling on X?}}` triggers full internal diversity; standard `{{What is the ruling on X?}}` triggers dominant-only.

### 3.6 The Ja'fari Question

Claude raises this cleanly. If the vault ever engages with questions where Sunni-Shia legal difference is material — and it will, because many fiqh questions are politically, historically, and theologically charged in exactly this dimension — excluding the Ja'fari tradition produces a structurally incomplete picture while presenting itself as comprehensive.

**Recommendation:** Design the architecture for five madhab agents from the start, with Ja'fari as optional/on-demand. The synthesizer should note when it was invoked without the Ja'fari perspective. Do not bake in Sunni-only assumptions invisibly.

### 3.7 The Synthesizer's Instruction Set is the Hardest Engineering Problem

This deserves its own section because underspecifying the synthesizer card will produce exactly what Claude warns against — confident verdicts on contested questions, majority-position bias dressed as neutral synthesis.

The synthesizer card must explicitly instruct:

1. **Consensus identification:** Only label something as "consensus" if all four (or five) agents agree. Majority (3/4) is "preponderant position," not consensus.
2. **Reasoning vs. ruling divergence:** The schools sometimes agree on a *ruling* but diverge on the *reason*. This distinction is jurisprudentially significant and must be noted explicitly.
3. **Methodological divergence flagging:** When schools disagree because of different methodological commitments (e.g., Hanafi's heavier use of qiyas vs. Hanbali's textualism), this is not an error to resolve — it is a fundamental feature of the tradition. The synthesizer must say so.
4. **Probabilistic language enforcement:** The synthesizer is banned from writing "the correct ruling is X." It must write "the preponderant position," "the strongest argument on balance," or "genuine disagreement with no clear resolution." These are the terms actual fuqaha use.
5. **Maqasid evaluation:** Every synthesis must include an evaluation through the five objectives: *Hifz al-Din* (religion), *Nafs* (life), *Aql* (intellect), *Nasl* (lineage), *Mal* (property). Which objective is this ruling protecting? Does the divergence reflect different weightings of these objectives?
6. **Ghazalian reflection:** What is the *spirit* behind this area of law? What human problem is it solving? This is what graduates the output from legal table to Kybernetes knowledge.

---

## 4. Fit Within Current Kybernetes Architecture

### 4.1 What Needs to Exist

| Component | Status | Notes |
| :--- | :--- | :--- |
| `@hanafi` agent | New | Advocacy agent, madhab-specific voice and tool access |
| `@maliki` agent | New | Same |
| `@shafii` agent | New | Same |
| `@hanbali` agent | New | Same |
| (Optional) `@jafari` agent | New | Ja'fari school; off by default |
| `@fiqh_synthesizer` agent | New | The hardest principle card to write |
| `madhab_pipeline` skill | New | Orchestrates the 4/5 → 1 flow |
| `/os:fiqh {question}` command | New | Entry point slash command |
| Classifier extension | Modification | Add `fiqh` domain + `pipeline: madhab` routing |
| `fiqh_synthesizer` card | New | The principle card for controlled synthesis |

### 4.2 What Can Be Reused Without Modification

- `write_expansion` tool — temp file writing per block_id works identically
- `stitch_files` tool — stitching 4+ temp files into a source note works identically
- `word_count` tool — verification step unchanged
- `read_note` tool — agents can read context from the vault as needed

### 4.3 Where the Model Deviates from Standard Expansion

Standard expansion: `1 block → @classifier → 1 domain agent → 1 temp file → stitch`

Madhab pipeline: `1 block → fiqh classifier branch → 4 agents (parallel?) → 4 temp files → @fiqh_synthesizer → synthesis temp file → stitch all 5 into structured output`

The key deviation is **parallel dispatch**. The four madhab agents are independent — they do not need each other's output. This is different from the two-pass system where Pass 2 depends on Pass 1. If the system supports parallel agent dispatch, madhab agents should run concurrently. If not, sequential dispatch with progress logging is acceptable.

### 4.4 The Output Note Structure

Each fiqh question that passes through the pipeline should produce a note with this structure:

```markdown
---
tags:
  - field/humanities
  - subject/fiqh
  - concept/{atomic-ruling-topic}
---
# Ruling: {Question}
[[T.O.C (Fiqh Notes)|Up to Fiqh]]

**Question:** {exact user query}
**Query Type:** [Classical / Derived / Mixed]
**Schools Consulted:** Hanafi · Maliki · Shafi'i · Hanbali [· Ja'fari]

---

## Hanafi Position
> [!NOTE] Methodological Disposition: Rationalist. Heavy qiyas. Istihsan preference.
{@hanafi expansion — dominant ruling, key classical reference (verified/uncertain), brief usul reasoning}

## Maliki Position
> [!NOTE] Methodological Disposition: Empiricist. Medinan practice. Maslaha as source.
{@maliki expansion}

## Shafi'i Position
> [!NOTE] Methodological Disposition: Systematic textualist. Al-Shafi'i's own usul as foundation.
{@shafii expansion}

## Hanbali Position
> [!NOTE] Methodological Disposition: Hadith literalism. Maximum skepticism of rational extrapolation.
{@hanbali expansion}

---

## Synthesis
{@fiqh_synthesizer output — consensus/divergence map, maqasid evaluation, probabilistic conclusion, Ghazalian reflection}
```

This structure is the permanent artefact. A human can read any layer independently.

---

## 5. Open Questions for Decision

1. **Parallel vs. sequential dispatch** — can the current orchestrator invoke four agents concurrently, or must they be sequential? If sequential, what is the acceptable latency per question?

2. **Ja'fari from the start or added later?** — A five-agent architecture built from the beginning is cleaner than retrofitting a fifth agent. But it increases initial complexity. Decision needed before implementation.

3. **Internal school diversity (Option A vs B)** — Dominant-only vs. dominant + minority. Whether to make this a directive parameter (`@deep`) or always-on.

4. **Where does fiqh live in the vault?** — Options:
   - `10_University/Semester_X/Islamic Studies/Notes` (course-specific)
   - `20_CS_Core` equivalent — a new `30_Knowledge_Base/Fiqh` partition
   - Inside `30_Knowledge_Base` with tags `#field/humanities #subject/fiqh`
   - A dedicated top-level `15_Fiqh` folder (breaks PARA structure, not recommended)
   
   **Recommendation:** `30_Knowledge_Base/10_Concepts` for individual rulings, `30_Knowledge_Base/00_Atlas` for the MOC hub, consistent with the existing KDB architecture. Fiqh is not university-specific — it is permanent knowledge.

5. **Citation verification tool** — does one need to be built, or is the "flag uncertain" norm in the agent prompt sufficient for the initial version?

---

## 6. Priority vs. Current Roadmap

The current active work is the Two-Pass expansion system and Surgeon decomposition. The madhab architecture is a significant new feature that should not interrupt this. Suggested sequencing:

1. Complete Two-Pass + Surgeon stabilization (current work).
2. Decide the five open questions above.
3. Write principle cards for all four/five madhab agents + the synthesizer.
4. Implement the `madhab_pipeline` skill.
5. Extend `@classifier` with fiqh routing.
6. Add `/os:fiqh` command.
7. Test with 3-5 representative questions (a classical question, a contemporary qiyas question, and a genuinely contested one where schools diverge sharply).

---

## 7. The Deeper Value — Why This Is Worth Building

Claude stated this clearly and it is worth reinforcing: this architecture does something no existing Islamic knowledge tool does. It makes the *structure of legitimate disagreement* visible. A user who reads the output of this pipeline does not just get an answer — they get a map of how 1,200 years of scholarship has engaged with the question. The divergence *is* the knowledge.

More broadly, this could become a template for any domain where legitimate expert disagreement is structurally inherent — political philosophy, bioethics, economics, constitutional interpretation. The madhab pipeline is the general pattern; fiqh is the first instantiation of it.

Inside Kybernetes, this also begins to fulfill the `@polymath` agent's deepest potential. When the synthesizer's Maqasid evaluation notes that the Hanafi preference for *maslaha* (public interest) maps onto Rawlsian justice, or that the usul al-fiqh problem of weighing conflicting hadith is structurally identical to Popper's falsificationism — those connections become entry points for `@polymath` synthesis. The fiqh notes become nodes in the vault graph that cluster with philosophy, epistemology, and social science. That cross-domain richness is the payoff.

---

*This document should be revisited after the Two-Pass system is stable. At that point, the principle card drafting for the madhab agents is the first concrete implementation step.*
