---
tags:
  - "#field/cs"
  - "#subject/algorithms"
  - "#concept/search/heuristic"
---
[[T.O.C (Algorithms)|Up to Algorithms]]

> **Prompt:** "What happens in A* when the heuristic cost exceeds the actual cost of the path towards the goal? Explain in detail."
> **Lens Applied:** The Chief Engineer / First Principles

# Deep Dive: Non-Admissible Heuristics in A* Search

## 1. Ontological Definition
In the context of A* search, a heuristic $h(n)$ is **admissible** if it never overestimates the cost to reach the goal (i.e., $h(n) \le h^*(n)$, where $h^*(n)$ is the true optimal cost). When a heuristic exceeds this actual cost, it is classified as **non-admissible**. The immediate formal consequence is the loss of the **Optimality Guarantee**: A* is no longer guaranteed to find the lowest-cost path.

## 2. The Internal Mechanics (Under the Hood)
A* selects nodes based on the evaluation function $f(n) = g(n) + h(n)$, where $g(n)$ is the cost from the start to node $n$.

### The Pruning Mechanism
When $h(n) > h^*(n)$, the algorithm "over-penalizes" potentially optimal paths. 
*   **State Conflict:** Suppose the optimal path goes through node $A$, but $h(A)$ is significantly overestimated. 
*   **Premature Termination:** A* may find a sub-optimal path through node $B$ where $f(B) = g(B) + h(B)$ is smaller than the inflated $f(A)$, even if the actual cost $g(B) + h^*(B) > g(A) + h^*(A)$.
*   **Math Representation:** If $f(goal)$ on a sub-optimal path is reached such that $f(suboptimal\_goal) < g(optimal\_node) + h(optimal\_node)$, the algorithm terminates and returns the sub-optimal solution.

### Efficiency vs. Accuracy
Non-admissible heuristics often act similarly to **Greedy Best-First Search**. By overestimating costs, the search "pushes" the frontier more aggressively toward what it *thinks* is the goal, often expanding far fewer nodes. This is the core trade-off: **Speed for Optimality**.

## 3. Systems Context & Anchoring (Analogy/C++)
Think of A* as a **C++ `std::priority_queue`** managing a set of path exploration tasks. If the priority (the $f(n)$ value) is calculated using an inflated $h(n)$, the true "shortest" task is pushed deep into the heap, buried under sub-optimal tasks that appear "cheaper" only because their heuristics were more modest or accurate. 

**Analogy:** Imagine a GPS that wrongly believes a highway has a massive 50-mile detour due to construction ($h(n)$ too high). It will redirect you through narrow side streets (the sub-optimal path) because the highway "looks" slower, even if the construction was actually cleared and the highway remains the fastest route.

## 4. Edge Cases & Constraints
*   **Bounded Sub-optimality:** If the heuristic is over-optimistic by a factor of $\epsilon$ (i.e., $h(n) \le (1+\epsilon)h^*(n)$), the resulting path cost is guaranteed to be no worse than $(1+\epsilon)$ times the optimal cost. This is the basis for **Weighted A***.
*   **Completeness:** As long as $h(n)$ is finite and edge costs are positive, A* remains **complete** (it will find *a* goal if one exists), even if the heuristic is non-admissible.
*   **Constraint failure:** If $h(n)$ is infinite for a reachable goal, the algorithm may fail to find a path, treating the node as a dead-end.