# from django.conf.urls import url
import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from CMDB.views import *
# from rbac.views import *
# from django.generic import TemplateView
from django.conf.urls.static import static

# hosts_info = {
#      'hosts' : Hosts.objects.all(),
#      'template_name' : 'hosts_list_page.html',
# }


urlpatterns = [
                  # url(r'^ueditor/',include('DjangoUeditor.urls' )),
                  url(r'^rbac/', include('rbac.urls') ),
                  url(r'^$', index),
                  url(r'^admin/', admin.site.urls),
                  url(r'^hostlist/$', hostlist),
                  url(r'^boot/$', boot),
                  url(r'^search/$', search),
                  url(r'^index/$', index),
                  url(r'^report/$', report),
                  url(r'^modelname/$', modelname),
                  url(r'^domain/$', domain),
                  url(r'^fu/$', fu),
                  url(r'^even/$', even),
                  url(r'^login/$', login),
                  url(r'^hosts/$', hosts),
                  url(r'^data/$', data),
                  url(r'^ajax_list/$', ajax_list),
                  url(r'^zabbix_get/$', zabbix_get),
                  url(r'^ratio/$', ratio),
                  url(r'^items/$', items),
                  url(r'^online/$', online_web),
                  url(r'^json_host/$', json_host),
                  url(r'^showlog/$', showlog_web),
                  url(r'^showlog_app/$', showlog_app),
                  # url(r'^list/$', test_view.as_view()),
                  url(r'^new/$', new),
                  url(r'^new_hosts/$', new_hosts),
                  url(r'^new_modelname/$', new_modelname),
                  url(r'^new_domain/$', new_domain),

                  url(r'^new_report/$', new_report),
                  url(r'^ajax_config/$', ajax_config),

                  url(r'^list/$', list, name='list'),
                  url(r'^dbsize/$', redis_db),
                  url(r'^mysql_rsy/$', mysql_db),
                  url(r'^weixin/$', weixin_test),
                  url(r'^weixin_check/$', weixin_check),
                  url(r'^chanell/$', chanell),
                  url(r'^chanell_check/$', chanell_check),
                  url(r'^chanell_get/$', chanell_get),
                  url(r'^chanell_history/$', chanell_history),
                  url(r'^get_share_domain_list/$', get_share_domain_list),
                  url(r'^usedomain/$', usedomain),
                  url(r'^checkdomain/$', checkdomain),
                  url(r'^send/$', send_message),
                  url(r'^monitordomain/$', monitor_domain),
                  url(r'^add_domain/$', add_domain),
                  url(r'^drop_domain/$', drop_domain),
                  url(r'^monitordomain_qq/$', monitor_qq_domain),
                  url(r'^add_qq_domain/$', add_qq_domain),
                  url(r'^drop_qq_domain/$', drop_qq_domain),
                  url(r'^imdomain/$', domain_import_web),
                  url(r'^domain_import/$', domain_import),
                  url(r'^coohua_jusharedomain/$', coohua_share_count),
                  url(r'^domain_muimport/$', domain_muimport),
                  url(r'^show_mu_domain/$', show_mu_domain),
                  url(r'^drop_nu_domain/$', drop_nu_domain),
                  url(r'^domain_pool_web/$', domain_pool_web),
                  url(r'^domainpool_import/$', domainpool_import),
                  url(r'^drop_domain_pool/$', drop_domain_pool),
                  url(r'^get_pool_domain/$', get_pool_domain),
                  url(r'^updata_count/$', updata_count),
                  url(r'^show_deny/$', show_deny),
                  url(r'^get_deny_count/$', get_deny_count),
                  url(r'^get_table_deny/$', get_table_deny),
                  url(r'^get_name_test/$', get_name),
                  url(r'^oss_upload/$', oss_upload),
                  url(r'^zaker/([0-9]+)/$', zaker),
                  url(r'^flushcdn/$', flushcdn),
                  url(r'^flushcdn_act/$', flushcdn_act),
                  url(r'^flushcdn_dr/$', flushcdn_dr),
                  url(r'^flushcdn_dr_act/$', flushcdn_dr_act),
                  url(r'^qiniuflushcdn/$', qiniuflushcdn),
                  url(r'^qiniuflushcdn_act/$', qiniuflushcdn_act),
                  url(r'^qiniuflushcdn_dr/$', qiniuflushcdn_dr),
                  url(r'^qiniuflushcdn_dr_act/$', qiniuflushcdn_dr_act),
                  url(r'^RefreshQuota/$', RefreshQuota),

                  url(r'^new_online/$', new_online_web),
                  url(r'^new_online/fre_host/$', fre_host),
                  url(r'^new_online/fre_log/$', fre_log),
                  url(r'^new_online/get_modelname/$', get_modelname),
                  url(r'^new_online/ajax_online/$', ajax_online),
                  url(r'^new_online/online_app/$', online_app),

                  url(r'^k8s_img/$', k8s_img),
                  url(r'^k8s_img/get_k8s_modelname/$', get_k8s_modelname),
                  url(r'^k8s_img/k8s_dockerfile/$', k8s_dockerfile),
                  url(r'^k8s_img/k8s_dockerfile_act/$', k8s_dockerfile_act),

                  url(r'^jed/$', jed),
                  url(r'^jed/ajax_jed/$', ajax_jed),
                  url(r'^jde/k8s_playbook_run/$', k8s_playbook_run),

                  url(r'^nginx_jed/$', nginx_jed),
                  url(r'^nginx_jed/ajax_jed/$', ajax_jed),
                  url(r'^nginx_jed/k8s_playbook_run/$', k8s_playbook_run),

                  url(r'^k8s_deploy/$', k8s_deploy_web),
                  url(r'^k8s_deploy/get_k8s_modelname/$', get_k8s_modelname),
                  url(r'^k8s_deploy/ajax_k8s_deploy/$', ajax_k8s_deploy),
                  url(r'^k8s_deploy/k8s_deploy_action/$', k8s_deploy_action),

                  url(r'^new_supervisor/$', new_supervisor),
                  # url(r'^supervisor_server/$', supervisor_server),
                  # url(r'^get_supervisor_ip/$', get_supervisor_ip),
                  url(r'^new_supervisor/supervisor_api/$', supervisor_api),
                  # url(r'^supervisor/$', supervisor),
                  url(r'^new_supervisor/control/$', control),

                  url(r'^mulfile/$', mulfile, name='mulfile'),
                  url(r'^mulfile/get_modelname/$', get_modelname),
                  url(r'^mulfile/sendfile/$', sendfile),

                  url(r'^mulcomm/$', mulcomm),
                  url(r'^mulcomm/get_modelname/$', get_modelname),

                  url(r'^mulshell/$', mulshell),
                  url(r'^mulshell/get_modelname/$', get_modelname),

                  url(r'^new_items/$', new_items),
                  url(r'^new_items/item_data/$', item_data),

                  url(r'^config_manage/$', config_manage),
                  url(r'^config_manage/openFile/$', openFile),
                  url(r'^config_manage/config_data/$', config_data),
                  url(r'^config_manage/config_update/$', config_update),
                  url(r'^config_manage/config_syn/$', config_syn),
                  url(r'^config_manage/backup_config/$', backup_config),
                  url(r'^config_manage/updatefile/$', updatefile),

                  url(r'^playbook_manage/$', playbook_manage),
                  url(r'^playbook_manage/updatefile/$', updatefile),
                  url(r'^playbook_manage/playbook_data/$', playbook_data),
                  url(r'^playbook_manage/playbookfile/$', playbookfile),
                  url(r'^playbook_manage/playbook_update/$', playbook_update),
                  url(r'^playbook_manage/playbook_run/$', playbook_run),

                  url(r'^idc/$', idc),
                  url(r'^idc/new/$', idc_new),
                  url(r'^idc/edit/(?P<id>\d+)/$', idc_edit),
                  url(r'^idc/delete/(?P<id>\d+)/$', idc_delete),
                #websocket test
                  url(r'^path', path),
                  url(r'^test_path/$', test_path),
                #ghost
                  url(r'^ghost/$',ghost),
                  url(r'^ghost/ghost_act/$',ghost_act),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
