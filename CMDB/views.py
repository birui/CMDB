#coding=utf-8
import os,sys
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
import subprocess
import zabbix_api
reload(sys)
sys.setdefaultencoding( "utf-8" )

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

def hosts(request):
    return render_to_response('hosts.html')

def json_host(request):
    return render_to_response('json_host_list.txt')

def ajax_list(request):
    hostname = request.GET['hostname2'] #获取提交过来的数据
    item = serializers.serialize("json", iterms.objects.all().filter(hostname=hostname)) #json格式输出
    return HttpResponse(item) 
     

def zabbix_get(request):
    itemid = request.GET['itemid']
    cmd = zabbix_api.get_history(itemid)
    return HttpResponse(min(cmd))

def ratio(request):
    iterm = iterms.objects.all()
    return render(request,'iterms.html',{'iterm':iterm})

# def item(request):
#     iterm = iterms.objects.all()

#     for i in iterm:
#         loc_hostid = i.hostid
#         id_value = { 'cpu_idle':i.cpu_itemid, 'cpu_load':i.cpu_load_itemsid,'eth0_in':i.eth0_in_itemsid,'eth0_out':i.eth0_out_itemsid,'eth1_in':i.eth1_in_itemsid,'eth1_out':i.eth1_out_itemsid,'memory_available':i.memory_available_itemsid,'memory_total':i.memory_total_itemsid }
#         #print type(id_value)
#         for k , v in id_value.items():
#             # print "Key is %s, value is %s" % (k, v)
#             cmd = zabbix_api.get_history(v)
#             try:
#                 print k,v,min(cmd)
#                 # p = iterms.objects.get(hostname=loc_hostid) #写入数据库的步骤
#                 # p.k = min(cmd)
#                 # p.cpu_idle = 1
#                 # p.save()   #保存到数据库
#             except:
#                 print 'null'
           
#     return HttpResponse(id_value) #return 必须写在for外面不然循环会停止
def item_data(request):
    items = serializers.serialize("json", iterms.objects.all())
    return HttpResponse(items, content_type='application/json')

def items(request):
    return render_to_response('items_list.html')

def online_web(request):
    return render_to_response('online.html')

def online_app(request):
    # online = online.objects.all()
    version = request.POST['version']
    modelname = request.POST['modelname']
    describe = request.POST['describe']
    
    print "%s , %s, %s" %(version,modelname,describe)
    u1 = online(models_name=modelname ,version=version ,describe=describe )
    u1.save()

    cmd = "scripts/playbooks/cooansible-api.sh "
    status = subprocess.check_output(cmd + modelname + " " + version ,shell=True)
    
    mailbox = [
    'birui@coohua.com',
    'zhubaofeng@coohua.com',
    ]
    
    subject = '%s %s 上线' % (modelname,version) 

    for i in mailbox:
        print i
        mail_cmd = "scripts/mail.py '%s' '%s' '%s' " % (i,subject,describe)
        os.system(mail_cmd)

    return HttpResponse(status)

def showlog_web(request):
    return render_to_response('showlog.html')

def showlog_app(request):
    modelname = request.POST['modelname']
    filters_segment= request.POST['version']
    cmd = "scripts/playbooks/show_log.sh"
    status = subprocess.check_output(cmd + " " + modelname ,shell=True)
    return HttpResponse(status)


   












