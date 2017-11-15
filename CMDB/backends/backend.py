#coding=utf-8
from xmlrpclib import ServerProxy, Fault
# from django.conf import settings
from urlparse import urlparse
from server_test import Server
import re
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coohua_CMDB.settings')
import django
django.setup()
from CMDB.models import supervisor_ip

class Backend(object):
	def __init__(self):
		#id对应的url
		self.super_url = {}
		#所有机器获取的服务列表
		self.server_list = {}
		self.id_hostname = {}
		#加入id方便以后通过id找到supervisor管理url
	def refresh(self):
		su_url_list = supervisor_ip.objects.all().values('id', 'su_hostname', 'su_url')
		for su_list in su_url_list:
			su_id = int(su_list['id'])
			self.super_url[su_id] = su_list['su_url'].encode('utf8')
			self.id_hostname[su_id] = su_list['su_hostname'].encode('utf8')

		# print 'url == >' , self.super_url

		# 将server.py 得到的多个机器的supervisor数据统一导入server_list字典方便统一输出到页面
		for k1,v1 in self.super_url.items():
			su_hostname = self.id_hostname[int(k1)]
			test = Server(v1,k1,su_hostname)
			test.refresh()
			for k in  test.dic.keys():
				self.server_list[k] = test.dic[k]

				print self.server_list

	def action(self,name,action):
		#通过name找到id，正则过滤出key里面的id
		for k in self.server_list.keys():
			p = re.compile("%s:.*" %(name))
			match = p.findall(k)
			if match != [] :
				id=re.findall("\d",match[0],flags=0)[-1]
		    	# print '==:>' ,id
		#通过id可以得到url
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
		for k in self.server_list.keys():
			p = re.compile("%s:.*" %(name))
			match = p.findall(k)
			if match != [] :
				id=re.findall("\d",match[0],flags=0)[-1]
				return int(id)

# test=Backend()
# # # test.action('0','a2-nginx','start')
# # test.id('a2-nginx')
# test.refresh()







