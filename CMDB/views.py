#coding=utf-8
from django.shortcuts import render
from django.template import loader,Context
from django.http import HttpResponse
from CMDB.models import *
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
# def test(request) :
#     hosts = Hosts.objects.all() #查出所有hosts表的数据
#     return render(request, 'test.html', {'hosts': hosts})
def test(request):
    hosts = Hosts.objects.all() #查出所有hosts表的数据
    paginator = Paginator(hosts, 50) #每页显示50个
    page = request.GET.get('page')
    try :
        hosts_list = paginator.page(page)
    except PageNotAnInteger :
        hosts_list = paginator.page(1)
    except EmptyPage :
        hosts_list = paginator.paginator(paginator.num_pages)
    return render(request, 'test.html', {'hosts_list' : hosts_list})

def boot(request):
    return render(request,'boot.html',)
