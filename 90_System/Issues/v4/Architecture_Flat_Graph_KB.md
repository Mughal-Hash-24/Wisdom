# Kybernetes Architecture: The Flat-Graph Knowledge Base (V4)

**Status:** Proposed Architecture  
**Target Category:** `30_Knowledge_Base`  
**Core Philosophy:** Move away from nested "Subject Folders" (which create messy boundaries) and rely entirely on structural types (`Atlas`, `Concepts`, `Entities`, `Frameworks`), letting the YAML Frontmatter Tags and `T.O.C` Backbones do the heavy lifting of domain routing.

---

## 1. Directory Structure

The `30_Knowledge_Base` folder will be strictly flattened into four subdirectories, representing the ontological nature of the note, *not* its subject matter.

```text
30_Knowledge_Base/
├── 00_Atlas/        (The Maps)
├── 10_Concepts/     (Atomic Ideas & Theories)
├── 20_Entities/     (Physical/Historical Things & People)
└── 30_Frameworks/   (Methodologies & Systems)
```

---

## 2. Definitions & Domain Mapping

How do the 7 non-CS Domain Agents map their content into these four structural buckets? 

### A. `00_Atlas/` (The Backbone)
*   **Purpose:** The central navigation hubs. This folder contains ONLY `T.O.C ({Subject}).md` files.
*   **Agent Interaction:** The `@librarian` updates these files when routing a new note.
*   **Format:** A bulleted list of links grouped by sub-theme.
*   **Examples:** `T.O.C (History).md`, `T.O.C (Philosophy).md`, `T.O.C (Economics).md`.

### B. `10_Concepts/`
*   **Purpose:** Atomic, abstract ideas or phenomena. If it is an intangible noun, it goes here.
*   **Agent Mapping:**
    *   `@iqbal` (Philosophy): `Nihilism.md`, `Categorical_Imperative.md`
    *   `@machiavelli` (Social Sci): `Opportunity_Cost.md`, `Tragedy_of_the_Commons.md`
    *   `@newton` / `@alhaytham` (Science): `Entropy.md`, `Natural_Selection.md`
    *   `@nabokov` (Literature): `The_Unreliable_Narrator.md`

### C. `20_Entities/`
*   **Purpose:** People, physical events, tangible artifacts, books, and empires. If you can touch it, point to it on a map, or shake its hand, it goes here.
*   **Agent Mapping:**
    *   `@ibnkhaldun` (History): `Julius_Caesar.md`, `The_French_Revolution.md`, `The_Bronze_Age_Collapse.md`
    *   `@davinci` (Art): `The_Mona_Lisa.md`, `The_Sistine_Chapel.md`
    *   `@nabokov` (Literature): `The_Brothers_Karamazov_Book.md`, `Hamlet_Character.md`
    *   `@machiavelli` (Social Sci): `The_Federal_Reserve.md`

### D. `30_Frameworks/`
*   **Purpose:** Systems, methodologies, complex models, and "Isms." If it is a lens through which to view the world or a multi-step process, it goes here.
*   **Agent Mapping:**
    *   `@machiavelli` (Social Sci): `Keynesian_Economics.md`, `Game_Theory.md`
    *   `@iqbal` (Philosophy): `Stoicism.md`, `Utilitarianism.md`
    *   `@alhaytham` (Science): `The_Scientific_Method.md`
    *   `@davinci` (Art): `Cubism.md`, `Gothic_Architecture.md`

---

## 3. The YAML Tagging Matrix ("Night Sky" Aesthetics)

Because the folders no longer dictate the subject, the **Frontmatter Tags** become the absolute source of truth for graphing and retrieval. The `@librarian` will enforce exactly two levels of hierarchy: `#field/` and `#subject/`.

| Domain Agent | Primary `#field` Tag | Visual Graph Color | Example `#subject` Tags |
| :--- | :--- | :--- | :--- |
| `@iqbal` | `#field/humanities` | Emerald Green | `#subject/philosophy`, `#subject/ethics` |
| `@nabokov` | `#field/humanities` | Emerald Green | `#subject/literature`, `#subject/poetry` |
| `@ibnkhaldun` | `#field/humanities` | Emerald Green | `#subject/history`, `#subject/geopolitics` |
| `@davinci` | `#field/humanities` | Emerald Green | `#subject/art`, `#subject/architecture` |
| `@machiavelli` | `#field/social_science` | Gold / Yellow | `#subject/economics`, `#subject/psychology` |
| `@newton` | `#field/hard_science` | Deep Purple | `#subject/physics`, `#subject/astronomy` |
| `@alhaytham` | `#field/hard_science` | Deep Purple | `#subject/biology`, `#subject/chemistry` |

*(Note: `#field/cs` (Neon Blue) and `#field/math` (Vivid Orange) are handled by `@turing` and `@euler` respectively, routing to `20_CS_Core`, not the general Knowledge Base.)*

---

## 4. Operational Workflow Updates (The `@librarian`)

To implement this, the `@librarian` skill/prompt must be updated.

**Current Librarian Logic:** "Is this history? Move to `30_Knowledge_Base/History`."
**V4 Librarian Logic:**
1. **Identify the Type:** Is the content an abstract idea (Concept), a tangible thing/person (Entity), or a system (Framework)?
2. **Move:** Route to `10_Concepts`, `20_Entities`, or `30_Frameworks`.
3. **Tag:** Read the expansion content to determine the agent's domain (`@iqbal` = `#subject/philosophy`). Inject the tags into the YAML frontmatter.
4. **Link to Atlas:** Append a downlink string (e.g., `- [[Nihilism]]`) to the corresponding `00_Atlas/T.O.C (Philosophy).md` file.
5. **Add Uplink:** Insert `[[T.O.C (Philosophy)|Up to Philosophy]]` at the top of the newly moved note.

## 5. Benefits of the Flat-Graph

1. **Eliminates Categorization Paralysis:** The user (or `@librarian`) no longer struggles with "Does the French Revolution go in History or Political Science?" It goes in `20_Entities`. The tags (`#subject/history`, `#subject/political_science`) handle the nuance.
2. **Prepares for `@polymath`:** When formatting the vault to support an agent explicitly searching for cross-disciplinary synthesis, flat structures ensure the agent isn't fighting nested directory traversals.
3. **Graph Aesthetics:** By relying on `#field` and `#subject` tags instead of folders, the Obsidian Graph View will cluster concepts purely by intellectual discipline, blooming outward from the `00_Atlas` hubs.
