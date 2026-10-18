"""BidMirror local-only browser application. Python 3.10+ required."""
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
from analyzer import compare, extract_quote, sanitize, _check_text

ROOT = Path(__file__).resolve().parent

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            data=(ROOT/"static/index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        elif self.path == "/health":
            data=b'{"ok":true,"inference":"local-only"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        else:
            self.send_error(404); return
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def do_POST(self):
        if self.path not in ("/analyze", "/demo"):
            self.send_error(404);return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 40000:
                raise ValueError("Invalid request size")
            body = json.loads(self.rfile.read(length))
            if self.path == "/demo":
                f = ROOT/"fixtures/demo_extracts.json"
                contents = json.loads(f.read_text(encoding="utf-8"))
                at=(ROOT/"fixtures/quote_a.txt").read_text()
                bt=(ROOT/"fixtures/quote_b.txt").read_text()
                a,b=sanitize(contents["a"],at),sanitize(contents["b"],bt)
                output = {"mode":"fixture demonstration: precomputed sample, not model inference", "quote_a":at, "quote_b":bt,
                          "comparison":compare(a,b)}
            else:
                at=_check_text(body.get("quote_a", ""))
                bt=_check_text(body.get("quote_b", ""))
                a,b=extract_quote(at),extract_quote(bt)
                output={"mode":"locally inferred with Ollama", "comparison":compare(a,b)}
            self.respond(200,output)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            self.respond(400,{"error":str(e)})
        except RuntimeError as e:
            self.respond(503,{"error":str(e)})

    def respond(self, code, obj):
        data=json.dumps(obj,ensure_ascii=False).encode("utf8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers();self.wfile.write(data)

    def log_message(self, fmt, *args):
        # Don't log private quote text or response bodies.
        super().log_message(fmt, *args)

if __name__=="__main__":
    p=ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    args=p.parse_args()
    print(f"BidMirror (local only): http://127.0.0.1:{args.port}")
    ThreadingHTTPServer(("127.0.0.1", args.port),Handler).serve_forever()
