#!/usr/bin/env python2.7
#coding=utf-8
import urllib2
import json
zabbix_url="http://115.28.203.116/zabbix/api_jsonrpc.php"
api_pass='CooHua007'
auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':'Admin','password':api_pass},'id':1}
#auth function验证登陆
def get_auth():
    request=urllib2.Request(zabbix_url,json.dumps(auth_data))
    request.add_header('Content-Type','application/json')
    response=urllib2.urlopen(request)
    var1=json.loads(response.read())
    return var1['result'],var1['id']

def get_history(itemid):
    session = get_auth()
    hostlist = []
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"history.get",
        "params":{
            "output":"extend",
            "history":0, #0 - float; ; 
            "itemids":itemid,
            "limit":10
        },
        "auth":session[0],
        "id":session[1],
    })
    request = urllib2.Request(zabbix_url,data)
    request.add_header('Content-Type','application/json')
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
    	response = json.loads(result.read())
        result.close()
        #print "Number Of Hosts: ", len(response['result'])
        for host in response['result']:
            hostlist.append(host['value'])
    return  hostlist

#test = get_history(35158)
