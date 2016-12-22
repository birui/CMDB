#coding=utf-8
import MySQLdb
import redis 
import mysql_config as cfg

def getdbsize_qd():
	conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='cmdb',port=3306)
	cur=conn.cursor()
	cur.execute(" select bj_ip,port from cmdb_dbsize ")
	qd_tbsize=cur.fetchall()
	for r in qd_tbsize:   
		print r[0],r[1]
		ip = r[0]
		port = int(r[1])
		setslave_bj(ip,port)
	cur.close()
	conn.close()
	# print  qd_tbsize

def setslave_bj(bj_ip,port):
	#bj_ip=self.get_bj_Ip()[0]
	r = redis.StrictRedis(bj_ip,port)
	#a = r.info('Replication')['role']
	a = r.slaveof()

getdbsize_qd()
    	
# test = mysql_tbsize('crm', 'tb_application')
# test.set_dbsie()
# qindao_size=test.getdbsize_qd()
# beijing_size=test.getdbsize_bj()
# print qindao_size,beijing_size


