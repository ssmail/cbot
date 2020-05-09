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
    zoom_msg = build_message(request.json)
    if zoom_msg.bot_id != "":
        last_message.append(zoom_msg)

    print("\n\n")
    return request.json


@app.route("/command", methods=['GET', 'POST'])
def command():
    print("\n\n")
    print(request.headers)
    print("\n")
    print(request.json)
    print("\n\n")

    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form,
        }
    )


@app.route("/query", methods=['GET', 'POST'])
def query():
    key = request.args.get("key", None)
    if key == "hkf":
        show()
        return jsonify({"message": last_message})
    else:
        return "bad request"


@app.route("/clean", methods=['GET', 'POST'])
def clean():
    key = request.args.get("key", None)
    if key == "hkf":
        last_message.clear()
        show()
        return jsonify({"message": last_message})
    else:
        return "bad request"


def show():
    print(f"\n\nlast_message length: ----- {len(last_message)}")
    for i in last_message:
        print(i)
