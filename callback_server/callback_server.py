import http.server # the server we will use
import socketserver # handle concurrent connections
import urllib.parse # parse incoming query parameters
import threading # so the server can run on a background thread

# specify the target site
target_url = "127.0.0.1"
port = 8000
host = "localhost"

# The request handler we will use for the CallbackServer
class CallbackServer(http.server.BaseHTTPRequestHandler):

    # what will happen if the XSS gets executed
    def do_GET(self):
        print("\nXSS DETECTED!") # prints "XSS DETECTED" in the terminal if a get request gets sent (this means that the XSS injection was successful)
        print(f"Path: {self.path}") # prints the path that was used for the successful XSS attack

        self.send_response(200) # sends an HTTP 200 OK status to the client to indicate successful receiving of the request

        # TODO: add further code to do the actual information gathering


def startServer():
    server = http.server.HTTPServer((host, port), CallbackServer) # The actual CallbackServer, first argument specifies the location at which it will run, the second argument specifies the argument handler
    # could add a message that prints where the server is starting for clarity
    server_thread = threading.Thread(target=server.serve_forever) # make a specific thread so the incoming request handler of the server can run continuously without interrupting the program
    server_thread.daemon = True # make it so the thread also stops when the program is stopped
    server_thread.start # actually starts the server

