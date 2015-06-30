"""
Raw network conversation with Googlemaps geocoding API v3 using sockets
"""

import socket
sock = socket.socket()
sock.connect(('maps.googleapis.com', 80))
sock.sendall(
    ('GET /maps/api/geocode/json?address=207+N.+Defiance+St%2C+Archbold%2C+OH ' 
     'HTTP/1.1\r\n'
     'Host: maps.googleapis.com:80\r\n'
     'User-Agent: search4.py\r\n'
     'Connection: close\r\n'
     '\r\n').encode("utf-8"))
rawreply = sock.recv(4096)
print(rawreply.decode("utf-8"))
