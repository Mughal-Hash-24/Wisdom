---
tags:
  - "#type/report"
  - "#field/cs"
  - "#subject/systems"
  - "#concept/prompt-engineering"
---
[[T.O.C (90_System)|Up to 90_System]]

# System Prompt Diagnostic Report: `GEMINI.md`

> **Date:** 2026-02-27
> **Subject:** `GEMINI.md` (388 lines, ~21 KB, ~5,500 tokens)
> **Verdict:** The prompt is architecturally sound in *intent* but critically bloated in *implementation*. It forces the LLM to hold ~5,500 tokens of mostly-inert reference material in its attention window at all times, diluting focus on actual task instructions. The Shell-Pipe Protocol is the single most dangerous hallucination vector and should be removed entirely.

---

## Table of Contents

1. [Context Bloat & Token Economy](#1-context-bloat--token-economy)
2. [Ambiguity & Hallucination Vectors](#2-ambiguity--hallucination-vectors-the-shell-protocol)
3. [Logic Conflicts & Impossible Constraints](#3-logic-conflicts--impossible-constraints)
4. [Architectural Strengths & Weaknesses](#4-architectural-strengths--weaknesses)
5. [Refactoring Strategy & Remediation](#5-refactoring-strategy--remediation)

---

## 1. Context Bloat & Token Economy

### 1.1 Token Budget Breakdown (Estimated)

| Section | Lines | Est. Tokens | % of Total | Active Use Frequency |
| :--- | :--- | :--- | :--- | :--- |
| Project Overview & Graph Architecture | 1-34 | ~450 | 8% | Every note creation |
| System Kernel & Drive Architecture | 36-84 | ~700 | 13% | File operations only |
| Inbox Processing Protocol (Steps 0-3) | 89-118 | ~550 | 10% | Inbox processing only |
| Template Selection Logic | 120-127 | ~100 | 2% | Inbox processing only |
| **Expansion Templates A-F** | **129-265** | **~1,400** | **25%** | **Inbox processing only** |
| Surgeon Rule & Memory Protocol | 267-280 | ~200 | 4% | Mixed |
| Directory Descriptions (10-90) | 282-329 | ~500 | 9% | Routing decisions |
| Mental Model Engine & Personas | 330-354 | ~350 | 6% | `{{...}}` expansion only |
| 17 Mental Models (names only) | 356-382 | ~300 | 5% | Rarely referenced directly |
| Conventions | 384-388 | ~50 | 1% | Every note creation |
| **TOTAL** | **388** | **~4,600** | **100%** | |

### 1.2 The Core Problem: Dead Weight Ratio

> [!CAUTION]
> **~60% of the prompt's tokens (Templates A-F + Mental Models + Personas + Drive Architecture) are consumed by reference material that is only relevant during one specific workflow: Inbox Processing.** This material sits inert in the context window during every other task (answering questions, writing code, managing files), actively competing with the user's actual query for attention.

**The Attention Dilution Effect:**
Modern transformer attention mechanisms allocate processing across *all* tokens in the context. When the model is asked to, say, help debug a C++ assignment, it must attend to ~1,400 tokens of template boilerplate (Templates A-F) that have zero relevance to the task. This:

1. **Reduces signal-to-noise ratio** -- the actual task instruction is a smaller percentage of the total context.
2. **Creates false activation paths** -- template keywords like "Ontological Definition", "Causal Chain", or "Mermaid graph" can bleed into unrelated outputs.
3. **Wastes the "primacy/recency" sweet spot** -- the templates are in the middle of the document (lines 129-265), which is precisely where LLMs have the weakest recall (the "lost in the middle" phenomenon).

### 1.3 The Mental Model Catalog (Lines 356-382)

The 17 mental models are listed *by name only* with a vague instruction to "get the detailed specifications of each model from `90_System/Agents/Gemini/`." This is problematic:

* The LLM **cannot dynamically load files** on its own initiative mid-generation. It needs to be *told* to use a tool or have the content already in context.
* Listing 17 names with one-line descriptions provides almost no actionable guidance -- it's a menu with no chef.
* If the intent is for the LLM to choose a mental model and then read the file, that multi-step tool-use chain is never explicitly orchestrated in the prompt.

**Diagnosis:** These 300 tokens act as a *decorative index* -- they feel thorough but produce no behavioral change in the LLM. The 23 actual `.md` files in `90_System/Agents/Gemini/` (confirmed on disk) are the real assets, but they are never loaded.

---

## 2. Ambiguity & Hallucination Vectors (The Shell Protocol)

### 2.1 The Shell-Pipe Protocol: A Hallucination Factory

> [!CAUTION]
> **This is the single most dangerous section of the entire prompt.** It instructs the LLM to compose and execute a shell command that spawns *another* LLM instance with a dynamically constructed prompt. This creates a cascade of failure modes.

**The instruction (Line 108):**
```
gemini -p "Expand this prompt with immense detail: {{prompt}}. Write the result directly to 00_Inbox/temp_expansion_N.md using your write_file tool." -y
```

#### Failure Mode 1: Nested Quoting Hell
The LLM must construct a string that contains:
- Outer shell quotes (`"..."`)
- The user's `{{prompt}}` content (which may itself contain quotes, special characters, or code)
- Instructions for the *child* LLM instance, including a file path

**Result:** The model frequently:
- Mangles the quoting (single vs double, escaping backslashes on Windows)
- Injects the template content *into* the shell command instead of the prompt
- Hallucinates a plausible-looking but syntactically broken command

#### Failure Mode 2: Recursive LLM Delegation
The parent LLM is told to delegate work to a child `gemini` CLI process. This is a **recursive self-invocation** with no shared context. The child process:
- Has no knowledge of the `GEMINI.md` system prompt
- Has no knowledge of the vault structure  
- Has no access to the Obsidian-specific formatting rules
- Has its own token limits, which may truncate the output

The parent LLM cannot reliably predict or control the child's output quality. The entire Inbox Processing pipeline assumes the child will:
1. Understand the vault context (it won't)
2. Use the correct template (it can't -- it doesn't have them)
3. Write to the correct file path (it might, if `write_file` is a tool it has)
4. Stay within the 500-word constraint (no enforcement mechanism)

#### Failure Mode 3: The "Immense Detail" vs. "500 Words" Paradox
The shell command says: *"Expand this prompt with immense detail."*
The constraint says: *"Each individual `{{...}}` expansion MUST be <= 500 words."*

These are **mutually exclusive directives**. "Immense detail" implies exhaustive coverage; 500 words implies ruthless compression. The LLM must resolve this contradiction on every invocation, and it does so unpredictably -- sometimes generating 1,500-word walls, sometimes producing terse 200-word stubs.

#### Failure Mode 4: The `-y` Auto-Approve Flag
The `-y` flag auto-approves tool calls in the child process. This means:
- File writes happen without confirmation
- If the child hallucinates a wrong path, it silently writes garbage to the vault
- There is no rollback mechanism

### 2.2 The `sequentialthinking` Tool Dependency (Line 94)

The prompt mandates: *"You MUST activate the `sequentialthinking` tool as your FIRST ACTION."*

This assumes:
1. The `sequentialthinking` MCP tool is always available (it may not be in every session)
2. The LLM correctly interprets "FIRST ACTION" as a literal tool call, not a mental planning step
3. The tool's output format is compatible with the next steps

If the tool is unavailable or returns an unexpected format, the entire processing pipeline stalls at Step 0 with no fallback defined.

---

## 3. Logic Conflicts & Impossible Constraints

### 3.1 Conflict Map

| # | Rule A | Rule B | Conflict |
| :--- | :--- | :--- | :--- |
| **C1** | "Immense Detail" (L105, L108) | "<= 500 words" (L117) | Directly contradictory output-length directives |
| **C2** | "Zero preamble" (Chief Engineer, L343) | Template headers require `> **Prompt:** "[Original Text]"` + `> **Lens Applied:**` (L133-134) | Templates mandate 2 lines of preamble before content |
| **C3** | "Surgeon Rule: Read-Only outside braces" (L268-270) | "Memory Protocol: silently save data" (L272-280) | Memory writes *are* modifications to external state, but Surgeon Rule implies strict non-modification |
| **C4** | "Treat each `{{...}}` as standalone" (L115) | "Link new notes to T.O.C" (L113) | Standalone implies self-contained; T.O.C linking implies dependency on vault structure |
| **C5** | "Start directly with definition" (Chief Engineer, L343) | "Include original text of prompt inside response" (Seed Rule, L118) | Seed Rule forces a preamble (the original prompt text) before the definition |
| **C6** | "Use Template" for creation (Convention 1, L385) | Templates A-F are for `{{...}}` expansion only | Ambiguous: does "creation" mean new notes generally, or only Obsidian Templater templates? |
| **C7** | Priority Rule: University > CS_Core (L97) | Graduation workflow: CS_Core is "evergreen" (L301) | No explicit trigger for when graduation happens; creates ambiguity about where synthesized notes live |

### 3.2 Deep Dive: C1 -- The "Immense Detail" Paradox

This is the root cause of the most visible failures. The conflict propagates through three layers:

```
Layer 1 (Shell Command): "Expand with immense detail"
    |
    v
Layer 2 (Balanced Depth Rule): "Strike a middle ground"
    |
    v
Layer 3 (Word Count): "<= 500 words"
```

The LLM encounters these in order during prompt processing. By the time it reaches Layer 3, it has already primed its generation strategy for "immense detail." The word count constraint then acts as a *post-hoc limiter* rather than a *planning constraint*, leading to either:
- Abrupt truncation mid-thought
- The model ignoring the constraint entirely
- Erratic output quality as the model tries to satisfy both

### 3.3 Deep Dive: C3 -- Surgeon Rule vs. Memory Protocol

The Surgeon Rule (L268-270) states: *"All text outside of `{{...}}` blocks is User Data. It is sacred and Read-Only."* This is scoped to file content during Inbox processing.

The Memory Protocol (L272-280) states: *"You MUST call the memory tool to save data AUTOMATICALLY."* This involves writing to an external knowledge graph (entities/relations).

**The ambiguity:** The Surgeon Rule uses absolute language ("sacred", "Read-Only", "strictly FORBIDDEN from...modifying"). A literal reading could cause the LLM to hesitate on *any* write operation -- including memory saves -- because the constraint's scope is not explicitly limited to "the current file's non-brace content." In practice, the LLM sometimes:
- Skips memory saves during Inbox processing (over-applying Surgeon Rule)
- Asks for permission to save memory (interpreting "silent" as conflicting with "sacred")

---

## 4. Architectural Strengths & Weaknesses

### 4.1 Strengths (Preserve These)

| Component | Lines | Why It Works |
| :--- | :--- | :--- |
| **Hybrid PARA Method** | 1-6 | Clear, proven organizational framework. Low token cost, high structural value. |
| **Graph Architecture & T.O.C Backbone** | 8-34 | Precise naming conventions and linking rules. Directly actionable. No ambiguity. |
| **Bridge Protocol** | 45-49 | Elegant mapping between physical and logical domains. Concise and unambiguous. |
| **Drive Architecture** | 53-83 | Clean partition map with access-level rules (ROM, RESTRICTED). Reads like an OS `fstab`. |
| **Directory Descriptions (10-90)** | 282-329 | Necessary routing context. Each section is concise and purpose-driven. |
| **Tagging Convention** | 22-33 | Three-axis taxonomy (`field/subject/concept`) is well-designed and enforceable. |
| **Conventions** | 384-388 | Four crisp rules. High signal density. |

**Common trait:** These sections are **declarative** (they describe *what* the system is) rather than **procedural** (they describe *how* to do things). Declarative context is cheap for LLMs -- it's reference material that doesn't create branching execution paths.

### 4.2 Weaknesses

#### W1: Over-Reliance on LLM Reasoning for Complex Orchestration
The Inbox Processing Protocol (Lines 89-265) is essentially a **program written in English** that the LLM is expected to interpret and execute as a state machine:

```
Step 0: Call sequentialthinking
Step 1: Classify files
Step 2: Split files atomically
Step 3: For each {{...}} block:
    3a: Try shell command
    3b: If fail, retry once
    3c: If fail again, fallback to internal generation
    3d: Classify and relocate output
    3e: Link to T.O.C
Step 4: Preserve non-brace content
Step 5: Save to memory
```

This is a 6-step procedure with conditional branching, error handling, and sub-loops. LLMs are not reliable state machines. They:
- Lose track of which step they're on after 3-4 tool calls
- Skip steps or execute them out of order
- Conflate sub-steps (e.g., doing classification *and* expansion in one pass, losing atomicity)

**This should be a script, not a prompt.**

#### W2: Templates as Dead Weight
The six templates (A-F) occupy ~1,400 tokens and are only used during `{{...}}` expansion. They are:
- Fully static (never modified by the LLM)
- Fully self-contained (no dependencies on other prompt sections)
- Infrequently triggered (only during Inbox processing)

**These are perfect candidates for RAG or dynamic loading.**

#### W3: Persona Definitions Without Activation Mechanism
The Chief Engineer and Navigator personas (Lines 334-354) define mandates, but there is no explicit mechanism for the LLM to "switch" between them. The prompt says *"fully inhabit the relevant persona"* but doesn't specify:
- How to determine which persona is relevant (the Template Selection Logic at L120-127 partially addresses this, but only for templates, not general conversation)
- Whether personas apply outside `{{...}}` expansion
- What happens when a topic spans both personas (e.g., "the psychology of debugging")

#### W4: The Mental Model Graveyard
23 mental model files exist in `90_System/Agents/Gemini/`. The prompt lists 17 of them by name. The remaining 6 files (`The_Archivist.md`, `The_Gardener.md`, `The_Pair_Programmer.md`, `The_Strict_Librarian.md`, `The_Study_Buddy.md`, `The_Tech_Lead.md`, `Mental_Model_Categories.md`) are unlisted -- orphaned knowledge assets that the LLM has no awareness of.

The listed 17 add ~300 tokens of cost with zero behavioral ROI, because:
1. The LLM never reads their backing `.md` files
2. The one-line descriptions are too vague to inform generation
3. No explicit instruction tells the LLM *when* or *how* to apply a specific model

---

## 5. Refactoring Strategy & Remediation

### 5.1 Guiding Principle: Separate Context from Procedure

```
GEMINI.md (Current)
================================
| Declarative Context (WHAT)   |  <-- Keep in system prompt
| Procedural Logic (HOW)       |  <-- Extract to scripts/workflows
| Reference Templates (FORMAT) |  <-- Extract to RAG/dynamic load
| Persona Definitions (WHO)    |  <-- Simplify or extract
================================

GEMINI.md (Refactored)
================================
| Declarative Context (WHAT)   |  ~1,700 tokens (from ~4,600)
| Minimal Procedural Hooks     |  ~300 tokens
================================
```

### 5.2 Concrete Refactoring Plan

#### Phase 1: Kill the Shell-Pipe Protocol (Critical -- Do First)

| Action | Detail |
| :--- | :--- |
| **Remove** Lines 105-113 entirely | The Shell-Pipe Protocol is unfixable within a prompt. |
| **Replace with** a simple rule | `"For each {{...}} block, expand it internally using the appropriate template. Load the template from 90_System/Templates/ if needed."` |
| **Alternative** | Write a Python/JS script in `90_System/Scripts/` that handles the orchestration externally, reading templates from disk and calling the Gemini API programmatically. |

#### Phase 2: Extract Templates to RAG / Dynamic Loading

| Action | Detail |
| :--- | :--- |
| **Move** Templates A-F | Create individual files: `90_System/Templates/Template_A_DeepDive.md`, `Template_B_Arena.md`, etc. |
| **Replace in GEMINI.md** | Keep only the Template Selection Logic (L120-127) and add: `"Load the selected template from 90_System/Templates/ before expanding."` |
| **Token savings** | ~1,400 tokens removed from persistent context. |

#### Phase 3: Collapse Mental Models into Actionable Rules

| Action | Detail |
| :--- | :--- |
| **Remove** the 17-model catalog (L356-382) | It produces no behavioral effect. |
| **Replace with** 3-4 core principles | Distill the 17 models into actionable heuristics, e.g.: `"Always explain WHY before WHAT. Identify edge cases. Use analogies for abstraction. Simplify at the end."` |
| **Keep** the backing `.md` files in `90_System/Agents/Gemini/` | They're useful reference material -- just don't load them into the system prompt. |
| **Token savings** | ~300 tokens removed. |

#### Phase 4: Simplify Personas

| Action | Detail |
| :--- | :--- |
| **Merge** Chief Engineer + Navigator | Into a single, concise behavioral directive: `"For CS/Technical topics: lead with internals, use analogies, cite edge cases. For general topics: trace root causes, connect to broader systems, cite evidence."` |
| **Remove** the "Trigger" concept | The LLM can naturally detect topic domain from the user's query. Explicit trigger lists add complexity without reliability. |
| **Token savings** | ~300 tokens removed. |

#### Phase 5: Resolve the Constraint Conflicts

| Conflict | Resolution |
| :--- | :--- |
| **C1** (Immense Detail vs. 500 words) | Remove "immense detail." Replace with: `"Provide a thorough but concise expansion (~300-500 words)."` |
| **C2** (Zero preamble vs. Template headers) | Add to templates: `"The Prompt/Lens header is structural metadata, not preamble. Content starts at Section 1."` |
| **C3** (Surgeon Rule vs. Memory Protocol) | Scope the Surgeon Rule explicitly: `"Do not modify user-written text in the source file. Memory tool writes to external storage and are always permitted."` |
| **C5** (Direct definition vs. Seed Rule) | Redefine Seed Rule: `"Include the original prompt text in the template's Prompt field (header), then start content immediately."` |

#### Phase 6: Convert Inbox Protocol to a Workflow Script

| Action | Detail |
| :--- | :--- |
| **Create** `90_System/Scripts/process_inbox.md` | A step-by-step workflow document that the LLM can be pointed to when Inbox processing is needed. |
| **In GEMINI.md** | Replace 176 lines of Inbox protocol with: `"To process the Inbox, follow the workflow in 90_System/Scripts/process_inbox.md."` |
| **Token savings** | ~2,100 tokens removed from persistent context. |

### 5.3 Projected Result

| Metric | Before | After | Change |
| :--- | :--- | :--- | :--- |
| **Total Lines** | 388 | ~130 | -66% |
| **Est. Tokens** | ~4,600 | ~1,700 | -63% |
| **Dead Weight Ratio** | ~60% | ~10% | -50pp |
| **Hallucination Vectors** | 4 identified | 0 critical | Eliminated |
| **Logic Conflicts** | 7 identified | 0 unresolved | Resolved |

### 5.4 Proposed Refactored File Structure

```
90_System/
  Templates/
    Template_A_DeepDive.md
    Template_B_Arena.md
    Template_C_RosettaStone.md
    Template_D_Chronograph.md
    Template_E_Algorithmist.md
    Template_F_Debugger.md
  Scripts/
    process_inbox.md          # Workflow for Inbox processing
  Agents/Gemini/
    [existing 23 mental model files -- unchanged]
  Issues/
    System_Prompt_Diagnostic_Report.md   # This file

GEMINI.md (Root)
  Section 1: Vault Overview & PARA Structure     (~200 tokens)
  Section 2: Graph Architecture & T.O.C Rules    (~300 tokens)
  Section 3: Drive Architecture & Bridge Protocol (~500 tokens)
  Section 4: Directory Routing Table (10-90)      (~400 tokens)
  Section 5: Core Behavioral Directives           (~200 tokens)
  Section 6: Conventions                          (~100 tokens)
  TOTAL:                                          ~1,700 tokens
```

---

## Appendix A: Risk Assessment of Inaction

If `GEMINI.md` is left in its current state:

1. **Inbox processing will continue to fail** -- the Shell-Pipe Protocol is structurally broken and will produce corrupted or misplaced files.
2. **General-purpose performance will degrade** -- every non-Inbox interaction pays a ~3,000 token "tax" for reference material it never uses.
3. **Mental Model investment is wasted** -- the 23 carefully written `.md` files in `Agents/Gemini/` are never loaded, making the entire Mental Model Engine decorative.
4. **Constraint conflicts will produce inconsistent output** -- the LLM will resolve contradictions differently each session, making behavior unpredictable.

---

## Appendix B: Quick Reference -- What to Keep vs. Remove

| Verdict | Section | Reason |
| :--- | :--- | :--- |
| **KEEP** | Vault Overview (L1-6) | Core identity, low cost |
| **KEEP** | Graph Architecture (L8-34) | Actionable, precise |
| **KEEP** | Bridge Protocol (L45-49) | Elegant, essential |
| **KEEP** | Drive Architecture (L53-83) | Necessary routing |
| **KEEP** | Directory Descriptions (L282-329) | Necessary routing |
| **KEEP** | Conventions (L384-388) | High signal density |
| **EXTRACT** | Templates A-F (L129-265) | To `90_System/Templates/` |
| **EXTRACT** | Inbox Protocol (L89-118) | To `90_System/Scripts/process_inbox.md` |
| **SIMPLIFY** | Personas (L334-354) | Merge into 2-3 behavioral sentences |
| **REMOVE** | Shell-Pipe Protocol (L105-113) | Unfixable hallucination vector |
| **REMOVE** | Mental Model Catalog (L356-382) | Zero behavioral ROI |
| **REMOVE** | "Immense Detail" phrasing (L105, L108) | Contradicts word constraints |
