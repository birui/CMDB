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
    cost = models.FloatField(blank=True)
    remark = models.CharField(max_length=250,blank=True)
    def __unicode__(self):
        return self.hostname
    class Meta:
        ordering = ['hostname']

class Brothers(models.Model):
    name = models.CharField(max_length=20)
    #1研发
    department = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20,blank=True)
    service = models.ManyToManyField(Services)
    #pic = models.ImageField(upload_to = 'uploadimages')
    def __unicode__(self):
        return self.name


class History(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(Brothers)
    host = models.ForeignKey(Hosts)
    remark = models.CharField(max_length=250)

class Domain(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    usename = models.CharField(max_length=20,blank=True)
    domain = models.CharField(max_length=100)
    remark = models.CharField(max_length=250,blank=True)
    service_model = models.ForeignKey(Services,blank=True)
    def __unicode__(self):
        return self.domain

class CalendarEvent(models.Model):
    title = models.CharField(blank=True, max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    class Meta:
        verbose_name = ('Event')
        verbose_name_plural = ('Events')

    def __unicode__(self):
        return self.title

class iterms(models.Model):
    hostid = models.IntegerField()
    hostname = models.CharField(blank=True, max_length=200)
    cpu_itemid = models.IntegerField(blank=True)
    cpu_idle = models.FloatField(null=True)
    cpu_graphs_itemsid = models.IntegerField(blank=True)
    eth0_graphs_itemsid = models.IntegerField(blank=True)
    eth1_graphs_itemsid = models.IntegerField(blank=True) 
    def __unicode__(self):
       return str(self.hostname) #返回的数据
       # return self.hostname

        





# Create your models here.
