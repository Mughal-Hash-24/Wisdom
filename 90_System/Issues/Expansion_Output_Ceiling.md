# Issue: Single-Prompt Expansion Output Ceiling

**Filed:** 2026-03-17
**Status:** Open
**Severity:** High (Quality Bottleneck)
**Component:** Expansion Pipeline (`inbox-sort` → Domain Agents → `@surgeon`)

---

## Problem Statement

When a single `{{...}}` prompt requests broad coverage of a large topic (e.g., "Explain all OOP design patterns with Java examples and use cases"), the domain agent's output is capped at approximately **800-1000 words** per invocation.

This ceiling means that a topic requiring 4000+ words of proper treatment gets compressed into ~1000, yielding shallow, incomplete coverage (e.g., only 2-3 design patterns instead of all 23 GoF patterns).

## Reproduction

```markdown
{{Explain to me in detail the industry standards and the specs of all the
design patterns and example codes in java plus example use cases}}
```

**Expected:** Comprehensive coverage of all major patterns (~4000+ words).
**Actual:** ~800-1000 words, covering 2-3 patterns before truncation.

## Contrast (Manual Workaround)

When the same topic is split into 5 separate prompts manually:

```markdown
{{Explain the Singleton, Factory Method, and Abstract Factory patterns in Java with code and use cases}}

{{Explain the Builder, Prototype, and Adapter patterns in Java with code and use cases}}

{{Explain the Observer, Strategy, and Command patterns in Java with code and use cases}}

... (etc.)
```

Each prompt yields ~800 words independently, producing **~4000 words total** with much greater depth on each pattern.

## Root Cause Analysis

The issue is **not** a system bug but an **architectural limitation** of the current expansion model:

1. **1 Prompt = 1 Agent Call = 1 Output Window.** The pipeline maps each `{{...}}` block to exactly one domain agent invocation. There is no mechanism to split a broad prompt into multiple agent calls.

2. **LLM output ceiling.** Each agent call (Gemini model invocation) has a practical output ceiling. Even though the system prompt says "DO NOT abbreviate or truncate," the model physically cannot produce 4000 words in a single generation pass. It hits ~800-1000 and wraps up.

3. **User burden for decomposition.** Currently, the user must manually decompose broad topics into focused sub-prompts to bypass this ceiling -- the system does not assist.

## Impact

- **Knowledge gaps:** Broad "survey" notes (design patterns, sorting algorithms, protocol families) are systematically under-covered.
- **User friction:** Manual decomposition requires the user to already know the sub-topics, defeating the purpose of asking for a comprehensive overview.
- **Quality inconsistency:** Focused prompts produce excellent output; broad prompts produce mediocre output. The system's quality becomes unpredictable.
