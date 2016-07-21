#!/bin/bash
APP=$1
VERSION=$2

if [[ -z "$1"  ]]; then
	echo " model is None"
fi

if [[ -n "$2" ]]; then
	cd /Users/admin/python/ENV2.7/coohua_CMDB/scripts/playbooks
    ansible $1 -a "cat /data/coohua/logs/$1/access.txt |grep  \'$2\' "

else
	cd /Users/admin/python/ENV2.7/coohua_CMDB/scripts/playbooks
    ansible $1 -a "tail -n 100 /data/coohua/logs/$1/access.txt "	

fi


#ansible $1 -a "/app/coohua/publish/$1/get.sh $2"
#/app/coohua/publish/asp/asp_pub_client.sh
#/app/coohua/publish/altair/altair_pub_client.sh 