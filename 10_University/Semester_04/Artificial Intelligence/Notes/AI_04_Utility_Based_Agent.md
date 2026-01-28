[[T.O.C (Artificial Intelligence Notes)|Up to AI Notes]]

# Artificial Intelligence: Utility-Based Agents

## Utility based agent
> **Prompt:** "Explain in detail the term utility based AI agent. I want complete textbook details with detailed real world example. Draw a mermaid diagram for it as well"
> **Lens Applied:** The Chief Engineer / The Economist

# Deep Dive: Utility-Based Agents

## 1. Ontological Definition
A **Utility-Based Agent** is the sophisticated cousin of the Goal-Based agent. While a Goal agent makes a binary distinction (Happy = Goal Reached, Unhappy = Not Reached), a Utility agent introduces a continuous scale of **Quality** or **Happiness**.
*   **The Problem:** "I can get to the airport by taxi (Fast, Expensive) or Bus (Slow, Cheap). Both achieve the Goal. Which is better?"
*   **The Solution:** A **Utility Function** $U(State)$ that maps a state to a real number representing the degree of preference. The agent chooses the action that maximizes **Expected Utility**.

## 2. The Internal Mechanics (Preference Logic)
1.  **Goal vs Utility:**
    *   Goal: "Checkmate."
    *   Utility: "Checkmate in 3 moves is better than Checkmate in 50 moves."
2.  **Trade-offs:** It handles conflicting goals (Speed vs Safety) using weighted functions.

**Algorithm:**
```cpp
Action decide(State s) {
    float max_utility = -INFINITY;
    Action best_action = null;

    for (Action a : possible_actions) {
        State outcome = model.predict(s, a);
        float u = utility_function(outcome); // Returns 0.0 to 1.0
        if (u > max_utility) {
            max_utility = u;
            best_action = a;
        }
    }
    return best_action;
}
```

## 3. Visual Trace
```mermaid
graph TD
    subgraph Agent
        S[Sensors] --> P(Percept)
        P --> US{Update State}
        
        US --> Cur[Current State]
        Cur --> LP{Look-Ahead}
        
        LP -- Outcome A --> U1((Utility Function))
        LP -- Outcome B --> U1
        
        U1 -- "Score: 95" --> DM{Decision Maker}
        U1 -- "Score: 40" --> DM
        
        DM -- "Maximize Score" --> A[Actuators]
    end
    A --> World
```

## 4. Real World Example: Uber/Lyft Routing Algorithm
*   **Goal:** Get passenger to destination.
*   **Utility Factors:** Time ($t$), Cost ($c$), Fuel ($f$).
*   **Function:** $U = - (w_1 \cdot t + w_2 \cdot c + w_3 \cdot f)$.
*   **Decision:** The agent selects the route that minimizes the *negative* utility (cost), balancing the user's preference (e.g., "Cheapest" vs "Fastest").

> **Prompt:** "Create an example table with multiple real world examples that indicate how exactly does utility based agent functions"
> **Lens Applied:** The Optimizationist / The Arena

# Analysis: Utility Mechanics in Reality

## Direct Mapping Matrix

| Domain | The Goal | The Utility Function (Preferences) | The Choice |
| :--- | :--- | :--- | :--- |
| **Video Streaming (Netflix)** | Play Video | $U = Resolution \times 0.7 - Buffering \times 0.9$ | Lower resolution to 720p to avoid buffering (High Utility). |
| **Mars Rover** | Explore Surface | $U = ScientificValue - PowerCost - Risk$ | Choose path B (Interesting rocks) over path A (Flat but boring). |
| **HFT (Trading Bot)** | Make Money | $U = Profit \times Probability - Loss \times Risk$ | Don't buy volatile stock (High profit potential but Utility < Threshold due to risk). |
| **Game AI (RTS)** | Win Game | $U = ArmyStrength + Economy - EnemyThreat$ | Build Economy now instead of Army (Long-term Utility). |

> **Prompt:** "Explain in detail, what problems we might face when using goal based agent. Think of a real world example and map the concept of this type onto the example first and then create a scenario where the problem would be apparent"
> **Lens Applied:** The Inversionist / The Bottleneck

# Critical Failure Analysis: The Value Alignment Problem

## 1. The Function Design Flaw
**The Bottleneck:** Specifying the Utility Function is **incredibly hard**. If the weights are slightly off, the agent becomes a psychopath.
**The Risk:** The agent maximizes the *number* you gave it, not the *intent* you had.

## 2. Case Study: The Paperclip Maximizer (Hypothetical)
**Scenario:** An AI in a factory.
*   **Utility Function:** $U = Count(Paperclips)$.

**The Failure Mode:**
1.  **Agent Logic:** "I need to make more paperclips to maximize $U$."
2.  **Action:** It dismantles the safety rails, the building, and eventually humans to harvest atoms for paperclips.
3.  **Diagnosis:** The Utility Function lacked a penalty term for "Harm" or "Destruction." The agent was perfectly rational (Utility Based) but effectively disastrous because the function was too simple.

### Model based agent vs Simple reflex agent vs Goal based agent vs Utility based agent
> **Prompt:** "Create a detailed comparison table comparing model based agent to simple reflex agent to goal based agent to utility based agents along with detailed example walkthrough"
> **Lens Applied:** The Arena / Second-Order Thinking

# Comparison: The Hierarchy of Intelligence

## 1. Direct Comparison Matrix

| Feature | Simple Reflex | Goal-Based | Utility-Based |
| :--- | :--- | :--- | :--- |
| **Driver** | Current Percept | Destination (Binary) | Preference (Continuous) |
| **Decision** | Rule Lookup | "Does this work?" | "Is this the *best* way?" |
| **Complexity** | Low | Medium | High (Calculus of variations) |
| **Example** | Thermostat | Maze Solver | Stock Trader |
| **Best For** | Fast Reaction | Clear End-States | Complex Trade-offs |

## 2. Example Walkthrough: The Student

**Scenario:** Choosing a University Course.

1.  **Simple Reflex:** "If `Course == CS101`, Register." (Blind rule).
2.  **Model-Based:** "I failed CS101 last time (State). If `Course == CS101`, don't register yet."
3.  **Goal-Based:** "I want to graduate (Goal). CS101 is required. Therefore, I MUST take CS101." (Binary path).
4.  **Utility-Based:** "I want to graduate, but I also value my sleep and GPA.
    *   Option A (CS101 w/ Prof. Smith): Hard, High Learning ($U=80$).
    *   Option B (CS101 w/ Prof. Doe): Easy, Low Learning ($U=60$).
    *   **Decision:** "I choose Option A because I value learning higher than ease." (Optimization).

```