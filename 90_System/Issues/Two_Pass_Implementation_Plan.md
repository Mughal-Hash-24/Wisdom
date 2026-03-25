# Two-Pass Directive System: Phased Implementation Plan

**Spec Reference:** [[Two_Pass_Directive_Spec]]
**Filed:** 2026-03-25
**Status:** Ready for Execution (Phase-by-Phase)

---

## Overview

The implementation is divided into 5 atomic phases. Each phase is independently testable and leaves the system in a working state. A phase must pass verification before the next begins.

| Phase | Title | Risk | Touches |
| :--- | :--- | :--- | :--- |
| 0 | Template → Card Migration | High | `90_System/Cards/`, `tools.py`, `classifier.md` |
| 1 | Extended Block Schema | Low | `tools.py` (`scan_inbox`) |
| 2 | `inject_subblocks` Tool | Medium | `tools.py` |
| 3 | Orchestrator Two-Pass Routing | High | `inbox-sort` SKILL.md |
| 4 | Verification | None | Test files, live run |

---

## Phase 0: Template → Principle Card Migration

**Goal:** Retire the 9 rigid structural templates (A-I). Replace with principle cards that define quality signals and voice, not mandatory section headers. This unblocks `@blueprint:N` and `@deep` for `@turing` and `@euler`.

**Risk:** High. This changes the core expansion quality for ALL `@turing` and `@euler` blocks permanently.

**Depends On:** Nothing (can execute immediately).

---

### Step 0.1: Write 9 Principle Cards

Create the following files in `D:\WISDOM\Kybernetes\90_System\Cards\`:

| Old Template | New Card Filename | Domain |
| :--- | :--- | :--- |
| Template_A_DeepDive.md | `turing_concept.md` | General CS theory |
| Template_B_Arena.md | `turing_comparison.md` | CS comparisons / X vs Y |
| Template_C_RosettaStone.md | `turing_language.md` | Language syntax / runtime theory |
| Template_D_Chronograph.md | `turing_history.md` | CS historical context / evolution |
| Template_E_Algorithmist.md | `turing_algorithm.md` | Algorithms, DSA, sorting, search |
| Template_F_Debugger.md | `turing_debugger.md` | Debugging, failure analysis |
| Template_G_Blueprint.md | `turing_design.md` | System design and architecture |
| Template_H_Mathematician.md | `euler_proof.md` | Mathematical proofs, theorems |
| Template_I_CaseStudy.md | `turing_case.md` | Industry case studies |

**Card format (NOT a rigid template):**
Each card is a principle card identical in philosophy to existing domain cards. It defines:
- **Goal:** What the reader should walk away understanding
- **Quality Signals:** What marks a great response (not mandatory headers)
- **Anti-Patterns:** What to avoid
- **Voice Directive:** How the agent should write

**Example new card (`turing_concept.md`):**
```markdown
# @turing — Concept Card

## Goal
The reader should understand the mechanism at a system level, not just the definition.

## Quality Signals
- Opens with the most precise technical definition possible, zero preamble
- Explains the HOW (control flow, state changes, data flow), not just the WHAT
- Grounds abstraction in a precise, load-bearing real-world analogy
- Includes code, pseudocode, or a diagram — not optional
- Addresses edge cases and failure modes explicitly

## Anti-Patterns
- Starting with "X is a type of..." followed by a vague paraphrase
- A definition without mechanism — NEVER explanation-only
- Generic analogies that carry zero explanatory weight ("think of it like a box")
- Truncating before covering edge cases

## Voice
Precise, mechanical, zero preamble. The Chief Engineer. Structure follows the topic's natural shape — do not impose a rigid skeleton.
```

---

### Step 0.2: Update `classifier.md`

Remove all references to `card_type: template` and template letters A-I for `@turing` and `@euler`. Replace with the new card names.

**Diff (Step 2 table for `@turing`):**

Before:
```markdown
| "compare", "X vs Y" | `card`     | `comparison_formal` |
| Default              | `template` | `A`                 |
| "algorithm"          | `template` | `E`                 |
```

After:
```markdown
| "compare", "X vs Y" | `card` | `turing_comparison` |
| Default              | `card` | `turing_concept`    |
| "algorithm"          | `card` | `turing_algorithm`  |
```

For `@euler`:
```markdown
| "prove", "theorem"  | `card` | `euler_proof`   |
| Default             | `card` | `euler_concept` |
```
(Also create `euler_concept.md` as a new card for general math explanation.)

---

### Step 0.3: Update `prepare_dispatch` Validation in `tools.py`

The Cold Path A validation currently allows `card_type: "template"` and letters A-I. After migration:
- Remove `"template"` from `VALID_CARD_TYPES` (only `"card"` remains)
- Remove `VALID_TEMPLATE_LETTERS` check
- Add all new card names to `VALID_CARDS`

---

### Step 0.4: Deprecate `load_template` Tool

The `load_template` tool in `tools.py` (and its handler) can be removed. The `prepare_dispatch` tool already reads card files via the vault path. After removing all template references from the classifier, this tool becomes dead code.

**Note:** Archive template files to `90_System/Archive/Templates/` — do not delete permanently until Phase 4 verification passes.

---

### Phase 0 Verification

1. Run `/os:sort` on `00_Inbox/Phase5_Split_Test.md` (or create a fresh test file with `{{@expand Explain Virtual Memory}}`).
2. Confirm the classifier no longer returns `card_type: "template"`.
3. Confirm the `prepare_dispatch` validation accepts the new card names.
4. Confirm the expansion reads the principle card (not a rigid template) and produces natural, topic-shaped structure.

---

## Phase 1: Extended Block Schema in `scan_inbox`

**Goal:** Make `scan_inbox` detect directive prefixes and populate `directive` + `n` on every block object. The orchestrator can then gate two-pass execution on these fields.

**Risk:** Low. `scan_inbox` is non-destructive (read-only). Existing `@expand` blocks are unaffected — they just get `directive: "expand"` and `n: null`.

**Depends On:** Phase 0 complete.

---

### Step 1.1: Modify `scan_inbox` Regex in `tools.py`

Current regex (extracts prompt only):
```python
prompts = re.findall(r'\{\{(.+?)\}\}', content, re.DOTALL)
```

New logic — parse directive prefix before extracting prompt:
```python
DIRECTIVE_RE = re.compile(
    r'\{\{(@(blueprint):(\d+)|@(deep)|@(expand))?\s*(.+?)\}\}',
    re.DOTALL
)
```

For each match, extract:
- `directive`: `"blueprint"`, `"deep"`, or `"expand"` (default if no prefix)
- `n`: integer if `blueprint`, else `None`
- `prompt`: the remaining text stripped of the directive prefix

Update the `prompt_blocks` list to include these fields:
```python
{
  "block_id": f"{f.stem}_{i+1}",
  "prompt": prompt,
  "directive": directive,  # NEW
  "n": n                   # NEW
}
```

---

### Phase 1 Verification

1. Create `00_Inbox/Directive_Test.md`:
   ```markdown
   {{@expand Explain the Singleton pattern}}
   {{@blueprint:3 Explain all GoF patterns}}
   {{@deep Explain the history of Rome}}
   ```
2. Call `scan_inbox` directly (via a test run) and confirm the returned JSON includes the correct `directive` and `n` values for all 3 blocks.

---

## Phase 2: `inject_subblocks` Tool

**Goal:** Add the Python tool that accepts the Planner's JSON and writes sub-blocks into the source file deterministically.

**Risk:** Medium. This tool writes to and restructures vault files.

**Depends On:** Phase 1 complete.

---

### Step 2.1: Add `inject_subblocks` Tool Definition in `tools.py`

**Input schema:**
```json
{
  "source_path": "vault-relative path to source note",
  "block_id": "block_id of the parent @blueprint/@deep block",
  "sections": [
    { "title": "Section Title", "prompt": "Focused sub-prompt text" }
  ]
}
```

**Handler logic:**
1. Read `source_path`.
2. Find the line containing the parent `{{@blueprint:N ...}}` or `{{@deep ...}}` tag using `block_id` to locate the exact block.
3. Replace that line with:
   `<!-- @{directive}:{n} processed: {original_prompt} -->`
4. Immediately after the comment, inject for each section:
   ```markdown
   
   ## {section.title}
   {{@expand {section.prompt}}}
   ```
5. Write the modified content back to `source_path`.
6. Return success payload with the count of injected sub-blocks.

---

### Phase 2 Verification

1. Create `00_Inbox/Blueprint_Test.md`:
   ```markdown
   # GoF Patterns
   {{@blueprint:3 Explain all GoF design patterns in Java}}
   ```
2. Call `inject_subblocks` manually with a hardcoded 3-section JSON payload.
3. Open the file in Obsidian. Confirm:
   - Original `{{@blueprint:3 ...}}` is now an HTML comment (invisible in Obsidian).
   - 3 `## Heading` + `{{@expand ...}}` sub-blocks are correctly injected.
   - `scan_inbox` re-scan finds exactly 3 `@expand` blocks (not the original tag).

---

## Phase 3: Orchestrator Two-Pass Routing

**Goal:** Rewrite Step 2 of `inbox-sort` to branch on `directive`. `@expand` follows the existing path. `@blueprint` and `@deep` trigger a Planner call followed by `inject_subblocks`, then loop into the executor path.

**Risk:** High. This rewrites core orchestration logic.

**Depends On:** Phases 0, 1, 2 all complete.

---

### Step 3.1: Modify `inbox-sort` SKILL.md Step 2

Replace the current Step 2 with the following branching logic:

```markdown
## Step 2: Prepare & Dispatch (Per Block, SEQUENTIAL)

For EACH block returned by `scan_inbox`:

### Path A: Standard (@expand)
If `directive == "expand"`:
  → Proceed with existing Steps 2a → 2a.5 → 2b → 2c → 2d (unchanged).

### Path B: Two-Pass (@deep or @blueprint:N)
If `directive == "deep"` or `directive == "blueprint"`:

  **Pass 1 — Planner:**
  1. Classify: Call `@classifier` with the prompt.
  2. Confirm gate: Show proposal, wait for y/override.
  3. Call the domain agent in PLANNER MODE:
     - For @blueprint:N: "Return a JSON object with a 'sections' array of EXACTLY {n} items. Each item has 'title' (string) and 'prompt' (string). No other output."
     - For @deep: "Return a JSON object with a 'sections' array covering the full scope of the topic. Each item has 'title' and 'prompt'. No other output."
  4. Parse the JSON response.
  5. Call `inject_subblocks` tool with `source_path`, `block_id`, and the parsed `sections` array.
  6. Log: `[PLAN] {filename} ({directive}:{n}) → {X} sections injected ✓`

  **Pass 2 — Executor:**
  7. Re-scan the source file (or use the injected sections list) to get the new @expand sub-blocks.
  8. Process each sub-block through the standard Path A pipeline (Steps 2a → 2d).
```

---

### Phase 3 Verification

Run `/os:sort` on a file containing all 3 directive types:
```markdown
# Test File

{{@expand Explain the Singleton pattern in Java}}

{{@blueprint:2 Explain the difference between TCP and UDP}}

{{@deep Explain the history of the Roman Empire}}
```

Confirm:
- `@expand` block processes in a single pass.
- `@blueprint:2` triggers Planner, exactly 2 sub-blocks injected, then 2 executor passes.
- `@deep` triggers Planner, N sub-blocks injected (agent's decision), N executor passes.
- All blocks are stitched and the file is fully expanded.

---

## Phase 4: Full System Verification

**Goal:** Run a realistic multi-directive inbox file end-to-end and confirm quality of output, T.O.C linking, and file organization.

**Test File:** A file with 3 prompts: one `@expand`, one `@blueprint:3`, one `@deep` spanning at least 2 different domains.

**Acceptance Criteria:**
- [ ] Templates A-I are never referenced in any log output.
- [ ] All expansions read from principle cards (confirm via `prepare_dispatch` payload logs).
- [ ] Blueprint:3 produces exactly 3 sub-sections, each ~800 words.
- [ ] Deep produces an agent-defined number of sub-sections.
- [ ] Surgeon stitches all sub-blocks correctly under their `## Level 2` headings.
- [ ] Librarian routes all resulting files correctly with T.O.C downlinks injected.
- [ ] Cold path gate shows classification confirmation before each block executes.
