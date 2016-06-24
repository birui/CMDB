#coding=utf-8
from xmlrpclib import ServerProxy, Fault
from django.conf import settings
from urlparse import urlparse
from server_test import Server
import re

class Backend(object):
	def __init__(self):
		#id对应的url
		self.super_url = {}
		#所有机器获取的服务列表
		self.server_list = {}
		#加入id方便以后通过id找到supervisor管理url
	def refresh(self):
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

	def action(self,name,action):
		#通过name找到id，正则过滤出key里面的id
		for k in self.server_list.keys():
			p = re.compile("%s:.*" %(name))
			match = p.findall(k)
			if match != [] :
				id=re.findall("\d",match[0],flags=0)[-1]
		#通过id可以得到url
		url = self.super_url[id]
		# print url
		# print id
		# print name
		# print action
		sup_action = Server(url,id)
		if action == 'start':
			sup_action.start(name)
		elif action == 'stop':
			sup_action.stop(name)
		elif action == 'restart':
			sup_action.restart(name)


# test=Backend()
# # test.action('0','a2-nginx','start')
# test.id('a2-nginx')







