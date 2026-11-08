"""The application: wires routers, middleware, the WebSocket and health checks together.

Run locally:  uvicorn taskboard.main:app --reload    then open http://127.0.0.1:8000/docs
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from taskboard import __version__
from taskboard.config import settings
from taskboard.db import Base, engine
from taskboard.realtime import notifier
from taskboard.routers import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(engine)   # demo convenience; real deployments run Alembic migrations
    yield


app = FastAPI(title="Taskboard", version=__version__, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                   allow_methods=["*"], allow_headers=["Authorization", "Content-Type"])
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.websocket("/ws")
async def live_updates(ws: WebSocket) -> None:
    await notifier.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        notifier.disconnect(ws)
