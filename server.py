import http.server
import ssl

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

def run(server_class=http.server.HTTPServer, handler_class=SimpleHandler, port=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    # Wrap the server socket with SSL
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile="server.key",  # Path to your private key file
                                   certfile="server.crt",  # Path to your certificate file
                                   server_side=True)
    
    print(f'Starting HTTPS server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
