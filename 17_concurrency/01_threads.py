"""Module 17 · Threads: do many WAITING tasks at the same time

Most programs spend their time WAITING: for the network, a disk, a database.
That's "I/O-bound" work. While one thread waits, another can run, so threads
make I/O-bound programs much faster.

(For heavy CALCULATION, "CPU-bound" work, threads don't help in CPython
because of the GIL; use processes instead -> lesson 02.)

Run it:  python 17_concurrency/01_threads.py
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def download(name):
    time.sleep(0.5)                      # pretend to wait 0.5 s for the network
    return f"{name}: done"


files = [f"file{i}.csv" for i in range(8)]

# --- 1. One after another: 8 x 0.5 s = 4 s ---------------------------------------------
start = time.perf_counter()
results = [download(f) for f in files]
print(f"sequential: {time.perf_counter() - start:.1f} s")

# --- 2. A thread pool: all 8 wait at the same time = ~0.5 s ------------------------------
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(download, files))      # same order as the input
print(f"8 threads:  {time.perf_counter() - start:.1f} s  -> {results[0]}")

# --- 3. The danger: a RACE CONDITION when threads share data -----------------------------
counter = 0

def unsafe_add(n):
    global counter
    for _ in range(n):
        value = counter                  # read...
        time.sleep(0)                    # (let another thread run in between)
        counter = value + 1              # ...write: another thread may have changed it!

threads = [threading.Thread(target=unsafe_add, args=(1000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()               # wait for all of them to finish
print(f"without a lock: {counter} (expected 4000)")   # usually far less: updates got lost

# --- 4. The fix: a Lock lets only ONE thread into the critical section at a time --------
counter = 0
lock = threading.Lock()

def safe_add(n):
    global counter
    for _ in range(n):
        with lock:                       # acquire... and always release, even on errors
            value = counter
            time.sleep(0)
            counter = value + 1

threads = [threading.Thread(target=safe_add, args=(1000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"with a lock:    {counter} (expected 4000)")
