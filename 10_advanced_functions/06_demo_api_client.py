"""Module 10 · Demo: a resilient API client built from decorators

A fake weather API that is slow and sometimes fails. Instead of filling
every function with try/except, timing and caching code, we write three
decorators once and stack them:

  @log_calls   -> print each call and its result
  @retry(3)    -> try again on ConnectionError
  @lru_cache   -> don't call the API twice for the same city

Run it:  python 10_advanced_functions/06_demo_api_client.py
"""
import functools
import random
import time

random.seed(7)                     # same "random" failures every run


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"  {func.__name__}{args} -> {result}")
        return result
    return wrapper


def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    print(f"  ! attempt {attempt} failed, retrying...")
            raise ConnectionError("API unavailable")
        return wrapper
    return decorator


@log_calls
@functools.lru_cache(maxsize=32)
@retry(times=3)
def get_temperature(city):
    """Pretend to call a slow, flaky weather API."""
    time.sleep(0.2)
    if random.random() < 0.4:
        raise ConnectionError("timeout")
    return {"Augsburg": 14, "Mumbai": 31, "Oslo": 3}.get(city, 20)


start = time.perf_counter()
for city in ["Augsburg", "Mumbai", "Augsburg", "Oslo", "Mumbai"]:
    get_temperature(city)
print(f"\n5 lookups in {time.perf_counter() - start:.1f} s")
print(get_temperature.__wrapped__.cache_info())   # repeats came from the cache
