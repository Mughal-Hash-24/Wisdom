---
created: 2026-01-22 12:20
tags:
- field/cs
- subject/programming/python
- concept/python/strings
related:
- - Python_Variables_and_Casting
---
# Python Strings and Literals

[[T.O.C (Python)|Up to Python]]

## Python Literals vs C++ Literals
In C++, a literal like `"hello"` is a `const char*` stored in the read-only section of the binary (Text segment).
In Python, literals are **Immediate Objects**.

| Feature | C++ Literals | Python Literals |
| :--- | :--- | :--- |
| **Storage** | Binary Data Segment (Static). | Created as Objects on the Heap. |
| **Mutability** | Immutable. | Immutable. |
| **Interning** | Handled by Compiler (sometimes). | **String Interning:** Python automatically reuses objects for small strings and certain integers (-5 to 256) to save memory. |

## Data Types Table
| Category | Type | Example Initialization |
| :--- | :--- | :--- |
| **Numeric** | `int` | `x = 42` |
| | `float` | `y = 3.14` |
| | `complex`| `z = 1 + 2j` |
| **Sequence** | `str` | `s = "text"` or `s = 'text'` |
| | `list` | `l = [1, 2, 3]` |
| | `tuple` | `t = (1, 2, 3)` |
| | `range` | `r = range(10)` |
| **Mapping** | `dict` | `d = {"key": "val"}` |
| **Set** | `set` | `s = {1, 2, 3}` |
| | `frozenset`| `fs = frozenset({1, 2})` |
| **Boolean** | `bool` | `b = True` |
| **None** | `NoneType`| `n = None` |

## Strings Deep Dive
Strings in Python are sequences of Unicode characters.

### Comparison to C++
*   **Encoding:** C++ `std::string` is usually a sequence of bytes (ASCII/UTF-8). Python `str` is fully Unicode-compliant.
*   **Immutability:** You cannot do `s[0] = 'A'` in Python. This prevents a whole class of bugs and allows for efficient memory sharing (interning).
*   **Memory:** Python strings store their length, hash, and encoding type along with the character data.

### String Operations Table
| Operation | Syntax | Usage Example |
| :--- | :--- | :--- |
| **Slicing** | `[start:end:step]`| `"Python"[0:2]` -> `"Py"` |
| **Joining** | `.join(iterable)` | `"-".join(["A", "B"])` -> `"A-B"` |
| **Splitting** | `.split(sep)` | `"A B".split(" ")` -> `["A", "B"]` |
| **Formatting** | `f"{var}"` | `f"Value: {x}"` (F-Strings) |
| **Replace** | `.replace(old, new)`| `"hi".replace("h", "b")` -> `"bi"` |
| **Find** | `.find(sub)` | `"abc".find("b")` -> `1` |
| **Multi-line** | `"""..."""` | Preserves newlines and quotes. |
