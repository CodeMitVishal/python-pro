"""Module 26 · Background work: answer fast, do the slow part later

Users shouldn't wait for emails, PDF reports or image processing.

  1. BackgroundTasks (FastAPI)   -> run a function AFTER the response is sent.
                                    Small jobs, same process, lost if the server restarts.
  2. A job queue + worker        -> return a job id at once; a worker processes jobs;
                                    the client polls GET /jobs/{id} for the status.
                                    Here: asyncio.Queue inside the app.
  3. In production               -> Celery, RQ or arq with Redis/RabbitMQ: workers run in
                                    separate processes/machines, jobs survive restarts,
                                    retries and schedules built in. Same idea as #2:

         # tasks.py (Celery)                         # in the API
         @celery.task(bind=True, max_retries=3)       report.delay(user_id)  # returns at once
         def report(self, user_id): ...

Run it:  python 26_realtime_tasks_caching/02_background_tasks.py
"""
import asyncio
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, HTTPException

SENT_EMAILS: list[str] = []
JOBS: dict[str, dict] = {}


def send_welcome_email(address: str) -> None:
    time.sleep(0.3)                                  # pretend to talk to an email service
    SENT_EMAILS.append(address)


async def worker(queue: asyncio.Queue) -> None:
    while True:
        job_id = await queue.get()                   # waits for the next job
        JOBS[job_id]["status"] = "running"
        await asyncio.sleep(0.5)                     # pretend: build a big PDF report
        JOBS[job_id].update(status="done", result=f"/reports/{job_id}.pdf")
        queue.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.queue = asyncio.Queue()
    task = asyncio.create_task(worker(app.state.queue))   # start the worker with the app
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


@app.post("/signup")
def signup(email: str, background: BackgroundTasks) -> dict:
    background.add_task(send_welcome_email, email)   # runs after the response is sent
    return {"welcome": email}


@app.post("/reports", status_code=202)               # 202 Accepted: "working on it"
async def create_report() -> dict:
    job_id = uuid.uuid4().hex[:8]
    JOBS[job_id] = {"status": "queued"}
    await app.state.queue.put(job_id)
    return {"job_id": job_id, "status_url": f"/jobs/{job_id}"}


@app.get("/jobs/{job_id}")
def job_status(job_id: str) -> dict:
    if job_id not in JOBS:
        raise HTTPException(404, "unknown job")
    return JOBS[job_id]


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        start = time.perf_counter()
        print("signup ->", c.post("/signup?email=vishal@example.com").json())
        print(f"   emails sent so far: {SENT_EMAILS} (TestClient waits for background tasks;"
              f" a real client got its answer before the email went out)")

        job = c.post("/reports").json()
        print("report ->", job)
        for _ in range(4):
            print("   poll:", c.get(job["status_url"]).json())
            if JOBS[job["job_id"]]["status"] == "done":
                break
            time.sleep(0.3)
