#! usr/bin/env python2

import PlayAsOne
from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, jsonify
from flask.ext.socketio import SocketIO, emit
from json import loads, dumps

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')
gui_server = PlayAsOne.PlayAsOne()
mode = gui_server.get_mode()
user_count = 0
users = {}
democracy = []


@app.route("/")
def hello():
    print("User entered")
    return render_template('index.html')


@socketio.on('connect', namespace="/")
def test_connect():
    print('test ran')


@socketio.on("add user", namespace="/")
def handle_add_user(username):
    global user_count
    user_count += 1
    user = username
    print user
    users[user] = {'input_count': 0}
    emit("initialize", {'input_type': gui_server.get_input_mode()}, {'mode': mode})


def handle_chaos(user_input):
    gui_server.execute_input(user_input)


def handle_democracy(user_input):
    global democracy
    for demo_input in democracy:
        if demo_input[0] == user_input['input']:
            demo_input[1] += 1
            break
    democracy.append((user_input['input'], 1))


def execute_democracy():
    most_votes = ("", 0)
    for user_input in democracy:
        if user_input[1] > most_votes[1]:
            most_votes = user_input
    gui_server.execute_input(most_votes[0])


@socketio.on('on disconnect', namespace="/")
def handle_disconnect(json):
    global user_count
    user_count -= 1
    user = loads(json)
    users.pop(user['username'])


@socketio.on("sendInput", namespace="/")
def handle_input(json):
    user_input = loads(json)
    users[input['username']]['input_count'] += 1
    if (mode == 'chaos'):
        handle_chaos(user_input)
    elif (mode == 'democracy'):
        handle_democracy(user_input)

if __name__ == '__main__':
    gui_server.gui.mainloop()
    socketio.run(app)
