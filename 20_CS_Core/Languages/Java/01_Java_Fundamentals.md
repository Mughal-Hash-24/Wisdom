---
created: 2026-01-22 10:20
tags: [concept, java, language_design, internals]
related: [[20_CS_Core/Theory/Kernel_Architecture_and_Development|OS Theory]]
---
# Java Fundamentals: Deep Dive

[[T.O.C (Java)|Up to Java]]

## 1. The "Write Once, Run Anywhere" Reality
Java achieves portability not by magic, but by **specification**.
*   **C++:** `sizeof(int)` depends on the compiler and CPU architecture (16-bit, 32-bit, or 64-bit). This causes "portability bugs" where code overflows on one machine but not another.
*   **Java:** The JVM Spec defines `int` as **exactly 32-bit signed two's complement** (-2^31 to 2^31-1), regardless of whether you run it on a 16-bit microcontroller or a 64-bit Supercomputer. The JVM is the "Virtual CPU" that enforces this consistency.

---

## 2. Anatomy of a Java Object (In Memory)
In C++, a `struct { int x; }` takes exactly 4 bytes (plus alignment padding).
In Java, `class A { int x; }` takes significantly more.

### The Object Header (12-16 bytes)
Every object in the Heap has a hidden header consisting of two machine words:
1.  **Mark Word (8 bytes on 64-bit):**
    *   Stores runtime metadata: **Hash Code**, **GC Age** (for generational collection), **Lock State** (Biased/Thin/Fat lock for synchronization).
2.  **Klass Pointer (4 bytes with Compressed Oops):**
    *   A pointer to the Class Metadata in the **Metaspace** (Method Area). This tells the JVM "I am an object of type A".

### The Body
3.  **Instance Data:** The actual fields (`int x`).
4.  **Padding:** The JVM aligns objects to 8-byte boundaries for performance.

*   **Total Size:** Header (12) + int (4) = 16 bytes.
*   *Compare to C++:* 4 bytes. Java trades memory for runtime intelligence (GC, Reflection, Locking).

---

## 3. The "Pass-by-Value" Truth
There is a massive misconception that "Primitives are pass-by-value, Objects are pass-by-reference."
**Correction:** Java is **ALWAYS Pass-by-Value**.

### The Mechanism
1.  **Primitives (`int a = 10`):** The *value* `10` is inside the box `a`. When passed to a function, the bits `10` are copied.
2.  **Objects (`Dog d = new Dog()`):**
    *   `d` is **NOT** the Dog. `d` is a **Reference** (a remote control) pointing to the Dog on the Heap.
    *   The "Value" of `d` is the **Memory Address** (e.g., `0x55A1`).
    *   When you pass `d` to a function, you copy the **Address** (`0x55A1`).
    *   *Result:* You have two remote controls pointing to the same Dog. If one remote changes the channel (modifies the object), the other sees it. But if one remote changes its batteries (reassigns the variable `d = new Cat()`), the other remote is unaffected.

---

## 4. Bytecode: The Language of the JVM
Java Source (`.java`) compiles to Bytecode (`.class`), which is a stack-based instruction set.

### Example: `int add(int a, int b) { return a + b; }`
Run `javap -c MyClass` to see this:

```asm
public int add(int, int);
  Code:
     0: iload_1       // Load integer from Local Variable 1 (a) onto Stack
     1: iload_2       // Load integer from Local Variable 2 (b) onto Stack
     2: iadd          // Pop top two, add them, push result
     3: ireturn       // Return top of stack
```

*   **Stack-Based Architecture:** The JVM doesn't use registers (mostly) for computation. It uses an **Operand Stack**.
*   **Why?** Compactness. Register-based instructions need to specify *which* register (`ADD R1, R2`). Stack instructions are implicit (`IADD` just adds the top two). This makes `.class` files tiny and network-friendly.

---

## 5. Execution Lifecycle: From Disk to CPU
When you run `java Main`:

1.  **Loading (ClassLoader):**
    *   Finds `Main.class` on disk.
    *   Reads the binary data.
    *   Creates a `Class` object in the Heap (representing the *type* Main).
2.  **Linking:**
    *   **Verification:** Checks for stack overflows, illegal pointers, and valid bytecode format. (Security).
    *   **Preparation:** Allocates memory for `static` variables (sets them to default 0/null).
    *   **Resolution:** Replaces symbolic references (`ConstantPool: #2 = Method System.out.println`) with direct memory references.
3.  **Initialization:**
    *   Executes `static { ... }` blocks and assigns initial values to static variables.
4.  **Invocation:**
    *   The JVM creates a **Main Thread**.
    *   It pushes the stack frame for `public static void main`.
    *   Execution begins.