from dataclasses import dataclass

from packages.utils import build_message

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to slack for slack</h1>"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    print("\n\n")
    print(request.json)
    build_message(request.json)
    print("\n\n")
    return request.json


@app.route("/command", methods=['GET', 'POST'])
def command():
    print("\n\n")
    print(request.json)
    print("\n\n")

    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form
        }
    )


@app.route("/query", methods=['GET', 'POST'])
def query():
    print(request.args)
    channel = request.args['channel']
    username = request.args['username']
