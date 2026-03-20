# Orchestrator Decomposition Plan

**Related Issue:** [[Expansion_Output_Ceiling]]
**Filed:** 2026-03-20
**Status:** In Design Phase
**Scope:** Current system only (Two-Pass directives deferred to Phase 1)

---

## 1. The Current Monolith

The `inbox-sort` SKILL.md is a single LLM prompt that handles **all** of the following:

| # | Responsibility | Currently Done By | Requires LLM? |
|---|---|---|---|
| 1 | Scan inbox for files and blocks | `scan_inbox` tool (Python) | No -- already code |
| 2 | Iterate over `prompt_blocks` JSON | `inbox-sort` (LLM) | No -- mechanical iteration |
| 3 | Classify domain (1 of 9 agents) | `inbox-sort` (LLM) | **Yes** -- semantic analysis |
| 4 | Select card/template within domain | `inbox-sort` (LLM) | **Yes** -- intent analysis |
| 5 | Read principle card files | `inbox-sort` (LLM) | No -- file read |
| 6 | Pre-create temp files | `inbox-sort` (LLM) | No -- mechanical file creation |
| 7 | Mask other `{{...}}` blocks in context | `inbox-sort` (LLM) | No -- string replacement |
| 8 | Dispatch domain agent with params | `inbox-sort` (LLM) | No -- mechanical invocation |
| 9 | Verify word count after expansion | `inbox-sort` (LLM) | No -- number comparison |
| 10 | Dispatch `@surgeon` with expansion map | `inbox-sort` (LLM) | No -- mechanical |
| 11 | Dispatch `@librarian` per file | `inbox-sort` (LLM) | No -- mechanical |

**Problem:** 9 out of 11 responsibilities do not require an LLM, yet all 11 are handled by a single LLM instance following a 200-line prompt. Every additional decision point is a hallucination risk.

---

## 2. Proposed Decomposition

### Principle
- **Agent** = requires LLM reasoning (semantic understanding, nuance, judgment)
- **Tool** = deterministic code (parsing, file I/O, iteration, comparison)
- Each agent has **exactly one job**

### New Components

#### A. `@classifier` (New Agent -- LLM)

**Single Responsibility:** Given a raw prompt and its surrounding context, return a structured classification.

**Input:**
```json
{
  "prompt": "Explain virtual memory in detail",
  "context": "This note covers OS fundamentals..."
}
```

**Output:**
```json
{
  "domain": "turing",
  "card_type": "template",
  "card_value": "A"
}
```

**Why this needs an LLM:** Determining whether "Explain the krebs cycle" belongs to `@alhaytham` vs `@euler`, or whether "compare merge sort and quicksort" should use Template E (Algorithmist) vs card `comparison_formal` -- these are semantic judgments that cannot be reduced to keyword matching alone.

**Why this must be a separate agent:** Classification is a distinct cognitive task from content generation. Mixing it into the orchestrator means the LLM must hold classification logic, card lookup tables, AND orchestration logic simultaneously -- increasing context noise and hallucination risk.

**Tools available to `@classifier`:**
- `read_note` (to fetch context from the source note)
- No write tools. Pure read-only, pure judgment.

---

#### B. `prepare_dispatch` (New Tool -- Python/MCP)

**Single Responsibility:** Given a classification result and a block_id, deterministically prepare everything needed for agent dispatch.

**What it does (all in code):**
1. Pre-creates the temp file (`_expand_{block_id}.md`)
2. If `card_type == "template"`: calls `load_template` internally and returns the template content
3. If `card_type == "card"`: reads the card file from `.gemini/skills/inbox-sort/cards/{card_value}.md` and returns its content
4. Reads the source note and masks all `{{...}}` blocks except the current one
5. Returns a structured dispatch payload:

```json
{
  "block_id": "Design_Patterns_OOP_1",
  "agent": "turing",
  "prompt": "Explain design patterns in OOP...",
  "context": "This note covers advanced Java topics... [...omitted...] ...",
  "card_content": "## Template A: Deep Dive\n...",
  "temp_file": "00_Inbox/_expand_Design_Patterns_OOP_1.md"
}
```

**Why this is a tool, not an agent:** Every step here is mechanical. Reading a file, creating a file, doing a string replacement. Zero judgment required. Zero hallucination possible.

---

#### C. `@surgeon` (Existing Agent -- Unchanged)

**Single Responsibility:** Stitches expansion temp files back into source notes. Already isolated with its own agent definition.

---

#### D. `@librarian` (Existing Agent -- Unchanged)

**Single Responsibility:** Splits, moves, renames, tags, and links notes. Already isolated.

---

#### E. Domain Agents (Existing -- Unchanged)

`@turing`, `@euler`, `@newton`, `@alhaytham`, `@iqbal`, `@nabokov`, `@ibnkhaldun`, `@davinci`, `@machiavelli`. Each receives a narrow prompt + card/template and generates content. Already isolated.

---

#### F. `inbox-sort` (Existing Skill -- Drastically Simplified)

**After decomposition, `inbox-sort` becomes a thin coordination layer.** Its only job is to call the above components in sequence. The SKILL.md shrinks from 200 lines to roughly:

```
Step 1: Call scan_inbox → get list of files and blocks
Step 2: For each block:
  2a: Dispatch @classifier → get {domain, card_type, card_value}
  2b: Call prepare_dispatch tool → get dispatch payload
  2c: Dispatch @{domain} agent with the payload
  2d: Call word_count tool → verify expansion
Step 3: Dispatch @surgeon per file
Step 4: Dispatch @librarian per file
Step 5: Report
```

**What was removed from `inbox-sort`:**
- The entire 50-line domain classification table (moved to `@classifier`)
- The entire 30-line card/template selection matrix (moved to `@classifier`)
- All file creation logic (moved to `prepare_dispatch` tool)
- All card-reading logic (moved to `prepare_dispatch` tool)
- All context-masking logic (moved to `prepare_dispatch` tool)

**What remains:** A flat, sequential checklist with zero branching. The LLM instance running `inbox-sort` no longer makes any judgment calls -- it just follows the sequence.

---

## 3. Component Interaction Diagram

```
User runs /os:sort
        │
        ▼
   ┌─────────┐
   │scan_inbox│ (Tool -- Python)
   │  Parse   │ Returns: files[], blocks[], block_ids[]
   └────┬─────┘
        │ For each block:
        ▼
  ┌────────────┐
  │ @classifier │ (Agent -- LLM)
  │  Classify   │ Returns: {domain, card_type, card_value}
  └─────┬──────┘
        │
        ▼
┌─────────────────┐
│ prepare_dispatch │ (Tool -- Python)
│   Pre-create     │ Returns: {dispatch_payload}
│   Read card      │
│   Mask context   │
└───────┬─────────┘
        │
        ▼
  ┌────────────┐
  │ @{domain}   │ (Agent -- LLM)
  │  Expand     │ Writes to temp file via write_expansion
  └─────┬──────┘
        │ After all blocks:
        ▼
   ┌──────────┐
   │ @surgeon  │ (Agent -- LLM)
   │  Stitch   │
   └────┬─────┘
        │
        ▼
  ┌────────────┐
  │ @librarian  │ (Agent -- LLM)
  │  Organize   │
  └─────┬──────┘
        │
        ▼
     [DONE]
```

---

## 4. Open Questions

### Q1: Can the Gemini CLI framework support a Python-based Controller?
Currently `inbox-sort` is a skill (LLM prompt). The simplified version is still an LLM following a checklist. Ideally the loop itself would be Python code calling agents programmatically. Is this possible within the current Gemini CLI agent framework, or must the controller remain an LLM-driven skill?

### Q2: Does `@classifier` warrant its own agent file?
It's a small, focused LLM task. Could it be implemented as a tool that internally calls an LLM (e.g., a Python function that makes an API call), or must it be a Gemini CLI sub-agent with its own `.md` definition?

### Q3: How does `prepare_dispatch` access card files?
The cards live in `.gemini/skills/inbox-sort/cards/`. The MCP tool `prepare_dispatch` would need to know the path to these files. Should they move to the vault (e.g., `90_System/Cards/`) for cleaner access, or should the tool hardcode the `.gemini` path?

### Q4: Future-proofing for Two-Pass
This decomposition is designed with the Two-Pass system in mind. When `@deep`/`@blueprint:N`/`@draft` are added later:
- `scan_inbox` gains directive parsing (deterministic, Python)
- `prepare_dispatch` gains blueprint-aware temp file creation
- A new `@planner` agent (or domain agent in planner mode) generates blueprints
- The controller loop gains a conditional branch (but it's code-level branching, not LLM-level)

The decomposition ensures none of these additions require the LLM orchestrator to make new decisions.
