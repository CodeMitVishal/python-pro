"""Module 17 · Structured concurrency: TaskGroup, producer/consumer queues, async HTTP

1. asyncio.TaskGroup (Python 3.11+): start many tasks; the `async with` block waits
   for ALL of them, and if one fails, the others are cancelled and you get an
   ExceptionGroup. Safer than loose create_task() calls that can be forgotten.
2. asyncio.Queue: producers put work in, a fixed number of workers take it out.
   This is backpressure: never more than N jobs in flight.
3. httpx.AsyncClient: a real async HTTP client (requests is blocking!).
   Here it talks to a fake transport, so the demo runs offline.

Run it:  python 17_concurrency/05_taskgroups_and_queues.py
"""
import asyncio
import random
import time

import httpx


# --- 1. TaskGroup: all or nothing ---------------------------------------------------------------
async def fetch(name: str, seconds: float, fail: bool = False) -> str:
    await asyncio.sleep(seconds)
    if fail:
        raise ConnectionError(f"{name} failed")
    return name


async def task_group_demo() -> None:
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch("users", 0.2))
        t2 = tg.create_task(fetch("orders", 0.3))
    print("both done:", t1.result(), t2.result())

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch("ok", 1.0))
            tg.create_task(fetch("broken", 0.1, fail=True))
    except* ConnectionError as group:
        print("failed fast:", [str(e) for e in group.exceptions], "(the slow task was cancelled)")


# --- 2. Producer / consumer with a bounded queue --------------------------------------------------
async def producer(queue: asyncio.Queue, n: int) -> None:
    for i in range(n):
        await queue.put(f"image-{i}")            # waits if the queue is full (backpressure)
    for _ in range(3):
        await queue.put(None)                    # one "stop" signal per worker


async def worker(name: str, queue: asyncio.Queue, done: list[str]) -> None:
    while (job := await queue.get()) is not None:
        await asyncio.sleep(random.uniform(0.05, 0.15))   # pretend: resize the image
        done.append(f"{job}@{name}")


async def queue_demo() -> None:
    queue: asyncio.Queue = asyncio.Queue(maxsize=5)
    done: list[str] = []
    start = time.perf_counter()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue, 12))
        for w in ("w1", "w2", "w3"):
            tg.create_task(worker(w, queue, done))
    print(f"12 jobs, 3 workers: {time.perf_counter() - start:.2f} s -> {done[:3]} ...")


# --- 3. Async HTTP: many requests concurrently, one shared client -----------------------------------
def fake_api(request: httpx.Request) -> httpx.Response:
    city = request.url.params["city"]
    return httpx.Response(200, json={"city": city, "temp": len(city) * 3})


async def http_demo() -> None:
    transport = httpx.MockTransport(fake_api)                 # real code: no transport argument
    async with httpx.AsyncClient(transport=transport, base_url="https://api.example.com",
                                 timeout=5) as client:
        cities = ["Augsburg", "Mumbai", "Oslo"]
        responses = await asyncio.gather(*(client.get("/weather", params={"city": c}) for c in cities))
        print({r.json()["city"]: r.json()["temp"] for r in responses})


async def main() -> None:
    await task_group_demo()
    await queue_demo()
    await http_demo()


random.seed(2)
asyncio.run(main())
