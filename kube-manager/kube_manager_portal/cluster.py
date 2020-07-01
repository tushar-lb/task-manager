from kubernetes import client, config
import traceback
import os
import logging
from kube_manager_portal.utils import *
from kube_manager_portal.orchestrator.kube import Kubernetes

logging.basicConfig(filename='/tmp/cluster-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Orchestration():
    def __init__(self,orch_type):
        self.orch_layer = None
        if orch_type == "kubernetes":
            self.orch_layer = Kubernetes()