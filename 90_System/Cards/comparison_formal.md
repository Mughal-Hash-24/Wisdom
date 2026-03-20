# Formal Comparison

## Goal
Compare two or more concepts, tools, or approaches within Computer Science or Mathematics, delivering a clear verdict on when to use each.

## Quality Signals
- Side-by-side analysis with concrete dimensions (performance, complexity, use cases, trade-offs)
- Each option's strengths AND weaknesses stated explicitly -- no false balance
- A clear recommendation or decision framework at the end
- Code examples or mathematical formulations where they clarify the comparison
- Real-world scenarios that illustrate when each option wins

## Anti-Patterns
- DO NOT present a balanced "both are good" conclusion -- commit to a recommendation with conditions
- DO NOT compare on superficial features only -- dig into internals and edge cases
- DO NOT use vague qualifiers ("slightly faster", "somewhat better") without data or reasoning
- DO NOT turn the comparison into two independent summaries placed next to each other

## Gold Standard
"TCP guarantees delivery. UDP doesn't. That's the textbook answer, and it's correct, and it tells you almost nothing about when to use which. Here's what actually matters: TCP pays for its guarantees with a three-way handshake, congestion control, and retransmission overhead. For a database query, that cost is invisible. For a video call streaming 30 frames per second, it's catastrophic -- by the time TCP retransmits a dropped packet, the frame it belonged to is three frames stale. UDP lets you drop that packet and move on. The real question isn't reliability vs speed. It's: can your application tolerate loss?"
