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
from kube_manager_portal.utils import *

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

class ManageMultipleResources(APIView):
    def post(self, request, format=None):
        """
        Update running resources with user provided spec.
        """
        orch_method = Orchestration('kubernetes')
        file_obj = request.FILES['file']
        filename = '/tmp/' + file_obj.name
        destination = open(filename, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
        if os.path.exists(filename):
            resource_update_status = orch_method.orch_layer.update_resources(filename)
            if resource_update_status is True:
                response_to = {"success":True, "data":resource_update_status, "message":"Requested resources uploaded successfully."}
            else:
                response_to = {"success":False, "data":resource_update_status, "message":"Failed to update requested resources."}
        else:
            response_to = {"success":False, "data":filename, "message":"Failed to upload file."}
        return JsonResponse(response_to)

class ManageIndividualResources(APIView):
    def post(self, request, format=None):
        """
        Update user requested resources
        """
        orch_method = Orchestration('kubernetes')
        content = json.loads(request.body)
        namespace = content.get("namespace")
        resource_name = content.get("resource_name")
        resource_type = content.get("resource_type")
        logging.info("Namespace: %s, resource name: %s, resource type: %s" % (namespace, resource_name, resource_type))
        if resource_type in ["deployment", "statefulset"]:
            operation = content.get("operation")
            if operation == "scale":
                scale_value = content.get("scale_value")
                if scale_value > 0:
                    scale_resource_status = orch_method.orch_layer.scale_resources(namespace, resource_name, resource_type, scale_value)
                    if scale_resource_status is True:
                        response_to = {"success":True, "status":scale_resource_status, "message":"resource updated successfully."}
                    else:
                        response_to = {"success":False, "status":scale_resource_status, "message":"failed to update requested resources."}
                else:
                    logging.info("Invalid input scale value: %s" % scale_value)
                    response_to = {"success":False, "message":"provide valid scale value."}
            elif operation == "image_update":
                image_name = content.get("image_name")
                if image_name:
                    image_update_status = orch_method.orch_layer.set_image(namespace, resource_name, resource_type, image_name)
                    if image_update_status is True:
                        response_to = {"success":True, "status":scale_resource_status, "message":"resource updated successfully."}
                    else:
                        response_to = {"success":False, "status":scale_resource_status, "message":"failed to update requested resources."}
                else:
                    response_to = {"success":False, "message":"provide valid image name."}
            else:
                response_to = {"success":False, "message":"Invalid request"}
        elif resource_type in ["configmap"]:
            key = content.get("key")
            value = content.get("value")
            configmap_update_status = orch_method.orch_layer.update_configmap(namespace, resource_name, key, value)
            if configmap_update_status is True:
                response_to = {"success":True, "status":scale_resource_status, "message":"resource updated successfully."}
            else:
                response_to = {"success":False, "status":scale_resource_status, "message":"failed to update requested resources."}
        else:
            response_to = {"success":False, "message":"Invalid request"}
        return JsonResponse(response_to)

class DeployServicesOnDifferentNodes(APIView):
    def post(self, request, format=None):
        """
        Deploy services on different nodes
        """
        orch_method = Orchestration('kubernetes')
        file_obj = request.FILES['file']
        filename = '/tmp/' + file_obj.name
        destination = open(filename, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
        if os.path.exists(filename):
            modify_spec_status, modified_file = orch_method.orch_layer.modify_service_spec(filename)
            logging.info("Modified spec status: %s, Modified file name: %s" % (modify_spec_status, modified_file))
            resource_update_status = orch_method.orch_layer.update_resources(modified_file)
            if resource_update_status is True:
                response_to = {"success":True, "data":resource_update_status, "message":"Service deployed successfully."}
            else:
                response_to = {"success":False, "data":resource_update_status, "message":"Failed to deploy service."}
        else:
            response_to = {"success":False, "data":filename, "message":"Failed to upload file."}
        return JsonResponse(response_to)

class PodsUtilization(APIView):
    def get(self, request, format=None):
        """
        Returns list of pods which are under heavy load and underperforming 
        """
        orch_method = Orchestration('kubernetes')
        pods_details = orch_method.orch_layer.get_heavy_loaded_pod_details()
        if pods_details:
            response_to = {"success":True, "data":pods_details, "message":"Successfully fetched first 10 heavy utilized pods."}
        else:
            response_to = {"success":False, "data":pods_details, "message":"Failed to fetch pods details."}
        return JsonResponse(response_to)
