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

#展示规则，应用到下面显示
class OlineAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('models_name', 'date_time', 'version','describe')
    #指定列表过滤器,页面右边
    list_filter = ('models_name',)
    # 指定要搜索的字段
    search_fields = ('models_name','date_time',)

class HostAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('hostname', 'lip','remark')
    #指定列表过滤器,页面右边
    list_filter = ('hostname',)
    # 指定要搜索的字段
    search_fields = ('hostname','lip',)

class configAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('name', 'models_name','path','date_time','describe','remote_user','playbook_path')
    #指定列表过滤器,页面右边
    list_filter = ('models_name',)
    # 指定要搜索的字段
    search_fields = ('models_name','name',)

class dbsizeAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('hostname', 'bj_ip','qd_ip','qd_s_ip','port','qd_size','bj_size',)
    #指定列表过滤器,页面右边
    list_filter = ('hostname',)
    # 指定要搜索的字段
    search_fields = ('hostname', 'bj_ip','qd_ip',)

class mysql_countAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('database_name','table_name', 'bj_table_size','qd_table_size',)
    #指定列表过滤器,页面右边
    list_filter = ('table_name',)
    # 指定要搜索的字段
    search_fields = ('table_name', 'bj_table_size','qd_table_size',)

class share_domain_show(admin.ModelAdmin):
    #显示字段
    list_display = ('domain_name','reg_date', 'last_date','weixin_status','deny_date','use_date','res_sta','Sponsoring_Registrar')
    #指定列表过滤器,页面右边
    list_filter = ('domain_name',)
    # 指定要搜索的字段
    search_fields = ('domain_name', 'reg_date','weixin_status',)

class nmonitordomain_show(admin.ModelAdmin):
    #显示字段
    list_display = ('url','weixin_status', 'last_date','weixin_status','remark','deny_time')
    #指定列表过滤器,页面右边
    list_filter = ('url',)
    # 指定要搜索的字段
    search_fields = ('url', 'last_date','weixin_status',)

class coohua_share_domain_show(admin.ModelAdmin):
    #显示字段
    list_display = ('domain_name','model_name','reg_date', 'last_date','weixin_status','qq_status','deny_date','use_date','res_sta','Sponsoring_Registrar')
    #指定列表过滤器,页面右边
    list_filter = ('model_name',)
    # 指定要搜索的字段
    search_fields = ('domain_name','model_name', 'deny_date','weixin_status',)

class coohua_domain_pool_show(admin.ModelAdmin):
    #显示字段
    list_display = ('pool_name','pool_count','date_time', 'domain_count','remark','qq_status','weixin_status')
    #指定列表过滤器,页面右边
    list_filter = ('pool_name',)
    # 指定要搜索的字段
    search_fields = ('pool_name', 'remark',)

#admin里面显示哪些表：
admin.site.register(Brothers)
admin.site.register(History)
admin.site.register(Hosts,HostAdmin)
admin.site.register(Server,ServerAdmin)
admin.site.register(Modelname,ServicesAdmin)
admin.site.register(Domain)
admin.site.register(iterms)
admin.site.register(online,OlineAdmin)
admin.site.register(config,configAdmin)
admin.site.register(dbsize,dbsizeAdmin)
admin.site.register(mysql_count,mysql_countAdmin)
admin.site.register(share_domain,share_domain_show)
admin.site.register(monitordomain,nmonitordomain_show)
admin.site.register(chanell_data)
admin.site.register(coohua_share_domain,coohua_share_domain_show)
admin.site.register(domain_pool,coohua_domain_pool_show)