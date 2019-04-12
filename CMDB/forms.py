#coding=utf-8
from django import forms
from django.forms import ModelForm
from CMDB.models import *
from models import UploadFile

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField()
    url = forms.URLField()

class idchostsModelForm(ModelForm):
    class Meta:
        #关联表
        model = idc_hosts
        #表单中使用所有字段
        fields = '__all__'
        #列表的值
        labels = {
            "lable": "机身标签",
            "hostname":"主机名",
            "light_ip": "光口ip",
            "lan_ip": "内网ip",
            "manage_ip": "远程管理ip",
            "outer_ip": "外网ip",
            "tmp_ip": "临时ip",
            "os": "系统",
            "cpu": "cpu",
            "mem": "内存",
            "disk": "磁盘",
            "disk_health": "磁盘健康",
            "status": "机器状态",
            "rack": "机架信息",
            "brand": "品牌",
            "services": "服务",
            "remark": "备注",
        }