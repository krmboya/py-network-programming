#!/usr/bin/env python
# Send a big UDP packet to our server
# Demonstrates packet fragmentation
from __future__ import print_function

import IN, socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1060

if len(sys.argv) != 2:
    sys.stderr.write('usage: big_sender.py host\n')
    sys.exit(2)

hostname = sys.argv[1]

s.connect((hostname, PORT))

s.setsockopt(socket.IPPROTO_IP, 
             IN.IP_MTU_DISCOVER, 
             IN.IP_PMTUDISC_DO)  # discover the mtu

try:
    s.send("#".encode("utf-8") * 65000)
except socket.error:
    print('The message did not make it')
    option = getattr(IN, "IP_MTU", 14)  # constant taken from <linux/in.h>
    print("MTU:", s.getsockopt(socket.IPPROTO_IP, option))
else:
    print('The big message was sent')
