# Fiqh Pipeline — Phased Implementation Plan

**Date:** 2026-03-28
**Spec Reference:** `Fiqh_Pipeline_Spec_v2.md`
**Status:** Planning

---

## Guiding Principles

Before reading the phases, internalize these rules from the os:sort precedent:

1. **Tools do mechanical work. Agents do cognitive work.** Creating files, moving files, patching wikilinks, updating T.O.C tables — all tool calls. Classifying query type, generating rulings, writing synthesis — all agents.
2. **Separation of concerns is enforced by agent tool access.** Madhab agents cannot call `organize_file` or `move_note`. The skill orchestrator calls those after all agents are done.
3. **Every agent write goes to a temp file first.** Agents never write to final vault locations directly. The orchestrator moves files when all agents have succeeded.
4. **Verify before proceeding.** After every agent dispatch, `word_count` confirms real output was written before the next step.
5. **No new tools if existing tools suffice.** Only add Python to `tools.py` if the task cannot be done with `create_note`, `move_note`, `append_to_note`, `word_count`, or `read_note`.

---

## Phase Overview

```
Phase 0 → tools.py additions (new tool: prepare_fiqh_dispatch)
Phase 1 → Vault scaffold (T.O.C file, Atlas link, folder)
Phase 2 → Four madhab agent .md files
Phase 3 → fiqh_synthesizer principle card + agent .md
Phase 4 → madhab_pipeline SKILL.md
Phase 5 → /os:fiqh command toml
Phase 6 → End-to-end tests (3 questions)
```

Each phase is atomic: it can be planned, implemented, and spot-checked independently before Phase N+1 begins.

---

## Phase 0 — tools.py: New Tool `prepare_fiqh_dispatch`

### Rationale

The os:sort pipeline has `prepare_dispatch` which does the mechanical work before an agent is invoked: creates the temp file, loads the card content, and returns a structured payload. The Fiqh pipeline needs its own equivalent that:
- Creates one temp file per school (`00_Inbox/_fiqh_{school}_{slug}.md`)
- Loads the selected card content from `90_System/Cards/fiqh_{card}.md`
- Returns a structured context payload to the orchestrator

Without this tool, the orchestrator must manually manage 4 temp file paths, card loading, and context preparation — cognitive overhead that belongs in a deterministic tool.

### What to Add

**Tool name:** `prepare_fiqh_dispatch`

**Inputs:**
| Field | Type | Description |
| :--- | :--- | :--- |
| `slug` | string | The question slug (e.g. `gold-jewelry-men`) |
| `school` | string | One of: `hanafi`, `maliki`, `shafii`, `hanbali`, `synthesizer` |
| `card` | string | Card filename without .md (e.g. `fiqh_ruling`, `fiqh_contemporary`) |
| `question` | string | The full original question text |
| `query_type` | string | `Classical`, `Derived`, or `Mixed` |

**What it does (deterministic Python):**
1. Derives `block_id` = `fiqh_{school}_{slug}`
2. Creates empty temp file at `00_Inbox/_fiqh_{school}_{slug}.md`
3. Reads card content from `90_System/Cards/{card}.md`
4. Returns JSON payload:
```json
{
  "block_id": "fiqh_hanafi_gold-jewelry-men",
  "temp_file": "00_Inbox/_fiqh_hanafi_gold-jewelry-men.md",
  "school": "hanafi",
  "question": "What is the ruling on gold jewelry for men?",
  "query_type": "Classical",
  "card_content": "...(card text)..."
}
```

**Why not reuse `prepare_dispatch`?**
`prepare_dispatch` is designed for `{{...}}` blocks in inbox files — it takes a `source_path` and `block_id` from `scan_inbox` output. The fiqh pipeline has no inbox source file; queries come from the slash command argument directly. A separate, clean tool avoids coupling two different workflows.

### Also Add: `fiqh_link_and_finalize`

A single tool that absorbs **all post-synthesis mechanical work**: frontmatter, back-links, file moves, and T.O.C update. It fully replaces what `@librarian` would do in the os:sort pipeline.

**Why no `@librarian`?**
In os:sort, `@librarian` does cognitive routing: it reads a note and *figures out* where it belongs. That LLM reasoning is necessary because destination and tags are unknown before the agent runs. In the Fiqh pipeline, every routing decision is fully known at Step 0 — before any agent fires:
- Destination: always `30_Knowledge_Base/Fiqh/{slug}/` — fixed
- T.O.C: always `T.O.C (Fiqh).md` — fixed
- `field/` tag: always `field/humanities` — fixed
- `subject/` tag: always `subject/fiqh` — fixed
- `concept/` tag: derived directly from the slug — trivial string, no LLM needed

There is nothing left for `@librarian` to decide. `fiqh_link_and_finalize` handles every step deterministically in Python — faster, zero agent turns, and no risk of misrouting.

**Inputs:**
| Field | Type | Description |
| :--- | :--- | :--- |
| `slug` | string | The question slug |
| `question` | string | Original full question text (used as T.O.C display text) |
| `concept` | string | The `concept/` tag value — inferred by orchestrator from slug (e.g. `gold-jewelry-men` → `concept/gold-jewelry`) |

**What it does:**
1. Creates the subfolder `30_Knowledge_Base/Fiqh/{slug}/` (via `mkdir`)
2. For each of the 4 madhab temp files (`_fiqh_{school}_{slug}.md`):
   - Reads the file content
   - Injects YAML frontmatter (merging with any existing): `field/humanities`, `subject/fiqh`, `concept/{concept}`
   - Appends the back-link line `[[Synthesis - {slug}|View Synthesis]]` immediately after the uplink header line
   - Renames and moves to `30_Knowledge_Base/Fiqh/{slug}/{School} - {slug}.md`
3. Reads the synthesis temp file, injects frontmatter (`type/map`, `field/humanities`, `subject/fiqh`, `concept/{concept}`), renames and moves to `30_Knowledge_Base/Fiqh/{slug}/Synthesis - {slug}.md`
4. Reads `T.O.C (Fiqh).md`, appends `- [[Synthesis - {slug}|{question}]]` to the `## Questions` section, writes it back
5. Returns a summary JSON of all 5 final file paths

### Implementation File

`D:\WISDOM\Kybernetes\90_System\Scripts\tools.py`

Add both tools to `handle_list_tools()` and implement handlers in `handle_call_tool()`.

**Checklist:**
- [ ] `prepare_fiqh_dispatch` tool definition added to `handle_list_tools()`
- [ ] `prepare_fiqh_dispatch` handler implemented
- [ ] `fiqh_link_and_finalize` tool definition added
- [ ] `fiqh_link_and_finalize` handler implemented
- [ ] Both tools registered under `# --- 🕌 FIQH PIPELINE ---` comment header
- [ ] Server restarted to pick up changes

---

## Phase 1 — Vault Scaffold

One-time vault setup. Done manually or by running the skill for the first time.

### Files to Create

**1. `30_Knowledge_Base/Fiqh/T.O.C (Fiqh).md`**

```markdown
---
tags:
  - type/map
  - field/humanities
  - subject/fiqh
---
# T.O.C (Fiqh)

Islamic jurisprudence. Four Sunni madhab perspectives (Hanafi, Maliki, Shafi'i, Hanbali) with synthesis. Each entry links to the synthesis note for that question; navigate from there to individual school positions.

[[T.O.C (30_Knowledge_Base)|Up to Knowledge Base]]

---

## Questions

*(Populated automatically by /os:fiqh)*
```

**2. Atlas entry**

Add to `30_Knowledge_Base/00_Atlas/` (whichever file serves as the Atlas hub — read it first to find the correct file):

```
- [[T.O.C (Fiqh)|Fiqh — Islamic Jurisprudence]]
```

### Checklist
- [ ] `30_Knowledge_Base/Fiqh/` folder exists
- [ ] `T.O.C (Fiqh).md` created with correct frontmatter and uplink
- [ ] Atlas hub updated with Fiqh link
- [ ] `T.O.C (Fiqh).md` appears in Obsidian graph (confirm not orphaned)

---

## Phase 2 — Four Madhab Agent Files

Four files in `C:\users\ibtas\.gemini\agents\`. Each is structurally identical; only the identity block differs.

### File: `hanafi.md`

```yaml
---
name: hanafi
description: Presents the Hanafi madhab position on a fiqh question. Covers ruling, complete usul derivation (source, asbab, textual analysis), and internal dissent.
kind: local
model: inherit
timeout_mins: 10
max_turns: 7
tools:
  - mcp_wisdom_os_read_note
  - mcp_wisdom_os_write_expansion
  - mcp_wisdom_os_word_count
---
```

**System prompt structure:**

```
# Identity

You are the Hanafi agent. [Full identity block from spec §6.2 — copied verbatim]

# Input

You will receive:
1. Question — the exact fiqh question to address
2. Query Type — [Classical / Derived / Mixed]
3. Card — the selected card (fiqh_ruling / fiqh_usul_deep / fiqh_historical / fiqh_contemporary)
4. Block ID — write your output to this block_id via write_expansion

# Workflow

1. Read the card content if a path is provided, or follow the inline card directive.
2. Generate your response following the madhab file structure exactly (from the card or the spec).
3. Call write_expansion with block_id and your full content.
4. Call word_count to confirm the file was written. Return the count.

# Output Rules

- Follow the §4.1 madhab file structure exactly. All sections are mandatory.
- Mark every ruling [CLASSICAL POSITION] or [DERIVED POSITION].
- Mark every citation (VERIFIED) or (UNCERTAIN). Never omit. Never fabricate.
- The ## Usul al-Fiqh section is the core deliverable. The ruling alone is insufficient.
- For Quran sources: cite verse, cover Asbab al-Nuzul, Muhkam/Mutashabih, Amm/Khass, Nasikh/Mansukh.
- For Sunnah sources: cite hadith gist + collector + narrator, cover Asbab al-Wurud and scope.
- For Qiyas: map all four components — Asl, Far', Illah, Hukm — and justify the Illah.
- Do NOT write to any file except the block_id temp file via write_expansion.
- Do NOT use create_note. Do NOT invent file paths.
```

**Replicate for:** `maliki.md`, `shafii.md`, `hanbali.md` — swap only the identity block (§6.2) and the `name`/`description` in YAML frontmatter.

### Checklist
- [ ] `hanafi.md` created
- [ ] `maliki.md` created
- [ ] `shafii.md` created
- [ ] `hanbali.md` created
- [ ] All four load without errors in Gemini CLI (test with `@hanafi "hello"`)
- [ ] Each agent writes to `write_expansion` only (confirm no stray `create_note` calls)

---

## Phase 3 — Synthesizer Principle Card + Agent

### 3a. Principle Card

**File:** `D:\WISDOM\Kybernetes\90_System\Cards\fiqh_synthesizer.md`

```markdown
# Goal
Synthesize four madhab positions on a single fiqh question into a structured, honest, probabilistic analysis. You are not a mufti. You do not issue fatwas. You map the tradition's internal debate and give the reader a principled basis for their own judgment.

# Formatting Rules (The Synthesis Template)
Follow §4.2 of Fiqh_Pipeline_Spec_v2.md exactly:
1. School Positions table (all four schools, with wikilinks to their files)
2. Consensus & Divergence (three divergence types: ruling / reasoning / methodological)
3. Maqasid Evaluation (five objectives table)
4. Synthesis Conclusion (probabilistic language only)
5. Spirit of the Law (Ghazalian reflection — mandatory, 2-3 paragraphs)

# Divergence Typing

Every disagreement MUST be categorized:
- **Ruling divergence** — schools reach different rulings
- **Reasoning divergence** — same ruling, different usul paths
- **Methodological divergence** — fundamental disagreement in legal philosophy (non-resolvable — state it as such)

You also synthesize at the usul level: why does Hanafi accept a qiyas that Hanbali rejects? Read the Usul al-Fiqh sections of each madhab file, not just the rulings.

# Probabilistic Language Mandate
BANNED: "the correct ruling is", "the answer is", "Islam says"
REQUIRED: "the preponderant position", "the strongest argument on balance", "genuine disagreement with no clear resolution", "all schools agree", "three of four schools"

# Uncertain Citations Rule
If any madhab file marks a citation (UNCERTAIN), note it in the School Positions table. Do NOT use uncertain citations as evidence in the Synthesis Conclusion.

# Quality Signals
- Consensus is only claimed when ALL FOUR schools agree on BOTH ruling AND reasoning
- Every disagreement is typed (ruling / reasoning / methodological)
- The Maqasid table has a substantive entry for every relevant objective
- The Spirit of the Law is a real paragraph, not a generic summary
- The human reader could defend any school's position after reading this

# Anti-Patterns
- Calling three-out-of-four agreement "consensus"
- Producing a clean verdict on a genuinely contested question
- Omitting the Spirit of the Law section
- Incorporating (UNCERTAIN) citations into the conclusion
- Treating the majority position as automatically correct
```

### 3b. Agent File

**File:** `C:\users\ibtas\.gemini\agents\fiqh_synthesizer.md`

```yaml
---
name: fiqh_synthesizer
description: Reads all four madhab temp files and synthesizes a structured, probabilistic, Maqasid-informed answer. The fifth and final agent in the Fiqh pipeline.
kind: local
model: inherit
timeout_mins: 12
max_turns: 8
tools:
  - mcp_wisdom_os_read_note
  - mcp_wisdom_os_write_expansion
  - mcp_wisdom_os_word_count
---
```

**System prompt structure:**

```
# Identity

You are the Fiqh Synthesizer. You hold no school allegiance. You read, compare, and honestly map four scholarly traditions without resolving what 1,200 years of scholarship has not resolved.

# Input

You will receive:
1. Question — the exact fiqh question
2. Query Type — [Classical / Derived / Mixed]
3. Four file paths — the four madhab temp files to read
4. Slug — for constructing wikilinks to the final file names
5. Block ID — write your synthesis to this block_id via write_expansion

# Workflow

1. Call read_note on each of the four madhab temp files.
2. Call read_note on 90_System/Cards/fiqh_synthesizer.md for the principle card.
3. Generate the synthesis following the card and §4.2 output structure exactly.
   - Wikilinks to madhab files use FINAL filenames: [[Hanafi - {slug}]], [[Maliki - {slug}]], etc.
4. Call write_expansion with block_id and your full synthesis.
5. Call word_count to confirm. Return the count.

# Output Rules

[all constraints from the principle card, stated directly here as well]
```

### Checklist
- [ ] `fiqh_synthesizer.md` card created in `90_System/Cards/`
- [ ] `fiqh_synthesizer.md` agent created in `.gemini/agents/`
- [ ] Agent loads in Gemini CLI without errors
- [ ] Agent tool list confirmed: only `read_note`, `write_expansion`, `word_count`

---

## Phase 4 — `madhab_pipeline` Skill

**File:** `C:\users\ibtas\.gemini\skills\madhab-pipeline\SKILL.md`

The skill is the step-by-step runbook. It references §5 of the spec. Write it in the same imperative, numbered format as `inbox-sort/SKILL.md`.

### Skill Structure

```
## Step 0: Initialization & Card Selection
## Step 1: prepare_fiqh_dispatch × 4 (all four schools)
## Step 2: Parallel Dispatch — @hanafi, @maliki, @shafii, @hanbali
## Step 3: Verify all four outputs (word_count × 4)
## Step 4: prepare_fiqh_dispatch for synthesizer
## Step 5: Dispatch @fiqh_synthesizer
## Step 6: Verify synthesis output
## Step 7: fiqh_link_and_finalize (move + link + T.O.C update)
## Step 8: Report
```

### Step 0 Detail — Card Selection Logic

The orchestrator classifies the question and selects a card before calling any agent:

| Question Pattern | Card Selected |
| :--- | :--- |
| "how does X school approach...", "what is the methodology..." | `fiqh_usul_deep` |
| "how did the ruling on X evolve...", "when did scholars first address..." | `fiqh_historical` |
| Clearly modern/novel situation (crypto, bioethics, AI, digital contracts) | `fiqh_contemporary` |
| Any other ruling question (default) | `fiqh_ruling` |

**Duplicate Check:** Before proceeding, check if `30_Knowledge_Base/Fiqh/{slug}/` already exists. If yes, show:
```
[WARN] A ruling on '{slug}' already exists.
Overwrite? (y / n)
```
Wait for user confirmation. On 'n', abort.

### Step 0 Log Format

```
[INIT] Question: "{question}"
[INIT] Slug: {slug}
[INIT] Query Type: {Classical / Derived / Mixed}
[INIT] Card: {card_name}
```

### Steps 1–3 Detail

Step 1 calls `prepare_fiqh_dispatch` four times (can be parallel — tool is pure Python, no agent involved):

```
[PREP] hanafi  → _fiqh_hanafi_{slug}.md ✓
[PREP] maliki  → _fiqh_maliki_{slug}.md ✓
[PREP] shafii  → _fiqh_shafii_{slug}.md ✓
[PREP] hanbali → _fiqh_hanbali_{slug}.md ✓
```

Step 2 dispatches all four agents simultaneously. Each agent receives its payload from Step 1.

Step 3 verifies with `word_count`:
```
[VERIFY] hanafi   → {N} words ✓
[VERIFY] maliki   → {N} words ✓
[VERIFY] shafii   → {N} words ✓
[VERIFY] hanbali  → {N} words ✓
```
If any `word_count` returns 0 or file missing: `[ERROR] @{school} produced no output. Re-dispatch? (y/n)`

### Steps 4–6 Detail

Step 4 calls `prepare_fiqh_dispatch` with `school=synthesizer` and passes the 4 temp file paths in the payload.

Step 5 dispatches `@fiqh_synthesizer` with the full payload (temp file paths, question, slug, card).

Step 6 verifies with `word_count`:
```
[VERIFY] synthesizer → {N} words ✓
```

### Step 7 Detail

Single tool call: `fiqh_link_and_finalize(slug, question, concept)`. This tool handles everything deterministically — no agent dispatch, no LLM reasoning:
```
[FINALIZE] Frontmatter injected into 5 files (field/humanities, subject/fiqh, concept/{concept}) ✓
[FINALIZE] Back-links injected into 4 madhab files ✓
[FINALIZE] 5 files moved to 30_Knowledge_Base/Fiqh/{slug}/ ✓
[FINALIZE] T.O.C (Fiqh).md updated ✓
```

The `concept` value is derived by the orchestrator in Step 0 from the slug — e.g. slug `gold-jewelry-men` → concept `gold-jewelry`. Pass it explicitly so the tool has no ambiguity.

### Step 8 Report

```
[DONE] Fiqh ruling on "{question}" complete.

Files (30_Knowledge_Base/Fiqh/{slug}/):
  Synthesis - {slug}.md     ({N} words)
  Hanafi - {slug}.md        ({N} words)
  Maliki - {slug}.md        ({N} words)
  Shafii - {slug}.md        ({N} words)
  Hanbali - {slug}.md       ({N} words)

Frontmatter: field/humanities · subject/fiqh · concept/{concept}
Cross-linked. T.O.C (Fiqh) updated.
```

### Checklist
- [ ] `C:\users\ibtas\.gemini\skills\madhab-pipeline\SKILL.md` created
- [ ] Step 0 card selection logic matches the table above
- [ ] Step 0 derives `concept` value from slug and passes it to Step 7
- [ ] Duplicate slug check and gate present
- [ ] All 8 steps written in imperative numbered format
- [ ] Log format matches os:sort style (`[TAG] message`)
- [ ] Step 7 passes all three args: `slug`, `question`, `concept`

---

## Phase 5 — `/os:fiqh` Command

**File:** `C:\users\ibtas\.gemini\commands\os\fiqh.toml`

```toml
description = "Asks a fiqh question. Runs all four Sunni madhabs in parallel then synthesizes."
prompt = """You MUST use the madhab-pipeline skill to process this request.
Load and follow the instructions in SKILL.md exactly.
Question: {{args}}"""
```

### Checklist
- [ ] `fiqh.toml` created in `commands/os/`
- [ ] Command loads in Gemini CLI (run `/os:fiqh test` and confirm skill is invoked)

---

## Phase 6 — End-to-End Testing

Three tests in sequence. Each validates a different layer of the pipeline.

### Test 1: Classical Question (Mechanics Validation)

**Goal:** Validate the pipeline mechanics on a settled, low-controversy question.
**Question:** `/os:fiqh "What is the ruling on the five daily prayers (salah)?"`
**Why this question:** All four schools agree (it is obligatory). The derivation is classical and direct from Quran + Sunnah. There is no inter-school divergence on the ruling — only potentially on specific details of execution.

**Pass criteria:**
- [ ] 5 files created in `30_Knowledge_Base/Fiqh/five-daily-prayers/`
- [ ] All 4 madhab files contain a `## Usul al-Fiqh` section (not blank)
- [ ] All 4 madhab files contain a `## Internal Dissent` section
- [ ] Synthesis file contains all 6 sections (School Positions, Consensus & Divergence, Maqasid, Synthesis Conclusion, Spirit of the Law, Personal Reflection)
- [ ] Synthesis correctly identifies this as consensus (all four schools agree), not "preponderant"
- [ ] All wikilinks in synthesis resolve correctly (check in Obsidian)
- [ ] `T.O.C (Fiqh).md` has a new entry linking to the synthesis file

### Test 2: Contested Classical Question (Divergence Validation)

**Goal:** Validate that the synthesizer correctly maps divergence without falsely resolving it.
**Question:** `/os:fiqh "What is the ruling on musical instruments?"`
**Why this question:** Schools diverge meaningfully here. The Hanbali position is the strictest prohibition; Maliki and Hanafi have more nuanced positions; there is significant internal dissent within the Maliki school. This tests the three-type divergence categorization.

**Pass criteria:**
- [ ] Synthesis does NOT write "the correct ruling is music is forbidden/allowed"
- [ ] Synthesis categorizes the divergence correctly — at minimum a methodological divergence note about hadith authenticity disputes
- [ ] At least one school's file has a non-trivial `## Internal Dissent` section
- [ ] Citations that cannot be verified are marked `(UNCERTAIN)`, not omitted or fabricated
- [ ] Synthesis Conclusion uses probabilistic language throughout

### Test 3: Contemporary / Derived Question (Qiyas Validation)

**Goal:** Validate the Derived Position labelling and qiyas chain coverage.
**Question:** `/os:fiqh "What is the ruling on cryptocurrency trading?"`
**Why this question:** No classical ruling exists. Every school must perform new qiyas from classical principles about currency, riba, and gharar (uncertainty). All output must be `[DERIVED POSITION]`.

**Pass criteria:**
- [ ] All 4 madhab files marked `[DERIVED POSITION]` at the top
- [ ] Every madhab file's Usul al-Fiqh section uses the Qiyas template (Asl → Illah → Far' → Hukm)
- [ ] No madhab file fabricates a classical citation for the cryptocurrency ruling itself
- [ ] Synthesis explicitly notes this is derived, not settled classical law
- [ ] Card used is `fiqh_contemporary` (check Step 0 log output)

---

## File Creation Checklist (All Phases)

| File | Phase | Location |
| :--- | :--- | :--- |
| `tools.py` — `prepare_fiqh_dispatch` + `fiqh_link_and_finalize` | 0 | `90_System/Scripts/tools.py` |
| `T.O.C (Fiqh).md` | 1 | `30_Knowledge_Base/Fiqh/T.O.C (Fiqh).md` |
| `hanafi.md` | 2 | `.gemini/agents/hanafi.md` |
| `maliki.md` | 2 | `.gemini/agents/maliki.md` |
| `shafii.md` | 2 | `.gemini/agents/shafii.md` |
| `hanbali.md` | 2 | `.gemini/agents/hanbali.md` |
| `fiqh_synthesizer.md` (card) | 3 | `90_System/Cards/fiqh_synthesizer.md` |
| `fiqh_synthesizer.md` (agent) | 3 | `.gemini/agents/fiqh_synthesizer.md` |
| `fiqh_ruling.md` (card) | 3 | `90_System/Cards/fiqh_ruling.md` |
| `fiqh_usul_deep.md` (card) | 3 | `90_System/Cards/fiqh_usul_deep.md` |
| `fiqh_historical.md` (card) | 3 | `90_System/Cards/fiqh_historical.md` |
| `fiqh_contemporary.md` (card) | 3 | `90_System/Cards/fiqh_contemporary.md` |
| `SKILL.md` | 4 | `.gemini/skills/madhab-pipeline/SKILL.md` |
| `fiqh.toml` | 5 | `.gemini/commands/os/fiqh.toml` |

---

## Dependencies Between Phases

```
Phase 0 → must complete before Phase 4 (skill calls the tools)
Phase 1 → can run parallel with Phase 0
Phase 2 → can run parallel with Phase 0, 1
Phase 3 → can run parallel with Phase 0, 1, 2
Phase 4 → requires Phase 0, 2, 3 complete (references tools + agents)
Phase 5 → requires Phase 4 complete (references the skill)
Phase 6 → requires all prior phases complete
```

Practical order: 0 + 1 → 2 + 3 → 4 → 5 → 6.

---

## Risk Register

| Risk | Likelihood | Mitigation |
| :--- | :--- | :--- |
| Agent hallucinates hadith citations | High | `(UNCERTAIN)` norm in prompt; synthesizer ignores uncertain citations |
| Synthesizer produces confident verdict | Medium | Probabilistic language mandate in principle card; Anti-Patterns list explicit |
| `write_expansion` scope issue (it only targets `_expand_` files in 00_Inbox) | **High** | **Phase 0 must generalize `write_expansion` or create a separate `write_fiqh_temp` variant that targets `_fiqh_` files** |
| Agent times out on complex question | Medium | `timeout_mins: 10-12`, `max_turns: 7-8`; re-dispatch gate in skill |
| Slug collision on similar questions | Low | Duplicate check in Step 0 with user gate |
| `fiqh_link_and_finalize` fails mid-run (partial move) | Low | Tool returns error JSON if any file is missing before proceeding; idempotent design |

> [!IMPORTANT]
> **The `write_expansion` scope issue is the highest structural risk.** The current implementation in `tools.py` maps `block_id` to `00_Inbox/_expand_{block_id}.md`. Fiqh agents need to write to `00_Inbox/_fiqh_{school}_{slug}.md`. Either `prepare_fiqh_dispatch` creates the file and passes the exact path, and agents use a different write path — or `write_expansion` is extended to accept an optional `prefix` parameter (`_expand_` vs `_fiqh_`). This must be resolved in Phase 0 before agents are built.

---

*Implementation proceeds one phase at a time. Each phase's checklist must be fully checked before the next phase begins.*
