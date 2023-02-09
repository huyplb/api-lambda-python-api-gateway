import csv
import os
import json
import urllib
# Create a list of dictionaries
class Task:
    def __init__(self):
        self.data = []
        current_directory = os.getcwd()
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
                    
    def is_json(self,obj):
        try:
            json.dumps(obj)
            return True
        except TypeError:
            return False
    def is_empty(self,obj):
        if obj:
            return False
        else:
            return True
    def get_task(self,task_id):
        return responses(200,"",self.data)

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

    def update_task(self,task_id, body):
        # :Load data 
        task = [task for task in self.data if task['id'] == task_id]
        index = 0
        
        return responses(400,"Task not exists")
        
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

# @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(self,task_id):
        # :Load data 
        task = [task for task in self.data if task['id'] == task_id]
        if len(task) == 0:
            return {
            'statusCode': 200,
            'body': json.dumps({"status": "error", "message": "task not found"})
        } 
            return jsonify(), 404
        tasks.remove(task[0])
        return  {
            'statusCode': 200,
            'body': json.dumps({"status": "done", "message": "tasked"})
        } 

# Local 
# if __name__ == '__main__':
#     app.run()


def responses(statusCode, error = "", body = None):
    response = {
        'statusCode': statusCode,
        "error": error, 
        'body': json.dumps(body)
    }
    return json.dumps(response)
    

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
        
        
        
