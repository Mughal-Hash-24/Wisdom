# Kybernetes OS: v4 Tentative Roadmap & Ideas

Now that the core Domain Agents (`@turing`, `@euler`, etc.) and the Pipeline Agents (`@librarian`, `@surgeon`) are functioning flawlessly, the focus for **Kybernetes v4** should shift from raw content generation to **synthesis, proactive automation, and deep connection.**

Here are some high-level architectural proposals for v4:

## 1. The `@polymath` (Synthesis Agent)
*   **Concept:** While the current 9 agents are hyper-specialized (vertical expansion), the system lacks an agent responsible for *horizontal integration*.
*   **Function:** The `@polymath` scans the vault (specifically `20_CS_Core`, `10_University`, `30_Knowledge_Base`) looking for structural similarities across domains. 
*   **Example:** It notices you are learning about Genetic Algorithms in CS and Natural Selection in Biology, and proactively drafts a synthesis note connecting the computational implementation to the biological reality, tagging it `#type/map`.

## 2. Active RAG (Retrieval-Augmented Generation) for Agents
*   **Concept:** Currently, domain agents expand prompts purely based on the original note's local context and their system prompts.
*   **Function:** Inject a Vector DB or semantic search tool into the domain agents. Before `@turing` explains a concept, it queries the vault to see how you previously defined related concepts. 
*   **Result:** The generated notes will reference *your* past notes (e.g., "Building on your previous definition of Heuristics in `1.3.10 - A Star Algorithm.md`, we can see..."). It creates an expanding web of self-referential knowledge.

## 3. The "Bridge Protocol" Daemon (Continuous Sync)
*   **Concept:** The physical drive (`D:\PROJECTS`) and the Brain (`40_Projects`) are currently linked via manual commands.
*   **Function:** A lightweight background service (or a scheduled script running on boot) that watches `D:\PROJECTS`. When you push code, create a new file, or update a `README.md` structurally, it automatically drafts an update to the corresponding `40_Projects` doc.
*   **Result:** True CI/CD for your Personal Knowledge Management. Real-time documentation mirroring your codebase.

## 4. Spaced Repetition (Anki/Flashcards) Extraction
*   **Concept:** Notes in `20_CS_Core` are "evergreen," but the underlying definitions must be memorized for long-term retention.
*   **Function:** Add an `@interrogator` agent tool to the `/os:sort` pipeline. After `@surgeon` stitches the note, the interrogator scans it for core definitions, theorems, or formulas, and compiles them into a JSON/CSV file.
*   **Integration:** You can then automatically push this file to an Anki deck via AnkiConnect API.

## 5. Web GUI Visualization Dashboards (Kybernetes UI)
*   **Concept:** The terminal output is functional, but as a system builder, you need a high-altitude view.
*   **Function:** Build the cyberpunk-aesthetic GUI project we discussed previously (React/Next.js/Tauri). It won't replace Obsidian for reading notes, but will serve as the *Control Panel*.
*   **Features:**
    *   Monitor the `/os:sort` pipeline passing data between agents visually (like a node-graph).
    *   Real-time system health alerts.
    *   A consolidated, physical "Inbox" visualizer before running the sorting command.

## 6. The "Devil's Advocate" Verification
*   **Concept:** Deliverables (Assignments, architectural plans) need rigorous testing before execution.
*   **Function:** Before a plan or assignment is finalized, dispatch the `@socrates` or `@machiavelli` agent to actively attack the logic. They will read a plan and output a critique document listing all edge cases, missing constraints, or architectural flaws.

---
*Brainstormed by Antigravity - 2026-03-09*
