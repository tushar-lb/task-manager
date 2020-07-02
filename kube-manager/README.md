## How to use:

## Step to deploy kube-manager on your k8s cluster:
`kubectl apply -f https://raw.githubusercontent.com/tusharraut1994/task-manager/master/kube-manager/kube-manager-deployment.yaml`

Above spec deploys api server as well as creates NodePort service to expose it to access it from outside.

Check the nodePort of the service using command:
`kubectl get svc kube-manager`

### Replace API endpoint in following api requests: 
`API_ENDPOINT = NodeIP:NodePort`

### API's list:

Method: GET 
Description: Health check 
`curl --location --request GET 'http://API_ENDPOINT/app'`

Method: GET 
Description: List all nodes with details
`curl --location --request GET 'http://API_ENDPOINT/app/list_cluster_nodes'`

Method: GET 
Description: List all nodes pods with details
`curl --location --request GET 'http://API_ENDPOINT/app/list_cluster_pods'`

Method: GET 
Description: List all nodes pods with details or resource utilization
`curl --location --request GET 'http://API_ENDPOINT/app/get_pods_utilization'`

Method: POST 
Description: Update single resources
curl --location --request POST 'http://API_ENDPOINT/app/manage_individual_resources/' --header 'Content-Type: application/json' --data-raw '{
	"namespace": "default",
	"resource_name": "redis-cache",
	"resource_type": "deployment",
	"operation": "scale",
	"scale_value": 1
}'

Method: POST 
Description: Update single or multiple resources by uploading spec
`curl --location --request POST 'http://API_ENDPOINT/app/manage_mulitple_resources/' --form ‘file=@/Users/tusharraut/test.yaml'`

Method: POST 
Description: Deploy services on different nodes
`curl --location --request POST 'http://API_ENDPOINT/app/deploy_services/' --form ‘file=@/Users/tusharraut/task-manager/kube-manager/services/first_service_spec.yaml'`

`curl --location --request POST 'http://API_ENDPOINT/app/deploy_services/' --form 'file=@/Users/tusharraut/task-manager/kube-manager/services/second_service_spec.yaml'`
