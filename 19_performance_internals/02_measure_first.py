"""Module 19 · Measure first: timeit and cProfile

Rule #1 of performance: DON'T GUESS. Programs usually spend 90% of their
time in 10% of the code. Find that 10% with a profiler, fix it, measure again.

  timeit   -> compare small snippets precisely
  cProfile -> see which functions take the time in a whole program

Run it:  python 19_performance_internals/02_measure_first.py
Profile any script yourself:  python -m cProfile -s cumtime your_script.py
"""
import cProfile
import io
import pstats
import timeit

# --- 1. timeit: run a snippet many times, report the total ---------------------------
setup = "words = ['python'] * 10_000"
t_plus = timeit.timeit("s = ''\nfor w in words: s += w", setup=setup, number=100)
t_join = timeit.timeit("''.join(words)", setup=setup, number=100)
print(f"+= in a loop: {t_plus * 10:.2f} ms per run")
print(f"''.join():    {t_join * 10:.2f} ms per run   ({t_plus / t_join:.0f}x faster)")


# --- 2. cProfile: where does a program spend its time? --------------------------------------
def load_orders():
    return [{"id": i, "customer": f"c{i % 500}", "total": i % 97} for i in range(60_000)]


def slow_unique_customers(orders):
    seen = []
    for o in orders:
        if o["customer"] not in seen:      # O(n) search in a list, for every order
            seen.append(o["customer"])
    return seen


def report():
    orders = load_orders()
    customers = slow_unique_customers(orders)
    revenue = sum(o["total"] for o in orders)
    return len(customers), revenue


profiler = cProfile.Profile()
profiler.enable()
report()
profiler.disable()

out = io.StringIO()
pstats.Stats(profiler, stream=out).sort_stats("cumulative").print_stats(5)
print("\n".join(line for line in out.getvalue().splitlines() if "(" in line or "ncalls" in line)[:900])
# Read it: "cumtime" = time inside the function INCLUDING what it calls.
# slow_unique_customers is the hotspot -> fix it with a set (see lesson 03).
