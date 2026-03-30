# Phase 7: Context Overhaul + H1-Sectional Processing

**Filed:** 2026-03-30
**Status:** Design Phase
**Goal:** Replace the noisy masked-context in `prepare_dispatch` with a clean rolling summary file, and restructure the orchestrator to process blocks H1-section by H1-section for robustness and coherence.

---

## Change 1: Running Summary File (Context Overhaul)

### Problem
`prepare_dispatch` currently slices the source file and masks every other `{{...}}` block as `[...omitted...]`. This gives domain agents 1,000+ tokens of noisy, placeholder-filled document skeleton that confuses rather than contextualizes.

### Solution
Maintain a `_summary_{stem}.md` file in `00_Inbox`. After each domain agent finishes, the orchestrator reads the first paragraph from `_expand_{block_id}.md` and writes a 1–2 sentence summary entry to the summary file. The next agent call receives only the path to this file as its context.

### Changes Required

#### A. `tools.py` — Modify `prepare_dispatch`
- Remove: masked source file construction logic (the `[...omitted...]` replacement).
- Add: `summary_file` field to the returned payload — e.g., `"00_Inbox/_summary_Kafka.md"`.
- Create the summary file on first call if it does not exist (empty starter).

#### B. `tools.py` — Add `append_summary` tool
A new minimal tool for the orchestrator to append a summary line after verifying each block:
```json
{
  "summary_file": "00_Inbox/_summary_Kafka.md",
  "entry": "Block 2 covered the symbolic significance of the apple thrown at Gregor and its role in accelerating his death."
}
```
The tool appends `"- {entry}\n"` to the file and returns the running count of entries.

#### C. `SKILL.md` — Update Step 2d
After `word_count` confirms the expansion is written, the orchestrator:
1. Reads the first paragraph from `_expand_{block_id}.md` (or uses the agent's own summary if it returns one).
2. Calls `append_summary` with the block's 1–2 sentence entry.
3. The next `prepare_dispatch` call automatically picks up the updated summary file.

### Before/After Comparison (Token Cost)

| Stage | Old Context | New Context |
| :--- | :--- | :--- |
| Block 1 | Full source (1,500 tokens) with [omitted] | Empty summary file (`_summary.md`, 0 tokens) |
| Block 2 | Full source (1,500 tokens) with [omitted] | 1 summary line (~30 tokens) |
| Block 5 | Full source (1,500 tokens) with [omitted] | 4 summary lines (~120 tokens) |

---

## Change 2: H1-Sectional Processing

### Problem
With 27-30 `{{}}` blocks in a single file, the orchestrator processes them as a flat sequential stream. A timeout or user interruption at block 14 leaves 4 incomplete sections scattered across the document. No complete unit of knowledge is produced.

### Solution
Tag each block with its parent H1 section in `scan_inbox`. The orchestrator processes all blocks within one H1 section before moving to the next — mirroring the `split_note` logic.

### Changes Required

#### A. `tools.py` — Modify `scan_inbox` block extraction
Add `h1_section` (the text of the last-seen `# H1` heading) and `h1_index` (0-indexed group number) to each block object:

```python
# Add before the DIRECTIVE_RE.finditer loop:
h1_re = re.compile(r'^# (?!#)(.+)$', re.MULTILINE)
h1_boundaries = [(m.start(), m.group(1).strip()) for m in h1_re.finditer(content)]

# Inside the loop, determine the parent H1 for each match position:
def get_h1(pos, boundaries):
    section = "Untitled"
    idx = 0
    for i, (start, name) in enumerate(boundaries):
        if start <= pos:
            section = name
            idx = i
    return section, idx

# In the block append:
h1_name, h1_idx = get_h1(m.start(), h1_boundaries)
prompt_blocks.append({
    "block_id": ...,
    "prompt": ...,
    "directive": ...,
    "n": ...,
    "h1_section": h1_name,
    "h1_index": h1_idx
})
```

#### B. `SKILL.md` — Restructure Step 2 processing loop
Change the outer loop from "For EACH block" to "For EACH H1 section group → For EACH block within that group":

```
For EACH h1_section group returned by scan_inbox (ordered by h1_index):
  [SECTION] Processing H1: "{h1_section}" ({N} blocks)
  → Initialize/clear summary file for this section
  → For EACH block in this section:
      → Run Path A or Path B as normal
      → Append summary entry after each block
  → [SECTION DONE] H1 "{h1_section}" complete
```

#### C. Summary File Scoping
The summary file resets per H1 section (not per full file), ensuring agents only read context relevant to their current discussion topic, not unrelated sections from earlier H1s.

---

## Implementation Plan

### Step 7.1 — Modify `scan_inbox` in `tools.py`
Add `h1_section` and `h1_index` to every block object. Simple regex addition, no logic change.

### Step 7.2 — Add `append_summary` tool schema + handler in `tools.py`
Minimal tool: accepts `summary_file` and `entry`, appends to file, returns count.

### Step 7.3 — Modify `prepare_dispatch` in `tools.py`
Remove masked-context construction; add `summary_file` path to the returned payload.

### Step 7.4 — Update `SKILL.md`
- Step 2 outer loop: section-group iteration
- Step 2d: add `append_summary` call after each `word_count`
- Section log message format

### Verification
Test file: `00_Inbox/Phase7_Test.md` with 2 H1 sections, 3 blocks each.
Confirm:
- Each H1 group processes completely before the next begins.
- Summary file resets between groups.
- Domain agents receive the correct scoped summary, not the noisy masked source.
