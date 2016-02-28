from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, jsonify
app = Flask(__name__)
from flask_socketio import SocketIO

socketio = SocketIO(app)
is_chaos = getchaos()
user_count = 0


@app.route("/")
def hello():
    render_template('index.html')


if __name__ == "__main__":
    app.run()
    socketio.run(app)

@socketio.on("add user")
def handle_add_user(json):



@socketio.on("sendInput")
def handle_input(json):
    if(is_chaos):
        handle_chaos(json)
