---
created: 2026-01-22 12:10
tags: [concept, python, memory, architecture]
related: [[Python_Philosophy_and_Intro]]
---
# Python Execution and Memory Model

[[T.O.C (Python)|Up to Python]]

## My First Python Program: Under the Hood

```python
def main():
    message = "Hello Python"
    print(message)

if __name__ == "__main__":
    main()
```

### Background Execution Process
1.  **Lexing & Parsing:** The interpreter reads the `.py` file, breaks it into tokens, and builds an Abstract Syntax Tree (AST).
2.  **Compilation to Bytecode:** Unlike C++ which compiles to machine code (binary), Python compiles the AST into **Bytecode** (`.pyc` files or `__pycache__`). This is a set of instructions for the Python Virtual Machine (PVM).
3.  **PVM Interpretation:** The PVM executes the bytecode.
4.  **The `if __name__` block:** In Python, every file is a "module." If you run a file directly, Python sets a special internal variable `__name__` to `"__main__"`. This block acts as the entry point, similar to `int main()` in C++.

## Indentation: The Lexer's Logic
Python uses indentation to define code blocks.
*   **Lexer Stack:** The lexer maintains a stack of indentation levels.
*   **INDENT Token:** When a line has more whitespace than the previous one, the lexer pushes the new level onto the stack and generates an `INDENT` token.
*   **DEDENT Token:** When whitespace decreases, the lexer pops from the stack until it matches a previous level, generating a `DEDENT` token for each pop.
*   **C++ Analogy:** `INDENT` is `{` and `DEDENT` is `}`.

## Memory Layout
In C++, memory is divided into Text, BSS, Data, Stack, and Heap. Python's layout is managed by the **CPython Memory Manager**.

1.  **The Python Heap (Private Heap):**
    *   Unlike the C++ heap where you manually allocate, the Python heap is managed by the interpreter.
    *   **Everything is an object** (integers, strings, functions). All these live on the heap.
2.  **Object-Specific Allocators:** Python has optimized allocators for small objects (under 512 bytes) to avoid frequent calls to the OS's `malloc`.
3.  **The Python Stack:**
    *   Each function call creates a **Frame Object** on the PVM stack.
    *   The frame contains the code object, local variables (references), and a reference to the global namespace.
    *   **Crucial Difference:** In C++, a local `int x` is raw bits on the stack. In Python, the stack frame only holds a **Reference (Pointer)** to an object sitting in the heap.

## Procedures & Stack Frames
In C++, a stack frame is a contiguous block of memory. In Python, a "Procedure" (function) call is more complex:
1.  **Frame Creation:** A new `PyFrameObject` is allocated on the heap (ironically) and linked to the current stack.
2.  **Input/Return:**
    *   Arguments are passed by **Assignment** (Object Reference).
    *   Every Python function returns something. If no `return` is specified, it returns `None` (a singleton object).
3.  **Dynamic Checking:** Unlike C++ where the return type is fixed at compile-time, Python checks the type of the returned object only when it is accessed by the caller.
