#!/usr/bin/python

import urllib2
import json
import hmac
import hashlib
import time
import base64
from sys import stdin
from bson import BSON

execfile('session.conf')

print "Enter the app ID"
app_id = stdin.readline().strip()

request = {}
request['method'] = 'log.show'
request['parameters'] = {
  'app_id': app_id
}
headers = {'content-type': 'application/bson'}

body = BSON.encode(request)

if session_id:
  headers['x-toto-session-id'] = session_id
  headers['x-toto-hmac'] = base64.b64encode(hmac.new(user_id, body, hashlib.sha1).digest())

req = urllib2.Request('http://localhost:8888/logservice', body, headers)
f = urllib2.urlopen(req)
response = BSON(f.read()).decode()

print response

