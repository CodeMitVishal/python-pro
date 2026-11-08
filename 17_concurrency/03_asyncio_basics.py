"""Module 17 · asyncio: thousands of waiting tasks on ONE thread

  async def f():   defines a COROUTINE: a function that can pause
  await x          "pause me here until x is ready, run something else meanwhile"
  asyncio.run(f()) starts the event loop, which juggles all the paused coroutines

Threads switch whenever the OS decides. asyncio switches ONLY at an `await`,
so there are far fewer race conditions, and 10,000 tasks are cheap.
The catch: everything must be async-aware (asyncio.sleep, aiohttp, asyncpg...).
One blocking call (time.sleep, requests.get) freezes the whole loop.

Run it:  python 17_concurrency/03_asyncio_basics.py
"""
import asyncio
import time


async def fetch(name, seconds):
    print(f"  start {name}")
    await asyncio.sleep(seconds)        # NOT time.sleep: this lets other tasks run
    print(f"  done  {name}")
    return f"{name} ({seconds}s)"


async def main():
    # --- 1. await one after another: 1 + 1 + 1 = 3 s ---------------------------------
    start = time.perf_counter()
    for n in ["a", "b", "c"]:
        await fetch(n, 1)
    print(f"one by one: {time.perf_counter() - start:.1f} s\n")

    # --- 2. gather: run them concurrently, ~1 s in total -------------------------------
    start = time.perf_counter()
    results = await asyncio.gather(fetch("x", 1), fetch("y", 1), fetch("z", 1))
    print(f"gather: {time.perf_counter() - start:.1f} s -> {results}\n")

    # --- 3. Timeouts: give up on slow tasks --------------------------------------------
    try:
        await asyncio.wait_for(fetch("slow", 5), timeout=0.5)
    except TimeoutError:
        print("slow task cancelled after 0.5 s\n")

    # --- 4. A Semaphore limits how many run at once (be polite to servers) ------------
    limit = asyncio.Semaphore(2)

    async def polite(name):
        async with limit:               # at most 2 inside at the same time
            return await fetch(name, 0.5)

    start = time.perf_counter()
    await asyncio.gather(*(polite(f"page{i}") for i in range(6)))
    print(f"6 pages, 2 at a time: {time.perf_counter() - start:.1f} s")   # ~1.5 s


asyncio.run(main())
