"""
Modified to use the Geocoding API v3. Uses file-like semantics
"""
import urllib, urllib2
import json

params = {"address": "207 N. Defiance St, Archbold, OH"}
url = "http://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(params)

rawreply = urllib2.urlopen(url).read()
reply = json.loads(rawreply)
location = reply["results"][0]["geometry"]["location"]
print location.values()
