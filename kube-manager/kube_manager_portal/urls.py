from django.conf.urls import url, include
from . import views

urlpatterns = [

    #url(r'^$', schema_view),
    url(r'^$', views.ping),
    url(r'^list_cluster_nodes/$', views.ListClusterNodes.as_view()),
    url(r'^list_cluster_pods/$', views.ListClusterNodesPods.as_view()),
    url(r'^manage_mulitple_resources/$', views.ManageMultipleResources.as_view()),
    url(r'^manage_individual_resources/$', views.ManageIndividualResources.as_view()),
    url(r'^deploy_services/$', views.DeployServicesOnDifferentNodes.as_view()),
    url(r'^get_pods_utilization/$', views.PodsUtilization.as_view())
]   
