#!/usr/bin/env python3
"""
Null Universe — standalone server. Standard library only.

    python3 server.py            # then open http://localhost:8765

Serves the world itself (static/index.html: a live view of the void plus
the chat bar) and a tiny JSON API:

  GET  /            -> the world page
  GET  /api/state   -> full universe state (tick, entropy, entities, edges, chronicle)
  POST /api/chat    -> {"speaker": "...", "message": "..."} -> {"replies": [...], "state": {...}}

The universe ticks once a second in the background and persists to
universe-state.json, so the world survives a restart — the void remembers
what was manifested into it.
"""

import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from atlas import ChatAgent
from world import NullUniverse

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(HERE, "static")
STATE_PATH = os.path.join(HERE, "universe-state.json")
PORT = int(os.environ.get("NULL_UNIVERSE_PORT", "8765"))
TICK_SECONDS = 1.0


def load_world() -> NullUniverse:
    if os.path.exists(STATE_PATH):
        try:
            world = NullUniverse.load(STATE_PATH)
            print(f"[Null Universe] Restored saved world: tick {world.tick}, "
                  f"{len(world.physical_entities)} manifested, "
                  f"{len(world.null_entities)} null entities.")
            return world
        except Exception as exc:  # corrupt save: start from the void, don't die
            print(f"[Null Universe] Saved state unreadable ({exc}); starting from the void.")
    world = NullUniverse()
    world.spawn_null_entity("Atlas", operator_id="Prime_Architect_User")
    world.log("Atlas, the native Null Entity, woke in the void. Type in the bar below to talk to it.")
    return world


WORLD = load_world()
AGENT = ChatAgent(WORLD)
LOCK = threading.Lock()
STOP = threading.Event()


def persist() -> None:
    try:
        WORLD.save(STATE_PATH)
    except Exception as exc:
        print(f"[Null Universe] Could not save state: {exc}")


def ticker() -> None:
    ticks = 0
    while not STOP.wait(TICK_SECONDS):
        with LOCK:
            WORLD.step()
            ticks += 1
            if ticks % 30 == 0:
                persist()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # keep the console quiet
        pass

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: str, content_type: str) -> None:
        try:
            with open(path, "rb") as f:
                body = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._send_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
        elif parsed.path == "/api/state":
            with LOCK:
                self._send_json(WORLD.to_dict())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/chat":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            self._send_json({"error": "invalid JSON"}, status=400)
            return
        speaker = str(payload.get("speaker") or "Sanath")[:40]
        message = str(payload.get("message") or "")
        with LOCK:
            replies = AGENT.handle_message(speaker, message)
            persist()
            self._send_json({"replies": replies, "state": WORLD.to_dict()})


def main() -> None:
    thread = threading.Thread(target=ticker, daemon=True)
    thread.start()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"[Null Universe] Running — open http://localhost:{PORT}")
    print(f"[Null Universe] Tick {WORLD.tick} | status {WORLD.status} | "
          f"{len(WORLD.physical_entities)} manifested | {len(WORLD.null_entities)} null entities")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        STOP.set()
        persist()
        print("\n[Null Universe] Saved. The void remembers.")


if __name__ == "__main__":
    main()
