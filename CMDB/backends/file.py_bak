#coding=utf-8
from xmlrpclib import ServerProxy, Fault
from django.conf import settings
from urlparse import urlparse
from server_test import Server
import re

class Backend(object):
	def __init__(self):
		self.super_url = {}
		self.server_list = {}
		#加入id方便以后通过id找到supervisor管理url
		index = 0
		fp = file('/Users/admin/python/ENV2.7/coohua_CMDB/CMDB/server.conf')
		for line in fp.readlines():
			id = str(index) 
			# server = Server(line.strip())
			# self.super_url.append(line.strip())
			# self.super_url[id] = line.strip()
			self.super_url[id] = line.strip()
			index += 1
			if len(line.strip()) == 0:break
		
		fp.close()
		#将server.py 得到的多个机器的supervisor数据统一导入server_list字典方便统一输出到页面
		for k1,v1 in self.super_url.items():
			# print s
			test = Server(v1,k1)
			test.refresh()
			for k in  test.dic.keys():
				self.server_list[k] = test.dic[k]
		# print self.server_list

    #通过name找到id的方法
	def id(self,name):
		for k in self.server_list.keys():
			p = re.compile("%s:.*" %(name))
			match = p.findall(k)
			if match != [] :
				id=re.findall("\d",match[0],flags=0)[-1]
				# print id

	def action(self,name,action):
		for k in self.server_list.keys():
			p = re.compile("%s:.*" %(name))
			match = p.findall(k)
			if match != [] :
				id=re.findall("\d",match[0],flags=0)[-1]

		url = self.super_url[id]
		sup_action = Server(url)
		if action == 'start':
			sup_action.start(name)
		elif action == 'stop':
			sup_action.stop(name)


test=Backend()
# test.action('0','a2-nginx','start')
test.id('a2-nginx')







