from kubernetes import client, config
import time
import yaml
import os, logging
from os import path
from kube_manager_portal.orchestrator.kube import Kubernetes

class KubeManager(object):
    """
    This class defines different kubernetes deployment
    """
    def __init__(self, user_namespace):
        """
        Constructor of class KubeManager
        """
        logging.basicConfig(filename='/tmp/cluster-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def create_namespace(self):
        """
        This function creates namespace
        """
        try:
	        logging.info("Creating new cluster :%s",self.user_namespace)
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            body = client.V1Namespace()
            body.metadata = client.V1ObjectMeta(name=self.user_namespace)
            resp = v1.create_namespace(body)
            logging.info("New cluster creation status:%s", resp.status)
        except Exception as ex:
            logging.error("Exception caught while creating namespace: %s" ,ex)

    def create_secret(self, secret_file):
        """
        This function create secret
        """
	    try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), secret_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_secret(
                    body=dep, namespace=self.user_namespace)
            logging.info("Secret created. status='%s'" % str(resp))
        except Exception as ex:
            logging.error("Exception caught while creating secret : [%s: %s]" % (secret_file, ex))

    def create_endpoint(self, end_point_file):
        """
        This function create end point
        """
        try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), end_point_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_endpoints(
                    body=dep, namespace=self.user_namespace)
            logging.info("End point created. status='%s'" % str(resp))
        except Exception as ex:
            logging.error("Exception caught while creating end point : [%s: %s]" % (end_point_file, ex))

    def create_service_account(self, service_account_file):
        """
        This function create service account
        """
        try:
	        kube = Kubernetes()
    	    v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), service_account_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_service_account(
                    body=dep, namespace=self.user_namespace)
            logging.info("Service account created. status='%s'" % str(resp))
        except Exception as ex:
            logging.error("Exception caught while creating service account : [%s: %s]" % (service_account_file, ex))


    def create_role(self, role_file):
        """
        This function create role
        """
        try:
	        rbac = kubernetes.client.RbacAuthorizationV1Api()
            with open(path.join(path.dirname(__file__), role_file)) as f:
                dep = yaml.load(f)
                resp = rbac.create_namespaced_role(
                    body=dep, namespace=self.user_namespace)
            logging.info("Role created. status='%s'" % str(resp))
        except Exception as ex:
            logging.error("Exception caught while creating role : [%s: %s]" % (role_file, ex))


    def create_role_binding(self, role_binding_file):
        """
        This function create role binding
        """
        try:
	        rbac = kubernetes.client.RbacAuthorizationV1Api()
            with open(path.join(path.dirname(__file__), role_binding_file)) as f:
                dep = yaml.load(f)
                resp = rbac.create_namespaced_role_binding(
                    body=dep, namespace=self.user_namespace)
            logging.info("Role binding created. status='%s'" % str(resp))
        except Exception as ex:
            logging.error("Exception caught while creating role binding : [%s: %s]" % (role_binding_file, ex))

    def create_replication_controller(self, deployment_file):
        """
        This function creates replication controller
        """
        try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), deployment_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_replication_controller(
                    body=dep, namespace=self.user_namespace)
            logging.info("Deployment created. status='%s'" % str(resp.status))
        except Exception as ex:
            logging.error("Exception caught while creating deployment : [%s: %s]" % (deployment_file, ex))

    def create_pvc_storage(self, deployment_file):
        """
        This function creates persistent volume claim
        """
        try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), deployment_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_persistent_volume_claim(
                    body=dep, namespace=self.user_namespace)
            logging.info("Deployment created. status='%s'" % str(resp.status))
        except Exception as ex:
            logging.error("Exception caught while creating deployment : [%s: %s]" % (deployment_file, ex))

 
    def create_service(self, deployment_file):
        """
        This function creates service
        """
        try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), deployment_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_service(
                    body=dep, namespace=self.user_namespace)
            logging.info("Service created. [%s] status='%s'" % ( deployment_file,str(resp.status)))
        except Exception as ex:
            logging.error("Exception caught while creating Service : [%s: %s]" % (deployment_file, ex))

    def create_pod(self, deployment_file):
        """
        This function creates pod
        """
        try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            with open(path.join(path.dirname(__file__), deployment_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_pod(
                    body=dep, namespace=self.user_namespace)
            logging.info("Deployment created. status='%s'" % str(resp.status))
        except Exception as ex:
            logging.error("Exception caught while creating deployment : [%s: %s]" % (deployment_file, ex))

    def create_statefull_set(self, deployment_file):
        """
        This function creates statefull set
        """
        try:
            v1 = client.AppsV1Api()
            with open(path.join(path.dirname(__file__), deployment_file)) as f:
                dep = yaml.load(f)
                resp = v1.create_namespaced_stateful_set(
                    body=dep, namespace=self.user_namespace)
            logging.info("Deployment created. status='%s'" % str(resp.status))
        except Exception as ex:
            logging.error("Exception caught while creating deployment : [%s: %s]" % (deployment_file, ex))

    def delete_namespace(self):
        """
        This function deletes deployment
        """
        try:
	        kube = Kubernetes()
	        v1 = kube.get_kube_api()
            body = client.V1DeleteOptions()
            resp = v1.delete_namespace(self.user_namespace, body)
            logging.info("Namespace [%s] delete status : [%s]" % (self.user_namespace, resp.status))
        except Exception as ex:
            logging.error("Exception caught while deleting namespace : %s" % ex)
