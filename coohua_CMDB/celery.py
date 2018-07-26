#! /usr/bin/env python
# coding: utf-8
 
from __future__ import absolute_import
import os
from celery import Celery, platforms
from django.conf import settings
 
platforms.C_FORCE_ROOT = True 
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coohua_CDMB.settings')
app = Celery('coohua_CDMB')
 
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
 
 
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))