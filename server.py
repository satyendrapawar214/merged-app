import http.server
import ssl
import sys

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

def run(server_class=http.server.HTTPServer, handler_class=SimpleHandler, port=8443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    try:
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    except Exception as e:
        print(f"Error loading certificate or key: {e}")
        sys.exit(1)

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f'Starting HTTPS server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

