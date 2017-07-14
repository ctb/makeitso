#!flask/bin/python
from flask import Flask, jsonify, abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


app = Flask('makeitso')

tasks = [
]


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/todo/api/v1.0/take_task', methods=['POST'])
def take_task():
    firsttask = None
    for task in tasks:
        if not task['taken']:
            firsttask = task
            task['taken'] = True
            break

    if firsttask:
        return jsonify({'task': make_public_task(firsttask)})
    else:
        return jsonify({'task': {}})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
        task = [task for task in tasks if task['id'] == task_id]
        if len(task) == 0:
            abort(404)
        return jsonify({'task': task[0]})


@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'taskname' in request.json \
             or not 'params' in request.json:
        abort(400)

    task = {
        'id': tasks[-1]['id'] + 1,
        'taskname': request.json.get('taskname', ""),
        'params': request.json.get('params', ""),
        'done': False,
        'taken': False,
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'taskname' in request.json:
        abort(400)
    if 'params' in request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})
