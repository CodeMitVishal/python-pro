"""Module 26 · WebSockets: a live chat room with FastAPI

HTTP is request -> response, then the connection is done. For live updates
(chat, notifications, dashboards, multiplayer games) the server must PUSH data.

A WebSocket starts as an HTTP request, "upgrades", and then stays open: both
sides can send messages at any time, until one side closes it.

Run the self-test:   python 26_realtime_tasks_caching/01_websockets_chat.py
Run a real server:   cd 26_realtime_tasks_caching && uvicorn 01_websockets_chat:app --reload
                     open http://127.0.0.1:8000 in TWO browser tabs and chat
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


class ChatRoom:
    """Keeps track of every open connection, so we can broadcast."""

    def __init__(self) -> None:
        self.connections: dict[WebSocket, str] = {}

    async def join(self, ws: WebSocket, name: str) -> None:
        await ws.accept()                                # complete the upgrade
        self.connections[ws] = name
        await self.broadcast(f"* {name} joined ({len(self.connections)} online)")

    async def leave(self, ws: WebSocket) -> None:
        name = self.connections.pop(ws, "someone")
        await self.broadcast(f"* {name} left")

    async def broadcast(self, message: str) -> None:
        for ws in list(self.connections):
            await ws.send_text(message)


room = ChatRoom()


@app.websocket("/ws/{name}")
async def chat(ws: WebSocket, name: str):
    await room.join(ws, name)
    try:
        while True:                                      # one loop per connected user
            text = await ws.receive_text()               # waits without blocking others
            await room.broadcast(f"{name}: {text}")
    except WebSocketDisconnect:                          # tab closed, network gone...
        await room.leave(ws)


PAGE = """<!doctype html><title>Chat</title>
<input id=name placeholder="your name"><button onclick="go()">Join</button>
<ul id=log></ul><input id=msg placeholder="message" onkeydown="if(event.key=='Enter')send()">
<script>
let ws;
function go(){ ws = new WebSocket(`ws://${location.host}/ws/${name.value}`);
  ws.onmessage = e => { const li = document.createElement('li'); li.textContent = e.data; log.append(li); }; }
function send(){ ws.send(msg.value); msg.value=''; }
</script>"""


@app.get("/")
def page() -> HTMLResponse:
    return HTMLResponse(PAGE)


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    client = TestClient(app)
    with client.websocket_connect("/ws/vishal") as vishal:
        print("vishal sees:", vishal.receive_text())
        with client.websocket_connect("/ws/raj") as raj:
            print("vishal sees:", vishal.receive_text())          # raj joined
            print("raj sees:   ", raj.receive_text())
            raj.send_text("hi everyone!")
            print("vishal sees:", vishal.receive_text())          # pushed by the server
            print("raj sees:   ", raj.receive_text())
        print("vishal sees:", vishal.receive_text())              # raj left
