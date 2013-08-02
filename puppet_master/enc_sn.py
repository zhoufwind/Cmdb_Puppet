#!/usr/local/python/bin/python
#!-*- coding:utf-8 -*-

import urllib, urllib2
import json
import sys
import yaml
import os

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_CACHE='/var/tmp/json_cache'

def getHosts():
    url = 'http://132.96.77.188:8000/api/gethostbyidentity.json?hostidentity=%s' % sys.argv[1]
    try:
        data = urllib2.urlopen(url).read()
        writeFile(JSON_CACHE,data)
    except:
        data = open(JSON_CACHE,'r').read()
    return json.loads(data)
    
def writeFile(f,s):
    with open(f,'w') as fd:
        fd.write(s)

def getHostClass(data):
    ret = set()
    for hostgroup in data['hostgroups']:
        ret.add(str(hostgroup))
    return ret

def main():
    cmdb_data = getHosts()
    classes = getHostClass(cmdb_data)
    data = {'classes':list(classes)}
    explicit_start = yaml.dump(data,explicit_start=True,default_flow_style=False)
    return explicit_start

if __name__ == '__main__':
    print main()
