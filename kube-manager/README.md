## How to use:

## Step to deploy kube-manager on your k8s cluster:
`kubectl apply -f https://raw.githubusercontent.com/tusharraut1994/task-manager/master/kube-manager/kube-manager-deployment.yaml`

Above spec deploys api server as well as creates NodePort service to expose it to access it from outside.

Check the nodePort of the service using command:
`kubectl get svc kube-manager`

### Replace API endpoint in following api requests: 
`API_ENDPOINT = NodeIP:NodePort`

### API's list:

1. 
	- Description: Health check 
	- Method: GET
	- `curl --location --request GET 'http://API_ENDPOINT/app'`

2. 
	- Description: List all nodes with details
	- Method: GET 
	- `curl --location --request GET 'http://API_ENDPOINT/app/list_cluster_nodes'`

3. 
	- Description: List all nodes pods with details
	- Method: GET 
	- `curl --location --request GET 'http://API_ENDPOINT/app/list_cluster_pods'`

4. 
	- Description: List all nodes pods with details or resource utilization
	- Method: GET 
	- `curl --location --request GET 'http://API_ENDPOINT/app/get_pods_utilization'`

5. 
	- Description: Update single resources
	- Method: POST 
	- `curl --location --request POST 'http://API_ENDPOINT/app/manage_individual_resources/' --header 'Content-Type: application/json' --data-raw '{ "namespace": "default", "resource_name": "redis-cache", "resource_type": "deployment", "operation": "scale","scale_value": 1 }'`

6. 
	- Description: Update single or multiple resources by uploading spec
	- Method: POST 
	- `curl --location --request POST 'http://API_ENDPOINT/app/manage_mulitple_resources/' --form ‘file=@/Users/tusharraut/test.yaml'`

7. 
	- Description: Deploy services on different nodes
	- Method: POST 
	- `curl --location --request POST 'http://API_ENDPOINT/app/deploy_services/' --form ‘file=@/Users/tusharraut/task-manager/kube-manager/services/first_service_spec.yaml'`

	- `curl --location --request POST 'http://API_ENDPOINT/app/deploy_services/' --form 'file=@/Users/tusharraut/task-manager/kube-manager/services/second_service_spec.yaml'`
