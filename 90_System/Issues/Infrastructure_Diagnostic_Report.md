---
tags:
  - "#type/report"
  - "#field/cs"
  - "#subject/systems"
  - "#concept/mcp"
---
[[T.O.C (90_System)|Up to 90_System]]

# Infrastructure Diagnostic Report: Gemini CLI Ecosystem

> **Date:** 2026-02-27
> **Subject:** `C:\Users\ibtas\.gemini\` -- MCP Servers, Extensions, Custom Commands, Custom Tooling
> **Companion Report:** [[System_Prompt_Diagnostic_Report|GEMINI.md Diagnostic]]
> **Verdict:** The infrastructure is ambitious and well-designed in *concept*, but suffers from tool overlap, phantom dependencies, a critical path bug in `tools.py`, and exposed secrets in `settings.json`. Several commands reference tools/APIs that don't exist in the MCP configuration, creating silent failures.

---

## Table of Contents

1. [MCP Server Inventory & Analysis](#1-mcp-server-inventory--analysis)
2. [Extension Ecosystem Analysis](#2-extension-ecosystem-analysis)
3. [Custom Commands Diagnostic](#3-custom-commands-diagnostic)
4. [The `wisdom-os` MCP Server (tools.py)](#4-the-wisdom-os-mcp-server-toolspy)
5. [Architectural Strengths & Weaknesses](#5-architectural-strengths--weaknesses)
6. [Refactoring Strategy & Remediation](#6-refactoring-strategy--remediation)

---

## 1. MCP Server Inventory & Analysis

### 1.1 Server Manifest

| # | Server Name | Package / Command | Purpose | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `wisdom-os` | `python tools.py` | Custom vault operations (10 tools) | **BROKEN** (path bug) |
| 2 | `github` | `@modelcontextprotocol/server-github` | GitHub issues, PRs, repos | Active |
| 3 | `memory` | `@modelcontextprotocol/server-memory` | Knowledge graph (entities/relations) | Active |
| 4 | `filesystem` | `@modelcontextprotocol/server-filesystem` | Raw file R/W on D:\ | Active |
| 5 | `puppeteer` | `@modelcontextprotocol/server-puppeteer` | Browser automation / scraping | Active |
| 6 | `notebooklm-mcp` | `notebooklm-mcp` (binary) | NotebookLM integration | **UNVERIFIED** |
| 7 | `brave-search` | `@modelcontextprotocol/server-brave-search` | Web search | Active |
| 8 | `sequential-thinking` | `@modelcontextprotocol/server-sequential-thinking` | Structured reasoning chains | Active |

### 1.2 Context Bloat Contribution

Every MCP server adds to the context window in two ways:
1. **Tool definitions** -- each tool's name, description, and JSON schema are injected into the system prompt at session start.
2. **Tool results** -- each tool call's output consumes context tokens mid-conversation.

**Estimated tool definition overhead:**

| Server | # Tools (Approx) | Est. Schema Tokens | Notes |
| :--- | :--- | :--- | :--- |
| `wisdom-os` | 10 | ~800 | Largest custom server |
| `filesystem` | ~6 | ~500 | Overlaps with wisdom-os |
| `github` | ~15 | ~1,200 | Large schema surface |
| `memory` | ~5 | ~400 | Used by Memory Protocol |
| `puppeteer` | ~5 | ~400 | Only used by `/web:eat` |
| `brave-search` | ~2 | ~150 | Lightweight |
| `sequential-thinking` | ~1 | ~100 | Single tool |
| `notebooklm-mcp` | ~3 | ~200 | Unknown schema |
| **context7** (ext) | ~2 | ~150 | From extension |
| **google-workspace** (ext) | ~5 | ~400 | From extension |
| **nanobanana** (ext) | ~3 | ~250 | From extension |
| **TOTAL** | **~57** | **~4,550** | |

> [!CAUTION]
> **The combined tool schema overhead (~4,550 tokens) is roughly EQUAL to the entire `GEMINI.md` system prompt (~4,600 tokens).** This means the LLM's context window starts every session with ~9,000+ tokens of static overhead before the user even types a single character. Adding conversation + tool results, the context fills fast.

### 1.3 Critical Issue: Tool Overlap (`wisdom-os` vs `filesystem`)

Both servers can read and write files in the vault. This creates:

| Operation | `wisdom-os` tool | `filesystem` tool | Conflict |
| :--- | :--- | :--- | :--- |
| Read file | `read_note` | `read_file` | Dual path, LLM must choose |
| Write file | `create_note` | `write_file` | Different behaviors (wisdom-os adds headers) |
| List directory | `list_files` | `list_directory` | Identical functionality |
| Search | `search_vault` | (grep via filesystem) | Overlapping but different |
| Move file | `graduate_concept` | `move_file` | wisdom-os is scoped; filesystem is general |

**Impact:** The LLM must decide between two tools that do the same thing but with different interfaces, error behaviors, and path conventions. This leads to:
- Inconsistent tool selection across sessions
- Path format confusion (`wisdom-os` uses relative paths from vault root; `filesystem` uses absolute paths)
- The `sort.toml` command says "use `wisdom-os` (specifically `Notes`)" but no tool named "Notes" exists -- it likely means `create_note` or `read_note`

### 1.4 Security Issue: Exposed API Keys

> [!WARNING]
> `settings.json` contains **plaintext API keys** for:

>
> These should be moved to environment variables or a secrets manager. If this file is ever committed to a git repo or shared, these keys are compromised. **Rotate them immediately** if the file has been shared.

---

## 2. Extension Ecosystem Analysis

### 2.1 Extension Inventory

| Extension | Version | Has MCP Server | Context File | Status |
| :--- | :--- | :--- | :--- | :--- |
| `context7` | 1.0.0 | Yes (`@upstash/context7-mcp`) | No | Active |
| `google-workspace` | 0.0.4 | Yes (local `dist/index.js`) | `WORKSPACE-Context.md` | Active |
| `nanobanana` | 1.0.10 | Yes (local `mcp-server/dist/index.js`) | Via `GEMINI.md` (contextFileName) | Active |
| `youtube-to-docs` | N/A | **No manifest found** | N/A | **DEAD** |

All 4 are enabled globally via `extension-enablement.json` with override pattern `/C:/Users/ibtas/*`.

### 2.2 Issues

#### Dead Extension: `youtube-to-docs`
- Contains only a `.venv` directory (empty Python virtual environment).
- **No `gemini-extension.json`**, no source code, no built artifacts.
- Likely a failed installation or abandoned experiment.
- **Recommendation:** Delete the directory. It's dead weight in the extension scan.

#### Context File Collision: `nanobanana`
- The `nanobanana` extension declares `"contextFileName": "GEMINI.md"` in its manifest.
- This means it looks for a `GEMINI.md` file in extension-scoped directories for additional context.
- **Risk:** If the extension resolution logic picks up the *vault's* `GEMINI.md` (21KB), it would inject the entire system prompt a second time into context. This is a potential context doubling vector.

#### Extension Token Tax
Each extension with an MCP server adds its tool schemas to the context. The 3 active extension servers (context7, google-workspace, nanobanana) contribute an estimated **~800 additional tokens** of tool definitions, on top of the 8 core MCP servers.

#### `context7` API Key
The extension manifest references `${CONTEXT7_API_KEY}` as an environment variable. If this variable is not set in the system environment, the server will fail silently at startup, and `resolve-library-id` / `get-library-docs` tools will be unavailable without any error message to the LLM.

---

## 3. Custom Commands Diagnostic

### 3.1 Command Inventory

| Command | File | Category | Description | Est. Prompt Tokens |
| :--- | :--- | :--- | :--- | :--- |
| `/dev:new` | `dev/new.toml` | Development | Scaffold C++ project + Wisdom link | ~200 |
| `/os:boot` | `os/boot.toml` | Daily Ops | Generate daily note + email/calendar sync | ~600 |
| `/os:sort` | `os/sort.toml` | Inbox | Execute Inbox Processing Protocol | ~450 |
| `/os:spawn` | `os/spawn.toml` | System | Fork a new Gemini CLI instance | ~80 |
| `/os:sync` | `os/sync.toml` | System | Re-index D:\ into memory graph | ~120 |
| `/web:eat` | `web/eat.toml` | Knowledge | Scrape URL into Obsidian note | ~250 |

### 3.2 Phantom Tool References

Several commands reference tools or APIs that **do not exist** in the current MCP configuration:

| Command     | Referenced Tool/API                | Actual Status                                                                                                                                              |
| :---------- | :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/os:boot`  | `gmail-custom.list_messages(...)`  | **NOT CONFIGURED.** No `gmail-custom` MCP server exists in `settings.json`.                                                                                |
| `/os:boot`  | `calendar-personal.list_events`    | **NOT CONFIGURED.** No `calendar-personal` MCP server exists.                                                                                              |
| `/os:boot`  | `auth_path="D:/Auth/Personal"`     | **PATH UNVERIFIED.** `D:\Auth` is not in the Drive Architecture.                                                                                           |
| `/os:sort`  | `wisdom-os` "specifically `Notes`" | **NO SUCH TOOL.** wisdom-os has `create_note`, `read_note`, not `Notes`.                                                                                   |
| `/os:spawn` | `run_shell_command`                | **NAME MISMATCH.** Gemini CLI's tool is typically `run_in_terminal` or similar, not `run_shell_command`. The exact name depends on the Gemini CLI version. |
| `/dev:new`  | `memory` (Add Entity)              | Works, but the command doesn't specify the memory tool explicitly -- it relies on the LLM inferring the correct `create_entities` call.                    |

> [!IMPORTANT]
> **`/os:boot` is fundamentally broken.** It references `gmail-custom` and `calendar-personal` MCP servers that don't exist. The `google-workspace` extension *might* provide similar functionality, but the command prompt uses different API names. This means every `/os:boot` execution either:
> 1. Silently skips the email/calendar phases (if the LLM gracefully handles missing tools)
> 2. Hallucinates fake email summaries (if the LLM tries to fulfill the instruction without the tool)
> 3. Errors out visibly

### 3.3 `/os:sort` -- The Dangerous Delegator

`/os:sort` is the operational manifestation of the Inbox Processing Protocol from `GEMINI.md`. Its design has a critical architectural flaw:

**It delegates to `GEMINI.md` by reference rather than by content.**

```toml
# From sort.toml
"Apply Kernel Logic (Refactor & Sort):
 Refer strictly to the Kybernetes Processing Protocol in GEMINI.md (Section 00_Inbox)."
```

This means the LLM must:
1. Receive the `/os:sort` command prompt (~450 tokens)
2. *Also* have `GEMINI.md` in context (~4,600 tokens)
3. Cross-reference the two documents
4. Execute the combined logic

**The problem:** If `GEMINI.md` is in context (loaded as a system prompt), the LLM has ~5,000 tokens of instructions to juggle. If it's *not* in context, the command tells it to "refer strictly" to a document it can't see. Either way, the cross-referencing increases cognitive load and error probability.

### 3.4 `/os:boot` -- Over-Ambitious Daily Ritual

The boot command attempts to orchestrate **7 distinct tool calls** in sequence:
1. Read Timetable file
2. Read Deadlines file
3. List Gmail messages (broken)
4. List Calendar events (broken)
5. Query memory
6. Query GitHub issues
7. Create daily note + brain dump file

Even with all tools available, this is an aggressive sequence. The LLM must:
- Synthesize outputs from 7 different sources
- Apply priority logic (deadline urgency, bug severity, memory focus)
- Generate a structured markdown note with correct internal links

**With 2 of 7 tools broken**, the command is guaranteed to produce incomplete output.

### 3.5 Command Strengths

| Command | Assessment |
| :--- | :--- |
| `/dev:new` | **Well-designed.** Clear 3-step process (Physical -> Logical -> Memory). Low complexity. Self-contained. |
| `/os:spawn` | **Elegant.** Minimal prompt, delegates to a Python script. Clean separation of concerns. |
| `/os:sync` | **Solid concept.** Simple reconciliation logic. Could be improved with a diff output format. |
| `/web:eat` | **Good design.** Clear pipeline: Acquire -> Refactor -> Persist. Correctly uses `puppeteer` for scraping. |

---

## 4. The `wisdom-os` MCP Server (`tools.py`)

### 4.1 Critical Bug: Wrong Vault Root Path

> [!CAUTION]
> **Line 24 of `tools.py`:**
> ```python
> VAULT_ROOT = Path(r"D:\WISDOM\WISDOM")
> ```
> **This is WRONG.** The actual vault root is `D:\WISDOM\Kybernetes`.
>
> **Impact:** Every single tool in the `wisdom-os` server -- `list_files`, `search_vault`, `read_note`, `create_note`, `append_to_note`, `graduate_concept`, `init_project`, `daily_log`, `get_daily_plan` -- is operating on a **nonexistent directory**. All calls will return "not found" errors or silently create files in the wrong location.

### 4.2 Tool Inventory

| # | Tool | Purpose | Quality |
| :--- | :--- | :--- | :--- |
| 1 | `list_files` | List folder contents | Good, but overlaps with `filesystem` |
| 2 | `search_vault` | Keyword search across all `.md` files | **Slow** -- reads every file sequentially |
| 3 | `read_note` | Read a note by path or fuzzy filename | Good -- has intelligent fallback |
| 4 | `create_note` | Create new note with auto-placement | Good -- defaults to Inbox |
| 5 | `append_to_note` | Append text to existing note | Good |
| 6 | `graduate_concept` | Move note from Inbox/University to CS_Core | **Good** -- unique, no overlap |
| 7 | `init_project` | Scaffold project in 40_Projects | Good -- unique |
| 8 | `daily_log` | Log to today's daily note | Good -- unique |
| 9 | `get_daily_plan` | Read today's/tomorrow's daily note | Good -- unique |

### 4.3 Code Quality Issues

| Issue | Location | Severity | Detail |
| :--- | :--- | :--- | :--- |
| **Wrong VAULT_ROOT** | L24 | **CRITICAL** | `D:\WISDOM\WISDOM` should be `D:\WISDOM\Kybernetes` |
| Bare `except` | L170 | Medium | `except:` catches *everything*, including `KeyboardInterrupt`. Use `except Exception:` |
| No input validation | L155-161 | Medium | `list_files` doesn't sanitize `folder` -- path traversal risk (e.g., `../../`) |
| `search_vault` performance | L162-174 | Medium | Reads *every* `.md` file in the vault on each call. No indexing, no caching. |
| Variable shadowing | L240 | Low | `name = arguments.get("name")` shadows the function parameter `name: str` |
| Missing `required` fields | L43-44 | Low | `list_files` doesn't mark `folder` as required, so `arguments.get("folder", "")` defaults to vault root -- this is intentional but undocumented |
| No T.O.C linking | L188-201 | Medium | `create_note` doesn't add T.O.C links, violating the Graph Architecture rule that every note must link to its parent T.O.C |
| No tagging | L188-201 | Medium | `create_note` doesn't add the required `field/subject/concept` tags to YAML frontmatter |

### 4.4 Missing Tools

Given the commands and `GEMINI.md` workflows, these tools are conspicuously absent from `wisdom-os`:

| Missing Tool | Needed By | Purpose |
| :--- | :--- | :--- |
| `move_note` | `/os:sort`, Inbox processing | Move a note between vault folders (general-purpose version of `graduate_concept`) |
| `update_toc` | All note creation workflows | Auto-add new notes to the parent T.O.C |
| `add_frontmatter` | All note creation workflows | Add/update YAML frontmatter (tags, dates) |
| `split_note` | `/os:sort`, Inbox processing | Atomically split a multi-topic note into separate files |
| `rename_note` | `/os:sort` | Rename a note with proper vault link updates |

---

## 5. Architectural Strengths & Weaknesses

### 5.1 Strengths

| Component                                    | Why It Works                                                                                                             |
| :------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Command taxonomy** (`dev/`, `os/`, `web/`) | Clean separation by domain. Discoverable and intuitive.                                                                  |
| **`/dev:new` pattern**                       | Textbook example of a well-scoped command: Physical -> Logical -> Memory, with clear outputs.                            |
| **`wisdom-os` as a domain-specific MCP**     | Correct instinct -- vault operations *should* be abstracted behind a purpose-built API rather than raw filesystem calls. |
| **`/os:spawn` delegation**                   | Properly delegates to a Python script instead of trying to orchestrate shell commands in the prompt.                     |
| **Extension enablement config**              | Global override pattern is clean and maintainable.                                                                       |

### 5.2 Weaknesses

| Weakness | Impact | Fix Complexity |
| :--- | :--- | :--- |
| **`tools.py` path bug** | All wisdom-os tools broken | Trivial (1-line fix) |
| **Phantom tool references** | `/os:boot` email/calendar broken | Medium (need to configure or remove) |
| **Tool overlap** (wisdom-os + filesystem) | Inconsistent tool selection, context bloat | Medium (consolidate or scope) |
| **No error propagation** | Commands fail silently or hallucinate | Medium (add error handling) |
| **Exposed API keys** | Security vulnerability | Trivial (move to env vars) |
| **Dead extension** (youtube-to-docs) | Wasted scan cycle | Trivial (delete) |
| **Missing essential tools** | Sort/split must be done via LLM reasoning | High (implement in tools.py) |
| **Commands don't validate tool availability** | LLM discovers missing tools mid-execution | Medium (add preflight checks) |

---

## 6. Refactoring Strategy & Remediation

### 6.1 Priority 1: Critical Fixes (Do Immediately)

#### Fix 1: Correct `tools.py` VAULT_ROOT
```diff
- VAULT_ROOT = Path(r"D:\WISDOM\WISDOM")
+ VAULT_ROOT = Path(r"D:\WISDOM\Kybernetes")
```

#### Fix 2: Rotate Exposed API Keys
2. Generate a new token with the same scopes
3. Move both keys to environment variables:

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}" }
}
```

#### Fix 3: Delete Dead Extension
Delete `C:\Users\ibtas\.gemini\extensions\youtube-to-docs\` entirely.

### 6.2 Priority 2: Fix Broken Commands

#### Fix `/os:boot`
**Option A (Recommended):** Remove the email/calendar phases until the `google-workspace` extension is properly configured:
```toml
# Remove Phase 1.2 (Digital HQ) entirely
# Add a comment: "# TODO: Re-enable when google-workspace MCP provides gmail/calendar tools"
```

**Option B:** Map the existing `google-workspace` extension's actual tools into the boot command. This requires inspecting the `google-workspace` MCP server's tool names (from `dist/index.js`) and updating the command prompt to use the correct API.

#### Fix `/os:sort` Tool Reference
Change "use `wisdom-os` (specifically `Notes`)" to "use `wisdom-os` tools: `read_note`, `create_note`, `list_files`".

### 6.3 Priority 3: Reduce Tool Overlap

**Strategy: Scope each server to its domain.**

| Server | Scoped Purpose | Remove From |
| :--- | :--- | :--- |
| `wisdom-os` | All vault-internal operations (notes, T.O.C, tags, search) | -- |
| `filesystem` | Physical drive operations (`D:\PROJECTS`, `D:\Languages`, `D:\Inbox`, `D:\Media`) | Remove `D:\WISDOM` from filesystem args |

```diff
  "filesystem": {
    "command": "npx",
    "args": [
      "-y", "@modelcontextprotocol/server-filesystem",
      "D:\\PROJECTS",
      "D:\\Languages",
      "D:\\University",
      "D:\\Inbox",
-     "D:\\Media",
-     "D:\\WISDOM"
+     "D:\\Media"
    ]
  }
```

This forces the LLM to use `wisdom-os` for vault operations and `filesystem` for physical drive operations -- matching the Brain/Body separation in `GEMINI.md`.

### 6.4 Priority 4: Expand `wisdom-os` to Match Workflows

Add these tools to `tools.py` to eliminate the need for LLM-orchestrated file operations during Inbox processing:

| New Tool | Purpose | Eliminates |
| :--- | :--- | :--- |
| `move_note(src, dest)` | Move any note between vault folders | LLM guessing between wisdom-os and filesystem for moves |
| `split_note(path, sections[])` | Split a multi-topic note into atomic files | LLM manually reading, extracting, writing, deleting |
| `ensure_toc_link(note_path)` | Auto-add note to nearest parent T.O.C | LLM forgetting to update T.O.C links |
| `add_frontmatter(path, tags[])` | Auto-add YAML frontmatter with proper tags | LLM forgetting tags or using wrong format |

### 6.5 Priority 5: Context Budget Optimization

**Current per-session static overhead:**

| Source | Est. Tokens | Reducible? |
| :--- | :--- | :--- |
| `GEMINI.md` system prompt | ~4,600 | Yes (see companion report) |
| MCP tool schemas (11 servers) | ~4,550 | Yes |
| Global memory files (GEMINI.md + GEMINI_g.md) | ~100 | No |
| **TOTAL** | **~9,250** | |

**Reduction strategies:**

1. **Remove `D:\WISDOM` from filesystem** (Priority 3 above) -- saves ~500 tokens of duplicate file tools.
2. **Disable `puppeteer` globally** -- it's only used by `/web:eat`. Enable it only in sessions where scraping is needed, or move it to an extension that activates on demand.
3. **Evaluate `notebooklm-mcp`** -- if rarely used, disable to save its schema tokens.
4. **Slim `wisdom-os` descriptions** -- the tool descriptions in `tools.py` are already reasonably concise, but `search_vault`'s description ("Semantic-like search") is misleading -- it's a literal substring match, not semantic. Fix the description to avoid the LLM expecting fuzzy/embedding-based results.

**Projected savings:**

| Action | Tokens Saved |
| :--- | :--- |
| Remove WISDOM from filesystem scope | ~500 |
| Disable puppeteer (on-demand only) | ~400 |
| Disable notebooklm-mcp (if unused) | ~200 |
| GEMINI.md refactoring (companion report) | ~2,900 |
| **TOTAL** | **~4,000** |

**Result: ~9,250 -> ~5,250 tokens static overhead (43% reduction).**

---

## Appendix: Cross-Reference with `GEMINI.md` Report

| GEMINI.md Issue | Infrastructure Implication |
| :--- | :--- |
| Shell-Pipe Protocol hallucinations | Child instance has GEMINI.md (same CWD), but NOT the MCP servers. The child runs with default tools only. |
| "Use `sequentialthinking` tool" mandate | Depends on `sequential-thinking` MCP server being available. Works in current config, but fails if server crashes. |
| Memory Protocol (save entities) | Depends on `memory` MCP server. Works in current config. |
| Template selection during Inbox processing | Templates should be loadable via `wisdom-os.read_note` -- but `tools.py` has wrong VAULT_ROOT, so this fails. |
| "Use Template for creation" convention | `wisdom-os.create_note` doesn't apply any template -- it creates a bare note with only a title and timestamp. |
