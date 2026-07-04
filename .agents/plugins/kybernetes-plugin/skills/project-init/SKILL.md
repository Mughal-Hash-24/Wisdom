---
name: project-init
description: Scaffolds a new project documentation note in the vault's 40_Projects folder and links it. Syncs with Memory.
---

# Project Init Workflow

Scaffold a new project documentation note and register it in Memory.

## Step 1: Vault Setup

- Call `init_project` (wisdom-os) to create `40_Projects/Active/{name}/{name}.md`.
- Call `ensure_toc_link` (wisdom-os) to link to `T.O.C (40_Projects).md` or `T.O.C (Active).md`.

Note content:
```markdown
# Project: {name}
[[T.O.C (Active)|Up to Active Projects]]

**Status:** #project/active
**Created:** {date}

## Architecture
[Describe the project here]

## Log
- {date}: Project initialized.
```

Call `add_frontmatter` (wisdom-os) with tags: `["#field/cs", "#type/project"]`.

## Step 2: Memory Sync

- Call `create_entities` (memory MCP) with entity: `{name}` (Type: Project, Status: Active).
- Call `create_relations` (memory MCP) linking the project to relevant subjects if mentioned by the user.

## Step 3: Report

Output: "Project {name} vault note initialized at `40_Projects/Active/{name}/`. Memory entity created."
