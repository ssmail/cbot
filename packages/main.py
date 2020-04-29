from dataclasses import dataclass

from packages.utils import build_message

from flask import Flask, jsonify, request

app = Flask(__name__)

last_message = []


@app.route("/")
def home_view():
    return "<h1>Welcome to slack for slack</h1>"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    print("\n\n")
    print(request.json)
    last_message.append(build_message(request.json))

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
    channel = request.args['channel']
    username = request.args['username']

    print(f"query: channel: {channel}, username:  {username}")
    show()


@app.route("/clean", methods=['GET', 'POST'])
def clean():
    last_message.clear()
    show()


def show():
    print(f"last_message length: ----- {len(last_message)}")
    for i in last_message:
        print(i)
