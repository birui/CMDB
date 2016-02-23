#coding=utf-8
from django.contrib import admin
from CMDB.models import *
# Register your models here.

class ServicesAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('name', 'lead', 'remark')
    #指定列表过滤器,页面右边
    list_filter = ('lead',)
    # 指定要搜索的字段
    search_fields = ('name',)

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

#admin里面显示哪些表：
admin.site.register(Brothers)
admin.site.register(History)
admin.site.register(Hosts)
admin.site.register(Server,ServerAdmin)
admin.site.register(Services,ServicesAdmin)
admin.site.register(Domain)