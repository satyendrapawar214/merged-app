import http.server
import ssl

# Define the handler for HTTP requests
class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Send message body
        self.wfile.write(b"OK")

def run(server_class=http.server.HTTPServer, handler_class=SimpleHandler, port=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    # Create SSLContext
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # Paths to your certificate and key files

    # Wrap the HTTP server with SSLContext
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f'Starting HTTPS server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
