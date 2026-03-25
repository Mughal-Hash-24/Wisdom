# How to use this prompt
Copy the text inside the bounds below and paste it directly into your AI UI generator (e.g., Stitch, v0, Lovable) to generate the exact UI we discussed.

---

**Copy from here:**

Build a highly interactive, 3-pane desktop layout for a "Vault Explorer" web application designed to navigate a local Markdown knowledge base. 

# 1. Design System & Aesthetics
The application must follow a sleek, futuristic "System Kernel" aesthetic.
- **Backgrounds:** Deep Obsidian (`#0A0A0C`), Carbon darks (`#15151A`) with subtle border lines (`#2A2A35`) separating the panes.
- **Typography:** Use a clean, modern sans-serif like `Inter` for UI elements, and a monospaced font like `Fira Code` or `JetBrains Mono` for tags and code blocks.
- **Accent Colors (Crucial for tags and links):**
  - Neon Blue (`#00D4FF`)
  - Vivid Orange (`#FF7B00`)
  - Emerald Green (`#00FF7F`)
  - Deep Purple (`#9D4EDD`)

# 2. Layout Specifications (3-Pane Full Height)

### Pane 1: Left Sidebar (Directory Tree)
- Width: Fixed `250px` or `300px` (or resizable).
- A multi-level nested file tree representing folders.
- Create mock folders: `10_University > Semester_01 > Artificial Intelligence`, and `20_CS_Core > Theory`.
- Use minimal chevron icons for expanding/collapsing.
- The active selected folder should have a subtle glowing border/background.

### Pane 2: Middle Pane (The T.O.C Hub)
- Width: Flex `1` (takes up remaining space) or a fixed wider pane like `400px`.
- This pane acts as the local "Table of Contents" dashboard for the selected folder.
- **Header:** "T.O.C (Artificial Intelligence Notes)"
- **Content:** Implement a mock interactive data grid (table). 
  - Columns: `ID` (e.g., 1.1.1), `Category` (e.g., Search Algorithms), `Content` (e.g., A Star Algorithm).
  - The `Content` cell text should act as clickable hyperlinks styled with the Neon Blue accent color.
- Add a subtle hover effect (opacity change or background bump) on the table rows.

### Pane 3: Right Pane (The Markdown Viewer)
- Width: Flex `2` (the largest pane).
- This pane renders the selected Markdown note.
- **Top Bar:** 
  - A prominent "⬅ Up to T.O.C" back button floating at the top left.
  - YAML Frontmatter tags displayed as beautiful pill-badges in the top right. Create mock badges: one reading `field/cs` (Neon Blue background with dark text) and `concept/search` (Carbon background with white text).
- **Body Content:**
  - Render a beautifully styled mock Markdown document.
  - Include an `<h1>` (e.g., "1.1.1 - A* Algorithm").
  - Include an `<h2>`.
  - Include paragraph text that occasionally contains inline wiki-links like `[[Search Heuristics]]`. Style these wiki-links so they stand out as clickable elements.
  - Include a styled code block.

# 3. Interactivity & State
- The Sidebar should have an active state highlighting the selected folder.
- Hover states are critical: buttons, links, tree nodes, and grid rows should visually react when hovered.
- Give the overall application a polished, "production-ready" dark mode feel. Do not use generic, flat Tailwind defaults; customize the hues heavily towards the #0A0A0C obsidian look.
