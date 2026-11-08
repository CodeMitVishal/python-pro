"""Module 11 · Two-way generators (.send) and async generators

1. gen.send(value) RESUMES a generator and makes `yield` RETURN that value.
   A generator can therefore keep state AND receive input: a "coroutine".
2. `async def` + `yield` = an ASYNC generator: it can `await` between items.
   Consume it with `async for`. Perfect for streaming: pages of an API,
   rows from an async database driver, messages from a queue.

TEACHING NOTES
  Why it matters  Two-way generators and async generators power coroutines and async streaming.
  Picture it      send() is a two-way radio: you hand a value in and get the next value out.
  Watch out       Prime a generator with next() before the first send(); async generators need
                  'async for'.
  In real jobs    Streaming paginated results from async HTTP APIs.
  Interview       Q: What is an async generator?
                  A: An 'async def' function with yield, consumed with 'async for'; ideal for
                     async streams.

Run it:  python 11_iterators_generators/06_send_and_async_generators.py
"""
import asyncio


# --- 1. A running average that you FEED with .send() ---------------------------------------
def averager():
    total = count = 0
    average = None
    while True:
        value = yield average          # hand out the average, receive the next value
        total += value
        count += 1
        average = total / count


avg = averager()
next(avg)                              # "prime" it: run to the first yield
print(avg.send(10), avg.send(20), avg.send(60))      # 10.0 15.0 30.0
avg.close()                            # stop it (raises GeneratorExit inside)


# --- 2. An async generator: stream pages from a (fake) paginated API -----------------------------
async def fetch_page(page: int) -> list[str]:
    await asyncio.sleep(0.1)           # pretend network latency
    data = {1: ["a", "b"], 2: ["c", "d"], 3: ["e"]}
    return data.get(page, [])


async def all_items():
    page = 1
    while items := await fetch_page(page):      # await INSIDE a generator
        for item in items:
            yield item                          # hand out one item at a time
        page += 1


async def main():
    async for item in all_items():              # `async for` consumes async generators
        print("got", item)
    # async comprehensions work too:
    upper = [i.upper() async for i in all_items()]
    print(upper)


asyncio.run(main())
