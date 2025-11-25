from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

STATIC_DIR = "static"

class MyHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200, content_type="text/html"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()

    def serve_static_file(self, filename="index.html"):
        filepath = os.path.join(STATIC_DIR, filename)

        if not os.path.exists(filepath):
            self._set_headers(404, "text/plain")
            self.wfile.write(b"404 File Not Found")
            return

        ext = filename.split(".")[-1]
        content_type = {
            "html": "text/html",
            "js": "application/javascript",
            "css": "text/css"
        }.get(ext, "text/plain")

        self._set_headers(200, content_type)
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_static_file("index.html")

        elif self.path == "/json":
            self._set_headers(200, "application/json")
            response = {"message": "Hello from merged server!"}
            self.wfile.write(json.dumps(response).encode())

        else:
            # Attempt to serve other static files
            requested = self.path.strip("/")
            self.serve_static_file(requested)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except:
            data = {"error": "Invalid JSON"}

        self._set_headers(200, "application/json")
        response = {"received": data}
        self.wfile.write(json.dumps(response).encode())


def run_server():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    print(f"Server running on port {port}")
    server = HTTPServer((host, port), MyHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
