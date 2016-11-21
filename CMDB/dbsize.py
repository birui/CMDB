#coding=utf-8
import redis 
import MySQLdb
import dbsize_config as cfg

class redis_dbsize(object):
	"""docstring for redis_comm"""
	def __init__(self, qd_host, bj_ip, qd_ip, port):
		self.qd_host = qd_host
		self.bj_ip = bj_ip
		self.qd_ip = qd_ip
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
		r = redis.StrictRedis(self.qd_ip, self.port)
		a=r.dbsize()
		if a :
			return a
		else:
			print "a is null"
			return 0

	def getdbsize_bj(self):
		#bj_ip=self.get_bj_Ip()[0]
		r = redis.StrictRedis(self.bj_ip, self.port)
		a=r.dbsize()
		if a :
			return a
		else:
			print "a is null"
			return 0

	def set_dbsie(self):
		qd = self.getdbsize_qd()
		bj = self.getdbsize_bj()
		# print qd,bj,self.qd_host
		update_db = """ update CMDB_dbsize set qd_size = %s ,bj_size = %s where hostname = %s """
		conn = MySQLdb.connect(host=cfg.mysql['host'],user=cfg.mysql['user'],passwd=cfg.mysql['passwd'],db=cfg.mysql['db'],port=cfg.mysql['port'])
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


