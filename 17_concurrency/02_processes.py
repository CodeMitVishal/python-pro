"""Module 17 · Processes: use ALL your CPU cores for heavy calculation

The GIL (Global Interpreter Lock) lets only ONE thread run Python bytecode at
a time in a process. So for CPU-bound work, 8 threads are no faster than 1.

A separate PROCESS has its own interpreter and its own GIL, so 8 processes
really run on 8 cores. The cost: starting a process is slower, and data must
be copied (pickled) between processes.

Run it:  python 17_concurrency/02_processes.py
"""
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def count_primes(limit):
    """Deliberately slow, pure-Python CPU work."""
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    return count


def timed(label, func):
    start = time.perf_counter()
    result = func()
    print(f"{label:<14} {time.perf_counter() - start:5.2f} s   {result}")


if __name__ == "__main__":      # REQUIRED for processes on Windows/macOS: each worker
    #                             re-imports this file, and must not start new pools itself
    jobs = [300_000] * 4
    print(f"CPU cores: {os.cpu_count()}")

    timed("sequential", lambda: [count_primes(j) for j in jobs])

    with ThreadPoolExecutor(max_workers=4) as pool:
        timed("4 threads", lambda: list(pool.map(count_primes, jobs)))   # no faster (even slower): the GIL

    with ProcessPoolExecutor(max_workers=4) as pool:
        timed("4 processes", lambda: list(pool.map(count_primes, jobs)))  # much faster

# Cheat sheet:
#   waiting (network, disk, DB)  -> threads or asyncio
#   calculating (maths, images)  -> processes (or NumPy, which releases the GIL)
