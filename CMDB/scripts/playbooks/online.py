#coding=utf-8
import redis  
  
r = redis.StrictRedis(host='127.0.0.1', port=6379)  
hostname = r.lrange('crm',0,-1)
for i in  hostname:
	ip_list = r.hgetall(i)
	# print ip_list
	r.hset(i,"weight","10")
	print ip_list

