from flask import Flask, request, jsonify
from marshmallow import Schema, fields

# instance of Flask
ToDoApp = Flask(__name__)

# dictionary to store tasks
tasks = {}
task_id_counter = 1

# schema for tasks
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title=fields.Str(required=True)
    descriptiop=fields.Str()
    done=fields.Bool()

# routes for API requests
@ToDoApp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@ToDoApp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@ToDoApp.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    schema = TaskSchema()
    try:
        task = schema.load(data)
        task['id']=task_id_counter
        tasks[task_id_counter] = task
        task_id_counter+=1
        return jsonify({'message': 'Task created successfully', 'task': task}),
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ToDoApp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = tasks.get(task_id)
    if task:
        data=request.get_json()
        schema = TaskSchema()
        try:
            updated_task = schema.load(data)
            task.update(updated_task)
            return jsonify({'message': 'Task updated successfully'}),
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        return jsonify({'error':'Task not found'}), 404

@ToDoApp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = tasks.pop(task_id, None)
    if task:
        return jsonify({'message': 'Task deleted successfully'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    ToDoApp.run(debug=True)