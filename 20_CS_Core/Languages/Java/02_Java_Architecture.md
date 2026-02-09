---
created: 2026-01-22 10:25
tags:
- field/cs
- subject/programming/java
- concept/02/java
related:
- - 01_Java_Fundamentals
---
# Java Architecture & Ecosystem: Under the Hood

[[T.O.C (Java)|Up to Java]]

## 1. The ClassLoader Subsystem
The ClassLoader is responsible for dynamic loading. It follows a **Delegation Hierarchy** to ensure security.

1.  **Bootstrap ClassLoader:**
    *   Written in native C++.
    *   Loads core Java libraries (`rt.jar`, `java.lang.*`) from the JDK home.
    *   *Trust Level:* Ultimate.
2.  **Platform/Extension ClassLoader:**
    *   Loads extensions and platform-specific modules.
3.  **Application/System ClassLoader:**
    *   Loads **your** code from the `CLASSPATH`.

**The Delegation Model:**
When you ask for `java.lang.String`, the App loader asks the Platform loader, which asks the Bootstrap loader.
*   *Why?* Security. If you write a malicious class named `java.lang.String`, the Bootstrap loader will find the *real* one first. Your fake one will be ignored, preventing you from crashing the core system.

---

## 2. Runtime Data Areas
The JVM memory is strictly partitioned.

### A. Thread-Private (Fast, No Locking)
1.  **Program Counter (PC) Register:**
    *   Holds the address of the *current* bytecode instruction being executed.
2.  **Java Virtual Machine Stack:**
    *   Stores **Stack Frames**. Each method call pushes a frame.
    *   **Frame Content:**
        *   **Local Variable Array:** Arguments and local vars.
        *   **Operand Stack:** Scratchpad for calculations (`iadd`, `imul`).
        *   **Frame Data:** Reference to Constant Pool, Exception table.
3.  **Native Method Stack:**
    *   Used for C/C++ code called via JNI (Java Native Interface).

### B. Thread-Shared (Needs Locking/GC)
1.  **Heap:**
    *   Where **ALL** Objects live.
    *   Divided into **Young Generation** (Eden, Survivor) and **Old Generation**.
2.  **Method Area (Metaspace):**
    *   Stores **Class Metadata**: Method code (bytecode), Field names, Runtime Constant Pool.
    *   *Note:* Since Java 8, this is in Native Memory (outside the Heap) to avoid `OutOfMemoryError: PermGen`.

---

## 3. The Execution Engine: Interpreter vs JIT
This is the "Brain" of the JVM.

### Phase 1: Interpretation
When the application starts, the **Interpreter** reads bytecode line-by-line and converts it to machine code.
*   **Pros:** Starts immediately.
*   **Cons:** Slow. Repeating a loop 1 million times means interpreting the same bytecode 1 million times.

### Phase 2: Profiling (The "Watcher")
The JVM includes a **Profiler** that counts method calls and loop iterations.
*   If a method runs > 10,000 times (configurable), it is marked as a **"Hot Spot"**.

### Phase 3: JIT (Just-In-Time) Compilation
The **C1 and C2 Compilers** kick in for Hot Spots.
1.  **C1 (Client Compiler):** Fast compilation, simple optimizations (method inlining).
2.  **C2 (Server Compiler):** Slow compilation, aggressive optimizations.
    *   **Dead Code Elimination:** Removes code that affects nothing.
    *   **Loop Unrolling:** Replaces loops with sequential instructions to avoid jump overhead.
    *   **Escape Analysis:** If an object is created inside a method and *never escapes* (never returned or assigned to a global), the JIT might **stack-allocate** it (skipping the Heap/GC entirely). This is black magic.

---

## 4. JNI (Java Native Interface)
How does Java talk to hardware (Network, Files, Graphics)?
*   It cannot do it directly. It uses **JNI** to call C functions in the OS kernel.
*   `System.out.println` eventually calls a `private native writeBytes()` method, which triggers a C function to write to the console stream.

## Architecture Diagram (Mental Model)

```mermaid
graph TD
    subgraph "ClassLoader Subsystem"
        Boot[Bootstrap Loader] --> Ext[Platform Loader] --> App[App Loader]
    end
    
    subgraph "Runtime Data Areas"
        subgraph Shared
            Heap[Heap (Objects)]
            Meta[Metaspace (Class Data)]
        end
        subgraph Private[Thread Private]
            Stack[JVM Stack]
            PC[PC Register]
        end
    end
    
    subgraph "Execution Engine"
        Int[Interpreter]
        JIT[JIT Compiler (C1/C2)]
        GC[Garbage Collector]
    end
    
    App --> Shared
    Shared --> Int
    Int --> JIT
```