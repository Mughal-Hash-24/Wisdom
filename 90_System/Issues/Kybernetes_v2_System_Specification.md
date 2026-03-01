---
tags:
  - "#type/spec"
  - "#field/cs"
  - "#subject/systems"
  - "#concept/architecture"
---
[[T.O.C (90_System)|Up to 90_System]]

# Kybernetes OS v2: Detailed System Specification

> **Date:** 2026-02-28
> **Architecture:** Merged Blueprint C+D (Hybrid Kernel with Sub-Agent Swarm)
> **Guiding Principle:** *"Deterministic tools for mechanical work. Atomic agents for judgment calls. Commands as hardware interrupts."*

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Layer 0: GEMINI.md (The Slim Kernel)](#2-layer-0-geminimd-the-slim-kernel)
3. [Layer 1: Custom Commands (Hardware Interrupts)](#3-layer-1-custom-commands-hardware-interrupts)
4. [Layer 2: Agent Skills (Interrupt Handlers)](#4-layer-2-agent-skills-interrupt-handlers)
5. [Layer 3: Sub-Agents (Specialist Units)](#5-layer-3-sub-agents-specialist-units)
6. [Layer 4: wisdom-os v2 (System Calls)](#6-layer-4-wisdom-os-v2-system-calls)
7. [Layer 5: MCP Server & Extension Configuration](#7-layer-5-mcp-server--extension-configuration)
8. [Workflow Specifications](#8-workflow-specifications)
9. [Old vs New: Full Migration Map](#9-old-vs-new-full-migration-map)
10. [File Tree: Complete Deliverables](#10-file-tree-complete-deliverables)

---

## 1. System Architecture Overview

### 1.1 The Execution Stack

```
┌─────────────────────────────────────────────────────────┐
│  Layer 0: GEMINI.md (~1,400 tokens)                     │
│  ├── Vault identity, structure, routing table            │
│  ├── Behavioral directives (3 sentences)                 │
│  └── Registry of skills, agents, and tools               │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Custom Commands (/os:sort, /os:boot, etc.)    │
│  └── Deterministic trigger -> forces specific skill      │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Agent Skills (SKILL.md workflows)              │
│  ├── inbox-sort    (Inbox processing pipeline)           │
│  ├── daily-boot    (Daily note generation)               │
│  ├── web-ingest    (URL scraping to note)                │
│  ├── project-init  (Project scaffolding)                 │
│  ├── drive-sync    (Memory graph reconciliation)         │
│  └── prompt-expand (Template expansion logic)            │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Sub-Agents (@expander, @librarian)             │
│  ├── @expander  -- Expands {{...}} blocks using template │
│  └── @librarian -- Manages T.O.C, frontmatter, graph    │
├─────────────────────────────────────────────────────────┤
│  Layer 4: wisdom-os v2 MCP Tools (Python)                │
│  ├── scan_inbox, move_note, split_note                   │
│  ├── ensure_toc_link, add_frontmatter                    │
│  ├── create_note (v2), read_note, search_vault           │
│  ├── load_template, expand_block                         │
│  └── graduate_concept, init_project, daily_log           │
├─────────────────────────────────────────────────────────┤
│  Layer 5: External MCP Servers + Extensions              │
│  ├── filesystem (scoped: D:\ minus D:\WISDOM)            │
│  ├── memory, github, brave-search, sequential-thinking   │
│  ├── puppeteer, notebooklm-mcp                           │
│  └── Extensions: context7, google-workspace, nanobanana  │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Design Rules

| Rule | Rationale |
| :--- | :--- |
| The LLM never reads/writes vault files directly via `filesystem` | All vault mutations go through `wisdom-os` tools (single API, consistent behavior) |
| Commands always name the skill they invoke | Guarantees the LLM loads the right SKILL.md (no probabilistic discovery) |
| Skills orchestrate, tools execute | Skills contain the *sequence*; tools contain the *implementation* |
| Sub-agents are dispatched by skills, not by the user | The skill decides when specialist help is needed |
| Every note creation MUST call `ensure_toc_link` + `add_frontmatter` | Enforced by the tools, not by LLM memory |

---

## 2. Layer 0: GEMINI.md (The Slim Kernel)

### 2.1 Old vs New

| Aspect | Old GEMINI.md | New GEMINI.md |
| :--- | :--- | :--- |
| **Lines** | 388 | ~90 |
| **Est. Tokens** | ~4,600 | ~1,400 |
| **Contains templates?** | Yes (6 templates, ~1,400 tokens) | No (moved to skill: `prompt-expand`) |
| **Contains Inbox protocol?** | Yes (176 lines of procedural logic) | No (moved to skill: `inbox-sort`) |
| **Contains personas?** | Yes (2 full persona blocks, ~350 tokens) | Merged into 3-sentence behavioral directive |
| **Contains mental models?** | Yes (17 names, ~300 tokens) | No (remain in `90_System/Agents/Gemini/`, loaded on-demand) |
| **Contains drive architecture?** | Yes (unchanged) | Yes (unchanged -- it's declarative, low cost) |
| **Contains directory routing?** | Yes (unchanged) | Yes (unchanged) |

### 2.2 New GEMINI.md Structure

```markdown
# Obsidian Vault Context: KYBERNETES

## Project Overview
[Keep lines 1-6 unchanged -- Hybrid PARA description]

## Graph Architecture & Linking Strategy
[Keep lines 8-34 unchanged -- T.O.C backbone, tagging, graph aesthetics]

# SYSTEM KERNEL: KYBERNETES OS

## 1. Identity & Mission
You are **Kybernetes** ("The Steersman") -- the OS Kernel for a CS student.
You manage two domains:
- **The Brain:** Obsidian Vault (`D:\WISDOM\Kybernetes`) -- use `wisdom-os` tools exclusively.
- **The Body:** Physical Drive (`D:\`) -- use `filesystem` tool.

## 2. Bridge Protocol
[Keep lines 45-49 unchanged -- mapping logic]

## 3. Drive Architecture
[Keep lines 53-83 unchanged -- partition map with access rules]

## 4. Directory Routing Table
[Keep lines 282-329 unchanged -- 10_University through 90_System descriptions]

## 5. Behavioral Directives
For CS/Technical topics: lead with internals and mechanics, use real-world
analogies for grounding, identify edge cases and trade-offs. Reserve C++
anchors (Pointers, Stack/Heap) for programming language and low-level topics.

For General Knowledge topics: trace root causes via first principles, connect
to broader systems (Game Theory, Psychology, Economics), cite evidence.

All outputs: zero preamble. Start with the definition or architecture. Aim
for 300-500 words per atomic concept. No emojis.

## 6. Conventions
1. Always use Obsidian templates (via Templater) for new notes.
2. Move fully synthesized concepts from `10_University` to `20_CS_Core`.
3. Always link to parent T.O.C (enforced by `ensure_toc_link` tool).
4. Always add YAML frontmatter with field/subject/concept tags.

## 7. System Registry
- **Skills:** `.gemini/skills/` -- workflows for sort, boot, expand, ingest
- **Agents:** `.gemini/agents/` -- @expander, @librarian
- **Tools:** `wisdom-os` MCP -- all vault operations
- **Mental Models:** `90_System/Agents/Gemini/*.md` -- load via `read_note` when needed
- **Templates:** `90_System/Templates/Template_{A-F}.md` -- loaded by prompt-expand skill

## 8. Memory Protocol
Silently save to the `memory` tool whenever the user defines a new project,
states a preference, mentions a struggle, or provides personal context.
This is always permitted regardless of other constraints.
```

### 2.3 What Was Removed & Where It Went

| Removed Section | Old Lines | Token Cost | New Location |
| :--- | :--- | :--- | :--- |
| Inbox Processing Protocol | 89-118 | ~550 | `.gemini/skills/inbox-sort/SKILL.md` |
| Template Selection Logic | 120-127 | ~100 | `.gemini/skills/prompt-expand/SKILL.md` |
| Templates A-F | 129-265 | ~1,400 | `90_System/Templates/Template_{A-F}.md` |
| Surgeon Rule | 267-270 | ~80 | `.gemini/skills/inbox-sort/SKILL.md` (scoped) |
| Memory Protocol triggers | 272-280 | ~120 | Compressed into 3 lines in new Section 8 |
| Personas (Chief Engineer + Navigator) | 334-354 | ~350 | Merged into Section 5 (3 sentences) |
| Mental Model catalog | 356-382 | ~300 | Deleted from prompt; files stay in `90_System/Agents/Gemini/` |

**Total tokens reclaimed: ~2,900 from GEMINI.md itself.**

---

## 3. Layer 1: Custom Commands (Hardware Interrupts)

### 3.1 Old vs New

| Command | Old Behavior | New Behavior |
| :--- | :--- | :--- |
| `/os:sort` | Inlines procedural logic + references GEMINI.md | Triggers `inbox-sort` skill explicitly |
| `/os:boot` | Orchestrates 7 tool calls inline; references phantom tools | Triggers `daily-boot` skill; phantom tools removed |
| `/os:spawn` | Spawns raw `gemini -p` via Python script | **Deprecated** -- replaced by native sub-agent dispatch |
| `/os:sync` | Inline reconciliation logic | Triggers `drive-sync` skill |
| `/dev:new` | Inline 3-step scaffold logic | Triggers `project-init` skill |
| `/web:eat` | Inline scraping pipeline | Triggers `web-ingest` skill |

### 3.2 New Command Specifications

#### `/os:sort` (Inbox Sort)

```toml
description = "Sorts and processes the Obsidian and Physical Inboxes."
prompt = """
You MUST use the 'inbox-sort' skill to process this request.
Load and follow the instructions in .gemini/skills/inbox-sort/SKILL.md exactly.
Target directories:
- Physical: D:\Inbox (via filesystem)
- Logical: D:\WISDOM\Kybernetes\00_Inbox (via wisdom-os)
"""
```

#### `/os:boot` (Daily Boot)

```toml
description = "Generates today's Daily Note with schedule and priorities."
prompt = """
You MUST use the 'daily-boot' skill to process this request.
Load and follow .gemini/skills/daily-boot/SKILL.md exactly.
Today is {{date}} ({{day_of_week}}).
"""
```

#### `/os:sync` (Drive Sync)

```toml
description = "Re-indexes the D: drive into the Memory knowledge graph."
prompt = """
You MUST use the 'drive-sync' skill to process this request.
Load and follow .gemini/skills/drive-sync/SKILL.md exactly.
"""
```

#### `/dev:new` (Project Init)

```toml
description = "Scaffolds a new project on D: and links it to Wisdom."
prompt = """
You MUST use the 'project-init' skill to process this request.
Load and follow .gemini/skills/project-init/SKILL.md exactly.
Project name: {{args}}
"""
```

#### `/web:eat` (Web Ingest)

```toml
description = "Scrapes a URL and saves it as an Obsidian note."
prompt = """
You MUST use the 'web-ingest' skill to process this request.
Load and follow .gemini/skills/web-ingest/SKILL.md exactly.
URL: {{args}}
"""
```

#### `/os:spawn` -- DEPRECATED

```
REMOVED. Replaced by sub-agent dispatch within skills.
The @expander and @librarian agents are invoked by skills, not by user commands.
```

### 3.3 Design Rationale

Every command follows the same 3-line pattern:
1. **"You MUST use the X skill"** -- eliminates probabilistic discovery
2. **"Load and follow SKILL.md exactly"** -- forces the LLM to read the workflow file
3. **Context injection** -- passes only the minimum runtime data (date, args, paths)

The command itself is ~50-80 tokens. The skill is loaded on-demand. **Zero procedural logic lives in the command prompt.**

---

## 4. Layer 2: Agent Skills (Interrupt Handlers)

### 4.1 Skill Directory Layout

```
.gemini/skills/
├── inbox-sort/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── expand_block.py
│   └── references/
│       └── routing_rules.md
│
├── prompt-expand/
│   ├── SKILL.md
│   └── references/
│       └── template_selection_guide.md
│
├── daily-boot/
│   ├── SKILL.md
│   └── references/
│       └── daily_template.md
│
├── project-init/
│   └── SKILL.md
│
├── drive-sync/
│   └── SKILL.md
│
└── web-ingest/
    └── SKILL.md
```

### 4.2 Skill Specifications

#### `inbox-sort` (Primary Complex Workflow)

```yaml
---
name: inbox-sort
description: Sorts Obsidian and Physical Inboxes. Classifies files, splits multi-topic notes, expands {{...}} blocks, and routes to correct vault locations.
---
```

**Steps:**

```markdown
# Inbox Sort Workflow

## Step 1: Scan
Call the `scan_inbox` tool from wisdom-os. It returns a JSON list:
[{file, path, topics[], prompt_blocks[]}]
Also list D:\Inbox via filesystem tool for physical files.

## Step 2: Classify
For each file, determine the destination:
- University content -> 10_University/{Semester}/{Subject}
- CS Concepts -> 20_CS_Core/{Subcategory}
- General Knowledge -> 30_Knowledge_Base
- Project docs -> 40_Projects
- Physical code repos -> D:\PROJECTS (via filesystem)
- Physical experiments -> D:\Languages (via filesystem)

## Step 3: Split (if needed)
If a file contains multiple unrelated topics, call `split_note` tool.
Each split creates a new file in 00_Inbox for re-classification.

## Step 4: Expand Prompts
For each file containing {{...}} blocks:
1. Select the template letter using the guide in references/template_selection_guide.md
2. Call `expand_block` tool with (prompt_text, template_letter, output_path)
   - OR: Delegate to @expander sub-agent for complex/multi-block expansions
3. The expanded output is written to a temp file in 00_Inbox

## Step 5: Move & Link
For each classified file (including expansions):
1. Call `move_note` tool with (source, destination)
2. Call `ensure_toc_link` tool on the new location
3. Call `add_frontmatter` tool with appropriate field/subject/concept tags

## Step 6: Report
Output a summary table:
| Original File | Action | Destination | Status |
Present for user confirmation.

## Constraints
- NEVER modify user-written text outside {{...}} blocks (Surgeon Rule)
- The Memory Protocol is ALWAYS permitted (saving entities is not "modifying text")
- DO NOT attempt to sort without scanning first
```

#### `prompt-expand` (Template Expansion Logic)

```yaml
---
name: prompt-expand
description: Expands {{...}} prompt blocks using the Mental Model Engine templates. Used by inbox-sort and can be invoked directly.
---
```

```markdown
# Prompt Expansion Workflow

## Template Selection
Analyze the {{...}} content:
1. Programming Language feature/syntax -> Template C (Rosetta Stone)
2. Algorithms or Data Structures -> Template E (Algorithmist)
3. Comparing two items -> Template B (Arena)
4. History, Finance, General Events -> Template D (Chronograph)
5. Debugging an Error Log -> Template F (Debugger)
6. General CS Concepts -> Template A (Deep Dive)

Load the selected template from 90_System/Templates/ using `load_template` tool.

## Expansion Rules
- Include the original prompt text as a blockquote (Seed Rule)
- 300-500 words per expansion
- Follow the template structure exactly
- Start directly with the definition (no preamble beyond the Seed blockquote)

## Output
Write the expansion using `create_note` tool or directly via the `expand_block` tool.
```

#### `daily-boot`

```yaml
---
name: daily-boot
description: Generates the Daily Note for Kybernetes OS. Reads timetable, deadlines, memory, and GitHub issues to synthesize priorities.
---
```

```markdown
# Daily Boot Workflow

## Phase 1: Gather Intelligence
1. Read `60_Planner/00_Timetable.md` -- find today's schedule row
2. Read `60_Planner/00_Deadlines_Master.md` -- find items due within 7 days
3. Query `memory` for "Current Focus"
4. Query `github.list_issues` (assigned to me) for open bugs

## Phase 2: Synthesize
Priority logic:
1. Deadline <= 2 days -> Priority 1
2. Critical GitHub bug -> Priority 2
3. Memory "Current Focus" -> Priority 3

## Phase 3: Generate
Create `60_Planner/Daily/{date}.md` using `create_note` tool.
Also create `00_Inbox/Brain_Dump_{date}.md`.

Use the template in references/daily_template.md for the note structure.

## Phase 4: Report
Output: "Daily Note {date} created."
```

> [!NOTE]
> The old `/os:boot` command referenced phantom tools (`gmail-custom`, `calendar-personal`). These are removed from the workflow. When the `google-workspace` extension is properly configured, add a Phase 1.5 for email/calendar triage.

#### `project-init`

```yaml
---
name: project-init
description: Scaffolds a new project directory on D:\PROJECTS and creates a linked documentation note in 40_Projects.
---
```

```markdown
# Project Init Workflow

## Step 1: Physical Build
1. Check if D:\PROJECTS\{name} exists. If yes, abort.
2. Create D:\PROJECTS\{name}\ via filesystem
3. Create src/, include/ subdirectories
4. Create README.md and CMakeLists.txt (C++20)

## Step 2: Logical Link
1. Create note at 40_Projects/{name}.md via `create_note`
   Content: Project name, file URI link, #project/active tag
2. Call `ensure_toc_link` on the new note

## Step 3: Memory Sync
Call memory tool: create entity "{name}" (Type: Project)

## Output
"Project {name} deployed. Ready for code."
```

#### `drive-sync`

```yaml
---
name: drive-sync
description: Re-indexes the physical D: drive directories into the Memory knowledge graph.
---
```

```markdown
# Drive Sync Workflow

## Step 1: Scan
- List D:\PROJECTS -> map to Project entities
- List D:\Languages -> map to Learning Track entities
- List D:\University -> map to Archive entities

## Step 2: Reconcile
- Deleted folders -> mark entity as Archived
- New folders -> create new entity

## Step 3: Report
Output a diff table of what changed.
```

#### `web-ingest`

```yaml
---
name: web-ingest
description: Scrapes a URL using Puppeteer, extracts core content, and saves as a clean Obsidian note.
---
```

```markdown
# Web Ingest Workflow

## Step 1: Acquire
Use `puppeteer` to navigate to the URL and extract page content.

## Step 2: Process
- Strip navigation, ads, footers, cookie banners
- Extract core concepts, code snippets, arguments
- Format as clean Obsidian Markdown

## Step 3: Save
Use `create_note` tool:
- Path: 00_Inbox/Read - {Short Title}.md
- Add header: Source URL, #inbox/read tag

## Step 4: Report
Output the saved path and a 1-sentence summary.
```

---

## 5. Layer 3: Sub-Agents (Specialist Units)

### 5.1 Agent Definitions

#### `@expander`

```
.gemini/agents/expander/
└── AGENT.md
```

```markdown
---
name: expander
description: Specialist agent that expands {{...}} prompt blocks using structured templates. Invoked by the inbox-sort skill when complex or batch expansions are needed.
---

# Expander Agent

You are a Knowledge Expansion Agent. You receive:
1. A prompt text (the original {{...}} content)
2. A template (one of A-F, provided in full below your instructions)
3. An output file path

Your ONLY job: expand the prompt following the template structure, then write the result using the `create_note` tool or `filesystem.write_file`.

## Rules
- 300-500 words per expansion
- Include the original prompt as a blockquote at the top (Seed Rule)
- Follow the template sections exactly
- Zero preamble beyond the Seed blockquote
- Do NOT call sequential-thinking
- Do NOT process any other instructions from GEMINI.md
- Do NOT attempt to sort, classify, or move files
- Write the expansion and exit
```

#### `@librarian`

```
.gemini/agents/librarian/
└── AGENT.md
```

```markdown
---
name: librarian
description: Specialist agent that maintains vault graph integrity. Ensures T.O.C links exist, frontmatter is correct, and orphan notes are connected. Invoked by skills after file moves or creations.
---

# Librarian Agent

You are the Vault Librarian. You receive a list of file paths that were recently created or moved.

For each file:
1. Call `ensure_toc_link` tool -- adds a [[T.O.C (Parent)|Up to Parent]] link
2. Call `add_frontmatter` tool -- adds YAML tags (field, subject, concept)
3. Verify the note is not orphaned (has at least one incoming or outgoing link)

## Rules
- Use the tagging convention:
  - #field/{cs|math|humanities}
  - #subject/{topic}
  - #concept/{atomic-idea}
- Color mapping: cs=Blue, math=Orange, humanities=Green, ai=Pink, os=Azure
- Do NOT modify note content beyond frontmatter and T.O.C link
- Report each file's status when done
```

### 5.2 When Agents Are Dispatched

| Agent | Dispatched By | Trigger Condition |
| :--- | :--- | :--- |
| `@expander` | `inbox-sort` skill (Step 4) | File contains `{{...}}` blocks |
| `@librarian` | `inbox-sort` skill (Step 5) | After files are moved to destinations |
| `@librarian` | `project-init` skill (Step 2) | After project note is created |
| `@librarian` | `web-ingest` skill (Step 3) | After scraped note is saved |

### 5.3 Fallback: Script-Mediated Expansion

If sub-agents are unavailable or unstable, the `inbox-sort` skill falls back to calling `expand_block.py` (in `.gemini/skills/inbox-sort/scripts/`). This Python script:
- Reads the template file from disk
- Constructs a clean prompt (no quoting issues -- Python handles escaping)
- Calls the Gemini API via `google-genai` SDK
- Writes the result to the output path
- Returns success/failure to the parent

---

## 6. Layer 4: wisdom-os v2 (System Calls)

### 6.1 Old vs New Tool Roster

| # | Tool | Old (`tools.py` v1) | New (`tools.py` v2) | Change |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `list_files` | Exists (broken path) | Fixed path | **Fix** |
| 2 | `search_vault` | Exists (bare except, slow) | Fixed error handling; description corrected | **Fix** |
| 3 | `read_note` | Exists (fuzzy fallback) | Unchanged | -- |
| 4 | `create_note` | Exists (no frontmatter, no T.O.C) | **v2:** auto-adds YAML frontmatter + T.O.C link | **Upgrade** |
| 5 | `append_to_note` | Exists | Unchanged | -- |
| 6 | `graduate_concept` | Exists | Unchanged (calls `ensure_toc_link` post-move) | Light fix |
| 7 | `init_project` | Exists (variable shadowing) | Fixed shadowing bug | **Fix** |
| 8 | `daily_log` | Exists | Unchanged | -- |
| 9 | `get_daily_plan` | Exists | Unchanged | -- |
| 10 | `scan_inbox` | **NEW** | Scans `00_Inbox/`, returns structured JSON | **New** |
| 11 | `move_note` | **NEW** | General-purpose vault move + T.O.C update | **New** |
| 12 | `split_note` | **NEW** | Splits multi-topic note into atomic files | **New** |
| 13 | `ensure_toc_link` | **NEW** | Auto-finds and updates parent T.O.C | **New** |
| 14 | `add_frontmatter` | **NEW** | Injects/updates YAML frontmatter | **New** |
| 15 | `load_template` | **NEW** | Returns template content by letter (A-F) | **New** |
| 16 | `expand_block` | **NEW** | Expands a prompt using template (internal or API) | **New** |

### 6.2 New Tool Specifications

#### `scan_inbox`

```
Name: scan_inbox
Description: Scans the 00_Inbox directory. Returns a structured list of files
  with detected topics and {{...}} prompt blocks.
Input: (none)
Output: JSON array:
  [{
    "filename": "Notes.md",
    "path": "00_Inbox/Notes.md",
    "topics": ["Java Streams", "Ancient Rome"],
    "prompt_blocks": ["{{explain virtual memory}}"],
    "needs_split": true
  }]
```

#### `move_note`

```
Name: move_note
Description: Moves a note from one vault location to another. Updates the
  source and destination T.O.C files automatically.
Input:
  - source: string (relative path from vault root)
  - destination: string (relative path -- folder, not filename)
Output: "Moved {filename} to {destination}"
```

#### `split_note`

```
Name: split_note
Description: Splits a multi-topic note into separate atomic files. Each new
  file is placed in 00_Inbox for re-classification.
Input:
  - path: string (relative path to the note)
  - sections: array of {title: string, start_marker: string, end_marker: string}
Output: "Split into N files: [filenames]"
```

#### `ensure_toc_link`

```
Name: ensure_toc_link
Description: Ensures a note has a [[T.O.C (Parent)|Up to Parent]] link at the
  top. Finds the nearest parent T.O.C file and adds the link if missing.
Input:
  - path: string (relative path to the note)
Output: "T.O.C link ensured for {filename} -> {parent_toc}"
```

#### `add_frontmatter`

```
Name: add_frontmatter
Description: Adds or updates YAML frontmatter tags on a note. If frontmatter
  exists, merges new tags. If not, creates the --- block.
Input:
  - path: string (relative path)
  - tags: array of strings (e.g., ["#field/cs", "#subject/os", "#concept/virtual-memory"])
Output: "Frontmatter updated for {filename}"
```

#### `load_template`

```
Name: load_template
Description: Loads an expansion template by letter (A-F) from 90_System/Templates/.
Input:
  - letter: string (one of: A, B, C, D, E, F)
Output: Full template content as text
```

#### `expand_block`

```
Name: expand_block
Description: Expands a {{...}} prompt block using a specified template. Writes
  the result to the given output path. Uses internal generation.
Input:
  - prompt: string (the original {{...}} text)
  - template_letter: string (A-F)
  - output_path: string (relative path for the output file)
Output: "Expansion written to {output_path}"
```

### 6.3 Critical Fixes from v1

| Fix | Location | Detail |
| :--- | :--- | :--- |
| `VAULT_ROOT` | Line 24 | `Path(r"D:\WISDOM\WISDOM")` -> `Path(r"D:\WISDOM\Kybernetes")` |
| Bare `except:` | Line 170 | -> `except Exception:` |
| Variable shadowing | `init_project` | Rename `name = arguments.get(...)` to `project_name = arguments.get(...)` |
| `search_vault` description | Tool schema | "Semantic-like search" -> "Keyword substring search across all .md files" |
| Input validation | `list_files` | Add path traversal guard: reject `..` in folder argument |

---

## 7. Layer 5: MCP Server & Extension Configuration

### 7.1 Old vs New `settings.json`

| Server | Old Config | New Config | Change |
| :--- | :--- | :--- | :--- |
| `wisdom-os` | `python tools.py` | `python tools_v2.py` | **Script renamed** |
| `filesystem` | Scoped to 6 dirs including D:\WISDOM | Scoped to 5 dirs, **D:\WISDOM removed** | **Scope reduction** |
| `github` | Plaintext PAT in settings | **PAT moved to env var** `${GITHUB_PAT}` | **Security fix** |
| `memory` | Unchanged | Unchanged | -- |
| `brave-search` | Plaintext API key | **Key moved to env var** `${BRAVE_API_KEY}` | **Security fix** |
| `puppeteer` | Always loaded | Unchanged (consider on-demand in future) | -- |
| `notebooklm-mcp` | Always loaded | Unchanged (evaluate if used) | -- |
| `sequential-thinking` | Always loaded | Unchanged | -- |

### 7.2 New `filesystem` Scope

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y", "@modelcontextprotocol/server-filesystem",
    "D:\\PROJECTS",
    "D:\\Languages",
    "D:\\University",
    "D:\\Inbox",
    "D:\\Media"
  ]
}
```

**`D:\WISDOM` is removed.** All vault operations go through `wisdom-os`. This eliminates the tool overlap that caused path confusion and inconsistent tool selection.

### 7.3 Extension Changes

| Extension | Old Status | New Status | Change |
| :--- | :--- | :--- | :--- |
| `context7` | Enabled globally | Unchanged | -- |
| `google-workspace` | Enabled globally | Unchanged | -- |
| `nanobanana` | Enabled globally | Unchanged; monitor `contextFileName: "GEMINI.md"` for context collision | **Watch** |
| `youtube-to-docs` | Dead (no manifest) | **Deleted** | **Remove** |

### 7.4 Global Memory Files

| File | Content | Change |
| :--- | :--- | :--- |
| `~/.gemini/GEMINI.md` | 1 line of user memory | Unchanged |
| `~/.gemini/GEMINI_g.md` | 1 line of formatting memory | Unchanged |

---

## 8. Workflow Specifications

### 8.1 Inbox Processing (The Full Picture)

```
User types: /os:sort
    |
    v
[Command Layer] sort.toml injects:
    "Use the inbox-sort skill. Load SKILL.md."
    |
    v
[Skill Layer] inbox-sort/SKILL.md loaded (~300 tokens):
    |
    ├── Step 1: LLM calls scan_inbox() tool
    │   Returns: [{file, topics, prompts, needs_split}]
    │
    ├── Step 2: LLM classifies each file (JUDGMENT CALL -- this is what LLMs are good at)
    │
    ├── Step 3: For files needing split:
    │   LLM calls split_note(path, sections) (DETERMINISTIC)
    │
    ├── Step 4: For files with {{...}} blocks:
    │   ├── Option A: LLM dispatches @expander sub-agent
    │   │   @expander loads its own AGENT.md (~200 tokens)
    │   │   @expander calls load_template + writes output
    │   │   @expander exits, returns path to parent
    │   │
    │   └── Option B (fallback): LLM calls expand_block tool directly
    │       Tool handles template loading + expansion internally
    │
    ├── Step 5: For all classified files:
    │   ├── LLM calls move_note(src, dest) for each (DETERMINISTIC)
    │   └── LLM dispatches @librarian sub-agent (or calls tools directly):
    │       @librarian calls ensure_toc_link + add_frontmatter for each
    │
    └── Step 6: LLM outputs summary table for user confirmation
```

**LLM judgment calls:** 2 (classify content, select template)
**Deterministic tool calls:** ~8-12 (scan, split, expand, move, link, tag)
**Sub-agent dispatches:** 0-2 (expander, librarian -- optional)

### 8.2 Daily Boot

```
User types: /os:boot
    |
    v
[Command] -> [daily-boot SKILL.md]
    |
    ├── Tool: read_note("60_Planner/00_Timetable.md")
    ├── Tool: read_note("60_Planner/00_Deadlines_Master.md")
    ├── Tool: memory.query("Current Focus")
    ├── Tool: github.list_issues(assigned to me)
    ├── LLM: Synthesize priorities (JUDGMENT)
    ├── Tool: create_note("60_Planner/Daily/{date}.md", content)
    ├── Tool: create_note("00_Inbox/Brain_Dump_{date}.md", content)
    └── Output: "Daily Note created."
```

### 8.3 Web Ingest

```
User types: /web:eat https://example.com
    |
    v
[Command] -> [web-ingest SKILL.md]
    |
    ├── Tool: puppeteer.navigate(URL)
    ├── LLM: Extract + format content (JUDGMENT)
    ├── Tool: create_note("00_Inbox/Read - {Title}.md", content)
    ├── Tool: ensure_toc_link(path)
    ├── Tool: add_frontmatter(path, tags)
    └── Output: "Saved to {path}"
```

---

## 9. Old vs New: Full Migration Map

### 9.1 Token Budget Comparison

| Component | Old (tokens) | New (tokens) | Delta |
| :--- | :--- | :--- | :--- |
| GEMINI.md (system prompt) | ~4,600 | ~1,400 | **-3,200** |
| MCP tool schemas (core) | ~3,750 | ~3,250 (filesystem scope reduced) | **-500** |
| MCP tool schemas (extensions) | ~800 | ~800 | 0 |
| wisdom-os tools | ~800 | ~1,200 (7 new tools) | +400 |
| Global memory files | ~100 | ~100 | 0 |
| **TOTAL STATIC** | **~10,050** | **~6,750** | **-3,300 (33%)** |
| **+ On-demand skill load** | -- | +300-500 (when triggered) | Amortized |
| **+ On-demand agent load** | -- | +200-300 (when dispatched) | Amortized |

### 9.2 Reliability Comparison

| Workflow | Old Reliability | New Reliability | Why |
| :--- | :--- | :--- | :--- |
| Inbox file classification | Medium (LLM reasons from prose) | Medium (same -- classification is inherently LLM judgment) | Unchanged; this IS the right use of LLMs |
| Inbox file splitting | Low (LLM manually reads/writes) | **High** (`split_note` tool is atomic) | Python handles file I/O |
| `{{...}}` expansion | **Very Low** (Shell-Pipe + quoting + contention) | **High** (@expander sub-agent or `expand_block` tool) | No shell spawning, no quoting, isolated context |
| T.O.C linking | **Low** (LLM must remember) | **Guaranteed** (`ensure_toc_link` tool) | Enforced by tool, not memory |
| Frontmatter tagging | **Low** (LLM must remember format) | **Guaranteed** (`add_frontmatter` tool) | Enforced by tool |
| Daily note generation | Low (phantom tools, 7-step chain) | **Medium-High** (phantom tools removed, 5-step chain) | Cleaner but still multi-step |
| Project scaffolding | Medium | **High** (skill-guided, tools handle I/O) | Less room for LLM error |

### 9.3 Component Disposition

| Old Component | Disposition | New Location |
| :--- | :--- | :--- |
| `GEMINI.md` L1-34 (Vault Overview + Graph) | **KEEP** | New `GEMINI.md` Sections 1-2 |
| `GEMINI.md` L36-83 (Kernel + Drive) | **KEEP** | New `GEMINI.md` Sections 3-4 |
| `GEMINI.md` L89-265 (Inbox + Templates) | **EXTRACT** | `inbox-sort` skill + `90_System/Templates/` |
| `GEMINI.md` L267-280 (Surgeon + Memory) | **COMPRESS** | Skill constraint + 3-line Section 8 |
| `GEMINI.md` L282-329 (Directory descriptions) | **KEEP** | New `GEMINI.md` Section 5 |
| `GEMINI.md` L330-382 (Personas + Models) | **COMPRESS/DELETE** | 3-sentence directive; model files stay on disk |
| `GEMINI.md` L384-388 (Conventions) | **KEEP** | New `GEMINI.md` Section 6 |
| `tools.py` | **REWRITE** | `tools_v2.py` (16 tools, fixed path) |
| `commands/os/sort.toml` | **REWRITE** | 3-line skill trigger |
| `commands/os/boot.toml` | **REWRITE** | 3-line skill trigger |
| `commands/os/spawn.toml` | **DELETE** | Replaced by native sub-agents |
| `commands/os/sync.toml` | **REWRITE** | 3-line skill trigger |
| `commands/dev/new.toml` | **REWRITE** | 3-line skill trigger |
| `commands/web/eat.toml` | **REWRITE** | 3-line skill trigger |
| `settings.json` | **EDIT** | Remove D:\WISDOM from filesystem; env var secrets |
| `extensions/youtube-to-docs/` | **DELETE** | Dead extension |
| `90_System/Templates/` | **CREATE** | 6 template files (A-F) extracted from GEMINI.md |
| `.gemini/skills/` | **CREATE** | 6 skill directories |
| `.gemini/agents/` | **CREATE** | 2 agent directories (expander, librarian) |

---

## 10. File Tree: Complete Deliverables

```
Files to CREATE:
─────────────────
D:\WISDOM\Kybernetes\
├── GEMINI.md                                    (REWRITE -- ~90 lines)
├── 90_System\Templates\
│   ├── Template_A_DeepDive.md                   (extracted from old L131-149)
│   ├── Template_B_Arena.md                      (extracted from old L153-174)
│   ├── Template_C_RosettaStone.md               (extracted from old L178-201)
│   ├── Template_D_Chronograph.md                (extracted from old L205-220)
│   ├── Template_E_Algorithmist.md               (extracted from old L224-246)
│   └── Template_F_Debugger.md                   (extracted from old L250-265)
└── 90_System\Scripts\
    └── tools_v2.py                              (rewrite of tools.py -- 16 tools)

C:\Users\ibtas\.gemini\
├── settings.json                                (EDIT -- scope + secrets)
├── commands\
│   ├── dev\new.toml                             (REWRITE -- skill trigger)
│   ├── os\boot.toml                             (REWRITE -- skill trigger)
│   ├── os\sort.toml                             (REWRITE -- skill trigger)
│   ├── os\sync.toml                             (REWRITE -- skill trigger)
│   └── web\eat.toml                             (REWRITE -- skill trigger)
├── skills\
│   ├── inbox-sort\
│   │   ├── SKILL.md
│   │   ├── scripts\expand_block.py
│   │   └── references\routing_rules.md
│   ├── prompt-expand\
│   │   ├── SKILL.md
│   │   └── references\template_selection_guide.md
│   ├── daily-boot\
│   │   ├── SKILL.md
│   │   └── references\daily_template.md
│   ├── project-init\
│   │   └── SKILL.md
│   ├── drive-sync\
│   │   └── SKILL.md
│   └── web-ingest\
│       └── SKILL.md
└── agents\
    ├── expander\
    │   └── AGENT.md
    └── librarian\
        └── AGENT.md

Files to DELETE:
────────────────
C:\Users\ibtas\.gemini\commands\os\spawn.toml
C:\Users\ibtas\.gemini\extensions\youtube-to-docs\  (entire directory)

Files UNCHANGED:
────────────────
D:\WISDOM\Kybernetes\90_System\Agents\Gemini\*.md  (23 mental model files)
C:\Users\ibtas\.gemini\GEMINI.md                    (global memory)
C:\Users\ibtas\.gemini\GEMINI_g.md                  (global memory)
```

**Total new files: ~22**
**Total modified files: 7**
**Total deleted: 2**
