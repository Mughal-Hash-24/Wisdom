---
name: madhab-pipeline
description: Runs a fiqh question through all four Sunni madhab agents in parallel, synthesizes the results, and organizes the output into the vault. Triggered by /os:fiqh.
---

# Madhab Pipeline Workflow

Processes one fiqh question through four parallel madhab agents and one synthesizer, then finalizes the vault output.

> **CRITICAL RULES for the Orchestrator:**
> - You do NOT generate any fiqh content. Agents do that.
> - You do NOT move or tag files. The `fiqh_link_and_finalize` tool does that.
> - You do NOT skip the duplicate check in Step 0.
> - You do NOT dispatch the synthesizer until all four madhab word counts are confirmed > 0.
> - You do NOT call `fiqh_link_and_finalize` until the synthesizer word count is confirmed > 0.

---

## Step 0: Initialization

**0a: Parse and validate the question**

Derive these four values from the user's question:

| Value | How to derive |
| :--- | :--- |
| `question` | The full question text exactly as entered |
| `slug` | Lowercase, hyphens only, max 5 words — e.g. "What is the ruling on gold jewelry for men?" → `gold-jewelry-men` |
| `query_type` | `Classical` (question has clear classical precedent) / `Derived` (modern/novel, no direct classical ruling) / `Mixed` (classical basis but modern application) |
| `concept` | Short noun phrase from the slug for the `concept/` tag — e.g. `gold-jewelry-men` → `gold-jewelry` |

**0b: Duplicate check**

Check if `30_Knowledge_Base/Fiqh/{slug}/` already exists by calling `list_files` on `30_Knowledge_Base/Fiqh`.

If the folder already exists:
```
[WARN] A ruling on '{slug}' already exists.
Files: 30_Knowledge_Base/Fiqh/{slug}/
Overwrite? (y / n)
```
Wait for user input. On `n`, abort entirely and report.

**0c: Card selection**

Select one card based on the question's framing:

| Question Pattern | Card |
| :--- | :--- |
| "how does X school approach...", "what is the methodology for..." | `fiqh_usul_deep` |
| "how did the ruling on X evolve...", "when did scholars first address..." | `fiqh_historical` |
| Clearly modern/novel (crypto, bioethics, AI, gene editing, digital contracts) | `fiqh_contemporary` |
| Anything else (default) | `fiqh_ruling` |

**Log:**
```
[INIT] Question: "{question}"
[INIT] Slug:     {slug}
[INIT] Type:     {query_type}
[INIT] Concept:  {concept}
[INIT] Card:     {card}
```

---

## Step 1: Prepare Dispatch × 4

Call `prepare_fiqh_dispatch` four times — one per school. These calls are independent and can be made in parallel (the tool is pure Python, no agents involved).

Arguments for each:
- `slug`: {slug}
- `school`: `hanafi` / `maliki` / `shafii` / `hanbali`
- `card`: {card}
- `question`: {question}
- `query_type`: {query_type}

Save the returned payloads — each contains `block_id` and `temp_file` needed for Steps 2 and 4.

If any call returns an `"error"` key (e.g. card not found):
```
[ERROR] prepare_fiqh_dispatch failed for {school}: {error message}
```
Abort and fix the error before continuing.

**Log:**
```
[PREP] hanafi  → 00_Inbox/_fiqh_fiqh_hanafi_{slug}.md ✓
[PREP] maliki  → 00_Inbox/_fiqh_fiqh_maliki_{slug}.md ✓
[PREP] shafii  → 00_Inbox/_fiqh_fiqh_shafii_{slug}.md ✓
[PREP] hanbali → 00_Inbox/_fiqh_fiqh_hanbali_{slug}.md ✓
```

---

## Step 2: Parallel Dispatch — Four Madhab Agents

Dispatch all four agents simultaneously. Each agent receives its full payload from Step 1.

Call `@hanafi`, `@maliki`, `@shafii`, `@hanbali` — each with:
- The `question`
- The `query_type`
- The `card` name and `card_content` from the Step 1 payload
- The `block_id` to write to

The agents will call `write_expansion` and `word_count` internally and return their word counts.

---

## Step 3: Verify All Four Outputs

For each school, call `word_count` on the temp file path from the Step 1 payload:

```
[VERIFY] hanafi   → {N} words ✓
[VERIFY] maliki   → {N} words ✓
[VERIFY] shafii   → {N} words ✓
[VERIFY] hanbali  → {N} words ✓
```

If any word count returns 0 or the file is missing:
```
[ERROR] @{school} produced no output (0 words).
Re-dispatch? (y / n)
```
On `y`: repeat Steps 1–2–3 for that school only. On `n`: abort.

**Do NOT proceed to Step 4 until all four word counts are > 0.**

---

## Step 4: Prepare Synthesizer Dispatch

Call `prepare_fiqh_dispatch` once for the synthesizer:
- `slug`: {slug}
- `school`: `synthesizer`
- `card`: {card} (same card as the madhab agents — the synthesizer adapts its framing accordingly)
- `question`: {question}
- `query_type`: {query_type}
- `madhab_temp_files`: [the four `temp_file` paths from Step 1 payloads]

If this returns an error, fix it before dispatching.

**Log:**
```
[PREP] synthesizer → 00_Inbox/_fiqh_fiqh_synthesizer_{slug}.md ✓
```

---

## Step 5: Dispatch @fiqh_synthesizer

Call `@fiqh_synthesizer` with:
- The `question`
- The `query_type`
- The `slug`
- The four madhab temp file paths (from the Step 1 payloads)
- The `card_content` from the Step 4 payload
- The `block_id` from the Step 4 payload

The synthesizer will `read_note` each madhab file, generate the synthesis, and call `write_expansion`.

---

## Step 6: Verify Synthesis Output

Call `word_count` on the synthesizer temp file:

```
[VERIFY] synthesizer → {N} words ✓
```

If 0 or missing:
```
[ERROR] @fiqh_synthesizer produced no output.
Re-dispatch? (y / n)
```
On `y`: repeat Steps 4–5–6. On `n`: abort.

**Do NOT proceed to Step 7 until synthesizer word count is > 0.**

---

## Step 7: Link and Finalize

Call `fiqh_link_and_finalize` once:
- `slug`: {slug}
- `question`: {question}
- `concept`: {concept}

This tool performs all remaining work atomically:
1. Pre-flight check (all 5 files exist and are non-empty — if not, it returns an error before touching anything)
2. Frontmatter injection into all 5 files
3. Back-link injection into 4 madhab files
4. Move all 5 files to `30_Knowledge_Base/Fiqh/{slug}/`
5. Update `T.O.C (Fiqh).md`

If the tool returns an `"error"` key:
```
[ERROR] fiqh_link_and_finalize failed: {error detail}
```
Read the error's `hint` field and resolve before retrying.

**Log:**
```
[FINALIZE] Frontmatter injected (field/humanities · subject/fiqh · concept/{concept}) ✓
[FINALIZE] Back-links injected into 4 madhab files ✓
[FINALIZE] 5 files moved to 30_Knowledge_Base/Fiqh/{slug}/ ✓
[FINALIZE] T.O.C (Fiqh).md {updated / created} ✓
```

---

## Step 8: Report

```
[DONE] Fiqh ruling complete.

Question: "{question}"

Files → 30_Knowledge_Base/Fiqh/{slug}/
  Synthesis - {slug}.md     ({N} words)
  Hanafi - {slug}.md        ({N} words)
  Maliki - {slug}.md        ({N} words)
  Shafii - {slug}.md        ({N} words)
  Hanbali - {slug}.md       ({N} words)

Tags: field/humanities · subject/fiqh · concept/{concept}
Cross-linked. T.O.C (Fiqh) updated.
Open: [[Synthesis - {slug}]]
```
