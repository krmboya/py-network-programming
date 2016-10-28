#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Foundations of Python Network Programming - Chapter 9 - verbose_http.py
# HTTP request handler for urllib2 that prints requests and responses.
from __future__ import print_function

from io import StringIO

try:
    from http.client import HTTPResponse, HTTPConnection
except ImportError as e:
    from httplib import HTTPResponse, HTTPConnection

try:
    from urllib.request import HTTPHandler
except ImportError:
    from urllib2 import HTTPHandler


class VerboseHTTPResponse(HTTPResponse):
    """ Class to use for the response"""
    def _read_status(self):
        s = self.fp.read()
        print( '-' * 20, 'Response', '-' * 20)
        print(s.split('\r\n\r\n')[0])  # print only header section
        self.fp = StringIO(s.decode("utf-8"))
        return HTTPResponse._read_status(self)

class VerboseHTTPConnection(HTTPConnection):
    """Class to use for the request"""
    response_class = VerboseHTTPResponse  # class for the response
    def send(self, s):
        """Overrides HTTPConnection.send with extra functionality

        Print request before sending"""

        print('-' * 50)
        print(s.strip())
        HTTPConnection.send(self, s)

class VerboseHTTPHandler(HTTPHandler):
    def http_open(self, req):
        """Returns a file-like object for the request"""
        
        return self.do_open(VerboseHTTPConnection, req)
