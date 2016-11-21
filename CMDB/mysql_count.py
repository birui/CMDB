#coding=utf-8
import MySQLdb
import mysql_config as cfg

class mysql_tbsize(object):
	"""docstring for redis_comm"""
	def __init__(self, tablename):
		self.tablename = tablename
	
	def getdbsize_qd(self):
		tb_size = """ select count(*)  from %s"""
		conn = MySQLdb.connect(host=cfg.qd_mysql['host'],user=cfg.qd_mysql['user'],passwd=cfg.qd_mysql['passwd'],db=cfg.qd_mysql['db'],port=cfg.qd_mysql['port'])
		cur=conn.cursor()
		qd_tbsize = cur.execute(tb_size,[self.tablename])
		cur.close()
		conn.close()
		return qd_tbsize

	def getdbsize_bj(self):
		tb_size = """ select count(*)  from %s"""
		conn = MySQLdb.connect(host=cfg.bj_mysql['host'],user=cfg.bj_mysql['user'],passwd=cfg.bj_mysql['passwd'],db=cfg.bj_mysql['db'],port=cfg.bj_mysql['port'])
		cur=conn.cursor()
		bj_tbsize = cur.execute(tb_size,[self.tablename])
		cur.close()
		conn.close()
		return bj_tbsize

	def set_dbsie(self):
		qd = self.getdbsize_qd()
		bj = self.getdbsize_bj()
		print qd,bj,self.qd_host
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


