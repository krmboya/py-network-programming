#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Foundations of Python Network Programming - Chapter 7 - server_multi.py
# Using multiple threads or processes to serve several clients in parallel.
from __future__ import print_function

import sys, time, lancelot
from multiprocessing import Process
from server_simple import server_loop
from threading import Thread

WORKER_CLASSES = {'thread': Thread, 'process': Process}
WORKER_MAX = 10

def start_worker(Worker, listen_sock):
    worker = Worker(target=server_loop, args=(listen_sock,))
    worker.daemon = True  # exit when the main process does
    worker.start()  # run server_loop w/provided args in separate process/thread
    return worker

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[2] not in WORKER_CLASSES:
        sys.stderr.write('usage: server_multi.py interface thread|process\n')
        sys.exit(2)
    # Select appropriate worker type: Process or Thread
    Worker = WORKER_CLASSES[sys.argv.pop()]  # setup() wants len(argv)==2

    # Every worker will accept() forever on the same listening socket.
    listen_sock = lancelot.setup()
    workers = []
    for i in range(WORKER_MAX):
        workers.append(start_worker(Worker, listen_sock))

    # Check every two seconds for dead workers, and replace them.
    # This part runs in the parent process/main thread
    while True:
        time.sleep(2)
        for worker in workers:
            if not worker.is_alive():
                print(worker.name, "died; starting replacement worker")
                workers.remove(worker)
                workers.append(start_worker(Worker, listen_sock))
