---
created: 2026-01-22 12:35
tags:
- field/cs
- subject/programming/python
- concept/python/oop
related:
- - Python_Execution_and_Memory_Model
---
# Python OOP Mechanics

[[T.O.C (Python)|Up to Python]]

## The Philosophy of Python OOP
In C++, OOP is enforced by the compiler. In Python, it is a runtime convention. Python follows **Duck Typing**: "If it walks like a duck and quacks like a duck, I'll treat it like a duck."

## 1. Constructors & Initialization
*   `__new__(cls)`: The actual constructor. It allocates the memory for the object.
*   `__init__(self)`: The initializer. It sets the initial state (attributes).
*   **Self:** Unlike C++'s implicit `this`, `self` must be explicitly named as the first parameter of every instance method. It represents the specific instance being operated on.

## 2. Operator Overloading (Magic Methods)
Python uses "Dunder" (Double Underscore) methods to hook into language operators.

| Category | Method | C++ Equivalent |
| :--- | :--- | :--- |
| **Arithmetic** | `__add__`, `__sub__` | `operator+`, `operator-` |
| **Comparison** | `__eq__`, `__lt__` | `operator==`, `operator<` |
| **String Rep** | `__str__`, `__repr__` | `ostream <<` |
| **Container** | `__getitem__`, `__len__`| `operator[]`, `.size()` |

**Example:**
```python
class ComplexNumber:
    def __init__(self, r, i):
        self.r = r
        self.i = i
    
    def __add__(self, other):
        return ComplexNumber(self.r + other.r, self.i + other.i)
```

## 3. Relationships: Composition, Aggregation, Inheritance

### Inheritance (Is-A)
```python
class Animal:
    def speak(self): pass

class Dog(Animal):
    def speak(self): print("Woof")
```
*   **Multiple Inheritance:** Python supports it. It uses the **C3 Linearization (MRO - Method Resolution Order)** to determine which method to call in complex diamond patterns.

### Composition & Aggregation (Has-A)
*   **Composition:** The child cannot exist without the parent.
    `class House: def __init__(self): self.room = Room()`
*   **Aggregation:** The child exists independently.
    `class Department: def __init__(self, teacher): self.teacher = teacher`

## 4. Polymorphism: Python vs C++
*   **C++:** Static Polymorphism (Templates) or Dynamic Polymorphism (Virtual Functions/V-Tables). You must have a common base class.
*   **Python:** **Duck Typing.**
    ```python
    def make_it_fly(thing):
        thing.fly() # I don't care what 'thing' is, as long as it has a fly() method.
    ```
*   **Benefit:** Extremely flexible. You can swap a `Mock` object for a real `Database` object in tests without any interface boilerplate.
*   **Risk:** Runtime `AttributeError` if the object doesn't have the method.
