#!/bin/bash
APP=$1
VERSION=$2
cd /Users/admin/python/ENV2.7/coohua_CMDB/scripts/playbooks
ansible $1 -a "/app/coohua/publish/$1/get.sh $2"
