#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 7 - server_SocketServer.py
# Answering Lancelot requests with a SocketServer.

try:
    from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
except ImportError:
    from SocketServer import ThreadingMixIn, TCPServer, BaseRequestHandler

import lancelot, server_simple, socket

class MyHandler(BaseRequestHandler):
    def handle(self):
        # self.request - the client socket
        server_simple.handle_client(self.request)

class MyServer(ThreadingMixIn, TCPServer):
    """TCP server that starts a thread for each new client"""
    allow_reuse_address = True
    # address_family = socket.AF_INET6  # if you need IPv6

server = MyServer(('', lancelot.PORT), MyHandler)
server.serve_forever()
