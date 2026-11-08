# Module 17 · Concurrency

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-17.pdf) · [Interview Q&A](INTERVIEW.md)

Do many things at once: threads for waiting, processes for calculating, asyncio for thousands of network tasks, and the GIL explained.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Threads | [`01_threads.py`](01_threads.py) | 4 s → 0.5 s; race conditions and locks |
| Processes | [`02_processes.py`](02_processes.py) | the GIL, and real multi-core speed-ups |
| asyncio | [`03_asyncio_basics.py`](03_asyncio_basics.py) | `async`/`await`, `gather`, timeouts, semaphores |
| Demo: price checker | [`04_demo_price_checker.py`](04_demo_price_checker.py) | 30 shops concurrently, with limits and timeouts |
| TaskGroup, queues, async HTTP | [`05_taskgroups_and_queues.py`](05_taskgroups_and_queues.py) | structured concurrency, backpressure, `httpx.AsyncClient` |

```bash
python 17_concurrency/01_threads.py
```

## Exercise: Parallel downloads

Download 10 files in under 1 s with threads AND asyncio, then count words with processes.

- Start here: [`exercises/ex17_parallel_downloads.py`](../exercises/ex17_parallel_downloads.py)
- Solution: [`solutions/ex17_parallel_downloads.py`](../solutions/ex17_parallel_downloads.py)

## Knowledge check

Preparing for interviews? Read the [Module 17 interview questions](INTERVIEW.md): short answers you can say out loud.

Test yourself with the [Module 17 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 18 · Data, APIs & databases](../18_data_apis_databases/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
