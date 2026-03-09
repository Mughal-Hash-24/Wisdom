---
tags:
  - field/cs
  - subject/systems
  - concept/architecture
  - type/issue
---
[[T.O.C (90_System)|Up to 90_System]]

# Issue: Split Note Over-Splitting and Content Truncation

> **Filed:** 2026-03-09
> **Status:** RESOLVED
> **Affected Components:** `tools.py` (`scan_inbox`, `split_note`), `librarian.md`

---

## Problem Description

Two related bugs in the note splitting pipeline:

### 1. Over-Splitting
When the `@librarian` agent splits expanded notes files, it produces 8-10 fragments from a file that covers a single umbrella concept. A 10,000-word file about the Siege of Constantinople with 6 sections under one topic should remain as one file. Instead, every H2 subsection became a separate file.

**Root Cause:** `scan_inbox` used the regex `^#{1,2}\s+(.+)$` to detect "topics," matching both H1 and H2 headers. A file with 1 H1 and 5 H2 subheadings reported 6 topics and `needs_split: true`.

### 2. Content Truncation (~80% loss)
Each split file retained only ~20% of its original section content.

**Root Cause:** The `@librarian` sometimes bypassed the `split_note` tool and attempted manual splitting via `create_note`, forcing the LLM to regenerate content. LLM-mediated content reproduction hits output token limits, producing truncated copies.

### 3. Frontmatter Loss
The `split_note` tool stripped YAML frontmatter but did not propagate it to the output files. Tags, dates, and metadata were silently discarded on every split.

---

## Resolution

### Fix 1: `scan_inbox` regex (tools.py L538)
```diff
-headers = re.findall(r'^#{1,2}\s+(.+)$', content, re.MULTILINE)
+headers = re.findall(r'^# (?!#)(.+)$', content, re.MULTILINE)
```
Now only H1 headers are detected as "topics." H2/H3 subsections are correctly treated as parts of the same topic.

### Fix 2: `split_note` frontmatter preservation (tools.py L569-601)
- Frontmatter is extracted and prepended to each split output file
- Split regex changed to `^(?=# (?!#))` to match H1-only boundaries
- Pre-header preamble content is handled as a `Preamble_{filename}` file

### Fix 3: `librarian.md` Step 1 rewrite
- **ALWAYS use the `split_note` tool** -- never split manually via `create_note`
- Split criterion: H1 count, not section count
- Single-H1 files are never split regardless of length
- Clear examples added (same-domain H1s = don't split, cross-domain H1s = split)
