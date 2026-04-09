# Kybernetes — Full System Analysis (v6)
**Date:** 2026-04-05
**Scope:** Complete traversal of `D:\WISDOM\Kybernetes` vault root, all sub-directories, `GEMINI.md`, and `C:\Users\ibtas\.gemini` (agents, skills, commands, extensions, settings).

---

## What This System Is — In One Sentence

**Kybernetes is a custom, LLM-native operating system built on Gemini CLI, using an Obsidian vault as its filesystem, a hand-written Python MCP server as its kernel, and a fleet of specialized sub-agents as its processes.**

It is not a note-taking app with AI features bolted on. It is an OS. The vault is the hard drive. The agents are the programs. The skills are the shell scripts. The commands are the hotkeys. The principle cards are the instruction set manuals.

---

## Layer 1: The File System — The Obsidian Vault

**Root:** `D:\WISDOM\Kybernetes`

The vault is structured around a **Hybrid PARA** scheme — Projects, Areas, Resources, Archives — heavily modified to separate academic logistics from evergreen knowledge.

### Directory Map

| Folder | Role | Analogy |
| :--- | :--- | :--- |
| `00_Inbox` | Raw dump zone for new notes and `{{...}}` expansion targets | `/tmp` — volatile staging |
| `10_University` | Active academic notes, Sem 1–4, lectures, assignments | `/home/user/coursework` |
| `20_CS_Core` | Evergreen CS knowledge: Theory, Languages, Dev, Tools | `/usr/share/knowledge` — permanent library |
| `30_Knowledge_Base` | Flat-graph general knowledge (History, Fiqh, Philosophy, Science) | Wikipedia, but curated |
| `40_Projects` | Active/Backlog/Portfolio projects with vault ↔ `D:\PROJECTS` bridge | `/home/user/projects` |
| `50_Resources` | Bookshelf, articles, online courses | `/home/user/library` |
| `60_Planner` | Daily/Weekly/Monthly temporal planning | `/var/log` meets a calendar |
| `90_System` | OS internals: Cards, Agents, Scripts, Issues, UI, Templates | `/etc` and `/lib` |

### The Graph Backbone — The T.O.C System

Every folder has a `T.O.C (Folder Name).md` file. Two formats exist:
- **Structured Tables** (for course Notes): `| ID | Category | Content |` rows, ordered by `X.Y.Z` ID scheme.
- **Bullet Lists** (for top-level aggregators): `- [[Note]]` entries.

Every note obeys a strict **bidirectional link rule**: uplink to parent T.O.C on line 1, and the parent T.O.C has a downlink entry to the note. Orphans are invisible (`showOrphans: OFF`). Root entry: `T.O.C (Root).md`.

University notes use hierarchical IDs: `{Sessional}.{Category}.{Sequence} - {Title}.md` (e.g., `2.3.4 - B-Tree Insertion.md`). The sessional number is read from `Admin/Deadlines.md`.

### Graph Aesthetics — "Night Sky"

The graph is colour-coded by a mandatory tagging matrix in YAML frontmatter:

| Tag | Colour |
| :--- | :--- |
| `field/cs` | Neon Blue |
| `field/math` | Vivid Orange |
| `field/humanities` | Emerald Green |
| `subject/ai` | Cyber Pink |
| `subject/os` | Azure |
| `type/map` | Pure White |

Every note carries exactly 3 tags: `field/`, `subject/`, and `concept/` axes.

---

## Layer 2: The Kernel — `tools.py` (wisdom_os MCP Server)

**Path:** `D:\WISDOM\Kybernetes\90_System\Scripts\tools.py` — **1,518 lines of Python**.

A custom **Model Context Protocol (MCP) server** that exposes vault operations as callable tools. Runs as a subprocess managed by Gemini CLI. Server name: `wisdom_os`.

### Tool Inventory

| Category | Tools |
| :--- | :--- |
| **Exploration** | `list_files`, `search_vault`, `read_note`, `semantic_search` |
| **Writing** | `create_note`, `rename_note`, `delete_note`, `move_note`, `append_to_note` |
| **University** | `graduate_concept` |
| **Projects** | `init_project` |
| **Planner** | `daily_log`, `get_daily_plan` |
| **Graph** | `ensure_toc_link`, `add_frontmatter`, `split_note`, `scan_inbox` |
| **Orchestration** | `prepare_dispatch`, `inject_subblocks`, `stitch_files`, `append_summary` |
| **Scoped Agent** | `write_expansion`, `word_count`, `organize_file` |
| **Fiqh Pipeline** | `prepare_fiqh_dispatch`, `fiqh_link_and_finalize` |

**Security Model:** `write_expansion` only writes to files in `00_Inbox` with names starting `_expand_` or `_fiqh_`. All structural operations (T.O.C, frontmatter, moving) are handled by Python tools, never by LLM inference.

`semantic_search` hijacks the Smart Connections plugin's `.smart-env/multi/*.ajson` vector DB using `SentenceTransformer('TaylorAI/bge-micro-v2')` for cosine similarity — no separate vector DB needed.

---

## Layer 3: External MCP Servers

Configured in `C:\Users\ibtas\.gemini\settings.json`. Eight servers:

| Server | Transport | Purpose |
| :--- | :--- | :--- |
| `wisdom_os` | Python subprocess | Vault kernel |
| `filesystem` | npx `@modelcontextprotocol/server-filesystem` | Physical drive: `D:\PROJECTS`, `D:\Languages`, `D:\Inbox`, `D:\Media`, `D:\WISDOM` |
| `github` | npx `@modelcontextprotocol/server-github` | GitHub repo management |
| `memory` | npx `@modelcontextprotocol/server-memory` | Persistent cross-session entity/relation memory |
| `puppeteer` | npx `@modelcontextprotocol/server-puppeteer` | Browser automation |
| `brave-search` | npx `@modelcontextprotocol/server-brave-search` | Web search |
| `sequential-thinking` | npx `@modelcontextprotocol/server-sequential-thinking` | Structured multi-step reasoning |
| `notebooklm-mcp` | Local binary | NotebookLM integration |

---

## Layer 4: The Agent Fleet — `C:\Users\ibtas\.gemini\agents\`

17 named agents. Each runs in an **isolated context window**.

### Orchestrator Layer

| Agent | Role |
| :--- | :--- |
| `@classifier` | Routes `{{...}}` prompts → `{domain, card_type, card_value}` JSON. No content generation. |
| `@librarian` | Routes finished notes → `{destination_dir, toc_parent, category, suggested_name, tags}` JSON. Never touches files. |

### Domain Expansion Agents (9)

| Agent | Domain | Voice |
| :--- | :--- | :--- |
| `@turing` | Computer Science | Zero preamble, mechanical analogies, failure modes mandatory |
| `@euler` | Mathematics | Formal-first, worked examples mandatory |
| `@newton` | Physics | Phenomenon-first, equations support narrative |
| `@alhaytham` | Sciences | Empirical, hypothesis-testing |
| `@iqbal` | Philosophy | Musing, prose-heavy, no bullets |
| `@nabokov` | Literature | Lofty, close reading, textual evidence |
| `@ibnkhaldun` | History | Storyteller, lesser-known details |
| `@davinci` | Arts | Technique-to-meaning, prose-heavy |
| `@machiavelli` | Social Sciences | Incentive-tracing, second-order effects |

Tools available to domain agents: `write_expansion`, `read_note`, `word_count` only.

### Fiqh Pipeline Agents (5)

| Agent | Role |
| :--- | :--- |
| `@hanafi` | Hanafi madhab position with mandatory usul al-fiqh derivation chain |
| `@maliki` | Maliki position |
| `@shafii` | Shafi'i position |
| `@hanbali` | Hanbali position |
| `@fiqh_synthesizer` | Neutral synthesis — reads all four madhab outputs, produces divergence-typed analysis |

### Specialist Agents

| Agent | Role |
| :--- | :--- |
| `@polymath` | Reads semantic search vector chunks, generates cross-domain Maps of Content (MOCs) |

---

## Layer 5: The Principle Card System — `90_System/Cards/`

**50 card files.** Cards are the instruction sets for domain agents. Each specifies: Goal, Quality Signals, Anti-Patterns, Voice.

### Card Taxonomy

| Type | Examples | Purpose |
| :--- | :--- | :--- |
| `@turing` cards | `turing_concept`, `turing_algorithm`, `turing_design`, `turing_debugger`, `turing_case`, `turing_history`, `turing_comparison`, `turing_language` | 8 output modes for CS |
| `@euler` cards | `euler_concept`, `euler_proof` | Exposition vs. formal proof |
| Domain cards | `philosophical`, `narrative_history`, `biography`, `aesthetic`, `game_theory`, `comparison_*`, `craft`, etc. | One per intent per domain |
| Fiqh cards | `fiqh_ruling`, `fiqh_usul_deep`, `fiqh_historical`, `fiqh_contemporary`, `fiqh_synthesizer` | Islamic jurisprudence output formats |
| Planner cards | `planner_turing`, `planner_iqbal`, ...(9 total) | Pass 1 decomposition — JSON output only, no content |
| Synthesis card | `synthesis` | MOC format for `@polymath` |

---

## Layer 6: The Skills — `C:\Users\ibtas\.gemini\skills\`

8 multi-step workflow scripts:

| Skill | Trigger | Summary |
| :--- | :--- | :--- |
| `inbox-sort` | `/os:sort` | Full pipeline: scan → classify → plan → approval gate → expand (parallel) → stitch → organize |
| `daily-boot` | `/os:boot` | Gmail + Calendar + deadlines + timetable → structured daily note |
| `madhab-pipeline` | `/os:fiqh` | 4 parallel madhab agents → verify → synthesizer → atomic finalization |
| `polymath-synthesize` | `/os:synthesize` | Semantic search → `@polymath` → MOC to `30_Knowledge_Base/00_Atlas/` |
| `web-ingest` | `/web:eat` | Puppeteer scrape → strip noise → Obsidian markdown → `00_Inbox` |
| `project-init` | `/dev:new` | `D:\PROJECTS\{name}` on disk + vault note in `40_Projects` + Memory MCP entity |
| `drive-sync` | `/os:sync` | Physical drive `D:\` reconciliation with vault records |
| `prompt-expand` | (internal) | Core expansion wrapper used by `inbox-sort` |

---

## Layer 7: The Commands — `C:\Users\ibtas\.gemini\commands\`

7 TOML files, pure dispatch:

| Command | Skill Invoked |
| :--- | :--- |
| `/os:sort` | `inbox-sort` |
| `/os:boot` | `daily-boot` |
| `/os:fiqh {question}` | `madhab-pipeline` |
| `/os:sync` | `drive-sync` |
| `/os:synthesize` | `polymath-synthesize` |
| `/dev:new {name}` | `project-init` |
| `/web:eat {url}` | `web-ingest` |

---

## Layer 8: Extensions — `C:\Users\ibtas\.gemini\extensions\`

| Extension | Provides |
| :--- | :--- |
| `google-workspace` | Gmail, Calendar, Docs, Sheets, Slides, Chat, People APIs |
| `context7` | Live, up-to-date library documentation via `@upstash/context7-mcp` |
| `nanobanana` | Image generation: `/icon`, `/pattern`, `/diagram`, `/edit`, `/restore`, `/story` |
| `youtube-to-docs` | YouTube video → structured vault-ready documentation |

---

## Layer 9: Physical Drive — The "Body"

Bridge Protocol — vault ↔ drive pairs:

| Physical | Vault | Relationship |
| :--- | :--- | :--- |
| `D:\PROJECTS` | `40_Projects` | Code ↔ Documentation |
| `D:\Languages` | `20_CS_Core\Languages` | Playground ↔ Theory |
| `D:\University` | `10_University` | Raw PDFs ↔ Notes (ROM — never modify) |
| `D:\Inbox` | `00_Inbox` | Physical dump ↔ Logical inbox |
| `D:\Identity` / `D:\Backup` / `D:\OSs` | — | RESTRICTED — no modifications |

---

## Layer 10: Auxiliary Sub-Systems

### VaultExplorer
A Vite/TypeScript web app — cyberpunk force-graph vault visualizer with command palette. Deployed statically on Vercel. Source at `D:\PROJECTS\VaultExplorer`, documentation at `90_System/VaultExplorer/`.

### Issues System (`90_System/Issues/`)
27 engineering documents — the system's living spec log. Architecture decisions, bug post-mortems, pipeline redesigns. Sub-folders: `polymath/` (RAG R&D), `v4/` (Knowledge Base restructure), `v6/` (this document).

### Memory MCP
The main orchestrator silently calls `create_entities` / `create_relations` whenever the user defines a project, states a preference, mentions a struggle, or provides personal context. Builds a long-term user model across sessions.

---

## What Makes This System Unusual

1. **The MCP server is custom-built** — it understands the vault's internal grammar: T.O.C structures, the `{{@deep}}` / `{{@blueprint:N}}` / `{{@expand}}` directive schema, expansion block scoping, fiqh pipeline mechanics.

2. **Agents are scoped, not trusted** — domain agents cannot create files, construct paths, or update T.O.C. All structural operations delegate to deterministic Python. LLM creativity is constrained to content generation only.

3. **Two-Pass is human-in-the-loop** — Pass 1 produces a decomposition plan reviewed in Obsidian before any content is generated in Pass 2. Editorial control over structure precedes commitment to generation.

4. **The Fiqh pipeline runs 4 LLM agents in parallel** with citation integrity rules (`(VERIFIED)` / `(UNCERTAIN)`), mandatory usul al-fiqh derivation chains, and a neutral fifth synthesizer — a multi-agent peer review system for Islamic jurisprudence.

5. **`@polymath` is a True PKM vision** — it ingests semantic search vectors from across the entire vault and generates emergent Maps of Content linking isomorphic ideas across CS, Philosophy, History, and Science.

6. **The principle card system makes agents reproducible** — the same `{{@expand Left Outer Join}}` always routes to `@turing` with `turing_concept`. Swapping cards produces measurably different outputs. Cards are the prompt engineering layer, made explicit and versionable.

7. **Everything is bidirectionally linked** — the vault is a connected graph. T.O.C files are active nodes that must be updated whenever any note moves. The Python kernel automates non-university destinations; university T.O.C updates require the orchestrator to surgically insert rows to preserve table aesthetics.
