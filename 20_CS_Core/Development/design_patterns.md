---
tags:
  - concept/design-patterns
  - field/cs
  - subject/software-engineering
---
[[T.O.C (Development)|Up to Development]]

# Design patterns
> **Seed:** "Explain in detail the design patterns used in OOP along with structural examples in JAVA code"
> **Lens:** First Principles / The Chief Engineer

## 1. Ontological Definition

In object-oriented programming (OOP), **design patterns** are formalized, reusable solutions to recurring architectural challenges encountered during software development. They represent "distilled wisdom" rather than finished designs; they are templates for how to solve a problem that can be used in many different situations. Design patterns belong to the domain of **Software Engineering and System Architecture**, specifically addressing the decoupling of object creation, structural composition, and behavioral communication to maximize maintainability, scalability, and robustness.

Design patterns are traditionally categorized into three fundamental groups based on their intent:
*   **Creational Patterns:** Mechanisms for object creation that increase flexibility and reuse of existing code.
*   **Structural Patterns:** Techniques for assembling objects and classes into larger structures while keeping these structures flexible and efficient.
*   **Behavioral Patterns:** Algorithms and the assignment of responsibilities between objects.

## 2. The Internal Mechanics (Under the Hood)

The core mechanism of design patterns relies on **polymorphism**, **encapsulation**, and **composition** over inheritance. By defining interfaces and abstract classes, patterns allow the system to remain agnostic of the specific concrete classes being instantiated or manipulated.

### 2.1 Creational: The Singleton Pattern
The Singleton ensures a class has only one instance and provides a global point of access to it. It manages its own lifecycle via a private constructor and a static holder.

**Java Implementation (Thread-Safe):**
```java
public class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    private DatabaseConnection() { /* Private constructor to prevent instantiation */ }

    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}
```

### 2.2 Structural: The Decorator Pattern
The Decorator allows behavior to be added to an individual object, dynamically, without affecting the behavior of other objects from the same class. It uses a "wrapper" approach.

**Java Implementation:**
```java
interface Coffee { double getCost(); }

class SimpleCoffee implements Coffee {
    public double getCost() { return 5.0; }
}

abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee;
    public CoffeeDecorator(Coffee coffee) { this.decoratedCoffee = coffee; }
    public double getCost() { return decoratedCoffee.getCost(); }
}

class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }
    public double getCost() { return super.getCost() + 1.5; }
}

// Usage: Coffee myCoffee = new MilkDecorator(new SimpleCoffee());
```

### 2.3 Behavioral: The Strategy Pattern
The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from the clients that use it.

**Java Implementation:**
```java
interface PaymentStrategy { void pay(int amount); }

class CreditCardPayment implements PaymentStrategy {
    public void pay(int amount) { System.out.println("Paid " + amount + " via Credit Card."); }
}

class PayPalPayment implements PaymentStrategy {
    public void pay(int amount) { System.out.println("Paid " + amount + " via PayPal."); }
}

class ShoppingCart {
    private PaymentStrategy strategy;
    public void setPaymentStrategy(PaymentStrategy strategy) { this.strategy = strategy; }
    public void checkout(int amount) { strategy.pay(amount); }
}
```

## 3. Systems Context & Anchoring

Design patterns are akin to a **modular construction site**.

*   **Creational Patterns** are the **Factory/Prefab Plant**. Instead of builders casting every concrete pillar on-site (manual instantiation), they request a specific "SupportPillar" from the plant. The plant decides whether to reuse a mold or create a new one, shielding the construction site from the complexities of manufacturing.
*   **Structural Patterns** are the **Standardized Adapters and Connectors**. Just as a universal pipe adapter allows a European faucet to connect to an American plumbing system, the *Adapter* pattern allows incompatible interfaces to collaborate. The *Decorator* is like adding insulation or cladding to a standard wall—it enhances the structure without changing the underlying foundation.
*   **Behavioral Patterns** are the **Intercom and Logistics Systems**. The *Observer* pattern is the site-wide alarm: when the "End of Shift" sensor triggers, all workers (subscribers) react accordingly. The *Strategy* pattern is the choice of logistics: today we use a crane (Algorithm A), tomorrow a pulley (Algorithm B), depending on the load, without changing the building's blueprint.

## 4. Edge Cases & Constraints

While powerful, design patterns introduce specific risks and trade-offs:

1.  **Patternitis (Over-Engineering):** The most common failure mode occurs when developers apply complex patterns to trivial problems. Implementing a *Abstract Factory* for a system that only ever needs one type of object increases cognitive load and boilerplate code without providing any actual benefit to flexibility.
2.  **Performance Overhead:** Indirection—the core of many patterns—is not free. Patterns like *Proxy* or *Decorator* introduce additional method calls and object allocations. In high-frequency, low-latency systems (e.g., game engines or HFT), the cost of multiple virtual function calls (vtable lookups) can become a bottleneck.
3.  **Fragility of Abstraction:** Patterns rely on stable interfaces. If the underlying requirements change such that the interface itself must be modified, every implementation and decorator in the chain must be updated, leading to a "shotgun surgery" anti-pattern where a single change forces modifications across dozens of files.