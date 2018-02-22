#!/usr/bin/env python

import urllib, urllib2
import requests
import re
from xml.dom import minidom

import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = 'https://localhost:8089'
username = 'admin'
password = '1'
search_query = "search=makeresults 1"

# Login and get the session key
request = urllib2.Request(base_url + '/servicesNS/admin/search/auth/login',
    data = urllib.urlencode({'username': username, 'password': password}))
server_content = urllib2.urlopen(request, context=ctx)

session_key = minidom.parseString(server_content.read()).\
        getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
print "Session Key: %s" % session_key

# Perform a search
r = requests.post(base_url + '/services/search/jobs/', data=search_query,
    headers = { 'Authorization': ('Splunk %s' %session_key)},
    verify = False)

print r.text.split('\n')[2]
prog = re.compile(r'[^\d]+(\d+\.\d+)[^\d]+')
id = prog.match(r.text.split('\n')[1]).group(1)

print base_url + '/services/search/jobs/%s/results' % id
r = requests.get(base_url + '/services/search/jobs/%s/results' % id, data="output_mode=csv",
    headers = { 'Authorization': ('Splunk %s' %session_key)},
    verify = False)
print r.text