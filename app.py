from flask import Flask, render_template, redirect,request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://<yourusername>:<yourpassword>@cluster0-thmep.mongodb.net/Task_Data?retryWrites=true&w=majority'

mongo = PyMongo(app)



lst = []

@app.route('/')
def index():
    task = request.form
    task = dict(task)
    print(task)
    return "Server Is Working"

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def tasks():
    tasks = mongo.db.tasks
    result = []
    for task in tasks.find():
        result.append({'title' : task['title'], 'desc' : task['desc'], 'status' : task['status']})
    return jsonify({'result' : result})
    

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    task = request.form
    task = dict(task)
    tasks = mongo.db.tasks
    tasks.insert_one(task)
    return jsonify({'ok': True, 'message': 'Task Inserted Successfully!'})

@app.route('/todo/api/v1.0/tasks/<id>', methods=['GET'])
def get_task(id):
    tasks = mongo.db.tasks
    id = ObjectId(id)
    task = tasks.find_one({'_id' : id})
    if task:
        result = {'title' : task['title'], 'desc' : task['desc'], 'status' : task['status']}
    else:
        result = "No such Id"
    return jsonify({'result' : result})

@app.route('/todo/api/v1.0/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = request.form
    tasks = mongo.db.tasks
    result = tasks.find_one_and_update({'_id' : ObjectId(id)}, {"$set": {'title' : task['title'], 'desc' : task['desc'], 'status' : task['status']}})
    if result:
        return jsonify({'ok': True, 'message': 'Task Updated Successfully!'})
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'})

@app.route('/todo/api/v1.0/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    tasks = mongo.db.tasks
    id = ObjectId(id)
    result = tasks.find_one_and_delete({"_id": id})
    if result:
        return jsonify({'ok': True, 'message': 'Task Deleted Successfully!'})
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)