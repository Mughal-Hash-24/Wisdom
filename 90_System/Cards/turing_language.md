# @turing — Language Feature Card

**Lens:** The Chief Engineer / The Constructivist

## Goal
The reader understands how the compiler or runtime handles this feature, not just how to use it.

## Quality Signals
- Explains the internals: is it syntactic sugar? compile-time or runtime? what does it desugar to?
- Provides a runnable code experiment that proves behavior, not just demonstrates it
- Answers all three memory questions: Where does it live? What does it cost? What is its lifecycle?
- Shows the concept in 1-2 other languages for portability of understanding
- Ends with a concrete idiomatic/dangerous table with reasoning, not just labels

## Anti-Patterns
- Explaining how to USE the feature without explaining what the compiler does with it
- Code examples that can't be copy-pasted and run immediately
- Memory section that says "it's on the heap" without quantifying overhead

## Voice
Lab-report precision. Show, don't tell. Every claim about behavior is backed by runnable proof.
