# Vault Explorer UI

## Purpose
A dedicated, lightweight frontend optimized for browsing the Obsidian Vault's strict folder structure, interpreting the `T.O.C` files natively, and rendering Markdown files with clickable Wiki-links (`[[...]]`).

## Interface Layout

### 1. Left Sidebar: The File Tree (Multi-level Traversal)
*   **Behavior:** A native folder tree displaying the `d:\WISDOM\Kybernetes` directories (`10_University`, `20_CS_Core`, etc.).
*   **T.O.C Auto-Detection:** If a folder contains a file named `T.O.C ({FolderName}).md`, clicking the folder itself automatically renders that T.O.C file in the main viewing pane.
*   **Aesthetic:** Clean, high-contrast text on a very dark background (`#0A0A0C`), hiding Markdown extensions (`.md`) from the UI for a cleaner look.

### 2. Main Pane: T.O.C Render Engine
When a T.O.C file is opened, the UI parses and renders it not just as plain markdown, but as an interactive dashboard.

*   **For Structured Tables (e.g. `| ID | Category | Content |`):**
    *   Parses the Markdown table and renders it as an interactive data grid.
    *   Any `[[NoteTitle]]` in the "Content" column is rendered as a clickable hyperlink.
*   **For Bullet Lists (e.g. `- [[NoteFile]]`):**
    *   Renders as a clean index list.
*   **Routing Logic:** Clicking any `[[Link]]` resolves the relative or absolute path within the vault and opens the target `.md` file.

### 3. Main Pane: Markdown Document Viewer
When a standard note (e.g., `1.1.1 - Defining Intelligence.md`) is opened:

*   **Frontmatter Parsing:** 
    *   Reads the YAML frontmatter.
    *   Visualizes tags beautifully as colored badges at the top right of the note. Uses the "Night Sky" coloring logic (e.g., `#field/cs` gets a **Neon Blue** badge, `#field/math` gets **Vivid Orange**).
*   **The Uplink / Breadcrumb:**
    *   The mandatory first line (e.g., `[[T.O.C (Artificial Intelligence Notes)|Up to AI Notes]]`) is rendered as a prominent "Back to Parent T.O.C" button floating at the top left of the document, ensuring you never get lost in the tree.
*   **Markdown Body Rendering:**
    *   Standard GitHub-flavored Markdown rendering for headers, lists, code blocks, etc.

## Technical Implementation Notes for Stitch
*   **Routing / State:** Needs a router that maps paths to the currently open file (e.g., `?file=10_University/T.O.C (10_University).md`).
*   **Regex Parsing for Links:** Use a regex like `/\[\[(.*?)\]\]/g` to find Obsidian Wiki-links and convert them into standard HTML `<a onClick={navigateToFile(...)}}>` tags.
    *   Handle aliases like `[[TargetFile|Alias]]`.
*   **Orphan Control:** Hide any files from the UI traverse tree that aren't linked in a T.O.C (optional, if you want to strictly enforce the graph rules).
