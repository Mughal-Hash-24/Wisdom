# V4 Migration Plan: The Flat-Graph Knowledge Base

**Objective:** Systematically migrate Kybernetes from the legacy nested-folder Knowledge Base (`30_Knowledge_Base/Finance`, `History`, etc.) to the V4 structural Flat-Graph model (`00_Atlas`, `10_Concepts`, `20_Entities`, `30_Frameworks`), updating all pipelines, agents, and system constraints.

This is a **Zero-Downtime** migration strategy broken into 4 distinct phases.

---

## Phase 1: Infrastructure Pre-requisites (The Scaffold)

Before touching a single note, the structural skeleton must be built.

1.  **Create V4 Directories:**
    *   Initialize `30_Knowledge_Base/00_Atlas/`
    *   Initialize `30_Knowledge_Base/10_Concepts/`
    *   Initialize `30_Knowledge_Base/20_Entities/`
    *   Initialize `30_Knowledge_Base/30_Frameworks/`
2.  **Generate `00_Atlas` Hubs:**
    *   Create the 7 primary `T.O.C ({Subject_Name}).md` files inside `00_Atlas/`.
    *   Populate each with the **Structured Table** format (empty rows for now).
    *   Create a master `T.O.C (00_Atlas).md` that links to the 7 subject maps.
3.  **Sanity Check Obsidian Settings:**
    *   Ensure "Automatically update internal links" is **enabled** in Obsidian. This is critical for Phase 2, so moving files doesn't break the graph.

---

## Phase 2: System Kernel & Agent Reprogramming

Updating the LLM logic to recognize the new reality.

1.  **Modify Global Kernel (`GEMINI.md`)**
    *   *Action:* Locate the `<MEMORY[GEMINI.md]>` section defining `30_Knowledge_Base`.
    *   *Change:* Remove references to "Finance, Psychology, History" folders.
    *   *Insert:* Hardcode the strict ontology: "30_Knowledge Base is structurally partitioned into: 00_Atlas (T.O.C Maps), 10_Concepts (Abstract Ideas), 20_Entities (Tangible Things/People), 30_Frameworks (Systems/Models). No nested subject folders are permitted."
    *   *Insert:* Hardcode the Tagging Matrix (`#field/...`, `#subject/...`) to bind the domain agents rigidly to their graph colors.

2.  **Reprogram `@librarian` (The Router)**
    *   *Action:* Overhaul `c:\Users\ibtas\.gemini\agents\librarian.md`.
    *   *Old Logic:* "Route based on subject matter."
    *   *New Logic:* 
        *   Determine if a note is an Idea, a Thing, or a System.
        *   Move to `10_Concepts`, `20_Entities`, or `30_Frameworks`.
        *   Ensure YAML frontmatter is injected (using the Taxonomic Matrix).
        *   Append the note as a Table Row (`| C.xx | Concept | [[NoteName]] | #tag |`) inside the appropriate `00_Atlas/T.O.C ({Subject_Name}).md` map.
        *   Inject the correct uplink at line 5: `[[T.O.C ({Subject_Name})\|Up to {Subject_Name}]]`.

3.  **Update `tools.py` Formatting Constraints**
    *   *Action:* Verify tools like `create_note` or `ensure_toc_link` do not use deprecated folder paths for fallback.

---

## Phase 3: The "Great Migration" (Content Sorting)

Moving the existing legacy notes into the new V4 flat structure.

1.  **The Extraction Protocol (`find` & move):**
    *   Script a Python job or manually use `@librarian` to scan all notes in `30_Knowledge_Base/History/`, `Finance/`, etc.
2.  **Per-File Migration Chain:**
    *   *Read Note.*
    *   *Decide Type* (Concept, Entity, Framework).
    *   *Inject Tags* (e.g., `#field/social_science`, `#subject/economics`).
    *   *Move* to `10_Concepts/`, `20_Entities/`, or `30_Frameworks/`.
    *   *Add Uplink* to the corresponding `00_Atlas` T.O.C.
    *   *Add Downlink Row* in the Atlas T.O.C table.
3.  **Legacy Directory Purge:**
    *   Once empty, permanently delete the old subject folders (e.g., `/Finance`, `/History`). 
    *   The `30_Knowledge_Base` root must contain only the 4 structural folders.

---

## Phase 4: Hub & Spoke Consolidation (Graph Pruning)

Addressing the "Multiplicity" problem for dense topics.

1.  **Identify Clustered Entities:**
    *   Scan `20_Entities/` for excessive semantic overlap (e.g., 4 notes about various World War II battles).
2.  **Generate Hubs:**
    *   Determine the central Entity (e.g., `World_War_II.md`).
    *   Format it as a Hub Note (containing the `## Facets & Deep Dives` table).
3.  **Refactor Spokes:**
    *   Ensure the facet notes (e.g., `WWII_Battle_of_Midway.md`) have their uplinks changed from `[[T.O.C (History)]]` to `[[World_War_II|Up to World War II]]`.
    *   Add them to the Hub's Table of Contents.
    *   Remove them from the primary `00_Atlas` T.O.C to clear the clutter, ensuring the Graph remains clean and hierarchical.

---

## Post-Migration Sign-Off

*   **Test 1 (Routing):** Drop a raw note with `{{Explain the gold standard}}` into `00_Inbox`. Run `/os:sort`. Verify it ends up in `10_Concepts/` with `#field/social_science` and `#subject/economics` tags, and appears precisely in the table of `T.O.C (Social Science).md`.
*   **Test 2 (Graph Visuals):** Open the Obsidian Graph View. Verify strict clustering of the designated Neon Blue, Deep Purple, Emerald Green, and Gold notes with no messy cross-contamination. 
