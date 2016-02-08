#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from CMDB.models import *
from datetime import datetime

# Create your views here.
def test(request) :
    hosts = Hosts.objects.all() #查出所有hosts表的数据
    return render(request, 'test.html', {'hosts': hosts})
