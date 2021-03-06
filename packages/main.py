import json

from packages.slackapi import AuthenticatedSlackUser, SlackMessageService, ZoomCommand
from packages.utils import build_message
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

chat_message = []

keys = ['ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09']

ZOOM_BOT_ID = 'B0146050FC3'
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


class Token:
    value = ""


class ZoomMessage:
    body = None


zoom_message = ZoomMessage()


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
        if zoom_msg.botId in ZOOM_BOT_LIST:
            zoom_message.body = zoom_msg
        else:
            logging.info("this is not zoom message")
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
    key = request.headers.get('Query-Key')
    msg_type = request.args.get("type", "zoom")
    logging.info(f"key: {key}, keys:{keys}")

    if key not in keys:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"

    if msg_type == "zoom":
        return jsonify({"zoomMessage": zoom_message.body})
    elif msg_type == "text":
        return jsonify({"normalMessage": chat_message})
    else:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"


@app.route("/clean", methods=['GET', 'POST'])
def clean():
    key = request.headers.get('Query-Key')
    if key not in keys:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"

    zoom_message.body = None
    chat_message.clear()

    return jsonify({"message": zoom_message, "chat_message": chat_message})


@app.route("/updateSlackToken", methods=['POST', 'GET'])
def update_slack_token():
    Token.value = request.form.get("token")
    return jsonify({"token": Token.value})


@app.route("/querySlackToken", methods=['POST', 'GET'])
def querySlackToken():
    return jsonify({"token": Token.value})


@app.route("/sendMessage", methods=['POST', 'GET'])
def send_message():
    slack_user = request.json.get("slackAuthUser")
    extend = request.json.get("extend")
    command_type = request.json.get("command")

    print(slack_user)
    print("extend", extend)
    print("command", command_type)

    test_slack_user = AuthenticatedSlackUser(
        **slack_user
    )

    print(test_slack_user)
    authorization_user_bot = SlackMessageService(test_slack_user)

    if command_type == "zoom":
        resp = authorization_user_bot.send_command_to_channel("C011V2G61P1", ZoomCommand.Zoom)
        return jsonify(resp)
    elif command_type == "zoom_meeting_topic":
        resp = authorization_user_bot.send_command_to_channel("C011V2G61P1", ZoomCommand.ZoomMeetingTopic, topic=extend)
        return jsonify(resp)
    elif command_type == "zoom_join_me":
        resp = authorization_user_bot.send_command_to_channel("C011V2G61P1", ZoomCommand.ZoomJoinMe)
        return jsonify(resp)
    elif command_type == "zoom_join_meeting_id":
        resp = authorization_user_bot.send_command_to_channel("C011V2G61P1", ZoomCommand.ZoomJoinMeetingId,
                                                              meeting_id=extend)
        return jsonify(resp)
