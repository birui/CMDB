#coding=utf-8

from __future__ import unicode_literals

from django.db import models

class Services(models.Model):
    name = models.CharField(max_length=70)
    lead = models.CharField(max_length=50)
    remark = models.CharField(max_length=250)
    def __unicode__(self):
        return self.name

class Server(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Hosts(models.Model):
    instance_id = models.CharField(max_length=50)
    hostname = models.CharField(max_length=50)
    lip = models.CharField(max_length=15)
    wip = models.CharField(max_length=15,blank=True)
    config = models.CharField(max_length=250)
    #1青岛,2杭州,3北京
    data_center = models.IntegerField()
    service_model = models.ForeignKey(Services,blank=True)
    server = models.ManyToManyField(Server,blank=True)
    environment = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    cost = models.IntegerField(blank=True)
    remark = models.CharField(max_length=250,blank=True)
    def __unicode__(self):
        return self.hostname

class Brothers(models.Model):
    name = models.CharField(max_length=20)
    #1研发
    department = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20,blank=True)
    service = models.ManyToManyField(Services)
    def __unicode__(self):
        return self.name


class History(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(Brothers)
    host = models.ForeignKey(Hosts)
    remark = models.CharField(max_length=250)




# Create your models here.
