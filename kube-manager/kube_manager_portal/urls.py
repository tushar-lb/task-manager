from django.conf.urls import url, include
from . import views

urlpatterns = [

    #url(r'^$', schema_view),
    url(r'^$', views.ping),
    url(r'^list_cluster_nodes/$', views.ListClusterNodes.as_view()),
    url(r'^list_cluster_pods/$', views.ListClusterNodesPods.as_view())
]
