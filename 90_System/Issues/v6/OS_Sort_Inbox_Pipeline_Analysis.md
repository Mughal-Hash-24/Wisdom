# `/os:sort` — Inbox Pipeline: Deep Analysis
**Date:** 2026-04-05
**Scope:** Complete analysis of the `sort.toml` command → `inbox-sort` skill → all tool implementations in `tools.py` → all agent interactions → all branches.

---

## Overview

`/os:sort` is the most complex workflow in the Kybernetes system. It is a **6-phase deterministic pipeline** that transforms raw, unexpanded notes from two inboxes into final, tagged, T.O.C-linked vault notes. It coordinates two separate inboxes, two classes of expansion blocks, up to 9 domain agents, a classifier, a librarian, and 10 distinct Python MCP tools.

The pipeline has **two distinct execution paths** depending on the directive type of the blocks found:

| Path | Trigger | Phases |
| :--- | :--- | :--- |
| **Simple Expand** | `{{@expand ...}}` or `{{...}}` blocks only | Phases 1 → 3 → 4 → 5 → 6 |
| **Two-Pass Deep** | `{{@deep ...}}` or `{{@blueprint:N ...}}` blocks | Phases 1 → 2 → [GATE] → 3 → 4 → 5 → 6 |

---

## Entry Point: `sort.toml`

```toml
description = "Sorts and processes the Obsidian and Physical Inboxes."
prompt = """You MUST use the inbox-sort skill to process this request.
Load and follow the instructions in the inbox-sort SKILL.md exactly.
Target directories:
- Physical: D:\\Inbox (via filesystem)
- Logical: D:\\WISDOM\\Kybernetes\\00_Inbox (via wisdom-os)"""
```

The command carries no logic. It tells the orchestrator to load `inbox-sort/SKILL.md` and passes two target directories as context. The orchestrator reads the skill file and treats it as a strict protocol.

---

## Phase 1: Scan

### What Happens

Two parallel scans:
1. `scan_inbox` (wisdom_os) — scans `00_Inbox/*.md`
2. `list_directory` (filesystem) — scans `D:\Inbox`

### `scan_inbox` — Implementation Detail

```python
# tools.py — scan_inbox handler (lines 758–825)
DIRECTIVE_RE = re.compile(
    r'\{\{(?:@(blueprint):(\d+)|@(deep)|@(expand))?\s*(.*?)\}\}',
    re.DOTALL
)
```

For each `.md` file in `00_Inbox` (excluding T.O.C files and temp `_expand_*` / `_fiqh_*` files):

1. **Directive extraction** — finds all `{{...}}` blocks and classifies each as:
   - `@blueprint:N` — Two-Pass decomposition with N mandatory sections
   - `@deep` — Two-Pass decomposition with unconstrained sections
   - `@expand` — Simple single-pass expansion (legacy `{{...}}` defaults to this)

2. **H1 boundary mapping** — builds a position index of all `# Header` lines to know which H1 section each block belongs to. This governs parallel grouping in Phase 3.

3. **Returns structured JSON per file:**
```json
{
  "filename": "GoF_Design_Patterns.md",
  "path": "00_Inbox/GoF_Design_Patterns.md",
  "topics": ["GoF Design Patterns"],
  "prompt_blocks": [
    {
      "block_id": "GoF_Design_Patterns_1",
      "prompt": "Explain the Factory pattern...",
      "directive": "deep",
      "n": null,
      "h1_section": "Creational Patterns",
      "h1_index": 0
    }
  ],
  "needs_split": false
}
```

4. **`needs_split` flag** — set to `true` if the file has more than one H1 header. This triggers `split_note` in Phase 5.

### Log Output
```
> **[SCAN]** Found **N** vault files, **N** physical files.
> **[TARGETS]** Files with `{{...}}` blocks: [list]
```

---

## Phase 2: Planning Phase (Two-Pass Only)

**Triggered only for files containing `@deep` or `@blueprint:N` blocks.**

This phase is a **sequential loop** — each block is processed one at a time to prevent file corruption from concurrent `inject_subblocks` writes.

### Step B1: Classify Domain (via `@classifier`)

The orchestrator dispatches `@classifier` with the block's prompt text. The classifier returns:
```json
{"domain": "turing", "card_type": "card", "card_value": "turing_concept"}
```

**Critical:** For Phase 2 (Planner Mode), the `card_value` from the classifier is **discarded**. The orchestrator always uses the domain-specific **planner card** regardless of what the classifier returned. The classifier here serves only to identify the domain.

### Step B2: Planner Call (Decomposition)

The orchestrator:
1. Uses `view_file` to read `90_System/Cards/planner_{domain}.md` (e.g., `planner_turing.md`)
2. Dispatches the domain agent (e.g., `@turing`) with:
   - The user's raw prompt
   - The full planner card content
   - The exact constraint: `"Return a JSON object with EXACTLY {N} sections"` (blueprint) or `"as many sections as the topic demands"` (deep)

The domain agent, operating under the planner card, returns **only JSON** — no prose, no markdown:
```json
{
  "sections": [
    {"title": "Set Theory Foundation", "prompt": "Explain the strict mathematical..."},
    {"title": "Engine Execution Algorithms", "prompt": "Detail exactly how..."},
    {"title": "NULL Supply Constraint", "prompt": "Deep dive into the NULL injection..."},
    {"title": "ON vs WHERE Trap", "prompt": "Provide the standard SQL syntax..."}
  ]
}
```

The planner card enforces textbook-level exhaustive depth. For `@turing`, the gold standard example uses Left Outer Joins to demonstrate: a vague prompt `{{@deep Left Outer Joins}}` must produce 4+ atomic sub-prompts covering set theory, engine algorithms, NULL mechanics, and SQL syntax traps.

### Step B3: Inject Subblocks

The orchestrator calls `inject_subblocks` with:
- `source_path`: the vault-relative path to the source note
- `block_id`: the block's identifier
- `directive`: `"deep"` or `"blueprint"`
- `prompt`: the original prompt text (used for precise regex targeting)
- `n`: the N value (blueprint only)
- `sections`: the planner agent's JSON output

**Implementation detail in `tools.py` (lines 1140–1198):**

```python
# Target the EXACT block by its prompt text using regex escape
escaped_prompt = re.escape(prompt_string)
pattern = r'\{\{\s*(?:@(blueprint):\d+|@(deep)|@(expand))?\s*' + escaped_prompt + r'\s*\}\}'
```

This regex is constructed from the **literal prompt text**, not the block index. This guarantees that even if previous blocks have already been injected and changed the file's block count, the target is always located precisely.

The original `{{@deep ...}}` tag is **converted to an HTML comment**:
```
<!-- @deep processed: original prompt text -->
```

Then the sections are injected as:
```markdown
## Set Theory Foundation
{{@expand Explain the strict mathematical set theory...}}

## Engine Execution Algorithms
{{@expand Detail exactly how a modern SQL relational...}}
```

A `@blueprint:N` injection **rejects** if the JSON contains ≠ N sections:
```python
if n is not None and len(sections) != n:
    return error("@blueprint:4 requires exactly 4 sections, but received 3.")
```

### Step B3.5: Approval Gate (Mandatory Pause)

After **all** `@deep`/`@blueprint` blocks in the file are injected, the orchestrator **pauses**:
```
> **[PHASE TRANSITION]** Pass 1 complete. Review the source file in Obsidian.
> **Proceed to Generation Phase? (y/n)**
```

The user opens Obsidian, sees their topic broken into structured `## Sections` with `{{@expand sub-prompt}}` blocks, and can:
- Accept → type `y` → proceed to Phase 3
- Reject → type `n` → abort or manually edit and retry

This is the **human-in-the-loop gate**. No content is generated until the user approves the structure.

---

## Phase 3: Generation Phase (Parallel per H1 Section)

After the approval gate (or immediately, for simple-expand-only files), `scan_inbox` is called again on the source file. This second scan captures:
- Original `@expand` blocks that were already present
- Newly injected `@expand` sub-blocks from Phase 2

Blocks are grouped by their `h1_section` (the H1 header they fall under). Each H1 section group is processed sequentially, but blocks **within** a section group are processed in parallel.

### 3a: Classify (Parallel)

`@classifier` is dispatched once per block, simultaneously for all blocks in the section group. Each returns `{domain, card_type, card_value}`.

The classifier maps prompts to agent+card pairs using a deterministic routing table:

**`@turing` card routing:**

| Prompt Pattern                          | Card                |
| :-------------------------------------- | :------------------ |
| "compare", "vs", "difference between"   | `turing_comparison` |
| "debug", "fix", stack trace             | `turing_debugger`   |
| "design", "architect", "build a system" | `turing_design`     |
| "algorithm", "sort", "search", Big-O    | `turing_algorithm`  |
| Language-specific feature               | `turing_language`   |
| "how did X evolve", "history of" in CS  | `turing_history`    |
| Company/product case                    | `turing_case`       |
| Default                                 | `turing_concept`    |

**`@euler` card routing:**

| Prompt Pattern | Card |
| :--- | :--- |
| "prove", "theorem", "show that" | `euler_proof` |
| Default | `euler_concept` |

**All other domains** follow similar pattern tables (e.g., `narrative_history`, `biography`, `case_history`, `philosophical`, `thought_experiment`, etc.)

Edge cases:
- Cross-domain prompts → primary intent wins (`"physics of neural networks"` → `newton`)
- Still unclear → `turing` for technical, `iqbal` for abstract
- Invalid card returned → `prepare_dispatch` validation rejects it

### 3b: Prepare Dispatch (Parallel)

`prepare_dispatch` is called simultaneously for all blocks in the section group. For each block:

**Step 1: Validate** — `prepare_dispatch` checks against hardcoded allowlists:
```python
VALID_DOMAINS = ["turing", "euler", "newton", "alhaytham", "iqbal", "nabokov", "ibnkhaldun", "davinci", "machiavelli"]
VALID_CARDS = ["turing_concept", "turing_comparison", ..., "game_theory"]  # 31 valid cards
```
If the classifier returned an invalid domain or card, the tool returns a JSON error — the pipeline aborts and shows the validation failure rather than dispatching an agent to a wrong target.

**Step 2: Pre-create temp file**
```python
temp_file = VAULT_ROOT / "00_Inbox" / f"_expand_{block_id}.md"
temp_file.write_text("", encoding="utf-8")
```
An **empty** temp file is created at `00_Inbox/_expand_{block_id}.md`. The file must exist before the agent can write to it (security constraint in `write_expansion`).

**Step 3: Load card**
```python
card_path = VAULT_ROOT / "90_System" / "Cards" / f"{card_value}.md"
card_content = card_path.read_text(encoding="utf-8")
```
The full card text is embedded in the dispatch payload.

**Step 4: Extract prompt from source**
The tool re-reads the source file and extracts the block's prompt text by index. Other `{{...}}` blocks are not masked (the agent receives no context from them).

**Returns dispatch payload:**
```json
{
  "block_id": "GoF_Design_Patterns_2",
  "agent": "turing",
  "prompt": "Explain the Singleton pattern...",
  "card_content": "# @turing — Concept Card\n...",
  "card_type": "card",
  "temp_file": "00_Inbox/_expand_GoF_Design_Patterns_2.md"
}
```

### 3c: Dispatch Domain Agent (Parallel)

The domain agent (e.g., `@turing`) is invoked simultaneously for all blocks in the section group. Each receives:
- The exact prompt text
- The card content (quality signal, not a rigid template)
- The `block_id`
- The `temp_file` path (the pre-created empty file to write to)

The agent's workflow:
1. Analyzes the prompt
2. Reads the card to understand voice and quality signals
3. Generates the expansion (depth scales with topic complexity — no fixed word count)
4. Calls `write_expansion(target_file=temp_file, content=expansion_text)`

**`write_expansion` security in `tools.py` (lines 952–965):**
```python
# Safety check: only write to 00_Inbox files with allowed prefixes
if not ("00_Inbox" in target.parts and 
        (target.name.startswith("_expand_") or target.name.startswith("_fiqh_"))):
    return error("Security: write_expansion can only write to 00_Inbox/_expand_ or _fiqh_ files")

# File must pre-exist (orchestrator created it in prepare_dispatch)
if not target.exists():
    return error("Target file not found. Orchestrator must pre-create before writing.")
```

Agents **cannot**:
- Create arbitrary files
- Write to any path outside `00_Inbox`
- Write to files not named `_expand_*` or `_fiqh_*`
- Modify the source note
- Update any T.O.C

### 3d: Verify

After each agent returns, `word_count` is called on the exact `temp_file` path:
```python
# word_count strips YAML frontmatter before counting
_, body = parse_frontmatter(content)
words = len(body.split())
```

If `word_count` returns 0 (agent wrote nothing), the orchestrator surfaces an error. The pipeline does not proceed with empty expansions.

**Log per block:**
```
> **[EXPAND]** Block 2/4: "Explain the Singleton pattern..." → **@turing** (`turing_concept`)
```

---

## Phase 4: Stitch Files

After **all blocks** for a single source file are expanded, `stitch_files` is called.

**Implementation in `tools.py` (lines 1213–1257):**

```python
# Re-scan file for all {{...}} block positions
all_matches = list(DIRECTIVE_RE.finditer(content))

# Map block_id → (temp_file_content, temp_file_path)
# block_id format: {filestem}_{index} — index is 1-based, used as array offset
temp_contents = {}
for b in blocks:
    b_idx = int(block_id.rsplit("_", 1)[-1]) - 1
    temp_contents[b_idx] = (t_path.read_text(), t_path)

# Iterate BACKWARDS through matches (reverse order prevents index shifting)
for idx in range(len(all_matches) - 1, -1, -1):
    if idx in temp_contents:
        match = all_matches[idx]
        replacement_text, t_path = temp_contents[idx]
        content = content[:match.start()] + replacement_text + content[match.end():]
        t_path.unlink()  # Delete temp file immediately after stitching
        stitched_count += 1

source_file.write_text(content, encoding="utf-8")
```

**Key design decisions:**
- **Reverse iteration** — processes blocks from last to first, so byte positions of earlier blocks remain valid after each substitution
- **Immediate `unlink()`** — temp files are deleted as they are stitched, preventing stale expansions on retry
- **Index-based mapping** — block_id suffix `_N` (1-based) maps directly to the N-th regex match in the file, preserving insertion order even after Phase 2 injected sub-blocks

**Result:** The source note now contains full expanded content inline where each `{{...}}` block was. The file is ready for classification and routing.

**Log:**
```
> **[STITCH]** GoF_Design_Patterns.md (**4** blocks) successfully integrated.
```

---

## Phase 5: Classify & Organize (Sequential per File)

**Critical:** This phase is always sequential — multiple files cannot be organized in parallel because simultaneous T.O.C writes would corrupt the table.

### Step 5a: Split Check

If `scan_inbox` flagged `needs_split: true` for this file (multiple H1 headers), `split_note` is called.

**`split_note` implementation (lines 845–896):**

1. Parses and preserves any existing YAML frontmatter
2. Splits the body on `# ` H1 headers, **ignoring headers inside code blocks** (tracks ` ``` ` open/close state)
3. Writes each section to `00_Inbox/{i:02d} - {safe_title}.md`
4. Prepends the preserved frontmatter to each split file
5. Deletes the original multi-topic file
6. Each split file is then processed independently through the rest of Phase 5

### Step 5b: Classify — `@librarian`

`@librarian` is dispatched with the file path. It reads the note content via `read_note` and returns strict JSON:

```json
{
  "destination_dir": "10_University/Semester_04/Artificial Intelligence/Notes",
  "toc_parent": "T.O.C (Artificial Intelligence Notes).md",
  "category": "Search Algorithms",
  "suggested_name": "2.1.5 - A Star Execution.md",
  "tags": ["field/cs", "subject/ai", "concept/a-star"]
}
```

The librarian uses a destination matrix:

| Content Type | `destination_dir` |
| :--- | :--- |
| University course concept | `10_University/Semester_X/{Course}/Notes` |
| University lecture log | `10_University/Semester_X/{Course}/Lectures` |
| CS code/systems | `20_CS_Core/{Languages/Theory/Development/Tools}` |
| General abstract | `30_Knowledge_Base/10_Concepts` |
| General tangible | `30_Knowledge_Base/20_Entities` |
| General system/model | `30_Knowledge_Base/30_Frameworks` |

### Step 5c: Routing Branch — University vs. Non-University

#### Branch A: `10_University` Destination

The librarian's `category` is **discarded**. This is mandatory — the orchestrator never trusts a generated category for university routing.

1. **User prompt (mandatory stop):**
   ```
   > **[UNIVERSITY ROUTING]** Moving 'A Star Execution' to '10_University/Semester_04/AI/Notes'.
   > **Please enter the T.O.C Category for this topic:**
   ```
2. User provides category (e.g., `"Search Algorithms"`)
3. Orchestrator reads the T.O.C file with `view_file`
4. Analyzes the markdown table to find all existing IDs in the user-provided category
5. Deduces the next correct `X.Y.Z` ID (e.g., last entry is `2.1.4`, so next is `2.1.5`)
6. Calls `organize_file` with `final_name = "2.1.5 - {suggested_name}"`
7. **Manually inserts the T.O.C row** using `multi_replace_file_content` — the Python `organize_file` tool deliberately **does not touch** university T.O.C tables (line 1122–1126 in tools.py: `pass`) because table aesthetic precision requires the orchestrator's native edit capability

**Why this branch requires human input:** University notes need exact sessional placement, category matching, and sequential ID generation. An LLM-generated category could mismatch the T.O.C table's established category strings, breaking the table's visual ordering.

#### Branch B: Non-University Destinations (`20_CS_Core`, `30_Knowledge_Base`)

Orchestrator auto-proceeds — trusts the librarian's JSON values entirely.

Calls `organize_file` with the full librarian payload.

**`organize_file` implementation (lines 1054–1138) — 4 sub-steps:**

**1. Frontmatter Injection:**
```python
# Strip existing frontmatter (if any), rebuild clean from tags array
content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
yaml_lines = ["---", "tags:"] + [f"  - {t}" for t in tags] + ["---"]
```

**2. Uplink Injection:**
```python
alias = toc_parent.replace("T.O.C (", "").replace(").md", "")
uplink = f"[[{toc_parent}|Up to {alias}]]\n\n"
final_content = yaml_str + uplink + content.lstrip()
```

**3. T.O.C Update (branch by destination):**

For `30_Knowledge_Base`:
```python
# Auto-generate Atlas IDs: E.01, C.02, F.03 etc.
prefix = "E" if category == "entity" else "C" if category == "concept" else "F"
ids = re.findall(rf'\|\s*\*\*{prefix}\.(\d+)\*\*\s*\|', toc_text)
next_num = max([int(i) for i in ids]) + 1 if ids else 1
new_id = f"{prefix}.{next_num:02d}"
new_row = f"| **{new_id}** | {category} | [[{core_name}]] | `{tags_str}` |"
# Inserts row after the last existing table row
```

For `20_CS_Core`:
```python
# Simple bullet append
new_row = f"- [[{core_name}]]"
toc_path.write_text(toc_text.rstrip() + "\n" + new_row + "\n")
```

For `10_University`: `pass` — Python tool does nothing; orchestrator handles it natively.

**T.O.C writes use `TOC_LOCK`** — a `threading.Lock()` — to prevent race conditions in case multiple organize_file calls somehow overlap.

**4. Overwrite and Move:**
```python
source_file.write_text(final_content, encoding="utf-8")
dest_dir_path.mkdir(parents=True, exist_ok=True)
target_path = dest_dir_path / final_name
shutil.move(str(source_file), str(target_path))
```

**Log:**
```
> **[ORGANIZE]** "A Star Execution" → `10_University/Semester_04/Artificial Intelligence/Notes`
```

---

## Phase 6: Report

Final summary table:

```markdown
# Inbox Sort Complete

| File | Blocks Expanded | Agent(s) | Destination | Status |
| :--- | :--- | :--- | :--- | :--- |
| **GoF_Design_Patterns.md** | 4 | `@turing` | `20_CS_Core/Theory` | DONE |
```

---

## Complete Pipeline Flow Diagram

```
/os:sort
  │
  ├─ scan_inbox (wisdom_os) ──────────────────┐
  ├─ list_directory (filesystem) → D:\Inbox   │
  │                                           │
  │  For each file with {{...}} blocks:       │
  │                                           ↓
  │  Has @deep or @blueprint blocks?
  │  ├─ YES → Phase 2: Planning (SEQUENTIAL)
  │  │         │
  │  │         ├─ For each deep/blueprint block:
  │  │         │   ├─ @classifier → domain name
  │  │         │   ├─ view_file(planner_{domain}.md)
  │  │         │   ├─ Dispatch domain agent (Planner Mode)
  │  │         │   │   └─ Returns JSON {sections:[{title,prompt}]}
  │  │         │   └─ inject_subblocks(source, block_id, sections)
  │  │         │       ├─ Regex-targets block by prompt text
  │  │         │       ├─ Converts {{@deep}} → HTML comment
  │  │         │       └─ Writes ## Title\n{{@expand sub-prompt}} × N
  │  │         │
  │  │         └─ [APPROVAL GATE] — User reviews in Obsidian → y/n
  │  │
  │  └─ NO → skip to Phase 3
  │
  │  Phase 3: Generation (scan_inbox again → captures injected blocks)
  │  │
  │  │  Group blocks by h1_section
  │  │  For each H1 group (sequential):
  │  │  │
  │  │  ├─ 3a: @classifier × N blocks (PARALLEL) → {domain, card_value}
  │  │  │
  │  │  ├─ 3b: prepare_dispatch × N (PARALLEL)
  │  │  │       ├─ Validate domain + card against allowlists
  │  │  │       ├─ Pre-create 00_Inbox/_expand_{block_id}.md (empty)
  │  │  │       ├─ Load card from 90_System/Cards/{card_value}.md
  │  │  │       └─ Extract prompt from source by index
  │  │  │
  │  │  ├─ 3c: Dispatch domain agents × N (PARALLEL)
  │  │  │       └─ Agent: analyze → read card → generate → write_expansion(temp_file)
  │  │  │           ├─ Security: only 00_Inbox/_expand_* or _fiqh_* files
  │  │  │           └─ File must pre-exist (created by prepare_dispatch)
  │  │  │
  │  │  └─ 3d: word_count(temp_file) per block — verify > 0
  │  │
  │  │  Phase 4: stitch_files(source, [{block_id, temp_file}])
  │  │           ├─ Re-scan for all {{...}} positions
  │  │           ├─ Map block_id → temp file content
  │  │           ├─ Reverse-iterate matches (prevents index shift)
  │  │           ├─ Replace each {{...}} with temp file content
  │  │           └─ unlink(temp_file) immediately after each stitch
  │  │
  │  │  Phase 5: Classify & Organize (SEQUENTIAL)
  │  │  │
  │  │  ├─ needs_split? → split_note → [process each split independently]
  │  │  │   ├─ Parse frontmatter, preserve it
  │  │  │   ├─ Split on H1 (ignores headers inside code blocks)
  │  │  │   ├─ Write N files to 00_Inbox/{i:02d} - {title}.md
  │  │  │   └─ Delete original
  │  │  │
  │  │  ├─ @librarian → {destination_dir, toc_parent, category, suggested_name, tags}
  │  │  │
  │  │  └─ destination == 10_University?
  │  │      ├─ YES → [MANDATORY USER STOP]
  │  │      │         ├─ User provides T.O.C Category
  │  │      │         ├─ Orchestrator reads T.O.C, deduces next X.Y.Z ID
  │  │      │         ├─ organize_file(final_name="{ID} - {name}")
  │  │      │         │   ├─ Inject frontmatter
  │  │      │         │   ├─ Inject uplink
  │  │      │         │   ├─ Python: pass (no T.O.C write)
  │  │      │         │   └─ shutil.move → destination
  │  │      │         └─ Orchestrator: multi_replace_file_content → T.O.C table row
  │  │      │
  │  │      └─ NO → organize_file (auto)
  │  │              ├─ Inject frontmatter
  │  │              ├─ Inject uplink
  │  │              ├─ 30_Knowledge_Base: auto-generate E./C./F. IDs, insert table row
  │  │              ├─ 20_CS_Core: append bullet to T.O.C
  │  │              └─ shutil.move → destination
  │  │
  │  └─ Phase 6: Report table
```

---

## Key Invariants Enforced by the System

| Invariant | Enforcement Mechanism |
| :--- | :--- |
| Only one block injected at a time (Pass 1) | `inject_subblocks` uses prompt-text regex, processes sequentially |
| Agents can only write to pre-created temp files | `write_expansion` checks `target.exists()` before writing |
| Agents can only write to `00_Inbox/_expand_*` | Hardcoded prefix check in `write_expansion` |
| No classification errors reach agents | `prepare_dispatch` validates against hardcoded allowlists before creating temp files |
| No empty expansion reaches stitch | `word_count` verification after every agent call |
| T.O.C writes don't race | `TOC_LOCK` threading lock in `organize_file` |
| T.O.C table aesthetic is preserved | University T.O.C updates handled by orchestrator's `multi_replace_file_content`, not Python |
| Multi-topic notes never pollute vault | `needs_split` check + `split_note` before classification |
| Block positions stable during reverse-stitch | `stitch_files` iterates matches in reverse |
| User approves structure before content | Approval gate between Phase 2 and Phase 3 |

---

## Error Branches

| Error Condition | Behaviour |
| :--- | :--- |
| `@classifier` returns invalid domain | `prepare_dispatch` returns JSON error; pipeline surfaces it to user |
| `@classifier` returns invalid card | Same — allowlist validation rejects it |
| Card file not found in `90_System/Cards/` | `prepare_dispatch` returns `❌ Card not found` |
| Agent writes 0 words | `word_count = 0` → orchestrator shows error, asks retry |
| `inject_subblocks` prompt not found in file | Returns error with fallback regex attempt |
| `@blueprint:N` agent returns ≠ N sections | `inject_subblocks` rejects with count mismatch error |
| `split_note` finds only 1 H1 | Returns "Only 1 section found. No split needed." |
| `organize_file` source not found | Returns `❌ Source note not found` |
| T.O.C file missing for `30_Knowledge_Base` | Auto-creates a minimal T.O.C (similar to fiqh behavior) |
| `write_expansion` path outside 00_Inbox | Returns security error, blocks write |
| `write_expansion` file doesn't pre-exist | Returns `❌ Target file not found` |
