#coding=utf-8
import os,sys
from django.shortcuts import render,render_to_response
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect,Http404
from CMDB.models import *
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import auth
import json
import re
import time
from django.core import serializers
import urllib2
from django.http import JsonResponse
import subprocess
import zabbix_api
from django.core.urlresolvers import reverse
import simplejson
# from CMDB.backends.server import Server #如果导入不成功touch __init__.py
from CMDB.backends.backend import Backend
from CMDB.redis_conn import redis_comm
from xmlrpclib import ServerProxy
from CMDB.scripts.playbooks.ansicmd import *
from django.views.generic import ListView
from django.views.generic import View


sup_backend = Backend()

reload(sys)
sys.setdefaultencoding( "utf-8" )

# Create your views here.
# def test(request) :
#     hosts = Hosts.objects.all() #查出所有hosts表的数据
#     return render(request, 'test.html', {'hosts': hosts})
def hosts(request):
    return render_to_response('hosts.html')

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
    Modelname = Modelname.objects.all() #服务模块总量
    paginator = Paginator(hosts, 50) #每页显示50个,分页器,实例化一个分页对象
    page = request.GET.get('page') #html传递参数page
    try :
        hosts_list = paginator.page(page) #当前需要显示的页
    except PageNotAnInteger : # 如果页码不是个整数
        hosts_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage : # 如果页码太大，没有相应的记录
        hosts_list = paginator.paginator(paginator.num_pages) # 取最后一页的记录
    return render(request, 'index_1.html', {'hosts_list' : hosts_list,'Modelname':Modelname})

def report(request):
    hosts = Hosts.objects.all()
    services = Modelname.objects.all()
    return render(request,'report.html',{'hosts':hosts,'services':services})

def modelname(request):
    modelname = Modelname.objects.all()
    return render(request,'services.html',{'services':modelname})

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


def item_data(request):
    items = serializers.serialize("json", iterms.objects.all())
    return HttpResponse(items, content_type='application/json')

def items(request):
    return render_to_response('items_list.html')

def online_web(request):
    return render_to_response('online.html')

def ajax_online(request):
    # pass
    modelname1 = request.GET['modelname1'] #获取提交过来的数据
    servers = serializers.serialize("json", Hosts.objects.all().filter(Modelname__name=modelname1)) #json格式输出
    # print servers
    return HttpResponse(servers)


def online_app(request):
    # online = online.objects.all()
    modelname = request.POST['modelname']
    version   = request.POST['version']
    liplists  = request.POST['liplists']
    describe  = request.POST['describe']
    hostname  = request.POST['hostname']

    # print modelname,version,liplists,describe,hostname

    # print liplists
    
    e = re.compile(r',')
    host_list = e.split(hostname)
    i = ''

    eip = re.compile(r',')
    ip_list = eip.split(liplists)
    j = ''

#循环获取hostname，一次操作，停服务，下载包，调动本地部署程序。
    # for i in host_name:
    #     rediscomm = redis_comm(i,modelname)
    #     ip = rediscomm.getip()
        #=============openresty==============================
        #1、去权重
        # rediscomm.drop_host()
        #2、停服务，【supervisor的服务名称必须是hostname】
        # time.sleep(4)
        # try:
        #     svr=ServerProxy("http://user:123@%s:9001" %(ip))
        # except Exception, e:
        #     print "supervisor no run"
        #print svr.supervisor.getAllProcessInfo()
        #svr.supervisor.stopProcess(host_name)

        #3、调动本地部署程序**本机脚本未完成，【本地脚本：①记录老版本②备份老版本 ③回滚】
        # print ip
        # runcmd = playansible('%s' %(ip),'uptime')
        # runcmd.runcmd()

        #4、下载新包
        #wget "http://10.163.251.17:8102/%s/%s/%s-%s.war" %(modelname,version,modelname,version)
        #如果是asp模块下的就要加一层目录。

        # runcmd = playansible('%s' %(ip),'wget -O /app/coohua/asp/webapps/alteir.war http://121.42.11.38:8120/altair/1.1/altair-1.1.war')
        # runcmd.runcmd()
        # print "runcmd------------------------------>"
        #5、启动服务器
        # try:
        #     svr=ServerProxy("http://user:123@%s:9001" %(ip))
        # except Exception, e:
        #     print "supervisor no run"
        #print svr.supervisor.getAllProcessInfo()
        #svr.supervisor.startProcess(host_name)
        #6、恢复权重，先要判断supervisor状态是否启动。

        # rediscomm.add_host()
        #==================end===========================
    status = []

    file('tmp_log.txt','w')
    
    for host in host_list:
        f = file('tmp.txt','w+')
        f.write(host)
        f.flush()
        f.close()
        # print host
        # print modelname
        # print version
        cmd = '/app/coohua/publish/deploy/deploy.sh deploy %s' %(version)
        #print cmd
        runcmd = playansible('%s' %(host),cmd)
        #print runcmd
        sta=runcmd.runcmd()
        print sta
        f = file('tmp_log.txt','w+')
        f.write(sta)
        f.flush()
        f.close()

        status.append(sta)
        time.sleep(5)


    # print "%s , %s, %s" %(version,modelname,describe)
    ##存入数据库
    # u1 = online(models_name=modelname ,version=version ,describe=describe )
    # u1.save()

    # cmd = "scripts/playbooks/cooansible-api.sh "
    # status = subprocess.check_output(cmd + modelname + " " + version ,shell=True)
    
    # mailbox = [
    # 'birui@coohua.com',
    # 'zhubaofeng@coohua.com',
    # ]
    
    # subject = '%s %s 上线' % (modelname,version) 

    # for i in mailbox:
    #     print i
    #     mail_cmd = "scripts/mail.py '%s' '%s' '%s' " % (i,subject,describe)
    #     os.system(mail_cmd)
    return HttpResponse(status)

def fre_host(request):
    line_name = []
    f = file('tmp.txt','r')
    c = f.readlines()
    # print c
    for line in  c:
        line_name.append(line)
    f.close()

    return HttpResponse(line_name)

def fre_log(request):
    line_log = []
    f = file('tmp_log.txt','r')
    c = f.readlines()
    # print c
    for line in  c:
        line_log.append(line)
    f.close()

    return HttpResponse(line_log)


def showlog_web(request):
    return render_to_response('showlog.html')

def showlog_app(request):
    modelname = request.POST['modelname']
    filters_segment= request.POST['version']
    cmd = "scripts/playbooks/show_log.sh"
    status = subprocess.check_output(cmd + " " + modelname ,shell=True)
    return HttpResponse(status)

def supervisor(request):
    
    # print test.server_list


    try:
        sup_backend.refresh()
    except Exception, e:

        default_err = { 'err':{'statename':'error','description':'error','name':'error'}, }
        return render_to_response('supervisor/supervisor.html',{
            'servers_list' : default_err,
            })
    else:
    #将所有机器的supervisor控制的程序列表传给模板，字典格式    
        return render_to_response('supervisor/supervisor.html',{
            'servers_list' : sup_backend.server_list,
            })

def control(request):
    sup_backend.refresh()
    process_name = request.GET['name']
    action = request.GET['action']
    print action
    print process_name
    if action not in ('start', 'stop', 'restart'):
        raise Http404
    getattr(sup_backend,'action')(process_name,action) #test实例里面的action方法对process_name进行操作
    return HttpResponse(action) # TODO url reverse

class test_view(ListView):
    a = 1
    b = 2
    def get(self,request):
        return HttpResponse(self.a)

# def inf(request):
#     line_name = []

#     f = file('tmp.txt','w+')
#     f.write('c')
#     f.flush()
#     f.close()

#     f = file('tmp.txt','r')
#     c = f.readlines()
#     print c
#     for line in  c:
#         line_name.append(line)
#     f.close()
#     return HttpResponse(line_name)









    


        








