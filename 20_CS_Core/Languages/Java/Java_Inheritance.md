---
tags:
- field/cs
- subject/programming/java
- concept/java/inheritance
---

[[T.O.C (Java)|Up to Java]]

> **Prompt:** "Write a detailed explanation of Inheritance in classes in java along with diverse code examples with proper syntax explanations of each case like what happens with certain access specifiers and what encapsulation takes place when composing. When is a constructor called when an object is created. When is the constructor of inherited class called"
> **Lens Applied:** The Chief Engineer / The Constructivist

# Technical breakdown: Inheritance ("Is-A")

## 1. Surgical Definition (Internals)
Inheritance is a mechanism where a child class acquires the memory layout and behavior (v-table) of a parent class.
In the JVM:
*   **Memory:** When `Child` is instantiated, the heap allocation MUST include space for all of `Parent`'s fields, even private ones (though they are inaccessible).
*   **Initialization:** Java enforces **Constructor Chaining**. The first line of *every* constructor is implicitly `super()`, unless specified otherwise. The `Object` class constructor is always the first code to actually execute.

## 2. The Laboratory (Proof of Concept)

### Experiment: The Constructor Chain Reaction

```java
// The Ancestor
class Entity {
    private int id; // Private: Not visible to Player, but exists in memory.
    
    public Entity() {
        // Implicit super() call to Object() happens here.
        System.out.println("[1] Entity Constructor: Base scaffolding built.");
        this.id = 0;
    }
    
    public Entity(int id) {
        System.out.println("[1*] Entity Arg-Constructor.");
        this.id = id;
    }
}

// The Child
class Player extends Entity {
    protected int health;

    public Player() {
        // Implicit 'super()' is inserted here by Compiler.
        System.out.println("[2] Player Constructor: Adding stats.");
        this.health = 100;
    }
    
    public Player(int id, int health) {
        // Explicit Super Call. MUST be the first statement.
        super(id); 
        System.out.println("[2*] Player Arg-Constructor.");
        this.health = health;
    }
}

// Execution Trace
class GameEngine {
    public static void main(String[] args) {
        System.out.println(">>> Spawning Player 1...");
        Player p1 = new Player();
        // Trace:
        // [1] Entity Constructor
        // [2] Player Constructor
        
        System.out.println(">>> Spawning Player 2...");
        Player p2 = new Player(101, 50);
        // Trace:
        // [1*] Entity Arg-Constructor
        // [2*] Player Arg-Constructor
    }
}
```

## 3. Memory & System Context
*   **The Object Header:** Every object in Java has a header. For `Player`, the memory layout looks like: `[Header] + [Entity.id] + [Player.health]`.
*   **V-Table (Virtual Method Table):** For dynamic dispatch (Overriding). The JVM creates a table of function pointers for `Player`. If `Player` overrides `move()`, the slot for `move` points to `Player.move`. If it doesn't, it points to `Entity.move`.
*   **Access Specifiers in Inheritance:**
    *   `public`: Inherited and accessible everywhere.
    *   `protected`: Inherited. Accessible in Child and Child's package. Critical for "Template Method" patterns.
    *   `default`: Inherited ONLY if Child is in the same package.
    *   `private`: **NOT Inherited** (Conceptually). The Child cannot see or touch it. However, the data *is* there in memory, managed by the Parent's public/protected methods.

## 4. Best Practices
*   **Liskov Substitution Principle (LSP):** `Player` should be swappable anywhere an `Entity` is expected.
*   **Prefer Composition:** Inheritance creates tight coupling. If you change `Entity`, you break `Player`. Only use Inheritance for true "Is-A" hierarchies (e.g., `Cat` is an `Animal`), not for code reuse (e.g., `Window` is a `Rectangle` -> Bad idea).
