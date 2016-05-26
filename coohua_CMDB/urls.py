#from django.conf.urls import url
from django.conf.urls import patterns, include, url
from django.contrib import admin
from CMDB.views import *
from django.views.generic import TemplateView

# hosts_info = {
#      'hosts' : Hosts.objects.all(),
#      'template_name' : 'hosts_list_page.html',
# }


urlpatterns = [
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
    
    #url(r'^add/$',add),
    #url(r'^test1/$',test1),
    # url(r'^hosts/$', list_detail.object_list, hosts_info),
    # url(r'^$', TemplateView.as_view(template_name='hosts_list_page.html'), name="home"),

]
