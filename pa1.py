from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    render_template('index.html')


if __name__ == "__main__":
    app.run()
