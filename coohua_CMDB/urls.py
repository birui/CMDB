#from django.conf.urls import url
import settings  
from django.conf.urls import patterns, include, url
from django.contrib import admin
from CMDB.views import *
from django.views.generic import TemplateView

# hosts_info = {
#      'hosts' : Hosts.objects.all(),
#      'template_name' : 'hosts_list_page.html',
# }


urlpatterns = [
    # url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^$',homepage),
    url(r'^admin/', admin.site.urls),
    url(r'^hostlist/$', hostlist),
    url(r'^boot/$', boot),
    # url(r'^search-form/$', search_form),
    url(r'^search/$', search),
    url(r'^index/$', index_1),
    url(r'^report/$', report),
    url(r'^services/$', services),
    url(r'^domain/$', domain),
    url(r'^fu/$',fu),
    url(r'^even/$',even),
    url(r'^login/$',account_login),
    url(r'^hosts/$',hosts),
    url(r'^data/$',data),
    url(r'^ajax_list/$',ajax_list),
    url(r'^zabbix_get/$',zabbix_get),
    url(r'^ratio/$',ratio),
    url(r'^items/$',items),
    url(r'^online/$',online_web),
    url(r'^online_app/$',online_app),
    url(r'^json_host/$',json_host),
    url(r'^item_data/$',item_data),
    url(r'^showlog/$',showlog_web),
    url(r'^showlog_app/$',showlog_app),
    url(r'^supervisor/$',supervisor),
    url(r'^control/$',control),
    url(r'^ajax_online/$',ajax_online),
    # url(r'^col/$',online_app.col),
    #url(r'^control/(?P<server>[a-z0-9\.]+)/(?P<process>[a-z:_-]+)/(?P<action>[a-z]+)/$',control),
    #url(r'^query/$',query),
    
    #url(r'^add/$',add),
    #url(r'^test1/$',test1),
    # url(r'^hosts/$', list_detail.object_list, hosts_info),
    # url(r'^$', TemplateView.as_view(template_name='hosts_list_page.html'), name="home"),

]
