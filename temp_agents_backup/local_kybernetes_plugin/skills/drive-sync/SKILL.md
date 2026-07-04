---
name: drive-sync
description: Re-indexes the Obsidian Vault directories into the Memory graph. Detects new, removed, and changed project, subject, and resource folders.
---

# Vault Sync Workflow

Reconcile the Obsidian Vault folders with the Memory knowledge graph.

## Step 1: Scan Vault Directories

Call `list_directory` (filesystem) on the vault folders:

| Directory | Entity Type |
| :--- | :--- |
| `40_Projects` | Project |
| `10_University` | Subject / Category |
| `20_CS_Core` | Learning Track |

Record the folder/note names in each directory.

## Step 2: Reconcile with Memory

- Call `search_nodes` (memory MCP) for existing entities of the corresponding types.
- Compare the vault directory listing with memory entities:

| Condition | Action |
| :--- | :--- |
| Folder/Note in vault, NOT in memory | Call `create_entities` to add it |
| Entity in memory, NOT in vault | Call `create_relations` to mark as "Archived" |
| Both match | No action |

## Step 3: Report

Output a diff table:

```
| Folder/Note | Status | Action Taken |
| :--- | :--- | :--- |
| 40_Projects/NewProject | NEW | Entity created |
| 40_Projects/OldProject | DELETED | Marked as Archived |
| 20_CS_Core/Languages/Rust | UNCHANGED | -- |
```
