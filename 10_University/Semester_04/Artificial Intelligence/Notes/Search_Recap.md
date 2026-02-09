[[T.O.C (Artificial Intelligence)|Up to Artificial Intelligence]]

> **Prompt:** "Create a detailed explanation on search problem, search tree, search algorithms with immense details in each and a real world example to go along"
> **Lens Applied:** The Chief Engineer / First Principles

# Deep Dive: Foundations of AI Search

## 1. Ontological Definition
A **Search Problem** is a formalization of a goal-oriented task. It consists of:
- **State Space:** The set of all possible configurations.
- **Initial State:** Where the agent starts.
- **Actions:** The set of available moves $A(s)$.
- **Transition Model:** Result $(s, a) ightarrow s'$.
- **Goal Test:** A boolean function determining if a state is the target.
- **Path Cost:** A function that assigns a numeric cost to a sequence of actions.

## 2. The Internal Mechanics (Under the Hood)
### The Search Tree
A **Search Tree** is a conceptual structure representing possible paths through the state space.
- **Nodes:** Represent paths to states (not the states themselves). A node contains: `state`, `parent`, `action`, `path_cost`.
- **Expansion:** Generating children of a node by applying all valid actions.
- **Frontier:** The set of all leaf nodes available for expansion.

### Search Algorithm Framework
```python
def general_search(problem, frontier):
    frontier.append(Node(problem.initial_state))
    while not frontier.empty():
        node = frontier.pop() # Strategy defines which node to pop
        if problem.goal_test(node.state):
            return node
        for child in expand(problem, node):
            frontier.append(child)
    return failure
```

## 3. Systems Context & C++ Anchor
In C++, the difference between BFS, DFS, and UCS is purely the data structure used for the `frontier`:
- **BFS (Breadth-First):** `std::queue` (FIFO).
- **DFS (Depth-First):** `std::stack` (LIFO).
- **UCS (Uniform Cost):** `std::priority_queue` (Ordered by $g(n)$).

**Memory Context:** 
- DFS is space-efficient ($O(bm)$) because it only stores the current path.
- BFS is time-optimal for uniform costs but memory-intensive ($O(b^d)$) because it must store all nodes at the current depth.

## 4. Real-World Example: Route Finding (Google Maps)
**State:** GPS Coordinates (Lat/Long).
**Initial State:** Your current location.
**Actions:** Driving to an adjacent intersection.
**Transition:** New intersection coordinates.
**Goal Test:** Coordinates match the destination.
**Path Cost:** Distance or Time.

**Execution:**
The algorithm builds a search tree starting from your house. It expands nodes (intersections). A "blind" search like BFS would explore every street in every direction equally. An "informed" search (A*) uses a heuristic (straight-line distance to destination) to prioritize intersections that lead towards the goal.

## 5. Edge Cases & Constraints
- **Cycles:** In graphs, search trees can be infinite. A `reached` set (Closed List) is mandatory to prevent redundant work.
- **State Space Explosion:** In games like Chess, the state space ($10^{40}$) is too large for a complete search tree; we must use depth-limited search and evaluation functions.
