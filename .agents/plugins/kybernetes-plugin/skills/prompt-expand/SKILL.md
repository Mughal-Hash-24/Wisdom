---
name: prompt-expand
description: Expands a {{...}} prompt block using the appropriate expansion template (A-I). Selects the template based on content analysis, loads it, and generates the full expansion.
---

# Prompt Expansion Workflow

Expand a single `{{...}}` prompt into a full knowledge note using the appropriate template.

## Step 1: Analyze the Prompt

Read the `{{...}}` text and any surrounding context in the note. Classify using:

| Prompt Content | Template |
| :--- | :--- |
| Programming language feature/syntax | C (Rosetta Stone) |
| Algorithm or Data Structure | E (Algorithmist) |
| Comparing two items | B (Arena) |
| History, Finance, General events | D (Chronograph) |
| Error log or debugging | F (Debugger) |
| System design / architecture | G (Blueprint) |
| Math, proofs, formal logic | H (Mathematician) |
| Real-world product/company case | I (Case Study) |
| General CS concept (default) | A (Deep Dive) |

## Step 2: Load the Template

Call `load_template` (wisdom-os) with the selected letter (A-I).

## Step 3: Generate the Expansion

Follow the template structure **section by section**:

- Start with the Seed block: `> **Seed:** "{original prompt text}"`
- Fill each section as instructed by the template.
- Use **real-world analogies** to anchor abstract concepts (not C++ anchors).
- Read any text surrounding the `{{...}}` block in the original note as **context** -- it reveals the user's intent, knowledge level, and the subject area.

### Depth Rule

Scale with the topic's complexity. No fixed word count:
- Simple concepts: keep lean (~200-300 words)
- Deep or multi-faceted topics: go as deep as needed (800+ words)
- Cover every template section fully. Do NOT truncate.

## Step 4: Write the Output

- If called from inbox-sort: write to the file path specified by the caller.
- If called standalone: write to `00_Inbox/Expansion_{sanitized_topic}.md`.
- Call `add_frontmatter` (wisdom-os) with `["#type/expansion"]` plus any relevant field/subject/concept tags.

## Constraints

- **Seed Rule:** Always include the original prompt text verbatim in the output.
- **No Preamble:** Start directly with content. No "Let's explore..." or "In this note..."
- **Context Awareness:** Text outside `{{...}}` is user data -- preserve it, but USE it as context for the expansion.
