from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to slack for slack</h1>"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    print("\n\n")
    print(request.json)
    print("\n\n")
    return request.json
