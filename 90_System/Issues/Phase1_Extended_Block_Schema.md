# Phase 1: Extended Block Schema in `scan_inbox`

**Parent Plan:** [[Two_Pass_Implementation_Plan]]
**Depends On:** Phase 0 complete ✓
**Status:** Ready for Execution
**Risk Level:** Low — `scan_inbox` is read-only; existing `@expand` blocks are unaffected
**Files Changed:** `tools.py` (lines 590-591, the `prompt_blocks` construction)

---

## Objective

Make `scan_inbox` detect directive prefixes (`@expand`, `@deep`, `@blueprint:N`) and populate two new fields — `directive` and `n` — on every block object. The orchestrator reads these fields to gate single-pass vs two-pass execution. Without this, the two-pass system has no way to differentiate block types.

---

## Current Code (lines 590-591)

```python
prompts = re.findall(r'\{\{(.+?)\}\}', content, re.DOTALL)
prompt_blocks = [{"block_id": f"{f.stem}_{i+1}", "prompt": p.strip()} for i, p in enumerate(prompts)]
```

**Current output per block:**
```json
{
  "block_id": "GoF_Patterns_1",
  "prompt": "@blueprint:3 Explain all GoF design patterns in Java"
}
```

The directive prefix leaks into the `prompt` string and is not parsed. The orchestrator has no machine-readable way to distinguish block types.

---

## Target Output Per Block

```json
{ "block_id": "GoF_Patterns_1",  "prompt": "Explain all GoF design patterns in Java", "directive": "blueprint", "n": 3 }
{ "block_id": "Rome_1",          "prompt": "Explain the history of Rome",               "directive": "deep",      "n": null }
{ "block_id": "Singleton_1",     "prompt": "Explain the Singleton pattern in Java",     "directive": "expand",    "n": null }
```

---

## Step 1.1: Replace the Block Extraction Logic

**Replace lines 590-591** with the following:

```python
# --- Directive-aware block extraction ---
DIRECTIVE_RE = re.compile(
    r'\{\{(?:@(blueprint):(\d+)|@(deep)|@(expand))?\s*(.*?)\}\}',
    re.DOTALL
)
prompt_blocks = []
for i, m in enumerate(DIRECTIVE_RE.finditer(content)):
    if m.group(1) == "blueprint":
        directive = "blueprint"
        n = int(m.group(2))
        raw_prompt = m.group(5).strip()
    elif m.group(3) == "deep":
        directive = "deep"
        n = None
        raw_prompt = m.group(5).strip()
    elif m.group(4) == "expand":
        directive = "expand"
        n = None
        raw_prompt = m.group(5).strip()
    else:
        # No prefix — legacy blocks treated as @expand
        directive = "expand"
        n = None
        raw_prompt = m.group(5).strip()
    
    # Skip already-processed blueprint/deep comments
    if not raw_prompt:
        continue

    prompt_blocks.append({
        "block_id": f"{f.stem}_{i+1}",
        "prompt": raw_prompt,
        "directive": directive,
        "n": n
    })
```

**Key decisions embedded in the regex:**
- `@blueprint:N` — captured as groups 1 (literal "blueprint") and 2 (the integer N)
- `@deep` — captured as group 3
- `@expand` — captured as group 4
- No prefix — falls to the `else` branch, defaults to `"expand"` (full backwards compatibility)
- `group(5)` always captures the raw prompt text regardless of which prefix matched
- Empty `raw_prompt` after stripping means the block was an HTML comment or empty — skip it

---

## Step 1.2: Update the `scan_inbox` Tool Schema

The tool definition's description should be updated to mention the new fields so agents know to read them. In the tool schema at line ~257, add to the output description:

```
Each block object now includes:
  - block_id: string
  - prompt: string (directive prefix stripped)
  - directive: "expand" | "deep" | "blueprint"
  - n: integer (only for blueprint, null otherwise)
```

---

## Backwards Compatibility

All existing notes in `00_Inbox` that use bare `{{...}}` syntax without any directive prefix will be assigned `directive: "expand"` and `n: null`. The orchestrator treats `"expand"` identically to the current single-pass flow. **Zero breaking changes for existing notes.**

---

## Verification

Create `00_Inbox/Phase1_Directive_Test.md`:

```markdown
# Test File

{{@expand Explain the Singleton pattern in Java}}

{{@blueprint:3 Explain all GoF design patterns in Java}}

{{@deep Explain the history of the Roman Empire}}

{{Bare prompt with no directive prefix}}
```

Call `scan_inbox` and confirm the returned JSON:

```json
[
  {
    "filename": "Phase1_Directive_Test.md",
    "prompt_blocks": [
      {"block_id": "Phase1_Directive_Test_1", "prompt": "Explain the Singleton pattern in Java",           "directive": "expand",    "n": null},
      {"block_id": "Phase1_Directive_Test_2", "prompt": "Explain all GoF design patterns in Java",         "directive": "blueprint", "n": 3},
      {"block_id": "Phase1_Directive_Test_3", "prompt": "Explain the history of the Roman Empire",         "directive": "deep",      "n": null},
      {"block_id": "Phase1_Directive_Test_4", "prompt": "Bare prompt with no directive prefix",            "directive": "expand",    "n": null}
    ],
    "needs_split": false
  }
]
```

**Acceptance criteria:**
- [ ] `@blueprint:3` block has `directive: "blueprint"`, `n: 3`, prompt stripped of prefix
- [ ] `@deep` block has `directive: "deep"`, `n: null`
- [ ] `@expand` block has `directive: "expand"`, `n: null`
- [ ] Bare `{{...}}` block defaults to `directive: "expand"`, `n: null`
- [ ] No existing `Phase5_Split_Test.md` blocks are broken (re-run scan on it to confirm)
