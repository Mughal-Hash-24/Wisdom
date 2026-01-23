---
created: 2026-01-22 14:15
tags: [concept, python, oop]
related: [[Python_OOP_Mechanics]]
---
# Advanced Polymorphism and Inheritance

[[T.O.C (Python)|Up to Python]]

## 1. The `super()` Proxy Object
In C++, `Base::method()` calls the parent directly.
In Python, `super()` does **not** simply return the parent class. It returns a **Proxy Object** that delegates method calls based on the **MRO** (Method Resolution Order).

### How it Works (The Internals)
`super()` is actually `super(CurrentClass, self)`.
1.  It looks at `self.__class__.__mro__`.
2.  It finds `CurrentClass` in that list.
3.  It picks the **next** class in the list.
4.  It binds the method call to `self` (the instance).

**Why this matters:**
In multiple inheritance (Diamond Problem), `super()` ensures that common base classes are initialized **only once**.
```python
class Base: 
    def __init__(self): print("Base init")

class A(Base): 
    def __init__(self): 
        print("A init")
        super().__init__()

class B(Base): 
    def __init__(self): 
        print("B init")
        super().__init__()

class C(A, B): 
    def __init__(self): 
        print("C init")
        super().__init__()

# C() Output: C init -> A init -> B init -> Base init
# Notice B is called even though A doesn't inherit from B. 
# That's because 'B' is 'A's successor in C's MRO.
```

## 2. Duck Typing vs. Protocols (Static Duck Typing)
*   **Classic Duck Typing (Runtime):** "I'll try to call `.quack()`. If it crashes, it crashes."
*   **Protocols (Python 3.8+):** Structural Subtyping. "I require a thing that *can* quack."

### `typing.Protocol`
This allows C++-style interface checking by static analysis tools (mypy) without enforcing inheritance at runtime.

```python
from typing import Protocol

class Quacker(Protocol):
    def quack(self) -> None: ...

def make_noise(duck: Quacker):
    duck.quack()

class Car:
    def quack(self): print("Honk") # Valid! Car implicitly implements Quacker.
```

## 3. Mixins: The "Behavior" Injection
A Mixin is a class designed **only** to add features to other classes via inheritance. It is not meant to be instantiated alone.
*   **Usage:** Adding `ToJSON` capability to Models.
*   **Pattern:** It doesn't use `super()` (usually) and holds no state.

```python
class JSONMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class User(JSONMixin):
    def __init__(self, name): self.name = name

u = User("Gemini")
print(u.to_json()) # {"name": "Gemini"}
```

## 4. Monkey Patching (Runtime Class Modification)
Because classes are mutable objects, you can modify them at runtime.
*   **Concept:** "Opening" a class and injecting a new method.
*   **Danger:** High. Can lead to "Spaghetti Code" where you don't know where a method came from.
*   **C++ Equivalent:** Impossible. Once compiled, the binary is sealed.

```python
# The standard library doesn't have this... let's add it.
def new_method(self):
    return "I am hacked in!"

MyClass.hack = new_method
obj = MyClass()
print(obj.hack())
```
