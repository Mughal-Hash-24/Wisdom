---
created: 2026-01-22 12:25
tags:
- field/cs
- subject/programming/python
- concept/python/lists
related:
- - Python_Execution_and_Memory_Model
---
# Python Lists and Arrays Deep Dive

[[T.O.C (Python)|Up to Python]]

## What is a Python List?
In C++, an array `int arr[5]` is a contiguous block of memory for 5 integers.
A Python `list` is a **Dynamic Array of Object References**.

### Memory Layout
*   A list does **not** store data directly. It stores **Pointers** to objects.
*   **Contiguity:** The array of pointers is contiguous in memory, allowing for O(1) random access by index.
*   **The "Heterogeneous" Secret:** Because the list only stores pointers (which are all the same size, 64-bit on modern systems), it doesn't matter if one pointer points to an `int` and the next points to a `string`. The list itself remains a uniform array of pointers.

### Comparison: Python List vs. C++ Array
| Feature | C++ Array | Python List |
| :--- | :--- | :--- |
| **Memory Architecture**| Contiguous Values. | Contiguous Pointers to Dispersed Objects. |
| **Identifier** | A pointer to the first element. | A pointer to a `PyListObject` structure. |
| **Resizing** | Impossible (Fixed size). | Dynamic (Uses over-allocation to make `append` O(1) amortized). |
| **Performance** | Cache-friendly (data is close). | Cache-unfriendly (chasing pointers). |

## List Operations Table
| Operation | Syntax | Background Process |
| :--- | :--- | :--- |
| **Append** | `l.append(x)` | Adds pointer to end. If full, doubles array size. |
| **Insert** | `l.insert(0, x)` | **O(n):** Must shift every pointer one index to the right. |
| **Remove** | `l.remove(x)` | Searches for `x`, then shifts all subsequent pointers. |
| **Pop** | `l.pop()` | Removes last pointer. O(1). |
| **Extend** | `l.extend(l2)` | Iterates and appends each reference from `l2`. |
| **Comprehension**| `[x*2 for x in l]`| Optimized internal C loop for creating new lists. |

## Lists in Memory: The Over-Allocation Strategy
When you create a list `[1, 2]`, Python might actually allocate space for 4 pointers.
*   **Growth Pattern:** 0, 4, 8, 16, 25, 35, 46, 58, 72, 88...
*   **Why?** To avoid calling `realloc()` every time you `append`.
*   **Multiple Types:** If you have `l = [1, "hi"]`, the list structure has two slots:
    1. Slot 0 -> Address of PyObject_Int(1)
    2. Slot 1 -> Address of PyObject_Str("hi")
    The list doesn't care about the content; it only cares that the addresses fit in its slots.
