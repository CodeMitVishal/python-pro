# Module 11 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 11](README.md) · [Quiz](QUIZ.md)

---

### 1. Iterable vs iterator?

**Say:** An **iterable** is anything you can loop over: it has `__iter__` and returns a fresh iterator (list, str, dict, file). An **iterator** has `__next__`, remembers its position, raises `StopIteration` when it's done, and returns itself from `__iter__`. Iterators are single-use.

---

### 2. How does a `for` loop work under the hood?

**Say:** It calls `iter(obj)` once, then calls `next()` on that iterator again and again, binding each value to the loop variable. It stops when `StopIteration` is raised.

---

### 3. What is a generator? How is it different from a normal function?

**Say:** A function containing `yield`. Calling it doesn't run the body; it returns a **generator object**. Each `next()` runs until the next `yield`, hands out the value and **pauses**, keeping local state. A normal function runs to completion and returns once.

```python
def countdown(n):
    while n:
        yield n
        n -= 1
```

---

### 4. Why are generators memory-efficient?

**Say:** They produce values **on demand** and don't store the sequence. Summing 10 million numbers with `sum(x for x in range(10**7))` uses a few hundred bytes. The list version needs tens of megabytes.

---

### 5. How do you read a 10 GB file in Python?

**Say:** Never `read()` or `readlines()` it. Loop over the file object, which is a lazy iterator of lines, or read fixed-size chunks:

```python
with open("big.log") as f:
    for line in f:
        handle(line)

while chunk := f.read(1024 * 1024):   # binary data
    handle(chunk)
```

---

### 6. What does `yield from` do?

**Say:** It yields every value from another iterable or sub-generator, and it passes `send()` and exceptions through. It's the clean way to delegate, e.g. when walking a tree recursively.

---

### 7. What happens if you loop over a generator twice?

**Say:** The second loop gets **nothing**: the generator is exhausted. Create a new one, or store the results in a list if they fit in memory. It's a common silent bug (for example, `sum()` returns 0).

---

### 8. Name some useful `itertools` functions.

**Say:**
- `islice` slices any iterator.
- `chain` glues iterables together.
- `batched` (3.12+) splits into chunks.
- `groupby` groups **consecutive** equal keys, so sort first.
- `count` and `cycle` make endless sequences.
- `product`, `permutations` and `combinations` are for combinatorics.
- `accumulate` gives running totals.

---

### 9. How are generators used in web frameworks?

**Say:**
- **Streaming responses**: FastAPI `StreamingResponse` or Django `StreamingHttpResponse` send a CSV export row by row.
- **pytest fixtures**: setup, then `yield`, then teardown.
- **`@contextmanager`**: the same setup and teardown pattern.
- **Paginating** external APIs.

---

### 10. What are `send()` and async generators?

**Say:** `gen.send(value)` resumes a generator **and** passes a value in, so `x = yield result` makes it two-way (coroutines were built on this). An **async generator** uses `async def` with `yield`. You consume it with `async for`, which is ideal for streaming pages from an async HTTP API.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
