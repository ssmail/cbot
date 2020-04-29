from pprint import pprint

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    print(10 * "---: request.args")
    pprint(request.args)
    print(10 * "--- request.json")
    pprint(request.json)
    print(10 * "--- request.form")
    pprint(request.form)

    pprint("respone json: ")
    pprint({"challenge": request.json['challenge']})
    return jsonify({"challenge": request.json['challenge']})


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
