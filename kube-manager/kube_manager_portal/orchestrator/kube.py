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
from time import sleep

logging.basicConfig(filename='/tmp/cluster-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
MAX_RETRY=50

class Kubernetes():
    def __init__(self):
        """
        Kubernetes defaults
        """
        try:
            logging.info("Loading Kubernetes config from incluster")
            config.load_incluster_config()
            self.metrics_service_spec = "/code/metrics-server.yaml"
        except Exception as ex:
            logging.error("Failed to initialize kubernete configuration %s" % ex)

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
                nodes['scheduling_enabled'] = node_schedulable
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
                        podhostip=pod_ip.replace(".", "-")
                        connection_status = self.check_pod_reachable(podhostip, pod_namespace)
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

    def check_pod_reachable(self, pod_hostname, pod_namespace):
        connection_status = False
        try:
            cmd = "nslookup %s.%s.pod.cluster.local" % (pod_hostname, pod_namespace)
            logging.info("Nslookup command for pod connectivity check: %s" % cmd)
            status, output = subprocess.getstatusoutput(cmd)
            logging.info("Status: %s, Output: %s" % (status, output))
            if status == 0:
                connection_status = True
        except Exception as ex:
            logging.error("Exception caught while checking pod connectivity")
            logging.error(traceback.print_exc())
        finally:
            return connection_status

    def modify_service_spec(self, filename):
        """
        This function add pod affinity and anti-affinity to user deployment spec
        """
        status = False
        try:
            status = True
        except Exception as ex:
            logging.error("Exception caught while modifying service spec.")
            logging.error(traceback.print_exc())
        finally:
            return status, filename

    def update_resources(self, input_file):
        file_update_status = False
        try:
            cmd = "kubectl apply -f %s " % input_file
            logging.info("Resources update command: %s" % cmd)
            status, output = subprocess.getstatusoutput(cmd)
            logging.info("Resource updatee command status: %s, output: %s" % (status, output))
            if status == 0:
                file_update_status = True
        except Exception as ex:
            logging.error("Exception caught while updating resources.")
            logging.error(traceback.print_exc())
        finally:
            return file_update_status

    def scale_resources(self, namespace, resource_name, resource_type, scale_value):
        scale_status = False
        try:
            resource_exists = self.check_resource_exists(namespace, resource_name, resource_type)
            if resource_exists:
                cmd = "kubectl scale %s %s --namespace %s --replicas=%s" % (resource_type, resource_name, namespace, scale_value)
                logging.info("Resource scale command : %s" % cmd)
                status, output = subprocess.getstatusoutput(cmd)
                logging.info("Resource scale command status: %s, output: %s" % (status, output))
                if status == 0:
                    scale_status = True
        except Exception as ex:
            logging.error("Exception caught while updaing resources.")
            logging.error(traceback.print_exc())
        finally:
            return scale_status

    def set_image(self, namespace, resource_name, resource_type, image_name):
        set_image_status = False
        try:
            resource_exists = self.check_resource_exists(namespace, resource_name, resource_type)
            if resource_exists:
                cmd = "kubectl set image %s --namespace %s %s=%s:%s" % (resource_type, namespace, resource_name, image_name)
                logging.info("Image set command : %s" % cmd)
                status, output = subprocess.getstatusoutput(cmd)
                logging.info("Image set command status: %s, output: %s" % (status, output))
                if status == 0:
                    set_image_status = True
        except Exception as ex:
            logging.error("Exception caught while updaing image.")
            logging.error(traceback.print_exc())
        finally:
            return set_image_status

    def update_configmap(self, namespace, resource_name, key, value):
        configmap_update_status = False
        try:
            configmap_exists = self.check_resource_exists(namespace, resource_name, "configmap")
            if configmap_exists is True:
                check_key_exists_cmd = "kubectl get cm --namespace %s %s -o jsonpath={.data.%s} | grep -iv error | grep -iv NAME | wc -l" % (namespace, resource_name, key)
                logging.info("Configmap key check command: %s" % check_key_exists_cmd)
                status, output = subprocess.getstatusoutput(cmd)
                if status == 0 and int(output) == 1:
                    update_cmd_key_value_cmd = "kubectl patch configmap %s --namespace %s --type merge  -p \'{\"data\":{\"%s\":\"%s\"}}\'" % (resource_name, namespace, key, value)
                    logging.info("Configmap update command: %s" % update_cmd_key_value_cmd)
                    status, output = subprocess.getstatusoutput(update_cmd_key_value_cmd)
                    logging.info("Update configmap command status: %s, output: %s" % (status, output))
                    if status == 0:
                        configmap_update_status = True
        except Exception as ex:
            logging.error("Exception caught while udpdating configmap.")
            logging.error(traceback.print_exc())
        finally:
            return configmap_update_status

    def check_resource_exists(self, namespace, resource_name, resource_type):
        resource_exists = False
        try:
            cmd = "kubectl get %s --namespace %s %s | grep -iv error | awk '{print $1}' | wc -l" % (resource_type, namespace, resource_name)
            logging.info("resource check command: %s" % cmd)
            status, output = subprocess.getstatusoutput(cmd) 
            logging.info("Resource check command status: %s, output: %s" % (status, output))
            if status == 0:
                resource_exists = True
        except Exception as ex:
            logging.error("Exception caught while checking resource exists.")
            logging.error(traceback.print_exc())
        finally:
            return resource_exists

    def get_heavy_loaded_pod_details(self):
        pods_details = {}
        try:
            metrics_server_deploy_status = self.update_resources(self.metrics_service_spec)
            logging.info("Metrics service deployed: %s" % metrics_server_deploy_status)
            metrics_server_running_status = self.check_metrics_server_up_running("kube-system", "metrics-server")
            logging.info("Metrics service running status: %s" % metrics_server_running_status)
            if metrics_server_running_status is True:
                cmd="kubectl top pod --all-namespaces | awk '{print $1,$2,$3,$4}' | grep -v NAME"
                logging.info("Fetch pods based on resources command: %s" % cmd)
                status, output = subprocess.getstatusoutput(cmd)
                if status == 0:
                    data = output.split("\n")
                    if data:
                        count = 0
                        pods_details = []
                        record = []
                        for d in data:
                            details = d.split(" ")
                            record.append(details)
                        pod_resource_details = {}
                        logging.info("All pods: %s" % record)
                        for rd in record:
                            pod_resource_details['namespace'] = rd[0]
                            pod_resource_details['pod_name'] = rd[1]
                            pod_resource_details['cpu'] = rd[2]
                            pod_resource_details['memory'] = rd[3]
                            count +=1
                            if count == 10:
                                break
                            pods_details.append(pod_resource_details.copy())                                    
        except Exception as ex:
            logging.error("Exception caught while checking heavy loaded pods.")
            logging.error(traceback.print_exc())
        finally:
            return pods_details

    def check_metrics_server_up_running(self, namespace, deployment_name):
        deployment_running_status = False
        retryCount=0
        while not deployment_running_status:
            try:
                api_instance = client.AppsV1Api()
                api_response = api_instance.read_namespaced_deployment_status(deployment_name, namespace)
                total_replicas = api_response.spec.replicas
                ready_replicas = api_response.status.ready_replicas
                logging.info("Total replicas:[%s], Ready replicas:[%s]" % (total_replicas, ready_replicas))
                if ready_replicas == total_replicas and ready_replicas >= 1:
                    deployment_running_status = True
                    break
            except Exception as ex:
                pass
            sleep(5)
            retryCount += 1
            logging.info("\nRetry count: [%s]" % retryCount)
            if retryCount > MAX_RETRY:
                break
            logging.info("Replica status check:[%s]" % deployment_running_status)
        return deployment_running_status