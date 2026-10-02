import json
import os
import sys

# Make `core` importable inside the Vercel function bundle.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def send_json(h, code, obj):
    body = json.dumps(obj).encode()
    h.send_response(code)
    h.send_header("Content-Type", "application/json")
    h.send_header("Content-Length", str(len(body)))
    h.end_headers()
    h.wfile.write(body)


def read_body(h, limit=4_000_000):
    n = int(h.headers.get("content-length") or 0)
    if n > limit:
        raise ValueError("File is too large (max 4 MB).")
    return h.rfile.read(n)
