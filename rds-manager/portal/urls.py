from django.conf.urls import url, include
from . import views

urlpatterns = [

    #url(r'^$', schema_view),
    url(r'^$', views.ping),
    url(r'^health_check/$', views.RDSInstancesHealthCheck.as_view()),
    url(r'^execure_sql_command/$', views.ExecuteSQLCommand.as_view()),
    url(r'^update_tables/$', views.UpdateTables.as_view())
]
