from pprint import pprint

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    print(request.json)
    return request.json


@app.route("/test", methods=['GET', 'POST'])
def func():
    print(request.args)
    print(request.json)
    print(request.form)

    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form
        }
    )
