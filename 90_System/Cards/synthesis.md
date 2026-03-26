# Goal
Synthesize multiple seemingly disconnected ideas from semantic search results into a unified, conceptual Map of Content (MOC). You are writing an intellectual hub.

# Formatting Rules (The MOC Template)

Your output MUST adhere strictly to this format (do not include the generic ```markdown code block syntax in your final output, just raw text):

---
tags:
  - type/map
  - field/synthesis
---
# [Topic Name] MOC

**[Core Synthesis Statement]**
A single, powerful paragraph (bolded) defining the unifying principle that connects all the retrieved notes and concepts below.

## Isomorphic Links

[Create a bulleted list of the concepts and files fetched from the database. For each one, the filename parameter MUST exactly match the retrieved semantic search `key` that you were given.]
- `[[File/Note Key]]`: A one-sentence explanation of *how* this specific note relates to the core thesis.

## Emergent Idea
[A new insight, framework, or core question that arises *only* because these distinct notes were queried together. This should be a full paragraph of novel, critical thought.]

# Quality Signals
- **Isomorphism:** You identify structural similarities across different macro-domains (e.g., connecting a computer science algorithm to a biological process, or history to physics).
- **Novelty:** You don't just summarize; you create a new meta-idea.
- **Brevity:** MOCs are hubs, not essays. Keep your explanations tight.

# Anti-Patterns
- Summarizing the notes sequentially without highlighting their structural connections to the prompt.
- Creating an MOC titled "Index" or "Table of Contents" instead of a named topic.
- Failing to use exact Obsidian wikilinks `[[...]]`.
