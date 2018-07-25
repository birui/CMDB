# -*- coding: utf-8 -*-
import qiniu
import os
import sys
from qiniu import CdnManager
import ConfigParser
import traceback

access_key = '';
secret_key = '';
CONFIGFILE = os.getcwd() + '/CMDB/flushcdn/qiniu.ini'
# CONFIGFILE = './qiniu.ini'
CONFIGSECTION = 'SecretKey'
config = ConfigParser.ConfigParser()

def setup_credentials():
    try:
        config.read(CONFIGFILE)
        global access_key
        global secret_key
        access_key = config.get(CONFIGSECTION, 'access_key')
        secret_key = config.get(CONFIGSECTION, 'secret_key')
        # print access_key,secret_key
    except Exception, e:
		print traceback.format_exc()
		print("can't get access key pair, use config --id=[access_key] --secret=[secret_key] to setup")
		sys.exit(1)

def qiniuflush_cdn(urls):
	setup_credentials()
	auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
	cdn_manager = CdnManager(auth)
	refresh_url_result = cdn_manager.refresh_urls(urls)
	# print(refresh_url_result)
	return refresh_url_result

def qiniuflush_cdn_dr(urls):
	setup_credentials()
	auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
	cdn_manager = CdnManager(auth)
	refresh_dir_result = cdn_manager.refresh_dirs(urls)
	# print(refresh_url_result)
	return refresh_dir_result
