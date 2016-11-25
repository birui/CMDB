#coding=utf-8
import MySQLdb
import mysql_config as cfg

class mysql_tbsize(object):
	"""docstring for redis_comm"""
	def __init__(self, database, tablename):
		self.tablename = tablename
		self.database = database
		# print cfg.qd_mysql['host']
		# print self.tablename , self.database ,cfg.qd_mysql['user']

	def getdbsize_qd(self):
		tb_size = """ select count(*)  from %s """
		try:
			conn = MySQLdb.connect(host=cfg.qd_mysql['host'],user=cfg.qd_mysql['user'],passwd=cfg.qd_mysql['passwd'],db=self.database,port=cfg.qd_mysql['port'])
			cur=conn.cursor()
			cur.execute("select count(*)  from %s" %(self.tablename))
			qd_tbsize=cur.fetchone()
			cur.close()
			conn.close()
		except MySQLdb.Error,e:
			return 0
		return qd_tbsize[0]

	def getdbsize_bj(self):
		tb_size = """ select count(*)  from %s"""
		try:
			conn = MySQLdb.connect(host=cfg.bj_mysql['host'],user=cfg.bj_mysql['user'],passwd=cfg.bj_mysql['passwd'],db=self.database,port=cfg.bj_mysql['port'])
			cur=conn.cursor()
			cur.execute("select count(*)  from %s" %(self.tablename))
			bj_tbsize = cur.fetchone()
			cur.close()
			conn.close()
		except MySQLdb.Error,e:
			return 0
		return bj_tbsize[0]

	def set_dbsie(self):
		qd = self.getdbsize_qd()
		bj = self.getdbsize_bj()
		diff = qd - bj
		update_db = """ update CMDB_mysql_count set qd_table_size = %s ,bj_table_size = %s ,diff_size = %s where table_name = %s and database_name = %s"""
		try:
			conn = MySQLdb.connect(host=cfg.mysql['host'],user=cfg.mysql['user'],passwd=cfg.mysql['passwd'],db=cfg.mysql['db'],port=cfg.mysql['port'])
			cur=conn.cursor()
			cur.execute(update_db,[qd,bj,diff,self.tablename,self.database])
			conn.commit()
			cur.close()
			conn.close()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def op():
	try:
		conn = MySQLdb.connect(host=cfg.mysql['host'],user=cfg.mysql['user'],passwd=cfg.mysql['passwd'],db=cfg.mysql['db'],port=cfg.mysql['port'])
		cur=conn.cursor()
		cur.execute("select database_name,table_name from CMDB_mysql_count;")
		db_num=cur.fetchall()
		for x in db_num:
			db_name = x[0]
			tb_name = x[1]
			print db_name ,tb_name
			table_size_rsyn=mysql_tbsize(db_name,tb_name)
			table_size_rsyn.set_dbsie()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

op()	
    	
# test = mysql_tbsize('crm', 'tb_application')
# test.op()
# #test.set_dbsie()
# qindao_size=test.getdbsize_qd()
# #beijing_size=test.getdbsize_bj()
# print qindao_size


