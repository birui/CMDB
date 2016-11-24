#coding=utf-8
import redis 
import MySQLdb
import dbsize_config as cfg

class redis_dbsize(object):
	"""docstring for redis_comm"""
	def __init__(self, qd_host, bj_ip, qd_ip ,qd_s_ip ,port):
		self.qd_host = qd_host
		self.bj_ip = bj_ip
		self.qd_ip = qd_ip
		self.qd_s_ip = qd_ip
		self.port = port

	# def get_bj_Ip(self):
	# 	print cfg.mysql['host']
	# 	#conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
		
	# 	conn = MySQLdb.connect(host=cfg.mysql['host'],user=cfg.mysql['user'],passwd=cfg.mysql['passwd'],db=cfg.mysql['db'],port=cfg.mysql['port'])
	# 	cur=conn.cursor()
	# 	cur.execute("select bj_ip from  CMDB_dbsize where hostname='%s' " % self.qd_host)
	# 	bj_ip = cur.fetchone()
	# 	return bj_ip
	# 	cur.close()
	# 	conn.close()
	
	def getdbsize_qd(self):
		try:
			r = redis.StrictRedis(self.qd_ip, self.port)
			a=r.dbsize()
		except Exception as e:
			return 0
			print "a is null %s" %(e)
		else:
			return a

	def getdbsize_qd_s(self):
		try:
			r = redis.StrictRedis(self.qd_s_ip, self.port)
			a=r.dbsize()
		except Exception as e:
			return 0
			print "a is null %s" %(e)
		else:
			return a


	def getdbsize_bj(self):
		try:
			#bj_ip=self.get_bj_Ip()[0]
			r = redis.StrictRedis(self.bj_ip, self.port)
			a=r.dbsize()

		except Exception as e:
			return 0
			print "a is null"
		else:
			return a



	def status_bj(self):
		try:
			r = redis.StrictRedis(self.bj_ip, self.port)
			a = r.info('Replication')['role']
		except Exception as e:
			return 0
			print "a is null"
		else:
			return a

				

	def set_dbsie(self):
		qd = self.getdbsize_qd()
		qd_s = self.getdbsize_qd_s()
		bj = self.getdbsize_bj()
		bj_status = self.status_bj()
		diff = qd - bj
		print qd,bj,diff 
		update_db = """ update CMDB_dbsize set qd_size = %s ,qd_s_size = %s ,bj_size = %s ,diff_size = %s ,bj_status = %s where hostname = %s """
		try:
			conn = MySQLdb.connect(host=cfg.mysql['host'],user=cfg.mysql['user'],passwd=cfg.mysql['passwd'],db=cfg.mysql['db'],port=cfg.mysql['port'])
			cur=conn.cursor()
			cur.execute(update_db,[qd,qd_s,bj,diff,bj_status,self.qd_host])
			conn.commit()
			cur.close()
			conn.close()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])



    	
# test = redis_dbsize('redis-altair001','123.56.11.110','115.28.108.0',6379)
# test.setslave_bj()
# test.set_dbsie()
# qindao_size=test.getdbsize_qd()
# beijing_size=test.getdbsize_bj()
# print qindao_size,beijing_size


