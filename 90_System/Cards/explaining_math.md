# Explaining Math

## Goal
Make a mathematical concept intuitively understood before formalizing it, so the reader grasps WHY a definition or theorem exists, not just what it says.

## Quality Signals
- Opens with the intuition or motivation BEFORE the formal definition
- Formal definition is precise and complete when presented
- At least one fully worked numerical or symbolic example
- Boundary conditions identified: where does this break, what assumptions are required?
- Connects to adjacent concepts the reader likely already knows

## Anti-Patterns
- DO NOT start with the formal definition and then try to explain it afterward -- intuition first
- DO NOT present a formula without explaining what each symbol means concretely
- DO NOT skip the worked example -- abstraction without computation is incomplete
- DO NOT present the concept in isolation -- show where it fits in the broader structure

## Gold Standard
"An eigenvector is a direction that a transformation doesn't change. Stretch it, compress it, flip it -- fine. But it stays on the same line. Think of a 2D rotation: almost everything moves. But if you rotate around the z-axis, the z-axis itself doesn't go anywhere. That's an eigenvector. The eigenvalue tells you how much it stretches along that direction. A value of 1 means nothing changes. A value of -1 means it flips. A value of 0 means it collapses. The entire machinery of diagonalization, spectral decomposition, and principal component analysis follows from this one question: which directions survive the transformation?"
