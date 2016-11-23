#coding=utf-8
import MySQLdb
import mysql_config as cfg

class mysql_tbsize(object):
	"""docstring for redis_comm"""
	def __init__(self, database, tablename):
		self.tablename = tablename
		self.database = database
		print cfg.qd_mysql['host']
		print self.tablename , self.database ,cfg.qd_mysql['user']

	def getdbsize_qd(self):
		tb_size = """ select count(*)  from %s """
		conn = MySQLdb.connect(host=cfg.qd_mysql['host'],user=cfg.qd_mysql['user'],passwd=cfg.qd_mysql['passwd'],db=self.database,port=cfg.qd_mysql['port'])
		cur=conn.cursor()
		cur.execute("select count(*)  from %s" %(self.tablename))
		qd_tbsize=cur.fetchone()
		cur.close()
		conn.close()
		return qd_tbsize[0]

	def getdbsize_bj(self):
		tb_size = """ select count(*)  from %s"""
		conn = MySQLdb.connect(host=cfg.bj_mysql['host'],user=cfg.bj_mysql['user'],passwd=cfg.bj_mysql['passwd'],db=self.database,port=cfg.bj_mysql['port'])
		cur=conn.cursor()
		cur.execute("select count(*)  from %s" %(self.tablename))
		bj_tbsize = cur.fetchone()
		cur.close()
		conn.close()
		return bj_tbsize[0]

	def set_dbsie(self):
		qd = self.getdbsize_qd()
		bj = self.getdbsize_bj()
		diff = qd - bj
		update_db = """ update CMDB_mysql_count set qd_table_size = %s ,bj_table_size = %s ,diff_size = %s where table_name = %s and database_name = %s"""
		conn = MySQLdb.connect(host=cfg.mysql['host'],user=cfg.mysql['user'],passwd=cfg.mysql['passwd'],db=cfg.mysql['db'],port=cfg.mysql['port'])
		cur=conn.cursor()
		cur.execute(update_db,[qd,bj,diff,self.tablename,self.database])
		conn.commit()
		cur.close()
		conn.close()
    	
# test = mysql_tbsize('crm', 'tb_application')
# test.set_dbsie()
# qindao_size=test.getdbsize_qd()
# beijing_size=test.getdbsize_bj()
# print qindao_size,beijing_size


