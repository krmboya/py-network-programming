"""
Modified to use the Geocoding API v3. Uses file-like semantics
"""

try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen
import json

params = {"address": "207 N. Defiance St, Archbold, OH"}
url = "http://maps.googleapis.com/maps/api/geocode/json?" + urlencode(params)

rawreply = urlopen(url).read()
unicode_reply = rawreply.decode('utf-8')
reply = json.loads(unicode_reply)
location = reply["results"][0]["geometry"]["location"]
print(list(location.values()))
