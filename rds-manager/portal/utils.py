import socket
import time
from time import gmtime, strftime
import subprocess
import traceback 
import mysql.connector
import sys
import boto3
import os
import psycopg2
import json

class RDSManager():
    def __init__(self):
        self.instances_file = "instance_details.json"
        self.profile_name = "RDSCreds"

    def read_instances_json(self, instances_file):
        instance_fetch_status, instances_details = False, {}
        try:
            if os.path.exists(instances_file):             
                with open(instances_file) as f:
                    data = json.load(f)
                    print(data)
                    instances_details = data
                if instances_details:
                    instance_fetch_status = True
            else:
                print("Instances details are not available.")
        except Exception as ex:
            print("Exception caught while reading instances details.")
        finally:
            return instance_fetch_status, instances_details

    def fetch_token(self, endpoint, port, user, region):
        token_fetch_status, token = False, ""
        try:
            session = boto3.Session(profile_name=self.profile_name)
            client = boto3.client('rds')
            token = client.generate_db_auth_token(DBHostname=endpoint, Port=port, DBUsername=user, Region=region)
            if token:
                token_fetch_status = True
        except Exception as ex:
            print("Exception caught while fetching token")
        finally:
            return token_fetch_status, token

    def test_multiple_db_connection(self, instances_file):
        """
        Loads json file of all rds instances and verify connectivity
        """
        connection_test_status = False
        result = []
        try:
            instance_fetch_status, instances_details = self.read_instances_json(instances_file)
            if instance_fetch_status is True:
                for data in instance_details:
                    rds_instance = {}
                    endpoint = data.get("ENDPOINT")
                    port = data.get("PORT")
                    user = data.get("USER")
                    region = data.get("REGION")
                    dbname = data.get("DBNAME")
                    rds_instance['endpoint'] = endpoint
                    rds_instance['port'] = port
                    rds_instance['user'] = user
                    rds_instance['region'] = region
                    rds_instance['dbname'] = dbname
                    token_fetch_status, token = fetch_token(endpoint, port, user, region)
                    if token_fetch_status is True:
                        try:
                            if dbname == "mysql":
                                conn =  mysql.connector.connect(host=endpoint, user=user, passwd=token, port=port, database=dbname)
                            elif dbname == "postgres":
                                conn =  psycopg2.connect(host=endpoint, user=user, passwd=token, port=port, database=dbname)
                            cur = conn.cursor()
                            cur.execute("""SELECT now()""")
                            query_results = cur.fetchall()
                            print(query_results)
                            connection_status = True
                            rds_instance['connection_status'] = connection_status
                        except Exception as e:
                            print("Database connection failed due to {}".format(e))      
                    result.append(rds_instance.copy())
            if result:
                connection_test_status = True
        except Exception as ex:
            print("Exception while connecting to db")
            print(traceback.print_exc())
        finally:
            return connection_test_status, result

    def test_db_connection(self, endpoint, port, user, region, dbname):
        """
        Check input rds instance connection
        """
        connection_status = False
        try:
            token_fetch_status, token = fetch_token(endpoint, port, user, region)
            if token_fetch_status is True:
                try:
                    if dbname == "mysql":
                        conn =  mysql.connector.connect(host=endpoint, user=user, passwd=token, port=port, database=dbname)
                    elif dbname == "postgres":
                        conn =  psycopg2.connect(host=endpoint, user=user, passwd=token, port=port, database=dbname)
                    cur = conn.cursor()
                    cur.execute("""SELECT now()""")
                    query_results = cur.fetchall()
                    print(query_results)
                    if query_results:
                        connection_status = True
                except Exception as e:
                    print("Database connection failed due to {}".format(e))
        except Exception as ex:
            print("Exception while connecting to db")
            print(traceback.print_exc())
        finally:
            return connection_status

    def get_db_pool_details(self):
        pass

    def executes_sql_on_pool(self, pool, sql_queries):
        pass

    def update_tables_in_rds(self):
        pass