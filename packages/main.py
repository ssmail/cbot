import json

from packages.utils import build_message
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

zoom_message = []
chat_message = []

query_key = ['online_1132683036224', 'dev_1232683036224']

ZOOM_BOT_ID = 'B012AA1UZ5H'
ZOOM_BOT_ID_2 = 'B013S9M3N69'

ZOOM_DEV_BOT_ID_1 = "B01352MV8SJ"
ZOOM_DEV_BOT_ID_2 = "B012VE561RV"

WEB_ZOOM_BOT_ID = 'B013ESGTREH'

ZOOM_BOT_LIST = [
    ZOOM_BOT_ID,
    ZOOM_BOT_ID_2,
    ZOOM_DEV_BOT_ID_1,
    ZOOM_DEV_BOT_ID_2,
    WEB_ZOOM_BOT_ID
]

WORK_SPACE = []


@app.route("/")
def alive():
    return "server is running"


@app.route("/message", methods=['GET', 'POST'])
def channel_message():
    logging.info(f"{request.json} \n")
    workspace = request.args.get('workspace', None)
    try:
        zoom_msg = build_message(request.json, workspace)
        logging.info(f"Zoom Msgbox: {zoom_msg}")
        if zoom_msg.bot_id in ZOOM_BOT_LIST:
            zoom_message.append(zoom_msg)
        else:
            logging.info("this is a normal message")
            chat_message.append(zoom_msg)
    except Exception as e:
        logging.error('add zoom msgbox failed')
        logging.exception(e)
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
    logging.info(f"query args: {request.args}")
    key = request.args.get("key", None)
    msg_type = request.args.get("type", "zoom")

    if key in query_key:
        if msg_type == "zoom":
            return jsonify({"zoom_message": zoom_message})
        elif msg_type == "text":
            return jsonify({"normal_message": chat_message})
        else:
            logging.error(f"bad request: {request.remote_addr}")
            return "bad request"
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
