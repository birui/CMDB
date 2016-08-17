#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import sys
import MySQLdb
import re

conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='cmdb', port=3306)
cur = conn.cursor()
update_db = """ update CMDB_hosts set config = %s  where  hostname = %s """

conn.autocommit(True)

t = os.popen(""" cat /Users/admin/coohua/ecs-api/vmList.txt """)

# os.system('echo > /Users/admin/coohua/ecs-api/test.txt')

for i in t.readlines():
    i = i.replace('\n', '')
    print i
    os.system("aliyuncli ecs ExportInstance --InstanceId %s --filename ./test.txt" % (i))
    lip1 = os.popen(
        "aliyuncli ecs DescribeInstanceAttribute --InstanceId %s  --output json  --filter InnerIpAddress.IpAddress\[0\]" % (
        i), "r")
    wip1 = os.popen(
        "aliyuncli ecs DescribeInstanceAttribute --InstanceId %s  --output json  --filter PublicIpAddress.IpAddress\[0\]" % (
        i), "r")

    lip = lip1.read()
    lip = lip.replace('"', '')
    wip = wip1.read()
    wip = wip.replace('"', '')
    # print lip,wip

    file = '/Users/admin/coohua/ecs-api/test.txt'
    fp = open(file, 'r')
    dict = json.loads(fp.read())
    instance_id = dict["InstanceId"]
    hostname = str(dict["InstanceName"])
    cpu = dict["Cpu"]
    mem = dict["Memory"]
    band = dict["InternetMaxBandwidthOut"]

    conf = "CPU:%s Memory:%s Band:%s" % (cpu, mem, band)
    # print conf
    config1 = str(conf)
    a1 = re.compile('\{.*\}')
    config = a1.sub('', config1)
    cur.execute("select hostname from  CMDB_hosts where hostname = %s", hostname)
    # fetchone()返回一条查询结果
    st_hostname = cur.fetchone()
    db_hostname = st_hostname[0]

    print config
    # print(type(config))
    # print db_hostname
    # print hostname
    # print(type(db_hostname))
    # print(type(hostname))
    # print(cmp(hostname,db_hostname))
    # 如果主机名一样，就看配置
    if cmp(hostname, db_hostname) == 0:
        cur.execute("select config from  CMDB_hosts where hostname = %s", hostname)
        st_config = cur.fetchone()
        db_config = st_config[0]
        # print db_config
        # print type(db_config)
        # print type(config)
        # print(cmp(db_config,config))
        # 配置不一样的改配置
        if cmp(db_config, config) != 0:
            cur.execute(update_db, [config, hostname])
            conn.commit()
            print " %s != %s  update db" % (db_config, config)

    # 库里没的主机新添加
    else:
        value = [instance_id, hostname, lip, wip, config, 1, 'online', 1, 1, 'test', 1]
        cur.execute(
            'insert into CMDB_hosts(instance_id,hostname,lip,wip,config,data_center,environment,status,cost,remark,service_model_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            value)
        conn.commit()
        print "%s no find create hosts" % hostname
    fp.close()

cur.close()
conn.close()

查出所有host
和hostid
select
hostid, host
from  hosts where

host
not like
'%Template%' and host
not like
'%CooHua%' and host
not like
'{%';

查出10204机器的
idle
cpu的
itemid。
select
itemid, name, key_
from items where

hostid = 10204 and key_ = 'system.cpu.util[,idle] ';

通过增额itemid
查
select
min(value_min)
from trends where

itemid = "27167" and from_unixtime(clock) >= '2016-03-03' and from_unixtime(clock) < '2016-03-04';

select
hosts.hostid, hosts.host, items.itemid, min(trends.value_min)
from

(items
left
join
hosts
on
hosts.host = items.host ) left
join
trends
on
items.itemid = trends.itemid
where
trends.from_unixtime(clock) >= '2016-03-03' and trends.from_unixtime(clock) < '2016-03-04';
