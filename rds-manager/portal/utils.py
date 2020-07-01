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

logging.basicConfig(filename='/tmp/rds-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
