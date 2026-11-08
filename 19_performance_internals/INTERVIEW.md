# Module 19 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 19](README.md) · [Quiz](QUIZ.md)

---

### 1. How does Python manage memory?

**Say:** All values are objects on a private heap, and variables are references to them. CPython frees an object as soon as its **reference count** reaches zero. A **generational garbage collector** (`gc`) finds and frees **reference cycles**. Small objects use the pymalloc allocator. Small ints (−5..256) and some strings are cached.

---

### 2. Is Python pass-by-value or pass-by-reference?

**Say:** Neither exactly: it's **pass-by-object-reference** ("call by sharing"). The function receives a reference to the same object. Mutating it (`lst.append`) is visible to the caller. **Rebinding** the parameter (`lst = []`) is not.

---

### 3. What is a memory leak in Python, and how do you find it?

**Say:** Objects that stay referenced by accident: ever-growing module-level caches or lists, global registries, closures holding big objects, `lru_cache` on methods (it keeps `self`). Find them with `tracemalloc` snapshots (compare two), `objgraph`, or memory profiling in production.

---

### 4. How do you find what's slow?

**Say:** Measure, don't guess. Use `timeit` for micro-benchmarks, `cProfile` with `snakeviz` or `py-spy` (a sampling profiler that also works on live processes) to find hot functions, and APM tracing for web requests. Then fix the biggest bottleneck first.

---

### 5. Name optimisations that really matter.

**Say:** In order of impact:
1. A better **algorithm or data structure** (set lookup, dict index).
2. **Fewer I/O round trips** (batch queries, fix N+1).
3. **Caching**.
4. **Built-ins / C libraries** (NumPy, pandas).
5. **Concurrency** for waits.
6. Micro-tricks only in proven hot loops.

---

### 6. What is `__slots__`?

**Say:** A class attribute listing the allowed instance attributes. Instances then have no per-object `__dict__`, which saves a lot of memory with millions of objects and slightly speeds up attribute access. The downside: you can't add new attributes dynamically.

---

### 7. Why is NumPy faster than Python loops?

**Say:** NumPy arrays store raw numbers in contiguous memory with one type. Operations run as compiled C loops (vectorisation) without creating Python objects per element and without bytecode overhead. That's often a 10–100× speedup.

---

### 8. What is bytecode? What does `dis` show?

**Say:** CPython compiles source to **bytecode**, a list of instructions for its virtual machine, cached in `__pycache__/*.pyc`. The `dis` module shows these instructions, which helps you understand why, for example, a local variable lookup is faster than a global one.

---

### 9. What are weak references for?

**Say:** A `weakref` points to an object **without** keeping it alive. It's useful for caches and observer lists that shouldn't prevent garbage collection (`WeakValueDictionary`).

---

### 10. List comprehension vs `map` vs a loop: which is fastest?

**Say:** Comprehensions are usually faster than an explicit `append` loop because the loop runs in optimised bytecode. `map` with a built-in function can be equally fast; with a `lambda`, it's often slower. But readability comes first, and the difference rarely matters compared with I/O.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
