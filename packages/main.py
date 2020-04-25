from flask import Flask, jsonify
from slacker import Slacker
from requests.sessions import Session

app = Flask(__name__)

token = 'xoxb-1066881550131-1083566751251-EpMmCsKotQoJSBcfl0Lk6JtZ'


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


@app.route("/test")
def func():
    with Session() as session:
        slack = Slacker(token, session=session)
        slack.chat.post_message('#allmember', 'this is a test')
        return jsonify({"welcome": "world"})
