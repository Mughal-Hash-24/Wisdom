# Process

## Goal
Walk through a biological, chemical, or physical process step by step, making each stage's inputs, outputs, and regulatory logic clear.

## Quality Signals
- Each step clearly states: what goes in, what comes out, what catalyzes or regulates it
- The sequence is explicit: step 1 produces X, which feeds into step 2
- Regulatory mechanisms (feedback loops, inhibitors, activators) are identified
- The overall purpose of the process is stated upfront
- Scale and location specified: where does this happen (organelle, tissue, environment)?

## Anti-Patterns
- DO NOT list steps without showing how each feeds into the next
- DO NOT ignore regulation -- most processes have feedback loops that are the interesting part
- DO NOT describe the process in isolation -- connect it to the larger system
- DO NOT use "then X happens" without explaining the mechanism that makes X happen

## Gold Standard
"Glycolysis starts with a glucose molecule and ends with two pyruvates, two ATPs, and two NADHs. But the interesting part isn't the output -- it's the investment. The cell spends two ATPs in the first half (to phosphorylate glucose and destabilize it), then earns four ATPs in the second half. Net gain: two. The enzyme phosphofructokinase-1 controls the whole thing -- it's the checkpoint. When ATP levels are high, PFK-1 slows down (why break down more sugar if you've got plenty of energy?). When AMP accumulates, PFK-1 accelerates. The cell isn't just running a reaction. It's running a business."
