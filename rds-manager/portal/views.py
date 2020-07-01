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
from utils.RDSManager import *

def ping(request):
    response_to = {"success":True, "message":"Pong"}
    return JsonResponse(response_to)

class BatchRDSInstancesHealthCheck(APIView):
    def post(self, request, format=None):
        """
        Health check for multiple rds instances
        """
        rds_mgr = RDSManager()
        file_obj = request.FILES['file']
        filename = '/tmp/' + file_obj.name
        destination = open(filename, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
        if os.path.exists(filename):
            connection_test_status, rds_instance_details = rds_mgr.test_multiple_db_connection(filename)
            if connection_test_status is True:
                response_to = {"success":True, "data":rds_instance_details, "message":"RDS instances connection verified."}
            else:
                response_to = {"success":False, "data":rds_instance_details, "message":"Failed to check connection of RDS instances."}
        else:
            response_to = {"success":False, "message":"Failed to upload RDS instances details."}
        return JsonResponse(response_to)

class RDSInstancesHealthCheck(APIView):
    def post(self, request, format=None):
        """
        Health check for rds instance
        """
        content = json.loads(request.body)
        endpoint = content.get("endpoint")
        port = content.get("port")
        user = content.get("user")
        region = content.get("region")
        dbname = content.get("dbname")
        if endpoint and port and user and region and dbname:
            rds_mgr = RDSManager()
            connection_status = rds_mgr.test_db_connection(endpoint, port, user, region, dbname)
            if connection_status is True:
                response_to = {"success":connection_status, "message":"Successfully connected to RDS instance."}
            else:
                response_to = {"success":connection_status, "message":"Failed to connect to RDS instance."}
        else:
            response_to = {"success":False, "message":"Incomplete parameters."}
        return JsonResponse(response_to)

class ExecuteSingleSQLCommand(APIView):
    def post(self, request, format=None):
        """
        Execute single SQL command
        """
        status = {}
        response_to = {"success":True, "data":status, "message":"SQL command executed successfully."}
        return JsonResponse(response_to)

class ExecuteMultipleSQLCommand(APIView):
    def post(self, request, format=None):
        """
        Execute multiple/batch SQL commands
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
