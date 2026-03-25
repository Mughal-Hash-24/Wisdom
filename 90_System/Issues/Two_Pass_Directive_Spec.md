# Two-Pass Directive System: Definitive Specification

**Status:** Design Complete — Ready for Phase Planning
**Related:** [[Expansion_Output_Ceiling]], [[Expansion_Output_Ceiling_Solutions]]
**Filed:** 2026-03-25

---

## 1. Problem Statement

The current `{{...}}` expansion pipeline maps one block to one agent call to one output window (~800 words). Broad prompts ("Explain all 23 GoF design patterns") get compressed into shallow coverage. The user is forced to manually decompose topics — defeating the system's purpose.

---

## 2. The Three Active Directives

> Note: `@draft` is deferred pending a better implementation design.

| Directive | Mode | Agent Calls | Use When |
| :--- | :--- | :--- | :--- |
| `{{@expand ...}}` | Single-Shot (Default) | 1 | Narrow, focused topics (~800 words sufficient) |
| `{{@deep ...}}` | Unconstrained Two-Pass | 1 + N | Broad topic, trust the agent to scope it |
| `{{@blueprint:N ...}}` | Constrained Two-Pass | 1 + N | Broad topic, you want exactly N × ~800 words |

---

## 3. Resolved Design Decisions

### 3.1 `scan_inbox` Block Schema (Extended)

Two new fields added to every block object:

```json
{ "block_id": "Patterns_1", "prompt": "...", "directive": "blueprint", "n": 3 }
{ "block_id": "Rome_1",     "prompt": "...", "directive": "deep",      "n": null }
{ "block_id": "Singleton_1","prompt": "...", "directive": "expand",    "n": null }
```

The orchestrator reads `directive` to route single-shot vs. two-pass execution.

---

### 3.2 Pass 1 — Planner Output Contract

Pass 1 calls the domain agent with a Planner instruction. The agent must return **strict JSON only**:

```json
{
  "sections": [
    { "title": "Creational Patterns", "prompt": "Explain Singleton, Factory Method..." },
    { "title": "Structural Patterns", "prompt": "Explain Adapter, Decorator..." },
    { "title": "Behavioral Patterns", "prompt": "Explain Observer, Strategy..." }
  ]
}
```

- `@blueprint:N` Planner instruction includes: *"Return EXACTLY N sections."*
- `@deep` Planner instruction is unconstrained: *"Return as many sections as the topic demands."*

**Why JSON:** The LLM deciding the section titles is the creative act. A Python tool (`inject_subblocks`) parsing and writing is the mechanical act. LLM never touches file structure.

---

### 3.3 `inject_subblocks` Tool (New)

A Python tool in `tools.py` that:
1. Finds the original `{{@blueprint:N ...}}` / `{{@deep ...}}` line in the source file.
2. Replaces it with an HTML comment (seed preservation, invisible in Obsidian, skipped by `{{...}}` regex): `<!-- @blueprint:3 processed: original prompt -->`
3. Injects each section as a `## Level 2` heading + `{{@expand ...}}` sub-block.

**File transformation:**

Before:
```markdown
# GoF Design Patterns

{{@blueprint:3 Explain all GoF design patterns in Java}}
```

After `inject_subblocks`:
```markdown
# GoF Design Patterns

<!-- @blueprint:3 processed: Explain all GoF design patterns in Java -->

## Creational Patterns
{{@expand Explain Singleton, Factory Method, and Abstract Factory in Java}}

## Structural Patterns
{{@expand Explain Adapter, Decorator, and Composite in Java}}

## Behavioral Patterns
{{@expand Explain Observer, Strategy, and Command in Java}}
```

The next `/os:sort` sees 3 standard `@expand` blocks. **No infinite re-processing.**

---

### 3.4 `@surgeon` Stitching

No changes required. Sub-blocks are regular `@expand` blocks. `@surgeon` stitches them as usual. The `## Level 2` headings from `inject_subblocks` remain as natural section dividers in the final note.

---

### 3.5 Template-to-Principle-Card Migration

**Rigid Templates A-I for `@turing` and `@euler` are deprecated.** Replaced by principle cards stored in `90_System/Cards/`, identical in philosophy to all other domain agent cards.

**Rationale:** Rigid templates force a fixed scaffold regardless of topic shape. A principle card defines *intent and quality signals* — the agent constructs the structure that best fits the topic. This is required for the Two-Pass system: `@blueprint:N` for `@turing` demands an adaptive outline, which is impossible with a pre-baked template skeleton.

**Migration:** `load_template` tool deprecated. `read_note` on card file replaces it. `TEMPLATE_MAP` constant removed from `tools.py`.

---

## 4. Example Runs

### Example A: `{{@expand ...}}` (Standard — Unchanged)

**Input file:**
```markdown
# Java Patterns
{{@expand Explain the Singleton pattern in Java}}
```

**Flow:**
```
[SCAN]    1 block: @expand
[CLASSIFY] @turing (card: turing_concept) — confirm? y
[PREPARE] prepare_dispatch ✓
[EXPAND]  Block 1/1 → @turing ✓ (~800 words)
[STITCH]  Java_Patterns.md ✓
[ORGANIZE] → 20_CS_Core/Theory ✓
```

---

### Example B: `{{@blueprint:3 ...}}` (Constrained Two-Pass)

**Input file:**
```markdown
# GoF Design Patterns
{{@blueprint:3 Explain all the GoF design patterns in Java with examples}}
```

**Phase 1 — Planner:**
```
[SCAN]    1 block: @blueprint:3
[CLASSIFY] @turing (card: turing_concept) — confirm? y
[PLAN]    Calling @turing (Planner mode, N=3)...
[PLAN]    Blueprint received: 3 sections ✓
[INJECT]  GoF_Design_Patterns.md → 3 @expand sub-blocks written ✓
```

**File after Phase 1:**
```markdown
# GoF Design Patterns

<!-- @blueprint:3 processed: Explain all GoF design patterns in Java -->

## Creational Patterns
{{@expand Explain Singleton, Factory Method, Abstract Factory in Java}}

## Structural Patterns
{{@expand Explain Adapter, Decorator, Composite in Java}}

## Behavioral Patterns
{{@expand Explain Observer, Strategy, Command in Java}}
```

**Phase 2 — Executor:**
```
[SCAN]    3 blocks: @expand (sub-blocks from blueprint)
[EXPAND]  Block 1/3: "Creational Patterns..." → @turing ✓ (~800 words)
[EXPAND]  Block 2/3: "Structural Patterns..." → @turing ✓ (~800 words)
[EXPAND]  Block 3/3: "Behavioral Patterns..." → @turing ✓ (~800 words)
[STITCH]  GoF_Design_Patterns.md (3 blocks) ✓
[ORGANIZE] → 20_CS_Core/Theory ✓
```

**Final output:** ~2,400 words. Complete GoF coverage with code.

---

### Example C: `{{@deep ...}}` (Unconstrained Two-Pass)

**Input file:**
```markdown
# Roman Empire
{{@deep Explain the history of the Roman Empire from Republic to Fall}}
```

**Phase 1 — Planner (unconstrained):**
```
[SCAN]    1 block: @deep
[CLASSIFY] @ibnkhaldun (card: narrative_history) — confirm? y
[PLAN]    Calling @ibnkhaldun (Planner mode, unconstrained)...
[PLAN]    Blueprint received: 5 sections ✓
[INJECT]  Roman_Empire.md → 5 @expand sub-blocks written ✓
```

**Phase 2 — Executor:**
```
[EXPAND] Block 1/5: "Origins of Rome and the Republic..." → @ibnkhaldun ✓
[EXPAND] Block 2/5: "The Punic Wars and Roman Expansion..." → @ibnkhaldun ✓
[EXPAND] Block 3/5: "The Fall of the Republic..." → @ibnkhaldun ✓
[EXPAND] Block 4/5: "The Imperial Era..." → @ibnkhaldun ✓
[EXPAND] Block 5/5: "Decline and Fall..." → @ibnkhaldun ✓
[STITCH] Roman_Empire.md (5 blocks) ✓
[ORGANIZE] → 30_Knowledge_Base/20_Entities ✓
```

**Final output:** ~4,000 words. Complete historical arc.

---

## 5. Components Requiring Change

| Component | Change | Description |
| :--- | :--- | :--- |
| `tools.py` → `scan_inbox` | Modify | Add `directive` + `n` fields to block objects |
| `tools.py` → `inject_subblocks` | New Tool | Parse Planner JSON, write sub-blocks into source file |
| `tools.py` → `prepare_dispatch` | Modify | Gate Planner vs Executor mode based on directive |
| `tools.py` → `load_template` | Deprecate | Replaced by `read_note` on card files |
| `tools.py` → `TEMPLATE_MAP` | Remove | No longer needed after card migration |
| `inbox-sort` SKILL.md | Modify | Add two-pass routing logic based on `directive` field |
| `agents/classifier.md` | Modify | Reference cards instead of template letters for `turing`/`euler` |
| `90_System/Cards/` | New Files | Principle cards replacing Templates A-I |
