#coding=utf-8
import redis 
import MySQLdb

class redis_dbsize(object):
	"""docstring for redis_comm"""
	def __init__(self, qd_host ):
		self.qd_host = qd_host

	def get_bj_Ip(self):
		conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
		cur=conn.cursor()
		cur.execute("select bj_ip from  CMDB_dbsize where hostname='%s' " % self.qd_host)
		bj_ip = cur.fetchone()
		return bj_ip
		cur.close()
		conn.close()
	
	def getdbsize_qd(self):
		r = redis.StrictRedis(self.qd_host, port=6379)
		a=r.dbsize()
		if a :
			return a
		else:
			print "a is null"
			return 0

	def getdbsize_bj(self):
		bj_ip=self.get_bj_Ip()[0]
		r = redis.StrictRedis(bj_ip, port=6379)
		a=r.dbsize()
		if a :
			return a
		else:
			print "a is null"
			return 0

	def set_dbsie(self):
		qd = self.getdbsize_qd()
		bj = self.getdbsize_bj()
		print qd,bj,self.qd_host
		update_db = """ update CMDB_dbsize set qd_size = %s ,bj_size = %s where hostname = %s """
		conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
		cur=conn.cursor()
		cur.execute(update_db,[qd,bj,self.qd_host])
		conn.commit()
		cur.close()
		conn.close()



    	
# test = redis_dbsize('redis-altair001')
# test.set_dbsie()
# qindao_size=test.getdbsize_qd()
# beijing_size=test.getdbsize_bj()
# print qindao_size,beijing_size


