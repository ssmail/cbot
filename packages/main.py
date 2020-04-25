from flask import Flask, jsonify
from slacker import Slacker

app = Flask(__name__)

from requests.sessions import Session

token = 'xoxb-1066881550131-1083566751251-swhs1IarrFt965IBcyzhlcCU'

session = Session()
slack = Slacker(token, session=session)


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"


@app.route("/test")
def func():
    slack.chat.post_message('#slacktestproject', 'this is a test from cbot api')
    return jsonify({"welcome": "world"})
