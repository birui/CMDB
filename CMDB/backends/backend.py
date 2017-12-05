#coding=utf-8
from xmlrpclib import ServerProxy, Fault
# from django.conf import settings
from urlparse import urlparse
from server_test import Server
import re
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coohua_CMDB.settings')
import django
django.setup()
from CMDB.models import supervisor_ip

class Backend(object):
	def __init__(self):
		#id对应的url
		self.super_url = {}
		# self.server_list = json.dumps(self.server_list)
		self.id_hostname = {}
		#加入id方便以后通过id找到supervisor管理url
	def refresh(self):
		#所有机器获取的服务列表
		self.server_list = []
		su_url_list = supervisor_ip.objects.all().values('id', 'su_hostname', 'su_url')
		for su_list in su_url_list:
			su_id = int(su_list['id'])
			self.super_url[su_id] = su_list['su_url'].encode('utf8')
			self.id_hostname[su_id] = su_list['su_hostname'].encode('utf8')

		# 将server.py 得到的多个机器的supervisor数据统一导入server_list字典方便统一输出到页面
		for k1,v1 in self.super_url.items():
			su_hostname = self.id_hostname[int(k1)]
			test = Server(v1,k1,su_hostname)
			test.refresh()
			for i in test.stats_list:
				self.server_list.append(i)

		print type(self.server_list )
		print self.server_list

	def action(self,name,action):
		#通过name找到id，正则过滤出key里面的id
		for i in self.server_list:
			if name == i['name']:
				id = i['id']
			else:
				print '%s name is no found' %(name)

		#通过id查数据库可以得到url
		url = self.super_url[int(id)]
		su_hostname = self.id_hostname[int(id)]
		sup_action = Server(url,id,su_hostname)
		if action == 'start':
			sup_action.start(name)
		elif action == 'stop':
			sup_action.stop(name)
		elif action == 'restart':
			sup_action.restart(name)
			
	def sup_id(self,name):

		for i in self.server_list:
			if name == i['name']:
				id = i['id']
				return int(id)
			else:
				print '%s name is no found' %(name)



# test=Backend()
# # # test.action('0','a2-nginx','start')
# # test.id('a2-nginx')
# test.refresh()







