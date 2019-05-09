#coding=utf-8
from __future__ import unicode_literals
from django.db import models
from DjangoUeditor.models import UEditorField
from django.conf import settings
from django import forms
import rbac.models

class Modelname(models.Model):
    """
    按业务划分的服务器组信息
    每个项目的own对应的是用户
    """
    name = models.CharField(max_length=70)
    lead = models.CharField(max_length=50)
    own = models.ManyToManyField(rbac.models.UserInfo, null=True, blank=True)
    remark = models.CharField(max_length=250)
    deploy = models.CharField(max_length=250,default='/app/coohua/publish/deploy/deploy.sh')
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
    Modelname = models.ManyToManyField(Modelname,blank=True)
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
    """
    业务own,每个人可以对应多个业务
    """
    name = models.CharField(max_length=20)
    #1研发
    department = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20,blank=True)
    service = models.ManyToManyField(Modelname)
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
    service_model = models.ForeignKey(Modelname,blank=True)
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
    cpu_itemid = models.IntegerField(default=1)
    cpu_idle = models.FloatField(default=1)
    cpu_graphs_itemsid = models.IntegerField(default=1)
    eth0_graphs_itemsid = models.IntegerField(default=1)
    eth1_graphs_itemsid = models.IntegerField(default=1)
    memory_total_itemsid = models.IntegerField(default=1)
    memory_total = models.FloatField(default=1.0)
    memory_available_itemsid = models.IntegerField(default=1)
    memory_available = models.FloatField(default=1.0)
    eth0_in_itemsid = models.IntegerField(default=1)
    eth0_in = models.FloatField(default=1.0)
    eth0_out_itemsid = models.IntegerField(default=1)
    eth0_out = models.FloatField(default=1.0)
    eth1_in_itemsid = models.IntegerField(default=1)
    eth1_in = models.FloatField(default=1.0)
    eth1_out_itemsid = models.IntegerField(default=1)
    eth1_out = models.FloatField(default=1.0)
    cpu_load_itemsid= models.IntegerField(default=1)
    cpu_load = models.FloatField(default=1.0)

    def __unicode__(self):
       return str(self.hostname) #返回的数据
       # return self.hostname

class host_metrics(models.Model):
    instance_id = models.CharField(blank=True, max_length=100)
    hostname = models.CharField(blank=True, max_length=100)
    memory = models.IntegerField(default=1)
    cpu_max_percent = models.IntegerField(default=1)
    loadaverage_max = models.IntegerField(default=1)
    memory_max_percent = models.IntegerField(default=1)
    wlan_max_in = models.IntegerField(default=1)
    wlan_max_out = models.IntegerField(default=1)
    lan_max_in = models.IntegerField(default=1)
    lan_max_out = models.IntegerField(default=1)

class online(models.Model):
    models_name = models.CharField(blank=True,max_length=20)
    version = models.CharField(blank=True,max_length=20)
    describe = models.CharField(blank=True,max_length=250)
    date_time = models.DateTimeField(auto_now_add = True)

    # def __unicode__(self):
    #    return str(self.models_name)

class config(models.Model):
    name = models.CharField(blank=True,max_length=50,null=True)
    models_name = models.CharField(blank=True,max_length=50)
    path = models.CharField(blank=True,max_length=100)
    describe = models.CharField(blank=True,max_length=250)
    date_time = models.DateTimeField(auto_now_add=True,)
    remote_user = models.CharField(blank=True, max_length=50)
    playbook_path = models.CharField(blank=True, max_length=250)
    # def __unicode__(self):
    #     return self.models_name
    # class Meta:
    #     ordering = ['models_name']

class playbook(models.Model):
    name = models.CharField(blank=True,max_length=50,null=True)
    playbook_path = models.CharField(blank=True, max_length=250)
    describe = models.CharField(blank=True,max_length=250)
    date_time = models.DateTimeField(auto_now_add=True,)



class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class UploadFile(models.Model):
	file = models.FileField(upload_to='files/%Y/%m/%d')

#上传作品表:作品名称，用户名
class Upload(models.Model):
    #注意这里的用户名是FileField类型
    name = models.FileField(upload_to = './upload/')
    username = models.CharField(max_length = 20)
    def __str__(self):
        return self.name

class dbsize(models.Model):
    hostname = models.CharField(max_length=50)
    port = models.IntegerField(blank=True,null=True)
    bj_ip = models.CharField(max_length=50,blank=True)
    qd_ip = models.CharField(max_length=50, blank=True)
    qd_s_ip = models.CharField(max_length=50, blank=True,default=0)
    qd_s_wip = models.CharField(max_length=50, blank=True, default=0)
    qd_s_size = models.CharField(max_length=50, blank=True,default=0)
    qd_size = models.IntegerField(blank=True,null=True,default=0)
    bj_size = models.IntegerField(blank=True,null=True,default=0)
    bj_status = models.CharField(blank=True,max_length=50,null=True)
    diff_size = models.IntegerField(blank=True, null=True,default=0)

    def __unicode__(self):
        return str(self.hostname)

class mysql_count(models.Model):
    database_name = models.CharField(max_length=50)
    table_name = models.CharField(max_length=50)
    qd_table_size = models.IntegerField(blank=True,null=True,default=0)
    bj_table_size = models.IntegerField(blank=True,null=True,default=0)
    diff_size = models.IntegerField(blank=True, null=True,default=0)

    def __unicode__(self):
        return str(self.table_name)

class chanell_data(models.Model):
    hourly_x = models.IntegerField(blank=True,null=True)
    hourly_y = models.IntegerField(blank=True,null=True)
    date_a = models.IntegerField(blank=True,null=True)
    date_b = models.IntegerField(blank=True,null=True)
    date_time = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return str(self.id)

class share_domain(models.Model):
    domain_name = models.CharField(max_length=100)
    reg_date = models.CharField(max_length=50,blank=True,null=True)
    last_date = models.CharField(max_length=50,blank=True,null=True)
    #1正常,-1被封
    weixin_status = models.IntegerField(blank=True,null=True)
    deny_date = models.CharField(max_length=50,blank=True,null=True)
    use_date = models.CharField(max_length=50,blank=True,null=True)
    #1正常 -1未解析
    res_sta = models.IntegerField(blank=True,null=True)
    Sponsoring_Registrar = models.CharField(max_length=50, blank=True, null=True)
    def __unicode__(self):
        return str(self.domain_name)

class monitordomain(models.Model):
    url = models.CharField(max_length=100)
    #1正常,-1被封
    weixin_status = models.IntegerField(blank=True,null=True)
    qq_statu = models.IntegerField(blank=True, null=True ,default=1)
    remark = models.CharField(max_length=200)
    last_date = models.DateTimeField(auto_now_add = True)
    deny_time = models.CharField(max_length=50,blank=True,null=True)
    qq_deny_time = models.CharField(max_length=50, blank=True, null=True)
    def __unicode__(self):
        return str(self.id)
class monitordomain_qq(models.Model):
    url = models.CharField(max_length=100)
    #1正常,-1被封
    qq_statu = models.IntegerField(blank=True, null=True ,default=1)
    remark = models.CharField(max_length=200)
    last_date = models.DateTimeField(auto_now_add = True)
    qq_deny_time = models.CharField(max_length=50, blank=True, null=True)
    def __unicode__(self):
        return str(self.id)

class coohua_share_domain(models.Model):
    domain_name = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    #当长期和短期用了,0长期,1短期
    reg_date = models.CharField(max_length=50,blank=True,null=True)
    last_date = models.CharField(max_length=50,blank=True,null=True)
    #1正常,-1被封
    weixin_status = models.IntegerField(blank=True,null=True)
    qq_status = models.IntegerField(blank=True,null=True)
    deny_date = models.CharField(max_length=50,blank=True,null=True)
    use_date = models.CharField(max_length=50,blank=True,null=True)
    #1正常 -1未解析
    res_sta = models.IntegerField(blank=True,null=True)
    Sponsoring_Registrar = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)


class domain_pool(models.Model):
    pool_name = models.CharField(max_length=100)
    pool_count = models.IntegerField(blank=True,null=True)
    date_time = models.DateTimeField(auto_now_add = True)
    domain_count = models.IntegerField(blank=True,null=True)
    #1检测或0不检测
    qq_status = models.IntegerField(blank=True, null=True)
    weixin_status = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=200)

    def __unicode__(self):
        return str(self.id)

class deny_count(models.Model):
    models_name = models.CharField(max_length=100)
    models_count = models.IntegerField(blank=True, null=True)
    date_time = models.CharField(max_length=20)
    cost_count = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

class zaker_spider(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    top_img = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    source_site = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.id)

class ngx_ip(models.Model):
    domain = models.CharField(max_length=200)
    ip = models.GenericIPAddressField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return str(self.id)

class ngx_api(models.Model):
    domain = models.CharField(max_length=200)
    api = models.CharField(max_length=200)
    num = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return str(self.id)

class supervisor_ip(models.Model):
    su_hostname = models.CharField(max_length=200)
    su_url = models.CharField(max_length=200)
    # su_hostname = models.CharField(max_length=200)
    # su_ip = models.GenericIPAddressField()
    # su_port = models.IntegerField(blank=True, null=True)
    # su_user = models.CharField(max_length=200)
    # su_password = models.CharField(max_length=200)
    su_remark = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.id)

class k8s_depoloy(models.Model):
    GENDER_CHOICES=(
        (1,'war'),
        (2,'jar'),
        )
    name = models.CharField(max_length=70)
    lead = models.CharField(max_length=50,blank=True,null=True)
    #ansible参数文件位置
    json_path = models.CharField(max_length=200,default='CMDB/scripts/playbooks/k8s/vars-json/')
    img_address = models.CharField(max_length=250,default='registry-vpc.cn-beijing.aliyuncs.com/coohua_img/')
    #不包含version的镜像名称
    image = models.CharField(max_length=100,blank=True,null=True)
    #镜像版本
    img_version = models.CharField(max_length=20 ,blank=True,null=True)
    bagtype = models.IntegerField(choices=GENDER_CHOICES,default=1)
    # war包在maven目录路径到版本号上层
    war_path = models.CharField(max_length=200,blank=True,null=True)
    war_name = models.CharField(max_length=20,blank=True,null=True)
    remark = models.CharField(max_length=250,blank=True,null=True)
    def __unicode__(self):
        return self.name
class clear_log(models.Model):
    group_name = models.CharField(max_length=50)
    log_path = models.CharField(max_length=200)
    keep_date = models.IntegerField(blank=True, null=True,default=3)
    recycled_date = models.IntegerField(blank=True, null=True, default=7)

class idc_hosts(models.Model):
    """
    线下IDC信息汇总表:
    lable        机身标签
    hostname      主机名
    light_ip      光口ip
    lan_ip        内网ip
    manage_ip     远程管理ip
    outer_ip      外网ip
    tmp_ip        临时ip
    os             系统
    cpu            cpu
    mem            内存
    disk           磁盘
    disk_health    磁盘健康
    status         机器状态，是否在运行
    rack           机架信息
    brand          品牌
    services       服务
    remark         备注
    """
    lable = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    light_ip = models.GenericIPAddressField(blank=True, null=True)
    lan_ip= models.GenericIPAddressField(blank=True, null=True)
    manage_ip = models.GenericIPAddressField(blank=True, null=True)
    outer_ip = models.GenericIPAddressField(blank=True, null=True)
    tmp_ip = models.GenericIPAddressField(blank=True, null=True)
    os = models.CharField(blank=True,max_length=50)
    cpu = models.IntegerField(blank=True,null=True,default=0)
    mem = models.IntegerField(blank=True,null=True,default=0)
    disk = models.CharField(blank=True,max_length=200)
    disk_health = models.CharField(blank=True,max_length=20)
    status = models.CharField(blank=True,max_length=20)
    rack  = models.CharField(blank=True,max_length=20)
    brand = models.CharField(blank=True, max_length=20)
    services = models.CharField(blank=True, max_length=50)
    remark = models.CharField(max_length=200, blank=True, null=True)
    def __unicode__(self):
        return self.lable


