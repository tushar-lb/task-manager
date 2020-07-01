from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, \
    StreamingHttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from  portal.utils import *
import json
from rest_framework.schemas import AutoSchema
import coreapi
import os
import logging
import inspect

logging.basicConfig(filename='/tmp/rds-api.log',level="INFO", format='[%(asctime)s] [%(levelname)-2s] [%(filename)s:%(lineno)s:%(funcName)2s()] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def ping(request):
    response_to = {"success":True, "message":"Pong"}
    return JsonResponse(response_to)

class RDSInstancesHealthCheck(APIView):
    def post(self, request, format=None):
        """
        Health check for rds instances
        """
        status = {}
        response_to = {"success":True, "data":status, "message":"RDS instances details fetched successfully."}
        return JsonResponse(response_to)

class ExecuteSQLCommand(APIView):
    def post(self, request, format=None):
        """
        Execute SQL commands
        """
        status = {}
        response_to = {"success":True, "data":status, "message":"SQL command executed successfully."}
        return JsonResponse(response_to)

class UpdateTables(APIView):
    def post(self, request, format=None):
        """
        Update tables
        """
        status = {}
        response_to = {"success":True, "data":status, "message":"Table updated successfully."}
        return JsonResponse(response_to)
