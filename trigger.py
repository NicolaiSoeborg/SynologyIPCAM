#!/usr/bin/env python3

##############################
user = 'USERNAME'
password = 'PASSWORD'
base_url = 'http://192.168.1.XXX:5000/webapi/'
MAX_ATTEMPTS = 3 # The api call sometimes fails for unknown reasons
##############################

import sys, datetime
from time import sleep
import urllib.request
import urllib.parse
import json

def log(txt, die = False):
    t = datetime.datetime.now().strftime("%Y/%b/%d %H:%M:%S")
    print("[%s] %s" % (t,txt))
    if die: sys.exit()

def call_syno_api(path, values, attempt = 0):
    global MAX_ATTEMPTS
    param = urllib.parse.urlencode(values)
    with urllib.request.urlopen(base_url + path + '?' + param) as response:
        r = response.read().decode('utf-8')
        j = json.loads(r)
        if not ('success' in j and j['success']):
            if attempt < MAX_ATTEMPTS:
                log("Warning: GET: %s PARAM: %s\nResponse: %s.\nRetrying in 3 sec." % (path,values,r))
                sleep(3)
                return call_syno_api(path, values, attempt+1)
            log("Error: Could not complete request!", die = True)
        #log("From %s\nGot: %s" % (values,j))
        return j

try:
    argument = int(str(sys.argv[1]))
except ValueError:
    log("Error: Please enter a eventId.", die = True)

if argument < 1 or argument > 10:
    log("Error: eventId has to be in range [1, 10].", die = True)


# Init
values = {'api' : 'SYNO.API.Info',
          'method' : 'Query',
          'version' : '1',
          'query' : 'ALL'}
info = call_syno_api("query.cgi", values)
log("Init done.")

# Login
path = info['data']['SYNO.API.Auth']['path']
values = {'api' : 'SYNO.API.Auth',
          'method' : 'Login',
          'version' : '2',
          'account' : user,
          'passwd' : password,
          'session' : 'SurveillanceStation',
          'format' : 'cookie'}
ret = call_syno_api(path, values)
sid = ret['data']['sid']
log("Login done.")

# Trigger
path = info['data']['SYNO.SurveillanceStation.ExternalEvent']['path']
values = {'api' : 'SYNO.SurveillanceStation.ExternalEvent',
          'method' : 'Trigger',
          'version' : '1',
          'eventId' : argument,
          '_sid' : sid}
ret = call_syno_api(path, values)
log("Trigger done.")

# Logout
path = info['data']['SYNO.API.Auth']['path']
values = {'api' : 'SYNO.API.Auth',
          'method' : 'Logout',
          'version' : '2',
          'session' : 'SurveillanceStation',
          '_sid' : sid}
ret = call_syno_api(path, values)
log("Logout done.\nDone sending EventId=%s: %s" % (argument,ret))
