from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, jsonify

app = Flask(__name__)
from flask_socketio import SocketIO, emit
from json import loads, dumps

socketio = SocketIO(app, async_mode='threading')
mode = get_mode()
user_count = 0
users = {}
democracy = {}


@app.route("/")
def hello():
    render_template('index.html')


if __name__ == "__main__":
    app.run()
    socketio.run(app)


@socketio.on('test')
def handle_test():
    emit('test')


@socketio.on('initialize')
def handle_initialize():
    emit("initialize", {'input_type': get_input_mode()}, {'mode': mode})


@socketio.on("add user")
def handle_add_user(json):
    global user_count
    user_count += 1
    user = loads(json)
    users[user['username']] = {'input_count': 0}


@socketio.on('on disconnect')
def handle_disconnect(json):
    global user_count
    user_count -= 1
    user = loads(json)
    users.pop(user['username'])


@socketio.on("sendInput")
def handle_input(json):
    input = loads(json)
    users[input['username']]['input_count'] += 1
    if (mode == 'chaos'):
        handle_chaos(input)
    elif (mode == 'democracy'):
        handle_democracy(input)


def handle_chaos(input):
    execute_input(input)


def handle_democracy(input):
    global democracy
    try:
        democracy[input['input']] +=1
    except KeyError:
        democracy[input['input']] = 0
