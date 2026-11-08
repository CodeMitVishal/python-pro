"""Live updates over WebSockets (Module 26): every task change is pushed to listeners."""
import json

from fastapi import WebSocket


class Notifier:
    def __init__(self) -> None:
        self.listeners: set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.listeners.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self.listeners.discard(ws)

    async def publish(self, event: str, payload: dict[str, object]) -> None:
        message = json.dumps({"event": event, **payload}, default=str)
        for ws in list(self.listeners):
            try:
                await ws.send_text(message)
            except Exception:                       # a dead connection: forget it
                self.disconnect(ws)


notifier = Notifier()
