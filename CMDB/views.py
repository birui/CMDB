# coding=utf-8
import os, sys
from django.shortcuts import render, render_to_response
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, Http404
from CMDB.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.shortcuts import redirect
from urllib import urlencode
from urllib import unquote
import json
import re
import time
import urllib2
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
from CMDB.redis_rsync.dbsize import redis_dbsize
from xmlrpclib import ServerProxy
from CMDB.scripts.playbooks.ansicmd import *
from CMDB.scripts.playbooks.ansiplaybook import *
from CMDB.scripts.weixin.weixin import *
from CMDB.scripts.weixin.coohua_domain import *
from django.views.generic import ListView
from django.views.generic import View
from django.core.files import File
from django import forms
from .forms import *
# from somewhere import handle_uploaded_file
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import FileSystemStorage
from django.db import connection

import random
import string
import datetime
from .forms import NameForm


sup_backend = Backend()

reload(sys)
sys.setdefaultencoding("utf-8")


# Create your views here.
# def test(request) :
#     hosts = Hosts.objects.all() #查出所有hosts表的数据
#     return render(request, 'test.html', {'hosts': hosts})
# ======new=======
def new(request):
    return render_to_response('new/base.html')


def new_hosts(request):
    return render(request, 'new/hosts.html', {'pagename': '服务器列表'})


def new_online_web(request):
    return render(request, 'new/online.html', {'pagename': '代码上线'})


def new_modelname(request):
    modelname = Modelname.objects.all()
    return render(request, 'new/services.html', {'services': modelname, 'pagename': '业务模块'})


def new_domain(request):
    domain = Domain.objects.all()
    return render(request, 'new/domain.html', {'domain': domain})


def new_items(request):
    return render_to_response('new/items_list.html')

def supervisor_server(request):
    return render_to_response('new/supervisor.html')

def supervisor_api(request):
    try:
        sup_backend.refresh()
    except Exception, e:

        default_err = {'err': {'statename': 'error', 'description': 'error', 'name': 'error'},}
        return render_to_response('new/supervisor.html', {
            'servers_list': default_err,
        })
    else:
        return HttpResponse(json.dumps(sup_backend.server_list),content_type='application/json')

def new_supervisor(request):
    # print test.server_list

    try:
        sup_backend.refresh()
    except Exception, e:

        default_err = {'err': {'statename': 'error', 'description': 'error', 'name': 'error'},}
        return render_to_response('new/supervisor.html', {
            'servers_list': default_err,
        })
    else:
        # 将所有机器的supervisor控制的程序列表传给模板，字典格式
        return render_to_response('new/supervisor.html', {
            'servers_list': sup_backend.server_list
        })
        # print type(sup_backend.server_list)
        # print sup_backend.server_list

        # return HttpResponse(json.dumps(sup_backend.server_list),content_type='application/json')



def get_supervisor_ip(request):
    su_url_list = supervisor_ip.objects.all().values('id','su_url')
    return HttpResponse(su_url_list)


def new_report(request):
    hosts = Hosts.objects.all()
    services = Modelname.objects.all()
    return render(request, 'new/report.html', {'hosts': hosts, 'services': services})


def config_manage(request):
    return render(request, 'new/config.html', {'pagename': '配置管理'})


def config_data(request):
    configname = serializers.serialize("json", config.objects.all())
    return HttpResponse(configname, content_type='application/json')


def config_update(request):
    return render(request, 'new/config_update.html', {'pagename': '配置同步'})


def ajax_config(request):
    # pass
    modelname1 = request.GET['modelname1']  # 获取提交过来的数据
    servers = serializers.serialize("json", Hosts.objects.all().filter(Modelname__name=modelname1))  # json格式输出
    # print servers
    return HttpResponse(servers)


def config_syn(request):
    mode = request.POST['mode']  # 执行模块
    name = request.POST['name']
    modelname = request.POST['modelname']  # 业务模块
    jsondata = serializers.serialize("json", config.objects.all().filter(models_name=modelname))
    listdata = json.loads(jsondata)
    playbook_path = listdata[0]['fields']['playbook_path']
    # remote_user = listdata[0]['fields']['remote_user']
    # path = listdata[0]['fields']['path']

    if mode == 'deploy':

        # 改之前同步到old备份,而不是现在
        cmd = 'cd %s; ansible-playbook %s/update.yml' %(playbook_path,name)
        print cmd

        #runplay = anplaybook('%s/update.yml' % (playbook_path), remote_user, modelname)


    elif mode == 'rollback':
        # 如果是回滚不用同步
        # runplay = anplaybook('%s/backup.yml' % (playbook_path), remote_user, modelname)
        cmd = 'cd %s; ansible-playbook %s/backup.yml' %(playbook_path,name)

    else:
        print 'ERROR NO ARGUMENT！！'

    # print test
    status1 = subprocess.check_output(cmd, shell=True)
    # status.append()
    # time.sleep(5)
    return HttpResponse(status1)


def playbook_manage(request):
    return render(request, 'new/playbook.html', {'pagename': 'playbook管理'})

def playbook_data(request):
    playbookname = serializers.serialize("json", playbook.objects.all())
    return HttpResponse(playbookname, content_type='application/json')

def playbookfile(request):
    path = request.GET.get('path')
    filename = request.GET.get('file_name')
    filepath = str(path) +'/'+ str(filename)
    print filepath
    num = request.session.get('num')
    num = filepath
    request.session['num'] = num
    f = file(filepath, 'r')
    c = f.read()
    f.close()
    return render(request, 'new/playbookfile.html', {'fileHandler1': c})

def playbook_update(request):
    return render(request, 'new/playbook_update.html', {'pagename': '配置同步'})

def playbook_run(request):
    playbook_path = request.POST['playbook_path']
    name = request.POST['file_name']
    cmd = 'cd %s; ansible-playbook %s' %(playbook_path,name)
    print cmd
    try:
        status1 = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        status1 = e.output
    return HttpResponse(status1)

def mulfile(request):
    if request.method == 'POST':
        f = request.POST.get('filename')  # 'uploadfile'与提交表单中input名一致，多个文件参见getlist()
        form = DocumentForm(request.POST, request.FILES)
        hostname = request.POST.get('hostname')

        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            return HttpResponseRedirect(reverse('mulfile'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()



    return render(
        request,
        'new/mulfile.html',
        {'pagename': '文件分发','documents': documents, 'form': form}
    )

def sendfile(request):
    if request.method == 'POST':
        f = request.POST.get('filename')  # 'uploadfile'与提交表单中input名一致，多个文件参见getlist()
        hostname = request.POST.get('hostname')

        file_e = re.compile(r'\\')
        d = file_e.split(f)
        s_filename = d[-1]

        host_e = re.compile(r',')
        host_d = host_e.split(hostname)


        for i in host_d:
            cmd = 'ansible %s -m copy -a "LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8;src=/tmp/ dest=/tmp/ mode=755 owner=coohua group=coohua' %(host_d,)


    else:
        print('POST ERROR')

    return render(
        request,
        'new/mulfile.html',
        {'pagename': '文件分发'}
    )



def mulcomm(request):
    return render(request, 'new/mulcomm.html', {'pagename': '批量命令'})


def mulshell(request):
    return render(request, 'new/mulshell.html', {'pagename': '批量脚本'})


def get_modelname(request):
    hostlist = []
    modelname = Modelname.objects.all()

    for i in modelname:
        hostname_list = {}
        hosts = []
        iname = i.name  # Modelname表里面的name字段

        get_hostlist = Hosts.objects.all().filter(Modelname=i)
        if get_hostlist:
            hostname_list['groupName'] = iname

            for j in get_hostlist:
                if j:
                    hosts.append(j.hostname)
                    # hostname_list['lists'] = j.hostname #hosts表里的hostname字段

            hostname_list['lists'] = hosts

            hostlist.append(hostname_list)  # 组合成字典

    return HttpResponse(json.dumps(hostlist), content_type='application/json')


# =========end new=======
def hosts(request):
    return render_to_response('hosts.html')


def hostlist(request):
    hosts = Hosts.objects.all()  # 查出所有hosts表的数据
    paginator = Paginator(hosts, 50)  # 每页显示50个,分页器,实例化一个分页对象
    page = request.GET.get('page')  # html传递参数page
    try:
        hosts_list = paginator.page(page)  # 当前需要显示的页
    except PageNotAnInteger:  # 如果页码不是个整数
        hosts_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        hosts_list = paginator.paginator(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'test.html', {'hosts_list': hosts_list})


def boot(request):
    return render(request, 'boot.html', )


# def search_form(request):
#     return render_to_response('search_form.html') 

def search(request):
    error = False
    if 'q' in request.GET:  # 有数据提交进来，q是变量名称
        q = request.GET['q']
        hosts = Hosts.objects.all().filter(hostname__icontains=q)
        paginator = Paginator(hosts, 200)  # 每页显示100个
        page = request.GET.get('page')
        try:
            hosts_list = paginator.page(page)
        except PageNotAnInteger:
            hosts_list = paginator.page(1)
        except EmptyPage:
            hosts_list = paginator.paginator(paginator.num_pages)
        return render(request, 'test.html', {'hosts_list': hosts_list})

    else:

        return render_to_response('test.html', {'error': error})


def index_1(request):
    hosts = Hosts.objects.all()  # 查出所有hosts表的数据
    Modelname = Modelname.objects.all()  # 服务模块总量
    paginator = Paginator(hosts, 50)  # 每页显示50个,分页器,实例化一个分页对象
    page = request.GET.get('page')  # html传递参数page
    try:
        hosts_list = paginator.page(page)  # 当前需要显示的页
    except PageNotAnInteger:  # 如果页码不是个整数
        hosts_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        hosts_list = paginator.paginator(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'index_1.html', {'hosts_list': hosts_list, 'Modelname': Modelname})


def report(request):
    hosts = Hosts.objects.all()
    services = Modelname.objects.all()
    return render(request, 'report.html', {'hosts': hosts, 'services': services})


def modelname(request):
    modelname = Modelname.objects.all()
    return render(request, 'services.html', {'services': modelname})


def services(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})


def domain(request):
    domain = Domain.objects.all()
    return render(request, 'domain.html', {'domain': domain})


def fu(request):
    return render_to_response('fu.html')


def even(request):
    return render_to_response('even.html')


# basepath=os.getcwd()+'\\dockerApp\\app\\templates\\';
def homepage(request):
    response = render_to_response("index.html");
    return response


def account_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    # print username,password
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect("/test/")
    else:
        return render_to_response('index.html', {'login_err': 'wrong username or password!'})


def data(request):
    hosts = serializers.serialize("json", Hosts.objects.all())
    print hosts
    return HttpResponse(hosts, content_type='application/json')


def json_host(request):
    return render_to_response('json_host_list.txt')


def ajax_list(request):
    hostname = request.GET['hostname2']  # 获取提交过来的数据
    item = serializers.serialize("json", iterms.objects.all().filter(hostname=hostname))  # json格式输出
    return HttpResponse(item)


def zabbix_get(request):
    itemid = request.GET['itemid']
    cmd = zabbix_api.get_history(itemid)
    return HttpResponse(min(cmd))


def ratio(request):
    iterm = iterms.objects.all()
    return render(request, 'iterms.html', {'iterm': iterm})


def item_data(request):
    items = serializers.serialize("json", iterms.objects.all())
    return HttpResponse(items, content_type='application/json')


def items(request):
    return render_to_response('items_list.html')


def online_web(request):
    return render_to_response('online.html')


def ajax_online(request):
    # pass
    modelname1 = request.GET['modelname1']  # 获取提交过来的数据
    servers = serializers.serialize("json", Hosts.objects.all().filter(Modelname__name=modelname1))  # json格式输出
    # print servers
    return HttpResponse(servers)


def online_app(request):
    # online = online.objects.all()
    mode = request.POST['mode']
    modelname = request.POST['modelname']
    version = request.POST['version']
    liplists = request.POST['liplists']
    describe = request.POST['describe']
    hostname = request.POST['hostname']
    print modelname


    deploy_dic = Modelname.objects.filter(name='%s' % (modelname)).values('deploy')
    print deploy_dic
    deploy_path = deploy_dic[0]['deploy']

    # print modelname,version,liplists,describe,hostname

    # print liplists

    e = re.compile(r',')
    host_list = e.split(hostname)
    i = ''

    eip = re.compile(r',')
    ip_list = eip.split(liplists)
    j = ''

    # 循环获取hostname，一次操作，停服务，下载包，调动本地部署程序。
    # for i in host_name:
    #     rediscomm = redis_comm(i,modelname)
    #     ip = rediscomm.getip()
    # =============openresty==============================
    # 1、去权重
    # rediscomm.drop_host()
    # 2、停服务，【supervisor的服务名称必须是hostname】
    # time.sleep(4)
    # try:
    #     svr=ServerProxy("http://user:123@%s:9001" %(ip))
    # except Exception, e:
    #     print "supervisor no run"
    # print svr.supervisor.getAllProcessInfo()
    # svr.supervisor.stopProcess(host_name)

    # 3、调动本地部署程序**本机脚本未完成，【本地脚本：①记录老版本②备份老版本 ③回滚】
    # print ip
    # runcmd = playansible('%s' %(ip),'uptime')
    # runcmd.runcmd()

    # 4、下载新包
    # wget "http://10.163.251.17:8102/%s/%s/%s-%s.war" %(modelname,version,modelname,version)
    # 如果是asp模块下的就要加一层目录。

    # runcmd = playansible('%s' %(ip),'wget -O /app/coohua/asp/webapps/alteir.war http://121.42.11.38:8120/altair/1.1/altair-1.1.war')
    # runcmd.runcmd()
    # print "runcmd------------------------------>"
    # 5、启动服务器
    # try:
    #     svr=ServerProxy("http://user:123@%s:9001" %(ip))
    # except Exception, e:
    #     print "supervisor no run"
    # print svr.supervisor.getAllProcessInfo()
    # svr.supervisor.startProcess(host_name)
    # 6、恢复权重，先要判断supervisor状态是否启动。

    # rediscomm.add_host()
    # ==================end===========================
    status = []

    file('tmp_log.txt', 'w')

    for host in host_list:
        f = file('tmp.txt', 'w+')
        f.write(host)
        f.flush()
        f.close()
        # print host
        # print modelname
        # print version
        if mode == 'deploy':
            # cmd = '/app/coohua/publish/deploy/deploy.sh %s %s' % (mode, version)
            cmd = '%s %s %s' % (deploy_path,mode,version)
        elif mode == 'rollback':
            # cmd = '/app/coohua/publish/deploy/deploy.sh %s' % (mode)
            cmd = '%s %s' % (deploy_path,mode)
        else:
            print 'ERROR NO ARGUMENT！！'

        print cmd
        runcmd = playansible('%s' % (host), cmd)
        # print runcmd
        sta = runcmd.runcmd()
        # print sta
        # f = file('tmp_log.txt', 'w+')
        # f.write(sta)
        # f.flush()
        # f.close()

        status.append(sta)

        time.sleep(2)

    # print "%s , %s, %s" %(version,modelname,describe)
    ##存入数据库
    u1 = online(models_name=modelname ,version=version ,describe=describe )
    u1.save()

    mailbox = [
    'birui@coohua.com',
    'wanglong@coohua.com',
    ]

    subject = '%s %s 上线' % (modelname,version)

    for i in mailbox:
        print i
        mail_cmd = "CMDB/scripts/mail.py '%s' '%s' '%s' " % (i,subject,describe)
        os.system(mail_cmd)
    return HttpResponse(status)


def fre_host(request):
    line_name = []
    f = file('tmp.txt', 'r')
    c = f.readlines()
    # print c
    for line in c:
        line_name.append(line)
    f.close()

    return HttpResponse(line_name)


def fre_log(request):
    line_log = []
    f = file('tmp_log.txt', 'r')
    c = f.readlines()
    # print c
    for line in c:
        line_log.append(line)
    f.close()

    return HttpResponse(line_log)


def showlog_web(request):
    return render_to_response('showlog.html')


def showlog_app(request):
    modelname = request.POST['modelname']
    filters_segment = request.POST['version']
    cmd = "scripts/playbooks/show_log.sh"
    status = subprocess.check_output(cmd + " " + modelname, shell=True)
    return HttpResponse(status)


def supervisor(request):
    # print test.server_list


    try:
        sup_backend.refresh()
    except Exception, e:

        default_err = {'err': {'statename': 'error', 'description': 'error', 'name': 'error'},}
        return render_to_response('supervisor/supervisor.html', {
            'servers_list': default_err,
        })
    else:
        # 将所有机器的supervisor控制的程序列表传给模板，字典格式
        return render_to_response('supervisor/supervisor.html', {
            'servers_list': sup_backend.server_list,
        })


def control(request):
    sup_backend.refresh()
    process_name = request.GET['name']
    action = request.GET['action']
    # print action
    # print process_name
    if action not in ('start', 'stop', 'restart','log'):
        raise Http404
    if action == 'log':
        su_id = getattr(sup_backend, 'sup_id')(process_name)
        # print '======-id---------------------->',su_id
        su_url_s= supervisor_ip.objects.filter(id=su_id).values('su_url')
        for i in su_url_s:
            url = i['su_url'] + '/logtail/' + process_name
            # print '=================url==================>',url
            return HttpResponse(url)
    else:
        getattr(sup_backend, 'action')(process_name, action)  # test实例里面的action方法对process_name进行操作
        return HttpResponse()  # TODO url reverse


class test_view(View):
    a = 1
    b = 2

    def get(self, request, *args, **kwargs):
        return HttpResponse('get')

    def test(self, request):
        return HttpResponse('test')


def openFile(request):
    path = request.GET.get('path')
    model_name = request.GET.get('model_name')
    g_model_name = request.session.get('g_model_name')
    g_model_name = model_name
    request.session['g_model_name'] = g_model_name

    num = request.session.get('num')
    num = path
    request.session['num'] = num

    # jsondata = serializers.serialize("json", config.objects.all().filter(models_name=model_name))
    # listdata = json.loads(jsondata)
    # playbook_path = listdata[0]['fields']['playbook_path']
    #
    # cmd = 'rsync -av  CMDB/scripts/playbooks/%s/roles/new/ CMDB/scripts/playbooks/%s/roles/old/' % (
    #     playbook_path, playbook_path)
    # # 调用playbook方法,实现配置文件同步。
    # status = subprocess.check_output(cmd, shell=True)

    # path of file
    line_name = []
    f = file(path, 'r')
    c = f.read()
    f.close()
    # return HttpResponse(fileHandler)
    # return render_to_response('new/updatafile.html',{'fileHandler1':c})
    return render(request, 'new/updatafile.html', {'fileHandler1': c})


def updatefile(request):
    num = request.session.get('num')
    g_model_name = request.session.get('g_model_name')

    filecent = request.POST['filecent']
    f = file(num, 'w+')
    f.write(filecent)
    f.flush()
    f.close()
    return HttpResponseRedirect('/openFile?path=%s&model_name=%s' % (num, g_model_name))


def getopen():
    page = request.GET.get('page')
    pass


def backup_config(request):
    model_name = request.GET.get('model_name')
    jsondata = serializers.serialize("json", config.objects.all().filter(models_name=model_name))
    listdata = json.loads(jsondata)
    playbook_path = listdata[0]['fields']['playbook_path']

    cmd = 'rsync -av  CMDB/scripts/playbooks/%s/roles/new/ CMDB/scripts/playbooks/%s/roles/old/' % (
        playbook_path, playbook_path)
    # 调用playbook方法,实现配置文件同步。
    status = subprocess.check_output(cmd, shell=True)
    return render_to_response('new/updatafile.html')

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'upload2.html',
        {'documents': documents, 'form': form}
    )

def redis_db(request):
    qd_hostname = dbsize.objects.all()
    for i in qd_hostname:
        qd_host=i.hostname
        bj_ip = i.bj_ip
        qd_ip = i.qd_ip
        qd_s_ip = i.qd_s_ip
        port = i.port
        #redis_db = redis_dbsize(qd_host,bj_ip,qd_ip,qd_s_ip,port)
        #redis_db.set_dbsie()
        #print i.bj_ip
    return render(
        request,
        'new/dbsize.html',
        {'hostname': qd_hostname}
    )

def mysql_db(request):
    mysql_database_name = mysql_count.objects.all()
    for i in mysql_database_name:
        db_name = i.database_name
        tb_name = i.table_name
        print db_name ,tb_name
        # mysql_db = mysql_tbsize(db_name,tb_name)
        # mysql_db.set_dbsie()
    return render(
        request,
        'new/mysqlsize.html',
        {'mysql_database': mysql_database_name}
    )
def weixin_test(request):
    return render(
        request,
        'weixin/weixin_test.html',
    )
#weixin检测web接口
def weixin_check(request):
    domain = request.GET['a']
    domain_status = {}
    p = re.compile(r'\n')
    domain_list = p.split(domain)
    sharedomain = check_share_domain()
    print domain_list
    for i in domain_list:
        status = sharedomain.weixin_domain(i)
        status = json.loads(status)
        domain_status[i] = status['msg']
    result = json.dumps(domain_status)
    return HttpResponse(result)

def chanell(request):
    return render(
        request,
        'weixin/chanell.html',
    )
#====chanell 接口========

def chanell_get(request):
    chanell_v = chanell_data.objects.all()
    sid = str(chanell_data.objects.last())
    jsondata = serializers.serialize("json", chanell_v.filter(id=sid))
    return HttpResponse(jsondata)


def chanell_check(request):
    chanell_v = chanell_data.objects.all()
    data_v = ''

    if request.method == 'POST':
        a = request.POST.get('a')
        b = request.POST.get('b')
        c = request.POST.get('c')
        d = request.POST.get('d')
        # print a,b,c,d
        data_v = chanell_data(hourly_x=a, hourly_y=b, date_a=c, date_b=d)
        data_v.save()
    return HttpResponse('OK')

def chanell_history(request):
    chanell_v = chanell_data.objects.all()
    print chanell_v
    last_id = chanell_data.objects.last()
    last_ten = []
    last_id = str(last_id)
    last_id = int(last_id)
    # print last_id

    for i in range(int(last_id) - 10,last_id + 1):
        i = int(i)
        # last_data = chanell_data.objects.filter(id=i)
        jsondata = serializers.serialize("json", chanell_v.filter(id=i))

        json_nc = json.loads(jsondata)
        json_data = json_nc[0]['fields']
        print json_data
        last_ten.append(json_data)

    return render(
        request,
        'weixin/chanell.html',
        {'last_ten': last_ten}
    )
#=====10个微信域名===========
#coohua news get share dimain
def get_share_domain_list(request):
    status_0 = {'status': 0}
    try:
        ten_domain = check_share_domain()
        # ten_domain.check_ten_domain()
        domain_lists = ten_domain.get_ten_domain()
        print domain_lists
    except Exception, e:
        # print e
        return HttpResponse(json.dumps(status_0))
    else:
        return HttpResponse(json.dumps(domain_lists))
#=====已经使用域名===========
def usedomain(request):
    #http://127.0.0.1:8000/usedomain/?domain=coohua.cn
    domain = request.GET['domain']
    status_1 = {'status':1}
    status_0 = {'status': 0}
    try:
        set_domain = check_share_domain()
        res = set_domain.set_used_domain(domain)
        print res
    except:
        return HttpResponse(json.dumps(status_0))
    else:
        if res == 1:
            return HttpResponse(json.dumps(status_1))
        else:
            return HttpResponse(json.dumps(status_0))
#=====检测接口===========
def checkdomain(request):
    # http://127.0.0.1:8000/checkdomain/?domain=coohua.cn
    domain = request.GET['domain']
    sharedomain = check_share_domain()
    res = sharedomain.weixin_domain(domain)
    return HttpResponse(res)

#=======报警接口=======

def send_message(request):
    #http://127.0.0.1:8000/send/?con=hshshshshshs
    content = request.GET['con']
    status_1 = {'status': 1}
    status_0 = {'status': 0}
    sharedomain = check_share_domain()

    mailbox = [
        'birui@coohua.com',
        'op@coohua.com',
    ]
    subject = '渠道分享信息'

    for i in mailbox:
        print i
        sharedomain.sendqqmail(i,subject,content)

    mobile_number = [
        '18600046769',
    ]

    for i in mobile_number:
        sharedomain.send_sms(i,content)

    return HttpResponse(json.dumps(status_1))
#====域名监控=====
def monitor_domain(request):
    monitordomain_v = monitordomain.objects.all()
    jsondata = serializers.serialize("json", monitordomain_v)
    json_nc = json.loads(jsondata)

    return render(
        request,
        'weixin/monitordomain.html',
        {'ck_domain': json_nc}
    )

def add_domain(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        remark = request.POST.get('remark')
        # print url,remark
        check_domain = check_share_domain()
        domain_str = check_domain.weixin_domain(url)
        json_nc = json.loads(domain_str)
        domain_status = int(json_nc['status'])
        sharedomain = check_share_domain()
        # print domain_status
        content = url
        if domain_status == -1:
            mailbox = [
                'domain_alarm@coohua.com',
            ]
            subject = '分享域名报警'

            for i in mailbox:
                print i
                sharedomain.sendqqmail(i, subject, content)

            mobile_number = [
                '18515937401',
                '18500324192',
                '18811346265',
                '15665229832',
                '18600046769',
                '18631084626',
                '15311956062',
            ]

            for i in mobile_number:
                sharedomain.send_sms(i, content)


        check_repeat = monitordomain.objects.filter(url=url,remark=remark)
        # print check_repeat
        if len(check_repeat) >= 1:
            monitordomain.objects.filter(url=url,remark=remark).update(remark=remark)
        else:
            data_v = monitordomain(url=url,weixin_status=domain_status, remark=remark)
        data_v.save()
    return HttpResponse('OK')

def drop_domain(request):
    if request.method == 'POST':
        url_l = request.POST.get('url')
        remark = request.POST.get('remark')
        content_ini = ' '.join(url_l.split())
        remark_v = ' '.join(remark.split())
        domain = content_ini.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        remark = remark_v.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        print remark,domain
        data_v = monitordomain.objects.filter(url=domain,remark=remark)
        data_v.delete()

    return HttpResponse('OK')


# def random_char(y):
#     return ''.join(random.choice(string.ascii_letters) for x in range(y))
#
# def coohua_change_share_domain(request):
#     #http://127.0.0.1:8000/send/?url=http://www.baidu.com/ss/sf/sf/ee
#     domain = request.GET['url']
#     status_1 = {'status': 1}
#     status_0 = {'status': 0}
#     content_ini = re.compile('/')
#     share_domain = content_ini.split(domain)
#     # print len(share_domain)
#     e = re.compile(r'\.')
#     t = e.split(share_domain[2])
#     coohua_domain = t[1]+'.'+t[2]
#     s_domain = random_char(5)+'.'+coohua_domain
#     uri = '/'.join(share_domain[3:])
#     url = 'http://'+s_domain+'/'+uri
#     return HttpResponse(url)

#coohua域名检测
#集合coohua share接口

#====qq域名监控=====

def monitor_qq_domain(request):
    # monitordomain_v = monitordomain_qq.objects.all().values('url','qq_statu','remark','last_date')
    monitordomain_v = monitordomain_qq.objects.all()
    jsondata = serializers.serialize("json", monitordomain_v)
    json_nc = json.loads(jsondata)

    return render(
        request,
        'weixin/qq_monitordomain.html',
        {'ck_domain': json_nc}
    )

def add_qq_domain(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        remark = request.POST.get('remark')
        # print url,remark
        # check_domain = check_share_domain()
        # domain_str = check_domain.weixin_domain(url)
        # json_nc = json.loads(domain_str)
        # domain_status = int(json_nc['status'])
        # sharedomain = check_share_domain()
        # # print domain_status
        # content = url
        # if domain_status == -1:
        #     mailbox = [
        #         'domain_alarm@coohua.com',
        #     ]
        #     subject = '分享域名报警'
        #
        #     for i in mailbox:
        #         print i
        #         sharedomain.sendqqmail(i, subject, content)
        #
        #     mobile_number = [
        #         '18515937401',
        #         '18500324192',
        #         '18811346265',
        #         '15801402572',
        #         '15665229832',
        #         '18600046769',
        #     ]
        #
        #     for i in mobile_number:
        #         sharedomain.send_sms(i, content)


        check_repeat = monitordomain_qq.objects.filter(url=url,remark=remark)
        # print check_repeat
        if len(check_repeat) >= 1:
            monitordomain_qq.objects.filter(url=url,remark=remark).update(remark=remark)
        else:
            data_v = monitordomain_qq(url=url, remark=remark)
        data_v.save()
    return HttpResponse('OK')

def drop_qq_domain(request):
    if request.method == 'POST':
        url_l = request.POST.get('url')
        remark = request.POST.get('remark')
        content_ini = ' '.join(url_l.split())
        remark_v = ' '.join(remark.split())
        domain = content_ini.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        remark = remark_v.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        # print remark,domain
        data_v = monitordomain_qq.objects.filter(url=domain,remark=remark)
        data_v.delete()

    return HttpResponse('OK')

#====qq doman monit END ====

def get_domain_1(model, count):
    ten_domain = {}
    qq_status = domain_pool.objects.filter(pool_name=model).values('qq_status')
    weixin_status = domain_pool.objects.filter(pool_name=model).values('weixin_status')
    qq_status = qq_status[0]['qq_status']
    weixin_status = weixin_status[0]['weixin_status']
    print qq_status,weixin_status
    if (qq_status == 1 and weixin_status == 0) or (qq_status == 1 and weixin_status == ''):
        with connection.cursor() as cursor:
            sql = "select domain_name,weixin_status from  CMDB_coohua_share_domain where qq_status <> -1 and res_sta = 1 and model_name = '%s' and DATE_FORMAT( last_date, '%%Y/%%m/%%d') > date_format(now(),'%%Y/%%m/%%d') limit %d;" % (model, count)
            cursor.execute(sql)
            row = cursor.fetchall()
            for i in row:
                ten_domain[i[0]] = i[1]
    elif (weixin_status == 1 and qq_status == 0) or (weixin_status == 1 and qq_status == ''):
        with connection.cursor() as cursor:
            sql = "select domain_name,weixin_status from  CMDB_coohua_share_domain where weixin_status <> -1 and res_sta = 1 and model_name = '%s' and DATE_FORMAT( last_date, '%%Y/%%m/%%d') > date_format(now(),'%%Y/%%m/%%d') limit %d;" % (model, count)
            cursor.execute(sql)
            row = cursor.fetchall()
            for i in row:
                ten_domain[i[0]] = i[1]
    elif weixin_status == 1 and qq_status == 1:
        with connection.cursor() as cursor:
            sql = "select domain_name,weixin_status from  CMDB_coohua_share_domain where weixin_status <> -1 and qq_status <> -1 and res_sta = 1 and model_name = '%s' and DATE_FORMAT( last_date, '%%Y/%%m/%%d') > date_format(now(),'%%Y/%%m/%%d') limit %d;" % (model, count)
            cursor.execute(sql)
            row = cursor.fetchall()
            for i in row:
                ten_domain[i[0]] = i[1]
    else:
        print 'Model Error !!!'

    return ten_domain

def coohua_share_count(request):

    status_0 = {'status': 0}
    domain = request.GET['name']
    count = int(request.GET['count'])
    print domain,count

    try:
        # coohua_domain = check_coohua_domain()
        # # ten_domain.check_ten_domain()
        # domain_lists = coohua_domain.get_domain(domain,count)
        # print domain_lists
        domain_lists = get_domain_1(domain,count)
        print domain_lists

    except Exception, e:
        print e
        return HttpResponse(json.dumps(status_0))
    else:
        return HttpResponse(json.dumps(domain_lists))

#导入域名接口

def domain_import_web(request):
    return render(
        request,
        'weixin/domain_import.html',
    )

def import_main(domain,mod,x,y):
    for i in domain[x:y]:
        i = i.split(',')
        i.insert(1, mod)
        print i
        insert_data = coohua_share_domain(domain_name=i[0], model_name=i[1], reg_date=i[2],last_date=i[3],
                                          Sponsoring_Registrar=i[4])
        insert_data.save()


def domain_import(request):

    if request.method == 'POST':
        domain = request.POST.get('a')

        domain = domain.split()
        print domain
        try:
            import_main(domain, 'qq', 0, 10)
            import_main(domain, 'sharewechat', 10, 30)
            import_main(domain, 'cpwechat', 30, 45)
            import_main(domain, 'sharemoment', 45, 50)
            import_main(domain, 'cpsh', 50, 90)
            import_main(domain, 'shareerweima', 90, 100)
            import_main(domain, 'h5', 100, 110)
            import_main(domain, 'h5shareerweima', 110, 115)
            import_main(domain, 'h5cpwechat', 115, 120)
            import_main(domain, 'h5sharewechat', 120, 130)

        except Exception, e:
            print e
            return HttpResponse('import error!')
        else:
            return HttpResponse('import succeed!')

#手动导入的域名优先防止微信接口失败

def manual_domain_get(request):
    chanell_v = coohua_share_domain.objects.all()
    sid = str(coohua_share_domain.objects.last())
    jsondata = serializers.serialize("json", chanell_v.filter(id=sid))
    return HttpResponse(jsondata)

def import_mudomain(domain,mod,reg,last,sre):
    insert_data = coohua_share_domain(domain_name=domain, model_name=mod, reg_date=reg, last_date=last,
                                      Sponsoring_Registrar=sre)
    insert_data.save()

def domain_muimport(request):

    if request.method == 'POST':
        domain = request.POST.get('a')

        domain = domain.split()
        print domain
        try:
            print domain
            for i in domain:
                i = i.split(',')
                import_mudomain(i[0], i[1], i[2], i[3], i[4])

        except Exception, e:
            print e
            return HttpResponse('import error!')
        else:
            return HttpResponse('import succeed!')

def show_mu_domain(request):
    chanell_v = coohua_share_domain.objects.filter(reg_date=1)
    print chanell_v
    last_id = coohua_share_domain.objects.last()
    print last_id

    last_ten = []
    last_id = str(last_id)
    last_id = int(last_id)
    # print last_id

    for i in range(0,int(last_id)+1):
        i = int(i)
        # last_data = chanell_data.objects.filter(id=i)
        try:
            jsondata = serializers.serialize("json", chanell_v.filter(id=i))
            json_nc = json.loads(jsondata)
            json_data = json_nc[0]['fields']
            # print jsondata
        except:
            pass
        else:
            last_ten.append(json_data)
        # print last_ten

    return render(
        request,
        'weixin/manual_domain.html',
        {'last_ten': last_ten}
    )

def drop_nu_domain(request):
    if request.method == 'POST':
        domain_1 = request.POST.get('domain')
        content_ini = ' '.join(domain_1.split())
        domain = content_ini.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        # print domain
        data_v = coohua_share_domain.objects.filter(domain_name=domain)
        data_v.delete()

    return HttpResponse('OK')
#=======域名池====
def domain_pool_web(request):
    # domain_count = coohua_share_domain.objects.filter(reg_date=1)
    chanell_v = domain_pool.objects.filter()
    last_id = domain_pool.objects.last()
    get_pool_name = domain_pool.objects.all().values('pool_name')
    print get_pool_name

    for i in get_pool_name:
        pool_name = i['pool_name']
        # print pool_name
        domain_list = coohua_share_domain.objects.filter(model_name=pool_name,weixin_status=1)
        domain_count = domain_list.count()
        # print domain_count
        domain_count = int(domain_count)
        domain_pool.objects.filter(pool_name=pool_name).update(domain_count=domain_count)

        # print domain_count

    last_ten = []
    last_id = str(last_id)
    try:
        last_id = int(last_id)
    except:
        last_id = 0

    for i in range(0, int(last_id) + 1):
        i = int(i)
        # last_data = chanell_data.objects.filter(id=i)
        try:
            jsondata = serializers.serialize("json", chanell_v.filter(id=i))
            json_nc = json.loads(jsondata)
            json_data = json_nc[0]['fields']
            # print json_data
        except:
            pass
        else:
            last_ten.append(json_data)
            # print last_ten
    return render(
        request,
        'weixin/domain_pool.html',
        {'last_ten': last_ten}
    )

def import_data(pool_name,pool_count,qq_status,weixin_status,remark):
    insert_data = domain_pool(pool_name=pool_name, pool_count=pool_count,qq_status=qq_status,weixin_status=weixin_status,remark=remark)
    insert_data.save()

def domainpool_import(request):
    if request.method == 'POST':
        pool = request.POST.get('pool')
        count = request.POST.get('count')
        remark = request.POST.get('remark')
        qq_status = request.POST.get('qq_status')
        weixin_status = request.POST.get('weixin_status')
        print pool,count,remark,qq_status,weixin_status
        import_data(pool,count,qq_status,weixin_status,remark)
        return HttpResponse('OK')

def drop_domain_pool(request):
    if request.method == 'POST':
        pool_name = request.POST.get('pool_name')
        content_ini = ' '.join(pool_name.split())
        pool_name = content_ini.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        data_v = domain_pool.objects.filter(pool_name=pool_name)
        data_v.delete()

    return HttpResponse('OK')

def get_pool_domain(request):
    status_0 = {'status': 0}
    dic_pool = {}
    try:
        pool = domain_pool.objects.all().values('pool_name','pool_count')
        for i in pool:
            dic_pool[i['pool_name']]=i['pool_count']
        json_pool = json.dumps(dic_pool)
    except:
        return HttpResponse(json.dumps(status_0), content_type='application/json')
    else:
        return HttpResponse(json_pool, content_type='application/json')

def updata_count(request):
    if request.method == 'POST':
        pool_count = request.POST.get('pool_count')
        pool_name = request.POST.get('pool_name')
        content_ini = ' '.join(pool_name.split())
        pool_name = content_ini.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        pool_count = int(pool_count)
        domain_pool.objects.filter(pool_name=pool_name).update(pool_count=pool_count)
        # # domain_pool.objects.filter(pool_name=pool_name).update(domain_count=domain_count)
        # print pool_name
        # print pool_count

    return HttpResponse('OK')

# def get_deny_count(request):
#     chanell_v = coohua_share_domain.objects.filter(weixin_status=-1).values('model_name','domain_name','deny_date')
#     pool_name = domain_pool.objects.values('pool_name')
#     with connection.cursor() as cursor:
#         cursor.execute("select model_name,count(domain_name) from  CMDB_coohua_share_domain where weixin_status = -1 and DATE_FORMAT( deny_date, '%Y-%m-%d') = date_sub(curdate(),interval 0 day) Group By model_name;")
#         row = cursor.fetchall()
#         print row
#     # print pool_name
#     # print chanell_v
#     return HttpResponse(row)

#=====显示域名屏蔽数=====
def show_deny(request):
    deny_model = deny_count.objects.all().values('date_time','models_name','models_count')
    tday = datetime.date.today()
    yesterday = tday - datetime.timedelta(days=1)
    dcount = deny_count.objects.all().filter(date_time='%s' %(yesterday)).values( 'models_name', 'models_count')

    return render(
        request,
        'weixin/deny_show.html',
        {'deny_model': deny_model}
    )

def get_deny_count(request):
    today_deny_count = {}
    with connection.cursor() as cursor:
        cursor.execute("select model_name,count(domain_name) from  CMDB_coohua_share_domain where weixin_status = -1 and DATE_FORMAT( deny_date, '%Y-%m-%d') = date_sub(curdate(),interval 0 day) Group By model_name;")
        row = cursor.fetchall()
        for i  in row:
            today_deny_count[i[0]] = i[1]

    json_today_deny = json.dumps(today_deny_count)

    return HttpResponse(json_today_deny)

def get_denymodel(model_name):
    model_data = []
    for i in range(7):
        time1 = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        time1 = str(time1)
        with connection.cursor() as cursor:
            cursor.execute("select count(domain_name) from CMDB_coohua_share_domain where weixin_status = -1 and DATE_FORMAT( deny_date, '%%Y-%%m-%%d') = '%s' and model_name = '%s' " %(time1,model_name))
            model_count = cursor.fetchall()
        for j in  model_count:
            str1 = j[0]
            # print str1
        model_data.append(str1)

    return model_data

def get_table_deny(request):
    pool_name = domain_pool.objects.all().values('pool_name')
    deny_data_extent = []
    dict_deny_data = {}
    pool_name_list = []
    list_sing_modle = []

    for i in range(7):
        time1 = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        deny_data_extent.append(time1)

    dict_deny_data['deny_data_extent'] = deny_data_extent

    for i in pool_name:
        dict_sing_modle = {}
        model_name = i['pool_name']
        print model_name
        pool_name_list.append(model_name)
        dict_sing_modle['name'] = model_name
        dict_sing_modle['type'] = 'line'
        dict_sing_modle['stack'] = '总量'
        dict_sing_modle['data'] = get_denymodel(model_name)
        dict_item = { 'normal': {'label' : {'show': 'true'}}}
        dict_sing_modle['itemStyle'] = dict_item
        # dict_sing_modle['smooth'] = 'true'
        list_sing_modle.append(dict_sing_modle)

    dict_deny_data['series'] = list_sing_modle
    dict_deny_data['pool_name'] = pool_name_list

    print list_sing_modle

    json_deny_data = json.dumps(dict_deny_data)

    return HttpResponse(json_deny_data)

#test--forms
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'test/name.html', {'form': form})

#======oss_upload=====
def oss_upload(request):
    return render(
        request,
        'weixin/oss/oss.html',
    )


#======spider test ===
def zaker(request,id):
    # print id
    zaker_spider_db = zaker_spider.objects.filter(id=id)
    for i in zaker_spider_db:
        title = i.title
        link = i.link
        content = i.content
        top_img = i.top_img
        author = i.author
        source_site = i.source_site

        # print title,link,content,top_img,author,source_site
        context = {'title': title, 'author': author, 'content': content, 'source_site':source_site}
    return render(request,'zaker/zaker.html',context)

#===k8s模板生成===========
def jed(request):
    return render(
        request,
        'jed/docs/index.html',
    )
#将提交的json存在为k8s.json
def ajax_jed(request):
    K8sTemplate = json.loads(request.POST['K8sTemplate'].encode('utf8'))
    k8sTemplate_dic = json.loads(K8sTemplate)
    print type(k8sTemplate_dic)
    war_name = k8sTemplate_dic['war']['war_path']
    print war_name
    war_path_src = search_maven(war_name)
    print war_path_src
    e = re.compile(r'maven/')
    war_path = e.split(war_path_src)[1].replace('\r','').replace('\n','').replace('\t','').replace(' ','_')
    print war_path
    war_url = 'http://172.16.11.1:8102/'+ war_path
    k8sTemplate_dic['war']['war_url'] = war_url
    k8sTemplate_json = json.dumps(k8sTemplate_dic)
    print k8sTemplate_json
    k8sjson = file('CMDB/scripts/playbooks/k8s/k8s.json', 'w+')
    k8sjson.write(k8sTemplate_json)
    k8sjson.flush()
    k8sjson.close()
    return HttpResponse(k8sTemplate_json)
#运行部署程序部署deployment
def k8s_playbook_run(request):
    playbook_path = 'CMDB/scripts/playbooks/k8s/site.yml'
    cmd = 'ansible-playbook %s --extra-vars "@CMDB/scripts/playbooks/k8s/k8s.json"' %(playbook_path)
    try:
        status2 = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        status2 = e.output
    return HttpResponse(status2)
#搜索war地址
def search_maven(filename):
    search_path = 'CMDB/scripts/maven/'
    cmd = 'find %s -name %s' %(search_path,filename)
    try:
        status2 = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        status2 = e.output
    return status2

