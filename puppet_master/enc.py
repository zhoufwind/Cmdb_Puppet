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
    url = 'http://132.96.77.188:8000/api/gethosts.json'
    try:
        data = urllib2.urlopen(url).read()
        writeFile(JSON_CACHE,data)
    except:
        data = open(JSON_CACHE,'r').read()
    
    return json.loads(data)
    
def writeFile(f,s):
    with open(f,'w') as fd:
        fd.write(s)

def getHostClass(data,hostname):
    ret = set()
    for hostgroup in data:
        if hostname in [h['hostname'] for h in  hostgroup['members']]:
            ret.add(str(hostgroup['hostgroup']))
    return ret
def main():
    cmdb_data = getHosts()
    if cmdb_data['status'] == 0:
        classes = getHostClass(cmdb_data['data'],sys.argv[1])
        data = {'classes':list(classes)}
        explicit_start = yaml.dump(data,explicit_start=True,default_flow_style=False)
        return explicit_start

if __name__ == '__main__':
    main()
    sys.exit(0)
