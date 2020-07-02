## Get started:

- Deploy RDS manager as container:
`docker run -d -p 8000:8000 tusharraut/rds-manager:1.0.0`

- Once the container is started access API's using:

`ENDPOINT: DOCKER_HOST_IP:8000`

## APIS:

1. 
    - Description: Get health of multiple RDS instances by all RDS instance details in JSON file
    - Method: POST
    - Endpoint: http://ENDPOINT/portal/verify_mulitple_instances_health_check/
    - Body:

2. 
    - Description: Get health of single RDS instance
    - Method: POST
    - Endpoint: http://ENDPOINT/portal/verify_single_instances_health_check/
    - Body:

3. 
    - Description: Execute single SQL command on one RDS instance or pool of RDS instances
    - Method: POST
    - Endpoint: http://ENDPOINT/portal/execute_single_sql_command/
    - Body:

4. 
    - Description: Execute batch SQL commands on one RDS instance or pool of RDS instances
    - Method: POST
    - Endpoint: http://ENDPOINT/portal/execute_batch_sql_command/
    - Body:


5. 
    - Description: Update tables on user provided RDS instances
    - Method: POST
    - Endpoint: http://ENDPOINT/portal/update_tables/
    - Body: