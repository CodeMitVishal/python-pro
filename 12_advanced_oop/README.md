# Module 12 · Advanced OOP

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-12.pdf) · [Interview Q&A](INTERVIEW.md)

Design classes that feel built-in and stay easy to change: dunder methods, properties, class methods, the MRO, ABCs, Protocols, composition and SOLID.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Dunder methods | [`01_dunder_methods.py`](01_dunder_methods.py) | `__repr__`, `__eq__`, `__hash__`, `__add__`, `__len__`, `__getitem__` |
| Properties | [`02_properties.py`](02_properties.py) | validated and computed attributes, `__slots__` |
| Class & static methods | [`03_class_and_static_methods.py`](03_class_and_static_methods.py) | alternative constructors like `from_csv()` |
| Inheritance & the MRO | [`04_inheritance_and_mro.py`](04_inheritance_and_mro.py) | `super()`, the diamond, mixins |
| ABCs & Protocols | [`05_abc_and_protocols.py`](05_abc_and_protocols.py) | contracts: nominal vs structural typing |
| Composition & SOLID | [`06_composition_and_solid.py`](06_composition_and_solid.py) | dependency injection, testable design |
| Descriptors & metaclasses | [`07_descriptors_and_metaclasses.py`](07_descriptors_and_metaclasses.py) | how `@property` works, `__new__`, `__init_subclass__`, metaclasses |

```bash
python 12_advanced_oop/01_dunder_methods.py
```

## Exercise: A Vector that feels built-in

Make `+`, `*`, `abs()`, `==`, sets, unpacking and a read-only property work.

- Start here: [`exercises/ex12_vector.py`](../exercises/ex12_vector.py)
- Solution: [`solutions/ex12_vector.py`](../solutions/ex12_vector.py)

## Knowledge check

Preparing for interviews? Read the [Module 12 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 12 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 13 · Errors, context managers & logging](../13_errors_context_logging/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
