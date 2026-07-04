---
name: polymath-synthesize
description: Orchestrates the /os:synthesize command. Uses semantic_search to fetch vectors, and dispatches @polymath to write True PKM MOCs.
---

# Polymath Synthesis Workflow

Triggered when the user types the exact slash command `/os:synthesize "Topic Query"`.

## Step 1: Semantic Search
- Call `semantic_search` (from the `wisdom-os` MCP server) with `query="{Topic Query}"` and `k=10`.
- Wait for the results to yield a markdown list of the most semantically relevant chunks across the DB.

## Step 2: Extract Context
- Use `read_note` on the `90_System/Cards/synthesis.md` Principle Card to understand the required MOC format.
- (Optional) Use `read_note` on the top 3 results from step 1 if the agent needs more context than just the titles, but usually, just combining the headers and chunks is sufficient to start the prompt.

## Step 3: Dispatch @polymath
- Call the `@polymath` agent.
- Provide the user's `"{Topic Query}"`.
- Provide the semantic search results (the concepts to be woven together).
- Provide the exact `synthesis.md` card logic regarding structure, isomorphism, and emergent ideas.
- Tell `@polymath` to generate the raw markdown content for the MOC. No conversational text.

## Step 4: Write MOC
- Call `create_note` (from `wisdom-os`) to save the generated MOC.
- The destination must be: `30_Knowledge_Base/00_Atlas/{Topic Query}_MOC.md` (Replace spaces with underscores if needed for the filename).
- Once created, notify the user.
