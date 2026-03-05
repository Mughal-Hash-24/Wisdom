# Post-Test Refinement: 4-Layer Architecture

## Problem Statement

Phase 5 testing revealed a separation-of-concerns violation: domain agents used `create_note` to write expansion files directly into destination folders (e.g., `30_Knowledge_Base/History_Culture/`), bypassing the orchestrator's stitch-back and the librarian's file organization. Multi-block files got fragmented -- each expansion went to a different folder instead of being stitched back into the source file.

**Root cause:** Domain agents have `create_note` access. Instructions say "write to output_path only," but LLMs override instructions when the prompt content suggests a "better" location. Instructions are suggestions. Tool access is enforcement.

## Current Architecture (Broken)

```
Orchestrator → Domain Agent (generates + writes file) → Librarian (links/tags)
                    ↑ PROBLEM: writes to wrong paths, fragments multi-block files
```

## Proposed Architecture (4-Layer)

```
ORCHESTRATOR (SKILL.md)
  │
  ├─ Scan inbox, find {{}} blocks
  ├─ For each block:
  │     ├─ Classify domain (9-way)
  │     ├─ Select card
  │     ├─ PRE-CREATE empty temp file: 00_Inbox/_expand_{source}_{N}.md
  │     └─ Dispatch @domain_agent with prompt + card + output_path
  │           → Agent writes expansion content into the pre-created file
  │           → Agent returns confirmation (word count only)
  │     └─ Orchestrator verifies file is no longer empty
  │
  ├─ Dispatch @surgeon
  │     ├─ Reads source file + all _expand_ temps
  │     ├─ Validates expansions (word count, missing files)
  │     ├─ Stitches: replaces {{}} markers with expansion content
  │     ├─ Overwrites source file with final stitched content
  │     └─ Deletes _expand_ temp files
  │
  └─ Dispatch @librarian (expanded role)
        ├─ Splits multi-topic files if needed
        ├─ Classifies destination folder
        ├─ APPROVAL GATE: shows proposed moves, waits for user "go"
        ├─ Moves files
        ├─ Renames (university ID scheme)
        ├─ Updates T.O.C
        └─ Adds frontmatter tags
```

## Tool Access Matrix (Enforcement)

| Layer | Tools | Cannot Do |
| :--- | :--- | :--- |
| Orchestrator | `scan_inbox`, `read_note`, `create_note` (creates temp files), `read_file` (cards) | Generate content |
| Domain Agents (9) | `read_note`, `create_note` (overwrite pre-created file ONLY), `load_template` (@Turing/@Euler only) | Create new files, move, delete, tag |
| @surgeon | `read_note`, `create_note`, `delete_note` | Classify, move, tag, generate |
| @librarian | `read_note`, `create_note`, `split_note`, `move_note`, `rename_note`, `add_frontmatter`, `list_files`, `search_vault`, `delete_note` | Generate content |

**Key constraint:** Domain agents have `create_note` but ONLY to overwrite the file the orchestrator pre-created. They are instructed: "Write ONLY to the output_path provided. This file already exists. Do NOT create files at any other path." The pre-created file acts as a strong anchor -- the agent sees a concrete path and has no reason to write elsewhere. If an agent goes rogue, the orchestrator detects it: the expected temp file is still empty.

## Changes Required

### Phase 6a: Update Domain Agent File Handling
- Remove `delete_note` from all 9 agent tool lists (keep `create_note` for overwriting)
- Update Output Rules: "Write expansion content to the EXACT output_path provided. This file already exists -- overwrite it. Do NOT create files at any other path."
- Update Workflow: agent writes to pre-created file, then returns confirmation with word count
- Add explicit rule: "The orchestrator has already created the output file. Your ONLY job is to fill it with content."

### Phase 6b: Create @surgeon Agent
- New file: `.gemini/agents/surgeon.md`
- Input: source file path + list of `_expand_` temp file paths
- Job: read source, read temps, validate, stitch, overwrite source, delete temps
- Key rule: **The Surgeon Rule** -- ALL text outside `{{...}}` markers is sacred. Never modify, rephrase, or "improve" user text.
- Tools: `read_note`, `create_note`, `delete_note`

### Phase 6c: Expand @librarian Role
- Add splitting (currently orchestrator Step 3) to librarian workflow
- Add destination classification (currently orchestrator Step 4) to librarian workflow
- Add file moving to librarian workflow
- Librarian already has: `move_note`, `rename_note`, `add_frontmatter`, `split_note`
- Add the APPROVAL GATE (show table, wait for "go") to librarian

### Phase 6d: Simplify Orchestrator (SKILL.md)
- Remove Steps 2c, 2d (validation + stitching) → now @surgeon's job
- Remove Steps 3, 4 (splitting + classifying/moving) → now @librarian's job
- Orchestrator becomes: Scan → Classify → Dispatch agents → Write temp files → Dispatch @surgeon → Dispatch @librarian → Report
- Much leaner SKILL.md

### Phase 6e: Update GEMINI.md
- Update Sub-Agent Roles: 11 agents now (9 domain + surgeon + librarian)
- Briefly describe the 4-layer architecture

## Verification Plan

1. Create test file with 3+ `{{...}}` blocks in different domains
2. Run `/os:sort`
3. Verify:
   - Domain agents return text (no files created by agents)
   - Orchestrator writes `_expand_` temp files
   - @surgeon stitches correctly (user text untouched)
   - @surgeon deletes temp files
   - @librarian splits if multi-topic
   - @librarian shows APPROVAL GATE before moving
   - @librarian handles T.O.C linking + tagging
4. Test edge case: single-topic file with 3 blocks (should NOT split)
5. Test edge case: file with 1 missing expansion (should leave `{{}}` intact)
