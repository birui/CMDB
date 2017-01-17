#!/usr/bin/env python
import sys,os
sys.path.append('/Users/admin/python/ENV2.7/coohua_CMDB')
os.environ['DJANGO_SETTINGS_MODULE'] ='coohua_CMDB.settings'
#----------------Use Django Mysql model----------------
from CMDB.models import *

def get_ip_list():
    domain = CMDB_share_domain.objects.all()
    return domain
aaa = get_ip_list()

print  aaa