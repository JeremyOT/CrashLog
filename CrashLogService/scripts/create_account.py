#!/usr/bin/python

import urllib2
import json
import hmac
import hashlib
import time
import base64
from sys import stdin
from bson import BSON

print "Enter your password"
password = stdin.readline().strip()
print "Enter your email"
email = stdin.readline().strip()

request = {}
request['method'] = 'account.create'
request['parameters'] = {
  'user_id': email,
  'password': password
}
headers = {'content-type': 'application/bson'}

body = BSON.encode(request)

req = urllib2.Request('http://localhost:8888/logservice', body, headers)
f = urllib2.urlopen(req)
response = BSON(f.read()).decode()

print response

with open('session.conf', 'wb') as session_file:
  session_file.write("session_id='%s'\n" % response['result']['session_id'])
  session_file.write("user_id='%s'\n" % response['result']['user_id'])

