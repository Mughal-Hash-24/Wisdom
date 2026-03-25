# Phase 6: Surgeon Decomposition Spec

**Filed:** 2026-03-25
**Status:** Design Phase
**Goal:** Deprecate the `@surgeon` LLM agent completely. Replace it with a deterministic Python tool (`stitch_files`) that executes string replacement in ~10ms with 0% risk of hallucinating edits to the user's surrounding prose.

---

## 1. The Problem

Currently, `inbox-sort` Step 3 dispatches the `@surgeon` agent to stitch expanded temp files (`_expand_{id}.md`) back into the source note. 

**Why this fails at scale:**
- **Extreme Latency:** The LLM must read the source note AND all temp files into context, then "read" the whole document out again with the slots filled. This takes 20-40 seconds per file.
- **The "Surgeon Rule" Violations:** Despite strict prompting ("never alter the user's surrounding text"), LLMs are generative down to the character. They occasionally rewrite surrounding sentences, alter markdown headers, or strip whitespace when reconstructing the file.
- **Token Waste:** Stitching is a mechanical string substitution. Using an LLM for string substitution is like using a supercomputer to operate a light switch.

---

## 2. The Solution: `stitch_files` Tool

A new Python tool added to `D:\WISDOM\Kybernetes\90_System\Scripts\tools.py` that handles the stitching deterministically.

### Tool Schema

```json
{
  "source_path": "Vault-relative path to the source note (e.g., '00_Inbox/Concept.md')",
  "blocks": [
    {
      "block_id": "Concept_1",
      "temp_file": "00_Inbox/_expand_Concept_1.md"
    },
    {
      "block_id": "Concept_2",
      "temp_file": "00_Inbox/_expand_Concept_2.md"
    }
  ]
}
```

### Execution Logic

The tool will process the file **purely by string replacement**, using the exact same parsing logic we just built for `scan_inbox` and `inject_subblocks`:

1. Read the `source_path`.
2. Map all active `{{...}}` blocks using `DIRECTIVE_RE.finditer()`.
3. For each block in the payload:
   - Extract the block integer index `i` from the `block_id`.
   - Read the corresponding `temp_file`.
   - Find the `i`-th block in the source string.
   - Replace the `{{...}}` tag with the text from the `temp_file`.
   - Delete the `temp_file` to keep the Inbox clean.
4. Write the final assembled string back to `source_path`.
5. Return a success message: `"✅ Stitched {N} blocks into Concept.md"`

**Crucial Technical Detail:** Because replacing strings changes text length and invalidates subsequent regex index offsets, the tool must perform substitutions from **bottom to top** (reverse index order), or use a rolling offset tracker.

---

## 3. Orchestrator Update (`inbox-sort` SKILL.md)

Step 3 of the pipeline currently reads:
> - Dispatch `@surgeon` (agent) with the source file path and a map of `{block_id: temp_file_path}`.

This will be replaced with:
> - Call `stitch_files` (tool) with:
>   `source_path`: (the stitched note)
>   `blocks`: (array of `block_id` + `temp_file` pairs)

---

## 4. Decommissioning the Agent

Once the tool is verified working:
1. Move `C:\Users\ibtas\.gemini\agents\surgeon.md` to `D:\WISDOM\Kybernetes\90_System\Archive\Agents\surgeon.md`.
2. This formally transitions the Kybernetes system strictly away from LLM "file writers" toward a pure "Planner-Executor" model where tools handle all structural file manipulation.

---

## Implementation Plan

If this spec looks good, execution is extremely fast (estimated 15 minutes):
1. Write the `stitch_files` Python function + regex logic into `tools.py`.
2. Update the `inbox-sort` Step 3 flowchart.
3. Test on `Phase2_Blueprint_Test.md` (which currently has 3 un-stitched temp files sitting in the inbox).
4. Archive the `@surgeon` agent file.
