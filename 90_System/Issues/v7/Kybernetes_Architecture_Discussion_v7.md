# Kybernetes — Architecture Discussion Log v7
**Date:** 2026-07-03
**Context:** Follow-up analysis consolidating the original problems, design discussion, and all decisions reached. This document supersedes the earlier `Kybernetes_Architecture_Discussion_v7.md` draft and records the full resolved design: heading-based AST as canonical structure, three-tier lazy-loaded context injection, single approval gate, Claude Agent SDK, and standalone app decoupled from inbox-sort.

---

## 1. Correction: The Redundancy Problem is Narrative, Not Definitional

### What v7 said
v7 framed redundancy as "the same *term* re-explained" and proposed a "ledger of terms/concepts" — essentially a glossary that tells downstream agents "Bid'ah has already been defined."

### What the actual problem is
Examined against real output (`Islamic_Sectarianism_in_the_Subcontinent.md`), the redundancy is not definitional. It is **narrative**. The same *stories*, *causal chains*, and *contextual setups* get retold from scratch in every section because each agent enters the topic cold:

| Narrative thread | Told in | Retold in |
|---|---|---|
| 1857 collapse / loss of Mughal patronage | Post-1857 Vacuum | Birth of Deoband, Barelvi Reaction, Bid'ah, Class Mapping |
| "Deobandis saw shrine practices as Shirk" | Tawassul | Bid'ah, Prophetology, Class Mapping |
| Ahmed Raza Khan's biography and counter-attack | Barelvi Reaction | Prophetology, Tawassul, Bid'ah |

A glossary ledger doesn't fix this. You can't glossary-entry a narrative arc. The fix requires that downstream agents know **which stories have already been told** — not just which words have been defined.

### Implication for the dependency graph
The payload carried along dependency edges must include **narrative summaries** (stories told, claims made, causal chains established), not just term definitions. This is what the heading-based AST + directive-enforced summaries provide (see below).

---

## 2. Decided: The Heading-Based AST is the Canonical Structure

### The insight
Every markdown file already contains a deterministic tree: the heading hierarchy. `#` is root, `##` is depth 1, `###` is depth 2, and so on. Parsing this into an AST is a **pure function** — same input, same tree, no model call, no temperature, no floating-point nondeterminism.

### What this means architecturally

**The document's heading structure IS the dependency graph's backbone.** The two structures v7 separated (the *tree* for decomposition and the *graph* for information flow) now share one representation:

- **The tree** = the heading hierarchy (H1 → H2 → H3 nesting)
- **The graph** = `depends_on` edges between AST node addresses

### AST node addressing
Each node in the heading AST has a deterministic address — a path from root:

```
"The Subcontinent > The Post-1857 Vacuum > From Swords to Syllabi"
```

Dependency edges reference these addresses directly. Retrieval is a tree lookup, like a filesystem path. No embeddings, no similarity thresholds, no tag vocabulary.

### Example AST (from `Islamic_Sectarianism_in_the_Subcontinent.md`)

```
H1: The Subcontinent                              ← root
├── H2: The Post-1857 Vacuum                      ← seed node
│   ├── H2: The Silence of the Red Fort           ← leaf
│   ├── H2: From Swords to Syllabi                ← leaf
│   └── H2: The Policing of the Soul              ← leaf
├── H2: The Birth of Deoband (1867)               ← seed node
│   ├── H2: The Pomegranate Tree and the Ruins    ← leaf
│   ├── H2: The Ledger as a Weapon                ← leaf
│   └── H2: The War for the Soul of the Village   ← leaf
├── H2: The Barelvi Reaction                      ← seed node
│   ├── H2: The Breach in the Wall                ← leaf
│   ├── H2: The Pen as a Shield                   ← leaf
│   └── H2: The Soul of the Great Majority        ← leaf
├── H2: Prophetology: Nur vs. Bashar              ← seed node
│   └── ...
├── H2: The Mechanics of Tawassul                 ← seed node
│   └── ...
├── H2: Defining Bid'ah                           ← seed node
│   └── ...
├── H2: Class and Socio-Economic Mapping           ← seed node
│   └── ...
├── H2: The Colonial 'Sorting' Effect             ← seed node
│   └── ...
└── H2: The Print Revolution and the Street War   ← seed node
    └── ...
```

With dependency edges:
```
"Barelvi Reaction"     depends_on → ["Post-1857 Vacuum", "Birth of Deoband"]
"Prophetology"         depends_on → ["Barelvi Reaction", "Birth of Deoband"]
"Tawassul"             depends_on → ["Prophetology"]
"Bid'ah"               depends_on → ["Tawassul", "Barelvi Reaction", "Birth of Deoband"]
"Class Mapping"        depends_on → ["Birth of Deoband", "Barelvi Reaction"]
"Colonial Sorting"     depends_on → []  (independent thread)
"Print Revolution"     depends_on → ["Bid'ah", "Colonial Sorting"]
```

The topological scheduler computes generation waves from these edges. Within each wave, nodes generate in parallel. Across waves, ordering is enforced.

---

## 3. Decided: Three-Tier Context Injection (Lazy Loading)

### The problem with structured summary schemas
The earlier design proposed a YAML schema (`narratives_told`, `terms_defined`, `claims_made`) attached to each node. This was rejected because:
- **Who writes it?** The same model that generated the content — so you're asking a model to self-report accurately. That's model judgment, not structure.
- **Who validates accuracy?** You can validate the YAML *parses*, but not that its contents faithfully represent what was written. Only a model can check that.
- **How does Agent N use it?** It reads natural-language strings and interprets them with model judgment to decide what not to retell. That's semantic comparison dressed in YAML clothing.

The full-text-injection alternative (pass the raw upstream text) solves accuracy but creates context bloat at scale.

### The solution: three tiers, lazy-loaded

Agent N's pre-generation context is assembled from its `depends_on` set using a **three-tier lazy-loading** strategy:

| Tier | What | Size | Source | Loaded |
|---|---|---|---|---|
| **1. AST headings** | The heading tree of the upstream node | ~10-20 lines | Deterministic parse of completed markdown | **Always** |
| **2. Summary paragraph** | A plain-prose summary, ≤100 words | ≤100 words | Directive-enforced: agent writes it as the final `<!-- summary: ... -->` block | **Always** |
| **3. Full text** | The complete generated content | ~1000+ words | The actual output stored at the AST node | **Only on agent request** |

**Tier 1** does most of the work. The heading names themselves signal what was covered — "The Silence of the Red Fort," "From Swords to Syllabi," "The Policing of the Soul" already tell the downstream agent *which topics were addressed* without any model interpretation.

**Tier 2** adds the argumentative thrust. A single paragraph, ≤100 words, stating the key moves the section made. At this length, it's almost impossible for the writing agent to get wrong — there's no room for omission or hallucination in 100 words about what you just wrote.

**Tier 3** is the escape hatch. If the downstream agent reads Tier 1 + 2 and still can't determine whether a prerequisite was covered, it can request the full text of a specific upstream node. This is the exception, not the default.

### Summary format (directive-enforced)
Each agent's generation prompt includes a **contract**: end your section with a `<!-- summary: ... -->` HTML comment containing a single plain-prose paragraph of ≤100 words.

```html
<!-- summary: The 1857 Rebellion destroyed the Mughal patronage system that had sustained the ulema for centuries. Without royal land grants, scholars pivoted from political influence to institutional self-preservation. Darul Uloom Deoband (1866) pioneered the public-funded madrasa model, refusing state money and relying on bazaar donations. The founders adopted British-style bureaucratic administration — fixed syllabi, exams, printed certificates — to create a portable, standardized scholarly identity. Their reform program targeted local "accretions" (shrine visits, shared Hindu-Muslim festivals) as causes of divine disfavor, narrowing Islamic identity to a text-heavy, scripturalist core that could survive without a king. -->
```

The system validates: (1) the `<!-- summary: ... -->` block exists, (2) it contains prose (not empty), (3) it is ≤100 words. If validation fails, the node is rejected and re-queued. No model call needed for validation.

### How downstream agents receive context
When Agent N is about to generate, the orchestrator assembles its context:

```
## Prerequisites covered by upstream nodes
(Review these. If you need more detail on any node, request its full text before writing.)

### "The Subcontinent > Post-1857 Vacuum"
**Sections written:**
- The Silence of the Red Fort
- From Swords to Syllabi
- The Policing of the Soul

**Summary:** The 1857 Rebellion destroyed the Mughal patronage system
that had sustained the ulema for centuries. Without royal land grants,
scholars pivoted from political influence to institutional
self-preservation...

### "The Subcontinent > Birth of Deoband"
**Sections written:**
- The Pomegranate Tree and the Ruins
- The Ledger as a Weapon
- The War for the Soul of the Village

**Summary:** Darul Uloom Deoband pioneered the public-funded madrasa
model, refusing state money and relying on bazaar donations. The
founders adopted British-style bureaucratic administration...

Do not retell these narratives. Reference them briefly to anchor
your argument, then advance into your own territory.
```

Agent N reads this (~200-300 words total for 2-3 upstream nodes), confirms it has enough context, and writes. If a heading like "The Ledger as a Weapon" is opaque, Agent N can request that specific node's full text before proceeding.

### The orchestration loop

```
1. Planner produces markdown outline (heading AST) + depends_on edges
2. ┌─────────────────────────────────────────────────┐
   │  APPROVAL GATE                                  │
   │  Human reviews: tree shape, depth, dependency   │
   │  edges, node assignments. Approves / edits.     │
   │  Everything after this gate runs autonomously.  │
   └─────────────────────────────────────────────────┘
3. Topological sort → generation waves
4. For each node in current wave:
   a. Orchestrator assembles: depends_on nodes' ASTs + summary paragraphs
   b. Agent reviews Tier 1 + 2 context
      - Satisfied → proceeds to write
      - Confused  → requests Tier 3 (full text) for specific node(s)
   c. Agent writes content + <!-- summary --> block
   d. Orchestrator validates summary (exists, prose, ≤100 words)
      - Pass → parse headings, update AST, attach summary, mark complete
      - Fail → reject, re-queue node
5. Advance to next wave
```

---

## 4. Resolution of v7 Open Items

### 5.1 — Ledger retrieval mechanism: **RESOLVED**
The heading-based AST IS the retrieval mechanism. Dependencies point to AST node addresses. Context is delivered via three-tier lazy loading: AST headings (always) + ≤100-word summary paragraph (always) + full text (on-demand). No embeddings, no tags, no fuzzy search. Deterministic by construction.

### 5.2 — Approval gate: **RESOLVED (simplified)**
The v7 design proposed "risk-adaptive gating" with model-scored confidence, precedent-matching against past trees, etc. This was overengineered. The gate is a single checkpoint between decomposition and generation:
- **Planner produces** the heading AST + `depends_on` edges.
- **Human reviews** the tree shape, depth, dependency edges, and node assignments.
- **Human approves or edits.**
- **Everything after the gate runs autonomously** — no per-node approval, no confidence scoring, no adaptive thresholds.

Rationale: the decomposition is where all the structural risk lives. If the tree is wrong, no amount of good generation saves it. If the tree is right, the three-tier context injection handles redundancy mechanically. One gate at the right place beats adaptive gates everywhere.

### 5.3 — Autonomous vocabulary extension: **Dissolved**
This was contingent on the tag-vocabulary approach (rejected in v7). With the AST + plain-prose summaries, there is no controlled vocabulary to extend. The summary is a ≤100-word paragraph, not a structured taxonomy. The problem no longer exists.

### 5.4 — Entry shape for large jobs: **RESOLVED (dissolved)**
This question was framed around `{{@deep ...}}` vs `@blueprint:N` syntax — both are features of the existing `inbox-sort` pipeline. The new pipeline is a **standalone app, fully decoupled from inbox-sort**. The existing `@deep`, `@blueprint`, and `inbox-sort` skill remain untouched.

The app's interface is simple: it receives a raw prompt (any prompt), and the root planner decomposes it into the heading AST. No special syntax, no entry-shape decision. The planner's job is always the same: take a prompt, produce a tree. The approval gate lets the human reshape the tree before generation begins, which handles any case where the planner's cold decomposition isn't right.

### 5.5 — SDK/runtime choice: **RESOLVED — Claude Agent SDK**
The Claude Agent SDK is selected. It provides:
- **Subagent context isolation** as a first-class primitive (each agent gets an explicitly assembled context, not a clone of the parent)
- **Tool permissioning** (agents can be restricted to specific tools per role)
- **Hooks** for lifecycle events (pre/post generation, validation, retry)
- **Embeddable in a custom app** rather than running as a CLI
- **Model-agnostic per node**: the SDK owns the agent-loop/tool-calling mechanics; individual node calls can route to whichever model fits the role (cheap/fast for structural work, best-tier for content generation)

---

## 5. Determinism Audit

The heading-based AST + directive-enforced summaries produce a fully deterministic structural layer:

| Operation | Deterministic? | Mechanism |
|---|---|---|
| Parse headings → AST | Yes | Pure string/regex parse |
| Compute dependency edges | Yes | Explicit `depends_on` declarations |
| Resolve AST node address | Yes | Tree path lookup |
| Extract summary at node | Yes | Parse `<!-- summary -->` block (regex) |
| Validate summary | Yes | Existence check + word count ≤100 |
| Assemble Tier 1+2 context | Yes | Concatenate headings + summary paragraphs |
| Tier 3 full-text retrieval | Yes | Direct read of completed node content |
| Compute generation waves | Yes | Topological sort of dependency graph |
| Detect cross-branch overlap at planning time | Yes | Compare planned sub-headings across branches |
| Cache/memoize by node | Yes | Content-hash of (AST path + dependency context + card version) |

The **only** nondeterministic operations are the model calls themselves (the planner's decomposition judgment and the agents' content generation). Everything structural — parsing, addressing, retrieval, scheduling, validation, caching — is deterministic.

This is a stronger guarantee than v7's "content-addressed memoization" strategy, which tried to paper over model nondeterminism with caching. The AST approach doesn't need to — the structural layer never touches a model.

---

## 6. What v7 Decided That Still Holds

All of the following from v7 remain unchanged and are compatible with the AST design:

- Custom app, not CLI-dependent (Section 3, "Orchestration / runtime")
- Model-agnostic per node
- Dependency-wave (topological) scheduler — now operating on AST node addresses
- Model tiering by role (Section 3, "Scale")
- Fractal QA/editing mirroring the generation tree — now the AST
- Node-level resumable regeneration with stable IDs — AST addresses are stable IDs
- Named tradeoff: bigger trees make global coherence structurally harder

---

## 7. What v7 Decided That Is Superseded

| v7 item | Superseded by |
|---|---|
| "Ledger of terms/concepts" for redundancy | Three-tier lazy-loaded context: AST headings + ≤100-word summary + full text on-demand |
| "Canon ledger" for cross-branch contradiction | Cross-branch overlap detection via AST sub-heading comparison at planning time; downstream agents can request Tier 3 (full text) to verify specific claims if needed |
| Content-addressed memoization as the determinism strategy | AST provides determinism at the structural layer by construction; memoization can still be used for generation-layer caching but is no longer the *primary* determinism mechanism |
| Structured YAML summary schema (`narratives_told`, `terms_defined`, `claims_made`) | Plain-prose ≤100-word summary paragraph — no structured fields, no schema to validate semantically |

---

## 8. Design Complete — System Summary

All open items from v7 are resolved or dissolved. The design is ready for implementation.

### What is being built
A **standalone app** (decoupled from inbox-sort / Kybernetes CLI) built on the **Claude Agent SDK**. It receives a raw prompt, produces a structured long-form document with no narrative redundancy.

### The pipeline

```
Prompt (raw text)
       │
       ▼
┌─────────────────┐
│  ROOT PLANNER   │  Decomposes prompt into heading AST + depends_on edges
└────────┬────────┘
         │
    ┌────▼────────────────────────────────────────────┐
    │  APPROVAL GATE                                  │
    │  Human reviews tree shape, depth, edges.        │
    │  Approves or edits. Everything after is auto.   │
    └────┬────────────────────────────────────────────┘
         │
    ┌────▼────────────┐
    │  TOPO SORT      │  Computes generation waves from depends_on
    └────┬────────────┘
         │
    ┌────▼────────────────────────────────────────────┐
    │  WAVE N (parallel)                              │
    │                                                 │
    │  For each node:                                 │
    │  1. Receive Tier 1 (AST headings of deps)       │
    │     + Tier 2 (≤100w summary of deps)            │
    │  2. Satisfied? Write. Confused? Pull Tier 3.    │
    │  3. Write content + <!-- summary --> block       │
    │  4. Orchestrator validates, parses AST, updates │
    │     graph, marks node complete                  │
    └────┬────────────────────────────────────────────┘
         │
         ▼
    (repeat for each wave)
         │
         ▼
┌─────────────────┐
│  ASSEMBLED DOC  │  All nodes stitched in AST order
└─────────────────┘
```

### Core mechanisms

| Mechanism | What it does | Deterministic? |
|---|---|---|
| **Heading AST** | Canonical structure — headings parsed into a tree, nodes addressed by path | Yes |
| **depends_on edges** | Information flow — explicit edges between AST nodes, cut across the tree | Yes |
| **Three-tier context** | Tier 1: AST headings (always). Tier 2: ≤100w summary (always). Tier 3: full text (on request) | Yes |
| **Approval gate** | Single checkpoint between decomposition and generation | Human |
| **Topological scheduler** | Computes parallel generation waves from dependency edges | Yes |
| **Summary validation** | Exists + prose + ≤100 words, else reject and re-queue | Yes |

### What it replaces vs. what it leaves alone

| Stays untouched | Replaced by this app |
|---|---|
| `inbox-sort` skill | Nothing — it continues to work as-is |
| `@deep` / `@blueprint` syntax | Nothing — they stay in the inbox-sort pipeline |
| Domain agents (@turing, @euler, etc.) | Nothing — they can be invoked as node generators within this app too |
| Principle cards | Nothing — they remain the generation templates |

The new app is an independent pipeline that can coexist with the existing system. It doesn't modify, replace, or depend on any existing Kybernetes infrastructure.
