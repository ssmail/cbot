from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


@app.route("/test")
def func():
    return jsonify({"welcome": "world"})
