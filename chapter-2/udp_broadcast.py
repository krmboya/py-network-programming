#!/usr/bin/env python
# UDP client and server for broadcast messages on local LAN
from __future__ import print_function

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

MAX = 65535
PORT = 1060

if 2 <= len(sys.argv) <=3 and sys.argv[1] == 'server':
    s.bind(('', PORT))
    print ('Listening for broadcasts at', s.getsockname())
    while True:
        data, address = s.recvfrom(MAX)
        print ('The client at %r says: %r' % (address, data))
elif len(sys.argv) == 3 and sys.argv[1] == 'client':
    network = sys.argv[2]
    s.sendto('Broadcast message!'.encode('utf-8'), (network, PORT))
else:
    sys.stderr.write('usage: udp_broadcast.py server\n')
    sys.stderr.write('   or: udp_broadcast.py client <host>\n')
    sys.exit(2)
