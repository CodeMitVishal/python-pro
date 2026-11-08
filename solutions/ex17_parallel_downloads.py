"""Solution · Exercise 17: Download 10 files fast

Run it:  python solutions/ex17_parallel_downloads.py
"""
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def slow_download(url):
    time.sleep(0.3)
    return f"<{url}>"


async def async_download(url):
    await asyncio.sleep(0.3)
    return f"<{url}>"


def count_words(text):
    return len(text.split())


def download_all_threads(urls):
    # I/O-bound: threads overlap the waiting. map() keeps the input order.
    with ThreadPoolExecutor(max_workers=len(urls) or 1) as pool:
        return list(pool.map(slow_download, urls))


async def download_all_async(urls):
    # gather runs all coroutines concurrently and returns results in input order
    return list(await asyncio.gather(*(async_download(u) for u in urls)))


def count_words_parallel(texts):
    # CPU-bound: separate processes sidestep the GIL. count_words must be a
    # top-level function so it can be sent (pickled) to the worker processes.
    with ProcessPoolExecutor() as pool:
        return sum(pool.map(count_words, texts))


if __name__ == "__main__":
    urls = [f"file{i}" for i in range(10)]
    expected = [f"<file{i}>" for i in range(10)]

    start = time.perf_counter()
    assert download_all_threads(urls) == expected
    t1 = time.perf_counter() - start
    assert t1 < 1.0

    start = time.perf_counter()
    assert asyncio.run(download_all_async(urls)) == expected
    t2 = time.perf_counter() - start
    assert t2 < 1.0

    assert count_words_parallel(["a b c", "d e", "f"]) == 6
    print(f"threads: {t1:.2f} s, asyncio: {t2:.2f} s")
    print("All checks passed!")
