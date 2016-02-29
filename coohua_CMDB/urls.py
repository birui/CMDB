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
    url(r'^test/$', test),
    url(r'^boot/$', boot),
    # url(r'^search-form/$', search_form),
    url(r'^search/$', search),
    url(r'^index/$', index_1),
    url(r'^report/$', report),
    url(r'^services/$', services),
    url(r'^domain/$', domain),
    url(r'^fu/$',fu),
    url(r'^even/$',even),
    url(r'login/$',account_login),
    # url(r'^hosts/$', list_detail.object_list, hosts_info),
    # url(r'^$', TemplateView.as_view(template_name='hosts_list_page.html'), name="home"),

]
