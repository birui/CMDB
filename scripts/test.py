#!/usr/bin/env python2.7
#coding=utf-8
import urllib2
import json
import os
import subprocess
import zabbix_api

def zabbix_get():
    #cmd = 'python /Users/admin/python/ENV2.7/coohua_CMDB/scripts/zabbix-api.py'
    cmd = zabbix_api.get_history()
    #status = subprocess.check_output(cmd,shell=True)
    # for i in status[0]:
    # 	print i
    print cmd
    #print(type(cmd))


test = zabbix_get()
