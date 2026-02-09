---
tags:
- field/cs
- subject/programming/java
- concept/java/composition
---

[[T.O.C (Java)|Up to Java]]

> **Prompt:** "Write a detailed explanation of composition in classes in java along with diverse code examples with proper syntax explanations of each case like what happens with certain access specifiers and what encapsulation takes place when composing. Is a class within a class composition. When is a constructor called when an object is created. When is the constructor of composed class called"
> **Lens Applied:** The Chief Engineer / The Constructivist

# Technical breakdown: Composition ("Has-A" Strong)

## 1. Surgical Definition (Internals)
Composition is a **Strong "Has-A" Relationship**. Ideally, it implies ownership and lifecycle dependency. If the container (Whole) is destroyed, the component (Part) is also destroyed (or becomes unreachable and GC'd).

In C++, this is often achieved by embedding an object directly in memory. In Java, everything is a reference (Pointer), so Composition is achieved by holding a `private final` reference to an object that is instantiated **inside** the container's constructor.

**Is a class within a class composition?**
No. That is nesting/scoping. Composition is about **Instances**, not Definitions. Composition happens on the **Heap** at runtime. Nesting happens in the **Namespace** at compile time.

## 2. The Laboratory (Proof of Concept)

### Experiment: The Human-Heart Dependency (Strict Composition)

```java
// The Part
class Heart {
    private int bpm;

    public Heart() {
        this.bpm = 60;
        System.out.println(">> Heart Tissue Generated (Heap Alloc)");
    }

    public void beat() { System.out.println("Thump-Thump"); }
}

// The Whole
public class Human {
    // Encapsulation: PRIVATE FINAL
    // 'private': No one outside Human can touch the heart.
    // 'final': The Human cannot swap their heart (immutable link).
    private final Heart heart;

    public Human() {
        System.out.println(">> Human Embryo Forming...");
        // CONSTRUCTOR CALL TIMING:
        // The Part is created INSIDE the Whole's constructor.
        // This enforces lifecycle dependency.
        this.heart = new Heart(); 
        System.out.println(">> Human Alive.");
    }

    public void live() {
        // Delegation: Human delegates 'living' to the heart's function.
        heart.beat();
    }
}

// Execution Trace
class GodMode {
    public static void main(String[] args) {
        Human adam = new Human();
        // Output Order:
        // 1. Human Embryo Forming...
        // 2. Heart Tissue Generated... (Constructor of Part)
        // 3. Human Alive. (Constructor of Whole completes)
        
        adam = null; 
        // When 'adam' is GC'd, 'heart' is also GC'd (Unreachable).
        // This confirms strict Composition.
    }
}
```

## 3. Memory & System Context
*   **Heap Graph:** The `Human` object on the Heap has a field reference pointing to a separate `Heart` object on the Heap.
*   **Encapsulation Boundary:** By making the `Heart` reference `private`, the `Human` class acts as a hardware abstraction layer (HAL). The outside world calls `human.live()`, unaware of the `Heart` object. This allows you to replace the `Heart` logic without breaking the external API.

## 4. Best Practices
*   **Favor Composition over Inheritance:** This is a golden rule (GoF). Inheritance breaks encapsulation (White-box reuse). Composition maintains encapsulation (Black-box reuse).
*   **Validation:** Use Composition when you need to enforce constraints. A `Car` can ensure its `Engine` is never null.
*   **Diaper Pattern (Anti-Pattern):** Leaking the reference.
    ```java
    public Heart getHeart() { return this.heart; } // DANGEROUS!
    ```
    If you return the `heart` reference, external code can modify it. If you must return it, return a defensive copy or an immutable view.
