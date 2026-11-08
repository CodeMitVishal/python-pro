"""Exercise 17 · Download 10 files fast: threads AND asyncio

Each fake download takes 0.3 s. One after another, 10 files take 3 s.
Make both versions finish in well under 1 s, and keep the results in
the same order as the input.

  1. download_all_threads(urls): use ThreadPoolExecutor with slow_download
  2. download_all_async(urls):   use asyncio.gather with async_download
     (it's a coroutine: call it with asyncio.run(download_all_async(urls)))
  3. count_words_parallel(texts): CPU work. Count the words of each text in a
     ProcessPoolExecutor and return the total. (The checks only verify the
     result, but think about WHY processes fit this one and threads don't.)

Run it to check your work:
    python exercises/ex17_parallel_downloads.py

Stuck? Compare with solutions/ex17_parallel_downloads.py
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
    """TODO 1"""
    return [slow_download(u) for u in urls]          # sequential: too slow


async def download_all_async(urls):
    """TODO 2"""
    return [await async_download(u) for u in urls]   # sequential: too slow


def count_words_parallel(texts):
    """TODO 3"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    urls = [f"file{i}" for i in range(10)]
    expected = [f"<file{i}>" for i in range(10)]

    start = time.perf_counter()
    assert download_all_threads(urls) == expected
    t1 = time.perf_counter() - start
    assert t1 < 1.0, f"threads took {t1:.1f} s: download in parallel"

    start = time.perf_counter()
    assert asyncio.run(download_all_async(urls)) == expected
    t2 = time.perf_counter() - start
    assert t2 < 1.0, f"asyncio took {t2:.1f} s: use asyncio.gather"

    assert count_words_parallel(["a b c", "d e", "f"]) == 6
    print(f"threads: {t1:.2f} s, asyncio: {t2:.2f} s")
    print("All checks passed!")
