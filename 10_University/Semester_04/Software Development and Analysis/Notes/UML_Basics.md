---
created: 2026-01-22 10:40
tags: [concept, sda, uml]
related: []
---
# UML (Unified Modeling Language)

[[T.O.C (Software Development and Analysis Notes)|Up to SDA Notes]]

## Gemini: The "Blueprints" Mental Model
UML is the **Architectural Blueprint** of software.
*   **English is ambiguous:** If I say "The user talks to the bank," does that mean an ATM, a teller, or an app?
*   **Code is too detailed:** You don't show the bricks when explaining the layout of a house.
*   **UML is the Standard:** It's a visual language (ISO standard) that everyone (Developers, PMs, Clients) agrees on.

---

## 1. Overview & Purpose
UML diagrams are used to **Visualize**, **Specify**, **Construct**, and **Document** the artifacts of a software system.

| Category | Purpose | Example Question it Answers |
| :--- | :--- | :--- |
| **Structural** (Static) | Shows the **things** in the system. The "Anatomy". | "What pieces make up this car?" (Engine, Wheels) |
| **Behavioral** (Dynamic) | Shows what happens **over time**. The "Physiology". | "What happens when I turn the key?" |
| **Interaction** | A subset of Behavioral. Shows **data flow** between things. | "How does the Engine talk to the Wheels?" |

## 2. Types of UML Diagrams

### A. Structural Diagrams (The "Nouns")
1.  **Class Diagram (The King):**
    *   Most common. Shows classes, attributes, methods, and relationships (Inheritance, Composition).
    *   *Example:* A `Student` class is connected to a `Course` class.
2.  **Object Diagram:**
    *   A snapshot of the system at a specific moment.
    *   *Example:* `John (Student)` is linked to `CS101 (Course)`.
3.  **Component Diagram:**
    *   Shows how code modules are wired together.
    *   *Example:* `BillingService.dll` talks to `Database.dll`.

### B. Behavioral Diagrams (The "Verbs")
1.  **Use Case Diagram:**
    *   High-level view of functionality.
    *   *Example:* Stick figure (Actor) -> Oval (Login).
2.  **Activity Diagram:**
    *   Flowchart of a process.
    *   *Example:* Start -> Check Balance -> If > 0, Withdraw -> End.
3.  **State Machine Diagram:**
    *   Lifecycle of an object.
    *   *Example:* Order Created -> Paid -> Shipped -> Delivered.

### C. Interaction Diagrams (The "Conversation")
1.  **Sequence Diagram:**
    *   Time-ordered message exchange.
    *   *Example:* User -> (Request) -> Server -> (Query) -> DB.
