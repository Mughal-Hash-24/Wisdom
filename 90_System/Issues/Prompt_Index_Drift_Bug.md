# Prompt Index Drift Bug

**Status:** Resolved
**Date:** 2026-03-09
**Affected Components:** `inbox-sort` orchestrator, `scan_inbox` tool, `@surgeon` agent.

## Description
When processing files with a large number of `{{...}}` prompt blocks (e.g., 12 blocks), the `inbox-sort` orchestrator would suffer from "LLM Counting Hallucination."
The orchestrator was instructed to manually read the file (`read_note`) and enumerate the blocks from 1 to N. Because of context limits and LLM tracking flaws, it would assign incorrect indices to prompts (e.g., assigning index 3 to the 12th prompt, or skipping index 5 completely).
This resulted in domain agents writing expansions to scrambled `_expand_` files, and the `@surgeon` blindly stitching them in order, leading to overwritten blocks and empty files.

## Resolution
Removed the "counting" responsibility from the LLM and moved it to a deterministic Python tool.
1. **`tools.py` (`scan_inbox`)**: Modified to use regex to extract all `{{...}}` blocks sequentially and return a strict JSON array of objects `[{"block_id": "File_1", "prompt": "..."}, ...]`.
2. **`inbox-sort/SKILL.md`**: Removed instructions to `read_note` for block identification. Enforced strict iteration over the `prompt_blocks` JSON array from `scan_inbox`, using the provided `block_id`.
3. **`surgeon.md`**: Clarified that the `{{...}}` blocks appearing sequentially from top-to-bottom in the source strictly correspond to the ordered Expansion Map provided by the orchestrator.

## Verification
- Expansions are now natively written to exactly matching `_expand_{block_id}.md` paths without skipping indices.
- Surgeon stitches top-to-bottom aligning perfectly with the deterministic Python sequence.
