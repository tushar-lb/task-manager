from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, \
    StreamingHttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
import json
from rest_framework.schemas import AutoSchema
import coreapi
import os
import logging
import inspect
from kube_manager_portal.cluster import Orchestration
from  kube_manager_portal.utils import *

logging.basicConfig(filename='/tmp/cluster-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def ping(request):
    response_to = {"success":True, "message":"Pong"}
    return JsonResponse(response_to)

class ListClusterNodes(APIView):
    def get(self, request, format=None):
        """
        List of nodes in the kubernetes cluster
        """
        orch_method = Orchestration('kubernetes')
        k8s_cluster_nodes = orch_method.orch_layer.get_nodes()
        if k8s_cluster_nodes:
            response_to = {"success":True, "data":k8s_cluster_nodes, "message":"Cluster nodes fetched successfully."}
        else:
            response_to = {"success":False, "data":k8s_cluster_nodes, "message":"Failed to fetch cluster nodes details."}
        return JsonResponse(response_to)

class ListClusterNodesPods(APIView):
    def get(self, request, format=None):
        """
        List of pods of all nodes in the kubernetes cluster
        """
        orch_method = Orchestration('kubernetes')
        k8s_nodes_pods = orch_method.orch_layer.get_details_pods_in_cluster()
        if k8s_nodes_pods:
            response_to = {"success":True, "data":k8s_nodes_pods, "message":"Cluster nodes and all pods details fetched successfully."}
        else:
            response_to = {"success":False, "data":k8s_nodes_pods, "message":"Failed to fetch cluster nodes and all pods details."}
        return JsonResponse(response_to)
