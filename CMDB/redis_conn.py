#coding=utf-8
import redis  

r = redis.StrictRedis(host='127.0.0.1', port=6379)


class redis_comm(object):
	"""docstring for redis_comm"""
	def __init__(self, host_name ,modelname):
		self.host_name = host_name
		self.modelname = modelname
		print self.host_name
		print self.modelname
	
	def getip(self):
		a=r.hgetall(self.host_name)
		if a :
			ip = r.hget(self.host_name,"ip")
			return ip
		else:
			print "a is null"
		
	
	def drop_host(self):
		#print self.host_name
		a=r.hgetall(self.host_name)
		if a :
			r.hset(self.host_name,"weight" , "0")
			print a
		else:
			print "a is null"
		
	def add_host(self):
		a=r.hgetall(self.host_name)
		if a :
			r.hset(self.host_name,"weight" , "10")
			print a
		else:
			print "a is null"

# test = redis_comm('nginx-crm001' ,'crm','192.168.11.11')
# test.drop_host()
