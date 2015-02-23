"""
Making a raw http request. Uses Google maps geocoding API v3
"""
import httplib
import json

path = '/maps/api/geocode/json?address=207+N.+Defiance+St%2C+Archbold%2C+OH'

connection = httplib.HTTPConnection('maps.googleapis.com')
connection.request('GET', path)
rawreply = connection.getresponse().read()
reply = json.loads(rawreply)
location = reply["results"][0]["geometry"]["location"]
print location.values()


