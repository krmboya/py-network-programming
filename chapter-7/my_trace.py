#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Foundations of Python Network Programming - Chapter 7 - my_trace.py
# Command-line tool for tracing a single function in a program.

import linecache, sys, time

def make_tracer(funcname):
    def mytrace(frame, event, arg):
        """Records info whenever a line in `funcname` is executed

        Returns a reference to itself"""
        
        if frame.f_code.co_name == funcname:
            if event == 'line':
                _events.append((time.time(), frame.f_code.co_filename,
                                frame.f_lineno))
            return mytrace
    return mytrace

if __name__ == '__main__':
    _events = []
    if len(sys.argv) < 3:
        sys.stderr.write('usage: my_trace.py funcname other_script.py ...\n')
        sys.exit(2)
    sys.settrace(make_tracer(sys.argv[1]))
    del sys.argv[0:2]  # show the script only its own name and arguments
    try:
        with open(sys.argv[0]) as f:
            code_obj = compile(f.read(), sys.argv[0], 'exec')
            exec(code_obj)
    finally:
        for t, filename, lineno in _events:
            s = linecache.getline(filename, lineno)
            sys.stdout.write('%9.6f  %s' % (t % 60.0, s))
