---
created: 2026-01-22 14:00
tags: [concept, python, oop, metaprogramming]
related: [[Python_OOP_Mechanics]]
---
# Advanced Python OOP & Metaprogramming

[[T.O.C (Python)|Up to Python]]

## 1. The "Everything is an Object" Rabbit Hole
In C++, a `class` is a compile-time blueprint. It disappears at runtime.
In Python, a `class` is **itself an object** (an instance of `type`) existing in memory at runtime.

### The Metaclass (`type`)
If an object is an instance of a Class, what is the Class an instance of? **A Metaclass.**
*   `x = 5` -> `x` is instance of `int`.
*   `int` -> `int` is instance of `type`.
*   `type` -> `type` is instance of `type` (Recursive self-reference).

**C++ Analogy:**
Think of Metaclasses as **Runtime Template Metaprogramming**. In C++, you use templates to generate code at compile time. In Python, you use Metaclasses to hook into the **creation of the class definition itself** at runtime.

```python
class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"Allocating memory for class: {name}")
        return super().__new__(cls, name, bases, dct)

class Dog(metaclass=Meta): # Logic runs when THIS line is executed, not when Dog() is called.
    pass
```

---

## 2. Slots (`__slots__`): Returning to C++ Structs
By default, every Python object stores its attributes in a dictionary `self.__dict__`.
*   **Pros:** Dynamic (add fields at runtime).
*   **Cons:** Heavy RAM usage (Hash Tables are sparse).
*   **Solution:** `__slots__` tells Python: "I promise I will ONLY have these fields."

```python
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
```
*   **Memory Layout:** Python allocates a static C-struct-like array of pointers for `x` and `y`. No Hash Table.
*   **Impact:** Reduces memory footprint by ~50-60% for millions of small objects.
*   **Restriction:** You cannot do `p.z = 10` later. It will crash (AttributeError).

---

## 3. Descriptors: The Logic Behind `.`
How does `obj.x` actually work? It's not just a simple lookup. It triggers the **Descriptor Protocol**.
If an object defines `__get__`, `__set__`, or `__delete__`, it overrides default attribute access.

### The `@property` Magic
The built-in `@property` is just a Descriptor.
```python
class TenaciousInt:
    def __get__(self, obj, objtype=None):
        return 10  # Always returns 10, no matter what.

class A:
    x = TenaciousInt()

a = A()
print(a.x) # 10
```
**Mechanism:**
1.  Python sees `a.x`.
2.  It looks up `x` in `A`.
3.  It sees `x` implements `__get__`.
4.  It calls `TenaciousInt.__get__(x, a, A)`.

---

## 4. MRO (Method Resolution Order): C3 Linearization
With Multiple Inheritance, how does Python decide which parent to call?
*   **Old Python (Pre-2.3):** Depth-First Search. (Failed for Diamond patterns).
*   **Modern Python:** **C3 Linearization Algorithm**.

### The Algorithm
It enforces two constraints:
1.  **Children before Parents:** Subclasses are checked before base classes.
2.  **Order Preservation:** If you write `class C(A, B)`, `A` is always checked before `B`.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
# D -> B -> C -> A -> Object
```
*   **Diagnostic:** Use `D.mro()` or `D.__mro__` to inspect the linearized path.

---

## 5. Abstract Base Classes (ABCs)
Python's version of C++ "Pure Virtual Functions".
*   **Module:** `abc`
*   **Usage:**
    ```python
    from abc import ABC, abstractmethod

    class Shape(ABC):
        @abstractmethod
        def area(self):
            pass
    ```
*   **Enforcement:** Python forbids instantiating `Shape()`. It throws a `TypeError` at runtime if you try. It also throws an error if a subclass fails to implement `area`.
