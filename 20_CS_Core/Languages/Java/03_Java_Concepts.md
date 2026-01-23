---
created: 2026-01-22 10:30
tags: [concept, java, oop, concurrency, gc, internals]
related: [[01_Java_Fundamentals]]
---
# Java Concepts: Deep Dive (OOP, GC, Concurrency)

[[T.O.C (Java)|Up to Java]]

## 1. OOP Internals: The V-Table (Itable)
How does Polymorphism work inside the machine?
`Animal a = new Dog(); a.makeSound();`

1.  **Compilation:** The compiler sees `Animal.makeSound()`. It doesn't know it's a Dog.
2.  **Runtime (The V-Table):**
    *   Every class in the Metaspace has a **Virtual Method Table (vtable)**.
    *   It's an array of function pointers.
    *   `Dog`'s vtable has `makeSound` pointing to `Dog::makeSound`.
    *   `Cat`'s vtable has `makeSound` pointing to `Cat::makeSound`.
3.  **Invocation:** The JVM looks at the **Klass Pointer** in the object header of `a`, goes to the `Dog` class metadata, looks up the 3rd method in the vtable (index is fixed at compile time), and jumps to that memory address.
    *   *Performance:* This "double indirection" is why virtual calls are slightly slower than static calls.

---

## 2. Garbage Collection (GC): The Algorithms
You don't free memory, the GC does. But how?

### A. The "Roots" of Reachability
The GC starts from **GC Roots**:
1.  Local variables on the Stack (currently active).
2.  Static variables (Global).
3.  JNI References.
*   **Algorithm:** It traces references from Roots. Anything connected is "Live". Anything unreachable is "Garbage".

### B. Generational Hypothesis
*   *Observation:* Most objects die young (temporary strings, iterators). Old objects (Connections, Singletons) tend to stay forever.
*   **Solution:** Split Heap into **Young Gen** and **Old Gen**.

### C. The Cycles
1.  **Minor GC (Young Gen):**
    *   **Eden Space:** New objects are born here.
    *   **Survivor Spaces (S0, S1):** When Eden is full, live objects are copied to S0. Dead ones are ignored (very fast).
    *   *The Copy:* Objects ping-pong between S0 and S1. Each time they survive, their "Age" (in the Object Header) increments.
2.  **Major/Full GC (Old Gen):**
    *   When an object hits Age 15 (default), it is **Tenured** (moved) to Old Gen.
    *   Old Gen fills up slower. When it does, a Major GC runs (often "Stop-The-World" pause).
    *   **Optimization:** Modern GCs (G1, ZGC) do this concurrently without pausing the app heavily.

---

## 3. Concurrency: The Java Memory Model (JMM)
In Multithreading, problems arise because **CPU Caches** are not instantly synced with Main Memory (RAM).

### A. The `volatile` Keyword
*   **Problem:** Thread A updates a flag `running = false`. Thread B (on a different CPU core) has cached `running = true`. Thread B loops forever.
*   **Solution:** `volatile boolean running;`
    *   Tells the JVM: "Do not cache this variable in CPU registers/L1 cache. Always read/write directly to Main RAM."
    *   **Happens-Before Guarantee:** A write to a volatile variable is visible to all subsequent reads.

### B. `synchronized` and Monitor Locks
*   **The Monitor:** Every Object in Java has an intrinsic "Monitor" lock (stored in the Object Header).
*   **Entry:** When a thread enters a `synchronized(obj)` block, it attempts to "Acquire ownership" of `obj`'s Monitor.
    *   If free: It marks the header with its Thread ID.
    *   If taken: The thread is put into a **BLOCKED** state (OS suspends the thread).
*   **Wait/Notify:**
    *   `obj.wait()`: "I own the lock, but I'm waiting for data. I release the lock and go to sleep."
    *   `obj.notify()`: "Wake up one sleeping thread on this object."

### C. Thread States
A thread is not just "Running" or "Stopped".
1.  **NEW:** Created but not `start()`ed.
2.  **RUNNABLE:** Executing (or waiting for CPU time).
3.  **BLOCKED:** Waiting for a lock (synchronized).
4.  **WAITING:** Waiting for a signal (`wait()`, `join()`).
5.  **TIMED_WAITING:** Sleeping for a fixed time.
6.  **TERMINATED:** `run()` method finished.

---

## 4. Checked vs Unchecked Exceptions
Java is unique in forcing you to handle errors.
1.  **Checked Exceptions (`IOException`, `SQLException`):**
    *   Errors that *might* happen in a correct program (File not found, Network down).
    *   **Rule:** You MUST `try-catch` or `throws`. The compiler forces this.
2.  **Unchecked Exceptions (`NullPointerException`, `ArrayIndexOutOfBounds`):**
    *   Programming errors (Bugs).
    *   **Rule:** You should fix the code, not catch the error.