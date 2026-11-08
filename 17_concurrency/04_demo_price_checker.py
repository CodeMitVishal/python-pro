"""Module 17 · Demo: check prices in 30 "shops" at once with asyncio

Each shop answers after a random delay; some are down. We:
  - query all shops concurrently, max 10 at a time (Semaphore)
  - give each shop 1.0 s (wait_for), so one slow shop can't block everything
  - keep going when a shop fails (return_exceptions=True)

Run it:  python 17_concurrency/04_demo_price_checker.py
"""
import asyncio
import random
import time

random.seed(3)
SHOPS = [f"shop-{i:02d}" for i in range(30)]


async def get_price(shop):
    delay = random.uniform(0.1, 1.2)
    await asyncio.sleep(delay)                 # pretend network latency
    if random.random() < 0.1:
        raise ConnectionError(f"{shop} is down")
    return shop, round(random.uniform(18, 25), 2)


async def checked(shop, limit):
    async with limit:
        return await asyncio.wait_for(get_price(shop), timeout=1.0)


async def main():
    limit = asyncio.Semaphore(10)
    start = time.perf_counter()
    results = await asyncio.gather(*(checked(s, limit) for s in SHOPS), return_exceptions=True)
    took = time.perf_counter() - start

    prices = [r for r in results if not isinstance(r, Exception)]
    timeouts = sum(isinstance(r, TimeoutError) for r in results)
    errors = sum(isinstance(r, ConnectionError) for r in results)
    shop, best = min(prices, key=lambda p: p[1])

    print(f"asked {len(SHOPS)} shops in {took:.1f} s (one by one would take ~{len(SHOPS) * 0.8:.0f} s)")
    print(f"answers: {len(prices)}, timeouts: {timeouts}, errors: {errors}")
    print(f"cheapest: {shop} at {best} EUR")


asyncio.run(main())
