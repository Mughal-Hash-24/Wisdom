# Fiqh Multi-Madhab Pipeline — Revised Specification

**Date:** 2026-03-28 (v4 — full source context + agent identity restructure)
**Status:** Approved Design / Pre-Implementation
**Supersedes:** `Fiqh_Madhab_Agent_Architecture.md`

---

## 1. Finalized Decisions

| Question | Decision |
| :--- | :--- |
| Parallel vs. sequential dispatch | **Parallel** — all 4 madhab agents run concurrently |
| Ja'fari school inclusion | **Excluded** — 4 Sunni schools only |
| Internal school diversity | **Option B** — dominant ruling + most significant internal minority opinion |
| Vault location | **`30_Knowledge_Base/Fiqh/`** — new dedicated partition inside the KDB |
| Citation verification tooling | **Agent prompt norm is sufficient** for v1 |
| Relation to `/os:sort` | **Completely separate pipeline** — this command never routes through inbox-sort |

---

## 2. Architecture Overview

The Fiqh pipeline is a standalone, question-driven multi-agent system. It is invoked exclusively via `/os:fiqh "{question}"`. It does not touch `00_Inbox`, does not use `@classifier`, and has no connection to the expansion pipeline.

```
User: /os:fiqh "What is the ruling on X?"
        |
        v
[madhab_pipeline SKILL]
        |
        |-- [Classify Q type: Classical / Derived / Mixed]
        |
        |-- Spawn 4 agents IN PARALLEL, each writes to a temp file:
        |       @hanafi   --> _fiqh_hanafi_{slug}.md
        |       @maliki   --> _fiqh_maliki_{slug}.md
        |       @shafii   --> _fiqh_shafii_{slug}.md
        |       @hanbali  --> _fiqh_hanbali_{slug}.md
        |
        |-- Wait for all 4 to complete. Verify via word_count.
        |
        |-- Spawn @fiqh_synthesizer with:
        |       - The 4 temp file paths
        |       - The question
        |       - The synthesis principle card
        |   --> writes: _fiqh_synthesis_{slug}.md
        |
        |-- Orchestrator adds back-links:
        |       - Synthesis file already contains wikilinks TO each madhab file
        |       - Orchestrator patches each of the 4 madhab files to add a link BACK to synthesis
        |
        |-- Move all 5 files to: 30_Knowledge_Base/Fiqh/{slug}/
        |
        |-- Update T.O.C (Fiqh).md with a new entry
        |
        v
[DONE] 5 files in vault. Fully cross-linked. T.O.C updated.
```

---

## 3. Vault Structure

### 3.1 Folder Layout

```
D:\WISDOM\Kybernetes\
└── 30_Knowledge_Base\
    └── Fiqh\
        ├── T.O.C (Fiqh).md                         ← Hub for all questions
        ├── {question-slug-1}\
        │   ├── Synthesis - {question-slug-1}.md     ← Primary entry point
        │   ├── Hanafi - {question-slug-1}.md
        │   ├── Maliki - {question-slug-1}.md
        │   ├── Shafii - {question-slug-1}.md
        │   └── Hanbali - {question-slug-1}.md
        └── {question-slug-2}\
            └── ...
```

The `{slug}` is a file-safe, lowercased, hyphenated abbreviation of the question derived by the skill before any agents are dispatched. Example: "What is the ruling on gold jewelry for men?" → `gold-jewelry-men`.

### 3.2 Atlas Link

`30_Knowledge_Base/00_Atlas/` must contain an entry to `T.O.C (Fiqh).md`. During pipeline setup (Step 0 of the skill), the orchestrator calls `ensure_toc_link` on the Atlas hub to add:

```
- [[T.O.C (Fiqh)|Fiqh — Islamic Jurisprudence]]
```

This is a one-time operation executed only if the link doesn't already exist.

### 3.3 T.O.C (Fiqh).md Format

```markdown
---
tags:
  - type/map
  - field/humanities
  - subject/fiqh
---
# T.O.C (Fiqh)

Islamic jurisprudence. Four madhab perspectives with synthesis. Each entry links to the synthesis note for that question; navigate from there to individual school positions.

[[30_Knowledge_Base/00_Atlas|Up to Atlas]]

---

## Questions

- [[Synthesis - {slug-1}|{Full question text 1}]]
- [[Synthesis - {slug-2}|{Full question text 2}]]
```

New entries are appended chronologically.

---

## 4. The Five Output Files

Each fiqh question produces exactly five permanent files.

### 4.1 Madhab Files (× 4)

Each madhab agent writes one file. Structure is identical across all four — only the school's name and content differ.

```markdown
---
tags:
  - field/humanities
  - subject/fiqh
  - concept/{atomic-ruling-topic}
---
# Hanafi Position: {Full Question}
[[T.O.C (Fiqh)|Up to Fiqh]] | [[Synthesis - {slug}|View Synthesis]]

**School:** Hanafi
**Methodological Disposition:** Rationalist. Heaviest use of analogical reasoning (*qiyas*) of all four schools. Preference for *istihsan* (juristic preference) when strict analogy produces inequitable results. Founded by Abu Hanifa (d. 767), dominant in Turkey, Central Asia, South Asia.
**Query Type:** [CLASSICAL POSITION / DERIVED POSITION / MIXED]

---

## Ruling

[The dominant (*mu'tamad*) Hanafi position on this question. Clear, unambiguous statement of the ruling first — permissible, impermissible, obligatory, recommended, disliked, or neutral.]

**Classical Reference:** [Source title, author — mark as (VERIFIED) or (UNCERTAIN). Never fabricate. If source unknown, omit rather than invent.]

---

## Usul al-Fiqh — How This Ruling Was Derived

This section explains the methodology behind the ruling, not just the ruling itself.

**Primary Legal Source:** [Quran / Sunnah / Ijma / Qiyas — select one primary source]

**Derivation Chain:**

*If Quran:*
- **Verse:** [Surah Name] (Q X:Y) — "{relevant portion}"
- **Asbab al-Nuzul (Context of Revelation):** [The circumstances under which this verse was revealed — the event, the audience, the situation. If the asbab are not well-established or multiple accounts exist, state that explicitly.]
- **Textual Analysis:**
  - *Muhkam or Mutashabih:* [Is this verse clear in its ruling (*muhkam*) or open to interpretation (*mutashabih*)?]
  - *Amm or Khass:* [Is the verse general (*amm* — applicable broadly) or particular (*khass* — specific to a group, time, or occasion)?]
  - *Nasikh/Mansukh:* [Does this verse abrogate an earlier ruling, or is it itself abrogated by a later one? State explicitly even if the answer is "no abrogation applies here."]
- **Juristic Reading:** [How this school applies this verse given the above context. The interpretation is the school's position, not objective truth — state it as such.]

*If Sunnah:*
- **Hadith:** "{gist of hadith}" — narrated by {Companion}, reported in {Collection} (VERIFIED / UNCERTAIN)
- **Authentication Status:** [Sahih / Hasan / Da'if — note if schools disagree on authenticity, since a hadith one school treats as sahih another may consider weak, and this is a direct source of ruling divergence]
- **Asbab al-Wurud (Context of the Hadith):** [The circumstances in which the Prophet said or did this — to whom, in what situation, was it a general pronouncement or a response to a specific person/event? A hadith addressed to one person in a specific situation cannot be automatically generalized to all cases.]
- **Scope:** [Does this school treat the hadith as *aam* (general — applicable to all Muslims in all circumstances) or as specific to its occasion? This determines how broadly the ruling extends.]
- **Application:** [How this hadith establishes the ruling for this school, given the above authentication and context]

*If Ijma:*
- **Consensus Body:** [Which generation of scholars — Companions (*Sahaba*), Successors (*Tabi'un*), later jurists]
- **Period:** [Approximate era]
- **Scope:** [Is this ijma universal across all schools, or specific to this school's tradition?]
- **Note:** [Is the claim of ijma itself contested? If so, by whom?]

*If Qiyas:*
- **Original Case (*Asl*):** [The established case with a clear ruling]
- **New Case (*Far'*):** [The question being ruled on]
- **Effective Cause (*Illah*):** [The connecting principle — why these two cases are analogous]
- **Extended Ruling (*Hukm*):** [The ruling carried from the original case to the new case]
- **Why This Illah:** [The school's justification for accepting this particular illah as valid]

**Usul-Level Disputes:**
[Where do the other schools diverge from this derivation — not necessarily the ruling itself, but the *method*? e.g., "The Hanbali school rejects this qiyas on the grounds that the illah is speculative; the Maliki school accepts a different illah that leads to the same ruling via a different path." This is the layer where inter-school disagreement is most intellectually substantive.]

---

## Internal Dissent

[The most significant minority opinion *within* the Hanafi school, attributed to its scholar, with the reason for divergence — particularly if it stems from a different usul reading. If no significant minority exists, state: "No significant internal dissent on this question."]

---

## Notes

[Optional: historical context of the ruling's development, geographical variation in application, or notable modern applications of this ruling.]
```

### 4.2 Synthesis File (× 1)

This is the primary entry point. A human reading only the synthesis gets the full picture; a human who wants depth navigates to individual files.

```markdown
---
tags:
  - type/map
  - field/humanities
  - subject/fiqh
  - concept/{atomic-ruling-topic}
---
# Ruling: {Full Question Text}
[[T.O.C (Fiqh)|Up to Fiqh]]

**Question:** {exact user query}
**Query Type:** [Classical / Derived / Mixed]
**Date:** {YYYY-MM-DD}

---

## School Positions

| School | Ruling | Reasoning Basis | Certainty |
| :--- | :--- | :--- | :--- |
| [[Hanafi - {slug}\\|Hanafi]] | {one-line ruling} | {primary usul source} | [Verified / Uncertain] |
| [[Maliki - {slug}\\|Maliki]] | {one-line ruling} | {primary usul source} | [Verified / Uncertain] |
| [[Shafii - {slug}\\|Shafi'i]] | {one-line ruling} | {primary usul source} | [Verified / Uncertain] |
| [[Hanbali - {slug}\\|Hanbali]] | {one-line ruling} | {primary usul source} | [Verified / Uncertain] |

---

## Consensus & Divergence

**Consensus:** [What all four schools agree on, if anything. Only use "consensus" when all four agree. Three out of four is "preponderant" not consensus.]

**Divergence Map:** [Why the schools diverge. Categorize: is this a ruling divergence, a reasoning divergence, or a methodological divergence? A methodological divergence — e.g., Hanbali textualism vs. Hanafi rationalism — is a feature of the tradition, not an error to resolve.]

**Internal Dissent:** [Any notable minority positions within a school that are relevant to the broader picture]

---

## Maqasid Evaluation

Which of the five foundational objectives (*maqasid al-shariah*) is this ruling protecting?

| Objective | Relevance |
| :--- | :--- |
| *Hifz al-Din* — Protection of Religion | {relevant / not directly relevant — brief note} |
| *Hifz al-Nafs* — Protection of Life | {relevant / not directly relevant} |
| *Hifz al-Aql* — Protection of Intellect | {relevant / not directly relevant} |
| *Hifz al-Nasl* — Protection of Lineage | {relevant / not directly relevant} |
| *Hifz al-Mal* — Protection of Property | {relevant / not directly relevant} |

Does the divergence between schools reflect different weightings of these objectives?

---

## Synthesis Conclusion

[Probabilistic, honest conclusion. BANNED phrase: "the correct ruling is X." Required language: "the preponderant position," "the strongest argument on balance," "genuine disagreement with no clear resolution." The synthesizer does not issue fatwas. It maps the intellectual tradition's honest internal debate and gives the reader a principled basis for their own judgment.]

---

## Spirit of the Law

[A Ghazalian reflection: What human problem is this area of law solving? What does the disagreement between schools illuminate about the *spirit* behind the ruling, separate from the letter? This section explicitly connects to Al-Ghazali's critique of jurists who know the rule but have lost the wisdom behind it. Keep this to 2-3 paragraphs, dense but not laboured.]

---

## Personal Reflection

[Optional, user-filled: space for personal notes, conclusions drawn, or questions raised after reading the synthesis. Left blank by the pipeline.]
```

---

## 4a. Handling the Four Legal Sources

This is the most important structural question in the pipeline: fiqh derives rulings from four sources, each with different epistemological weight and different hallucination risk profiles. Every madhab agent must explicitly identify which source drives its ruling, and must handle that source according to the rules below.

### Quran

**Hallucination Risk:** Low. Quranic text is canonical and widely memorized. Verse content is generally reliable; verse numbering is the main risk point.

**Agent Handling:**
- Cite by Surah name and verse number: `[Surah Al-Baqarah] (Q 2:219)`. If uncertain of the exact verse number, omit it rather than guess.
- Cover **Asbab al-Nuzul** (context of revelation): what event or situation prompted this verse? If multiple accounts exist or the asbab is disputed, say so. If no asbab is recorded, state "no specific occasion of revelation recorded."
- Perform **textual analysis** on three axes:
  - *Muhkam/Mutashabih*: is the verse's meaning clear or ambiguous?
  - *Amm/Khass*: is it a general ruling or specific to a particular group or occasion?
  - *Nasikh/Mansukh*: does it abrogate a prior ruling or is it itself abrogated? This must always be addressed — abrogation silently changes everything if ignored.
- The verse text is objective; the school's *juristic reading* is the school's position. These must never be conflated.

### Sunnah (Hadith)

**Hallucination Risk:** Highest of the four. Specific hadith references (volume, page, hadith number, narrator chains) are frequently fabricated by LLMs in a way that reads as authoritative. This is the most dangerous failure mode in the entire architecture.

**Agent Handling:**
- Cite by: Collection name, primary narrator (Companion), and gist — e.g., *"The Prophet is reported to have said '{gist}', narrated by {Companion} in {Collection}"*
- Authenticity grade (*Sahih / Hasan / Da'if*) from this school's perspective. Note inter-school disputes: a hadith one school treats as sahih another may consider weak — this is a primary engine of ruling divergence.
- Mark all hadith citations `(VERIFIED)` or `(UNCERTAIN)`. Default to `(UNCERTAIN)` when not fully confident. If no specific hadith can be cited, describe the *class* of evidence ("multiple hadiths establish the principle that...") — never fabricate a specific report.
- Cover **Asbab al-Wurud** (context of the hadith): to whom was it said, in what situation, was it a general statement or a response to a specific person/event? A ruling given in a specific situation cannot be automatically universalized.
- Determine and state the hadith's **scope**: does this school treat it as *aam* (general, applicable to all) or specific to its occasion? The scope determination is itself a juristic position, not a fact.

### Ijma (Scholarly Consensus)

**Hallucination Risk:** Medium. "Scholars agree" is a claim that is itself frequently contested in fiqh. The agent must not assert ijma casually.

**Agent Handling:**
- Specify the *generation* of the consensus: Companions (*Sahaba*), Successors (*Tabi'un*), or later classical jurists
- Specify the approximate era
- Explicitly note if the claim of ijma is itself disputed — in fiqh, claiming ijma on a contested question is a jurisprudential move, not a neutral fact
- Ijma among all four schools (if it exists) is noted in the synthesis, not in individual madhab files — individual files note only this school's view on when consensus was reached

### Qiyas (Analogical Reasoning)

**Hallucination Risk:** Low — qiyas is logical reasoning, not a factual citation. But the agent must be explicit about the *illah* (effective cause), because different schools accepting different illah definitions is the primary engine of methodological divergence.

**Agent Handling:**
All four components must be stated explicitly:

| Component | Arabic Term | What to Write |
| :--- | :--- | :--- |
| Original case | *Asl* | The established case whose ruling is known |
| New case | *Far'* | The question being ruled on |
| Effective cause | *Illah* | The shared property that connects old to new |
| Extended ruling | *Hukm* | The ruling carried across from asl to far' |

The agent must also explain *why the school accepts this illah as valid* — because illah validity is where schools diverge most. The Hanafi school uses a broader criteria for valid illah than the Hanbali school; this is not arbitrary — it reflects Abu Hanifa's rationalist vs. Ibn Hanbal's textualist usul commitments.

### Source Hierarchy and Mixed Cases

The four sources have a classical hierarchy: Quran > Sunnah > Ijma > Qiyas. A ruling supported by multiple sources must cite the highest-order source as primary and note supporting sources below. A ruling with no Quranic or Sunnah basis that rests entirely on qiyas must be labelled `[DERIVED POSITION]` regardless of the school's confidence in the analogy.

---

## 5. The `madhab_pipeline` Skill — Step-by-Step

### Step 0: Initialization

1. Derive the `{slug}` from the question: lowercase, hyphenated, max 5 words.
2. Check if `30_Knowledge_Base/Fiqh/T.O.C (Fiqh).md` exists. If not, create it with the structure defined in §3.3.
3. Call `ensure_toc_link` on `30_Knowledge_Base/00_Atlas/` to add the Fiqh T.O.C link (idempotent).
4. Classify the question type: **Classical** (settled ruling exists in classical literature) / **Derived** (no classical ruling, new qiyas required) / **Mixed** (partially settled, partially novel). Log this classification — it will be passed to all agents.

**Log:**
```
[INIT] Question: "{question}"
[INIT] Slug: {slug}
[INIT] Type: {Classical / Derived / Mixed}
```

### Step 1: Parallel Dispatch

Dispatch all four agents **simultaneously**:

```
@hanafi  ← (question, slug, query_type, school="Hanafi", disposition=<see §6>)
@maliki  ← (question, slug, query_type, school="Maliki", disposition=<see §6>)
@shafii  ← (question, slug, query_type, school="Shafi'i", disposition=<see §6>)
@hanbali ← (question, slug, query_type, school="Hanbali", disposition=<see §6>)
```

Each agent is instructed to write its output to a temp file named `_fiqh_{school}_{slug}.md` via `write_expansion` (block_id = `fiqh_{school}_{slug}`).

**Log (after all complete):**
```
[MADHAB] @hanafi  → _fiqh_hanafi_{slug}.md  ({N} words) ✓
[MADHAB] @maliki  → _fiqh_maliki_{slug}.md  ({N} words) ✓
[MADHAB] @shafii  → _fiqh_shafii_{slug}.md  ({N} words) ✓
[MADHAB] @hanbali → _fiqh_hanbali_{slug}.md ({N} words) ✓
```

### Step 2: Synthesis

Dispatch `@fiqh_synthesizer` with:
- The full question and slug
- The query type classification from Step 0
- The **paths** to all four temp files (agent uses `read_note` to read them)
- The contents of the `fiqh_synthesizer` principle card
- The output note structure from §4.2 (the synthesizer fills it in)

The synthesizer writes to `_fiqh_synthesis_{slug}.md` via `write_expansion`.

The synthesizer's output already contains wikilinks to the four madhab files using their final destination filenames (not temp file names), because the final names are deterministic: `Hanafi - {slug}`, `Maliki - {slug}`, etc.

**Log:**
```
[SYNTH] @fiqh_synthesizer → _fiqh_synthesis_{slug}.md ({N} words) ✓
```

### Step 3: Back-Link Injection

The four madhab files do not yet contain a link back to the synthesis file (they were written before synthesis existed). The orchestrator patches each one:

For each of the 4 temp files: call `read_note`, append the following line to the header block immediately after the uplink:

```
[[T.O.C (Fiqh)|Up to Fiqh]] | [[Synthesis - {slug}|View Synthesis]]
```

Then `create_note` to overwrite.

**Log:**
```
[LINK] Back-links injected into 4 madhab files ✓
```

### Step 4: Move to Final Location

Create the folder `30_Knowledge_Base/Fiqh/{slug}/` if it does not exist.

Rename and move each temp file to its final path:

| Temp File | Final Path |
| :--- | :--- |
| `_fiqh_hanafi_{slug}.md` | `30_Knowledge_Base/Fiqh/{slug}/Hanafi - {slug}.md` |
| `_fiqh_maliki_{slug}.md` | `30_Knowledge_Base/Fiqh/{slug}/Maliki - {slug}.md` |
| `_fiqh_shafii_{slug}.md` | `30_Knowledge_Base/Fiqh/{slug}/Shafii - {slug}.md` |
| `_fiqh_hanbali_{slug}.md` | `30_Knowledge_Base/Fiqh/{slug}/Hanbali - {slug}.md` |
| `_fiqh_synthesis_{slug}.md` | `30_Knowledge_Base/Fiqh/{slug}/Synthesis - {slug}.md` |

Use `organize_file` or `filesystem` rename+move as appropriate.

**Log:**
```
[MOVE] 5 files → 30_Knowledge_Base/Fiqh/{slug}/ ✓
```

### Step 5: Update T.O.C (Fiqh)

Call `read_note` on `T.O.C (Fiqh).md`. Append a new bullet to the `## Questions` section:

```markdown
- [[Synthesis - {slug}|{Full original question text}]]
```

Call `create_note` to overwrite with updated content.

**Log:**
```
[TOC] T.O.C (Fiqh).md updated ✓
```

### Step 6: Report

```
[DONE] Fiqh ruling on "{question}" processed.

Files created (30_Knowledge_Base/Fiqh/{slug}/):
  - Synthesis - {slug}.md        ({N} words)
  - Hanafi - {slug}.md           ({N} words)
  - Maliki - {slug}.md           ({N} words)
  - Shafii - {slug}.md           ({N} words)
  - Hanbali - {slug}.md          ({N} words)

All files cross-linked. T.O.C (Fiqh) updated.
```

---

## 6. Agent Definitions

### 6.1 Shared Agent Structure

All four madhab agents share the same tool set and output contract. They differ only in their principle voice and school disposition `in their GEMINI.md`.

**Tools:** `read_note`, `write_expansion`, `word_count`

**Turn limit:** 5 (these are focused, single-output agents)

**Output contract:**
- Write output to the block_id provided: `fiqh_{school}_{slug}`
- Follow the madhab file structure from §4.1 exactly — all sections are mandatory
- Mark every ruling `[CLASSICAL POSITION]` or `[DERIVED POSITION]`
- Mark every citation `(VERIFIED)` or `(UNCERTAIN)` — never omit a citation marker; never fabricate a source
- The `## Usul al-Fiqh — How This Ruling Was Derived` section is **not optional** — it is the core deliverable, not a footnote. The ruling alone is insufficient
- Follow source-specific handling rules from §4a for whichever source drives the ruling
- Present dominant ruling first. Then the most significant internal minority under `## Internal Dissent` — include the usul reason for the minority's divergence, not just the ruling difference

### 6.2 School Identity — What Lives in the Agent's `.md` System Prompt

The school's identity, methodological disposition, voice, and classical reference corpus are encoded **directly in the agent's `.md` file** (the system prompt). This is not a card — it is the permanent character of the agent. Cards narrow the *query type*; they do not define the school.

Each madhab agent's `.md` must contain the following identity block in its system prompt:

**Hanafi identity block:**
> You are the Hanafi agent. The Hanafi school is the most rationalist of the four madhabs. Abu Hanifa (d. 767) and his principal disciples — Abu Yusuf and Al-Shaybani — established a tradition that places heavy weight on analogical reasoning (*qiyas*) and juristic preference (*istihsan*): the ability to depart from strict analogy when it produces an inequitable result. The school is comfortable extending principles to novel cases through careful independent reasoning. When you cite classical sources, draw primarily from: *Al-Hidaya* (Al-Marghinani), *Radd al-Muhtar* (Ibn Abidin), *Bada'i al-Sana'i* (Al-Kasani). Your dominant school in geographic terms: Turkey, Central Asia, South Asia.

**Maliki identity block:**
> You are the Maliki agent. The Maliki school is empiricist and practice-grounded. Malik ibn Anas (d. 795) added the living practice of the people of Medina (*amal ahl al-Madina*) as a legal source not recognized by any other school, privileging observed communal practice over theoretical analogy. The school has the most developed doctrine of *maslaha mursala* — unattested public interest — as an independent legal source. When you cite classical sources, draw primarily from: *Al-Mudawwana* (Sahnun), *Al-Muwatta* (Malik ibn Anas), *Bidayat al-Mujtahid* (Ibn Rushd al-Hafid). Your dominant school in geographic terms: North Africa, West Africa.

**Shafi'i identity block:**
> You are the Shafi'i agent. Al-Shafi'i (d. 820) wrote *Al-Risala*, the foundational text of Islamic legal theory (*usul al-fiqh*), and is considered the architect of the classical discipline. The school is textualist but not literalist — it uses analogy within strict, systematically defined methodological constraints. Al-Shafi'i was deeply skeptical of open-ended maslaha or istihsan reasoning that departed from the textual sources. When you cite classical sources, draw primarily from: *Al-Umm* (Al-Shafi'i), *Minhaj al-Talibin* (Al-Nawawi), *Fath al-Wahhab* (Zakariyya al-Ansari). Your dominant school in geographic terms: East Africa, Southeast Asia, parts of the Middle East.

**Hanbali identity block:**
> You are the Hanbali agent. Ahmad ibn Hanbal (d. 855) was deeply skeptical of rationalist extrapolation and placed maximum weight on direct hadith evidence — even weak narrations (*da'if*) if no stronger evidence existed and no stronger analogy was possible. The school is the most resistant to *qiyas* and *maslaha* as independent sources of law; revelation is not to be supplemented by human reasoning beyond strict necessity. When you cite classical sources, draw primarily from: *Al-Mughni* (Ibn Qudama), *Al-Insaf* (Al-Mardawi), *Sharh al-Muntaha* (Al-Buhuti). Your dominant school in geographic terms: Saudi Arabia, Qatar.

---

### 6.2b Fiqh Agent Cards — Query Narrowing

Cards do not define the school — that is fixed in the system prompt above. Cards narrow *how the agent should frame its response* based on the nature of the query submitted. The pipeline's Step 0 selects the card based on question analysis.

| Card | Triggered By | Focus |
| :--- | :--- | :--- |
| `fiqh_ruling` | Default — any ruling question | Full output per §4.1: dominant ruling + complete usul derivation + internal dissent |
| `fiqh_usul_deep` | "how does X school approach...", "what is the methodology for..." | Emphasis on the school's usul framework as applied to this category of problem; ruling is secondary to methodology |
| `fiqh_historical` | "how did the ruling on X evolve...", "when did scholars first address..." | Traces the development of the ruling within the school's tradition across generations; includes key jurists and turning points |
| `fiqh_contemporary` | Modern/novel situations — cryptocurrencies, bioethics, digital contracts | Emphasizes the qiyas chain from classical asl to modern far'; explicitly labels all output `[DERIVED POSITION]`; no classical citations for the modern case itself |

The card is passed to each agent as part of the dispatch context. The school identity in the agent's `.md` remains unchanged regardless of card.

### 6.3 The `@fiqh_synthesizer` Agent

This is the hardest agent to specify correctly. It must hold no school allegiance and must resist the natural LLM tendency to produce confident, clean verdicts on genuinely contested questions.

**Tools:** `read_note` (to read the 4 madhab files), `write_expansion`, `word_count`

**Prompt constraints:**

1. **Consensus rule:** Only use the word "consensus" when all four schools agree on both ruling AND reasoning. Three out of four is "the preponderant position."
2. **Divergence typing:** Every disagreement must be categorized as: (a) *ruling divergence* — schools reach different rulings; (b) *reasoning divergence* — schools reach the same ruling but through different usul paths; (c) *methodological divergence* — schools disagree because of fundamental differences in legal philosophy (e.g., Hanbali rejection of independent qiyas vs. Hanafi embrace of it). Category (c) is non-resolvable and must be stated as such.
3. **Usul-level synthesis:** After synthesizing the rulings, the synthesizer must also synthesize at the *methodology* level — what do the schools' different usul paths reveal about their underlying commitments? Why does Hanafi accept this qiyas and Hanbali reject it? This is not derivable from the ruling alone; the synthesizer must read the `## Usul al-Fiqh` sections of each madhab file carefully.
4. **Probabilistic language mandate:** BANNED PHRASE: "the correct ruling is." REQUIRED PHRASES: "the preponderant position," "the strongest argument on balance," "genuine disagreement with no clear resolution among the schools," "a jurist of any school would recognize as valid."
5. **Uncertain citations:** If any madhab file contains a citation marked `(UNCERTAIN)`, the synthesizer notes this in the School Positions table and does not use that citation as evidence in the synthesis conclusion.
6. **Fill the complete output structure** from §4.2 — all sections are mandatory. "Spirit of the Law" cannot be omitted.
7. **Write wikilinks** to all four madhab files using their final filenames (Hanafi - {slug}, etc.) not their temp file paths.

---

## 7. The `/os:fiqh` Command

**File:** `commands/os/fiqh.toml`

```toml
description = "Asks a fiqh question. Runs all four Sunni madhabs in parallel then synthesizes."
prompt = """You MUST use the madhab_pipeline skill to process this request.
Load and follow the instructions in the madhab_pipeline SKILL.md exactly.
Question: {{args}}"""
```

---

## 8. New Components Required

| Component | Type | Priority |
| :--- | :--- | :--- |
| `@hanafi` agent | New agent file | Core |
| `@maliki` agent | New agent file | Core |
| `@shafii` agent | New agent file | Core |
| `@hanbali` agent | New agent file | Core |
| `@fiqh_synthesizer` agent | New agent file | Core |
| `madhab_pipeline` skill | New skill dir + SKILL.md | Core |
| `/os:fiqh` command | New command toml | Core |
| `T.O.C (Fiqh).md` | New vault file | Created by skill on first run |
| Atlas update | One-time vault edit | Done on first `/os:fiqh` run |
| `fiqh_synthesizer` principle card | New card in `90_System/Cards/` | Core |

## 9. What Does NOT Need to Change

| Component | Reason |
| :--- | :--- |
| `@classifier` agent | Not involved in this pipeline |
| `inbox-sort` skill | Completely separate |
| `@surgeon` agent | Not involved |
| `@librarian` agent | Not involved — the skill handles routing directly |
| `tools.py` MCP server | Existing `write_expansion`, `read_note`, `word_count`, `create_note` are sufficient |
| `prepare_dispatch` tool | Not needed — agents are dispatched directly with inline context |

---

## 10. Remaining Concerns

### 10.1 Option B Adds Significant Output Depth

Each madhab file includes the dominant ruling AND the most significant internal minority. This is the right call for knowledge depth but doubles the output per agent. Monitor turn limits and `write_expansion` word counts on first tests — if an agent truncates, the turn limit may need to increase from 5 to 8 for this pipeline.

### 10.2 Synthesis Reads All Four Files — Context Window Load

The `@fiqh_synthesizer` calls `read_note` on four files before generating output. If each madhab file averages 800-1200 words, the synthesis agent receives 3,200–4,800 words of input plus its principle card. This is well within Gemini's context window but should be noted for future complex questions (e.g. a question with extensive Option B minority positions).

### 10.3 The `fiqh_synthesizer` Principle Card is the Hardest Artefact to Write

This card must encode probabalistic language norms, divergence typing taxonomy, Maqasid evaluation logic, and the Ghazalian reflection framework — without becoming so prescriptive that the output is mechanical. The card should be drafted, tested on 2-3 questions, and refined before the pipeline is considered stable. Draft it last, after the madhab agents have been tested independently.

### 10.4 Slug Determinism

The slug derivation must be deterministic and consistent: the same question asked twice must produce the same slug, or the vault will accumulate duplicates. The skill must check whether `30_Knowledge_Base/Fiqh/{slug}/` already exists before proceeding. If it does, prompt the user: "A ruling on '{slug}' already exists. Overwrite? (y/n)"

---

## 11. Implementation Sequence

1. **Draft all four madhab agent `.md` files** (they are structurally similar — write one and derive the others by swapping the disposition card).
2. **Draft the `fiqh_synthesizer` principle card** in `90_System/Cards/fiqh_synthesizer.md`.
3. **Draft the `@fiqh_synthesizer` agent `.md` file**.
4. **Write `madhab_pipeline/SKILL.md`** following the step-by-step in §5.
5. **Add `/os:fiqh` command toml**.
6. **Create `T.O.C (Fiqh).md`** manually or let the first run create it.
7. **Test with a classical question** (settled, all four schools likely agree): e.g., *"What is the ruling on praying the five daily prayers?"* — use this to validate the pipeline mechanics without the risk of controversial content.
8. **Test with a genuinely contested question**: e.g., *"What is the ruling on music?"* — schools diverge sharply here. Validate that synthesis correctly maps divergence without falsely resolving it.
9. **Test with a derived/modern question**: e.g., *"What is the ruling on cryptocurrency?"* — validate that `[DERIVED POSITION]` labelling works and agents reason from usul principles rather than fabricating classical citations.
10. **Refine the `fiqh_synthesizer` card** based on test outputs.

---

*This document is the authoritative specification for the Fiqh pipeline. All implementation should reference this document. Consult `Fiqh_Madhab_Agent_Architecture.md` only for historical context on early design discussion.*
