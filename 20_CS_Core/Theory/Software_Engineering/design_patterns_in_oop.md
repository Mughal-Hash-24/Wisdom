---
field/cs
subject/software-engineering
concept/design-patterns
---
[[T.O.C (Software Engineering)|Up to Software Engineering]]

# Design Patterns

## Singleton
> **Seed:** "Explain in detail the singleton pattern with examples in JAVA."
> **Lens:** First Principles / The Chief Engineer

## 1. Ontological Definition

The Singleton pattern is a **creational design pattern** that restricts the instantiation of a class to one "canonical" instance and provides a global point of access to that instance. It belongs to the domain of **software architecture and object-oriented design**, specifically addressing the need for controlled access to shared resources such as configuration managers, connection pools, or hardware interfaces.

## 2. The Internal Mechanics (Under the Hood)

The Singleton pattern functions by encapsulating the instantiation logic within the class itself and hiding the constructor from external actors. The mechanism relies on three core components:
1.  **Private Static Variable:** A reference that holds the unique instance of the class.
2.  **Private Constructor:** Prevents other classes from using the `new` operator.
3.  **Public Static Factory Method:** A method (usually named `getInstance()`) that returns the reference to the static variable, creating it if necessary.

### Implementation Variants in Java

#### A. Eager Initialization
The instance is created at the time of class loading. This is the simplest but can lead to resource wastage if the instance is never used.
```java
public class EagerSingleton {
    private static final EagerSingleton INSTANCE = new EagerSingleton();

    private EagerSingleton() {}

    public static EagerSingleton getInstance() {
        return INSTANCE;
    }
}
```

#### B. Lazy Initialization (Thread-Unsafe)
The instance is created only when requested. However, in a multithreaded environment, two threads could simultaneously check if the instance is null and create two separate objects.
```java
public class LazySingleton {
    private static LazySingleton instance;

    private LazySingleton() {}

    public static LazySingleton getInstance() {
        if (instance == null) {
            instance = new LazySingleton();
        }
        return instance;
    }
}
```

#### C. Double-Checked Locking (Thread-Safe)
To optimize performance, synchronization is applied only during the first creation. The `volatile` keyword is critical here to ensure that multiple threads handle the `instance` variable correctly as it is being initialized.
```java
public class ThreadSafeSingleton {
    private static volatile ThreadSafeSingleton instance;

    private ThreadSafeSingleton() {}

    public static ThreadSafeSingleton getInstance() {
        if (instance == null) {
            synchronized (ThreadSafeSingleton.class) {
                if (instance == null) {
                    instance = new ThreadSafeSingleton();
                }
            }
        }
        return instance;
    }
}
```

#### D. Bill Pugh Singleton (Inner Static Helper Class)
This is the most widely recommended approach. It uses the Java Classloader mechanism to ensure thread safety and lazy loading without explicit synchronization overhead.
```java
public class BillPughSingleton {
    private BillPughSingleton() {}

    private static class SingletonHelper {
        private static final BillPughSingleton INSTANCE = new BillPughSingleton();
    }

    public static BillPughSingleton getInstance() {
        return SingletonHelper.INSTANCE;
    }
}
```

## 3. Systems Context & Anchoring

The Singleton is like a **Nuclear Launch Console** in a military bunker. 
- **The Console (Instance):** There is only one physical unit that can authorize a launch.
- **The Protocol (getInstance):** Anyone needing to interact with the launch system must go through a specific security checkpoint (the factory method) rather than trying to build their own console.
- **The Guard (Private Constructor):** The guard prevents anyone from bringing in a second console from the outside.

In a computing system, this is exactly how a **Print Spooler** or a **Database Connection Pool** works. If multiple spoolers existed, they would fight over the printer hardware, leading to interleaved or corrupted documents. The Singleton ensures a single "traffic cop" manages the resource.

## 4. Edge Cases & Constraints

Even with robust implementations, the Singleton pattern can be compromised or create architectural bottlenecks:

1.  **Reflection Attack:** Java's Reflection API can change the access modifier of the private constructor to `public` at runtime.
    - *Defense:* Throw an exception inside the constructor if an instance already exists.
2.  **Serialization/Deserialization:** When a Singleton is serialized and then deserialized, a new instance is created by default.
    - *Defense:* Implement the `readResolve()` method to return the existing instance.
3.  **Classloader Isolation:** In complex environments (like OSGi or some Web Servers), if the same class is loaded by two different ClassLoaders, you may end up with two instances of the Singleton—one per ClassLoader.
4.  **Unit Testing:** Singletons introduce global state, making it difficult to isolate classes during testing. They often require mocking frameworks or "Reset" methods that break the pattern's core philosophy.
5.  **Enum Singleton:** Joshua Bloch (author of *Effective Java*) recommends using a single-element Enum as the best way to implement a Singleton, as it handles serialization and reflection attacks natively.
    ```java
    public enum EnumSingleton {
        INSTANCE;
        public void someMethod() { /* ... */ }
    }
    ```

## Factory
> **Seed:** "Explain in detail the factory pattern with examples in JAVA"
> **Lens:** First Principles / The Chief Engineer

## 1. Ontological Definition
The Factory Pattern is a creational design pattern that defines an interface for creating an object, but lets subclasses or specialized methods decide which class to instantiate. It belongs to the domain of **Creational Design Patterns** in Software Engineering. Its primary purpose is to decouple the client code (the requester) from the concrete implementation of the objects it consumes, promoting the **Dependency Inversion Principle** (depending on abstractions, not concretions).

## 2. The Internal Mechanics (Under the Hood)
The Factory Pattern operates by encapsulating the `new` operator. In a standard system, the client is responsible for both choosing the class and instantiating it. With the Factory Pattern, the client delegates these responsibilities to a dedicated object or method.

### Control and Data Flow
1. **Request Phase:** The client invokes a factory method, often passing a parameter (a string, an enum, or a configuration object) that specifies the desired product type.
2. **Decision Phase:** The factory evaluates the request logic (often via a switch-case, if-else, or registry lookup).
3. **Instantiation Phase:** The factory invokes the constructor of the specific `ConcreteProduct`.
4. **Return Phase:** The factory returns the new instance upcast to a common `Product` interface. The client never sees the concrete class name.

### Java Implementation: Factory Method Pattern
In the formal **Factory Method** (GoF), the creation is deferred to subclasses.

```java
// 1. The Product Interface
interface Transport {
    void deliver();
}

// 2. Concrete Products
class Truck implements Transport {
    public void deliver() { System.out.println("Delivering by land in a box."); }
}

class Ship implements Transport {
    public void deliver() { System.out.println("Delivering by sea in a container."); }
}

// 3. The Creator (Factory)
abstract class Logistics {
    // This is the core 'Factory Method'
    public abstract Transport createTransport();

    public void planDelivery() {
        Transport t = createTransport();
        t.deliver();
    }
}

// 4. Concrete Creators
class RoadLogistics extends Logistics {
    @Override
    public Transport createTransport() {
        return new Truck();
    }
}

class SeaLogistics extends Logistics {
    @Override
    public Transport createTransport() {
        return new Ship();
    }
}
```

### Data Structures Involved
- **Virtual Method Table (vtable):** Java uses dynamic dispatch to resolve which `createTransport()` to call at runtime.
- **Class Metadata:** The JVM uses its internal class loading mechanism to resolve the `ConcreteProduct` types when the factory invokes `new`.

## 3. Systems Context & Anchoring
The Factory Pattern is analogous to a **Restaurant's Front-of-House (Interface) and Kitchen (Factory)**.

- **The Customer (Client):** Browses a Menu (Interface) and orders a "Burger." They do not know if the kitchen uses a grill or a broiler, or which specific chef is working.
- **The Waiter (Factory/Creator):** Takes the order. The waiter doesn't cook; they pass the "type" to the kitchen.
- **The Kitchen (Factory Method):** Based on the order type ("Burger" vs "Pizza"), the kitchen decides which station (Subclass/Logic) prepares the food.
- **The Meal (Product):** What arrives at the table is simply "Food" (the Interface). The customer interacts with it (e.g., `eat()`) regardless of its concrete ingredients.

This separation allows the restaurant to change its kitchen equipment or chef staff (Implementation) without the customer needing to change how they order or eat.

## 4. Edge Cases & Constraints

### The "Switch-Case" Explosion (Maintenance Debt)
In the "Simple Factory" variant (a static method with a switch block), adding a new product type requires modifying the factory's source code. This violates the **Open/Closed Principle**. If the number of types grows to dozens or hundreds, the factory method becomes a massive, unmaintainable "God Method."
*   *Mitigation:* Use a **Registry Pattern** where products register themselves with the factory via reflection or dependency injection.

### Abstraction Overkill (The "YAGNI" Violation)
If a system only ever requires one type of `Transport`, implementing three interfaces and two factory classes adds unnecessary cognitive load and "boilerplate" code. The factory pattern adds a layer of indirection that can make debugging harder (jumping through multiple files to find the actual constructor call).
*   *Constraint:* Avoid factories for stable, non-varying object types. Use them only when the product family is expected to grow or change.

### Object Lifecycle Management
The Factory creates the object, but who owns it? If the Factory returns a `Closeable` resource (like a Database Connection), the client must be aware of the lifecycle, even if they aren't aware of the concrete type. Failure to manage this leads to resource leaks.

## Strategy
> **Seed:** "Explain in detail the strategy pattern with examples in JAVA"
> **Lens:** First Principles / The Chief Engineer

## 1. Ontological Definition

The **Strategy Pattern** is a behavioral design pattern that defines a family of algorithms, encapsulates each one within a separate class, and makes them interchangeable via a common interface. It belongs to the domain of **Object-Oriented Design (OOD)** and is primarily used to adhere to the **Open/Closed Principle**, allowing the behavior of a class (the "Context") to be extended without modifying its source code.

## 2. The Internal Mechanics (Under the Hood)

The Strategy pattern decouples the *selection* of an algorithm from its *execution*. This is achieved through three primary components:

1.  **Strategy Interface:** A common contract for all supported algorithms.
2.  **Concrete Strategies:** Individual classes implementing the specific logic of the algorithm.
3.  **Context:** The class that maintains a reference to a Strategy object and delegates the work to it.

### Control and Data Flow
- **Initialization:** The Client creates a `Context` and passes a `ConcreteStrategy` instance to it (often via constructor or setter).
- **Execution:** When the `Context` needs to perform a task, it calls the strategy's method. It does not know which concrete implementation it is using; it only knows the interface.
- **Dynamic Swapping:** Because the reference is polymorphic, the Strategy can be replaced at runtime (e.g., switching from a `HighPrecisionStrategy` to a `HighSpeedStrategy` based on system load).

### Java Implementation: Payment System Example

```java
// 1. The Strategy Interface
interface PaymentStrategy {
    void pay(int amount);
}

// 2. Concrete Strategy A: Credit Card
class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;
    public CreditCardStrategy(String card) { this.cardNumber = card; }
    
    @Override
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Credit Card: " + cardNumber);
    }
}

// 3. Concrete Strategy B: PayPal
class PayPalStrategy implements PaymentStrategy {
    private String email;
    public PayPalStrategy(String email) { this.email = email; }
    
    @Override
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using PayPal: " + email);
    }
}

// 4. The Context
class ShoppingCart {
    private PaymentStrategy strategy;

    // The Context accepts any object that implements PaymentStrategy
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    public void checkout(int amount) {
        if (strategy == null) {
            throw new IllegalStateException("Payment strategy not set");
        }
        strategy.pay(amount); // Delegation
    }
}

// 5. Client Usage
public class Main {
    public static void main(String[] args) {
        ShoppingCart cart = new ShoppingCart();
        
        // Dynamic selection of strategy
        cart.setPaymentStrategy(new CreditCardStrategy("1234-5678-9012"));
        cart.checkout(100);
        
        cart.setPaymentStrategy(new PayPalStrategy("user@example.com"));
        cart.checkout(200);
    }
}
```

### Key Data Structures
- **Polymorphic Reference Table (vtable):** In the JVM, calling `strategy.pay()` involves a virtual method lookup. The `Context` holds a pointer to the object on the heap; the JVM uses the object's header to find the correct method implementation in the class's method table.

## 3. Systems Context & Anchoring

The Strategy Pattern is functionally equivalent to a **Universal Power Tool with Interchangeable Bits**.

- **The Drill (Context):** Provides the motor, battery, and trigger. It knows how to "spin," but it doesn't know what material it is working on.
- **The Drill Bit (Strategy):** There are specific bits for masonry, wood, and metal. Each bit fits into the drill's chuck (the Interface).
- **The Operator (Client):** Chooses the bit based on the task and inserts it into the drill.

If you need to drill through glass, you don't redesign the drill; you simply create a new "Glass Bit" (Concrete Strategy) that conforms to the standard shank size (Interface). The drill remains unchanged, yet its capability is extended.

## 4. Edge Cases & Constraints

### Strategy Explosion
When a system has dozens of small algorithmic variations, the Strategy pattern leads to a "class explosion." Each variation requires a new `.java` file and class definition. In modern Java (8+), this is often mitigated by using **Lambdas or Method References** for simple strategies, treating the interface as a `@FunctionalInterface`.

### Client Awareness Requirement
The Client must be aware of the differences between strategies to choose the correct one. This can leak implementation details upward. If the Client shouldn't know these details, the Strategy pattern is often paired with a **Factory Pattern** to encapsulate the strategy selection logic.

### Communication Overhead
The Strategy interface is shared by all concrete implementations. If `StrategyA` requires 5 parameters but `StrategyB` requires only 1, the interface must either pass all 5 (forcing `StrategyB` to ignore 4) or pass a generic `Context` object, which increases coupling between the Strategy and the Context.
