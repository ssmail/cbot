import json

from packages.utils import build_message
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

zoom_message = []
chat_message = []

query_key = ['online_1132683036224', 'dev_1232683036224']

ZOOM_BOT_ID = 'B012AA1UZ5H'
ZOOM_DEV_BOT_ID = "B01352MV8SJ"
WORK_SPACE = []


@app.route("/")
def alive():
    return "server is running"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    logging.info(f"{request.json} \n")
    try:
        zoom_msg = build_message(request.json)

        logging.info(zoom_msg + "\n")

        if zoom_msg.bot_id == ZOOM_BOT_ID or zoom_msg.bot_id == ZOOM_DEV_BOT_ID:
            logging.info(f"zoom box: {zoom_msg}\n")
            zoom_message.append(zoom_msg)
        else:
            logging.info("this is a normal message")
            chat_message.append(request.json)
    except Exception:
        logging.error('add zoom msgbox failed')
    finally:
        if request.json:
            return request.json
        else:
            return "hello"


@app.route("/command", methods=['GET', 'POST'])
def command():
    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form,
        }
    )


@app.route("/query", methods=['GET', 'POST'])
def query():
    logging.info(f"command: {request.args}")
    key = request.args.get("key", None)
    if key in query_key:
        return jsonify(
            {"zoom_message": zoom_message}
        )
    else:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"


@app.route("/clean", methods=['GET', 'POST'])
def clean():
    key = request.args.get("key", None)
    if key in query_key:
        zoom_message.clear()
        chat_message.clear()
        return jsonify(
            {"message": zoom_message, "chat_message": chat_message}
        )
    else:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"
