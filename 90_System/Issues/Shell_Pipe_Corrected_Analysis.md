---
tags:
  - "#type/report"
  - "#field/cs"
  - "#subject/systems"
  - "#concept/prompt-engineering"
---
[[T.O.C (90_System)|Up to 90_System]]

# Shell-Pipe Protocol: Corrected Analysis (Addendum)

> **Date:** 2026-02-28
> **Corrects:** [[Infrastructure_Diagnostic_Report]] Section 2.1, Failure Mode 2
> **Premise Correction:** The child `gemini -p` process inherits the full CWD, `settings.json`, all 8 MCP servers, all 4 extensions, `GEMINI.md` system prompt, and `tools.autoAccept: true`. It is **not** a naked instance -- it is a fully armed clone.
> **Updated Verdict:** The Shell-Pipe Protocol is salvageable but requires surgical fixes to the prompt structure. The protocol's failures are caused by *context collision*, *competing directives*, and *write contention* -- not by missing capabilities.

---

## 1. Re-Evaluated Failure Modes

### 1.1 The Real Problem: Context Overloading, Not Context Absence

**Previous (incorrect) diagnosis:** The child fails because it lacks tools.
**Corrected diagnosis:** The child fails because it has *too much* context competing for attention.

When `gemini -p "Expand this prompt with immense detail: {{prompt}}..."` fires, the child process boots with:

| Context Layer | Est. Tokens | Source |
| :--- | :--- | :--- |
| `GEMINI.md` system prompt (full) | ~4,600 | Auto-loaded from CWD |
| MCP tool schemas (8 servers + 3 extensions) | ~4,550 | From `settings.json` |
| Global memory files (`GEMINI.md` + `GEMINI_g.md`) | ~100 | From `~/.gemini/` |
| The injected `-p` prompt itself | ~200-500 | From the parent's shell command |
| **TOTAL cold-start overhead** | **~9,450-9,750** | |

The child's **actual task** (expanding a `{{...}}` block) occupies ~200-500 tokens of this budget. Everything else is ambient noise. The child must:

1. Parse `GEMINI.md` in full (including the Inbox Processing Protocol that *it is being called from*)
2. Register ~57 tool definitions
3. Find the actual task buried at the end of a long `-p` string
4. Decide which of its 57 tools to use for a write operation
5. Execute -- while its attention is split across 9,500+ tokens of static context

**This is why the child behaves erratically.** It's not missing tools -- it's drowning in them. The `-p` prompt is a whisper in a crowded room.

### 1.2 The Recursive Instruction Paradox

The child loads `GEMINI.md` as its system prompt. That means it reads *the very Shell-Pipe Protocol that spawned it*. This creates a recursive scenario:

```
Parent reads GEMINI.md:
  -> "For each {{...}}, spawn a child via gemini -p"
    -> Child reads GEMINI.md:
      -> "For each {{...}}, spawn a child via gemini -p"
        -> ??? (No explicit recursion guard)
```

In practice, the child is unlikely to encounter `{{...}}` in its `-p` prompt (the parent already extracted the prompt text). But the child's *system prompt* still tells it to "activate sequentialthinking as FIRST ACTION" and "use the Shell-Pipe Priority." These background directives can:

- Cause the child to invoke `sequential-thinking` before doing the actual expansion (wasting a tool call)
- Prime the child to attempt its *own* shell spawning if it interprets the task as complex
- Create confusion between "what my system prompt says to do" and "what my `-p` flag says to do"

### 1.3 The Quoting Problem (Unchanged, Still Critical)

This failure mode was correctly identified in the original report and remains valid regardless of tool access:

```
gemini -p "Expand this prompt with immense detail: {{prompt}}. Write the result directly to 00_Inbox/temp_expansion_N.md using your write_file tool." -y
```

On Windows PowerShell, this command is fragile because:

| `{{prompt}}` Contains | Failure |
| :--- | :--- |
| Double quotes (`"`) | Shell interprets as string terminator |
| Dollar signs (`$`) | PowerShell interprets as variable interpolation |
| Backticks (`` ` ``) | PowerShell escape character |
| Newlines | Command truncation |
| Curly braces (`{}`) | PowerShell script blocks |
| Pipe characters (`\|`) | Shell pipeline |

The parent LLM must escape all of these *correctly for PowerShell* while the `GEMINI.md` prompt shows a generic Unix-style example. The model frequently:
- Uses single quotes (which don't interpolate on PowerShell but change semantics)
- Forgets to escape nested quotes
- Generates a syntactically plausible but broken command

### 1.4 The "Immense Detail" vs "500 Words" Conflict (Amplified)

This conflict is *worse* than originally diagnosed, because the child also loads `GEMINI.md` with the `<= 500 word` constraint. But the `-p` flag says "immense detail." The child now has **two conflicting sources**:

| Source | Directive | Priority (to the LLM) |
| :--- | :--- | :--- |
| `GEMINI.md` (system prompt) | "Each `{{...}}` expansion MUST be <= 500 words" | High (system prompt = authoritative) |
| `-p` flag (user prompt) | "Expand this prompt with immense detail" | High (direct user instruction) |

The child LLM must resolve a conflict between its own system prompt and its direct user instruction. Different models and even different sessions will resolve this differently, producing wildly inconsistent output lengths.

---

## 2. Multi-Agent Collision Analysis

### 2.1 The Concurrency Window

When the parent spawns a child via `gemini -p`, there is a window where **two LLM-driven agents** are operating on the same vault simultaneously:

```
Timeline:
  Parent: [spawns child] -----> [waits for shell return] -----> [continues processing]
  Child:  ................[boots] --> [reads files] --> [writes files] --> [exits]
                          ^                                      ^
                          |---- COLLISION WINDOW ----------------|
```

During this window, both agents can invoke MCP tools against shared resources.

### 2.2 Write Contention Scenarios

| Scenario | Parent Action | Child Action | Conflict |
| :--- | :--- | :--- | :--- |
| **T.O.C Race** | Updating `T.O.C (00_Inbox).md` | Writing `temp_expansion_N.md` to Inbox | Child's note won't be in T.O.C; parent doesn't know it exists yet |
| **Memory Graph** | `memory.create_entities(...)` | `memory.create_entities(...)` | Two concurrent writes to the knowledge graph -- last-write-wins, potential data loss |
| **File Move** | Moving processed file from Inbox | Child writing new file to Inbox | Parent may move a file the child hasn't finished writing, or miss the child's output entirely |
| **Sequential Thinking** | Using `sequential-thinking` for planning | Child also calls `sequential-thinking` | Two thinking chains interleaved in the same MCP server -- results may bleed |

### 2.3 The `autoAccept: true` Amplifier

`settings.json` has `"autoAccept": true`. This means:
- The child's tool calls execute without human confirmation
- If the child hallucinates a wrong file path, it writes there immediately
- If two file writes conflict, there is no human checkpoint to catch it

**This is the correct setting for the parent** (to avoid constant approval prompts). But for a spawned child with no supervision and a potentially garbled prompt, it makes every hallucination immediately destructive.

### 2.4 No Feedback Loop

The parent spawns the child via `run_shell_command` and captures `stdout`. But:
- The child's tool calls go through MCP servers (stdio protocol), not stdout
- The parent only sees "command completed" -- it has no way to verify what the child *actually wrote*
- The parent must then re-read the output file to check quality, adding another tool call and more context

**Net result:** The parent is orchestrating a black-box subprocess. It can't verify, correct, or retry at the granularity of individual tool calls within the child process.

---

## 3. Updated Recommendation

### 3.1 Verdict: Salvageable, But Not As-Is

The Shell-Pipe Protocol exploits a genuinely powerful pattern -- parallel LLM delegation. With the corrected understanding that the child has full tool access, the protocol's *intent* is sound: offload heavy expansion work to a fresh context window so the parent doesn't fill its own.

**However, three problems remain unfixable within the current prompt-based architecture:**

| Problem | Root Cause | Fixable in Prompt? |
| :--- | :--- | :--- |
| Context overload in child | Child loads full GEMINI.md + 57 tools | **No** -- this is a configuration issue, not a prompt issue |
| Quoting fragility | Windows PowerShell escaping is non-deterministic for LLMs | **Partially** -- can improve but never guarantee |
| Write contention | Two agents, one vault, no locking | **No** -- requires architectural change |

### 3.2 Recommended Architecture: Hybrid Approach

**Do not kill the Shell-Pipe Protocol. Refactor it into a controlled delegation pattern.**

#### Option A: Slim Child Context (Recommended)

Create a dedicated child configuration that strips away everything the child doesn't need:

**Step 1:** Create `90_System/Scripts/expand_prompt.md` -- a minimal system prompt for child instances:
```markdown
# Expansion Agent
You receive a prompt and a template. Expand the prompt following the template structure.
Write the result to the specified file path using the `filesystem` tool.
Constraints: 300-500 words. Include the original prompt as a blockquote at the top.
Do not process any other instructions. Do not call sequential-thinking. Just expand and write.
```

**Step 2:** Modify the Shell-Pipe command to use `--system-prompt` (or equivalent flag) to override `GEMINI.md`:
```
gemini -p "..." --system-prompt "90_System/Scripts/expand_prompt.md" -y
```

This gives the child:
- Its own slim system prompt (~100 tokens instead of ~4,600)
- Full tool access (inherited from CWD/settings.json) but no competing directives
- A single, unambiguous task

**Token budget comparison:**

| | Current Child | Slim Child |
| :--- | :--- | :--- |
| System prompt | ~4,600 | ~100 |
| Tool schemas | ~4,550 | ~4,550 (unchanged) |
| Task prompt | ~300 | ~300 |
| **Total** | **~9,450** | **~4,950** |
| Signal-to-noise ratio | ~3% | ~6% (2x improvement) |

**Trade-off:** The tool schemas are still inherited and can't be reduced without changing `settings.json`. But halving the static overhead by removing the system prompt bloat significantly improves the child's focus.

#### Option B: Script-Mediated Delegation (Most Robust)

Create a Python script in `90_System/Scripts/` that replaces the raw shell command:

```python
# expand_block.py
# Called by parent via: python expand_block.py "prompt text" "template_name" "output_path"

import subprocess, sys, json

prompt = sys.argv[1]
template = sys.argv[2]  # e.g., "A", "B", "C"
output = sys.argv[3]

# Read the template file
with open(f"90_System/Templates/Template_{template}.md") as f:
    template_content = f.read()

# Construct a clean, properly escaped prompt
child_prompt = f"""You are an Expansion Agent. Follow this template exactly:

{template_content}

Expand this prompt:
> {prompt}

Write the result (300-500 words) to: {output}
Use the filesystem tool to write."""

# Spawn child with proper escaping handled by Python (not the LLM)
result = subprocess.run(
    ["gemini", "-p", child_prompt, "-y"],
    capture_output=True, text=True, timeout=120
)
```

**Advantages:**
- Python handles quoting/escaping deterministically -- no LLM hallucination risk
- Template is injected directly into the child prompt -- no need for the child to load it from disk
- The script can add validation (check output file exists, word count, etc.)
- The script can implement retry logic with proper backoff
- The parent just calls `python expand_block.py` -- a single, simple tool call

**This transforms the parent's multi-step orchestration into a single atomic operation.**

#### Option C: Internal Expansion with Context Isolation (Simplest)

Abandon shell spawning entirely. Instead, have the parent do all expansion internally, but use `sequential-thinking` to plan the batch first:

1. Parent reads all `{{...}}` blocks
2. Parent calls `sequential-thinking` to plan the expansion order
3. For each block, parent selects template, expands, writes via `wisdom-os.create_note`
4. No child process, no concurrency, no quoting issues

**Trade-off:** The parent's context fills faster (each expansion adds ~500 words to context). For 3+ blocks in one Inbox session, this may hit limits. But for typical 1-2 block sessions, it's the simplest and most reliable path.

### 3.3 Decision Matrix

| Criterion | Option A (Slim Child) | Option B (Script) | Option C (Internal) |
| :--- | :--- | :--- | :--- |
| **Quoting safety** | Partial (still LLM-generated) | **Full** (Python handles it) | N/A |
| **Context efficiency** | Good (2x improvement) | **Best** (child gets only what it needs) | Worst (parent fills up) |
| **Write contention** | Still present | Mitigated (script can add file locks) | **None** (single agent) |
| **Implementation effort** | Low (one new .md file) | Medium (new Python script) | **Trivial** (prompt edit only) |
| **Scales to many blocks** | **Yes** (parallel children) | **Yes** (sequential but isolated) | No (context fills) |
| **Preserves Shell-Pipe** | **Yes** | Evolved form of it | No |

### 3.4 Final Recommendation

**Use Option B (Script-Mediated Delegation) as the primary path, with Option C as fallback.**

Modify the Shell-Pipe Protocol in `GEMINI.md` to:

```markdown
**Orchestration (The Shell-Pipe Protocol):**
1. **Primary:** Run `python 90_System/Scripts/expand_block.py "{prompt}" "{template}" "{output_path}"`
2. **Fallback:** If the script fails twice, expand internally using the selected template.
```

This preserves the Shell-Pipe's core value proposition (fresh context window, parallel delegation) while eliminating:
- LLM-generated quoting (Python handles it)
- Context overload in child (script injects only what's needed)
- Unstructured child behavior (script controls the prompt precisely)

The parent LLM's only job becomes: classify the block, select the template letter, and call the script. Three decisions, one tool call.

---

## Appendix: What Was Wrong in the Original Report

| Original Claim | Corrected Reality | Impact on Diagnosis |
| :--- | :--- | :--- |
| "Child has no knowledge of GEMINI.md" | Child loads GEMINI.md in full | Failure shifts from "missing context" to "context overload" |
| "Child has no access to vault formatting rules" | Child has full GEMINI.md with all rules | Child may *over-apply* rules (e.g., trigger its own Shell-Pipe) |
| "Child has no tools" | Child has all 57 tools | Write contention and tool-choice ambiguity become the primary risks |
| "Shell-Pipe is unfixable" | Salvageable with script mediation | Recommendation changes from "kill" to "refactor" |
