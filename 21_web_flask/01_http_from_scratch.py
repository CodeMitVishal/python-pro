"""Module 21 · HTTP from scratch: what a browser and a server really say

HTTP is just TEXT sent over a network connection.

  Request  (client -> server)        Response (server -> client)
  ---------------------------        ----------------------------
  GET /hello?name=Vishal HTTP/1.1    HTTP/1.0 200 OK
  Host: localhost:8765               Content-Type: application/json
  Accept: application/json           Set-Cookie: visits=1

  (optional body)                    {"message": "Hello, Vishal!"}

We start a tiny server with the standard library, then talk to it with a raw
socket so you can SEE the text, and finally with urllib like a normal client.

Run it:  python 21_web_flask/01_http_from_scratch.py
"""
import json
import socket
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PORT = 8765


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):                                   # one method per HTTP verb
        url = urlparse(self.path)
        if url.path != "/hello":
            self.send_response(404)                     # status code
            self.end_headers()
            return
        name = parse_qs(url.query).get("name", ["world"])[0]
        body = json.dumps({"message": f"Hello, {name}!"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")   # headers describe the body
        self.send_header("Set-Cookie", "visits=1")              # the server asks the browser to remember
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()                              # blank line = headers done
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(length))      # the request BODY
        self.send_response(201)                         # 201 Created
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"created": data["title"]}).encode())

    def log_message(self, *args):                       # keep the console quiet
        pass


server = HTTPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()

# --- 1. A raw request over a socket: HTTP really is text ----------------------------
raw_request = (
    "GET /hello?name=Vishal HTTP/1.1\r\n"
    f"Host: localhost:{PORT}\r\n"
    "Accept: application/json\r\n"
    "Connection: close\r\n"
    "\r\n"                                               # blank line ends the headers
)
with socket.create_connection(("127.0.0.1", PORT)) as sock:
    sock.sendall(raw_request.encode())
    chunks = []
    while chunk := sock.recv(4096):              # read until the server closes the connection
        chunks.append(chunk)
    response = b"".join(chunks).decode()
print("----- raw response -----")
print("\n".join(line for line in response.splitlines() if not line.startswith(("Server", "Date"))))

# --- 2. The same with a client library -------------------------------------------------
with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/hello?name=Raj") as resp:
    print("\nstatus:", resp.status, "| type:", resp.headers["Content-Type"])
    print("json:", json.load(resp))

# --- 3. POST with a JSON body ----------------------------------------------------------------
req = urllib.request.Request(
    f"http://127.0.0.1:{PORT}/todos",
    data=json.dumps({"title": "learn HTTP"}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    print("\nPOST ->", resp.status, json.load(resp))

# --- 4. Errors come back as status codes, not crashes ------------------------------------------
try:
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/nope")
except urllib.error.HTTPError as e:
    print("GET /nope ->", e.code)

server.shutdown()

# Status code families:
#   2xx success   (200 OK, 201 Created, 204 No Content)
#   3xx redirect  (301 Moved Permanently, 303 See Other)
#   4xx YOUR fault (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422)
#   5xx SERVER fault (500 Internal Server Error, 503 Service Unavailable)
