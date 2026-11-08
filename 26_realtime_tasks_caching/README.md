# Module 26 · WebSockets, background tasks & caching

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-26.pdf) · [Interview Q&A](INTERVIEW.md)

Make apps feel instant: push live updates over WebSockets, move slow work to the background, and cache with Redis.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| WebSocket chat | [`01_websockets_chat.py`](01_websockets_chat.py) | a live chat room with broadcast |
| Background tasks | [`02_background_tasks.py`](02_background_tasks.py) | BackgroundTasks, a job queue + worker, 202 + polling, Celery |
| Caching with Redis | [`03_caching_with_redis.py`](03_caching_with_redis.py) | cache-aside, TTL, invalidation, counters, leaderboards |

```bash
pip install fastapi fakeredis httpx
```

```bash
python 26_realtime_tasks_caching/01_websockets_chat.py
```

## Exercise: Live prices

Cache-aside with an X-Cache header, invalidation, and WebSocket price pushes.

- Start here: [`exercises/ex26_live_prices.py`](../exercises/ex26_live_prices.py)
- Solution: [`solutions/ex26_live_prices.py`](../solutions/ex26_live_prices.py)

## Knowledge check

Preparing for interviews? Read the [Module 26 interview questions](INTERVIEW.md): short answers you can say out loud.

Test yourself with the [Module 26 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 27 · Docker, CI/CD & Azure](../27_deployment/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
