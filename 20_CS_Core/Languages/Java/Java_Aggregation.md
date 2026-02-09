---
tags:
- field/cs
- subject/programming/java
- concept/java/aggregation
---

[[T.O.C (Java)|Up to Java]]

> **Prompt:** "Write a detailed explanation of Aggregation in classes in java along with diverse code examples with proper syntax explanations of each case like what happens with certain access specifiers and what encapsulation takes place when composing."
> **Lens Applied:** The Chief Engineer / The Constructivist

# Technical breakdown: Aggregation ("Has-A" Weak)

## 1. Surgical Definition (Internals)
Aggregation is a **Weak "Has-A" Relationship**. It implies a relationship where the Part can exist independently of the Whole. They have separate lifecycles.

In memory terms: The Container holds a reference to the Part, but the Part was likely created *outside* the Container and passed in (Dependency Injection). If the Container is Garbage Collected, the Part lives on.

## 2. The Laboratory (Proof of Concept)

### Experiment: Department & Teacher (Loose Coupling)

```java
// The Part (Independent Entity)
class Teacher {
    private String name;

    public Teacher(String name) {
        this.name = name;
        System.out.println(">> Teacher " + name + " Hired.");
    }
    
    public String getName() { return name; }
}

// The Whole (Container)
public class Department {
    private String deptName;
    // Aggregation: List of references to External Objects
    private List<Teacher> staff;

    public Department(String deptName, List<Teacher> staff) {
        this.deptName = deptName;
        // Shallow Copy or Direct Reference implies Aggregation
        this.staff = staff; 
        System.out.println(">> Department " + deptName + " Created.");
    }
}

// Execution Trace
class UniversityAdmin {
    public static void main(String[] args) {
        // 1. Create Parts INDEPENDENTLY
        Teacher t1 = new Teacher("Einstein");
        Teacher t2 = new Teacher("Feynman");

        List<Teacher> physicsStaff = new ArrayList<>();
        physicsStaff.add(t1);
        physicsStaff.add(t2);

        // 2. Create Whole (Inject Parts)
        Department physics = new Department("Physics", physicsStaff);

        // 3. Destroy Whole
        physics = null;
        System.gc(); // Request Garbage Collection

        // 4. Verification
        // 't1' and 't2' ARE STILL ALIVE. 
        // They are referenced by 'physicsStaff' and main stack frame.
        System.out.println(t1.getName() + " is still researching.");
    }
}
```

## 3. Memory & System Context
*   **Reference Counting (Conceptual):** In Aggregation, the object being pointed to (Teacher) has at least two incoming references: one from the `main` scope/registry and one from the `Department`. Destroying the `Department` removes only one edge. The node remains.
*   **Encapsulation:** Aggregation usually exposes less encapsulation than Composition because the objects are often mutable and shared. This is necessary for systems like Databases or School Registries where entities (Students/Teachers) move between containers (Classes/Departments).

## 4. Best Practices
*   **Use for Shared Resources:** Use Aggregation when multiple objects need to access the same resource (e.g., a Logger, a Database Connection, or a Config object).
*   **Defensive Copying:** If the `Department` needs to ensure the list of staff isn't modified externally after creation, it should create a `new ArrayList<>(staff)` in the constructor. This creates a hybrid: The *List* is composed (owned), but the *Teachers* inside are aggregated (shared).
