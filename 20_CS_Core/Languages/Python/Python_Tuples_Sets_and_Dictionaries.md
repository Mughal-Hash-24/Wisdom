---
created: 2026-01-22 12:30
tags:
- field/cs
- subject/programming/python
- concept/python/tuples
related:
- - Python_Lists_and_Arrays_Deep_Dive
---
# Python Tuples, Sets, and Dictionaries

[[T.O.C (Python)|Up to Python]]

## 1. Tuples: The Immutable Sequence
*   **In Memory:** Exactly like a list (array of pointers), but the `PyTupleObject` structure lacks the logic to change its size or contents after creation.
*   **Performance:** Slightly faster than lists because they are simpler and can be "constant-folded" by the compiler.

| Operation | Syntax | Notes |
| :--- | :--- | :--- |
| **Unpacking** | `a, b = (1, 2)` | Extremely common in Python for multi-return. |
| **Count** | `t.count(x)` | Counts occurrences. |
| **Index** | `t.index(x)` | Finds first position. |

### Mutability Nuance
A tuple is immutable, but if it contains a mutable object (like a list), that list can still be modified.
`t = ([1, 2], 3)`
`t[0].append(3)` # This works! The tuple's *pointer* to the list didn't change.

## 2. Sets: The Unordered Collection
*   **In Memory:** A **Hash Table**.
*   **Logic:** It uses the `hash()` of the object to determine its position.
*   **Complexity:** O(1) for `in` checks.
*   **Requirement:** Elements must be **Hashable** (Immutable). You cannot put a list inside a set.

| Operation | Syntax | Code Example |
| :--- | :--- | :--- |
| **Add** | `.add(x)` | `s.add(10)` |
| **Union** | `s1 | s2` | `all_items = s1.union(s2)` |
| **Intersection**| `s1 & s2` | `common = s1.intersection(s2)` |

## 3. Dictionaries: The Core of Python
Nearly everything in Python (classes, modules, globals) is internally a Dictionary.

### Memory Architecture
*   **Hash Table with Open Addressing:** Python uses a sparse array of "entries". Each entry contains `(hash, key_ptr, value_ptr)`.
*   **Collision Handling:** Uses a sophisticated pseudo-random probing sequence.
*   **Compact Dicts (Python 3.6+):** Python now maintains an "indices" array and a separate "entries" array. This makes dictionaries significantly more memory-efficient and **preserves insertion order**.

| Operation | Syntax | Performance |
| :--- | :--- | :--- |
| **Insert** | `d[k] = v` | O(1) average. |
| **Lookup** | `d[k]` | O(1) average. |
| **Delete** | `del d[k]` | O(1) average. |
| **Items** | `.items()` | Returns a dynamic view of `(k, v)` pairs. |

## Comparison Table
| Feature | List | Tuple | Set | Dictionary |
| :--- | :--- | :--- | :--- | :--- |
| **Ordered** | Yes | Yes | No | Yes (3.7+) |
| **Mutable** | Yes | No | Yes | Yes |
| **Duplicates** | Yes | Yes | No | No (Keys) |
| **Use Case** | Sequence of data. | Fixed records. | Unique items. | Key-Value mapping. |
