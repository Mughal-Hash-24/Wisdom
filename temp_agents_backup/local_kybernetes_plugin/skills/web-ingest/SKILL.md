---
name: web-ingest
description: Scrapes a URL using Puppeteer, refactors the content into clean Obsidian markdown, and saves it to the vault's Inbox for later sorting.
---

# Web Ingest Workflow

Convert a web page into a permanent vault note.

## Step 1: Acquire

- Call `puppeteer_navigate` (puppeteer MCP) to load the URL.
- Extract the page content as text/markdown.
- Optionally call `puppeteer_screenshot` for visual reference.

## Step 2: Process

Refactor the raw content:
- **Strip noise:** Navigation menus, ads, footers, cookie banners, sidebars.
- **Extract signal:** Core concepts, arguments, code snippets, key data.
- **Format for Obsidian:**
  - Use `## Headings` for sections.
  - Use fenced code blocks with language tags.
  - Convert inline links to wikilinks where they reference vault topics.

## Step 3: Save

Call `create_note` (wisdom-os) with:
- **Folder:** `00_Inbox`
- **Topic:** `Read - {Short Title}`
- **Content:**
  ```markdown
  # {Title of Article}
  **Source:** {URL}
  **Ingested:** {date}

  ---

  [Cleaned, formatted content]
  ```

Call `add_frontmatter` (wisdom-os) with tags: `["#type/ingested", "#source/web"]`.

## Step 4: Report

Output: "Saved to `00_Inbox/Read - {title}.md`. Summary: {1-sentence summary of the article's key point}."
