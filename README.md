
# api-lambda-python-api-gateway

# Create an API Lambda using python and AWS API Gateway


A brief description of what this project does and who it's for


## Introduction

In this tutorial, we will learn how to build a RESTful API using AWS Lambda and Python. We will start by creating a simple Python function and deploying it to AWS Lambda, and then we will add the necessary components to create a RESTful API.


## Creating a API Python code

The first step in creating a RESTful API using AWS Lambda and Python is to create a simple Python function that returns a response to an HTTP request. 

I created a ``lambda_func.py`` file

Here is an example of a simple Python function in :

```python
class Task:
    def __init__(self):
        self.data = [] # Storage data read from movies.csv file
        # Read data
        list_length = len(self.data)
        if list_length == 0:
            with open('movies.csv', 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    # Create a dictionary for each row, mapping the headers to the values
                    row_data = dict(zip(headers, row))
                    # Add a new dictionary to the list
                    self.data.append(row_data)

```
## API Code


### HTTP GET


```python
def get_task(self,task_id):
    return responses(200,"",self.data)
```


### HTTP POST


```python
def update_task(self,task_id, body):
        # :Load data 
        task = [task for task in self.data if task['id'] == task_id]
        index = 0

        if task:
            index = self.data.index(task[0])
        else:
            index = -1
            
        if index < 0:
            return responses(400,"Task not exists")
        if not body:
            return responses(400,'Bad request')
        
        self.data[index]['name'] = body.get("name","")
        self.data[index]['description'] = body.get('description',"")
        self.data[index]['category'] = body.get('category',"")
        self.data[index]['director'] = body.get('director',"")
        self.data[index]['income'] = body.get('income',"")
        self.data[index]['invest'] = body.get('invest',0)
        self.data[index]['location'] = body.get('location',"")   
        self.data[index]['percentage'] = body.get('percentage',0)
        self.data[index]['rating'] = body.get('rating',0)
        self.data[index]['revenue'] = body.get('revenue',0) 
        return {'data': self.data[index]} 
```

## HTTP CREATE

```python
def create_task(self, body):
        # :Load data 
        if not body:
            return responses(400,"body data is empty")
        id = int(self.data[-1]["id"]) +1
        task = {
            'id': id,
            'name': body.get("name",""),
            'description':body.get('description',""),
            'category' :body.get('category',""),
            'director' :body.get('director',""),
            'income' :body.get('income',""),   
            'invest' :body.get('invest',0),   
            'location' :body.get('location',""),     
            'percentage':  body.get('percentage',0),     
            'rating':  body.get('rating',0),   
            'revenue': body.get('revenue',0) ,     
        }
        self.data.append(task)
        return responses(200,"", task)
```


### HTTP DELETE


```python
 def delete_task(self,task_id):
        # :Load data 
        task = [task for task in self.data if task['id'] == task_id]
        index = 0

        if task:
            index = self.data.index(task[0])
        else:
            index = -1
            
        if index < 0:
            return responses(400,"Task not exists")
        self.data.remove(task[0])
        return  responses(200,"",{'id':task_id})
```


### Lambda Handler

In lambda_handler fucntion will receive request from AWS API Gateway. Using `event.get("routeKey")` HTTP Mehod.


```python
def lambda_handler(event, context):
    api = Task()
    httpmethod = event.get("routeKey").split(" /")[0]
    # return query_params
    # return httpmethod
    if  httpmethod == 'GET':
        result = api.get_task(0)
        return result
    elif  httpmethod == 'PUT':
        if not event.get('body'):
            return {"error": "Request body is not in JSON format"}
     
        body = json.loads(event.get('body',{}))
        result = api.create_task(body)
        return result
    elif httpmethod == 'POST':
        raw_query_string = event.get('rawQueryString')
        query_params = urllib.parse.parse_qs(raw_query_string)
        try:
        # code that might raise an exception
            id = query_params.get('id',"")[0]
            if id == "":
                return { 'error': "id is not valid"} 
           
            if not event.get('body'):
                return {"error": "Request body is not in JSON format"}
                
            body = json.loads(event.get('body',{}))
            result = api.update_task(id,body)
            return result
        except Exception as err:
        # code to handle the exception
            return { 'error':str(err), 'data': {} }
        
        
```


## AWS API Gateway

Here is the procedure to add an API Gateway:

Open the AWS Management Console and navigate to the API Gateway service.

Click the "Create API" button and choose "HTTP".

Give your API a name and choose "RESTful".

Click the "Routes" button and give your resource a name.

Choose the "Action" drop-down and choose "POST".

Choose "Lambda Function" as the integration type and select the region where your Lambda function is deployed.

Enter the name of your Lambda function in the "Lambda function name"

