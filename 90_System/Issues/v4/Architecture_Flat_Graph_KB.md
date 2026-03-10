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
## 3. The YAML Tagging Matrix (Expanded Taxonomy)

Because the folders no longer dictate the subject, the **Frontmatter Tags** become the absolute source of truth for graphing and retrieval. The system enforces exactly two levels of hierarchy: `#field/` and `#subject/`. Atomic ideas are tagged `#concept/...`.

Below is the definitive taxonomy for `30_Knowledge_Base`. This ensures your graph view colors ("Night Sky" aesthetics) remain pristine and clustered correctly.

| Domain Agent | Primary `#field` Tag | Visual Graph Color | Valid `#subject` Tags (Examples) |
| :--- | :--- | :--- | :--- |
| `@iqbal` | `#field/humanities` | Emerald Green | `philosophy`, `ethics`, `epistemology`, `logic`, `theology` |
| `@nabokov` | `#field/humanities` | Emerald Green | `literature`, `poetry`, `mythology`, `rhetoric`, `linguistics` |
| `@ibnkhaldun` | `#field/humanities` | Emerald Green | `history`, `geopolitics`, `law`, `anthropology`, `archaeology` |
| `@davinci` | `#field/humanities` | Emerald Green | `art`, `architecture`, `music`, `design`, `photography` |
| `@machiavelli` | `#field/social_science` | Gold / Yellow | `economics`, `psychology`, `sociology`, `game_theory`, `political_science` |
| `@newton` | `#field/hard_science` | Deep Purple | `physics`, `astronomy`, `mechanics`, `thermodynamics` |
| `@alhaytham` | `#field/hard_science` | Deep Purple | `biology`, `chemistry`, `medicine`, `ecology`, `genetics` |

*(Note: `#field/cs` (Neon Blue) and `#field/math` (Vivid Orange) are strictly handled by `@turing` and `@euler` respectively, routing to `20_CS_Core`, not `30_Knowledge_Base`.)*

### Cross-Disciplinary Tagging Rules:
- A note can legally have **two** `#subject/` tags, but ideally only **one** `#field/` tag to maintain its primary color cluster. 
- Example: "Behavioral Economics" goes in `10_Concepts/` with tags: `tags: ["field/social_science", "subject/economics", "subject/psychology"]`.

---

## 4. Handling Multiplicity (The Hub and Spoke Model)

**The User Question:** *What if we have multiple files for the same entity or concept?*
**The Problem:** If you write 5 different notes about "Julius Caesar" (e.g., his military campaigns, his assassination, his youth), placing them all in `20_Entities/` clutters the list with variations like `Julius_Caesar_Assassination.md`, `Julius_Caesar_Youth.md`.

**The Solution:** Implement the **Map of Content (MOC) / Hub and Spoke Model**.

1. **The Hub (Base Entity):**
   - The primary file remains in `20_Entities/Julius_Caesar.md`.
   - This note acts as an encyclopedia entry and a **mini-T.O.C** for this specific entity.
2. **The Spokes (Facets):**
   - If a topic warrants its own deep-dive file (e.g., "The Assassination of Julius Caesar"), it is created with a strict naming convention: `Entity_Facet.md` (e.g., `Julius_Caesar_Assassination.md`).
   - The Spoke file lives either in the same folder `20_Entities/` OR, more cleanly, you create a subfolder exactly matching the Hub's name *only if* it has more than 3 spokes: `20_Entities/Julius_Caesar/Assassination.md`.
3. **The Linking Rule:**
   - The Hub (`Julius_Caesar.md`) links *down* to all its spokes.
   - Every Spoke (`Julius_Caesar_Assassination.md`) must link *up* to the Hub immediately after its frontmatter:
     `[[Julius_Caesar|Up to Julius Caesar]]`
   
This maintains the Flat-Graph integrity. If you search for "Julius Caesar", you hit the Hub, which elegantly arrays all detailed sub-notes, rather than wading through a flat list of 50 disconnected Roman history files.

---

## 5. The `00_Atlas` Foundation (Initial Subject Hubs)

When starting V4, the `00_Atlas` directory will be populated with a standardized set of `T.O.C` files. These act as the root nodes for your Knowledge Base graph. 

Because the strict folder rule states `T.O.C ({Folder_Name}).md`, but these files live in `00_Atlas`, the convention here is: `T.O.C ({Subject_Name}).md`. 

Here are the **Initial 7 Subject Hubs** mapped to your agents, alongside their standard internal format:

1.  **`T.O.C (Philosophy).md`** (Ethics, Logic, Epistemology — `@iqbal`)
2.  **`T.O.C (History).md`** (Geopolitics, Eras, Biographies — `@ibnkhaldun`)
3.  **`T.O.C (Social Science).md`** (Economics, Psychology, Sociology — `@machiavelli`)
4.  **`T.O.C (Literature).md`** (Fiction, Poetry, Rhetoric — `@nabokov`)
5.  **`T.O.C (Arts & Aesthetics).md`** (Architecture, Music, Design — `@davinci`)
6.  **`T.O.C (Physical Science).md`** (Physics, Astronomy, Mechanics — `@newton`)
7.  **`T.O.C (Biological Science).md`** (Biology, Medicine, Ecology — `@alhaytham`)

### Standard T.O.C Format (Structured Table Paradigm)
As per your graph architecture rules for complex subjects, the `00_Atlas` T.O.C files must use the **Structured Table** format. This ensures metadata (like specific domain tags) is visible at a glance.

*Example content for `T.O.C (Philosophy).md`:*
```markdown
# Philosophy & Ethics Hub
#type/map #field/humanities #subject/philosophy

[[T.O.C (00_Atlas)|Up to Atlas Index]]

| ID | Category | Concept / Entity | Field/Tags |
| :--- | :--- | :--- | :--- |
| **F.01** | Framework | [[Stoicism]] | `#subject/ethics` |
| **F.02** | Framework | [[Utilitarianism]] | `#subject/ethics` |
| **E.01** | Entity | [[Friedrich_Nietzsche]] | `#subject/philosophy` |
| **E.02** | Entity | [[Immanuel_Kant]] | `#subject/philosophy` |
| **C.01** | Concept | [[The_Overman]] | `#concept/existentialism` |
| **C.02** | Concept | [[Categorical_Imperative]] | `#concept/morality` |
```
*(Note: ID format uses `C.xx` for Concepts, `E.xx` for Entities, `F.xx` for Frameworks to maintain order and structure without clashing with the University X.Y.Z numbered system).*

---

## 6. Strict File Formatting Standards

To ensure the `@librarian` and domain agents output perfectly uniform files, every file type in the `30_Knowledge_Base` must adhere to these rigid templates.

### A. The Standard Note (Concepts, Frameworks, Entities)
*Target: `10_Concepts/`, `20_Entities/`, `30_Frameworks/`*
*Rule: Strict YAML frontmatter + Uplink.*

```markdown
---
tags:
  - field/[domain]
  - subject/[topic]
  - concept/[atomic_idea] (Optional)
---
[[T.O.C ({Subject_Name})|Up to {Subject_Name}]]

# {Note Title}

{Agent Expanded Content...}
```

### B. The Hub Note (MOC for Complex Entities)
*Target: `20_Entities/{Hub_Name}.md`*
*Rule: Acts as both a standard note AND a mini table of contents for its Spokes.*

```markdown
---
tags:
  - field/[domain]
  - subject/[topic]
---
[[T.O.C ({Subject_Name})|Up to {Subject_Name}]]

# {Hub Title} (e.g., Julius Caesar)

{Brief Encyclopedia Summary Content...}

## Facets & Deep Dives
| ID | Topic | Link |
| :--- | :--- | :--- |
| **S.01** | Assassination | [[Julius_Caesar_Assassination]] |
| **S.02** | Gallic Wars | [[Julius_Caesar_Gallic_Wars]] |
```

### C. The Spoke Note (Deep-Dive Facet)
*Target: `20_Entities/` or `20_Entities/{Hub_Name}/`*
*Rule: Must uplink to the HUB rather than the `00_Atlas` T.O.C.*

```markdown
---
tags:
  - field/[domain]
  - subject/[topic]
---
[[{Hub_Name}|Up to {Hub_Name}]]

# {Spoke Title} (e.g., The Assassination of Julius Caesar)

{Granular Deep-Dive Content...}
```

---

## 7. Operational Workflow Updates (The `@librarian`)

To implement this, the `@librarian` skill/prompt must be updated.

**Current Librarian Logic:** "Is this history? Move to `30_Knowledge_Base/History`."
**V4 Librarian Logic:**
1. **Identify the Type:** Is the content an abstract idea (Concept), a tangible thing/person (Entity), or a system (Framework)?
2. **Move:** Route to `10_Concepts`, `20_Entities`, or `30_Frameworks`.
3. **Tag:** Read the expansion content to determine the agent's domain (`@iqbal` = `#subject/philosophy`). Inject the tags into the YAML frontmatter per the Taxonomic Matrix.
4. **Link to Atlas/Hub:** Append a downlink string (e.g., `- [[Nihilism]]`) to the corresponding `00_Atlas/T.O.C ({Subject}).md` file under the correct structural heading (Concepts/Entities/Frameworks). If the file is a Spoke, link it to its Entity Hub instead.
5. **Add Uplink:** Insert `[[T.O.C ({Subject})|Up to {Subject}]]` at the top of the newly moved note.

## 7. Benefits of the Flat-Graph

1. **Eliminates Categorization Paralysis:** The user (or `@librarian`) no longer struggles with "Does the French Revolution go in History or Political Science?" It goes in `20_Entities`. The tags (`#subject/history`, `#subject/political_science`) handle the nuance.
2. **Prepares for `@polymath`:** When formatting the vault to support an agent explicitly searching for cross-disciplinary synthesis, flat structures ensure the agent isn't fighting nested directory traversals.
3. **Graph Aesthetics:** By relying on `#field` and `#subject` tags instead of folders, the Obsidian Graph View will cluster concepts purely by intellectual discipline, blooming outward from the `00_Atlas` hubs.
