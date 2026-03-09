---
tags:
  - field/cs
  - subject/systems
  - concept/architecture
  - type/issue
---
[[T.O.C (90_System)|Up to 90_System]]

# Issue: Domain Agents Writing to Wrong Files

> **Filed:** 2026-03-09
> **Status:** RESOLVED
> **Affected Components:** `tools.py`, all 9 domain agents, `inbox-sort` SKILL.md

---

## Problem Description

The `@turing` agent (and potentially other domain agents) consistently writes expansion content to the wrong pre-created temp file. For example, block 3's expansion overwrites block 1's file (`_expand_AI_Semester_4_1.md`), destroying previously generated content.

**Root Cause:** Domain agents had `create_note` access -- a general-purpose write tool that accepts any file path. The correct output path was communicated as text in the dispatch prompt, but the LLM confused similar paths (e.g., `_expand_AI_Semester_4_1.md` vs `_expand_AI_Semester_4_3.md`).

As documented in `Post_Test_Refinement_Plan.md`: "Instructions are suggestions. Tool access is enforcement."

---

## Resolution: Scoped `write_expansion` Tool

### New Tool: `write_expansion(block_id, content)`

- Takes a `block_id` (e.g., `Artificial_Intelligence_Semester_4_3`) and `content`
- Constructs the path internally: `00_Inbox/_expand_{block_id}.md`
- Validates the file was pre-created by the orchestrator before writing
- Returns word count automatically (eliminates separate `word_count` call)
- Can ONLY write to `_expand_` prefixed files in `00_Inbox` -- no arbitrary vault writes

### Changes

| Component | Change |
| :--- | :--- |
| `tools.py` | Added `write_expansion` tool definition + handler |
| 9 domain agents | Replaced `create_note` with `write_expansion` in tool list, workflow, output rules |
| `inbox-sort` SKILL.md | Orchestrator now passes `block_id` to agents, not `output_path` |

### Security Model

- Agents cannot write to arbitrary paths (no `create_note` access)
- Agents cannot create new files (tool requires pre-existing file)
- Path is constructed server-side from a simple identifier
- Agent receives `block_id = "AI_Semester_4_3"` instead of full path `00_Inbox/_expand_AI_Semester_4_3.md`
