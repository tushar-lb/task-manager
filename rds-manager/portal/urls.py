from django.conf.urls import url, include
from . import views

urlpatterns = [

    #url(r'^$', schema_view),
    url(r'^$', views.ping),
    url(r'^verify_mulitple_instances_health_check/$', views.BatchRDSInstancesHealthCheck.as_view()),
    url(r'^verify_single_instance_health_check/$', views.RDSInstancesHealthCheck.as_view()),
    url(r'^execute_single_sql_command/$', views.ExecuteSingleSQLCommand.as_view()),
    url(r'^execute_batch_sql_command/$', views.ExecuteMultipleSQLCommand.as_view()),
    url(r'^update_tables/$', views.UpdateTables.as_view())
]
