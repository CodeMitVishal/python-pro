# Python Pro – Module 12 Knowledge Check
**Advanced OOP**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. Which method does `print(obj)` use first?**
- A) `__repr__`
- B) `__str__`
- C) `__print__`
- D) `__format__`

**2. What should `__eq__` return when it can't compare with the other type?**
- A) `False`
- B) `None`
- C) `NotImplemented`
- D) Raise `TypeError`

**3. You define `__eq__`. What else must you define so objects work in sets and as dict keys?**
- A) `__lt__`
- B) `__hash__`
- C) `__len__`
- D) Nothing

**4. Which single method makes `obj[i]`, slicing AND `for x in obj` work?**
- A) `__iter__`
- B) `__getitem__`
- C) `__contains__`
- D) `__call__`

**5. What does `@property` let you do?**
- A) Make a method run in the background
- B) Run code when an attribute is read or set, while it still looks like a normal attribute
- C) Make a class abstract
- D) Cache a method

**6. What's a typical use of `@classmethod`?**
- A) Helper functions with no access to anything
- B) Alternative constructors like `from_csv()`
- C) Making attributes private
- D) Defining abstract methods

**7. `Manager.from_csv(...)` is a classmethod inherited from `Employee`. What does it return?**
- A) An `Employee`
- B) A `Manager`, because `cls` is `Manager`
- C) A string
- D) An error

**8. In multiple inheritance, what does `super()` call?**
- A) Always the first parent
- B) The next class in the MRO
- C) The `object` class
- D) All parents at once

**9. What happens when you create an object of an ABC subclass that didn't implement an `@abstractmethod`?**
- A) It works, and the method returns `None`
- B) `TypeError` when you create it
- C) A warning
- D) An error only when you call the method

**10. What's the key difference between `Protocol` and `ABC`?**
- A) There is none
- B) A Protocol matches any class with the right methods, with no inheritance needed
- C) A Protocol is faster
- D) An ABC can't have methods

**11. "Depend on an abstraction and pass the details in" is which SOLID principle?**
- A) Single responsibility
- B) Open/closed
- C) Liskov substitution
- D) Dependency inversion

**12. A `Car` has an `Engine`. Inheritance or composition?**
- A) `class Car(Engine)`
- B) Composition: `self.engine = Engine()`
- C) Multiple inheritance
- D) A mixin

---

### Part B – What's the output?

**13.**
```python
class A:
    def hi(self): return "A"
class B(A):
    def hi(self): return "B" + super().hi()
class C(A):
    def hi(self): return "C" + super().hi()
class D(B, C):
    def hi(self): return "D" + super().hi()
print(D().hi())
```

**14.**
```python
class Box:
    def __init__(self, *items): self.items = list(items)
    def __len__(self): return len(self.items)
    def __bool__(self): return len(self) > 0
print(len(Box(1, 2)), bool(Box()))
```

---

### Part C – Fix it

**15.** `t.celsius = -500` should raise `ValueError`, but nothing happens. Fix it with a property:
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
```

**16.** `2 * Money(5)` raises `TypeError`, but `Money(5) * 2` works. What's missing?

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | `__str__` for users; `__repr__` is the fallback. | `01_dunder_methods.py` |
| 2 | C | It lets Python try the other side. | `01_dunder_methods.py` |
| 3 | B | Equal objects must have equal hashes. | `01_dunder_methods.py` |
| 4 | B | Python falls back to indexing 0, 1, 2… for loops. | `01_dunder_methods.py` |
| 5 | B | Getter/setter behind normal attribute syntax. | `02_properties.py` |
| 6 | B | `cls(...)` builds an object a different way. | `03_class_and_static_methods.py` |
| 7 | B | `cls` is the class it was called on. | `03_class_and_static_methods.py` |
| 8 | B | That's how cooperative classes and mixins work. | `04_inheritance_and_mro.py` |
| 9 | B | ABCs block creation until every abstract method exists. | `05_abc_and_protocols.py` |
| 10 | B | Structural ("duck") typing. | `05_abc_and_protocols.py` |
| 11 | D | Inject the notifier or discount instead of hard-coding it. | `06_composition_and_solid.py` |
| 12 | B | HAS-A → composition. | `06_composition_and_solid.py` |
| 13 | `DBCA` | MRO: D → B → C → A. | `04_inheritance_and_mro.py` |
| 14 | `2 False` | `__len__` and `__bool__`. | `01_dunder_methods.py` |
| 15 | Add `@property def celsius` returning `self._celsius`, and `@celsius.setter` that validates, then sets `self._celsius`. | `__init__` goes through the setter. | `02_properties.py` |
| 16 | `__rmul__` (for example `__rmul__ = __mul__`). | Python tries `int.__mul__`, then `Money.__rmul__`. | `ex12_vector.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
