#coding=utf-8
import os
from django.shortcuts import render,render_to_response
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect
from CMDB.models import *
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import auth
import json
from django.core import serializers
import urllib2
from django.http import JsonResponse

zabbix_url="http://115.28.203.116/zabbix/api_jsonrpc.php"
api_pass='CooHua007'
auth_data={ 'jsonrpc':'2.0','method':'user.login','params':{'user':'Admin','password':api_pass},'id':1}


# Create your views here.
# def test(request) :
#     hosts = Hosts.objects.all() #查出所有hosts表的数据
#     return render(request, 'test.html', {'hosts': hosts})
def hostlist(request):
    hosts = Hosts.objects.all() #查出所有hosts表的数据
    paginator = Paginator(hosts, 50) #每页显示50个,分页器,实例化一个分页对象
    page = request.GET.get('page') #html传递参数page
    try :
        hosts_list = paginator.page(page) #当前需要显示的页
    except PageNotAnInteger : # 如果页码不是个整数
        hosts_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage : # 如果页码太大，没有相应的记录
        hosts_list = paginator.paginator(paginator.num_pages) # 取最后一页的记录
    return render(request, 'test.html', {'hosts_list' : hosts_list})

def boot(request):
    return render(request,'boot.html',)

# def search_form(request):
#     return render_to_response('search_form.html') 

def search(request):
    error = False
    if 'q' in request.GET: #有数据提交进来，q是变量名称
        q = request.GET['q']
        hosts = Hosts.objects.all().filter(hostname__icontains = q)
        paginator = Paginator(hosts, 200) #每页显示100个
        page = request.GET.get('page')
        try :
            hosts_list = paginator.page(page)
        except PageNotAnInteger :
            hosts_list = paginator.page(1)
        except EmptyPage :
            hosts_list = paginator.paginator(paginator.num_pages)
        return render(request, 'test.html', {'hosts_list' : hosts_list})

    else:

        return render_to_response('test.html', {'error': error})
def index_1(request):
    hosts = Hosts.objects.all() #查出所有hosts表的数据
    services = Services.objects.all() #服务模块总量
    paginator = Paginator(hosts, 50) #每页显示50个,分页器,实例化一个分页对象
    page = request.GET.get('page') #html传递参数page
    try :
        hosts_list = paginator.page(page) #当前需要显示的页
    except PageNotAnInteger : # 如果页码不是个整数
        hosts_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage : # 如果页码太大，没有相应的记录
        hosts_list = paginator.paginator(paginator.num_pages) # 取最后一页的记录
    return render(request, 'index_1.html', {'hosts_list' : hosts_list,'services':services})

def report(request):
    hosts = Hosts.objects.all()
    services = Services.objects.all()
    return render(request,'report.html',{'hosts':hosts,'services':services})

def services(request):
    services = Services.objects.all()
    return render(request,'services.html',{'services':services})

def domain(request):
    domain = Domain.objects.all()
    return render(request,'domain.html',{'domain':domain})
def fu(request):
    return render_to_response('fu.html') 
def even(request):
    return render_to_response('even.html') 

#basepath=os.getcwd()+'\\dockerApp\\app\\templates\\';
def homepage(request):
    response=render_to_response("index.html");
    return response

def account_login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    #print username,password
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect("/test/")
    else:
        return render_to_response('index.html',{'login_err':'wrong username or password!'})
def data(request):
    hosts = serializers.serialize("json", Hosts.objects.all())
    return HttpResponse(hosts, content_type='application/json')

def table(request):
    #hosts = Hosts.objects.all() 
    #return render_to_response("table.html")
    #host_js = json.dumps(hosts)
    #print(type(hosts))
    #hosts = serializers.serialize("json", Hosts.objects.all())
    #return render(request, 'table.html', {'hosts_list' : hosts })
    return render_to_response('table.html')

#auth function验证登陆
def zabbix_api(request):
    request=urllib2.Request(zabbix_url,json.dumps(auth_data))
    request.add_header('Content-Type','application/json')
    response=urllib2.urlopen(request)
    var1=json.loads(response.read())
    

def ajax_list(request):
    hostname = request.GET['hostname2'] #获取提交过来的数据
    item = serializers.serialize("json", iterms.objects.all().filter(hostname=hostname)) #json格式输出
    return HttpResponse(item) 
     
def test1(request):
    return render(request,'test.html')

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))







