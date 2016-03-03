#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Foundations of Python Network Programming - Chapter 5 - blocks.py
# Sending data one block at a time.

from __future__ import print_function

import socket, struct, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 1060
format = struct.Struct('!I')  # for messages up to 2**32 - 1 in length

def recvall(sock, length):
    data = bytes()
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message'
                           % (len(data), length))
        data += more
    return data

def get(sock):
    lendata = recvall(sock, format.size)
    (length,) = format.unpack(lendata)
    return recvall(sock, length).decode("utf-8")

def put(sock, message):
    bytes_ = message.encode("utf-8")
    sock.send(format.pack(len(bytes_)) + bytes_)

if sys.argv[1:] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Listening at', s.getsockname())
    sc, sockname = s.accept()
    print('Accepted connection from', sockname)
    sc.shutdown(socket.SHUT_WR)  # only reading, no writing
    while True:
        message = get(sc)
        if not message:
            break
        print('Message says:', repr(message))
    sc.close()
    s.close()

elif sys.argv[1:] == ['client']:
    s.connect((HOST, PORT))
    s.shutdown(socket.SHUT_RD)  # only writing, no reading
    put(s, 'Beautiful is better than ugly.')
    put(s, 'Explicit is better than implicit.')
    put(s, 'Simple is better than complex.')
    put(s, '')
    s.close()

else:
    sys.stderr.write('usage: blocks.py server|client [host]\n')
