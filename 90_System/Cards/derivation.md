# Derivation

## Goal
Walk through a mathematical physics derivation so the reader understands every step's physical motivation, not just its algebraic correctness.

## Quality Signals
- Physical setup described before any math begins
- Assumptions stated explicitly and justified physically
- Each major step accompanied by what it MEANS physically, not just what it does algebraically
- Final result interpreted: what does this equation tell us about nature?
- Limiting cases checked: does the result reduce to known answers in simple limits?

## Anti-Patterns
- DO NOT present a wall of algebra without physical commentary between steps
- DO NOT skip steps and say "it follows that" -- show the work or explain the shortcut
- DO NOT forget to check limiting cases (it's the most powerful sanity check in physics)
- DO NOT end with the equation -- end with its interpretation

## Gold Standard
"Start with a vibrating string. Fix both ends, apply tension T, give it mass per length mu. A small segment dx feels the net vertical force from the tension on either side. The curvature determines the restoring force. Newton's second law on that segment gives us: T * (d2y/dx2) = mu * (d2y/dt2). Rearrange: d2y/dt2 = (T/mu) * d2y/dx2. That ratio T/mu has units of velocity squared. Call it v2. You've just derived the wave equation, and the speed of the wave is sqrt(T/mu). Heavier string, slower wave. Tighter string, faster wave. Every guitarist already knows this. Now they know why."
