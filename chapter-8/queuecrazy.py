#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 8 - queuecrazy.py
# Small application that uses several different message queues

import random, threading, time, zmq
zcontext = zmq.Context()

def fountain(url):
    """Produces a steady stream of words."""
    zsock = zcontext.socket(zmq.PUSH)  # a zmq producer
    zsock.bind(url)  # bind to a well known port that consumers can connect to
    words = [ w for w in dir(__builtins__) if w.islower() ]
    while True:
        zsock.send(random.choice(words))
        time.sleep(0.4)

def responder(url, function):
    """Performs a string operation on each word received."""
    zsock = zcontext.socket(zmq.REP)  # a zmq responder - services requests
    zsock.bind(url)
    while True:
        word = zsock.recv()  # receive word from processor
        zsock.send(function(word))  # send the modified word back

def processor(n, fountain_url, responder_urls):
    """Read words as they are produced; get them processed; print them."""
    zpullsock = zcontext.socket(zmq.PULL)  # receives messages from producer
    zpullsock.connect(fountain_url)  # connects to producer

    zreqsock = zcontext.socket(zmq.REQ)  # sends requests and recieves responses

    # connect to responder sockets
    for url in responder_urls:
        zreqsock.connect(url)

    while True:
        word = zpullsock.recv()  # receive message from producer
        zreqsock.send(word)  # sends message to responder, alternates btn the 2
        print n, zreqsock.recv()  # receives response from producer

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Control-C the whole program
    thread.start()

# start a thread each for the producer and the two responders    
start_thread(fountain, 'tcp://127.0.0.1:6700')
start_thread(responder, 'tcp://127.0.0.1:6701', str.upper)
start_thread(responder, 'tcp://127.0.0.1:6702', str.lower)

# start 3 processor threads
for n in range(3):
    start_thread(processor, n + 1, 'tcp://127.0.0.1:6700',
                 ['tcp://127.0.0.1:6701', 'tcp://127.0.0.1:6702'])
time.sleep(30)
