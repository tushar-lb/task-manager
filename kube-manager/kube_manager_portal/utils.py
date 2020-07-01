import os
import math
import base64
import ruamel.yaml
import socket
import time
from time import gmtime, strftime
import sqlite3
import subprocess
from string import Template
from random import randint
import logging
import inspect
from ftplib import FTP
import traceback 
from kube_manager_portal.orchestrator.kube import Kubernetes

logging.basicConfig(filename='/tmp/cluster-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def get_k8s_nodes_ip():
    """
    List k8s cluster nodes internal ip
    """
    try:
        kube = Kubernetes()
        v1 = kube.get_kube_api()
        result = v1.list_node()
        node_ips = []
        for node in result.items:
            raw = node.status.addresses
            internal_ip =raw[0].address
            logging.info("IP: %s" % internal_ip)
            node_ips.append(internal_ip)
        logging.info("Node IP list: %s" % node_ips)
        return node_ips
    except Exception as ex:
        logging.error("Exception caught while fetching node details: %s" % ex)
        return None
