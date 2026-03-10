# The Polymath Agent: Implementation Plan

## 1. Context & Core Purpose
Currently, your 9 domain agents (e.g., `@turing`, `@euler`, `@nabokov`) represent **vertical expansion**. They take a specific seed in a specific field and drill deep into it. 

The `@polymath` represents **horizontal synthesis**. Its purpose is to act as the "connective tissue" of your Kybernetes OS. Instead of generating new foundational knowledge, it scans the existing structured knowledge in `10_Concepts`, `20_Entities`, and `30_Frameworks` to find isomorphic patterns across completely unrelated disciplines.

**Key Values:**
- **Serendipity Engine:** It finds connections you might have missed (e.g., Game Theory in Economics vs. Evolutionary Biology vs. System Architecture).
- **Map Generation:** It creates `#type/map` notes that sit above individual concepts, weaving them into a cohesive narrative.
- **True PKM:** It fulfills the ultimate goal of a Second Brain—not just storing information, but actively generating new insights from the combination of stored ideas.

---

## 2. Trigger Mechanism & Workflow
Unlike the domain agents triggered by `/os:sort` on individual `{{...}}` prompts, `@polymath` should operate on a macro-level. 

### Proposed Command: `/os:synthesize {Concept/Topic}`
When you run this command, the system triggers a dedicated `synthesis_engine` skill.

**Workflow Pipeline:**
1. **The Scout:** A tool queries the vault (via `grep_search` or an active RAG vector search) using the target topic to retrieve paths of related notes across *all* domains.
2. **The Reader:** The `@polymath` agent is dispatched. It reads the raw contents of 5-10 retrieved notes.
3. **The Synthesizer:** The `@polymath` identifies cross-disciplinary analogies, common structural patterns, and conflicting viewpoints.
4. **The Cartographer:** It drafts a new Map of Content (MOC) note (e.g., `MOC - The Architecture of Feedback Loops.md`), effectively linking all the source notes together.
5. **The Archivist:** It saves this new Map in `10_Concepts/Maps` or directly in `00_Atlas/MOCs`.

---

## 3. Agent Definition (`.gemini/agents/polymath.md`)
We will need to create a new agent configuration file.

**Personality/Voice:** The Synthesizer. Curious, pattern-seeking, and highly structural. 
**Directive:** 
- Look for structural isomorphisms. 
- Use analogies to bridge hard sciences (CS, Math, Physics) with humanities/social sciences (History, Philosophy, Economics).
- Never just list things; draw the thread connecting them.

**Required Tools:**
- `wisdom-os__search_vault`: To find keyword overlaps across directory structures.
- `wisdom-os__read_note` (or batch file reader): To ingest the context of multiple notes.
- `wisdom-os__create_note`: To write the synthesized Map note.

---

## 4. RAG Integration (Crucial Dependency)
For the `@polymath` to truly shine, we cannot rely solely on simple keyword searches (like `grep`). We need **Semantic Search (Active RAG)**.

Before deploying `@polymath`, we should implement a lightweight Vector Database (e.g., using a local embedding model or a text-based semantic plugin within Obsidian/Kybernetes). 
**Why?** Because a search for "optimization" should pull up both a CS note on "A* Algorithms" and a Philosophy note on "Utilitarianism", even if they don't share exact keywords.

---

## 5. Phased Rollout Strategy

### Phase A: The Manual Polymath (No RAG)
1. Create `polymath.md` in `agents/`.
2. Create a `synthesis` skill.
3. The user passes 2 or 3 explicitly defined note URLs to the command (e.g., `/os:synthesize [[Game_Theory_Basics]] [[Darwinian_Evolution]]`).
4. `@polymath` reads those specific files and drafts a connection note.

### Phase B: The Automated Polymath (With RAG)
1. Implement a semantic search tool within `tools.py`.
2. Update the `synthesis` skill so the user only provides a *theme* (e.g., `/os:synthesize "Resource Scarcity"`).
3. The tool automatically fetches the 5 most semantically relevant notes across the vault.
4. `@polymath` reads them and builds the macro-map.

### Phase C: The Background Daemon
1. `@polymath` runs passively in the background (e.g., during the `/os:boot` sequence).
2. It randomly selects notes and suggests "Did you know?" connections in your Daily Note, prompting you to review unseen alignments in your own brain.
