#coding=utf-8
from django.contrib import admin
from CMDB.models import *
# Register your models here.

class ServicesAdmin(admin.ModelAdmin):
    #显示字段
    list_display = ('name', 'lead', 'deploy','remark')
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
    list_display = ('url','weixin_status', 'last_date','weixin_status','qq_statu','remark','deny_time','qq_deny_time')
    #指定列表过滤器,页面右边
    list_filter = ('url',)
    # 指定要搜索的字段
    search_fields = ('url', 'last_date','weixin_status','qq_statu')

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

class monitordomain_qq_show(admin.ModelAdmin):
    #显示字段
    list_display = ('url','qq_statu','remark','qq_deny_time','last_date')
    #指定列表过滤器,页面右边
    list_filter = ('url','qq_statu')
    # 指定要搜索的字段
    search_fields = ('url', 'last_date','qq_status')

class ngx_ip_show(admin.ModelAdmin):
    #显示字段
    list_display = ('domain','ip','num')
    #指定列表过滤器,页面右边
    list_filter = ('domain','ip')
    # 指定要搜索的字段
    search_fields = ('domain', 'ip')

class ngx_api_show(admin.ModelAdmin):
    #显示字段
    list_display = ('domain','api','num')
    #指定列表过滤器,页面右边
    list_filter = ('domain','api')
    # 指定要搜索的字段
    search_fields = ('domain', 'api')

class supervisor_ip_show(admin.ModelAdmin):
    #显示字段
    list_display = ('su_hostname','su_url','su_remark')
    #指定列表过滤器,页面右边
    list_filter = ('su_hostname','su_url')
    # 指定要搜索的字段
    search_fields = ('su_hostname', 'su_url')

class playbook_show(admin.ModelAdmin):
    #显示字段
    list_display = ('name','playbook_path','describe','date_time')
    #指定列表过滤器,页面右边
    list_filter = ('name',)
    # 指定要搜索的字段
    search_fields = ('name', 'describe')

class k8s_depoloy_show(admin.ModelAdmin):
    #显示字段
    list_display = ('name','lead','json_path','img_address','image','img_version','war_path','war_name','remark')
    #指定列表过滤器,页面右边
    list_filter = ('name',)
    # 指定要搜索的字段
    search_fields = ('name', 'lead','image')

class clear_log_show(admin.ModelAdmin):
    #显示字段
    list_display = ('group_name','log_path','keep_date','recycled_date')
    #指定列表过滤器,页面右边
    list_filter = ('group_name',)
    # 指定要搜索的字段
    search_fields = ('group_name',)

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
admin.site.register(monitordomain_qq,monitordomain_qq_show)
admin.site.register(ngx_ip,ngx_ip_show)
admin.site.register(supervisor_ip,supervisor_ip_show)
admin.site.register(playbook,playbook_show)
admin.site.register(k8s_depoloy,k8s_depoloy_show)
admin.site.register(clear_log,clear_log_show)