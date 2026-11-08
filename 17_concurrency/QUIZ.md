# Python Pro – Module 17 Knowledge Check
**Concurrency: threads, processes, asyncio**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. What is "I/O-bound" work?**
- A) Heavy maths
- B) Work that mostly waits for the network, disk or a database
- C) Printing to the screen only
- D) Work with no input

**2. What does the GIL do in CPython?**
- A) Speeds up threads
- B) Lets only one thread run Python bytecode at a time within a process
- C) Blocks the network
- D) Manages memory for processes

**3. You need to download 100 web pages. Best choice?**
- A) Processes
- B) Threads or asyncio
- C) A single loop
- D) Recursion

**4. You need to resize 1,000 images in pure Python. Best choice?**
- A) Threads
- B) Processes (`ProcessPoolExecutor`)
- C) asyncio
- D) A bigger `sleep`

**5. What is a race condition?**
- A) A fast program
- B) Threads changing shared data at the same time, so updates get lost
- C) A deadlock
- D) A test that runs twice

**6. How do you protect shared data between threads?**
- A) `time.sleep()`
- B) A `threading.Lock` (`with lock:`)
- C) A global variable
- D) `print()`

**7. Why do process pools need `if __name__ == "__main__":` on Windows?**
- A) Speed
- B) Workers re-import the file, and must not start new pools themselves
- C) It's style only
- D) It isn't needed

**8. Inside `async def`, what does `await asyncio.sleep(1)` do?**
- A) Freezes the whole program for 1 s
- B) Pauses this coroutine and lets others run meanwhile
- C) Starts a thread
- D) Nothing

**9. What happens if you call `time.sleep(5)` inside a coroutine?**
- A) The same as `asyncio.sleep`
- B) It blocks the whole event loop: no other task runs
- C) It raises an error
- D) It runs in the background

**10. What does `asyncio.gather(a(), b(), c())` do?**
- A) Runs them one by one
- B) Runs them concurrently and returns the results in order
- C) Returns the fastest result only
- D) Cancels them

**11. Why use an `asyncio.Semaphore(10)`?**
- A) To stop the program
- B) To limit how many tasks run at once
- C) To make tasks faster
- D) To retry failures

**12. Which call gives up on a slow coroutine after 2 seconds?**
- A) `asyncio.sleep(2)`
- B) `asyncio.wait_for(coro, timeout=2)`
- C) `time.timeout(2)`
- D) `gather(timeout=2)`

---

### Part B – Estimate the time

**13.** 8 downloads of 0.5 s each, run with `ThreadPoolExecutor(max_workers=8)`. About how long?

**14.**
```python
async def main():
    await job(1)        # each job sleeps with asyncio.sleep(1)
    await job(1)
    await asyncio.gather(job(1), job(1), job(1))
```
About how long does `asyncio.run(main())` take?

---

### Part C – Fix it

**15.** This crawler is no faster than a normal loop. Why?
```python
async def get(url):
    return requests.get(url).text      # requests is a blocking library
```

**16.** This counter shared by 4 threads ends up below 4,000. Fix it:
```python
def add():
    global counter
    for _ in range(1000):
        counter += 1
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Waiting, not calculating. | `01_threads.py` |
| 2 | B | That's why threads don't speed up CPU work. | `02_processes.py` |
| 3 | B | Overlap the waiting. | `01_threads.py`, `03_asyncio_basics.py` |
| 4 | B | Each process has its own GIL. | `02_processes.py` |
| 5 | B | Read-modify-write gets interleaved. | `01_threads.py` |
| 6 | B | Only one thread at a time inside `with lock`. | `01_threads.py` |
| 7 | B | Windows starts processes by re-importing. | `02_processes.py` |
| 8 | B | It yields to the event loop. | `03_asyncio_basics.py` |
| 9 | B | Use `await asyncio.sleep()`. | `03_asyncio_basics.py` |
| 10 | B | Concurrent, results in input order. | `03_asyncio_basics.py` |
| 11 | B | Be polite to servers. | `04_demo_price_checker.py` |
| 12 | B | Raises `TimeoutError`. | `03_asyncio_basics.py` |
| 13 | ~0.5 s | All 8 wait at the same time. | `01_threads.py` |
| 14 | ~3 s | 1 + 1 + 1 (the gather runs in parallel). | `03_asyncio_basics.py` |
| 15 | `requests.get` blocks the event loop. Use an async client (aiohttp, httpx), or threads. | | `03_asyncio_basics.py` |
| 16 | Create `lock = threading.Lock()` and do `with lock: counter += 1`. | | `01_threads.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
