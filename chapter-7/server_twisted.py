#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 7 - server_twisted.py
# Using Twisted to serve Lancelot users.

from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor
import lancelot

class Lancelot(Protocol):
    def connectionMade(self):
        self.question = b''

    def dataReceived(self, data):
        self.question += data
        if self.question.endswith(b'?'):
            question = self.question.decode("utf-8")
            answer = dict(lancelot.qa)[question]
            self.transport.write(answer.encode("utf-8"))
            self.question = b''

factory = ServerFactory()
factory.protocol = Lancelot
reactor.listenTCP(1060, factory)
reactor.run()
