#!/usr/bin/env python
# UDP client and server talking over a network
# Demonstrating exponential backoff
from __future__ import print_function

import socket
import sys
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1060

if 2 <= len(sys.argv) <= 3 and sys.argv[1] == 'server':
    interface = sys.argv[2] if len(sys.argv) > 2 else ''
    s.bind((interface, PORT))
    print('Listening at', s.getsockname())
    while True:
        data, address = s.recvfrom(MAX)
        if random.randint(0, 2) == 1:
            print('The client at', address, 'says', repr(data))
            s.sendto(
                'Your data was {0} bytes'.format(len(data)).encode("utf-8"), 
                address)
        else:
            print("Pretending to drop packet from", address)

elif len(sys.argv) == 3 and sys.argv[1] == 'client':
    hostname = sys.argv[2]
    s.connect((hostname, PORT))
    print ('Client socket name is', s.getsockname())
    delay = 0.1
    while True:
        s.send("This is another message".encode("utf-8"))
        print ("Waiting up to", delay, "seconds for a reply")
        s.settimeout(delay)
        try:
            data = s.recv(MAX)
        except socket.timeout:
            delay *= 2  # wait even longer next request
            if delay > 2.0:
                raise RuntimeError('I think he server is down')
        except:
            raise
        else:
            break
    print('The server says', repr(data))

else:
    sys.stderr.write('usage: udp_remote.py server [ <interface> ]\n')
    sys.stderr.write('   or: udp_remote.py client <host>\n')
    sys.exit(2)
