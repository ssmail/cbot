from pprint import pprint

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


@app.route("/test", methods=['GET', 'POST'])
def func():
    print(10 * "---")
    pprint(request.args)
    print(10 * "---")
    pprint(request.json)
    print(10 * "---")
    pprint(request.form)

    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form
        }
    )
