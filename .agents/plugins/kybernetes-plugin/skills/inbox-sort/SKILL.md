---
name: inbox-sort
description: Sorts and processes the Obsidian Inbox (00_Inbox). Scans, classifies prompts, dispatches domain agents, stitches via @surgeon, organizes via @librarian.
---

# Inbox Sort Workflow

Process files from both inboxes into their correct vault/drive destinations.

> **CRITICAL RULES for the Orchestrator:**
> - You MUST process files and blocks ONE AT A TIME in exact sequence.
> - You MUST invoke the pre-defined custom subagents directly by their registered names (e.g., `TypeName: "classifier"`, `TypeName: "librarian"`, and the domain agents `TypeName: "turing"`, `TypeName: "euler"`, etc.) without dynamic definitions or self-emulation.
> - You do NOT classify domains directly. Call the `@classifier` subagent (`TypeName: "classifier"`) for that.
> - You do NOT prepare files directly. Call the `prepare_dispatch` tool.
> - You do NOT generate expansions directly. Call the domain subagent (`TypeName: "{domain}"`) directly.
> - You do NOT stitch files. Call the `stitch_files` tool.
> - You do NOT organize files directly. Call the `@librarian` subagent (`TypeName: "librarian"`) for that.

## Step 1: Scan

- Call `scan_inbox` (wisdom-os) to get structured JSON of all `00_Inbox/*.md` files.

**Log:**
```markdown
> **[SCAN]** Found **{N}** vault files.
> **[TARGETS]** Files with `{{...}}` blocks: {list}
```

## Step 2: Planning Phase (Deep Directives)

First, process ONLY the Two-Pass Expansion blocks (`directive == "deep"` or `directive == "blueprint"`) for the given file. If the file has no deep blocks, skip to Step 3.

**CRITICAL RULE:** You MUST process all Planner blocks **SEQUENTIALLY** (one by one) to prevent file-write corruption during injection. Do NOT process them in parallel.

For EACH two-pass block in the file (Sequentially):

**B1: Classify System**
- Call the `@classifier` subagent (`TypeName: "classifier"`) with the block's `prompt` to determine the `domain` (e.g., `turing`).
- **Ignore** the classifier's `card_type` and `card_value` (For Pass 1, we ALWAYS use the specialized Planner card).
- Auto-proceed. Do not ask for confirmation.
- **Log:**
  ```markdown
  > **[PASS 1]** Block {i}/{N}: Assigned to **@{domain}** (Planner Mode)
  ```

**B2: Planner Call (Decomposition)**
- The Orchestrator **MUST** use `view_file` to read the domain-specific planner card located at `/home/ibtasaam/Kybernetes/90_System/Cards/planner_{domain_name_without_@}.md` (e.g. `planner_turing.md`).
- Call the assigned domain subagent (`TypeName: "{domain}"`) directly and provide it with:
  1. The user's `prompt`.
  2. The full text of the specific `planner_{domain}.md` card.
  3. The exact length constraint:
     - For `@blueprint:N`: *"Execute the Planner Protocol. Return a JSON object with EXACTLY {n} sections."*
     - For `@deep`: *"Execute the Planner Protocol. Return a JSON object with as many sections as the topic demands."*
- Parse the JSON response. If parsing fails, show the error and ask the user for manual input or to retry.

**B3: Inject**
- Call `inject_subblocks` (tool) with: `source_path`, `block_id`, `directive`, `prompt`, `n` (if blueprint), `sections` (from Planner JSON).
- This converts the original tag to an HTML comment and writes the `## Title\n{{@expand ...}}` sub-blocks into the file.
- **Log:**
  ```markdown
  > **[INJECT]** Block {i}/{N}: "{first 50 chars}..." → **@{domain}** generated **{X}** atomic sections.
  ```

**B3.5: Pass 1 Approval Gate (Mandatory Pause)**
- After **ALL** Pass 1 injections are complete for all deep blocks in this file, pause and ask the user:
  ```markdown
  > **[PHASE TRANSITION]** Pass 1 complete. Review the source file in Obsidian. 
  > **Proceed to Generation Phase? (y/n)**
  ```
- **Wait for explicit user approval** before continuing to Step 3.

---

## Step 3: Generation Phase (Expand Directives)

- Call `scan_inbox` (tool) again on the source file. This captures all original `@expand` blocks **PLUS** all the newly injected `@expand` sub-blocks!
- Group the `prompt_blocks` by `h1_section` (ordered by `h1_index`).

**For EACH h1_section group:**
```markdown
> **[SECTION]** "{h1_section}" — **{N}** blocks
```
- Process all blocks in this section **IN PARALLEL**:

#### 3a: Classify (Parallel)
- Call the `@classifier` subagent (`TypeName: "classifier"`) with the exact `prompt` for ALL blocks in this section **simultaneously**.
- Wait for JSON `{domain, card_type, card_value}` for all blocks.
- **Log:**
  ```markdown
  > **[BATCH CLASSIFY]** {N} blocks mapped to domains. Auto-proceeding to Generation...
  ```

#### 3b: Prepare (Parallel)
- Call `prepare_dispatch` (tool) for ALL blocks **simultaneously** with their respective: `block_id`, `source_path`, `domain`, `card_type`, `card_value`.
- Returns JSON payload with `prompt`, `card_content`, `card_type`, `temp_file`, `block_id`.

#### 3c: Dispatch Domain Agent (Parallel)
- Call the domain subagent (`TypeName: "{domain}"`) **simultaneously** for all blocks using the prompt, card_content, and **temp_file** (passed as `target_file`) from their payloads.

#### 3d: Verify (Sequential check)
- Call `word_count` (tool) on the EXACT `temp_file` path to confirm each agent wrote output.

**Log:**
```markdown
> **[EXPAND]** Block {j}/{N}: "{first 50 chars}..." → **@{domain}** (`{card_value}`)
```

---

## Step 4: Stitch Files (Per Source File)

After ALL blocks for a single source file are expanded, stitch them:
- Call `stitch_files` (tool) with:
  `source_path`: (the original stitched note path)
  `blocks`: (array of `{"block_id": "...", "temp_file": "..."}` objects)

**Log:**
```markdown
> **[STITCH]** {filename} (**{N}** blocks) successfully integrated.
```

## Step 5: Classify & Organize (Per Stitched File)

**CRITICAL RULE:** When processing files (especially split files), you MUST execute Step 5 **SEQUENTIALLY**. You cannot organize multiple files in parallel to avoid T.O.C collisions.

For EACH stitched file in `00_Inbox`:

1. **Split Check:** If `scan_inbox` flagged `needs_split: True` for this file (because it has multiple `# ` topics), call `split_note` (wisdom-os) on the file. If new files are generated, process each split file independently.
2. **Classify:** Call the `@librarian` subagent (`TypeName: "librarian"`) with the exact file path. Wait for it to read the note and return the strict JSON routing payload.
3. **Hierarchy & Routing:** 
   
   **If the destination is `10_University`:**
   - **DO NOT** trust the Librarian's generated `category` string.
   - Ask the user to explicitly provide the T.O.C Category (Mandatory stop):
     ```markdown
     > **[UNIVERSITY ROUTING]** Moving '{suggested_name}' to '{destination}'. 
     > **Please enter the T.O.C Category for this topic:**
     ```
   - Once the user provides the Category, the Orchestrator **MUST** use the `view_file` tool to natively read the `toc_parent` file.
   - Analyze the markdown table sequence for the **user-provided** Category. Deduce the next mathematically correct `X.Y.Z` ID for the incoming file (e.g., `2.1.8`).
   - Call `organize_file` (tool) and explicitly pass `"final_name": "{X.Y.Z} - {suggested_name}"` as a parameter! The tool handles moving and frontmatter.
   - The Orchestrator **MUST** then use the `multi_replace_file_content` tool to surgically insert the new row (`| {X.Y.Z} | | [[...]] |`) directly into the T.O.C file's markdown table under the correct category header.

   **If the destination is NOT `10_University` (e.g. 30_Knowledge_Base):**
   - Auto-proceed. Trust the Librarian's JSON values.
   - Call `organize_file` (tool) using the Librarian's JSON array. The Python tool handles the Atlas TOC structures automatically.

**Log:**
```markdown
> **[ORGANIZE]** "{suggested_name}" → `{destination_dir}`
```

## Step 6: Report

```markdown
# Inbox Sort Complete

| File | Blocks Expanded | Agent(s) | Destination | Status |
| :--- | :--- | :--- | :--- | :--- |
| **{name}** | {N} | `@{agents}` | `{path}` | DONE |
```
