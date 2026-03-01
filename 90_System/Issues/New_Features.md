# Kybernetes v2 -- Feature Backlog

> Ideas for new skills, commands, agents, and tools. Prioritized by impact.

---

## New Skills

### `exam-prep`
**Trigger:** `/os:prep {subject}`
**Purpose:** Generate a study session for an upcoming exam.
- Read `00_Deadlines_Master.md` to find the exam date.
- Scan all notes in the subject folder, identify weak spots (notes with few expansions or missing sections).
- Generate a prioritized study plan with estimated time per topic.
- Create flashcard-style Q&A pairs from each note's key concepts.
- Output a `60_Planner/Exam_Prep_{Subject}_{Date}.md` file.

### `concept-link`
**Trigger:** `/os:link`
**Purpose:** Discover and create cross-references between related notes across different folders.
- Scan all notes for shared concepts (e.g., "heuristic" appears in both AI Search and Optimization Theory).
- Suggest horizontal `[[wikilinks]]` between related notes.
- Show a table of proposed links for approval before writing.
- Strengthens the graph without polluting T.O.C structure.

### `weekly-review`
**Trigger:** `/os:review`
**Purpose:** Generate the weekly reflection note.
- Read all daily notes from the past 7 days.
- Aggregate completed tasks, brain dump highlights, and EOD reflections.
- Calculate completion rate (tasks done / tasks planned).
- Identify recurring blockers from reflections.
- Output `60_Planner/Weekly/{YYYY}-W{NN}.md`.

### `note-audit`
**Trigger:** `/os:audit`
**Purpose:** Health check on vault quality.
- Scan for orphan notes (not linked to any T.O.C).
- Find notes missing frontmatter tags.
- Detect empty notes or stubs (< 50 words).
- Find broken wikilinks (references to notes that don't exist).
- Output a report with fix suggestions.

### `semester-init`
**Trigger:** `/os:semester {number}`
**Purpose:** Scaffold a new semester folder with all subjects and T.O.C files.
- Create `10_University/Semester_{N}/` with Admin, Timetable, Deadlines.
- For each subject: create the full subfolder tree (Assignments, Exams, Lectures, Notes, Quizzes, Resources) with T.O.C files.
- Generate the structured table T.O.C template for Notes.
- Link everything to parent T.O.C.

---

## New Commands

### `/os:focus {topic}`
Route to a hypothetical `deep-focus` skill. Sets the "Current Focus" in memory, creates a brain dump file, and surfaces all related notes.

### `/os:export {folder}`
Export a folder of notes to a clean PDF or HTML bundle for sharing (e.g., sharing AI notes with classmates).

### `/os:digest`
Summarize unread items across all inboxes (physical, email, vault inbox) into a single briefing note.

### `/dev:log {project}`
Append a timestamped dev log entry to the project's vault note. Reads recent git commits if available.

---

## New Agents

### @reviewer
**Purpose:** Code review agent scoped to `D:\PROJECTS`.
- Reads a project's source files and identifies issues (style, bugs, complexity).
- Uses `filesystem` tools only.
- Reports findings without modifying code.

### @tutor
**Purpose:** Socratic questioning agent for active recall.
- Reads a note and generates questions to test understanding.
- Uses `wisdom-os__read_note` only.
- Outputs questions + hidden answers (collapsible sections in Obsidian).

### @archivist
**Purpose:** End-of-semester archival agent.
- Moves completed semester folders to `90_System/Archive/`.
- Graduates portable concepts to `20_CS_Core/`.
- Updates all T.O.C files and memory entities.
- Generates a semester summary report.

---

## New wisdom-os Tools

### `find_orphans`
Scan the vault for `.md` files not linked from any T.O.C. Return a list of orphan paths.

### `rename_note`
Safely rename a note: update the filename, update all wikilinks across the vault that reference it, and update the parent T.O.C entry.

### `get_note_stats`
Return metadata for a note: word count, tag count, link count, last modified date, parent T.O.C path.

### `bulk_tag`
Apply tags to all notes in a folder that match a pattern. Useful for batch-tagging after a semester.

---

## Integration Ideas

### Google Calendar <-> Deadlines Sync
- `calendar.listEvents` feeds into `00_Deadlines_Master.md` automatically during `/os:boot`.
- If a new assignment is added to Calendar, it appears in Deadlines next boot.

### GitHub Issues <-> Projects
- `/dev:sync {project}` pulls open issues from GitHub and appends them to the project's vault note as tasks.

### NotebookLM Integration
- Export a folder of notes to NotebookLM for AI-powered study sessions and podcast generation.
