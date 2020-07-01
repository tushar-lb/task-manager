import traceback
import os
from kubernetes import client, config
import logging
import time
import json
import yaml
import uuid
import subprocess
import ruamel.yaml
from ruamel.yaml import YAML
import inspect
import platform


logging.basicConfig(filename='/tmp/cluster-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Kubernetes():
    def __init__(self):
        """
        Kubernetes defaults
        """
        self.config_file="/Users/tusharraut/git/go/src/github.com/portworx/2_central.yaml"
        """
        try:
            logging.info("Loading Kubernetes config from incluster")
            config.load_incluster_config()
        except Exception as ex:
            logging.error("Failed to initialize kubernete configuration %s" % ex)
        """
        if os.path.exists(self.config_file):
            config.load_kube_config(config_file=self.config_file)

    def get_kube_api(self):
        '''
        Return the kube API handler
        '''
        try:
            v1 = client.CoreV1Api()
            return v1
        except Exception as ex:
            logging.error("Exception caught while fetching k8s instance.")
            logging.error(traceback.print_exc())

    def get_nodes(self, request_ip=None):
        """
        Return no of nodes in cluster
        """
        nodes_details = []
        try:
            v1 = self.get_kube_api() 
            result = v1.list_node()
            nodes = {}
            for node in result.items:
                raw = node.status.addresses
                nodes['private_ip']=raw[0].address
                nodes['public_ip']=raw[1].address
                labels = node.metadata.labels
                name = node.metadata.name
                conditions = node.status.conditions
                node_status="NotReady"
                for data in conditions:
                    status=data.status
                    condition_type=data.type
                    reason=data.reason
                    if status in ["True", True] and condition_type == "Ready" and reason == "KubeletReady":
                        node_status="Ready"
                roles = node.metadata.labels
                node_schedulable=True
                raw_spec = node.spec
                if raw_spec:
                    taints = raw_spec.taints
                    if taints:
                        for data in taints:
                            effect=data.effect
                            if "NoSchedule" in effect:
                                node_schedulable=False
                nodes['node_schedulable'] = node_schedulable
                nodes['node_name'] = name
                nodes['node_status'] = node_status
                nodes_details.append(nodes.copy())	
        except Exception as ex:
            logging.error("Exception caught while fetching k8s node details.")
            logging.error(traceback.print_exc())
        finally:
            return nodes_details

    def get_details_pods_in_cluster(self):
        """
        Returns total number of pods in cluster
        """
        k8s_cluster_node_details = []
        try:
            v1 = client.CoreV1Api()
            result = v1.list_node()
            nodes = {}
            for node in result.items:
                labels = node.metadata.labels
                name = node.metadata.name
                field_selector = 'spec.nodeName='+name
                nodes['all_pods_details']=[]
                nodes['name'] = name
                pods_wise_details={}
                ret = v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
                for pod in ret.items:
                    pod_ip = pod.status.pod_ip
                    pods_wise_details['pod_ip'] = pod_ip
                    pod_namespace = pod.metadata.namespace
                    pods_wise_details['pod_namespace'] = pod_namespace
                    pod_name = pod.metadata.name
                    pods_wise_details['pod_name'] = pod_name
                    connection_status=False
                    if pod_ip:
                        connection_status = self.check_pod_reachable(pod_ip)
                    if connection_status is True:
                        pods_wise_details['pod_connectivity_status'] = "reachable"
                    else:
                        pods_wise_details['pod_connectivity_status'] = "not-reachable"
                    pod_conditions=pod.status.conditions
                    pod_health=""
                    for conditions_data in pod_conditions:
                        status=conditions_data.status
                        condition_type=conditions_data.type
                        if status in ["True", True] and condition_type == "ContainersReady":
                            pod_health="Running"
                            break
                        else:
                            pod_health="NotRunning"
                    pods_wise_details['pod_health']=pod_health
                    nodes['all_pods_details'].append(pods_wise_details.copy())
                k8s_cluster_node_details.append(nodes.copy())
        except Exception as ex:
            logging.error("Exception caught while listing pods of all nodes.")
            logging.error(traceback.print_exc())
        finally:
            return k8s_cluster_node_details

    def check_pod_reachable(self, pod_ip):
        connection_status = False
        try:
            #ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", pod_ip], stdout=subprocess.PIPE).stdout.read()
            #if ping_response == 0:
            connection_status = True
        except Exception as ex:
            logging.error("Exception caught while checking pod connectivity")
            logging.error(traceback.print_exc())
        finally:
            return connection_status
