---
created: 2026-01-22 12:15
tags: [concept, python, memory]
related: [[Python_Execution_and_Memory_Model]]
---
# Python Variables and Casting

[[T.O.C (Python)|Up to Python]]

## The Variable System: Reference vs. Box
In C++, a variable is a **Memory Address** with a name. `int x = 5;` means "At address 0x100, store the 4-byte representation of 5."
In Python, a variable is a **Name** (Symbol) in a namespace dictionary that points to an **Object**.

### Key Characteristics
1.  **Dynamic Typing:** A variable `x` can point to an `int`, then later to a `list`. The variable itself has no type; only the object it points to has a type.
2.  **No Type Constraints:** If you try to store a float in a variable that previously held an int, Python simply updates the pointer.
3.  **Const Variables:** Python **does not have built-in `const` keywords.**
    *   *Convention:* Use all-caps (e.g., `PI = 3.14`).
    *   *Alternative:* Use a `NamedTuple` or a custom Class with `@property` and no setter.
4.  **IEEE 754:** Python's `float` type is equivalent to a C++ `double` (64-bit). It follows the IEEE 754 standard for floating-point arithmetic.

## Memory Internals of a Variable
Every Python object (even a simple integer) is a C structure called `PyObject`.
```c
// Simplified CPython Source
struct _object {
    Py_ssize_t ob_refcnt;   // Reference count for Garbage Collection
    struct _typeobject *ob_type; // Pointer to the type (e.g., int class)
};
```
*   **Reference Counting:** When you do `y = x`, the `ob_refcnt` of the object `x` points to is incremented. When `y` goes out of scope, it's decremented. When it hits 0, the object is deallocated.

## Casting: Re-Construction vs. Re-Interpretation
In C++, casting (especially `reinterpret_cast`) is about telling the compiler "Treat these bits as this type."
In Python, casting is **Constructor Invocation**.

*   `x = int("10")`: This calls the `__init__` method of the `int` class, which parses the string and creates a brand-new `int` object.
*   **Python vs C++ Flexibility:**
    *   C++ allows dangerous casting (pointer to int).
    *   Python only allows "Logical" casting. You can't cast a random class to an `int` unless you define the `__int__` magic method for that class.

## Local vs Global Memory
Memory management for variables depends on their scope:
1.  **Global Variables:**
    *   Stored in the `__dict__` of the module.
    *   Lifetime: They exist as long as the module is loaded (usually the life of the program).
2.  **Local Variables:**
    *   Stored in the current Stack Frame's `f_locals` array.
    *   Lifetime: They are marked for deletion as soon as the function returns (unless they are part of a Closure).
3.  **Memory Location:** Both live in the **Heap** (as objects), but the *references* to them live in different namespace dictionaries.
    *   *Analogy:* In C++, locals are on the stack. In Python, the *pointer* to the local is on the stack, but the data is always on the heap.
