# coding=utf-8
import os, sys
from django.shortcuts import render, render_to_response
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect, Http404
from CMDB.models import *
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
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
from CMDB.mysql_rsync.mysql_count import *

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
            'servers_list': sup_backend.server_list,
        })


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
    version = request.POST['version']
    liplists = request.POST['liplists']
    describe = request.POST['describe']
    hostname = request.POST['hostname']
    jsondata = serializers.serialize("json", config.objects.all().filter(models_name=modelname))
    listdata = json.loads(jsondata)
    playbook_path = listdata[0]['fields']['playbook_path']
    remote_user = listdata[0]['fields']['remote_user']
    path = listdata[0]['fields']['path']

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
            cmd = '/app/coohua/publish/deploy/deploy.sh %s %s' % (mode, version)
        elif mode == 'rollback':
            cmd = '/app/coohua/publish/deploy/deploy.sh %s' % (mode)
        else:
            print 'ERROR NO ARGUMENT！！'

        print cmd
        runcmd = playansible('%s' % (host), cmd)
        # print runcmd
        sta = runcmd.runcmd()
        # print sta
        f = file('tmp_log.txt', 'w+')
        f.write(sta)
        f.flush()
        f.close()

        status.append(sta)

        time.sleep(5)

    # print "%s , %s, %s" %(version,modelname,describe)
    ##存入数据库
    u1 = online(models_name=modelname ,version=version ,describe=describe )
    u1.save()

    mailbox = [
    'birui@coohua.com',
    'zhubaofeng@coohua.com',
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
    print action
    print process_name
    if action not in ('start', 'stop', 'restart'):
        raise Http404
    getattr(sup_backend, 'action')(process_name, action)  # test实例里面的action方法对process_name进行操作
    return HttpResponse(action)  # TODO url reverse


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
def weixin_check(request):

    domain = request.GET['a']
    domain_status = {}
    p = re.compile(r'\n')
    domain_list = p.split(domain)
    print domain_list
    for i in domain_list:
        print i
        response = urllib2.urlopen("http://wx.mecnss.top/wx2.php?url=%s" %(i))
        status = response.read()
        print status
        if status == '0':
            domain_status[i] = '屏蔽，域名在微信中无法访问'
        elif status == '1':
            domain_status[i] = '域名可以正常访问'
        elif status == '2':
            domain_status[i] = '域名可以正常访问 但是在网页版微信中会有提示'
        elif status == '3':
            domain_status[i] = '会提示 如需浏览，请长按网址复制后使用浏览器访问 如淘宝等网站'

    result = json.dumps(domain_status)
    print result
    return HttpResponse(result)
