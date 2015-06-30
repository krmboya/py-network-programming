"""
Making a raw http request to Google maps geocoding API v3
"""
import json
try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

path = u'/maps/api/geocode/json?address=207+N.+Defiance+St%2C+Archbold%2C+OH'

connection = HTTPConnection('maps.googleapis.com')
connection.request('GET', path)
rawreply = connection.getresponse().read()
unicode_reply = rawreply.decode("utf-8")
reply = json.loads(unicode_reply)
location = reply["results"][0]["geometry"]["location"]
print(list((location.values())))


