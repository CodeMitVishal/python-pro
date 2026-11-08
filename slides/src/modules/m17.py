"""Slides · Module 17 · Concurrency"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 17 · Concurrency"
SLIDES = [
 cover("17", "Concurrency", "Threads, processes and asyncio: when each one helps, and the GIL question every interview asks.",
       [("Threads", "01_threads.py"), ("Processes", "02_processes.py"), ("asyncio basics", "03_asyncio_basics.py"),
        ("Demo: 30 shops at once", "04_demo_price_checker.py"), ("TaskGroup &amp; queues", "05_taskgroups_and_queues.py"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Concurrency", "Most programs spend their time waiting",
     "Your script checks prices in <b>30 online shops</b>. Each request takes 1 second, and 0.99 s of that is <b>waiting</b> for the network.<br><br>"
     "One after another: <b>30 seconds</b>. The CPU is idle the whole time.",
     "Start all 30 requests, then wait for them <b>together</b>: about <b>1 second</b>. That's concurrency."),

 picture(M, "Concurrency", "I/O-bound vs CPU-bound",
     "&#127859; A cook with 3 pots: while water boils (<b>waiting</b>), she chops vegetables. That's <b>concurrency</b>: one person, many tasks. "
     "Three cooks chopping at the same time is <b>parallelism</b>: more hands, more work done.",
     [("I/O-bound", "network, disk, DB: mostly waiting"), ("use", "asyncio or threads"),
      ("CPU-bound", "maths, images, parsing: busy CPU"), ("use", "processes (all cores)")]),

 trace(M, "The GIL", "The GIL in one slide", ["", "Threads", "Processes", "asyncio"],
       [["Runs Python code in parallel?", "<b>no</b> (one thread at a time, the GIL)", "<b>yes</b>, one per core", "no (one thread)"],
        ["Good for", "waiting: HTTP, files, DB", "heavy CPU work", "<b>thousands</b> of waits"],
        ["Cost per task", "~MBs (an OS thread)", "high (a whole interpreter)", "tiny (a coroutine)"],
        ["Shared memory?", "yes: needs <b>locks</b>", "no: data is copied (pickled)", "yes, but switches only at <b>await</b>"],
        ["Tool", "<span class=\"m\">ThreadPoolExecutor</span>", "<span class=\"m\">ProcessPoolExecutor</span>", "<span class=\"m\">asyncio.gather / TaskGroup</span>"]],
       "The <b>GIL</b> (Global Interpreter Lock) is released while a thread waits for I/O, so threads still help with waiting. Python 3.13+ has an experimental free-threaded build."),

 code_out(M, "Threads", "30 seconds become 1 second", '''
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_price(shop):
    time.sleep(1)                       # pretend network wait
    return shop, 19.99

shops = [f"shop{i}" for i in range(30)]

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=30) as pool:
    prices = list(pool.map(fetch_price, shops))
print(len(prices), "prices in", round(time.perf_counter() - start, 1), "s")''',
     steps=["<b>pool.map</b> runs the function in many threads.", "Sequential would take 30 s.",
            "Perfect for <b>requests</b>, file downloads, DB calls."]),

 mistake(M, "Threads", "Race condition: two threads, one counter",
     '''
balance = 0
def deposit():
    global balance
    for _ in range(100_000):
        balance += 1      # read, add, write:
                          # not atomic!
# 4 threads -> often LESS than 400,000''',
     "Two threads read the same old value, both add 1, both write it back: one deposit is <b>lost</b>. The bug appears randomly.",
     '''
import threading
lock = threading.Lock()
def deposit():
    global balance
    for _ in range(100_000):
        with lock:        # one thread at a time
            balance += 1
# always 400,000''',
     "Protect shared data with a <b>Lock</b>, or avoid sharing: give each thread its own data and combine the results."),

 code_out(M, "Processes", "Use every CPU core", '''
import time
from concurrent.futures import ProcessPoolExecutor

def count_primes(limit):
    return sum(all(n % d for d in range(2, int(n ** .5) + 1))
               for n in range(2, limit))

if __name__ == "__main__":              # required for processes!
    jobs = [200_000] * 4
    start = time.perf_counter()
    [count_primes(j) for j in jobs]
    one = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor() as pool:
        list(pool.map(count_primes, jobs))
    many = time.perf_counter() - start
    print(f"1 process : {one:.1f} s")
    print(f"processes : {many:.1f} s")''',
     steps=["Each process has its own interpreter and its own GIL.", "Arguments and results are <b>pickled</b> between processes.",
            "The <b>__main__</b> guard is required on Windows and macOS."]),

 picture(M, "asyncio", "async / await: one thread, many waits",
     "&#127861; A <b>barista</b> takes your order, starts the machine, and while it runs takes the next order. "
     "<b>await</b> = \"I'm waiting here, serve someone else meanwhile\". The <b>event loop</b> is the barista.",
     [("async def fetch()", "defines a coroutine"), ("await sleep / http", "pause and give control back"),
      ("event loop", "runs whoever is ready"), ("gather / TaskGroup", "wait for many at once")]),

 code_out(M, "asyncio", "Check 30 shops on one thread", '''
import asyncio
import time

async def fetch_price(shop):
    await asyncio.sleep(1)                 # non-blocking wait
    return shop, 19.99

async def main():
    shops = [f"shop{i}" for i in range(30)]
    async with asyncio.TaskGroup() as tg:  # 3.11+
        tasks = [tg.create_task(fetch_price(s)) for s in shops]
    return [t.result() for t in tasks]

start = time.perf_counter()
prices = asyncio.run(main())
print(len(prices), "prices in", round(time.perf_counter() - start, 1), "s")''',
     steps=["<b>asyncio.run</b> starts the event loop.", "<b>TaskGroup</b>: if one task fails, the others are cancelled.",
            "Real HTTP: <b>httpx.AsyncClient</b> or aiohttp, not requests."]),

 mistake(M, "asyncio", "Blocking the event loop",
     '''
async def handler():
    data = requests.get(URL)     # blocks!
    time.sleep(2)                # blocks!
    return data.json()''',
     "A blocking call freezes the <b>whole</b> event loop: every other request in your FastAPI app waits too.",
     '''
async def handler():
    async with httpx.AsyncClient() as c:
        data = await c.get(URL)
    await asyncio.sleep(2)
    return data.json()
# or: await asyncio.to_thread(blocking_func)''',
     "In <b>async def</b>, only use awaitable libraries. Wrap old blocking code with <b>asyncio.to_thread</b>."),

 job(M, "Concurrency", "Concurrency at work", [
     ("FastAPI endpoints", '''
@app.get("/quote")
async def quote():
    return await pricing_client.get_quote()'''),
     ("Call several services in parallel", '''
user, orders = await asyncio.gather(
    users_api.get(uid), orders_api.list(uid))'''),
     ("Background jobs (Module 26)", '''
send_email.delay(order_id)    # Celery worker'''),
     ("Batch CPU work", '''
with ProcessPoolExecutor() as pool:
    pool.map(resize_image, paths)'''),
 ]),

 interview(M, "What is the GIL? Does Python support multithreading?",
     ["The <b>Global Interpreter Lock</b> lets only <b>one thread run Python bytecode at a time</b> in CPython.",
      "It keeps reference counting simple and safe, but stops threads using several cores for <b>pure Python CPU work</b>.",
      "Threads <b>still help for I/O</b>: the GIL is released while waiting for the network or disk.",
      "For CPU work: <b>multiprocessing</b>, or C extensions like NumPy that release the GIL.",
      "Python 3.13+ offers an experimental <b>free-threaded</b> (no-GIL) build."],
     None,
     "\"Threads vs processes vs asyncio: which would you use for a web scraper? For image resizing?\" (scraper: asyncio or threads; resizing: processes)."),

 interview(M, "How does async/await work?",
     ["<b>async def</b> creates a <b>coroutine</b>; calling it doesn't run it yet.",
      "<b>await</b> pauses the coroutine until the awaited thing is done and gives control back to the <b>event loop</b>.",
      "The event loop runs whichever coroutine is ready, so one thread can handle thousands of waiting connections.",
      "It's <b>cooperative</b>: one blocking call freezes everyone.",
      "Run many with <b>asyncio.gather</b> or a <b>TaskGroup</b>."],
     '''
async def main():
    async with asyncio.TaskGroup() as tg:
        a = tg.create_task(get_user(1))
        b = tg.create_task(get_orders(1))
    return a.result(), b.result()''',
     "\"What is a race condition and how do you prevent it?\" (unsynchronised access to shared state; use locks, queues, or don't share state)."),

 recap(M, "Module 17 in 6 lines",
     ["Waiting (I/O) &#8594; <b>asyncio</b> or <b>threads</b>. Computing (CPU) &#8594; <b>processes</b>.",
      "The <b>GIL</b>: one thread runs Python at a time, but it's released during I/O.",
      "<b>ThreadPoolExecutor</b> / <b>ProcessPoolExecutor</b>: the easy, high-level APIs.",
      "Shared data + threads = race conditions; use a <b>Lock</b> or don't share.",
      "<b>async/await</b>: one thread, an event loop, thousands of tasks; <b>TaskGroup</b> to run many.",
      "Never block inside <b>async def</b>; use <b>asyncio.to_thread</b>."],
     "Do <b>exercises/ex17_parallel_downloads.py</b>: make 20 slow downloads finish in about 1 second."),
]
