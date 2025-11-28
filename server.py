import http.server
import ssl

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

def run(server_class=http.server.HTTPServer, handler_class=SimpleHandler):
    server_address = ('', 8080)  # Use port 8080 for HTTP
    httpd = server_class(server_address, handler_class)
    
    # Optionally use SSL on port 443
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile="server.key",
                                   certfile="server.crt",
                                   server_side=True)
    print("Starting HTTPS server...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
