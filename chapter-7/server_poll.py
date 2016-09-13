#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Foundations of Python Network Programming - Chapter 7 - server_poll.py
# An event-driven approach to serving several clients with poll().

import lancelot
import select

listen_sock = lancelot.setup()
# a dict tracking sockets via their file descriptors
sockets = { listen_sock.fileno(): listen_sock }
requests = {}
responses = {}

# Get a poll object and register the listening socket
# for the incoming data event
poll = select.poll()
poll.register(listen_sock, select.POLLIN)

while True:
    for fd, event in poll.poll():
        # For each socket file descriptor with an event to be handled
        
        sock = sockets[fd]

        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            # socket hung up, error or invalid requests condition occurred
            # sock.close can trigger this
            # clear info about socket
            poll.unregister(fd)
            del sockets[fd]
            requests.pop(sock, None)
            responses.pop(sock, None)

        # Accept connections from new sockets.
        elif sock is listen_sock:
            newsock, sockname = sock.accept()
            # set communicating socket to non-blocking
            # throws error if no data can be sent or received
            newsock.setblocking(False) 
            fd = newsock.fileno()
            # track it using file descriptor
            # and register with poll object for incoming data
            sockets[fd] = newsock
            poll.register(fd, select.POLLIN)
            requests[newsock] = b''

        # Collect incoming data until it forms a question.
        elif event & select.POLLIN:
            data = sock.recv(4096)
            if not data:      # received end-of-file
                sock.close()  # makes POLLNVAL happen next time
                continue
            requests[sock] += data
            if b'?' in requests[sock]:
                # Recieved a complete question
                # Retrieve the answer and mark the socket for outgoing data
                question = requests.pop(sock)
                # convert from bytes to unicode, and retrieve response
                question = question.decode("utf-8")
                answer = dict(lancelot.qa)[question]
                answer = answer.encode("utf-8")  # convert response to bytes
                poll.modify(sock, select.POLLOUT)
                responses[sock] = answer  # set the outgoing response

        # Send out pieces of each reply until they are all sent.
        elif event & select.POLLOUT:
            # socket ready for outgoing data
            response = responses.pop(sock)
            n = sock.send(response)
            if n < len(response):
                # not whole response sent, truncate to unsent
                responses[sock] = response[n:]
            else:
                # whole response sent, modify to expect incoming data
                poll.modify(sock, select.POLLIN)
                requests[sock] = b''
